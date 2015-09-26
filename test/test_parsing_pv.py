# -*- coding: utf-8 -*-

import unittest2

from parse_PV import parse_PV


class PVParsingTest(unittest2.TestCase):

    def setUp(self):
        self.maxDiff = 10000

    def pv_2008(self):
        data = parse_PV(open('html/CM 28 mars 2007.html').read().decode('utf-8'))

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

    def test_pv_2014(self):
        data = parse_PV(open('html/CM 16 décembre 2014.html').read().decode('utf-8'))

        presents = [
            u'Georges Lecleve',
            u'Virginie Porcher',
            u'Michel Gravouil',
            u'Marie-Laure David',
            u'Gérard Chauvet',
            u'Jean-Marc Voyau',
            u'Jacques Chevalier',
            u'Romain Rungoat',
            u'Sabrina Pennetier-Bigot',
            u'Anthony Latouche',
            u'Sylviane Gibet',
            u'Anne Bruneteau',
            u'Philippe Briand',
            u'Christelle Guignon',
            u'Dominique Muslewski',
            u'Nicolas Boucher',
            u'Tatiana Berthelot',
            u'Thierry Favreau'
        ]

        self.assertEquals(presents, data['presents'])

    def test_pv_2015(self):
        data = parse_PV(open('html/CM 15 septembre 2015.html').read().decode('utf-8'))

        presents = [
            u'Georges Lecleve',
            u'Virginie Porcher',
            u'Michel Gravouil',
            u'Marie-Laure David',
            u'Gérard Chauvet',
            u'Jean-Marc Voyau',
            u'Jacques Chevalier',
            u'Karine Fouquet',
            u'Romain Rungoat',
            u'Sabrina Pennetier-Bigot',
            u'Anthony Latouche',
            u'Sylviane Gibet',
            u'Anne Bruneteau',
            u'Philippe Briand',
            u'Christelle Guignon',
            u'Dominique Muslewski'
        ]

        self.assertEquals(presents, data['presents'])
        self.assertEquals([u'Nicolas Boucher', u'Tatiana Berthelot', u'Thierry Favreau'], data['excuses'])
        self.assertEquals(u'19:30', data['heure_debut'])
        self.assertEquals(u'22:40', data['heure_fin'])
        self.assertEquals(u'Philippe Briand', data['secretaire'])
        self.assertEquals(u'2015-09-15', data['date'])
        self.assertEquals(u'2015-09-09', data['date_convocation'])
        self.assertEquals(u'2015-09-21', data['date_affichage'])

if __name__ == '__main__':
    unittest2.main()