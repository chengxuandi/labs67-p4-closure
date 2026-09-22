"""Compose exact input coverage and all finite NO chains. No solver is called.

Successful acceptance proves P(S) != 4 for ALL length-67 binary words.
It deliberately does not prove the LABS energy lower bound E>=241.
"""
from pathlib import Path
import argparse,json,hashlib
import verify_cm_coverage as coverage
import verify_cm_result as chain

ROOT=Path(__file__).resolve().parent
CERT=ROOT/'certificates'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def check():
    cov=coverage.verify(CERT/'cm_coverage_certificate.json')
    document=json.loads((CERT/'cm_coverage_certificate.json').read_text())
    expected={}
    for row in document['survivors']:
        for index,(rho,conj_rho) in enumerate(row['conjugate_pairs']):
            expected[f"b{row['b']}_pair{index}"]=(row['b'],row['norm'],rho,conj_rho)
    need(len(expected)==27,'incorrect exact cover')
    listed=json.loads((CERT/'cm_representative_cases.json').read_text())
    need(len(listed)==27 and len({r['case_id'] for r in listed})==27,'duplicated/missing representative')
    for r in listed:
        need(r['case_id'] in expected,'unknown representative')
        need((r['b'],r['norm'],r['rho'],r['conjugate_rho'])==expected[r['case_id']],'representative mismatch')
    records=json.loads((CERT/'cm_batch_results.json').read_text())
    need(len(records)==27 and {r['case_id'] for r in records}==set(expected),'incomplete result coverage')
    seen=set();results=[];files={CERT/'cm_coverage_certificate.json',CERT/'cm_representative_cases.json',
                               CERT/'cm_batch_results.json'}
    def local_path(relative):
        p=(ROOT/relative.replace('\\','/')).resolve()
        need(p.is_relative_to(ROOT),'certificate path outside artifact root')
        return p
    for record in sorted(records,key=lambda r:expected[r['case_id']]):
        cid=record['case_id'];need(cid not in seen,'duplicate case');seen.add(cid)
        b,R,rho,conj=expected[cid]
        ip=local_path(record['input']);cp=local_path(record['certificate']);files.update((ip,cp))
        inp=json.loads(ip.read_text());cert=json.loads(cp.read_text())
        need(inp['case'] in ('p4','b13'),'wrong case kind')
        actual_b=13 if inp['case']=='b13' else inp['b']
        need((actual_b,inp['ideal_index'],inp['rho'])==(b,R,rho),'wrong chain input binding')
        need(cert['status']=='NO_CHAIN','not a NO certificate')
        result=chain.verify_chain(inp,cert)
        need(result['status']=='PASS_NO','absence not proved')
        result.update(case_id=cid,b=b,rho=rho,conjugate_rho=conj)
        results.append(result)
        print(cid,'PASS_NO',result['prime'],result['trace'],result['residue'],flush=True)
    # Do not trust a negative-only implementation: require the actual new GS control.
    ip=CERT/'cm_inputs/positive67.json';cp=CERT/'cm_outputs/control.json'
    pc=CERT/'cm_outputs/control_certificate.json';files.update((ip,cp,pc))
    inp=json.loads(ip.read_text())
    need(chain.verify(inp,json.loads(cp.read_text()))['status']=='PASS','positive generator failed')
    need(chain.verify_chain(inp,json.loads(pc.read_text()))['status']=='PASS_CONTROL_CHAIN','positive chain failed')
    for p in (Path(coverage.__file__),Path(chain.__file__),Path(__file__),
              coverage.LEGACY/'lowp_orbit_norm_certificate.csv',
              coverage.LEGACY/'p4_original_survivor_full_factorization.csv'):
        files.add(p)
    hashes={str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(files)}
    return dict(status='P4_CLOSED',support_orbits=32,inert_excluded=20,
                no_chain_representatives=27,polarized_ideals_excluded=54,
                positive_generator_and_chain='PASS',cases=results,coverage=cov,sha256=hashes,
                proves='For every S in {+1,-1}^67, periodic penalty P(S) is not 4; also Pprime(S) is not 4 by alternation.',
                LABS67_global_optimality_proved=False)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output')
    a=ap.parse_args();result=check()
    if a.output:Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print('P4_CLOSED: 32/32 support orbits excluded; NOT a global LABS energy proof.')
