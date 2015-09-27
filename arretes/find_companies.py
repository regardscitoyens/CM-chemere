#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json
import re

re_personnes_morales = re.compile(ur'(sociétés?|entreprises?|associations?) ?([^,\.:]+)', re.I)
re_suppr_phrase = re.compile(ur'( est| sont| et| dès| chargé| à| \d| de | TP| SAG| SARL| agence| ouest| ouets).*', re.I)
re_exclude = re.compile(ur'(personne physique|\()')

def find_personnes_morales(filename):
    companies = []
    with open(filename, 'r') as input:
        data = json.load(input, encoding='utf-8')
        for article in data['articles']:        
            m = re_personnes_morales.search(article)
            if (m):
                companie = re_suppr_phrase.sub('', m.group(2))
                if not re_exclude.search(companie):
                    companies.append(companie)
    companies = list(set(companies))
    if (companies):
        print companies
    return companies

                
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print find_personnes_morales(arg)
