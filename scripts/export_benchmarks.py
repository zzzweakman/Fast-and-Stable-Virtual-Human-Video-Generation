"""Export the HDTF and StreamEval tables shown in the current manuscript."""
from pathlib import Path
import argparse
import csv
import json
import re

RELEASE = 'v10'
HDTF_METRICS = ('sync_c', 'sync_d', 'identity', 'fid', 'fvd')
STREAM_METRICS = ('quality', 'stability', 'following', 'identity')


def hdtf_rows(text):
    rows = []
    for line in text.splitlines():
        cells = [s.strip() for s in line.removesuffix(r'\\').split(' & ')]
        if len(cells) != 8 or r'\cite{' not in cells[0]:
            continue
        cite = re.search(r'\\cite\{([^}]+)\}', cells[0]).group(1)
        name = re.sub(r'~\\cite\{[^}]+\}', '', cells[0])
        rows.append(dict(method=name, cite_key=cite, year=int(cells[1]), route=cells[2],
                         **dict(zip(HDTF_METRICS, map(float, cells[3:])))))
    return rows


def streaming_rows(text):
    rows = []
    for line in text.splitlines():
        cells = [s.strip() for s in line.removesuffix(r'\\').split(' & ')]
        if len(cells) != 5 or cells[0] == 'Model':
            continue
        rows.append(dict(method=cells[0], **dict(zip(STREAM_METRICS, map(float, cells[1:])))))
    return rows


def write_csv(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manuscript-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    hdtf = hdtf_rows((args.manuscript_dir / 'tables/measured_hdtf_quality.tex').read_text())
    streaming = streaming_rows((args.manuscript_dir / 'tables/measured_streaming_subset20.tex').read_text())
    assert len(hdtf) == 23 and len(streaming) == 6
    result = {
        'release': RELEASE, 'manuscript_revision': args.manuscript_dir.name,
        'hdtf': {
            'configurations': 23, 'test_cases': 40, 'clip_seconds': 15, 'generated_videos': 920,
            'real_reference_clips': 20, 'display_decimals': 4,
            'protocol': 'Matched inputs from the Let Them Talk HDTF split. SyncNet uses 25 FPS without offset correction. Identity is raw ArcFace cosine similarity averaged over 16 temporal-bin midpoint frames per clip. FID and FVD use center-square full-frame clips.',
            'limits': 'Identity scores depend on preserved source pixels and pose variation. FID and FVD are sensitive to framing and the small reference pool. These measurements do not establish long-session stability.',
            'rows': hdtf,
        },
        'streameval': {
            'configurations': 6, 'condition_fraction': 0.2, 'repetitions': 3,
            'sessions_per_configuration': 36, 'sessions': 216, 'display_decimals': 2,
            'duration_strata_seconds': [15, 30, 60, 120, 300],
            'protocol': 'Avatar-performance subset with supplied portraits, incrementally released speech, and live visual directions. Average repetitions, then conditions within each duration stratum, then the five strata equally. Failures and unsupported controls remain in the denominator.',
            'judges': 'Local Qwen vision models replace the reference judges. Independent calibration has not been established.',
            'limits': 'The selected subset and local judges limit direct comparison with published StreamEval scores. Unresolved synchronization and its dependent aggregate scores are omitted. All tested configurations support custom portraits, so the fixed five-point customization bonus is also omitted.',
            'rows': streaming,
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / f'benchmark-results-{RELEASE}.json').write_text(json.dumps(result, indent=2) + '\n')
    write_csv(args.output_dir / f'hdtf-results-{RELEASE}.csv', hdtf)
    write_csv(args.output_dir / f'streameval-results-{RELEASE}.csv', streaming)
    print('Exported 23 HDTF configurations and six StreamEval configurations from manuscript tables.')


if __name__ == '__main__':
    main()
