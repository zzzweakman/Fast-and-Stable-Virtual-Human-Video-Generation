"""Check repeated results, raw calls, readable tables and downloadable formats."""
from collections import Counter
from pathlib import Path
import csv
import json
import math
import statistics

from export_measurements import NUMERIC, csv_cell
from render_measurements import DATA, SURVEY, render

ROOT = Path(__file__).resolve().parents[1]


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-8, abs_tol=1e-8), (a, b)


def validate_measurements():
    data = json.loads((ROOT / 'data' / f'{DATA}.json').read_text())
    rows = data['rows']
    assert len(rows) == data['published_results'] == 56
    assert len({r['config_id'] for r in rows}) == 56
    assert len({r['method_family'] for r in rows}) == data['methods'] == 55
    assert data['pending_results'] == 0 and all(r['status'] == 'measured' for r in rows)
    assert Counter(r['route'] for r in rows) == {'gan': 11, 'diffusion': 20, 'render': 24, 'motion': 1}
    assert Counter(r['model_mode'] for r in rows) == {'resident_models_or_worker': 15, 'reload_each_call': 41}
    trials = []
    for row in rows:
        assert row['warmup_calls'] == row['measured_calls'] == 3
        for key in NUMERIC:
            value = row[key]
            if value is None:
                assert key in ('frames', 'duration_s', 'load_s', 'load_sd_s'), (row['method'], key)
            else:
                assert isinstance(value, (int, float)) and math.isfinite(value) and value >= -1e-8
        for field, kind in [('warmup_iterations', 'warmup'), ('measured_iterations', 'measured')]:
            group = row[field]
            assert len(group) == 3 and [t['repeat'] for t in group] == [1, 2, 3]
            assert all(t['kind'] == kind and t['config_id'] == row['config_id'] for t in group)
            for t in group:
                close(t['pre_s'] + t['generation_s'] + t['post_s'] - t['stage_union_s'], t['stage_overlap_s'])
                assert t['stage_union_s'] <= t['call_s'] + 1e-8
            trials += group
        measured = row['measured_iterations']
        frame_values = [t['frames'] for t in measured]
        assert row['frames_per_repeat'] == frame_values
        assert row['frames'] == (frame_values[0] if len(set(frame_values)) == 1 else None)
        for key, summary in row['statistics'].items():
            values = [t[key] for t in measured]
            assert summary['values'] == values
            if any(v is None for v in values):
                assert row[key] is summary['mean'] is summary['sample_sd'] is None
            else:
                close(row[key], statistics.mean(values))
                close(row[key.replace('_s', '_sd_s')], statistics.stdev(values))
                close(summary['median'], statistics.median(values))
        close(row['measured_nvml_peak_gib'], max(t['nvml_peak_gib'] for t in measured))
        close(row['first_warmup_nvml_peak_gib'], row['warmup_iterations'][0]['nvml_peak_gib'])
        assert row['suite_nvml_peak_gib'] >= max(t['nvml_peak_gib'] for t in row['warmup_iterations'] + measured) - 1e-8
        assert row['suite_process_s'] >= sum(t['call_s'] for t in row['warmup_iterations'] + measured)
    assert len(trials) == 336
    assert Counter(t['kind'] for t in trials) == {'warmup': data['warmup_calls'], 'measured': data['measured_calls']} == {'warmup': 168, 'measured': 168}
    flat = [{k: v for k, v in r.items() if k not in ('statistics', 'measured_iterations', 'warmup_iterations')} for r in rows]
    for file, expected in [(f'{DATA}.csv', flat), ('h200-trials-2026-10-19.csv', trials)]:
        with (ROOT / 'data' / file).open(newline='') as stream:
            actual = list(csv.DictReader(stream))
        assert actual == [{k: csv_cell(v) for k, v in r.items()} for r in expected], file
    page = (ROOT / 'measurements.html').read_text()
    assert page == render(data) + '\n', 'Generated result page is stale'
    assert page.count('data-status="measured"') == 56
    assert '35 / 33 / 34' in page and 'Suite total' in page and 'Call ± SD' in page
    assert 'Warm peak' in page and 'id="memory-diagnostics"' not in page
    assert 'awaiting measurement' not in page.lower()
    index = (ROOT / 'index.html').read_text()
    assert '56 configurations' in index and '55 methods' in index
    for text in [json.dumps(data, ensure_ascii=False), page]:
        assert all(token not in text for token in ('/aiboxian/', '/bxai/', 'VR-boxian-dev', 'Mao-dev-', 'GPU-')), 'Private machine identifiers in public export'
    assert (ROOT / 'assets/survey' / SURVEY).read_bytes().startswith(b'%PDF')
    print('Validated 56 configurations, 336 calls, means/sample SDs, memory windows, HTML and CSV/JSON.')
    return data


if __name__ == '__main__':
    validate_measurements()
