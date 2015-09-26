#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, pprint

with open(sys.argv[1], 'r') as PV:
    text = PV.read().decode('utf-8')

data = {'date': '', 'heure': '', 'heure_fin': '', 'date_convocation': '', 'date_affichage': '', 'session' : '', 'president': '', 'presents': [], 'excuses': [], 'absents': [], 'secretaire': '', 'ODJ': '', 'deliberations': []}

re_html = re.compile(r'<[^>]*>')
re_nbsp = re.compile(r'\s*&(#160|nbsp);\s*')
re_assemble_lines = re.compile(r'([^>])\n\s*')
clean_html = lambda x: re_html.sub('', re_assemble_lines.sub(r'\1 ', re_nbsp.sub(' ', x.replace('&amp;', '&'))))

months={'janvier': '01', 'fevrier': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06', 'juillet': '07', 'aout': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'decembre': '12'}
def convert_month(text):
    month = text.lower().strip().replace(u'É', 'e').replace(u'é', 'e').replace(u'û', 'u').replace(u'Û', 'u')
    if month in months:
        return months[month]
    return text

re_split = re.compile(r"([ \-'])")
def lowerize(text):
    res = ""
    for a in re_split.split(text):
        if len(a) < 2:
            res += a
        else:
            res += a[0]+a[1:].lower().replace(u'É', u'é').replace(u'È', u'è').replace(u'À', u'à').replace(u'Î', u'î').replace(u'Ï', u'ï').replace(u'Ô', u'ô').replace(u'Ù', u'ù').replace(u'Û', u'û').replace(u'Ü', u'ü')
    return res.strip()

re_clean_parent = re.compile(r'\s*\([^)]+\)')
def handle_elus(text, field):
    for elu in text.split(u','):
        elu = re_clean_parent.sub('', elu)
        nom = lowerize(elu.strip())
        if nom not in data[field]:
            data[field].append(nom)

nohtml = clean_html(text)

#print >> sys.stderr, nohtml
#print >> sys.stderr, text

re_seance = re.compile(ur'S[EÉ]ANCE DU (\d+)[eErR]* *([\wéû]+) *(\d{4})')
re_date = re.compile(ur'(\d+)[eErR]* *([\wéû]+) *(\d{4})')
#re_heure = re.compile(r"L'an [^,]+, le [^,]+, [àAÀ]\s*(\d+) *H\w* *(\d+)?", re.I)
re_affichage = re.compile(ur"Date d’affichage", re.I)
re_convoc = re.compile(r'Convocation\s*:', re.I)
re_presents = re.compile(ur'Pr(?:e|é|É)sents\s*:', re.I)
re_absents = re.compile(ur'Absents? (non-* *)?excus(?:e|é|É)s? *:', re.I)
re_secretaire = re.compile(ur'secrétaire de séance *: *M[ME\. ]* +(.+)', re.I)
re_conseillers = re.compile(ur'^(?:M(?:\.|MES?) )*(.+?)(, (Maire|Adjoints?|Conseill(?:e|è)re?s? municipa(le?s?|ux)( déléguée?s?)?|pouvoir donné à [^,]+))+', re.I)

read = ""
for line in nohtml.split('\n'):
    line = line.strip()
    if not line:
        continue
    if len(sys.argv) > 3:
        print >> sys.stderr, "TEST %s: %s" % (read, line)
#    heure = re_heure.search(line)
#    if heure:
#        mins = 0
#        if heure.group(2):
#            mins = int(heure.group(2))
#        data['heure'] = "%02d:%02d" % (int(heure.group(1)), mins)
#        continue
    seance = re_seance.search(line)
    abse = re_absents.match(line)
    if seance:
        data['date'] = "%04d-%s-%02d" % (int(seance.group(3)), convert_month(seance.group(2)), int(seance.group(1)))
    elif re_affichage.match(line):
        read = "date_affichage"
    elif re_convoc.match(line):
        read = "date_convocation"
    elif re_presents.match(line):
        print >> sys.stderr, line
        read = "presents"
    elif abse:
        if abse.group(1):
            read = 'absents'
        else: read = 'excuses'
    elif read.startswith("date_"):
        dateconv = re_date.search(line)
        data[read] = "%04d-%s-%02d" % (int(dateconv.group(3)), convert_month(dateconv.group(2)), int(dateconv.group(1)))
        read = ""
    elif read:
        conseil = re_conseillers.search(line)
        if conseil:
            print >> sys.stderr, "FOUND:", read, conseil.group(1)
            handle_elus(conseil.group(1), read)
        else:
            print >> sys.stderr, "WEIRD:", read, line
            read = ""
    secretaire = re_secretaire.search(line)
    if secretaire:
        data['secretaire'] = lowerize(secretaire.group(1))

for abse in data['absents'] + data['excuses']:
    if abse in data['presents']:
        data['presents'].remove(abse)

if len(sys.argv) > 2:
    pprint.pprint(data)
else:
    for a in data['presents']:
        print "%s,%s,%s,%s" % (data['date'],data['heure'],data['convocation'],a)
