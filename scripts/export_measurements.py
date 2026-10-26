"""Export the manuscript subset with first-call loading and warmed statistics."""
from pathlib import Path
import argparse
import csv
import json
import re

RELEASE = 'v9'
SOURCE_RELEASE = '2026-10-19'
ROOT = Path(__file__).resolve().parents[1]
NUMERIC = ('frames', 'duration_s', 'output_width', 'output_height', 'encoded_width', 'encoded_height',
           'video_fps', 'pre_s', 'generation_s', 'post_s', 'load_s', 'call_s',
           'pre_sd_s', 'generation_sd_s', 'post_sd_s', 'load_sd_s', 'call_sd_s',
           'stage_union_s', 'stage_overlap_s', 'evaluation_s',
           'stage_union_sd_s', 'stage_overlap_sd_s', 'evaluation_sd_s',
           'measured_nvml_peak_gib', 'first_warmup_nvml_peak_gib', 'suite_nvml_peak_gib',
           'suite_process_s', 'torch_allocated_peak_gib', 'torch_reserved_peak_gib',
           'warmup_calls', 'measured_calls')
CONTEXT = ('config_id', 'method', 'method_family', 'route', 'cite_key', 'source_title', 'arxiv_id',
           'cohort', 'status', 'model_mode', 'input_configuration', 'stage_definition',
           'attention_backend', 'attention_evidence', 'code_commit_observed',
           'torch_version_observed', 'flash_attention_version_observed', 'xformers_version_observed',
           'metadata_observed_at', 'metadata_scope', 'implementation_status')
NESTED = ('frames_per_repeat', 'duration_s_per_repeat', 'statistics', 'measured_iterations', 'warmup_iterations')
TRIAL_FIELDS = ('config_id', 'kind', 'repeat', 'frames', 'video_fps', 'encoded_width', 'encoded_height',
                'pre_s', 'generation_s', 'post_s', 'load_s', 'call_s', 'nvml_peak_gib',
                'torch_allocated_peak_gib', 'torch_reserved_peak_gib', 'stage_union_s',
                'stage_overlap_s', 'evaluation_s')


def export_rows(source):
    """Allow only publication fields, including all six calls without server paths."""
    rows = []
    for row in source:
        public = {k: row.get(k) for k in (*CONTEXT, *NUMERIC, *NESTED)}
        for key in ('measured_iterations', 'warmup_iterations'):
            public[key] = [{k: t.get(k) for k in TRIAL_FIELDS} for t in row[key]]
        rows.append(public)
    return rows


def publication_years(manuscript):
    """Read the cited publication years from the manuscript's measured tables."""
    years = {}
    for path in (manuscript / 'tables').glob('measured_*.tex'):
        for key, year in re.findall(r'\\cite\{([^}]+)\}\s*&\s*(\d{4})\s*&', path.read_text()):
            assert key not in years or years[key] == int(year)
            years[key] = int(year)
    return years


def complete_rows(source, years, annotations=None):
    """Select complete table records without changing the archived trial values."""
    rows, excluded = [], []
    for row in export_rows(source):
        first = next(t for t in row['warmup_iterations'] if t['repeat'] == 1)
        if first['load_s'] is None:
            excluded.append(row['config_id'])
            continue
        for key in ('frames', 'output_width', 'output_height', 'pre_s', 'generation_s',
                    'post_s', 'call_s', 'call_sd_s', 'measured_nvml_peak_gib', 'suite_process_s'):
            assert row[key] is not None, (row['config_id'], key)
        row['first_load_s'] = first['load_s']
        row['publication_year'] = years[row['cite_key']]
        # Measured loading statistics remain in statistics and the individual
        # calls. Do not give them an ambiguous top-level Load column.
        del row['load_s'], row['load_sd_s']
        annotation = (annotations or {}).get(row['config_id'], {})
        for key in ('input_configuration', 'stage_definition'):
            if key in annotation:
                row[key] = annotation[key]
        rows.append(row)
    return rows, excluded


def csv_cell(value):
    if value is None:
        return ''
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    return str(value)


