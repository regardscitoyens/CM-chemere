#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import csv

all_data = []

with open('umap.csv', 'w') as output:
    writer = csv.writer(output)
    writer.writerow(['lon', 'lat', 'nom', 'description'])

    for arg in sys.argv[1:]:
        print arg
        data = json.load(open(arg, 'r'), encoding='utf-8')

        nom = u'Arrêté n°' + data.get('numero', '')

        if 'date' in data:
            nom += ' du ' + data['date']

        if data['meta']['streets']:
            for street in data['meta']['streets']:
                writer.writerow([street['coordinates'][0], street['coordinates'][1], nom.encode('utf-8'), data.get('titre', '').encode('utf-8')])