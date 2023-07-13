from django.test import TestCase
from .lib import dotplot
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