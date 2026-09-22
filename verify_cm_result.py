"""Independent polarized ideal verifier, Python standard library.

Usage: python verify_cm_result.py INPUT.json RESULT.json [--mutations]
Does not trust solver, old generators, Gram reduction, embeddings, or LLL.
Bare NO / UNKNOWN is not accepted. NO_CHAIN requires an exact GS transcript
and an explicit final norm-versus-residue contradiction.
"""
import argparse, copy, json, sys
from fractions import Fraction
from pathlib import Path

N=67; D=66
sys.set_int_max_str_digits(100000)
def require(ok,msg):
    if not ok: raise ValueError(msg)
def red(v):
    require(len(v)<=N,'polynomial length')
    v=list(v)+[0]*(N-len(v))
    return [c-v[-1] for c in v[:-1]]
def mul(a,b):
    c=[0]*N
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[(i+j)%N]+=x*y
    return red(c)
def conjugate(a):
    c=[0]*N
    for i,x in enumerate(a): c[-i%N]+=x
    return red(c)
def shift(a):
    return mul(a,[0,1])
def det(a):
    a=[r[:] for r in a]; old=1;sign=1
    for k in range(len(a)-1):
        p=next((i for i in range(k,len(a)) if a[i][k]),None)
        if p is None:return 0
        if p!=k:a[k],a[p]=a[p],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                num=pivot*a[i][j]-a[i][k]*a[k][j]
                require(num%old==0,'nonexact determinant division')
                a[i][j]=num//old
            a[i][k]=0
        old=pivot
    return sign*a[-1][-1]
def row_coordinates(B, rows):
    # Solve all row membership equations by exact Gauss-Jordan.
    A=[[Fraction(B[j][i]) for j in range(D)]+[Fraction(r[i]) for r in rows]
       for i in range(D)]
    for k in range(D):
        p=next((i for i in range(k,D) if A[i][k]),None)
        require(p is not None,'singular ideal basis')
        A[k],A[p]=A[p],A[k]; q=A[k][k]
        A[k]=[x/q for x in A[k]]
        for i in range(D):
            if i!=k and A[i][k]:
                q=A[i][k]; A[i]=[x-q*y for x,y in zip(A[i],A[k])]
    return [[A[i][D+j] for i in range(D)] for j in range(len(rows))]
def verify(inp,result):
    require(inp['conductor']==67 and inp['modulus']==[1]*67,'field mismatch')
    require(inp['involution']=='zeta -> zeta^-1','involution mismatch')
    B=inp['basis'];alpha=inp['alpha']
    require(len(B)==D and all(len(r)==D for r in B),'basis shape')
    require(all(type(x) is int for r in B for x in r),'basis must be integral')
    require(len(alpha)==D and all(type(x) is int for x in alpha),'alpha format')
    if inp['case']=='positive67':
        require(alpha==[17]+[0]*65 and inp['ideal_index']==17**33,'control interface')
    elif inp['case'] in ('b13','p4'):
        b=13 if inp['case']=='b13' else inp['b'];require(type(b) is int and 2<=b<=33,'support range')
        p=[0]*67;p[0]=17;p[1]=p[66]=1;p[b]=p[67-b]=-1
        require(alpha==red(p),'P4 interface')
        R=inp['ideal_index']
        require(type(R) is int and R>1,'P4 index interface')
        if inp['case']=='b13':require(R==31806854896213121365583994489006030403217,'b13 index')
        rho=inp['rho']
        expected=[[R]+[0]*65]+[[-pow(rho,i,R)]+[int(i==j) for j in range(1,66)]
                                 for i in range(1,66)]
        require(B==expected,'b13 ideal basis mismatch')
    else:raise ValueError('unknown pinned case')
    require(conjugate(alpha)==alpha,'nonreal polarization')
    require(result['status']=='YES','NO/UNKNOWN is not a verified absence certificate')
    beta=result['beta']
    require(len(beta)==D and all(type(x) is int for x in beta),'generator format')
    require(any(beta),'zero generator')
    require(mul(beta,conjugate(beta))==alpha,'full relative norm mismatch')
    coords=row_coordinates(B,[beta]+[shift(r) for r in B])
    require(all(c.denominator==1 for row in coords for c in row),'membership/ideal closure failure')
    index=abs(det(B))
    require(index==inp['ideal_index'] and index>0,'ideal index mismatch')
    cols=[];v=beta
    for _ in range(D): cols.append(v);v=shift(v)
    require(abs(det(cols))==index,'principal ideal index mismatch')
    return {'status':'PASS','case':inp['case'],'index':index,
            'proves':'beta in I, O beta = I, beta conjugate(beta) = alpha'}
