"""Render the current repeated-measurement release as a static accessible page."""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = 'h200-results-v10'
TRIALS = 'h200-trials-v10.csv'
SURVEY = 'survey-measured-v10.pdf'
SOURCE = 'virtual-human-survey-measured-v10.zip'
PROTOCOL = 'h200-measurement-notes-v10.md'
MANIFEST = 'data/snapshots/measured-v10/manifest.json'
BENCHMARKS = 'benchmark-results-v10.json'
EVIDENCE = 'h200-output-evidence-v1.json'
GROUPS = [('gan', 'GAN-based'), ('diffusion', 'Diffusion-based'), ('render', 'Render-based'), ('motion', 'Motion visualization')]
NAMES = {'Wav2Lip-GAN': 'Wav2Lip+GAN', 'LiveSpeechPortraits': 'Live Speech Portraits',
         'AvatarForcing-SlidingWindow': 'AvatarForcing-SW', 'TalkLikeYou': 'Talk Like You',
         'First-Order-Motion-Model': 'FOMM', 'TPS-Motion-Model': 'TPS Motion Model',
         'LiveAvatar': 'Live Avatar', 'LipForcing': 'Lip Forcing'}
ESC = html.escape


def number(value):
    if value is None:
        return 'NR'
    if 0 < value < 0.005:
        return '&lt;0.01'
    return f'{value:.2f}'


def row_html(row):
    name = NAMES.get(row['method'], row['method'])
    url = 'https://arxiv.org/abs/' + row['arxiv_id']
    heading = f'<a href="{ESC(url, quote=True)}" target="_blank" rel="noopener noreferrer">{ESC(name)}</a>'
    if row['model_mode'] == 'resident_models_or_worker':
        heading += '<sup title="Models retained between calls">R</sup>'
    frames = str(row['frames']) if row['frames'] is not None else ' / '.join(map(str, row['frames_per_repeat']))
    attention = ESC(row['attention_label'])
    if row['attention_source_only']:
        attention += '<sup title="Source/configuration inspection">S</sup>'
    values = [str(row['publication_year']), frames, f'{row["output_width"]} × {row["output_height"]}', attention]
    values += [number(row[k]) for k in ('pre_s', 'generation_s', 'post_s', 'first_load_s')]
    values += [f'{row["call_s"]:.2f} ± {row["call_sd_s"]:.2f}']
    values += [number(row['measured_nvml_peak_gib'])]
    return (f'<tr data-method="{ESC(row["method"], quote=True)}" data-config="{ESC(row["config_id"], quote=True)}" data-status="measured">'
            f'<th scope="row">{heading}</th>' + ''.join(f'<td>{v}</td>' for v in values) + '</tr>')


