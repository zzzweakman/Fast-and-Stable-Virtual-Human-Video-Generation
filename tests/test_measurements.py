"""Public data must never expose provisional values through another format."""
from pathlib import Path
import sys, unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from export_measurements import export_rows, NUMERIC, CONTEXT
from validate_measurements import validate_measurements

class PublicMeasurementTests(unittest.TestCase):
    def test_provisional_values_and_context_are_withheld_at_export(self):
        source=[dict(method=name,route='gan',cite_key='test',arxiv_id='2008.10010',**{k:123.456 for k in NUMERIC},**{k:'private configuration' for k in CONTEXT},extra='not for export') for name in ['MuseTalk','VideoReTalking']]
        exported=export_rows(source)
        self.assertEqual(len(exported),5)
        for row in exported:
            self.assertTrue(all(row[k] is None for k in (*NUMERIC,*CONTEXT)))
            self.assertNotIn('extra',row)

    def test_public_artifacts_agree_and_missing_values_are_blank(self):
        validate_measurements()

if __name__=='__main__': unittest.main()
