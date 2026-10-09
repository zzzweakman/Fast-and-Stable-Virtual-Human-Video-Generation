export const ROUTES = {
  gan: { label: 'GAN-based', color: '#956333', cover: '#f3ede4' },
  diffusion: { label: 'Diffusion-based', color: '#536dc6', cover: '#edf0fb' },
  autoregressive: { label: 'Autoregressive', color: '#92558b', cover: '#f4edf5' },
  rendering: { label: 'Render-based', color: '#27786e', cover: '#eaf3ef' },
  supporting: { label: 'Supporting references', color: '#68736c', cover: '#edf1eb' }
};
export const SUPPORT_LABELS = { foundations: 'Foundations', datasets: 'Datasets', evaluation: 'Evaluation', surveys: 'Surveys', context: 'Related methods' };
export const groupOf = paper => Object.hasOwn ? (Object.hasOwn(ROUTES, paper.category) ? paper.category : 'supporting') : (Object.prototype.hasOwnProperty.call(ROUTES, paper.category) ? paper.category : 'supporting');
export const textOf = value => Array.isArray(value) ? value.join(', ') : String(value || '');
export const normalize = value => textOf(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
export const crossListingOf = (paper, route) => (paper.crossListings || []).find(listing => listing.route === route);
export const matchesRoute = (paper, route) => route === 'all' || groupOf(paper) === route || Boolean(crossListingOf(paper, route));
export function countBrowseRoutes(papers) {
  return Object.fromEntries(Object.keys(ROUTES).map(route => [route, papers.filter(p => matchesRoute(p, route)).length]));
}
export function filterPapers(papers, state) {
  const tokens = normalize(state.q).trim().split(/\s+/).filter(Boolean);
  const result = papers.filter(p => {
    if (!matchesRoute(p, state.route)) return false;
    if (state.year !== 'all' && (state.year.startsWith('before:') ? p.year >= +state.year.split(':')[1] : p.year !== +state.year)) return false;
    const haystack = normalize([p.title, p.shortTitle, p.authors, p.summary, p.subcategory, ...(p.tags || []), ...(p.crossListings || []).map(c => `${c.shortTitle || ''} ${c.label} ${c.summary} ${(c.tags || []).join(' ')}`)].join(' '));
    if (state.tag && !haystack.includes(normalize(state.tag))) return false;
    return tokens.every(token => haystack.includes(token));
  });
  result.sort((a, b) => state.sort === 'title'
    ? textOf(a.shortTitle || a.title).localeCompare(textOf(b.shortTitle || b.title))
    : (state.sort === 'oldest' ? a.year - b.year : b.year - a.year) || Number(Boolean(b.featured)) - Number(Boolean(a.featured)) || a.title.localeCompare(b.title));
  return result;
}
export function countRoutes(papers) {
  const result = Object.fromEntries(Object.keys(ROUTES).map(key => [key, 0]));
  papers.forEach(p => result[groupOf(p)]++);
  return result;
}
export function safeUrl(value) {
  try { const url = new URL(value); return ['http:', 'https:'].includes(url.protocol) ? url.href : ''; } catch { return ''; }
}
export function paperUrl(paper) {
  return safeUrl(paper.url) || (paper.arxiv && /^\d{4}\.\d{4,5}(v\d+)?$/.test(paper.arxiv) ? `https://arxiv.org/abs/${paper.arxiv}` : '');
}
export function readState(search) {
  const p = new URLSearchParams(search);
  return { q: (p.get('q') || '').slice(0, 300), route: ['all', ...Object.keys(ROUTES)].includes(p.get('route')) ? p.get('route') : 'all', year: /^(\d{4}|before:\d{4})$/.test(p.get('year')) ? p.get('year') : 'all', sort: ['newest', 'oldest', 'title'].includes(p.get('sort')) ? p.get('sort') : 'newest', view: p.get('view') === 'list' ? 'list' : 'grid', tag: (p.get('tag') || '').slice(0, 80) };
}
