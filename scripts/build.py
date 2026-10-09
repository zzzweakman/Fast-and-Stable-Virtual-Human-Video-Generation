"""Package only public website files; no runtime dependencies or source bundler."""
from pathlib import Path
import shutil
from validate import validate

ROOT = Path(__file__).resolve().parents[1]
validate()
out = ROOT / 'dist'
out.mkdir(exist_ok=True)
for name in ('index.html', 'styles.css', 'app.js', 'catalog.js'):
    shutil.copy2(ROOT / name, out / name)
shutil.copytree(ROOT / 'assets', out / 'assets', dirs_exist_ok=True)
(out / 'data').mkdir(exist_ok=True)
shutil.copy2(ROOT / 'data/papers.json', out / 'data/papers.json')
(out / '.nojekyll').touch()
print(f'Built static website: {out}')
