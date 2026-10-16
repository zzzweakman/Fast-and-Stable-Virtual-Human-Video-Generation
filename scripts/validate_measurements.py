"""Validate public results and enforce blank fields for pending methods."""
from pathlib import Path
import csv, json, re
from export_measurements import NUMERIC, CONTEXT
from render_measurements import render

ROOT=Path(__file__).resolve().parents[1]
PENDING={'MuseTalk','VideoReTalking','SoulX-LiveAct','SoulX-FlashTalk','SoulX-FlashHead'}

def validate_measurements():
    data=json.loads((ROOT/'data/h200-results-2026-10-16.json').read_text())
    rows=data['rows']
    assert len(rows)==49 and len({r['method'] for r in rows})==49
    measured=[r for r in rows if r['status']=='measured']
    pending=[r for r in rows if r['status']!='measured']
    assert len(measured)==data['published_results']==44
    assert len(pending)==data['pending_results']==5
    assert {r['method'] for r in pending}==PENDING
    for r in pending:
        assert all(r[k] is None for k in (*NUMERIC,*CONTEXT)),r['method']
    for r in measured:
        assert all(isinstance(r[k],(int,float)) and r[k]>=0 for k in NUMERIC),r['method']
        assert r['input_configuration'] and r['stage_definition']
    with (ROOT/'data/h200-results-2026-10-16.csv').open(newline='') as stream:
        csvrows=list(csv.DictReader(stream))
    assert len(csvrows)==len(rows)
    for actual,raw in zip(csvrows,rows):
        assert set(actual)==set(raw)
        for k,v in raw.items(): assert actual[k]==('' if v is None else str(v)),(raw['method'],k)
    page=(ROOT/'measurements.html').read_text()
    assert page==render(data)+'\n','Generated result page is stale'
    assert page.count('data-status="measured"')==44
    assert page.count('data-status="pending_remeasurement"')==2
    assert page.count('data-status="pending_measurement"')==3
    for r in pending:
        line=next(s for s in re.findall(r'<tr .*?</tr>',page) if f'data-method="{r["method"]}"' in s)
        cells=re.findall(r'<td>(.*?)</td>',line)
        assert len(cells)==8 and all(re.fullmatch(r'<span class="sr-only">Awaiting (?:re)?measurement</span>',c) for c in cells)
    assert 'Runtime &amp; memory results' in (ROOT/'index.html').read_text()
    print('Validated 44 public runs and five blank rows across HTML, CSV and JSON.')
    return data

if __name__=='__main__': validate_measurements()
