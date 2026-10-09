"""Optional real-browser checks. Requires the Playwright Python package/browser."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('SURVEY_TEST_URL', 'http://127.0.0.1:4173/')
OUT = ROOT / '.impeccable/review'
OUT.mkdir(parents=True, exist_ok=True)
papers = json.loads((ROOT / 'data/papers.json').read_text())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1, reduced_motion='reduce')
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    response = page.goto(BASE, wait_until='networkidle')
    assert response.status == 200
    page.wait_for_selector('.paper-card')
    assert page.locator('.paper-card').count() == 12
    assert str(len(papers)) in page.locator('#results-count').inner_text()
    assert page.locator('#error-state').is_hidden()
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.evaluate('document.fonts.check("700 16px Manrope")')
    page.screenshot(path=str(OUT / 'desktop.png'), full_page=True)
    page.screenshot(path=str(OUT / 'desktop-overview.png'))
    page.locator('#literature').scroll_into_view_if_needed()
    page.screenshot(path=str(OUT / 'desktop-library.png'))
    first_image = page.locator('#hero-image img').get_attribute('src')
    page.locator('#gallery-next').click()
    assert page.locator('#hero-image img').get_attribute('src') != first_image
    page.locator('#gallery-prev').click()
    assert page.locator('#hero-image img').get_attribute('src') == first_image
    page.locator('[data-filter-route="autoregressive"]').click()
    expected_ar = sum(p['category'] == 'autoregressive' for p in papers)
    assert page.locator('.paper-card').count() == expected_ar
    page.locator('#search').fill('MIDAS')
    assert page.locator('.paper-card').count() == 1
    page.locator('#list-view').click()
    assert 'list-view' in page.locator('#paper-grid').get_attribute('class')
    page.reload(wait_until='networkidle')
    assert page.locator('#search').input_value() == 'MIDAS'
    assert page.locator('.paper-card').count() == 1
    page.locator('[data-cite]').click()
    assert page.locator('.citation-details').is_visible()
    with page.expect_download() as download:
        page.locator('[data-download]').click()
    assert download.value.suggested_filename.endswith('.bib')
    with page.expect_download() as export:
        page.locator('#export-button').click()
    assert export.value.suggested_filename == 'fast-and-stable-literature.bib'
    page.locator('#search').fill('zzzz-unavailable-paper-98765')
    assert page.locator('#empty-state').is_visible()
    page.locator('#empty-reset').click()
    assert page.locator('.paper-card').count() == 12
    page.locator('#grid-view').click()
    page.locator('#load-more').click()
    assert page.locator('.paper-card').count() == 24
    page.locator('[data-stats-route="rendering"]').click()
    assert 'route=rendering' in page.url
    assert all('Render-based' in label for label in page.locator('.paper-category').all_text_contents())
    page.locator('#year').select_option('2024')
    assert all(label == '2024' for label in page.locator('.paper-year').all_text_contents())
    page.locator('#sort').select_option('oldest')
    page.locator('#reset-filters').click()
    page.keyboard.press('Tab')
    page.keyboard.press('/')
    assert page.locator('#search').evaluate('(e) => e === document.activeElement')
    page.locator('.stability-patterns summary').first.click()
    assert page.locator('.stability-patterns details').first.get_attribute('open') is not None
    page.goto(BASE, wait_until='networkidle')
    broken = page.locator('img').evaluate_all('(imgs) => imgs.filter(i => i.complete && !i.naturalWidth).map(i => i.src)')
    assert not broken, broken
    assert not errors, errors
    print('Desktop: filter combinations, shared URL state, search, empty state, list/grid, citations, exports, pagination, charts, keyboard and image checks passed.')
    for width in (768, 390):
        page.set_viewport_size({'width': width, 'height': 844})
        page.goto(BASE, wait_until='networkidle')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
        assert page.locator('.paper-card').count() == 12
        if width == 390:
            page.screenshot(path=str(OUT / 'mobile.png'), full_page=True)
            page.screenshot(path=str(OUT / 'mobile-overview.png'))
            page.locator('#literature').scroll_into_view_if_needed()
            page.screenshot(path=str(OUT / 'mobile-library.png'))
            page.locator('[data-filter-route="autoregressive"]').click()
            assert page.locator('.paper-card').count() == expected_ar
            page.locator('#list-view').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        print(f'Responsive: {width}px checks passed.')
    print('Browser errors:', errors)
    browser.close()
