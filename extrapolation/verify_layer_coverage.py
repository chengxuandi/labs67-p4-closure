"""Independent exact coverage (P3/P5 simple-split template), standard library.

Rebuilds positioned orbits from combinations, all norms, local NO witnesses,
Lucas proofs and every CRT ideal choice. Does not import the producer.
"""
from pathlib import Path
from itertools import combinations,product
import argparse,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent));import verify_cm_coverage as ar
from verify_new_lemmas import independent_types,need

def canon(s):
    return min(tuple(sorted((z,min(a*k%67,67-a*k%67)) for z,k in s)) for a in range(1,34))
def support_cover(P):
    expected=independent_types(P)
    if P==3:
        need(expected=={(3,0,0,0,0,0)},'P3 histogram')
        return {canon(tuple((1,k) for k in ks)) for ks in combinations(range(1,34),3)}
    if P==5:
        need(expected=={(2,1,0,0,0,0)},'P5 histogram')
        return {canon(((-1,1),(1,a),(1,b))) for a,b in combinations(range(2,34),2)}
    raise ValueError('unsupported layer')

def verify(path):
    doc=json.loads(Path(path).read_text());P=doc['P']
    need(doc['schema']=='lowp-layer-coverage-v1','schema')
    expected=support_cover(P);got={tuple(map(tuple,r['support'])) for r in doc['rows']}
    need(len(got)==len(doc['rows']) and got==expected,'positioned orbit cover missing/extra')
    targets={67}
    for r in doc['rows']:
        if r['kind']=='obstructed':targets.add(r['prime'])
        else:targets.update(p for p,e in r['factors'])
    nodes=ar.check_primes(doc['prime_nodes'],targets)
    T,psi=ar.real_polynomials();cases=[];local=[];total=0
    for index,row in enumerate(doc['rows']):
        support=row['support'];h=[17];alpha=[17]+[0]*66
        for z,k in support:
            h=ar.plus(h,T[k],z);alpha[k]+=z;alpha[67-k]+=z
        need(17-2*sum(abs(z) for z,k in support)>0,'total positivity not established')
        R=ar.norm_real(h,psi);need(R==row['norm'] and R>0,'wrong norm')
        if row['kind']=='obstructed':
            p=row['prime'];v=0;u=R
            while u%p==0:u//=p;v+=1
            d=len(ar.pgcd(psi,h,p))-1
            need(ar.order67(p)%2==0,'not inert')
            need(len(ar.pgcd(psi,[i*psi[i] for i in range(1,len(psi))],p))==1,'ramified')
            need(v==d==row['valuation']==row['gcd_degree'] and d>0,'local valuations not odd')
            local.append(support);continue
        need(row['kind']=='survivor','unknown conclusion')
        factors=row['factors'];need(len({p for p,e in factors})==len(factors),'duplicate factors')
        prod=1
        for p,e in factors:need(e==1 and p%67==1,'not squarefree split');prod*=p
        need(prod==R,'incomplete factorization')
        need(len(row['roots'])==len(factors),'root count')
        for (p,e),data in zip(factors,row['roots']):
            need(data['prime']==p,'prime binding');r,t=data['roots']
            need(1<r<t<p and r*t%p==1 and pow(r,67,p)==pow(t,67,p)==1,'invalid roots')
            g=ar.pgcd([1]*67,alpha,p)
            need(g==[1,-(r+t)%p,1],'gcd root cover')
        roots=[]
        for choices in product((0,1),repeat=len(factors)):
            rho=sum(data['roots'][c]*(R//p)*pow(R//p,-1,p) for (p,e),data,c in zip(factors,row['roots'],choices))%R
            roots.append(rho)
        need(len(set(roots))==len(roots) and sorted(roots)==row['all_rho'],'CRT cover')
        pairs=sorted((r,pow(r,-1,R)) for r in roots if r<pow(r,-1,R))
        need(2*len(pairs)==len(roots) and list(map(list,pairs))==row['conjugate_pairs'],'conjugacy cover')
        for j,(rho,conj) in enumerate(pairs):
            cases.append(dict(case_id=f'p{P:02}_s{index:03}_i{j}',P=P,support=support,norm=R,rho=rho,conjugate_rho=conj))
        total+=len(roots)
    result=dict(status='COVERAGE_PASS_NOT_CLOSED',P=P,orbits=len(expected),local_excluded=len(local),
                polarized_ideals=total,representatives=len(cases),prime_nodes=nodes,cases=cases)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('P',type=int);a=ap.parse_args()
    r=verify(ROOT/'certificates'/f'p{a.P:02}_coverage.json')
    (ROOT/'verifier_logs'/f'p{a.P:02}_coverage.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='cases'}))
