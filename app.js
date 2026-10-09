import { ROUTES, SUPPORT_LABELS, groupOf, textOf, filterPapers, countRoutes, countBrowseRoutes, crossListingOf, paperUrl, safeUrl, readState } from './catalog.js';

const $ = selector => document.querySelector(selector);
const esc = value => textOf(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const icons = {
  external: '<path d="M7 17 17 7M7 7h10v10"/>',
  quote: '<path d="M10 6H4v7h6v-7Zm0 7c0 4-2 5-4 5M20 6h-6v7h6v-7Zm0 7c0 4-2 5-4 5"/>',
  close: '<path d="m6 6 12 12M18 6 6 18"/>'
};
const icon = name => `<svg viewBox="0 0 24 24" aria-hidden="true">${icons[name]}</svg>`;
let papers = [], images = {}, visible = 12, filtered = [], featured = [], featureIndex = 0, toastTimer;
let state = readState(location.search);
const mechanisms = ['Streaming', 'Distillation', 'Caching', 'Identity', '3D Gaussian'];

function imageFor(p) {
  const record = images[p.id];
  return record && /^assets\/[a-zA-Z0-9_./-]+$/.test(record.path || '') && !record.path.includes('..') ? record : null;
}
function cover(p) {
  const route = ROUTES[groupOf(p)];
  return `<div class="paper-cover" style="--category:${route.color};--cover:${route.cover}"><span class="cover-rule" aria-hidden="true"></span><strong>${esc(p.shortTitle || p.title)}</strong><small>TEXT COVER · ${p.year} · ${esc(SUPPORT_LABELS[p.category] || route.label)}</small></div>`;
}
function renderPaper(p, index) {
  const listing = crossListingOf(p, state.route);
  const displayTitle = listing?.shortTitle || p.shortTitle || p.title;
  const route = ROUTES[listing?.route || groupOf(p)], media = imageFor(p), url = paperUrl(p);
  const label = listing ? `${listing.label} · ${SUPPORT_LABELS[p.category] || ROUTES[groupOf(p)].label}` : SUPPORT_LABELS[p.category] || route.label;
  const preview = media ? `<img src="${esc(media.path)}" alt="${esc(media.caption || `Preview from ${p.title}`)}" width="800" height="500" loading="lazy" decoding="async" ${media.kind === 'page' ? 'class="page-preview"' : ''}>` : cover(p);
  const arxiv = url.includes('arxiv.org/');
  return `<article class="paper-card" style="--category:${route.color}" data-paper-id="${esc(p.id)}">
    <a class="paper-image-link" href="${esc(url)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${esc(p.title)}">${preview}</a>
    <div class="paper-body"><div class="paper-meta"><span class="paper-category">${esc(label)}</span><span class="paper-year">${p.year}</span></div>
    <h3 class="paper-title"><a href="${esc(url)}" target="_blank" rel="noopener noreferrer" title="${esc(p.title)}">${esc(displayTitle)}</a></h3>
    ${displayTitle !== p.title ? `<p class="paper-full-title" title="${esc(p.title)}">${esc(p.title)}</p>` : ''}
    <p class="paper-authors" title="${esc(p.authors)}">${esc(p.authors)}</p>
    <p class="paper-summary">${esc(listing?.summary || p.summary)}</p>
    <div class="paper-tags">${(listing?.tags || p.tags || []).slice(0, 3).map(tag => `<span class="paper-tag">${esc(tag)}</span>`).join('')}</div></div>
    <div class="paper-footer"><a class="paper-source" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${arxiv ? 'arXiv' : 'Read paper'} ${icon('external')}</a><button class="citation-button" type="button" data-cite="${esc(p.id)}" aria-expanded="false" aria-controls="citation-${index}">${icon('quote')} Cite</button></div>
    <div class="citation-details" id="citation-${index}" hidden><strong>BibTeX citation</strong><p>Citation from the recorded source edition. Verify the publication record before use.</p><label class="sr-only" for="bib-${index}">BibTeX for ${esc(p.shortTitle || p.title)}</label><textarea id="bib-${index}" readonly spellcheck="false">${esc(p.bibtex)}</textarea><div class="citation-actions"><button type="button" data-copy="${esc(p.id)}">Copy citation</button><button type="button" data-download="${esc(p.id)}">Download .bib</button></div></div>
    </article>`;
}

function syncInputs() {
  $('#search').value = state.q; $('#sort').value = state.sort;
  if (state.year.startsWith('before:') && !Array.from($('#year').options).some(o => o.value === state.year)) {
    $('#year').add(new Option(`Before ${state.year.split(':')[1]}`, state.year));
  }
  if (!Array.from($('#year').options).some(o => o.value === state.year)) state.year = 'all';
  $('#year').value = state.year;
}
function saveUrl() {
  const url = new URL(location.href);
  for (const key of ['q', 'route', 'year', 'sort', 'view', 'tag']) {
    const defaults = { q: '', route: 'all', year: 'all', sort: 'newest', view: 'grid', tag: '' };
    if (state[key] === defaults[key]) url.searchParams.delete(key); else url.searchParams.set(key, state[key]);
  }
  history.replaceState(null, '', url);
}
function updateFilters() {
  const focused = document.activeElement;
  const restore = focused?.matches('[data-filter-route]') ? ['data-filter-route', focused.dataset.filterRoute]
    : focused?.matches('[data-mechanism]') ? ['data-mechanism', focused.dataset.mechanism] : null;
  const counts = countBrowseRoutes(papers);
  $('#route-filters').innerHTML = `<button class="route-filter ${state.route === 'all' ? 'active' : ''}" type="button" data-filter-route="all" aria-pressed="${state.route === 'all'}">All literature <span class="filter-count">${papers.length}</span></button>` + Object.entries(ROUTES).map(([key, route]) => `${key === 'supporting' ? '<div class="filter-separator"></div>' : ''}<button class="route-filter ${state.route === key ? 'active' : ''}" style="--category:${route.color}" type="button" data-filter-route="${key}" aria-pressed="${state.route === key}"><span class="filter-dot" aria-hidden="true"></span>${route.label}<span class="filter-count">${counts[key]}</span></button>`).join('');
  $('#mechanism-filters').innerHTML = mechanisms.map(tag => `<button type="button" class="mechanism-button ${state.tag === tag ? 'active' : ''}" data-mechanism="${esc(tag)}" aria-pressed="${state.tag === tag}">${esc(tag)}</button>`).join('');
  const chips = [];
  if (state.route !== 'all') chips.push(['route', ROUTES[state.route].label]);
  if (state.year !== 'all') chips.push(['year', state.year.startsWith('before:') ? `Before ${state.year.split(':')[1]}` : state.year]);
  if (state.tag) chips.push(['tag', state.tag]);
  if (state.q) chips.push(['q', `“${state.q}”`]);
  $('#active-filters').innerHTML = chips.map(([key, label]) => `<button type="button" class="filter-chip" data-clear="${key}" aria-label="Remove ${esc(label)} filter">${esc(label)}${icon('close')}</button>`).join('');
  if (restore) document.querySelector(`[${restore[0]}="${CSS.escape(restore[1])}"]`)?.focus({ preventScroll: true });
  else if (focused?.matches('[data-clear]')) ($('#active-filters button') || $('#search')).focus({ preventScroll: true });
}
function render({ preserveFilters = false } = {}) {
  filtered = filterPapers(papers, state);
  const shown = Math.min(visible, filtered.length);
  $('#paper-grid').innerHTML = filtered.slice(0, shown).map(renderPaper).join('');
  $('#paper-grid').classList.toggle('list-view', state.view === 'list');
  $('#paper-grid').setAttribute('aria-busy', 'false');
  $('#results-count').innerHTML = `<strong>${filtered.length}</strong> ${filtered.length === 1 ? 'paper' : 'papers'}${filtered.length !== papers.length ? ` of ${papers.length}` : ' in the catalogue'}`;
  $('#pagination-note').textContent = filtered.length ? `Showing ${shown} of ${filtered.length} papers` : '';
  const primaryCount = papers.filter(p => p.category === 'autoregressive').length;
  const crossCount = papers.filter(p => crossListingOf(p, 'autoregressive')).length;
  const foundationCount = papers.filter(p => p.category === 'foundations' && p.tags.includes('AR foundations')).length;
  const contextCount = papers.filter(p => p.category === 'context' && p.tags.includes('AR scope context')).length;
  $('#ar-scope').hidden = state.route !== 'autoregressive';
  $('#ar-scope-summary').textContent = `${primaryCount} primary-route papers + ${crossCount} cross-listed baselines. Includes historical lip-region models; charts count each source paper once.`;
  $('#ar-foundations-link').textContent = `Explore ${foundationCount} general-video AR foundations`;
  $('#ar-context-link').textContent = `Explore ${contextCount} spatial or unresolved AR papers`;
  $('#empty-state').hidden = filtered.length > 0; $('#load-more').hidden = shown >= filtered.length;
  $('#export-button').disabled = !filtered.length;
  for (const view of ['grid', 'list']) {
    $(`#${view}-view`).classList.toggle('selected', state.view === view);
    $(`#${view}-view`).setAttribute('aria-pressed', String(state.view === view));
  }
  if (!preserveFilters) updateFilters();
  $('#paper-grid').querySelectorAll('img').forEach(img => img.addEventListener('error', () => {
    const p = papers.find(p => p.id === img.closest('[data-paper-id]').dataset.paperId);
    if (p) img.parentElement.innerHTML = cover(p);
  }, { once: true }));
  saveUrl();
}
function change(patch, scroll = false) {
  Object.assign(state, patch); visible = 12; syncInputs(); render();
  if (scroll) $('#literature').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
}
function reset() { change({ q: '', route: 'all', year: 'all', tag: '' }); }
function toast(message) { clearTimeout(toastTimer); $('#toast').textContent = message; $('#toast').hidden = false; toastTimer = setTimeout(() => { $('#toast').hidden = true; }, 3600); }
function download(text, filename, type = 'application/x-bibtex') {
  const blobUrl = URL.createObjectURL(new Blob([text], { type }));
  const link = document.createElement('a'); link.href = blobUrl; link.download = filename; document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
}

function renderStats() {
  const counts = countRoutes(papers), mainRoutes = Object.keys(ROUTES).filter(k => k !== 'supporting'), total = papers.length - counts.supporting;
  $('#method-total').textContent = `${total} method papers`;
  const maxCount = Math.max(...mainRoutes.map(k => counts[k]), 1);
  $('#route-chart').innerHTML = mainRoutes.map(key => `<button class="bar-row" type="button" data-stats-route="${key}" aria-label="${counts[key]} primary ${ROUTES[key].label} papers; explore this route and any cross-listed baselines"><span>${ROUTES[key].label}</span><span class="bar-track"><span class="bar-fill" style="--percent:${counts[key] / maxCount * 100}%;--category:${ROUTES[key].color}"></span></span><span class="bar-value">${counts[key]}</span></button>`).join('');
  const allYears = [...new Set(papers.map(p => p.year))].sort((a, b) => a - b), latest = allYears.at(-1), cutoff = latest - 9;
  const buckets = [];
  const older = papers.filter(p => p.year < cutoff);
  if (older.length) buckets.push({ label: `≤${cutoff - 1}`, value: `before:${cutoff}`, papers: older });
  for (let year = Math.max(cutoff, allYears[0]); year <= latest; year++) buckets.push({ label: String(year), value: String(year), papers: papers.filter(p => p.year === year) });
  const max = Math.max(...buckets.map(b => b.papers.length), 1);
  $('#year-chart').innerHTML = buckets.map(b => {
    const c = countRoutes(b.papers);
    return `<button class="year-column" type="button" data-stats-year="${b.value}" title="${b.label}: ${b.papers.length} papers" aria-label="Explore ${b.papers.length} papers from ${b.label}"><span class="year-value">${b.papers.length}</span><span class="year-bar" style="--height:${b.papers.length / max * 126}px">${Object.keys(ROUTES).filter(k => c[k]).map(k => `<span class="year-segment" style="--part:${c[k] / b.papers.length * 100}%;--category:${ROUTES[k].color}"></span>`).join('')}</span><span class="year-label">${b.label}</span></button>`;
  }).join('');
  $('#year-legend').innerHTML = Object.values(ROUTES).map(route => `<li><span class="legend-swatch" style="background:${route.color}" aria-hidden="true"></span>${route.label}</li>`).join('');
  const imageCount = papers.filter(p => imageFor(p)).length;
  $('#coverage-line').innerHTML = `<span><strong>${papers.length}</strong> catalogued papers</span><span><strong>${total}</strong> route-assigned papers</span><span><strong>${counts.supporting}</strong> supporting references</span><span><strong>${imageCount}</strong> source previews</span>`;
}
function renderFeature() {
  if (!featured.length) return;
  const p = featured[featureIndex], media = imageFor(p), route = ROUTES[groupOf(p)];
  $('#gallery-counter').textContent = `${String(featureIndex + 1).padStart(2, '0')} / ${String(featured.length).padStart(2, '0')}`;
  const heroPath = media?.heroPath && /^assets\/[a-zA-Z0-9_./-]+$/.test(media.heroPath) && !media.heroPath.includes('..') ? media.heroPath : media?.path;
  $('#hero-image').innerHTML = media ? `<img src="${esc(heroPath)}" alt="${esc(media.heroCaption || media.caption || `Research figure from ${p.title}`)}" width="800" height="500" decoding="async" fetchpriority="high">` : cover(p);
  const img = $('#hero-image img'); if (img) img.addEventListener('error', () => { $('#hero-image').innerHTML = cover(p); }, { once: true });
  $('#hero-paper-link').href = paperUrl(p); $('#hero-paper-link').target = '_blank'; $('#hero-paper-link').rel = 'noopener noreferrer'; $('#hero-paper-link').setAttribute('aria-label', `Read ${p.title}`);
  $('#hero-category').textContent = route.label; $('#hero-category').style.setProperty('--category', route.color);
  $('#hero-paper-title').textContent = p.shortTitle || p.title;
  $('#hero-paper-description').textContent = `${p.year} · ${media?.kind === 'page' ? 'Paper preview' : media ? 'Figure from the original paper' : 'Explore the source paper'}`;
}
function setupFeatured() {
  const preferences = ['guo2024liveportrait', 'tian2024emo', 'zhang2024musetalk', 'chen2025midas'];
  featured = preferences.map(id => papers.find(p => p.id === id)).filter(p => p && imageFor(p));
  const selectedRoutes = new Set(featured.map(groupOf));
  for (const route of ['rendering', 'diffusion', 'gan', 'autoregressive']) {
    if (!selectedRoutes.has(route)) {
      const candidate = papers.find(p => groupOf(p) === route && imageFor(p));
      if (candidate) { featured.push(candidate); selectedRoutes.add(route); }
    }
  }
  if (!featured.length) featured = papers.filter(p => p.featured).slice(0, 4);
  $('#gallery-prev').disabled = featured.length < 2; $('#gallery-next').disabled = featured.length < 2;
  renderFeature();
}

async function load() {
  $('#error-state').hidden = true; $('#results-count').textContent = 'Loading the literature…'; $('#paper-grid').setAttribute('aria-busy', 'true');
  try {
    const response = await fetch(new URL('data/papers.json', import.meta.url));
    if (!response.ok) throw new Error(`Catalogue HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data) || !data.length || data.some(p => !p.id || !p.title || !paperUrl(p))) throw new Error('Invalid catalogue');
    papers = data;
    try {
      const res = await fetch(new URL('assets/papers/manifest.json', import.meta.url));
      if (res.ok) { const manifest = await res.json(); images = manifest.papers || manifest; }
    } catch { images = {}; }
    $('#year').innerHTML = '<option value="all">All years</option>' + [...new Set(papers.map(p => p.year))].sort((a, b) => b - a).map(year => `<option value="${year}">${year}</option>`).join('');
    syncInputs(); render(); renderStats(); setupFeatured();
  } catch (error) {
    console.error('Catalogue could not load:', error.message);
    $('#paper-grid').setAttribute('aria-busy', 'false'); $('#results-count').textContent = 'Catalogue unavailable'; $('#error-state').hidden = false; $('#empty-state').hidden = true; $('#load-more').hidden = true;
  }
}

$('#search').addEventListener('input', event => change({ q: event.target.value }));
$('#sort').addEventListener('change', event => change({ sort: event.target.value }));
$('#year').addEventListener('change', event => change({ year: event.target.value }));
$('#reset-filters').addEventListener('click', reset); $('#empty-reset').addEventListener('click', reset);
$('#retry-load').addEventListener('click', load);
$('#load-more').addEventListener('click', () => {
  const previous = Math.min(visible, filtered.length); visible += 12; render({ preserveFilters: true });
  const next = $('#paper-grid').children[previous]?.querySelector('h3 a'); if (next) next.focus({ preventScroll: true });
});
for (const view of ['grid', 'list']) $(`#${view}-view`).addEventListener('click', () => { state.view = view; render({ preserveFilters: true }); });
$('#export-button').addEventListener('click', () => { download(filtered.map(p => p.bibtex).join('\n\n') + '\n', 'fast-and-stable-literature.bib'); toast(`Exported ${filtered.length} citations`); });
for (const [id, tag] of [['ar-foundations-link', 'AR foundations'], ['ar-context-link', 'AR scope context']]) $(`#${id}`).addEventListener('click', event => {
  if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  event.preventDefault(); change({ route: 'supporting', tag, q: '', year: 'all' });
  $('#search').focus({ preventScroll: true });
});
$('#gallery-prev').addEventListener('click', () => { featureIndex = (featureIndex - 1 + featured.length) % featured.length; renderFeature(); });
$('#gallery-next').addEventListener('click', () => { featureIndex = (featureIndex + 1) % featured.length; renderFeature(); });
document.addEventListener('click', async event => {
  const route = event.target.closest('[data-filter-route]'); if (route) change({ route: route.dataset.filterRoute });
  const routeLink = event.target.closest('[data-route]'); if (routeLink) change({ route: routeLink.dataset.route, q: '', year: 'all', tag: '' });
  const tag = event.target.closest('[data-mechanism]'); if (tag) change({ tag: state.tag === tag.dataset.mechanism ? '' : tag.dataset.mechanism });
  const clear = event.target.closest('[data-clear]'); if (clear) change({ [clear.dataset.clear]: ['route', 'year'].includes(clear.dataset.clear) ? 'all' : '' });
  const statsRoute = event.target.closest('[data-stats-route]'); if (statsRoute) change({ route: statsRoute.dataset.statsRoute, q: '', year: 'all', tag: '' }, true);
  const statsYear = event.target.closest('[data-stats-year]'); if (statsYear) change({ year: statsYear.dataset.statsYear, route: 'all', q: '', tag: '' }, true);
  const cite = event.target.closest('[data-cite]');
  if (cite) { const panel = document.getElementById(cite.getAttribute('aria-controls')); panel.hidden = !panel.hidden; cite.setAttribute('aria-expanded', String(!panel.hidden)); }
  const copy = event.target.closest('[data-copy]');
  if (copy) {
    const paper = papers.find(p => p.id === copy.dataset.copy);
    try { await navigator.clipboard.writeText(paper.bibtex); toast('Citation copied'); }
    catch { const field = copy.closest('.citation-details').querySelector('textarea'); field.focus(); field.select(); toast('Citation selected. Use your keyboard to copy.'); }
  }
  const down = event.target.closest('[data-download]'); if (down) { const p = papers.find(p => p.id === down.dataset.download); download(p.bibtex + '\n', `${p.id.replace(/[^\w-]/g, '')}.bib`); }
});
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) && !document.activeElement.isContentEditable) { event.preventDefault(); $('#search').focus(); }
});
window.addEventListener('popstate', () => { state = readState(location.search); visible = 12; syncInputs(); render(); });
function updateNavigation() {
  let current = 'survey';
  const line = $('.site-header').getBoundingClientRect().bottom + 90;
  for (const id of ['survey', 'literature', 'landscape', 'perspectives']) {
    if (document.getElementById(id).getBoundingClientRect().top <= line) current = id;
  }
  document.querySelectorAll('.nav-link').forEach(a => {
    const active = a.hash === `#${current}`; a.classList.toggle('active', active);
    if (active) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
  });
}
let navigationFrame = false;
window.addEventListener('scroll', () => {
  if (!navigationFrame) { navigationFrame = true; requestAnimationFrame(() => { updateNavigation(); navigationFrame = false; }); }
}, { passive: true });
window.addEventListener('resize', updateNavigation);
updateNavigation();
load();
