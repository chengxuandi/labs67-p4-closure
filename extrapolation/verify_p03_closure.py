"""Whole P3 closure, not an energy lower bound. Refuse incomplete case lists."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
from verify_layer_coverage import verify as coverage
from verify_new_lemmas import need
ROOT=Path(__file__).resolve().parent

def bind_records(cov,batch):
    expected={r['case_id']:r for r in cov['cases']}
    records=batch['records'];seen={r['case_id'] for r in records}
    need(len(records)==len(seen)==len(expected) and seen==set(expected),'incomplete whole-layer certificate')
    bound=[]
    for rec in sorted(records,key=lambda r:r['case_id']):
        row=expected[rec['case_id']]
        ip=(ROOT/rec['input'].replace('\\','/')).resolve();cp=(ROOT/rec['certificate'].replace('\\','/')).resolve()
        need(ip.is_relative_to(ROOT) and cp.is_relative_to(ROOT),'unsafe input path')
        inp=json.loads(ip.read_text())
        need(all(inp[k]==row[k] for k in ('P','support','norm','rho','conjugate_rho')),'wrong certificate input binding')
        bound.append((rec['case_id'],ip,cp))
    return bound

def check(workers=4):
    cov=coverage(ROOT/'certificates/p03_coverage.json')
    # Discovery logs contain machine-local command lines and are not proof
    # dependencies. Reconstruct the public index from verified coverage.
    batch={'records':[dict(case_id=r['case_id'],
                           input=f"inputs/{r['case_id']}.json",
                           certificate=f"certificates/{r['case_id']}.json")
                      for r in cov['cases']]}
    bound=bind_records(cov,batch)
    files={ROOT/'certificates/p03_coverage.json'}
    def task(bound_row):
        cid,ip,cp=bound_row
        # Ignore all saved PASS labels: ask the exact verifier in a fresh process.
        cmd=[sys.executable,'-B',str(ROOT/'verify_norm_chain.py'),str(ip),str(cp)]
        r=subprocess.run(cmd,capture_output=True,timeout=90)
        need(r.returncode==0,'invalid norm certificate: '+cid)
        result=json.loads(r.stdout);need(result['status']=='PASS_NO','not an absence certificate')
        return dict(case_id=cid,result=result,input=ip,certificate=cp)
    results=[]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for row in pool.map(task,bound):
            files.update((row.pop('input'),row.pop('certificate')));results.append(row)
    control=subprocess.run([sys.executable,'-B',str(ROOT/'audit_general_chain.py')],capture_output=True,timeout=60)
    need(control.returncode==0 and json.loads(control.stdout)['status']=='PASS','positive/mutation control failed')
    files.update(ROOT/name for name in ('verify_p03_closure.py','verify_layer_coverage.py','verify_norm_chain.py',
                                        'verify_new_lemmas.py','audit_general_chain.py'))
    files.update((ROOT.parent/'verify_cm_result.py',ROOT.parent/'verify_cm_coverage.py'))
    hashes={p.relative_to(ROOT.parent).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    return dict(status='P3_CLOSED',P=3,orbits=cov['orbits'],local_exclusions=cov['local_excluded'],
                ideal_exclusions=cov['polarized_ideals'],conjugate_representatives=len(results),
                results=results,sha256=hashes,proves='For all binary length67 words P!=3 and Pprime!=3.',
                global_optimality_proved=False)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--workers',type=int,default=4);args=a.parse_args()
    start=time.monotonic();r=check(args.workers);r['replay_seconds']=time.monotonic()-start
    (ROOT/'verifier_logs').mkdir(exist_ok=True)
    (ROOT/'verifier_logs/p03_closure.json').write_text(json.dumps(r,indent=2)+'\n')
    print('P3_CLOSED: all166 support orbits excluded; NOT global LABS optimality.')
