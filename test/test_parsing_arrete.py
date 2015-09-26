# -*- coding: utf-8 -*-

import unittest2

from arrete_parser import parse_arrete


class ArreteParsingTest(unittest2.TestCase):

    def setUp(self):
        self.maxDiff = 10000

    def arrete_2010(self):
        data = parse_arrete("html/Arrete 2010-11.html")

        expected_result = {
            'numero': u'2010/11',
            'refs': [
                u'Vu le Code général des collectivités territoriales, et notamment son article L 2122-18, qui confère le pouvoir au maire d’une commune de déléguer une partie de ses fonctions à un ou plusieurs adjoints et à des membres du Conseil municipal',
                u'Vu la délibération n°2009/160 du Conseil municipal en date du 15 décembre 2009 fixant le nombre d’adjoints à quatre et élisant Mademoiselle Alice BICZYSKO comme conseillère municipale déléguée à l’environnement',
                u'Vu la délibération n°2009/161 du Conseil municipal en date du 15 décembre 2009 instituant une indemnité de fonction aux conseillers municipaux délégués'
            ],
            'articles': [
                u'Article 1 –  A compter du 15 décembre 2009, Mademoiselle Alice BICZYSKO, Conseillère municipale, est déléguée, sous ma surveillance et ma responsabilité, pour intervenir dans le domaine suivant : Environnement. Dans ce domaine, elle assumera les fonctions suivantes : Etude et suivi des dossiers, Elaboration des dossiers.'
            ]
        }

        self.assertEquals(u'2010-01-28', data['date'])
        self.assertEquals(expected_result['numero'], data['numero'])
        self.assertEquals(expected_result['refs'], data['refs'])
        self.assertEquals(expected_result['articles'][0], data['articles'][0])

    def test_arrete_2013(self):
        data = parse_arrete("html/Arrete 2015-1.html")

        self.assertEquals('2015/1', data['numero'])
        self.assertEquals('2015-01-12', data['date'])
        self.assertEquals(len(data['refs']), 10)
        self.assertEquals(len(data['articles']), 7)



if __name__ == '__main__':
    unittest2.main()