from django.test import TestCase
from .lib import dotplot
from .lib import simple_search
import unittest
from .forms import DotplotForm

class TestDotplot(TestCase):
    
    def test_get_result(self):
        # Fall 1: Sequenzen mit der gleichen Länge
        res1 = [[' ','A','T','A','C'],
                ['A',1,0,1,0],
                ['C',0,0,0,1],
                ['C',0,0,0,1],
                ['A',1,0,1,0]]
        self.assertEqual(dotplot.get_result('ATAC','ACCA'),res1) 

        # Fall 2: Sequenzen mit unterschiedlicher Längen
        res2 = [[' ','A','T','A','C'],
                ['A',1,0,1,0],
                ['C',0,0,0,1],
                ['C',0,0,0,1]]
        self.assertEqual(dotplot.get_result('ATAC','ACC'),res2)

        # Fall 3: Eine Sequenz fehlt
        res3 = [[' ','A','A','A','C']]
        self.assertEqual(dotplot.get_result('AAAC',''),res3) 

        res4 = [[' '],
                ['C'],
                ['C'],
                ['G']]
        self.assertEqual(dotplot.get_result('','CCG'),res4)

        # Fall 4: Keine Sequenzen
        res5 = [[' ']]
        self.assertEqual(dotplot.get_result('',''),res5)

class TestDotplotForm(TestCase):
    
    def test_latin_letters(self):
        form = DotplotForm(data = {'sequence1':'ATR-R', 'sequence2':'XX*WQ'})
        form.is_valid()
        self.assertEqual(form.errors['sequence1'], ['Nur lateinische Buchstaben sind erlaubt.'])
        self.assertEqual(form.errors['sequence2'], ['Nur lateinische Buchstaben sind erlaubt.'])




# Simple Search Tests
class TestSimpleSearch(unittest.TestCase):
    def test_comparsions_count(self):
        # one comparsions
        # no results
        result = simple_search.get_result('T', 'A')

        self.assertEquals(result['comparsions_count'], 1)
        self.assertEquals(result['results'], [])

        # one result
        result = simple_search.get_result('A', 'A')

        self.assertEquals(result['comparsions_count'], 1)
        self.assertEquals(result['results'], [0])

        # multiple comparsions
        # no results
        result = simple_search.get_result('UA', 'ACGUCAC')

        self.assertEquals(result['comparsions_count'], 7)
        self.assertEquals(result['results'], [])

        # one result
        result = simple_search.get_result('UA', 'ACGUUAC')

        self.assertEquals(result['comparsions_count'], 8)
        self.assertEquals(result['results'], [4])

        # multiple results
        result = simple_search.get_result('UA', 'AUACGUUAUA')

        self.assertEquals(result['comparsions_count'], 13)
        self.assertEquals(result['results'], [1, 6, 8])


    def test_no_result(self):
        # Sequence to short
        result = simple_search.get_result('ACA', 'U')

        self.assertEquals(result['comparsions_count'], 0)
        self.assertEquals(result['results'], [])

        # Pattern not in Sequence
        result = simple_search.get_result('U', 'ACA')

        self.assertEquals(result['comparsions_count'], 3)
        self.assertEquals(result['results'], [])