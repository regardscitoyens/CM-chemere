# -*- coding: utf-8 -*-

import unittest2

from pv_parser import parse_pv


class PVParsingTest(unittest2.TestCase):

    def setUp(self):
        self.maxDiff = 10000

    def test_arrete_2010(self):
        data = parse_pv('html/CM 28 mars 2007.html')

        presents = [
            'M. MMES Sonia BAILLY',
            'Marie-Josèphe BATARD',
            'Gérard BIGOT',
            'Jacques CHEVALIER',
            'Régine CORMIER',
            'Louis-Marie DRONEAU',
            'Jean-Marie GATARD',
            'Michel GRAVOUIL',
            'Alain GUILBAUD',
            'Gérard GUILBAUD',
            'Jacques JAUNATRE',
            'Georges LECLEVE',
            'Jean-Paul LERAY',
            'Jean RONDEAU',
            'Pierre VOYAU'
        ]

        absents = ['M. MME Karine MOSNIER', 'Bernard PENNETIER']

        self.assertEquals(presents, data['presents'])
        self.assertEquals(absents, data['absents'])
        self.assertEquals('28 MARS 2007', data['date'])
        self.assertEquals('20 mars 2007', data['date_convocation'])
        self.assertEquals('MME Régine CORMIER', data['secretaire'])
        self.assertEquals('Jean-Paul LERAY', data['president'])
        #self.assertTrue(data['ODJ'].startswith('Monsieur le Maire donne lecture'))
        #self.assertTrue(data['ODJ'].endswith('Demande de subvention.'))
        #self.assertTrue(len(data['deliberations']) == )


if __name__ == '__main__':
    unittest2.main()