def benchmark_sections(benchmarks):
    sections = []
    definitions = [
        ('hdtf', 'HDTF quality', ['Configuration', 'Year', 'Route', 'Sync-C ↑', 'Sync-D ↓', 'ID ↑', 'FID ↓', 'FVD ↓'],
         ('sync_c', 'sync_d', 'identity', 'fid', 'fvd'), 4),
        ('streameval', 'StreamEval avatar performance', ['Model', 'Quality ↑', 'Stability ↑', 'Following ↑', 'Identity ↑'],
         ('quality', 'stability', 'following', 'identity'), 2),
    ]
    for key, title, headings, metrics, decimals in definitions:
        group = benchmarks[key]
        rows = []
        for row in group['rows']:
            cells = [str(row['year']), ESC(row['route'])] if key == 'hdtf' else []
            cells += [f'{row[m]:.{decimals}f}' for m in metrics]
            rows.append(f'<tr data-benchmark="{key}" data-method="{ESC(row["method"], quote=True)}"><th scope="row">{ESC(row["method"])}</th>'
                        + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')
        scope = ('23 configurations on 40 fifteen-second HDTF cases (920 generated videos).'
                 if key == 'hdtf' else 'Six configurations on a 20% subset of StreamEval avatar performance. Scores range from 0 to 100.')
        judge = f'<p>{ESC(group["judges"])}</p>' if key == 'streameval' else ''
        sections.append(f'''<section class="result-group" id="{key}" aria-labelledby="{key}-title">
<h2 id="{key}-title">{title}</h2><p class="result-group-note">{scope}</p>
<div class="results-scroll" role="region" aria-label="{title} table; scroll horizontally for all columns" tabindex="0">
<table class="results-table"><caption>{title}: values and column order match the survey.</caption>
<thead><tr>{''.join(f'<th scope="col">{label}</th>' for label in headings)}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p>{ESC(group['protocol'])}</p>{judge}<p>{ESC(group['limits'])}</p>
<p><a href="data/{key}-results-v10.csv" download>Download {title} CSV</a> · <a href="data/{BENCHMARKS}" download>Benchmark JSON</a></p></section>''')
    return '\n'.join(sections)


def render(data, benchmarks=None):
    if benchmarks is None:
        benchmarks = json.loads((ROOT / 'data' / BENCHMARKS).read_text())
    groups = []
    for route, title in GROUPS:
        rows = [r for r in data['rows'] if r['route'] == route]
        context = ('UniLS predicts motion and exports a FLAME visualization. Native visual-AR coverage is zero. '
                   'DyStream and Talker-T2AV remain under Render-based because their renderers own appearance.'
                   if route == 'motion' else 'Implementation-specific demo workloads; stage contents and model-residency modes differ.')
        if route == 'diffusion':
            context += ' All included diffusion configurations reload models each call.'
        groups.append(f'''<section class="result-group" id="{route}" aria-labelledby="{route}-title">
<h2 id="{route}-title">{title}</h2><p class="result-group-note">{context}</p>
<div class="results-scroll" role="region" aria-label="{title} measurement table; scroll horizontally for all columns" tabindex="0">
<table class="results-table"><caption>{title}: {len(rows)} configurations. Times in seconds. Load₁: first invocation. Other times: means of three warmed calls. ±: sample SD. Warm peak: measured-call maximum (GiB).</caption>
<thead><tr><th scope="col">Configuration</th><th scope="col">Year</th><th scope="col">Frames</th><th scope="col">Output<br><span>W × H</span></th><th scope="col">Attn.</th><th scope="col">Pre<br><span>s</span></th><th scope="col">Gen<br><span>s</span></th><th scope="col">Post<br><span>s</span></th><th scope="col">Load<sub>1</sub><br><span>s · first call</span></th><th scope="col">Call ± SD<br><span>s</span></th><th scope="col">Warm peak<br><span>GiB · after 3 warm-ups</span></th></tr></thead>
<tbody>{''.join(row_html(r) for r in rows)}</tbody></table></div></section>''')
    configs = ''.join(
        f'<dt>{ESC(NAMES.get(r["method"], r["method"]))}</dt><dd><p>{ESC(r["input_configuration"])}</p>'
        f'<p>{ESC(r["stage_definition"])}</p><p>Attention: {ESC(r["attention_backend"])}. {ESC(r["attention_evidence"])}</p></dd>'
        for r in data['rows'])
    nav = ''.join(f'<a href="#{key}">{title}</a>' for key, title in [*GROUPS, ('hdtf', 'HDTF'), ('streameval', 'StreamEval')])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#193e35"><meta name="description" content="Runtime and memory measurements, HDTF quality results, and StreamEval avatar performance aligned with the survey.">
<title>Measured results | Fast &amp; Stable</title><link rel="canonical" href="https://zzzweakman.github.io/Fast-and-Stable-Virtual-Human-Video-Generation/measurements.html">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"></head>
<body class="results-page"><a class="skip-link" href="#results">Skip to measured results</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html">Fast <span class="brand-amp">&amp;</span> Stable</a><a class="results-back" href="index.html#literature">Back to the literature</a></div></header>
<main class="container results-main" id="results">
<div class="results-intro"><h1>Measured results.</h1><p class="results-lead">Runtime, HDTF quality, and StreamEval avatar performance.</p>
<p>The runtime suite covers {data['published_results']} configurations and {data['methods']} methods, using one H200 per configuration.</p>
<p>The tables include configurations with recorded first-call loading and all reported timing and memory fields. Three complete warm-ups precede three measured calls in the same interpreter: 306 included calls.</p>
<p>Ten configurations retain audited models; 41 reload models each call. Inputs, settings and residency differ, so these results describe implementations under their stated workloads.</p>
<div class="results-downloads"><a class="button button-primary" href="data/{DATA}.csv" download>Summary CSV</a><a class="button button-outline" href="data/{DATA}.json" download>Full JSON</a><a class="button button-outline" href="data/{TRIALS}" download>Included 306 calls</a><a class="results-protocol-link" href="#protocol">Read the protocol</a></div>
<p class="results-pending-note"><strong>Load₁ reports the first invocation.</strong> It comes from <code>warmup_01</code>, before any previous full warm-up. Pre, Gen, Post and Call summarize the three later measured calls. Load₁ cannot be added to those means to obtain a measured total.</p>
<p class="results-pending-note"><strong>Call and suite are different clocks.</strong> Call reports the measured request. Suite total includes setup, all three warm-ups, all three measured calls, output checks and shutdown. Neither is time to first frame.</p>
<p class="results-pending-note"><strong>Main tables report warmed memory.</strong> Each value is the maximum sampled peak over the three measured calls and includes loading, pre-processing, generation and output processing.</p></div>
<nav class="result-jump-links" aria-label="Result groups">{nav}</nav>
<p class="results-scroll-hint">Scroll tables horizontally to see all columns. R marks retained models. Attn. lists attention backends: FA2/FA3, FlashAttention 2/3; xF, xFormers; SDPA-m/e/f/c, math/memory-efficient/flash/cuDNN paths. S marks source-inspected labels. Eager means no fused attention API was reported. Individual calls and stage statistics remain in the downloads.</p>
{''.join(groups)}
{benchmark_sections(benchmarks)}
<section class="result-protocol" id="protocol" aria-labelledby="protocol-title"><h2 id="protocol-title">How to read the measurements</h2>
<dl><dt>Repeatability and hardware</dt><dd>Three full warm-ups, then three measured calls per configuration, using one H200 across three nodes. Every call repeats its selected clip and writes fresh output. Four CPU-affinity identifiers and numerical-library thread limits of four do not imply four independent physical cores. Host memory, storage and caches remain shared.</dd>
<dt>Selection and archive</dt><dd>The displayed 51 configurations have all table metrics recorded. Five configurations without an initial loading interval are excluded. The <a href="data/h200-results-2026-10-19.json">original 56-configuration archive</a> and <a href="data/h200-trials-2026-10-19.csv">all 336 calls</a> remain available.</dd>
<dt>Output workload</dt><dd>Dimensions show generated regions or paste-back canvases, excluding comparison panels. Internal face crops may be smaller. Talker-T2AV resets seed 42 at the generation boundary and produces 136 frames in all six calls. No common seed is imposed across methods.</dd>
<dt>Initial loading and warmed stages</dt><dd>Load₁ is one observation from the first recorded invocation, <code>warmup_01</code>; disk caches may already be populated. Pre, Gen and Post use implementation-specific synchronized event boundaries. VAE decoding is generally in Post for dense diffusion; controller plus renderer are generally in Gen for appearance reuse. Warmed Call includes any loading performed in that call, native validation and unclassified overhead. Ditto and Talk Like You overlap phases, so stage sums are not elapsed time. SyncTalk has native validation inside Call, outside Pre/Gen/Post. Generic output QA is outside Call.</dd>
<dt>Suite total</dt><dd>The complete 3+3 process includes startup/import, setup, all six calls, output QA and shutdown. This replaces the old fresh-process interpretation and must not be divided by six to estimate measured-call latency. The first measured call is already after three warm-ups.</dd>
<dt>Memory measurement</dt><dd>Own-process/worker NVML samples are collected approximately every 100 ms. Warm peak is the maximum of the three measured-window peaks after warm-up. Sampling may miss brief allocations; framework counters do not cover every CUDA allocator.</dd>
<dt>Model and input state</dt><dd>Unless stated otherwise, inputs follow the demo recommended in the official open-source README. Wav2Lip+GAN uses the EDTalk pair, and FOMM uses the TPS Motion Model pair. Third-party implementations use their supplied demos. Ten configurations retain models; 41 reload each call. Precomputed tracking, features, masks and subject-trained assets remain prerequisites where required. LAM performs fresh FLAME tracking.</dd>
<dt>Metadata and evidence</dt><dd>No new attention capture accompanies these timed runs. Labels for 44 included implementations are historical execution observations; seven use source/configuration inspections. Package versions and Git heads are post-run inventories. Archived launch records supplement six configurations; unrecorded sampler and decoder defaults remain unspecified.</dd>
<dt>Archived outputs and paper figures</dt><dd>The updated survey includes compact runtime tables, HDTF and StreamEval results, and a stage-cost figure derived from first-call timings. The 306 included runtime calls retain their original records. Earlier output crops and their <a href="data/{EVIDENCE}">provenance</a> remain archived.</dd>
<dt>Interpretation limits</dt><dd>Initial loads, measured means, sample SDs, memory maxima, phase unions and frame sequences were reconciled with the corresponding records. Adapter source, model weights and complete environments were not included in the archive. Output checks do not measure perceptual quality. Different workloads and repeated short clips do not establish a controlled ranking, TTFF, sustained service or long-session stability.</dd></dl>
<details class="result-configurations"><summary>Input settings, stage boundaries and attention evidence</summary><dl>{configs}</dl></details>
<p><a href="data/{PROTOCOL}">Download the full protocol</a> · <a href="assets/survey/{SURVEY}">Read the updated survey</a> · <a href="assets/survey/{SOURCE}">Clean source package</a> · <a href="{MANIFEST}">Release manifest</a> · <a href="data/h200-results-2026-10-16.json">Archived single-run results</a></p></section>
</main><footer class="container results-footer"><p>Runtime, HDTF quality, and StreamEval measurements.</p><a href="https://github.com/zzzweakman/Fast-and-Stable-Virtual-Human-Video-Generation">View data and source on GitHub</a></footer>
</body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists(), args.output
    data = json.loads((ROOT / 'data' / f'{DATA}.json').read_text())
    args.output.write_text(render(data) + '\n')
    print('Generated', args.output)


if __name__ == '__main__':
    main()
