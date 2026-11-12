import unittest
from radioatlas.core import search
class CoreTests(unittest.TestCase):
    def setUp(self):
        self.data=[{'state':'RJ','mode':'DMR','city':'Rio de Janeiro'}, {'state':'SP','mode':'FM','city':'São Paulo'}]
    def test_filter_by_state(self):
        self.assertEqual(len(search(self.data,state='rj')),1)
    def test_filter_by_city(self):
        self.assertEqual(search(self.data,city='SÃO')[0]['state'],'SP')
