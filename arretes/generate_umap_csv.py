#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import csv

all_data = []

with open('umap.csv', 'w') as output:
    writer = csv.writer(output)
    writer.writerow(['lat', 'lon', 'numero', 'date', 'titre'])

    for arg in sys.argv[1:]:
        print arg
        data = json.load(open(arg, 'r'), encoding='utf-8')

        if data['meta']['streets']:
            for street in data['meta']['streets']:
                writer.writerow([street['coordinates'][0], street['coordinates'][1], data['numero'], data.get('date', ''), data.get('titre', '').encode('utf-8')])