def mutations(inp,result):
    cases=[]
    a=copy.deepcopy(inp);a['basis'][0]=[2*x for x in a['basis'][0]];cases.append(('ideal',a,result))
    a=copy.deepcopy(inp);a['alpha'][0]+=1;cases.append(('alpha',a,result))
    a=copy.deepcopy(inp);a['involution']='identity';cases.append(('involution',a,result))
    b=copy.deepcopy(result);b['beta'][0]+=1;cases.append(('generator',inp,b))
    b=copy.deepcopy(result);b['status']='NO';cases.append(('unsupported_NO',inp,b))
    for name,a,b in cases:
        try:verify(a,b)
        except (ValueError,KeyError,ZeroDivisionError):print('REJECT',name)
        else:raise ValueError('accepted mutation '+name)
def verify_chain(inp,doc):
    """Verify a GS necessary-condition contradiction, not an incomplete search.

    Each certificate membership is an explicit O-linear polynomial identity.
    No HNF, ideal factorization, LLL, algebraic embeddings, or root solver is trusted.
    """
    require(inp['conductor']==67 and inp['modulus']==[1]*67,'field mismatch')
    require(inp['involution']=='zeta -> zeta^-1','involution mismatch')
    alpha=inp['alpha']; B=inp['basis']; gg0=doc['base_generators']
    def poly(a):
        require(len(a)==66 and all(type(x) is int for x in a),'integer polynomial expected')
    poly(alpha)
    if inp['case'] in ('b13','p4'):
        b=13 if inp['case']=='b13' else inp['b'];require(type(b) is int and 2<=b<=33,'support range')
        p=[0]*67;p[0]=17;p[1]=p[66]=1;p[b]=p[67-b]=-1
        require(alpha==red(p),'P4 polarization mismatch')
        R=inp['ideal_index'];rho=inp['rho']
        require(type(R) is int and R>1,'P4 ideal index')
        if inp['case']=='b13':require(R==31806854896213121365583994489006030403217,'b13 ideal index')
        require(B==[[R]+[0]*65]+[[-pow(rho,i,R)]+[int(i==j) for j in range(1,66)] for i in range(1,66)],'b13 basis mismatch')
        for g in gg0:
            poly(g);require(sum(v*pow(rho,i,R) for i,v in enumerate(g))%R==0,'initial ideal membership')
    elif inp['case']=='positive67':
        require(alpha==[17]+[0]*65,'positive polarization mismatch')
        for g in gg0:poly(g)
        require(all(c.denominator==1 for row in row_coordinates(B,gg0) for c in row),'initial ideal membership')
    else:raise ValueError('unknown pinned case')
    P=doc['prime']
    require(type(P) is int and P>2 and P%67==1,'prime must split completely')
    require(all(P%d for d in range(2,__import__('math').isqrt(P)+1)),'composite modulus')
    one=[1]+[0]*65
    def mp(a,b):return [c%P for c in mul(a,b)]
    def pw(a,n):
        r=one
        while n:
            if n&1:r=mp(r,a)
            a=mp(a,a);n>>=1
        return r
    def inv(a):
        require(pw(a,P-1)==one,'nonunit norm modulo P')
        return pw(a,P-2)
    def comb(raw,qs):
        require(len(qs)==len(raw),'wrong membership term count')
        s=[0]*66
        for a,q in zip(raw,qs):
            poly(q);s=[x+y for x,y in zip(s,mul(a,q))]
        return s
    inv(alpha)
    eta=alpha;gg=gg0;F=[x%P for x in alpha]
    digits=[int(c) for c in bin(P-1)[3:]]
    require(len(doc['steps'])==len(digits),'incomplete exponent chain')
    for step,c in zip(doc['steps'],digits):
        require(len(step)==6 and step[0]==c,'wrong binary step')
        _,w,eta1,wcoef,gg1,gcoef=step
        poly(w);poly(eta1)
        require(len(gg1)==len(gcoef) and len(gg1)>0,'next generator count')
        raw=[]
        for i,a in enumerate(gg):
            for b in gg[i:]:
                product=mul(a,b)
                raw.extend([mul(product,g) for g in gg0] if c else [product])
        nop=mul(eta,eta)
        if c:nop=mul(nop,alpha)
        require(comb(raw,wcoef)==w,'w membership identity failed')
        require(mul(eta1,nop)==mul(w,conjugate(w)),'relative norm recurrence failed')
        for g,qs in zip(gg1,gcoef):
            poly(g)
            require(mul(nop,g)==mul(conjugate(w),comb(raw,qs)),'next-ideal membership failed')
        inv_eta=inv(eta)
        F=mp(mp(mp(F,F),w),mp(inv_eta,inv_eta))
        inv(eta1)
        gg=gg1;eta=eta1
    T=67*eta[0]-sum(eta)
    require(T>=0,'negative trace can be separately excluded, unsupported format')
    center=[r if 2*r<=P else r-P for r in F]
    bad=[i for i,r in enumerate(center) if 67*r*r>2*T]
    if doc['status']=='NO_CHAIN':
        require(bad,'no coefficient-norm contradiction')
        return {'status':'PASS_NO','case':inp['case'],'prime':P,'exponent':P-1,
                'steps':len(digits),'trace':T,'coefficient_index':bad[0],
                'residue':center[bad[0]],'proves':'No beta with O beta = I and beta conjugate(beta) = alpha'}
    require(doc['status']=='CONTROL_CHAIN','unsupported chain conclusion')
    require(not bad and 67*P*P>8*T,'positive chain lifting check')
    require(mul(center,conjugate(center))==eta,'positive endpoint norm mismatch')
    return {'status':'PASS_CONTROL_CHAIN','trace':T,'steps':len(digits)}
