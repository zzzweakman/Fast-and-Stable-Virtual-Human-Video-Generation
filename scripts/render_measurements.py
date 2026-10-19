"""Render the current repeated-measurement release as a static accessible page."""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = 'h200-results-2026-10-19'
SURVEY = 'survey-measured-v4.pdf'
PROTOCOL = 'h200-measurement-notes-v4.md'
MANIFEST = 'data/snapshots/measured-v4/manifest.json'
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
    mode = 'Retained' if row['model_mode'] == 'resident_models_or_worker' else 'Reloaded'
    frames = str(row['frames']) if row['frames'] is not None else ' / '.join(map(str, row['frames_per_repeat']))
    values = [mode, frames, f'{row["output_width"]} × {row["output_height"]}']
    values += [number(row[k]) for k in ('pre_s', 'generation_s', 'post_s', 'load_s')]
    values += [f'{row["call_s"]:.2f} ± {row["call_sd_s"]:.2f}']
    values += [number(row[k]) for k in ('measured_nvml_peak_gib', 'suite_process_s')]
    return (f'<tr data-method="{ESC(row["method"], quote=True)}" data-config="{ESC(row["config_id"], quote=True)}" data-status="measured">'
            f'<th scope="row">{heading}</th>' + ''.join(f'<td>{v}</td>' for v in values) + '</tr>')


def render(data):
    groups = []
    for route, title in GROUPS:
        rows = [r for r in data['rows'] if r['route'] == route]
        context = ('UniLS predicts motion and exports a FLAME visualization. Native visual-AR coverage is zero. '
                   'DyStream and Talker-T2AV remain under Render-based because their renderers own appearance.'
                   if route == 'motion' else 'Implementation-specific demo workloads; stage contents and model-residency modes differ.')
        if route == 'diffusion':
            context += ' Twenty configurations cover 19 methods, including separate FlashHead Lite and Pro results.'
        groups.append(f'''<section class="result-group" id="{route}" aria-labelledby="{route}-title">
<h2 id="{route}-title">{title}</h2><p class="result-group-note">{context}</p>
<div class="results-scroll" role="region" aria-label="{title} measurement table; scroll horizontally for all columns" tabindex="0">
<table class="results-table"><caption>{title}: {len(rows)} configurations. Times are measured-call means in seconds; ± is sample SD over three calls. Warm peak is the maximum sampled memory across those calls after three complete warm-ups, in GiB.</caption>
<thead><tr><th scope="col">Configuration</th><th scope="col">Models</th><th scope="col">Frames</th><th scope="col">Output<br><span>W × H</span></th><th scope="col">Pre<br><span>s</span></th><th scope="col">Gen<br><span>s</span></th><th scope="col">Post<br><span>s</span></th><th scope="col">Load/call<br><span>s</span></th><th scope="col">Call ± SD<br><span>s</span></th><th scope="col">Warm peak<br><span>GiB · after 3 warm-ups</span></th><th scope="col">Suite total<br><span>s · all 6 calls</span></th></tr></thead>
<tbody>{''.join(row_html(r) for r in rows)}</tbody></table></div></section>''')
    configs = ''.join(
        f'<dt>{ESC(NAMES.get(r["method"], r["method"]))}</dt><dd><p>{ESC(r["input_configuration"])}</p>'
        f'<p>{ESC(r["stage_definition"])}</p><p>Attention: {ESC(r["attention_backend"])}. {ESC(r["attention_evidence"])}</p></dd>'
        for r in data['rows'])
    nav = ''.join(f'<a href="#{key}">{title}</a>' for key, title in GROUPS)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#193e35"><meta name="description" content="Repeated single-H200 runtime and memory measurements: 56 configurations, 55 methods, three warm-ups and three measured calls each.">
