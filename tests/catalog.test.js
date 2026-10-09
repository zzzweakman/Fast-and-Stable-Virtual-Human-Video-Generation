import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { countRoutes, countBrowseRoutes, crossListingOf, filterPapers, groupOf, paperUrl, readState, safeUrl } from '../catalog.js';
import { attachEvidence, defaultConfiguration, fieldText, matchesPattern } from '../evidence.js';

const papers = JSON.parse(fs.readFileSync(new URL('../data/papers.json', import.meta.url), 'utf8'));
const defaults = { q: '', route: 'all', year: 'all', tag: '', sort: 'newest' };
const snapshot = JSON.parse(fs.readFileSync(new URL('../data/evidence-2026-10-09.json', import.meta.url), 'utf8'));
const audited = attachEvidence(papers, snapshot);

test('hybrid correction preserves one primary record and the total catalogue', () => {
  assert.equal(papers.find(p => p.id === 'wang2023styleavatar').category, 'rendering');
  assert.equal(papers.length, 164);
  assert.deepEqual(countRoutes(papers), { gan: 21, diffusion: 43, autoregressive: 5, rendering: 54, supporting: 41 });
});

test('pattern filters distinguish corrupted history, generated history, and memory types', () => {
  const find = id => audited.find(p => p.id === id);
  assert.ok(matchesPattern(find('weng2026eartalking'), 'L4-C'));
  assert.ok(!matchesPattern(find('weng2026eartalking'), 'L4-G'));
  assert.ok(matchesPattern(find('huang2025live'), 'L4-G'));
  assert.ok(!matchesPattern(find('li2026personalive'), 'L2'));
  assert.ok(!matchesPattern(find('chen2025midas'), 'L2'));
  assert.ok(matchesPattern(find('zhen2026soulx'), 'L2'));
  assert.ok(matchesPattern(find('li2025joyavatar'), 'L5'));
  const hypothetical = { evidence: [{ patterns: [{ code: 'L2', status: ['H'], note: 'Proposed only' }] }] };
  assert.ok(!matchesPattern(hypothetical, 'L2'));
  const results = filterPapers(audited, { ...defaults, route: 'autoregressive', tag: 'L4-C', q: 'EARTalking' });
  assert.deepEqual(results.map(p => p.id), ['weng2026eartalking']);
});

test('configuration selection preserves source values and unresolved conflicts', () => {
  const live = audited.find(p => p.id === 'huang2025live').evidence;
  assert.equal(live.length, 6);
  const full = defaultConfiguration(live);
  assert.equal(full.fields.throughput.value, 45.2);
  assert.equal(full.fields.hardware.value, '5 NVIDIA H100');
  assert.match(full.source.edition, /v6$/);
  assert.equal(full.fields.latency.status, 'conflict');
  assert.match(fieldText(full.fields.latency), /conflict.*1\.21 s/);
  assert.equal(live.find(r => r.configuration === 'teacher').fields.throughput.value, 0.29);
  assert.match(fieldText({ status: 'not-reported' }), /Not reported/);
  assert.equal(fieldText({ status: 'reported', value: 0, unit: 'ms' }), '0 ms');
});

