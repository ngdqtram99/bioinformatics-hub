from django.test import TestCase
import lib.dotplot
import unittest

class TestDotplot(unittest.TestCase):
    
    def test_get_result(self):
        res1 = [[',','A','T','A','C'],
                ['A',1,0,1,0],
                ['C',0,0,0,1],
                ['C',0,0,0,1],
                ['A',1,0,1,0]]
        self.assertEqual(lib.dotplot.get_result('ATAC','ACCA'),res1) 


if __name__ == '__main__':
     unittest.main()