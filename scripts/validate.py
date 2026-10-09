"""Check the data and local assets that actually ship to GitHub Pages."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def validate():
    papers = json.loads((ROOT / 'data/papers.json').read_text())
    assets = json.loads((ROOT / 'assets/papers/manifest.json').read_text())
    assert papers, 'Empty catalogue'
    ids = [p['id'] for p in papers]
    assert len(ids) == len(set(ids)), 'Duplicate paper IDs'
    categories = {'gan', 'diffusion', 'autoregressive', 'rendering', 'foundations', 'datasets', 'evaluation', 'surveys', 'context'}
    evidence = json.loads((ROOT / 'data/evidence-2026-10-09-final.json').read_text())
    configurations = evidence['configurations']
    snapshot = json.loads((ROOT / 'data/snapshots/2026-10-09-final/manifest.json').read_text())
    assert snapshot['snapshot'] == evidence['snapshot'], 'Snapshot identifiers disagree'
    for manifest_path in sorted((ROOT / 'data/snapshots').glob('*/manifest.json')):
        for entry in json.loads(manifest_path.read_text())['files']:
            path = (ROOT / entry['path']).resolve()
            assert path.is_relative_to(ROOT), 'Snapshot path escapes site'
            assert path.is_file(), f'Missing frozen artifact: {path}'
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], f'Frozen artifact changed: {path}'
    assert (ROOT / snapshot['manuscript']['path']).read_bytes().startswith(b'%PDF'), 'Invalid revision PDF'
    frozen = json.loads((ROOT / snapshot['catalogue']['path']).read_text())
    assert len(frozen) == snapshot['catalogue']['records'], 'Frozen catalogue count differs'
    assert len(evidence['cohort']) == snapshot['evidence']['cohortSystems'], 'Cohort count differs'
    assert len(configurations) == snapshot['evidence']['checkedConfigurations'], 'Configuration count differs'
    assert len({r['paperId'] for r in configurations}) == snapshot['evidence']['checkedSystems'], 'Checked-system count differs'
    with (ROOT / 'data/configurations-2026-10-09-final.csv').open(newline='') as stream:
        exported = list(csv.DictReader(stream))
    assert len(exported) == len(configurations), 'CSV configuration count differs'
    for row, original in zip(exported, configurations):
        assert row['id'] == original['id'] and json.loads(row['fields']) == original['fields'], 'CSV configuration differs from JSON'
        assert json.loads(row['additionalSources']) == original.get('additionalSources', []), 'CSV supplementary sources differ'
    row_ids = [r['id'] for r in configurations]
    assert len(row_ids) == len(set(row_ids)), 'Duplicate evidence configuration'
    allowed_status = set(evidence['statusDefinitions']) | {'reported'}
    for row in configurations:
        assert row['paperId'] in ids, f"Orphan evidence row: {row['id']}"
        assert row['source']['locations'] and row['source']['edition'], f"Missing exact source: {row['id']}"
        assert urlparse(row['source']['url']).scheme == 'https', f"Invalid evidence URL: {row['id']}"
        assert re.fullmatch(r'[a-f0-9]{64}', row['source']['sha256']), f"Missing source hash: {row['id']}"
        assert row.get('boundary'), f"Missing measurement boundary: {row['id']}"
        for source in row.get('additionalSources', []):
            assert source['edition'] and source['locations'], f"Missing supplementary source: {row['id']}"
            assert urlparse(source['url']).scheme == 'https', f"Invalid supplementary URL: {row['id']}"
            assert re.fullmatch(r'[a-f0-9]{64}', source['sha256']), f"Missing supplementary hash: {row['id']}"
        for key, field in row['fields'].items():
            assert field['status'] in allowed_status, f"Unknown field state: {row['id']}/{key}"
            if field['status'] == 'reported':
                assert 'value' in field, f"Reported field without a value: {row['id']}/{key}"
            elif field['status'] != 'conflict':
                assert 'value' not in field, f"Missing field disguised as a value: {row['id']}/{key}"
        for pattern in row.get('patterns', []):
            assert pattern['code'] in {'L1','L2','L3','L4-G','L4-C','L5'}, f"Invalid pattern: {row['id']}"
            assert pattern['status'] and set(pattern['status']) <= set(evidence['patternStatusDefinitions']), f"Missing pattern evidence: {row['id']}"
    by_paper = {p['id']: {r['id'] for r in configurations if r['paperId'] == p['id']} for p in papers}
    for paper in papers:
        for key in ('id', 'title', 'shortTitle', 'authors', 'summary', 'url', 'section', 'source', 'bibtex'):
            assert paper.get(key), f"Missing {key}: {paper['id']}"
        assert paper['category'] in categories, f"Unknown category: {paper['id']}"
        assert isinstance(paper['year'], int) and 1900 <= paper['year'] <= 2026, f"Invalid year: {paper['id']}"
        assert urlparse(paper['url']).scheme in ('https', 'http'), f"Invalid URL: {paper['id']}"
        assert isinstance(paper['tags'], list), f"Tags must be a list: {paper['id']}"
        assert set(paper.get('evidenceIds', [])) == by_paper[paper['id']], f"Evidence links out of sync: {paper['id']}"
        assert re.match(r'@\w+\s*\{', paper['bibtex']), f"Invalid citation: {paper['id']}"
        listings = paper.get('crossListings', [])
        assert isinstance(listings, list), f"Invalid cross-listings: {paper['id']}"
        routes = [listing.get('route') for listing in listings]
        assert len(routes) == len(set(routes)), f"Repeated cross-listing route: {paper['id']}"
        for listing in listings:
            assert listing.get('kind', 'baseline') in {'baseline', 'controller'}, f"Invalid cross-listing kind: {paper['id']}"
            assert listing['route'] in {'gan', 'diffusion', 'autoregressive', 'rendering'}, f"Invalid cross-listing route: {paper['id']}"
            assert listing['route'] != paper['category'], f"Redundant cross-listing: {paper['id']}"
            assert listing.get('label') and listing.get('summary'), f"Missing cross-listing context: {paper['id']}"
            assert urlparse(listing.get('evidenceUrl', '')).scheme == 'https', f"Missing cross-listing evidence: {paper['id']}"
            if 'shortTitle' in listing:
                assert isinstance(listing['shortTitle'], str) and listing['shortTitle'].strip(), f"Invalid baseline title: {paper['id']}"
            if 'tags' in listing:
                assert isinstance(listing['tags'], list) and all(isinstance(tag, str) and tag.strip() for tag in listing['tags']), f"Invalid baseline tags: {paper['id']}"
    for key, asset in assets.items():
        for field in ('path', 'heroPath'):
            if field not in asset:
                continue
            path = (ROOT / asset[field]).resolve()
            assert path.is_relative_to(ROOT / 'assets'), f'Asset escapes directory: {key}'
            assert path.is_file() and path.stat().st_size > 500, f'Missing/empty image: {path}'
        assert asset.get('sourceUrl') and asset.get('caption'), f'Missing image provenance: {key}'
    for path in ('index.html', 'styles.css', 'app.js', 'catalog.js', 'evidence.js', 'data/evidence-guide.md', 'data/configurations-2026-10-09.csv', 'data/cohort-2026-10-09.csv', 'data/snapshots/2026-10-09/papers.json', 'assets/favicon.svg', 'assets/fonts/manrope.ttf', 'assets/fonts/OFL.txt', 'assets/survey/survey.pdf'):
        assert (ROOT / path).is_file(), f'Missing required asset: {path}'
    assert (ROOT / 'assets/survey/survey.pdf').read_bytes().startswith(b'%PDF'), 'Invalid survey PDF'
    used_previews = len(set(assets) & set(ids))
    print(f'Validated {len(papers)} papers, {used_previews} linked source previews, and all required assets.')
    if set(assets) - set(ids):
        print('Unused preview records:', ', '.join(sorted(set(assets) - set(ids))))
    print(dict(Counter(p['category'] for p in papers)))
    return papers

if __name__ == '__main__':
    validate()
