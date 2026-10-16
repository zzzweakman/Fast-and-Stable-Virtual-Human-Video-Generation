"""Generate a static, accessible reading page from the public measurement data.

Usage: python scripts/render_measurements.py --output /tmp/new-measurements.html
"""
from pathlib import Path
import argparse, html, json

ROOT=Path(__file__).resolve().parents[1]
DATA='h200-results-2026-10-16'
GROUPS=[('gan','GAN-based'),('diffusion','Diffusion-based'),('render','Render-based'),('motion','Motion visualization')]
NAMES={'Wav2Lip-GAN':'Wav2Lip+GAN','LiveSpeechPortraits':'Live Speech Portraits','AvatarForcing-SlidingWindow':'AvatarForcing-SW','TalkLikeYou':'Talk Like You'}
ESC=html.escape

def row_html(row):
    pending=row['status']!='measured'
    name=NAMES.get(row['method'],row['method'])
    url=row['repository'] or 'https://arxiv.org/abs/'+row['arxiv_id']
    name=f'<a href="{ESC(url,quote=True)}" target="_blank" rel="noopener noreferrer">{ESC(name)}</a>'
    status='Awaiting remeasurement' if row['status']=='pending_remeasurement' else 'Awaiting measurement'
    if pending: name+=f'<span class="result-status">{status}</span>'
    cells=[]
    for k in ['frames','resolution','pre_s','generation_s','post_s','load_s','process_s','nvml_peak_gib']:
        if pending: cell=f'<span class="sr-only">{status}</span>'
        elif k=='resolution': cell=f'{row["output_width"]} × {row["output_height"]}'
        elif k=='frames': cell=str(row[k])
        else: cell=f'{row[k]:.2f}'
        cells.append('<td>'+cell+'</td>')
    return f'<tr data-method="{ESC(row["method"],quote=True)}" data-status="{row["status"]}"><th scope="row">{name}</th>'+''.join(cells)+'</tr>'

def render(data):
    groups=[]
    for route,title in GROUPS:
        rows=[r for r in data['rows'] if r['route']==route]
        context='UniLS predicts motion and exports a FLAME visualization. This is not a native visual-AR or photorealistic appearance measurement.' if route=='motion' else 'Original demo inputs and implementation-specific processing stages.'
        groups.append(f'''<section class="result-group" id="{route}" aria-labelledby="{route}-title">
<h2 id="{route}-title">{title}</h2><p class="result-group-note">{context}</p>
<div class="results-scroll" role="region" aria-label="{title} measurement table; scroll horizontally for all columns" tabindex="0">
<table class="results-table"><caption>{title} results on one H200. Times in seconds; memory in GiB.</caption>
<thead><tr><th scope="col">Implementation</th><th scope="col">Frames</th><th scope="col">Output<br><span>W × H</span></th><th scope="col">Pre<br><span>s</span></th><th scope="col">Gen<br><span>s</span></th><th scope="col">Post<br><span>s</span></th><th scope="col">Load<br><span>s</span></th><th scope="col">Process<br><span>s</span></th><th scope="col">Memory<br><span>GiB</span></th></tr></thead>
<tbody>{''.join(row_html(r) for r in rows)}</tbody></table></div></section>''')
    configs=''.join(f'<dt>{ESC(NAMES.get(r["method"],r["method"]))}</dt><dd><p>{ESC(r["input_configuration"] or "")}</p><p>{ESC(r["stage_definition"] or "")}</p></dd>' for r in data['rows'] if r['status']=='measured')
    nav=''.join(f'<a href="#{key}">{title}</a>' for key,title in GROUPS)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#193e35"><meta name="description" content="Single-H200 runtime and sampled GPU-memory results for 44 open-source virtual-human implementations, with five pending entries.">
