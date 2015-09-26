#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

months = {'janvier': '01', 'fevrier': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06', 'juillet': '07', 'aout': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'decembre': '12'}

re_date = re.compile(ur'(\d+)[eErR]* *([\wéû]+) *(\d{4})')


def extract_date(line):
    dateconv = re_date.search(line)
    return "%04d-%s-%02d" % (int(dateconv.group(3)), convert_month(dateconv.group(2)), int(dateconv.group(1)))


def convert_month(text):
    month = text.lower().strip().replace(u'É', 'e').replace(u'é', 'e').replace(u'û', 'u').replace(u'Û', 'u')
    if month in months:
        return months[month]
    return text
