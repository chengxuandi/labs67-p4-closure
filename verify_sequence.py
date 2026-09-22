"""Independent direct LABS witness checker (no PB/solver imports)."""
import json,argparse
from pathlib import Path

def verify(word):
    assert len(word)==67 and all(type(v) is int and v in (0,1) for v in word)
    s=[1-2*b for b in word]
    c=[sum(s[i]*s[i+k] for i in range(67-k)) for k in range(1,67)]
    r=[c[k-1]+c[66-k] for k in range(1,34)]
    q=[(-1)**k*(c[k-1]-c[66-k]) for k in range(1,34)]
    assert all(v%4==3 for v in r+q)
    p=sum(((v+1)//4)*(2*((v+1)//4)-1) for v in r)
    pp=sum(((v+1)//4)*(2*((v+1)//4)-1) for v in q)
    e=sum(v*v for v in c);assert e==33+4*(p+pp)
    return dict(word=word,energy=e,correlations=c,P=p,Pprime=pp,DC=sum(s),
                alternating_DC=sum((-1)**i*v for i,v in enumerate(s)),
                normalized_skew=(s[0]==s[33]==1 and all(s[66-i]==(-1)**(33-i)*s[i] for i in range(33))))
def incumbent():
    runs=[11,4,1,2,3,2,3,4,4,1,1,2,1,1,2,1,2,2,1,2,3,1,1,2,1,1,1,1,1,1,1,1,1,1]
    result=verify([j%2 for j,r in enumerate(runs) for _ in range(r)])
    assert result['energy']==241 and result['P']==result['Pprime']==26
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input',nargs='?');ap.add_argument('--bound',type=int)
    a=ap.parse_args()
    if a.input:
        d=json.loads(Path(a.input).read_text());r=verify(d['word'] if isinstance(d,dict) else d)
    else:r=incumbent()
    if a.bound is not None:assert r['energy']<=a.bound
    print(json.dumps(r))
