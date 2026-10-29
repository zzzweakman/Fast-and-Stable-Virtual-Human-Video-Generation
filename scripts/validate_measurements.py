"""Check repeated results, raw calls, readable tables and downloadable formats."""
from collections import Counter
from pathlib import Path
import csv
import json
import math
import statistics
import zipfile

from export_measurements import NUMERIC, attention_labels, csv_cell
from export_benchmarks import hdtf_rows, streaming_rows
from render_measurements import BENCHMARKS, DATA, TRIALS, SURVEY, SOURCE, render

ROOT = Path(__file__).resolve().parents[1]


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-8, abs_tol=1e-8), (a, b)


def validate_measurements():
    data = json.loads((ROOT / 'data' / f'{DATA}.json').read_text())
    rows = data['rows']
    assert len(rows) == data['published_results'] == 51
    assert len({r['config_id'] for r in rows}) == 51
    assert len({r['method_family'] for r in rows}) == data['methods'] == 51
    assert data['pending_results'] == 0 and all(r['status'] == 'measured' for r in rows)
    assert Counter(r['route'] for r in rows) == {'gan': 11, 'diffusion': 16, 'render': 23, 'motion': 1}
    assert Counter(r['model_mode'] for r in rows) == {'resident_models_or_worker': 10, 'reload_each_call': 41}
    archived = json.loads((ROOT / 'data' / data['source_archive']).read_text())['rows']
    assert len(archived) == data['archive_configurations'] == 56
    expected_ids = {r['config_id'] for r in archived if r['warmup_iterations'][0]['load_s'] is not None}
    assert {r['config_id'] for r in rows} == expected_ids
    assert set(data['selection']['excluded_config_ids']) == {r['config_id'] for r in archived} - expected_ids
    archived_by_id = {r['config_id']: r for r in archived}
    trials = []
    for row in rows:
        assert row['warmup_calls'] == row['measured_calls'] == 3
        assert 'load_s' not in row and 'load_sd_s' not in row
        assert isinstance(row['publication_year'], int) and 1900 <= row['publication_year'] <= 2026
        close(row['first_load_s'], row['warmup_iterations'][0]['load_s'])
        assert math.isfinite(row['first_load_s']) and row['first_load_s'] >= 0
        for key in (k for k in NUMERIC if k not in ('load_s', 'load_sd_s')):
            value = row[key]
            assert isinstance(value, (int, float)) and math.isfinite(value) and value >= -1e-8
            assert value == archived_by_id[row['config_id']][key]
        for field, kind in [('warmup_iterations', 'warmup'), ('measured_iterations', 'measured')]:
            group = row[field]
            assert group == archived_by_id[row['config_id']][field], 'Archived call values changed'
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
                assert key == 'load_s' and summary['mean'] is summary['sample_sd'] is None
            else:
                close(summary['mean'], statistics.mean(values))
                close(summary['sample_sd'], statistics.stdev(values))
                if key != 'load_s':
                    close(row[key], summary['mean'])
                    close(row[key.replace('_s', '_sd_s')], summary['sample_sd'])
                close(summary['median'], statistics.median(values))
        close(row['measured_nvml_peak_gib'], max(t['nvml_peak_gib'] for t in measured))
        close(row['first_warmup_nvml_peak_gib'], row['warmup_iterations'][0]['nvml_peak_gib'])
        assert row['suite_nvml_peak_gib'] >= max(t['nvml_peak_gib'] for t in row['warmup_iterations'] + measured) - 1e-8
        assert row['suite_process_s'] >= sum(t['call_s'] for t in row['warmup_iterations'] + measured)
    assert len(trials) == 306
    assert Counter(t['kind'] for t in trials) == {'warmup': data['warmup_calls'], 'measured': data['measured_calls']} == {'warmup': 153, 'measured': 153}
    flat = [{k: v for k, v in r.items() if k not in ('statistics', 'measured_iterations', 'warmup_iterations')} for r in rows]
    for file, expected in [(f'{DATA}.csv', flat), (TRIALS, trials)]:
        with (ROOT / 'data' / file).open(newline='') as stream:
            actual = list(csv.DictReader(stream))
        assert actual == [{k: csv_cell(v) for k, v in r.items()} for r in expected], file
    page = (ROOT / 'measurements.html').read_text()
    assert page == render(data) + '\n', 'Generated result page is stale'
    assert page.count('data-status="measured"') == 51
    assert 'Suite total' in page and 'Call ± SD' in page and 'Load<sub>1</sub>' in page
    assert '<td>NR</td>' not in page and 'Load/call' not in page
    assert 'Warm peak' in page and 'id="memory-diagnostics"' not in page
    assert 'awaiting measurement' not in page.lower()
    index = (ROOT / 'index.html').read_text()
    assert '51 configurations' in index and '51 methods' in index
    for text in [json.dumps(data, ensure_ascii=False), page]:
        assert all(token not in text for token in ('/aiboxian/', '/bxai/', 'VR-boxian-dev', 'Mao-dev-', 'GPU-')), 'Private machine identifiers in public export'
    assert (ROOT / 'assets/survey' / SURVEY).read_bytes().startswith(b'%PDF')
    benchmarks = json.loads((ROOT / 'data' / BENCHMARKS).read_text())
    with zipfile.ZipFile(ROOT / 'assets/survey' / SOURCE) as archive:
        manuscript = zipfile.Path(archive) / benchmarks['manuscript_revision']
        attention = attention_labels(manuscript)
        assert sum(r['attention_source_only'] for r in rows) == 7
        for row in rows:
            assert {k: row[k] for k in ('attention_label', 'attention_source_only')} == attention[row['cite_key']]
        for key, filename, parse, count in [
            ('hdtf', 'measured_hdtf_quality.tex', hdtf_rows, 23),
            ('streameval', 'measured_streaming_subset20.tex', streaming_rows, 6),
        ]:
            group = benchmarks[key]
            assert len(group['rows']) == group['configurations'] == count
            assert group['rows'] == parse((manuscript / 'tables' / filename).read_text()), f'{key}: manuscript and website differ'
            with (ROOT / 'data' / f'{key}-results-v11.csv').open(newline='') as stream:
                actual = list(csv.DictReader(stream))
            assert actual == [{k: str(v) for k, v in r.items()} for r in group['rows']], f'{key}: CSV and JSON differ'
            assert page.count(f'data-benchmark="{key}"') == count
    assert all(set(row) == {'method', 'quality', 'stability', 'following', 'identity'} for row in benchmarks['streameval']['rows'])
    print('Validated 51 runtime configurations, 306 calls, 23 HDTF rows, six StreamEval rows, and agreement with the downloadable manuscript.')
    return data


if __name__ == '__main__':
    validate_measurements()
