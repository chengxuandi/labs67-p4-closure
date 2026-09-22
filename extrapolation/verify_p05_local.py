"""Exact local269 audit only. Does not close P5 or certify other factors."""
from pathlib import Path
import json,math,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent));import verify_cm_coverage as a
from verify_new_lemmas import need
p=269;need(all(p%d for d in range(2,math.isqrt(p)+1)) and p%67==1,'prime')
T,psi=a.real_polynomials();results=[]
for support in (((-1,1),(1,7),(1,15)),((-1,1),(1,10),(1,17))):
    h=[17];alpha=[17]+[0]*66
    for z,k in support:h=a.plus(h,T[k],z);alpha[k]+=z;alpha[67-k]+=z
    R=a.norm_real(h,psi);need(R%(p*p)==0 and R%(p**3)!=0,'real norm valuation2')
    g=a.pgcd([1]*67,alpha,p);roots=[r for r in range(1,p) if sum(c*pow(r,j,p) for j,c in enumerate(g))%p==0]
    need(len(g)==5 and len(roots)==4 and all(pow(r,67,p)==1 and r!=1 for r in roots),'four split roots')
    pairs=sorted((r,pow(r,-1,p)) for r in roots if r<pow(r,-1,p))
    need(len(pairs)==2 and {v for pair in pairs for v in pair}==set(roots),'reciprocal pairing')
    results.append(dict(support=support,norm=R,prime=p,real_norm_valuation=2,
                        gcd=g,roots=roots,conjugate_pairs=pairs,
                        valuation_each_complex_prime=1,local_ideal_choices=4,
                        reason='NormK(alpha) has valuation4 and exactly4 positive-valuation degree1 prime factors'))
out=dict(status='P5_LOCAL_269_PASS_NOT_CLOSED',cases=results)
(ROOT/'verifier_logs/p05_local_269.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
