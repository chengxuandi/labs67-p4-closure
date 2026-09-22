"""General signature CM chain verifier; integers only, no discovery imports."""
from pathlib import Path
import argparse,json,math,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from verify_cm_result import mul,conjugate,red,row_coordinates
from verify_new_lemmas import need,coset_bound
sys.set_int_max_str_digits(100000)

def alpha_for(support):
    a=[17]+[0]*66
    for z,k in support:a[k]+=z;a[67-k]+=z
    return red(a)
def verify(inp,doc):
    need(inp['conductor']==67 and inp['involution']=='zeta -> zeta^-1','field interface')
    support=inp['support'];P=inp['P']
    need(len({k for z,k in support})==len(support),'duplicate shifts')
    need(all(type(z) is int and type(k) is int and 1<=k<=33 and z!=0 for z,k in support),'support format')
    need(sum(z*(2*z-1) for z,k in support)==P,'penalty binding')
    sigma=sum(z for z,k in support)
    need(sigma>=0 and math.isqrt(1+8*sigma)**2==1+8*sigma,'balance square')
    alpha=alpha_for(support);need(alpha==inp['alpha'],'full polarization binding')
    def poly(a):need(len(a)==66 and all(type(x) is int for x in a),'integer power basis polynomial')
    initial=doc['base_generators'];need(bool(initial),'empty initial module')
    if inp.get('positive_control'):
        need(P==0 and alpha==[17]+[0]*65,'positive control interface')
        for g in initial:poly(g)
        need(all(c.denominator==1 for row in row_coordinates(inp['basis'],initial) for c in row),'positive membership')
    else:
        R=inp['norm'];rho=inp['rho'];need(type(R) is int and R>0 and 0<=rho<R,'CRT ideal data')
        # Validity of the ideal and I bar(I)=alpha O are independently checked by coverage.
        for g in initial:
            poly(g);need(sum(a*pow(rho,j,R) for j,a in enumerate(g))%R==0,'initial ideal membership')
    p=doc['prime']
    need(type(p) is int and p>2 and p%67==1 and all(p%d for d in range(2,math.isqrt(p)+1)),'split prime')
    one=[1]+[0]*65
    def mp(a,b):return [x%p for x in mul(a,b)]
    def power(a,e):
        r=one
        while e:
            if e&1:r=mp(r,a)
            a=mp(a,a);e>>=1
        return r
    def inverse(a):
        need(power(a,p-1)==one,'nonunit denominator');return power(a,p-2)
    def combination(gens,coeff):
        need(len(gens)==len(coeff),'membership dimension');out=[0]*66
        for g,q in zip(gens,coeff):poly(q);out=[a+b for a,b in zip(out,mul(g,q))]
        return out
    inverse(alpha);eta=alpha;gens=initial;F=[x%p for x in alpha]
    digits=list(map(int,bin(p-1)[3:]))
    need(len(doc['steps'])==len(digits),'incomplete exponent chain')
    for step,bit in zip(doc['steps'],digits):
        need(len(step)==6 and step[0]==bit,'wrong exponent step')
        _,w,eta1,wc,gn,gc=step;poly(w);poly(eta1)
        need(len(gn)>0 and len(gn)==len(gc),'next module shape')
        raw=[]
        for i,a in enumerate(gens):
            for b in gens[i:]:
                r=mul(a,b);raw.extend([mul(r,g) for g in initial] if bit else [r])
        d=mul(eta,eta)
        if bit:d=mul(d,alpha)
        need(combination(raw,wc)==w,'w member identity')
        need(mul(eta1,d)==mul(w,conjugate(w)),'norm recurrence')
        for g,c in zip(gn,gc):
            poly(g);need(mul(d,g)==mul(conjugate(w),combination(raw,c)),'next member identity')
        inv=inverse(eta);F=mp(mp(mp(F,F),w),mp(inv,inv))
        inverse(eta1);eta=eta1;gens=gn
    trace=67*eta[0]-sum(eta);need(trace>=0,'unsupported negative trace')
    bound=coset_bound(F,p);center=[a if 2*a<=p else a-p for a in F]
    scalar=max(67*a*a for a in center)
    if doc['status']=='NO_CHAIN':
        need(bound>trace,'no coset-norm contradiction')
        return dict(status='PASS_NO',P=P,prime=p,steps=len(digits),trace=trace,coset_min_trace=bound,
                    scalar_max_twice_bound=scalar,old_scalar_would_close=scalar>2*trace)
    need(doc['status']=='CONTROL_CHAIN' and bound<=trace,'control contradiction')
    return dict(status='PASS_CONTROL_CHAIN',trace=trace,coset_min_trace=bound)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('certificate');a=ap.parse_args()
    print(json.dumps(verify(json.loads(Path(a.input).read_text()),json.loads(Path(a.certificate).read_text()))))
