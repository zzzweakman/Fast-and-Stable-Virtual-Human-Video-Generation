"""Capture fully decoded content and run an optional local axe accessibility audit."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.impeccable/review'
OUT.mkdir(parents=True, exist_ok=True)
suffix = os.environ.get('SURVEY_CAPTURE_SUFFIX', 'loaded')
url = os.environ.get('SURVEY_TEST_URL', 'http://127.0.0.1:4173/')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    page.goto(url, wait_until='networkidle')
    page.wait_for_selector('.paper-card')
    page.evaluate('''async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(async i => {i.loading='eager'; try {await i.decode();} catch {}}));
    }''')
    print('Image states:', page.locator('img').evaluate_all('(imgs)=>imgs.map(i=>({src:i.getAttribute("src"),loaded:i.complete&&i.naturalWidth>0}))'))
    axe = Path('/tmp/survey-axe-4.10.3.js')
    report = {}
    for name, width, height in [('desktop',1440,1000),('mobile',390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT/f'{name}-{suffix}.png'),full_page=True)
        page.screenshot(path=str(OUT/f'{name}-overview-{suffix}.png'))
        page.evaluate('document.querySelector("#literature").scrollIntoView({block:"start",behavior:"instant"})')
        page.wait_for_function('document.querySelector(".nav-link.active").hash === "#literature"')
        page.screenshot(path=str(OUT/f'{name}-library-{suffix}.png'))
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        if axe.exists():
            page.add_script_tag(path=str(axe))
            result=page.evaluate('async () => await axe.run(document, {runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}})')
            report[name]=[{'id':v['id'],'impact':v['impact'],'description':v['description'],'nodes':[{'target':n['target'],'summary':n.get('failureSummary')} for n in v['nodes']]} for v in result['violations']]
    if report:
        (OUT/f'accessibility-{suffix}.json').write_text(json.dumps(report,indent=2))
        print('Accessibility findings:', {k:[{'id':v['id'],'nodes':len(v['nodes'])} for v in values] for k,values in report.items()})
    page.locator('[data-filter-route="autoregressive"]').focus()
    page.keyboard.press('Enter')
    assert page.locator('[data-filter-route="autoregressive"]').evaluate('(e)=>e===document.activeElement')
    page.locator('[data-mechanism="Streaming"]').focus()
    page.keyboard.press('Enter')
    assert page.locator('[data-mechanism="Streaming"]').evaluate('(e)=>e===document.activeElement')
    page.locator('[data-clear="tag"]').click()
    assert page.evaluate('document.activeElement!==document.body')
    for width in (320,360,768):
        page.set_viewport_size({'width':width,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), f'Overflow at {width}'
    assert page.locator('#year-legend li').count()==5
    print('Filter focus, chart legend, active navigation, and 320/360/768px layout checks passed.')
    browser.close()
