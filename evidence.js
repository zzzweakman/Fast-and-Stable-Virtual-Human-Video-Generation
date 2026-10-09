// Source configurations remain separate: no averaging across editions or devices.
export const PATTERNS = {
  L1: 'Identity anchor', L2: 'Bounded multiscale memory', L3: 'Position re-indexing',
  'L4-G': 'Generated-history training', 'L4-C': 'Corrupted-history training', L5: 'Boundary-state transfer'
};
export const EVIDENCE_STATUS = { A: 'documented architecture', Q: 'qualitative example', T: 'quantitative temporal evidence', B: 'component ablation', H: 'proposed transfer' };
export const FIELD_STATUS = { 'not-reported': 'Not reported in the checked source', unavailable: 'Source unavailable', conflict: 'Unresolved source conflict', 'not-applicable': 'Not applicable', 'not-audited': 'Not yet audited' };

export function attachEvidence(papers, snapshot) {
  const byPaper = new Map();
  for (const row of snapshot.configurations || []) {
    if (!byPaper.has(row.paperId)) byPaper.set(row.paperId, []);
    byPaper.get(row.paperId).push(row);
  }
  return papers.map(p => ({ ...p, evidence: byPaper.get(p.id) || [] }));
}

export function patternAssociations(paper) {
  const unique = new Map();
  for (const row of paper.evidence || []) for (const p of row.patterns || []) {
    const key = `${p.code}:${p.note}`;
    if (!unique.has(key)) unique.set(key, p);
  }
  return [...unique.values()];
}

export function matchesPattern(paper, code) {
  return patternAssociations(paper).some(p => (p.code === code || (code === 'L4' && p.code.startsWith('L4-'))) && p.status.includes('A'));
}

export function defaultConfiguration(rows) {
  return rows.find(r => /--(full-kernel-optimized|sd-vae|full|live-system)$/.test(r.id)) || rows[0];
}

export function fieldText(field) {
  if (!field) return 'Not yet audited';
  if (field.status !== 'reported') {
    const status = FIELD_STATUS[field.status] || 'Unknown evidence status';
    return field.status === 'conflict' && field.value !== undefined ? `${status}: ${field.value}${field.unit ? ` ${field.unit}` : ''} in the recorded table` : status;
  }
  const value = typeof field.value === 'object' && field.value !== null
    ? Object.entries(field.value).map(([k, v]) => `${k}: ${v}`).join('; ')
    : String(field.value);
  return `${value}${field.unit ? ` ${field.unit}` : ''}`;
}
