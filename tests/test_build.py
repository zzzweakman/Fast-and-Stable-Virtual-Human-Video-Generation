"""Regression checks for cached assets from an earlier page release."""
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build import write_web_assets


class AssetReleaseTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix='survey-asset-test-'))
        self.files = {
            'index.html': '<link rel="stylesheet" href="styles.css"><script type="module" src="app.js"></script><div id="year-chart"></div>',
            'styles.css': '.year-bar{background:green}',
            'app.js': "import { papers } from './catalog.js'; import './evidence.js';",
            'catalog.js': 'import "./evidence.js"; export const papers = [];',
            'evidence.js': 'export const patterns = {};',
        }

    def publish(self, label, files):
        source, output = self.work / (label + '-source'), self.work / label
        source.mkdir()
        output.mkdir()
        for name, content in files.items():
            (source / name).write_text(content, encoding='utf-8')
        write_web_assets(source, output)
        return output

    def release_urls(self, output):
        html = (output / 'index.html').read_text()
        return re.findall(r'(?:href|src)="([^"]+)"', html)

    def test_page_and_imports_bypass_unversioned_cached_files(self):
        output = self.publish('release', self.files)
        urls = self.release_urls(output)
        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertNotIn(url, self.files)
            self.assertTrue((output / url).is_file(), url)
        pending = [url for url in urls if url.endswith('.js')]
        visited = set()
        while pending:
            url = pending.pop()
            if url in visited:
                continue
            visited.add(url)
            self.assertTrue((output / url).is_file(), url)
            imports = re.findall(r'''["']\./([^"']+\.js)["']''', (output / url).read_text())
            self.assertFalse(set(imports) & self.files.keys())
            pending.extend(imports)
        self.assertEqual(len(visited), 3)

    def test_markup_styles_and_module_changes_all_refresh_asset_urls(self):
        baseline = self.release_urls(self.publish('baseline', self.files))
        for name in self.files:
            with self.subTest(changed=name):
                changed = {**self.files, name: self.files[name] + '\n<!-- changed -->' if name.endswith('.html') else self.files[name] + '\n/* changed */'}
                current = self.release_urls(self.publish(name.replace('.', '-'), changed))
                self.assertTrue(set(baseline).isdisjoint(current))

    def test_identical_source_keeps_stable_asset_urls(self):
        first = self.release_urls(self.publish('first', self.files))
        second = self.release_urls(self.publish('second', self.files))
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
