"""Package only public website files; no runtime dependencies or source bundler."""
from pathlib import Path
import argparse
import hashlib
import shutil
from validate import validate

ROOT = Path(__file__).resolve().parents[1]
WEB_ASSETS = ('styles.css', 'app.js', 'catalog.js', 'evidence.js')


def write_web_assets(source, output):
    """Keep each HTML release paired with its own styles and module graph."""
    pages = sorted(path.name for path in source.glob('*.html'))
    texts = {name: (source / name).read_text(encoding='utf-8') for name in (*pages, *WEB_ASSETS)}
    digest = hashlib.sha256()
    for name, content in texts.items():
        digest.update(name.encode('utf-8') + b'\0' + content.encode('utf-8') + b'\0')
    version = digest.hexdigest()[:12]
    names = {name: f'{Path(name).stem}.{version}{Path(name).suffix}' for name in WEB_ASSETS}
    for name in WEB_ASSETS:
        content = texts[name]
        if name.endswith('.js'):
            for module in WEB_ASSETS:
                if module.endswith('.js'):
                    for quote in ("'", '"'):
                        content = content.replace(f'{quote}./{module}{quote}', f'{quote}./{names[module]}{quote}')
        (output / names[name]).write_text(content, encoding='utf-8')
        # Retain the original URLs for existing links and local source previews.
        shutil.copy2(source / name, output / name)
    for page in pages:
        html = texts[page].replace('href="styles.css"', f'href="{names["styles.css"]}"')
        html = html.replace('src="app.js"', f'src="{names["app.js"]}"')
        (output / page).write_text(html, encoding='utf-8')


def main():
    validate()
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    out = parser.parse_args().output.resolve()
    assert out != ROOT and out not in ROOT.parents, 'Build output must not replace the source tree'
    out.mkdir(exist_ok=True)
    write_web_assets(ROOT, out)
    shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
    (out / 'data').mkdir(exist_ok=True)
    for name in ('papers.json', 'evidence-2026-10-09.json', 'configurations-2026-10-09.csv', 'cohort-2026-10-09.csv', 'evidence-guide.md', 'evidence-2026-10-09-final.json', 'configurations-2026-10-09-final.csv', 'evidence-guide-final.md', 'omniresponse-review.md', 'literature-update-2026-10-13.md', 'literature-additions-2026-10-13.bib', 'measurement-template-2026-10-13.csv'):
        shutil.copy2(ROOT / 'data' / name, out / 'data' / name)
    shutil.copytree(ROOT / 'data/snapshots', out / 'data/snapshots', dirs_exist_ok=True)
    for name in ('dblp-update-2026-10-13.md', 'references-dblp-2026-10-13.bib', 'dblp-reference-check-2026-10-13.json'):
        shutil.copy2(ROOT / 'data' / name, out / 'data' / name)
    for name in ('h200-results-2026-10-16.json', 'h200-results-2026-10-16.csv', 'h200-measurement-notes-2026-10-16.md', 'ar-measurement-coverage-2026-10-16.md'):
        shutil.copy2(ROOT / 'data' / name, out / 'data' / name)
    (out / '.nojekyll').touch()
    print(f'Built static website: {out}')


if __name__ == '__main__':
    main()
