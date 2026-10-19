"""Regression checks for the changed timing, memory and publication boundaries."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from export_measurements import export_rows
from validate_measurements import validate_measurements


class PublicMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads((ROOT / 'data/h200-results-2026-10-19.json').read_text())['rows']

    def test_export_omits_private_machine_fields(self):
        source = dict(self.rows[0], node='private-host', gpu_uuid='GPU-private', command='/private/input')
        source['measured_iterations'] = [dict(t, output_video='/private/video', iteration_file='/private/run') for t in source['measured_iterations']]
        public = export_rows([source])[0]
        self.assertNotIn('private', json.dumps(public))

    def test_variable_output_length_and_missing_load_remain_explicit(self):
        wan = next(r for r in self.rows if r['method'] == 'Wan-Animate-2')
        self.assertIsNone(wan['frames'])
        self.assertEqual(wan['frames_per_repeat'], [35, 33, 34])
        self.assertIsNone(wan['load_s'])
        self.assertGreater(wan['suite_process_s'], wan['call_s'] * 6)

    def test_completed_remeasurement_retains_first_call_peak(self):
        muse = next(r for r in self.rows if r['method'] == 'MuseTalk')
        self.assertEqual(muse['status'], 'measured')
        self.assertAlmostEqual(muse['measured_nvml_peak_gib'], 9.4921875)
        self.assertAlmostEqual(muse['first_warmup_nvml_peak_gib'], 137.849609375)
        self.assertEqual(muse['model_mode'], 'resident_models_or_worker')

    def test_public_artifacts_and_statistics_agree(self):
        validate_measurements()


if __name__ == '__main__':
    unittest.main()
