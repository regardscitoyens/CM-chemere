#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json


def find_streets(filename):
    with open(filename, 'r') as input:
        for line in input.readlines():
            line.strip()

        data = json.load(input, encoding='utf-8')

        for article in data['articles']:
            pass

if __name__ == '__main__':
    print json.dumps(find_streets(sys.argv[1]), ensure_ascii=False).encode('utf-8')