test('cited proceedings edition is visible for the ART-V baseline', () => {
  const mmvid = papers.find(p => p.id === 'han2022mmvid');
  assert.match(paperUrl(mmvid), /openaccess\.thecvf\.com/);
  assert.match(mmvid.crossListings[0].evidenceUrl, /CVPR2022.*pdf#page=5$/);
  assert.ok(mmvid.provenance.evidence.every(e => e.version === 'CVPR proceedings'));
});

test('all catalogue entries have a single count and a usable source link', () => {
  assert.equal(new Set(papers.map(p => p.id)).size, papers.length);
  assert.equal(Object.values(countRoutes(papers)).reduce((a, b) => a + b, 0), papers.length);
  for (const p of papers) assert.match(paperUrl(p), /^https?:\/\//, p.id);
});

test('visual ownership keeps motion controllers with their rendering family', () => {
  const liveportrait = papers.find(p => p.id === 'guo2024liveportrait');
  const midas = papers.find(p => p.id === 'chen2025midas');
  assert.equal(groupOf(liveportrait), 'rendering');
  assert.equal(groupOf(midas), 'autoregressive');
  const ar = filterPapers(papers, { ...defaults, route: 'autoregressive' });
  assert.ok(ar.some(p => p.id === midas.id));
  assert.ok(!ar.some(p => p.id === liveportrait.id));
});

test('combined search, year, and route filters can find a specific paper', () => {
  const p = papers.find(p => p.id === 'guo2024liveportrait');
  const matches = filterPapers(papers, { ...defaults, q: 'LIVEPORTRAIT', route: 'rendering', year: String(p.year) });
  assert.ok(matches.some(m => m.id === p.id));
  assert.equal(filterPapers(papers, { ...defaults, q: 'zzzz-no-such-method-98765' }).length, 0);
  assert.equal(filterPapers(papers, { ...defaults, q: 'LivePortrait', route: 'gan' }).length, 0);
});

test('a dataset baseline is discoverable in AR without duplicating records or statistics', () => {
  const speaker = papers.find(p => p.id === 'zhang2025speakervid');
  assert.equal(speaker.category, 'datasets');
  assert.equal(crossListingOf(speaker, 'autoregressive').label, 'AR baseline');
  for (const route of ['all', 'supporting', 'autoregressive']) {
    const matches = filterPapers(papers, { ...defaults, route, q: 'SpeakerVid', year: String(speaker.year) });
    assert.deepEqual(matches.map(p => p.id), [speaker.id]);
    assert.equal(matches[0].bibtex, speaker.bibtex);
  }
  assert.equal(filterPapers(papers, { ...defaults, route: 'diffusion', q: 'SpeakerVid' }).length, 0);
  const primary = countRoutes(papers), browsing = countBrowseRoutes(papers);
  assert.equal(primary.autoregressive, papers.filter(p => p.category === 'autoregressive').length);
  assert.equal(browsing.autoregressive, primary.autoregressive + papers.filter(p => crossListingOf(p, 'autoregressive')).length);
  assert.equal(Object.values(primary).reduce((a, b) => a + b, 0), papers.length);
  assert.equal(filterPapers(papers, { ...defaults, route: 'autoregressive' }).length, browsing.autoregressive);
  assert.ok(filterPapers(papers, { ...defaults, route: 'autoregressive', q: 'SpeakerVid 3D-VAE' }).some(p => p.id === speaker.id));
});

test('general-video AR foundations remain separate from the native method route', () => {
  const foundations = filterPapers(papers, { ...defaults, route: 'supporting', tag: 'AR foundations' });
  assert.deepEqual(new Set(foundations.map(p => p.shortTitle)), new Set(['NOVA', 'VideoPoet', 'VideoGPT']));
  assert.ok(foundations.every(p => p.category === 'foundations'));
  assert.equal(filterPapers(papers, { ...defaults, route: 'autoregressive', tag: 'AR foundations' }).length, 0);
  assert.equal(new Set(papers.map(p => p.id)).size, papers.length);
});

test('historical AR baselines reuse their non-AR source paper and citation', () => {
  for (const [id, alias] of [['han2022mmvid', 'ART-V'], ['liu2022paralip', 'TransformerT2L']]) {
    const paper = papers.find(p => p.id === id);
    assert.equal(paper.category, 'context');
    assert.equal(groupOf(paper), 'supporting');
    assert.match(crossListingOf(paper, 'autoregressive').shortTitle, new RegExp(alias));
    for (const route of ['all', 'supporting', 'autoregressive']) {
      const matches = filterPapers(papers, { ...defaults, route, q: alias });
      assert.deepEqual(matches.map(p => p.id), [id]);
      assert.equal(matches[0].bibtex, paper.bibtex);
    }
  }
  const regional = filterPapers(papers, { ...defaults, route: 'autoregressive', tag: 'lip-region' });
  assert.deepEqual(new Set(regional.map(p => p.id)), new Set(['chen2020duallip', 'liu2022paralip']));
  const dual = papers.find(p => p.id === 'chen2020duallip');
  assert.equal(dual.category, 'autoregressive');
  assert.match(dual.shortTitle, /without duration/);
});

test('spatial and unresolved AR cases remain discoverable outside strict temporal counts', () => {
  const context = filterPapers(papers, { ...defaults, route: 'supporting', tag: 'AR scope context' });
  assert.deepEqual(new Set(context.map(p => p.id)), new Set(['deng2026fluentavatarflickerfreetalkingheadanimation', 'zhang2025tamingtransformer']));
  assert.ok(context.every(p => p.category === 'context'));
  assert.equal(filterPapers(papers, { ...defaults, route: 'autoregressive', tag: 'AR scope context' }).length, 0);
  assert.equal(countRoutes(papers).autoregressive, 5);
  assert.equal(countBrowseRoutes(papers).autoregressive, 8);
});

test('sorting and historical buckets operate on numeric bibliography years', () => {
  const oldest = filterPapers(papers, { ...defaults, sort: 'oldest' });
  const newest = filterPapers(papers, defaults);
  assert.ok(oldest.every((p, i) => i === 0 || oldest[i - 1].year <= p.year));
  assert.ok(newest.every((p, i) => i === 0 || newest[i - 1].year >= p.year));
  const old = filterPapers(papers, { ...defaults, year: 'before:2017' });
  assert.ok(old.length > 0);
  assert.ok(old.every(p => p.year < 2017));
});

test('shared filters accept valid state and reject unsafe or unsupported values', () => {
  assert.deepEqual(readState('?route=rendering&year=2024&view=list&q=LivePortrait&sort=oldest'), { ...defaults, route: 'rendering', year: '2024', view: 'list', q: 'LivePortrait', sort: 'oldest' });
  const state = readState('?route=bogus&year=NaN&view=unknown&sort=bad');
  assert.equal(state.route, 'all'); assert.equal(state.year, 'all'); assert.equal(state.view, 'grid');
  assert.equal(safeUrl('javascript:alert(1)'), '');
  assert.equal(safeUrl('data:text/html,hello'), '');
});
