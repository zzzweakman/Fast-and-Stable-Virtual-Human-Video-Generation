"""Package only public website files; no runtime dependencies or source bundler."""
from pathlib import Path
import argparse
import shutil
from validate import validate

ROOT = Path(__file__).resolve().parents[1]
validate()
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=ROOT / 'dist')
out = parser.parse_args().output.resolve()
assert out != ROOT and out not in ROOT.parents, 'Build output must not replace the source tree'
out.mkdir(exist_ok=True)
for name in ('index.html', 'styles.css', 'app.js', 'catalog.js', 'evidence.js'):
    shutil.copy2(ROOT / name, out / name)
shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
(out / 'data').mkdir(exist_ok=True)
for name in ('papers.json', 'evidence-2026-10-09.json', 'configurations-2026-10-09.csv', 'cohort-2026-10-09.csv', 'evidence-guide.md', 'evidence-2026-10-09-final.json', 'configurations-2026-10-09-final.csv', 'evidence-guide-final.md', 'omniresponse-review.md'):
    shutil.copy2(ROOT / 'data' / name, out / 'data' / name)
shutil.copytree(ROOT / 'data/snapshots', out / 'data/snapshots', dirs_exist_ok=True)
(out / '.nojekyll').touch()
print(f'Built static website: {out}')
