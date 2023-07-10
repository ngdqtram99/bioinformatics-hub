from django.test import TestCase
import lib.dotplot
import lib.simple_search
import unittest

class TestDotplot(unittest.TestCase):
    
    def test_get_result(self):
        res1 = [[' ','A','T','A','C'],
                ['A',1,0,1,0],
                ['C',0,0,0,1],
                ['C',0,0,0,1],
                ['A',1,0,1,0]]
        self.assertEqual(lib.dotplot.get_result('ATAC','ACCA'),res1) 




# algorithm tests
class TestAlgorithm(unittest.TestCase):
    def test_comparsions_count(self):
        # one comparsions
        # no results
        result = lib.simple_search.get_result('T', 'A')

        self.assertEquals(result['comparsions_count'], 1)
        self.assertEquals(result['results'], [])

        # one result
        result = lib.simple_search.get_result('A', 'A')

        self.assertEquals(result['comparsions_count'], 1)
        self.assertEquals(result['results'], [0])

        # multiple comparsions
        # no results
        result = lib.simple_search.get_result('UA', 'ACGUCAC')

        self.assertEquals(result['comparsions_count'], 7)
        self.assertEquals(result['results'], [])

        # one result
        result = lib.simple_search.get_result('UA', 'ACGUUAC')

        self.assertEquals(result['comparsions_count'], 8)
        self.assertEquals(result['results'], [4])

        # multiple results
        result = lib.simple_search.get_result('UA', 'AUACGUUAUA')

        self.assertEquals(result['comparsions_count'], 13)
        self.assertEquals(result['results'], [1, 6, 8])


    def test_no_result(self):
        # Sequence to short
        result = lib.simple_search.get_result('ACA', 'U')

        self.assertEquals(result['comparsions_count'], 0)
        self.assertEquals(result['results'], [])

        # Pattern not in Sequence
        result = lib.simple_search.get_result('U', 'ACA')

        self.assertEquals(result['comparsions_count'], 3)
        self.assertEquals(result['results'], [])





if __name__ == '__main__':
     unittest.main()