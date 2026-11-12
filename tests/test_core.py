import unittest
from radioatlas.core import search
class CoreTests(unittest.TestCase):
    def setUp(self):
        self.data=[{'state':'RJ','mode':'DMR','city':'Rio de Janeiro'}, {'state':'SP','mode':'FM','city':'São Paulo'}]
    def test_filter_by_state(self):
        self.assertEqual(len(search(self.data,state='rj')),1)
    def test_filter_by_city(self):
        self.assertEqual(search(self.data,city='SÃO')[0]['state'],'SP')

    def test_export_csv_with_filters(self):
        import tempfile, csv
        from pathlib import Path
        from radioatlas.core import export_csv
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'export.csv'
            export_csv(search(self.data,state='RJ'),target)
            with target.open(encoding='utf-8',newline='') as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['state'],'RJ')
    def test_export_escapes_spreadsheet_formulas(self):
        import tempfile, csv
        from pathlib import Path
        from radioatlas.core import export_csv
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'export.csv'
            export_csv([{'id':'demo','city':'=1+2','state':'RJ','mode':'DMR'}],target)
            with target.open(encoding='utf-8',newline='') as f:
                row=next(csv.DictReader(f))
            self.assertEqual(row['city'], "'=1+2")