<title>Runtime &amp; memory — Fast &amp; Stable</title><link rel="canonical" href="https://zzzweakman.github.io/Fast-and-Stable-Virtual-Human-Video-Generation/measurements.html">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"></head>
<body class="results-page"><a class="skip-link" href="#results">Skip to measured results</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html">Fast <span class="brand-amp">&amp;</span> Stable</a><a class="results-back" href="index.html#literature">Back to the literature</a></div></header>
<main class="container results-main" id="results">
<div class="results-intro"><h1>Runtime and memory.</h1><p class="results-lead">{data['published_results']} implementation results on a single H200, with {data['pending_results']} entries awaiting measurement.</p>
<p>Measured on 15 October 2026. Each run records completed frames, output size, processing time, and sampled GPU memory. Inputs and software differ, so these results describe individual implementations rather than a method ranking.</p>
<div class="results-downloads"><a class="button button-primary" href="data/{DATA}.csv" download>Download CSV</a><a class="button button-outline" href="data/{DATA}.json" download>Download JSON</a><a class="results-protocol-link" href="#protocol">Read the protocol</a></div>
<p class="results-pending-note">MuseTalk, VideoReTalking, SoulX-LiveAct, SoulX-FlashTalk, and SoulX-FlashHead have blank result cells. Their downloadable fields are empty too.</p></div>
<nav class="result-jump-links" aria-label="Result groups">{nav}</nav>
<p class="results-scroll-hint">On smaller screens, scroll each table horizontally to see every column.</p>
{''.join(groups)}
<section class="result-protocol" id="protocol" aria-labelledby="protocol-title"><h2 id="protocol-title">How to read the measurements</h2>
<dl><dt>Hardware and repeatability</dt><dd>One H200 per run on a shared eight-GPU host. Up to eight workers use separate GPUs and CPU affinity sets, but share host memory and storage; NUMA locality varies. Each result is one measured run after a separate-process warm-up. Software, precision, compilation, and offloading differ.</dd>
<dt>Frames and output size</dt><dd>Frames count completed output across chunks. Dimensions describe the output region after cropping or paste-back, excluding comparison panels. A lip-editing canvas can be larger than the internal synthesized crop.</dd>
<dt>Pre, Gen, and Post</dt><dd>Stages follow each implementation. Gen usually covers denoising for dense diffusion or motion prediction plus rendering for appearance reuse. Dense-diffusion VAE decoding is generally in Post. Supplied training, tracking, or features are excluded where accepted as prerequisites.</dd>
<dt>Load and Process</dt><dd>Load is model initialization. Process includes loading, stages, and additional overhead; it is not their sum or time to first frame. Ditto and TalkLikeYou have overlapping threaded stages. SyncTalk includes an extra evaluation pass in Process and memory, outside the three inference phases.</dd>
<dt>Memory</dt><dd>NVML samples the process and descendants every 100 ms over the entire process, including loading and auxiliary stages. This sampled peak can miss brief allocations and is not a minimum device-capacity requirement. Separate PyTorch allocated/reserved counters are included in the downloads; some exceed the sampled NVML peak.</dd>
<dt>Scope</dt><dd>These short demo runs do not measure matched visual quality, sustained service, streaming startup, or long-session drift. StyleAvatar uses two frames; LeapTalk uses one chunk; TaoMate uses one window. Paper-reported performance remains attached to the literature records.</dd></dl>
<details class="result-configurations"><summary>Input settings and stage boundaries for each published run</summary><dl>{configs}</dl></details>
<p><a href="data/h200-measurement-notes-2026-10-16.md">Download the protocol and field definitions</a></p></section>
</main><footer class="container results-footer"><p>Results published 16 October 2026.</p><a href="https://github.com/zzzweakman/Fast-and-Stable-Virtual-Human-Video-Generation">View data and source on GitHub</a></footer>
</body></html>'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    assert not a.output.exists(),a.output
    data=json.loads((ROOT/'data'/f'{DATA}.json').read_text())
    a.output.write_text(render(data)+'\n')
    print('Generated',a.output)

if __name__=='__main__': main()
