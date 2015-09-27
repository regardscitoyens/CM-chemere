#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import re

def load_streetnames():
    renames = []
    with open('voies.txt', 'r') as input:
        for line in input.readlines():
            str = ur'(\w+ '+line.strip()+')'
            renames.append(re.compile(str, re.I))
    return renames



def find_pio_from_streetnames(filename):
    with open(filename, 'r') as input:
        data = json.load(input, encoding='utf-8')

        print data['articles']
        
        re_streetnames = load_streetnames()
        
        for article in data['articles']:
            for p in re_streetnames:
                m = p.search(article)
                if (m):
                    print m.group()

def find_streets(filename):
    return find_pio_from_streetnames(filename)
                
if __name__ == '__main__':
    print json.dumps(find_streets(sys.argv[1]), ensure_ascii=False).encode('utf-8')
