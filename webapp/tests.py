from django.test import TestCase
from webapp.lib.simple_search import get_result


# algorithm tests
class TestAlgorithm(TestCase):
    def test_comparsions_count(self):
        # one comparsions
        # no results
        result = get_result('T', 'A')

        self.assertEquals(result['comparsions_count'], 1)
        self.assertEquals(result['results'], [])

        # one result
        result = get_result('A', 'A')

        self.assertEquals(result['comparsions_count'], 1)
        self.assertEquals(result['results'], [0])

        # multiple comparsions
        # no results
        result = get_result('UA', 'ACGUCAC')

        self.assertEquals(result['comparsions_count'], 7)
        self.assertEquals(result['results'], [])

        # one result
        result = get_result('UA', 'ACGUUAC')

        self.assertEquals(result['comparsions_count'], 8)
        self.assertEquals(result['results'], [4])

        # multiple results
        result = get_result('UA', 'AUACGUUAUA')

        self.assertEquals(result['comparsions_count'], 13)
        self.assertEquals(result['results'], [1, 6, 8])


    def test_no_result(self):
        # Sequence to short
        result = get_result('ACA', 'U')

        self.assertEquals(result['comparsions_count'], 0)
        self.assertEquals(result['results'], [])

        # Pattern not in Sequence
        result = get_result('U', 'ACA')

        self.assertEquals(result['comparsions_count'], 3)
        self.assertEquals(result['results'], [])




