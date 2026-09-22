"""Exact adversarial tests, plus independent symbolic-signature coverage audit."""
import itertools,json,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)
def qform(a):return len(a)*sum(x*x for x in a)-sum(a)**2
def coset_bound(residues,m):
    r=[v%m for v in residues]+[0]
    return min(qform([v if v>=cut else v+m for v in r]) for cut in set(r))

def independent_types(P):
    vals=(-3,-2,-1,1,2,3)
    result=set()
    def visit(j,slots,budget,sigma,counts):
        if j==6:
            if budget==0 and sigma>=0 and math.isqrt(1+8*sigma)**2==1+8*sigma:
                result.add(tuple(counts[vals.index(z)] for z in (1,-1,2,-2,3,-3)))
            return
        z=vals[j];cost=z*(2*z-1)
        for c in range(min(slots,budget//cost)+1):visit(j+1,slots-c,budget-c*cost,sigma+c*z,counts+[c])
    visit(0,33,P,0,[])
    return result

def orbit_count(h):
    full=[33-sum(h)]+list(h);total=0
    # Count cycles of each actual multiplier permutation, not a prefilled divisor table.
    for a in range(1,34):
        unseen=set(range(1,34));lengths=[]
        while unseen:
            start=next(iter(unseen));k=start;size=0
            while k in unseen:
                unseen.remove(k);size+=1;k=min(k*a%67,67-k*a%67)
            lengths.append(size)
        need(len(set(lengths))==1,'nonregular group action')
        d=lengths[0]
        if any(c%d for c in full):continue
        left=len(lengths);ways=1
        for c in full:ways*=math.comb(left,c//d);left-=c//d
        total+=ways
    need(total%33==0,'Burnside divisibility')
    return total//33

def check_signatures():
    total_types=0
    for P in range(26):
        doc=json.loads((ROOT/'signatures'/f'P{P:02}.json').read_text())
        need(doc['P']==P and doc['values']==[1,-1,2,-2,3,-3],'wrong binding')
        actual=independent_types(P);claimed={tuple(h['counts']) for h in doc['histograms']}
        need(actual==claimed and len(claimed)==len(doc['histograms']),'incomplete histogram cover')
        o=0;n=0
        for h in doc['histograms']:
            counts=h['counts'];sigma=sum(c*z for c,z in zip(counts,doc['values']))
            need(h['sigma']==sigma and h['DC_abs']**2==1+8*sigma,'bad square identity')
            full=[33-sum(counts)]+counts;left=33;ways=1
            for c in full:ways*=math.comb(left,c);left-=c
            count=orbit_count(counts)
            need(count==h['orbits'] and ways==h['raw_vectors'],'wrong type count')
            o+=count;n+=ways
        need((n,o)==(doc['candidate_vector_count'],doc['candidate_orbit_count']),'wrong layer count')
        if doc['orbit_representatives'] is not None:
            seen=set();covered=0
            for supp in doc['orbit_representatives']:
                supp=tuple(map(tuple,supp))
                need(len({k for z,k in supp})==len(supp) and all(1<=k<=33 for z,k in supp),'bad shifts')
                need(sum(z*(2*z-1) for z,k in supp)==P,'wrong penalty')
                sigma=sum(z for z,k in supp)
                need(sigma>=0 and math.isqrt(1+8*sigma)**2==1+8*sigma,'wrong sum')
                images={tuple(sorted((z,min(a*k%67,67-a*k%67)) for z,k in supp)) for a in range(1,34)}
                canonical=min(images)
                need(supp==canonical and canonical not in seen,'noncanonical or duplicate orbit')
                seen.add(canonical);covered+=len(images)
            need(len(seen)==o and covered==n,'positioned signature cover incomplete')
        total_types+=len(actual)
    need(total_types==113,'113 type baseline mismatch')
    return total_types

def main():
    nt=check_signatures();checks=0;strict_example=None
    for n,m in ((3,3),(3,5),(3,7),(5,2),(5,3)):
        for r in itertools.product(range(m),repeat=n-1):
            exact=min(qform([r[i]+m*z[i] for i in range(n-1)]+[0]) for z in itertools.product((-1,0,1),repeat=n-1))
            bound=coset_bound(r,m);need(bound==exact,'coset theorem counterexample')
            centered=[min(v,m-v) for v in r]
            old=max([n*v*v for v in centered]+[0])
            need(2*bound>=old,'weaker than scalar bound')
            if bound>(old+1)//2 and strict_example is None:strict_example=dict(n=n,m=m,r=r,coset=bound,scalar_twice=old)
            checks+=1
    words=0
    for n in range(3,14,2):
        for s in itertools.product((-1,1),repeat=n):
            alt=[(-1)**i*x for i,x in enumerate(s)]
            c=[sum(s[i]*s[i+k] for i in range(n-k)) for k in range(1,n)]
            for k in range(1,(n+1)//2):
                cyc=sum(alt[i]*alt[(i+k)%n] for i in range(n))
                need(cyc==(-1)**k*(c[k-1]-c[n-k-1]),'alternation duality failure')
            words+=1
    out=dict(status='PASS',signature_histograms=nt,positioned_low_layers='COMPLETE',
             coset_exhaustive_checks=checks,strict_improvement_example=strict_example,
             exact_duality_words=words,realizability_not_inferred=True)
    (ROOT/'verifier_logs/new_lemma_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))
if __name__=='__main__':main()
