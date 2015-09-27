#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
# - data conseillers
# - ODJ
# - delibs

import re, sys, json
from pprint import pprint

re_nbsp = re.compile(r'\s*&(#160|nbsp);\s*')
re_assemble_lines = re.compile(r'([^>:])\n\s*')
re_clean_secretaire = re.compile(ur'(secrétaire de séance.*:)\s*\n\s*', re.I|re.M)
re_clean_presents = re.compile(ur'(M[MLES,\. ]+)(?:<[^>]+>)+\s*\n\s*(?:<[^>]+>)+', re.M)
re_clean_presents2 = re.compile(ur'(M\.)([A-Z])', re.M)
re_html = re.compile(r'<[^>]*>')
re_spaces = re.compile(r' +')
clean_html = lambda x: re_spaces.sub(' ', re_html.sub('', re_clean_presents2.sub(r'\1 \2', re_clean_presents.sub(r'\1 ', re_clean_secretaire.sub(r'\1 ', re_assemble_lines.sub(r'\1 ', re_nbsp.sub(' ', x.replace('&amp;', '&'))))))))
clean_html_light = lambda x: re_spaces.sub(' ', re_html.sub('', re_nbsp.sub(' ', x.replace('&amp;', '&'))))

re_format_xml_like_html = re.compile(ur'(Convocation|Présents?|Pouvoirs? donn[^:]*|Absents?[^:]*)\s*:\s*')
re_format_xml_like_html2 = re.compile(ur'(Maire|Adjoints?|Conseill(?:e|è)re?s? municipa(le?s?|ux)( déléguée?s?)?)', re.I)
re_format_xml_like_html3 = re.compile(ur'(pouvoir (?:donné )?à(?: M(?:\.|[MmLl][Ee]))? .+?[A-Z]{3,})(?: M(?:\.|[MmLl][Ee]))? ([A-Z][a-zéè]+)')
re_parse_xml = re.compile(ur'^<text top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*)</text>$')
def clean_xml_from_pdf(text):
    text = text.replace(u'', '')
    result = ""
    lasttop = None
    lastleft = None
    lastfont = None
    for line in text.split("\n"):
        if not line.startswith('<text'):
            continue
        parsed = re_parse_xml.search(line)
        top = parsed.group(1)
        left = parsed.group(2)
        font = parsed.group(5)
        text = parsed.group(6)
        if text == u"er": continue # Skip misformatting of dates as 1er
        if lasttop and lastleft and lastfont is not None and top != lasttop and left != lastleft and font != lastfont:
            result += "\n"
        result += text
        lasttop = top
        lastleft = left
        lastfont = font
    return re_format_xml_like_html3.sub(r'\2', re_format_xml_like_html2.sub(r'\1\n', re_format_xml_like_html.sub(r'\n\1 :\n', clean_html_light(result))))

