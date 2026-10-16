"""Export a public subset of supplied measurements, withholding pending results.

python scripts/export_measurements.py --input /path/to/h200_results.json \
    --output-dir /tmp/new-public-data
The output directory must be new. No raw input is copied into the repository.
"""
from pathlib import Path
import argparse, csv, json

RELEASE='2026-10-16'
NUMERIC=('frames','output_width','output_height','pre_s','generation_s','post_s','load_s','process_s','nvml_peak_gib','duration_s','video_fps','encoded_width','encoded_height','stage_union_s','stage_overlap_s','evaluation_s','torch_allocated_peak_gib','torch_reserved_peak_gib','nvml_peak_mib')
CONTEXT=('input_configuration','stage_definition','code_commit','torch_version','attention_backend','implementation_status')
WITHHELD={'MuseTalk','VideoReTalking'}
SOUL=[('SoulX-LiveAct','zhen2026soulx','2603.11746'),('SoulX-FlashTalk','shen2026soulxflashtalkrealtimeinfinitestreaming','2512.23379'),('SoulX-FlashHead','yu2026soulx','2602.07449')]

def export_rows(source):
    result=[]
    for row in source:
        pending=row['method'] in WITHHELD
        public={k:row[k] for k in ('method','route','cite_key','arxiv_id')}
        public['repository']=None
        public['status']='pending_remeasurement' if pending else 'measured'
        for k in (*NUMERIC,*CONTEXT): public[k]=None if pending else row.get(k)
        result.append(public)
    for method,key,arxiv in SOUL:
        result.append(dict(method=method,route='diffusion',cite_key=key,arxiv_id=arxiv,repository=f'https://github.com/Soul-AILab/{method}',status='pending_measurement',**{k:None for k in (*NUMERIC,*CONTEXT)}))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True,type=Path);p.add_argument('--output-dir',required=True,type=Path);a=p.parse_args()
    rows=export_rows(json.loads(a.input.read_text()))
    assert len(rows)==49 and sum(r['status']=='measured' for r in rows)==44
    a.output_dir.mkdir(parents=True,exist_ok=False)
    public={'release':RELEASE,'measured_at':'2026-10-15','published_results':44,'pending_results':5,
      'hardware':{'gpu_per_run':'one NVIDIA H200','device_memory_gib':140.40,'host':'eight H200 GPUs; two Intel Xeon Platinum 8558 CPUs','workers':'up to eight on separate GPUs; 20 logical CPUs per worker; numerical-library threads limited to four','os':'Ubuntu 22.04.4 / Linux 5.15','driver':'570.124.06'},
      'protocol':{'trials':'One measured run after one warm-up in a separate process; no repeated-trial statistics.','inputs':'Demo workloads, lengths, dimensions, supplied prerequisites and software differ.','timing':'CUDA synchronization at stage boundaries; stages follow each implementation. Load is separate; Proc is whole-process elapsed time, not TTFF or a phase sum.','memory':'NVML samples the process and descendants every 100 ms over the whole process, including loading and auxiliary stages. The sampled peak can miss short allocations. Framework counters are retained separately.','limits':'No matched quality evaluation, streaming TTFF, sustained service or long-session drift measurement. Shared host resources and varying NUMA locality remain.','missing':'Pending rows have null numerical and configuration fields; CSV fields are empty. Missing results are not zero.'},
      'rows':rows}
    (a.output_dir/f'h200-results-{RELEASE}.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
    with (a.output_dir/f'h200-results-{RELEASE}.csv').open('x',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    print(f'Exported 44 results and five blank pending rows to {a.output_dir}')

if __name__=='__main__': main()
