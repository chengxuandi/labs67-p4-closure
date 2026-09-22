"""Finite certified list only. Stop dispatch on first unproved case."""
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
import argparse,json,time
from discover_chain import run
from verify_layer_coverage import verify
from verify_norm_chain import verify as replay
ROOT=Path(__file__).resolve().parent
def main(P,workers):
    coverage=verify(ROOT/'certificates'/f'p{P:02}_coverage.json')
    expected=coverage['cases'];results=[];pending=[]
    for row in expected:
        path=ROOT/'verifier_logs'/f"{row['case_id']}.run.json"
        if path.exists():
            rec=json.loads(path.read_text())
            if rec['status']=='PASS_NO':
                result=replay(json.loads((ROOT/rec['input']).read_text()),json.loads((ROOT/rec['certificate']).read_text()))
                if result['status']=='PASS_NO':results.append(rec);continue
        pending.append(row)
    output=ROOT/'verifier_logs'/f'p{P:02}_batch.json'
    start=time.monotonic();stop=False;iterator=iter(pending)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        active={}
        def dispatch():
            row=next(iterator,None)
            if row is not None:active[pool.submit(run,row)]=row
        for _ in range(workers):dispatch()
        while active:
            done,_=wait(active,return_when=FIRST_COMPLETED)
            for future in done:
                row=active.pop(future)
                try:rec=future.result()
                except Exception as exc:rec=dict(case_id=row['case_id'],status='OPEN',reason=repr(exc))
                results.append(rec)
                output.write_text(json.dumps(dict(P=P,expected=len(expected),completed=len(results),
                    all_no=sum(r['status']=='PASS_NO' for r in results),records=results,
                    elapsed=time.monotonic()-start),indent=2)+'\n')
                print(len(results),len(expected),row['case_id'],rec['status'],round(rec.get('seconds',0),2),flush=True)
                if rec['status']!='PASS_NO':stop=True
            if not stop:
                while len(active)<workers:
                    before=len(active);dispatch()
                    if before==len(active):break
    print('BATCH STOP' if stop else 'FINITE LIST COMPLETE',len(results),len(expected))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('P',type=int);a.add_argument('--workers',type=int,default=6);args=a.parse_args();main(args.P,args.workers)
