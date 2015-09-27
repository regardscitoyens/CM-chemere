#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests

BAN_URL = "http://api-adresse.data.gouv.fr/search"


def geocode(address):
    response = requests.get(BAN_URL + '?q=' + address)

    for feature in response.json()['features']:
        if feature['properties']['score'] > 0.8:
            return feature

if __name__ == '__main__':
    print geocode(sys.argv[1])
