"""Check the data and local assets that actually ship to GitHub Pages."""
from collections import Counter
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
    categories = {'gan', 'diffusion', 'autoregressive', 'rendering', 'foundations', 'datasets', 'evaluation', 'surveys'}
    for paper in papers:
        for key in ('id', 'title', 'shortTitle', 'authors', 'summary', 'url', 'section', 'source', 'bibtex'):
            assert paper.get(key), f"Missing {key}: {paper['id']}"
        assert paper['category'] in categories, f"Unknown category: {paper['id']}"
        assert isinstance(paper['year'], int) and 1900 <= paper['year'] <= 2026, f"Invalid year: {paper['id']}"
        assert urlparse(paper['url']).scheme in ('https', 'http'), f"Invalid URL: {paper['id']}"
        assert isinstance(paper['tags'], list), f"Tags must be a list: {paper['id']}"
        assert re.match(r'@\w+\s*\{', paper['bibtex']), f"Invalid citation: {paper['id']}"
    for key, asset in assets.items():
        for field in ('path', 'heroPath'):
            if field not in asset:
                continue
            path = (ROOT / asset[field]).resolve()
            assert path.is_relative_to(ROOT / 'assets'), f'Asset escapes directory: {key}'
            assert path.is_file() and path.stat().st_size > 500, f'Missing/empty image: {path}'
        assert asset.get('sourceUrl') and asset.get('caption'), f'Missing image provenance: {key}'
    for path in ('index.html', 'styles.css', 'app.js', 'catalog.js', 'assets/favicon.svg', 'assets/fonts/manrope.ttf', 'assets/fonts/OFL.txt', 'assets/survey/survey.pdf'):
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