months = {'janvier': '01', 'fevrier': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06', 'juillet': '07', 'aout': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'decembre': '12'}
def convert_month(text):
    month = text.lower().strip().replace(u'É', 'e').replace(u'é', 'e').replace(u'û', 'u').replace(u'Û', 'u')
    if month in months:
        return months[month]
    return text

numbers = {
    "": 00,
    "dix": 10,
    "dix-huit": 18,
    "dix-neuf": 19,
    "vingt": 20,
    "vint-et-un": 21,
    "vingt-deux": 22,
    "vingt-trois": 22,
    "trente": 30
}
def numberize(text):
    try:
        return int(text)
    except:
        return numbers[text.replace(' ', '-')]

re_clean_mins = re.compile(r'\s*minutes?\s*$')
re_clean_hours = re.compile(r'\s*heures?\s*')
re_clean_hours2 = re.compile(r'(\d)h(\d)')
re_time = re.compile(ur'^(.+?)H(.*)$')
def clean_time(text):
    text = re_clean_hours2.sub(r"\1H\2", re_clean_hours.sub('H', re_clean_mins.sub('', text.lower().strip())))
    if text == "minuit":
        return "00:00"
    hourmins = re_time.search(text)
    if hourmins:
        return "%02d:%02d" % (numberize(hourmins.group(1)), numberize(hourmins.group(2)))
    return ""

re_split = re.compile(r"([ \-'])")
def lowerize(text):
    res = ""
    for a in re_split.split(text):
        if len(a) < 2:
            res += a
        else:
            res += a[0]+a[1:].lower().replace(u'É', u'é').replace(u'È', u'è').replace(u'À', u'à').replace(u'Î', u'î').replace(u'Ï', u'ï').replace(u'Ô', u'ô').replace(u'Ù', u'ù').replace(u'Û', u'û').replace(u'Ü', u'ü')
    return res.strip()

re_miss_commas = re.compile(ur'([A-Z][a-z]{3,}(-[A-Z][a-èz]+)? [A-Z]{3,}) ([A-Z][a-z]{3,}(-[A-Z][a-z]+)? [A-Z]{3,})')
def fix_missing_commas(text):
    if re_miss_commas.search(text):
        return re_miss_commas.sub(r'\1, \3', text)
    return text

re_clean_parent = re.compile(r'\s*\([^)]+\)')
def handle_elus(data, text, field):
    text = re_clean_parent.sub('', text)
    text = fix_missing_commas(text)
    for elu in text.replace('.', ',').split(u','):
        elu = elu.strip()
        if not elu or (field == 'excuses' and elu.lower().startswith(u"pouvoir ")):
            continue
        nom = re_clean_fonctions.sub('', lowerize(elu.strip()))
        nom = nom.replace(u"Marie-Josèphe ", u"Marie-Jo ")
        if nom not in data[field]:
            data[field].append(nom)

clear_alpha = re.compile(r'\D')

re_seance = re.compile(ur'(?:CONSEIL MUNICIPAL|S[EÉ]ANCE) DU (\d+)[eErR]* *([\wéû]+) *(\d{4})')
re_date = re.compile(ur'(\d+)[eErR]* *([\wéû]+) *(\d{4})')
re_header = re.compile(ur"L'an [^,]+, le [^,]+(, [àAÀ]\s*([^,]+))?, .*, sous la présidence de (Monsieur|Madame) *([^,\.]+)", re.I)
re_heurefin = re.compile(ur"Séance levée à *([^\.]+?)(\.|$)+", re.I)
re_affichage = re.compile(ur"Date d’affichage", re.I)
re_convoc = re.compile(ur'Convocation\s*:?$', re.I)
re_presents = re.compile(ur'Pr(?:e|é|É)sents\s*:', re.I)
re_absents = re.compile(ur'Absents? (non-* *)?(?:et *)?excus(?:e|é|É)s? *[^:]*:', re.I)
re_secretaire = re.compile(ur'secrétaire de séance *: *(.+)', re.I)
re_conseillers = re.compile(ur'^(?:M[MLES,\.]* )*(.+?)(, *(Maire|Adjoints?|Conseill(?:e|è)re?s? municipa(le?s?|ux)( déléguée?s?)?|pouvoir (?:donné )?à [^,]+))+', re.I)
re_conseillers2 = re.compile(ur'^(?:M[MLES,\.]* )+(.+?)\.?$', re.I)
re_clean_MMLE = re.compile(ur'^M(\.|[MLml][Ee])? +')
re_clean_fonctions = re.compile(ur'([, ]*(Maire|Adjoints?|Conseill(?:e|è)re?s? municipa(le?s?|ux)( déléguée?s?)?|pouvoir (?:donné )?à [^,]+))+', re.I)

def parse_PV(text, xml=False):
    data = {'date': '', 'heure_debut': '', 'heure_fin': '', 'date_convocation': '', 'date_affichage': '', 'president': '', 'presents': [], 'excuses': [], 'absents': [], 'secretaire': '', 'ODJ': '', 'deliberations': []}
    if xml:
        nohtml = clean_xml_from_pdf(text)
    else:
        nohtml = clean_html(text)
    read = ""
    data['total_presents'] = 0
    for line in nohtml.split('\n'):
        line = line.strip()
        if not line:
            continue
        if len(sys.argv) > 3:
            print >> sys.stderr, ("TEST %s: %s" % (read, line)).encode('utf-8')
        header = re_header.search(line)
        heurefin = re_heurefin.search(line)
        seance = re_seance.search(line)
        abse = re_absents.match(line)
        if header:
            if header.group(1):
                data['heure_debut'] = clean_time(header.group(2))
            data['president'] = lowerize(header.group(4))
        elif heurefin:
            data['heure_fin'] = clean_time(heurefin.group(1))
        elif seance:
            data['date'] = "%04d-%s-%02d" % (int(seance.group(3)), convert_month(seance.group(2)), int(seance.group(1)))
        elif re_affichage.match(line):
            read = "date_affichage"
        elif re_convoc.match(line):
            read = "date_convocation"
        elif re_presents.match(line):
            read = "presents"
            try:
                data['total_presents'] = int(clear_alpha.sub('', line))
            except: pass
        elif abse:
            if abse.group(1):
                read = 'absents'
            else: read = 'excuses'
        elif read.startswith("date_"):
            dateconv = re_date.search(line)
            try:
                data[read] = "%04d-%s-%02d" % (int(dateconv.group(3)), convert_month(dateconv.group(2)), int(dateconv.group(1)))
            except: pass
            read = ""
        elif read:
            conseil = re_conseillers.search(line)
            if conseil:
                handle_elus(data, conseil.group(1), read)
            else:
                conseil = re_conseillers2.search(line)
                if conseil:
                    handle_elus(data, conseil.group(1), read)
                else:
                    read = ""
        secretaire = re_secretaire.search(line)
        if secretaire:
            data['secretaire'] = lowerize(re_clean_MMLE.sub('', secretaire.group(1)).rstrip("."))

    for abse in data['absents'] + data['excuses']:
        if abse in data['presents']:
            data['presents'].remove(abse)
    return data

def test_data(data):
    errors = 0
    if not len(data['presents']):
        print >> sys.stderr, ("ERROR presents missing: %s, %s" % (data['total_presents'], data["presents"])).encode('utf-8')
        errors +=1
    for k, v in data.items():
        if k in ["absents", "presents", "excuses", "total_presents", "date_affichage", "heure_fin", "heure_debut"]: continue
        if k in ["ODJ", "deliberations"]: continue      # TO BE REMOVED WHEN PARSED
        if not v:
            print >> sys.stderr, ("ERROR field missing: %s" % k).encode('utf-8')
            errors +=1
    if errors:
        if len(sys.argv) > 2:
            pprint(data)
        sys.exit(1)

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'r') as PV:
        text = PV.read().decode('utf-8')
    data = parse_PV(text, xml=(filename.endswith('.xml')))
    test_data(data)
    if len(sys.argv) > 2:
        print json.dumps(data, indent=2)
    else:
        for a in data['presents']:
            print ("%s,%s,%s" % (data['date'], data['heure_debut'], a)).encode('utf-8')

