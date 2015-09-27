#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import csv

all_data = []

writer = csv.writer(open('umap.csv', 'w'))
writer.write(['lat', 'lon', 'numero', 'date', ''])

for arg in sys.argv[1:]:
    data = json.load(open(arg, 'r'), encoding='utf-8')

    if data['meta']['streets']:
        import pdb
        pdb.set_trace()

