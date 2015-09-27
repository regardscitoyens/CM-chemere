#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json
import re

re_street_id = re.compile(ur'(\d+)?\s*(impasse|rue|rues|chemin|allée|allee|lotissement|place|route)\s([\w\s-]+)(?:,|et|\s-)', re.I)
re_lieu_dit = re.compile(ur'(lieu-dit|lieux-dits|lieudit)')

def load_streetnames():
    renames = []
    with open('voies.txt', 'r') as input:
        for line in input.readlines():
            str = ur'(\w+ '+line.strip()+')'
            renames.append(re.compile(str, re.I))
    return renames


def find_poi_from_streetnames(filename):
    with open(filename, 'r') as input:
        data = json.load(input, encoding='utf-8')

        re_streetnames = load_streetnames()

        streets = []
        
        for article in data['articles']:
            for p in re_streetnames:
                m = p.search(article)
                if (m):
                    streets.append(m.group())
    return streets
                    
def find_poi_from_street_id(filename):
    streets = []
    with open(filename, 'r') as input:
        data = json.load(input, encoding='utf-8')
        for article in data['articles']:        
            for group in re_street_id.findall(article):
                streets.append(' '.join(group).strip())
    return streets


def find_poi(filename):
    streets = []
    streets = find_poi_from_street_id(filename)
    if not streets:
        streets = find_poi_from_streetnames(filename)
    print streets
                
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        find_poi(arg)
