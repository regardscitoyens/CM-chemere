#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json


re_street_id = re.compile(ur'(\d+)?\s*(impasse|rue|rues|chemin|allée|allee|lotissement|place|route)\s([\w\s-]+)(?:,|et|\s-)', re.I)
re_lieu_dit = re.compile(ur'(lieu-dit|lieux-dits|lieudit)')


def find_poi_from_street_id(filename):
    with open(filename, 'r') as input:
        data = json.load(input, encoding='utf-8')

        for article in data['articles']:
            for group in re_street_id.findall(article):
                print data['numero'], group

if __name__ == '__main__':
    find_poi_from_street_id(sys.argv[1])
