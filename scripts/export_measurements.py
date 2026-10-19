"""Export the verified 19 October repeated-call measurements for publication."""
from pathlib import Path
import argparse
import csv
import json

RELEASE = '2026-10-19'
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
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    rows = export_rows(json.loads(args.input.read_text()))
    assert len(rows) == 56 and len({r['method_family'] for r in rows}) == 55
    args.output_dir.mkdir(parents=True, exist_ok=False)
    data = {
        'release': RELEASE, 'measured_at': RELEASE,
        'published_results': 56, 'methods': 55, 'pending_results': 0,
        'warmup_calls': 168, 'measured_calls': 168,
        'hardware': {
            'gpu_per_configuration': 'one NVIDIA H200',
            'host_scope': 'Three nodes; shared host memory, storage and caches.',
            'cpu_scope': 'Four CPU-affinity identifiers per configuration; numerical-library thread limits of four. Identifiers do not establish four independent physical cores.'
        },
        'protocol': {
            'trials': 'Three complete warm-ups then three measured calls, sequentially in the same interpreter; output and clip state recreated for every call. Timing summaries use measured calls only; sample SD uses n-1.',
            'residency': '15 configurations retain audited model objects or the GPU worker; 41 reload models every call while retaining interpreter/kernel caches.',
            'timing': 'Implementation-specific synchronized stage unions. Call spans inference entry to synchronized return; it includes per-call loading, native validation and unclassified overhead. Generic output QA follows Call.',
            'suite_time': 'suite_process_s covers the entire 3+3 process, including setup, warm-ups, measured calls, QA and shutdown. It is neither single-call latency nor TTFF; do not divide by six to estimate measured latency.',
            'memory': 'Approximately 100-ms own-process/worker NVML sampling. measured_nvml_peak_gib is the maximum of three measured-window peaks; first_warmup_nvml_peak_gib is the first call; suite_nvml_peak_gib includes setup, all calls and QA.',
            'inputs': 'Unmatched demo inputs, lengths, dimensions, sampling, precision, offloading and precomputed prerequisites. Wan final encoded frames are 35/33/34. Talker-T2AV resets generation seed 42 and produces 136 frames in every call.',
            'metadata': 'No current-run attention capture. Original 46 labels are historical execution observations (15 October); new labels are source/configuration inspections. Package versions and Git heads are post-run inventories.',
            'limits': 'No matched quality, TTFF, delivery jitter or continuous-session drift evaluation. Three short repetitions do not establish sustained service. First-call peaks may greatly exceed warmed peaks.',
            'missing': 'Null/empty means unavailable, not zero. Wan frames is null because its three actual values differ; frames_per_repeat preserves them. Full sampling/decoder settings for six additional configurations are absent.',
            'provenance': 'Workbook and README supplied; 336 calls and aggregate statistics reconciled. Referenced separate JSON, server-side adapters/traces and videos were not delivered for independent inspection.'
        },
        'rows': rows
    }
    (args.output_dir / f'h200-results-{RELEASE}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    write_csv(args.output_dir / f'h200-results-{RELEASE}.csv',
              [{k: v for k, v in r.items() if k not in ('statistics', 'measured_iterations', 'warmup_iterations')} for r in rows])
    trials = [t for row in rows for kind in ('warmup_iterations', 'measured_iterations') for t in row[kind]]
    write_csv(args.output_dir / f'h200-trials-{RELEASE}.csv', trials)
    print('Exported 56 configurations, 55 methods and 336 individual calls.')


if __name__ == '__main__':
    main()
