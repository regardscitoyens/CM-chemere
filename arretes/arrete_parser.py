#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json

from bs4 import BeautifulSoup, NavigableString
from utils import extract_date

re_html = re.compile(r'<[^>]*>')
re_nbsp = re.compile(r'\s*&(#160|nbsp);\s*')
re_assemble_lines = re.compile(r'([^>])\n\s*')
clean_html = lambda x: re_html.sub('', re_assemble_lines.sub(r'\1 ', re_nbsp.sub(' ', x.replace('&amp;', '&'))))

re_numero_arrete = re.compile(ur'ARRETE MUNICIPAL n°(.+)')
re_references = re.compile(ur'Vu (?:la|le|les|l\’)(.+)')
re_articles = re.compile(ur'Article \d+ (?:–|-)\s*(.+)')
re_date = re.compile(ur'le (\d+ \w+ \d+)')
re_end = re.compile(ur'Fait à')


def parse_arrete(filename):
    with open(filename, 'r') as input:
        soup = BeautifulSoup(input.read().decode('utf-8'))

        prev_article = None

        data = {'refs': [], 'articles': []}

        for tag in soup.findAll(['p']):
            line = tag.text.replace('\n', ' ').strip()

            if not line:
                continue

            if re_end.search(line) and not re_date.search(line):
                continue

            if re_end.search(line) and re_date.search(line):
                data['date'] = extract_date(line)
                break

            numero = re_numero_arrete.search(line)
            if numero:
                data['numero'] = numero.group(1).strip()
                continue

            reference = re_references.search(line)
            if reference:
                data['refs'].append(line[:-1])
                continue

            current_article = re_articles.search(line)

            if current_article:
                data['articles'].append(line)
                prev_article = current_article
                continue

            if prev_article:
                data['articles'][-1] += ' ' + line

        return data


if __name__ == '__main__':
    print json.dumps(parse_arrete(sys.argv[1]), ensure_ascii=False).encode('utf-8')
