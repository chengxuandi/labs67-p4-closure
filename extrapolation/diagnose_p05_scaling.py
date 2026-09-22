"""Bounded next-layer diagnostic only; does not claim P5 exclusion."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent));import verify_cm_coverage as a
from verify_layer_coverage import support_cover
from verify_new_lemmas import need

def main():
    closed=json.loads((ROOT/'verifier_logs/p03_closure.json').read_text())
    need(closed['status']=='P3_CLOSED','only run after P3 closure')
    proposals=json.loads((ROOT/'inputs/legacy_factor_proposals.json').read_text())[1]
    special=[];T,psi=a.real_polynomials()
    for r in proposals['details']:
        product=1
        for p,e in r['factors']:product*=p**e
        need(product==r['norm'],'factor proposal product')
        if r['simple_split_proposal']:continue
        alpha=[17]+[0]*66;h=[17]
        for item in r['support'].split(';'):
            z,k=map(int,item.split(':'));alpha[k]+=z;alpha[67-k]+=z;h=a.plus(h,T[k],z)
        p=269;g=a.pgcd([1]*67,alpha,p)
        norm=a.norm_real(h,psi)
        need(norm==r['norm'] and norm%(p*p)==0 and norm%(p*p*p)!=0,'exact repeated-prime norm')
        roots=[r for r in range(1,p) if sum(c*pow(r,j,p) for j,c in enumerate(g))%p==0]
        special.append(dict(support=r['support'],prime=p,norm_valuation=2,gcd_degree=len(g)-1,roots=roots,
                            note='Local269 calculation exact; full factor primality not replayed for P5'))
    # Exact matching analysis for already-completed P3 transition identities.
    batch=json.loads((ROOT/'verifier_logs/p03_batch.json').read_text());states={};transitions=0;size=0
    import hashlib
    sys.set_int_max_str_digits(100000)
    for record in batch['records']:
        inp=json.loads((ROOT/record['input']).read_text());path=ROOT/record['certificate'];doc=json.loads(path.read_text());size+=path.stat().st_size
        eta=inp['alpha'];gens=doc['base_generators']
        for step in doc['steps']:
            key=[eta,gens,doc['base_generators'] if step[0] else None,step]
            digest=hashlib.sha256(json.dumps(key,separators=(',',':')).encode()).hexdigest()
            states[digest]=states.get(digest,0)+1;transitions+=1;eta=step[2];gens=step[4]
    lower=proposals['ideal_proposal_total']//2
    result=dict(status='P5_OPEN_SCALING_DIAGNOSTIC',P3_closed=True,P5_support_orbits=len(support_cover(5)),
                P5_simple_ideal_proposal_total=proposals['ideal_proposal_total'],
                P5_simple_representative_proposal_lower=lower,
                P5_vs_P4_proposed_representative_ratio=f'{lower}/27',special_269_inputs=special,
                P3_certificate_bytes=size,P3_transitions=transitions,P3_unique_transitions=len(states),
                literal_DAG_reuse=transitions-len(states),
                predicted_P5_certificate_bytes_lower=size*lower//len(batch['records']),
                claims_no_new_P5_NO=True,full_P5_ideal_coverage_verified=False)
    (ROOT/'verifier_logs/p05_scaling.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