def chain_mutations(inp,doc):
    cases=[]
    a=copy.deepcopy(inp);a['alpha'][0]+=1;cases.append(('alpha',a,doc))
    a=copy.deepcopy(inp);a['involution']='identity';cases.append(('involution',a,doc))
    b=copy.deepcopy(doc);b['steps'][0][3][0][0]+=1;cases.append(('membership',inp,b))
    b=copy.deepcopy(doc);b['steps'][0][2][0]+=1;cases.append(('norm',inp,b))
    b=copy.deepcopy(doc);b['steps'][0][4][0][0]+=1;cases.append(('next_generator',inp,b))
    b=copy.deepcopy(doc);b['steps'].pop();cases.append(('missing_step',inp,b))
    b=copy.deepcopy(doc);b['prime']=268;cases.append(('prime',inp,b))
    for name,a,b in cases:
        try:verify_chain(a,b)
        except (ValueError,KeyError,ZeroDivisionError):print('REJECT',name)
        else:raise ValueError('accepted chain mutation '+name)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('result');ap.add_argument('--mutations',action='store_true');args=ap.parse_args()
    inp=json.loads(Path(args.input).read_text());result=json.loads(Path(args.result).read_text())
    ischain=result['status'] in ('NO_CHAIN','CONTROL_CHAIN')
    print(json.dumps(verify_chain(inp,result) if ischain else verify(inp,result)))
    if args.mutations:
        (chain_mutations if ischain else mutations)(inp,result)
if __name__=='__main__':main()