def write_csv(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows({k: csv_cell(v) for k, v in r.items()} for r in rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--manuscript-dir', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    if isinstance(source, dict):
        source = source['rows']
    annotations = json.loads((ROOT / 'data/h200-output-evidence-v1.json').read_text())['configuration_annotations']
    rows, excluded = complete_rows(source, publication_years(args.manuscript_dir), annotations)
    assert len(source) == 56 and len(rows) == 51 and len({r['method_family'] for r in rows}) == 51
    args.output_dir.mkdir(parents=True, exist_ok=False)
    data = {
        'release': RELEASE, 'measured_at': SOURCE_RELEASE,
        'published_results': 51, 'methods': 51, 'pending_results': 0,
        'warmup_calls': 153, 'measured_calls': 153,
        'source_archive': f'h200-results-{SOURCE_RELEASE}.json',
        'archive_configurations': 56, 'archive_calls': 336,
        'selection': {
            'criterion': 'Recorded first-call loading and all reported timing and memory fields.',
            'excluded_config_ids': excluded,
            'reason': 'No recorded loading interval in the first invocation.'
        },
        'hardware': {
            'gpu_per_configuration': 'one NVIDIA H200',
            'host_scope': 'Three nodes; shared host memory, storage and caches.',
            'cpu_scope': 'Four CPU-affinity identifiers per configuration; numerical-library thread limits of four. Identifiers do not establish four independent physical cores.'
        },
        'protocol': {
            'trials': 'Three complete warm-ups then three measured calls, sequentially in the same interpreter; output and clip state recreated for every call. Pre, Gen, Post and Call summarize the three measured calls; sample SD uses n-1.',
            'first_load': 'first_load_s is the loading interval in the first recorded invocation, warmup_01: one observation, with disk caches potentially already populated. It cannot be added to warmed stage means to obtain a measured total. statistics.load_s and trial load_s retain their per-call meanings.',
            'publication_year': 'Year of the cited publication, matching the current manuscript tables.',
            'residency': '10 configurations retain audited model objects; 41 reload models every call while retaining interpreter/kernel caches.',
            'timing': 'Implementation-specific synchronized stage unions. Call spans inference entry to synchronized return; it includes per-call loading, native validation and unclassified overhead. Generic output QA follows Call.',
            'suite_time': 'suite_process_s covers the entire 3+3 process, including setup, warm-ups, measured calls, QA and shutdown. It is neither single-call latency nor TTFF; do not divide by six to estimate measured latency.',
            'memory': 'Approximately 100-ms own-process/worker NVML sampling. measured_nvml_peak_gib is the maximum of three measured-window peaks; first_warmup_nvml_peak_gib is the first call; suite_nvml_peak_gib includes setup, all calls and QA.',
            'inputs': 'Unmatched demo inputs, lengths, dimensions, sampling, precision, offloading and precomputed prerequisites. Talker-T2AV resets generation seed 42 and produces 136 frames in every call.',
            'metadata': 'No current-run attention capture. Labels for 44 included implementations are historical execution observations; seven use source/configuration inspections. Package versions and Git heads are post-run inventories.',
            'limits': 'No matched quality, TTFF, delivery jitter or continuous-session drift evaluation. Three short repetitions do not establish sustained service.',
            'missing': 'The displayed subset has all table metrics. Null/empty fields elsewhere in the underlying records mean unavailable, not zero. Unrecorded sampler and decoder defaults for six configurations remain unspecified.',
            'provenance': 'The workbook is supported by archived JSON reports, iteration records, phase events, NVML samples and output videos. The 306 included calls and aggregate statistics were reconciled; original exports preserve all 336 calls. Adapter source, model weights and complete environments were not supplied.'
        },
        'rows': rows
    }
    (args.output_dir / f'h200-results-{RELEASE}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    write_csv(args.output_dir / f'h200-results-{RELEASE}.csv',
              [{k: v for k, v in r.items() if k not in ('statistics', 'measured_iterations', 'warmup_iterations')} for r in rows])
    trials = [t for row in rows for kind in ('warmup_iterations', 'measured_iterations') for t in row[kind]]
    write_csv(args.output_dir / f'h200-trials-{RELEASE}.csv', trials)
    print('Exported 51 configurations, 51 methods and 306 individual calls; five incomplete configurations remain in the original archive.')


if __name__ == '__main__':
    main()
