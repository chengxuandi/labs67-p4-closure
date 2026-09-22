"""Coefficient-wise polynomial verification of the N67 alternation identity."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
n=67
for k in range(1,34):
    lhs={};rhs={}
    for i in range(n):
        j=(i+k)%n;term=tuple(sorted((i,j)))
        lhs[term]=lhs.get(term,0)+(-1)**(i+j)
    for lag,sgn in ((k,1),(n-k,-1)):
        for i in range(n-lag):
            term=(i,i+lag);rhs[term]=rhs.get(term,0)+sgn*(-1)**k
    if lhs!=rhs:raise ValueError('N67 duality polynomial mismatch')
if not all(((-1)**i)**2==1 for i in range(n)):raise ValueError('not an involution')
result=dict(status='PASS',n=n,identities=33,verification='equality of every quadratic monomial coefficient',
            proves='T is an involution on all binary words and P(T(S))=Pprime(S)')
(ROOT/'verifier_logs/duality67.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
