#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import csv

all_data = []

writer = csv.writer(open('companies.csv', 'w'))
writer.writerow(['numero', 'date', 'company', 'type'])

for arg in sys.argv[1:]:
    data = json.load(open(arg, 'r'), encoding='utf-8')

    if data['meta']['companies']:
        for companie in data['meta']['companies']:
            writer.writerow([data['date'], data['numero'], companie['nom'], companie['type']])