<title>Runtime &amp; memory — Fast &amp; Stable</title><link rel="canonical" href="https://zzzweakman.github.io/Fast-and-Stable-Virtual-Human-Video-Generation/measurements.html">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"></head>
<body class="results-page"><a class="skip-link" href="#results">Skip to measured results</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html">Fast <span class="brand-amp">&amp;</span> Stable</a><a class="results-back" href="index.html#literature">Back to the literature</a></div></header>
<main class="container results-main" id="results">
<div class="results-intro"><h1>Runtime and memory.</h1><p class="results-lead">{data['published_results']} configurations. {data['methods']} methods. One H200 per configuration.</p>
<p>Three complete warm-ups followed by three measured calls in the same interpreter. All 336 calls are available.</p>
<p>Fifteen configurations retain audited models or a GPU worker; 41 reload models each call. Different inputs, settings and residency modes make these configuration-specific observations. They do not form a controlled quality or speed ranking.</p>
<div class="results-downloads"><a class="button button-primary" href="data/{DATA}.csv" download>Summary CSV</a><a class="button button-outline" href="data/{DATA}.json" download>Full JSON</a><a class="button button-outline" href="data/h200-trials-2026-10-19.csv" download>All 336 calls</a><a class="results-protocol-link" href="#protocol">Read the protocol</a></div>
<p class="results-pending-note"><strong>Call and suite are different clocks.</strong> Call reports the measured request. Suite total includes setup, all three warm-ups, all three measured calls, output checks and shutdown. Neither is time to first frame.</p>
<p class="results-pending-note"><strong>Main tables report warmed memory.</strong> Each value is the maximum sampled peak over the three measured calls and includes preparation, generation and output processing.</p></div>
<nav class="result-jump-links" aria-label="Result groups">{nav}</nav>
<p class="results-scroll-hint">Scroll each table horizontally to see all columns. Retained means audited model objects or the neural worker remain resident; clip state is rebuilt. NR means no recorded value, not zero. Stage SDs and per-call values are in the downloads.</p>
{''.join(groups)}
<section class="result-protocol" id="protocol" aria-labelledby="protocol-title"><h2 id="protocol-title">How to read the measurements</h2>
<dl><dt>Repeatability and hardware</dt><dd>Three full warm-ups, then three measured calls per configuration, using one H200 across three nodes. Every call repeats its selected clip and writes fresh output. Four CPU-affinity identifiers and numerical-library thread limits of four do not imply four independent physical cores. Host memory, storage and caches remain shared.</dd>
<dt>Output workload</dt><dd>Dimensions show generated regions or paste-back canvases, excluding comparison panels. Internal face crops may be smaller. Wan retains the actual final frame counts 35 / 33 / 34; their mean is not substituted. Talker-T2AV resets seed 42 at the generation boundary and produces 136 frames in all six calls. No common seed is imposed across methods.</dd>
<dt>Stages and Call</dt><dd>Pre, Gen and Post use implementation-specific synchronized event boundaries. VAE decoding is generally in Post for dense diffusion; controller plus renderer are generally in Gen for appearance reuse. Call includes per-call loading, native validation and unclassified overhead. Ditto and Talk Like You overlap phases, so stage sums are not elapsed time. SyncTalk has native validation inside Call, outside Pre/Gen/Post. Generic output QA is outside Call.</dd>
<dt>Suite total</dt><dd>The complete 3+3 process includes startup/import, setup, all six calls, output QA and shutdown. This replaces the old fresh-process interpretation and must not be divided by six to estimate measured-call latency. The first measured call is already after three warm-ups.</dd>
<dt>Memory measurement</dt><dd>Own-process/worker NVML samples are collected approximately every 100 ms. Warm peak is the maximum of the three measured-window peaks after warm-up. Sampling may miss brief allocations; framework counters do not cover every CUDA allocator.</dd>
<dt>Model and input state</dt><dd>Same interpreter does not mean every model stays resident. StyleAvatar retains neural objects while rebuilding FaceVerse state; Wan retains its actual GPU worker. Precomputed tracking, features, masks and subject-trained assets remain prerequisites where the demo expects them. First calls may reuse disk caches.</dd>
<dt>Metadata and evidence</dt><dd>No new attention capture accompanies these timed runs. The original 46 labels are historical execution observations; the ten new labels are source/configuration inspections. Package versions and Git heads are post-run inventories. Full sampling/decoder settings for six additional configurations were not supplied.</dd>
<dt>Interpretation limits</dt><dd>The delivery contains a workbook and README; referenced server-side traces, adapters, separate JSON and videos were not provided for independent inspection. All reported means, sample SDs, memory maxima, phase unions and frame sequences were reconciled with the workbook's 336 calls. Basic output validity checks do not measure visual quality. Repeated short clips do not establish TTFF, sustained service or long-session stability.</dd></dl>
<details class="result-configurations"><summary>Input settings, stage boundaries and attention evidence</summary><dl>{configs}</dl></details>
<p><a href="data/{PROTOCOL}">Download the full protocol</a> · <a href="assets/survey/{SURVEY}">Read the updated survey</a> · <a href="{MANIFEST}">Release manifest</a> · <a href="data/h200-results-2026-10-16.json">Archived single-run results</a></p></section>
</main><footer class="container results-footer"><p>Repeated-call runtime and memory measurements.</p><a href="https://github.com/zzzweakman/Fast-and-Stable-Virtual-Human-Video-Generation">View data and source on GitHub</a></footer>
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
