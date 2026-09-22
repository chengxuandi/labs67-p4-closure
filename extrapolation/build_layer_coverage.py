"""Untrusted positioned-layer arithmetic certificate producer (P3 first)."""
from pathlib import Path
from itertools import product
from math import gcd
import argparse,ast,csv,json,subprocess,sys
import sympy as sp
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
sys.path.insert(0,str(BASE));import verify_cm_coverage as arithmetic
sys.set_int_max_str_digits(100000)
GP=Path('D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs/gp64-gmp-git-latest.exe')
OLD=Path('D:/ai4sc/LABS_N67/low_periodic_classification')

def prime_certificate(targets):
    nodes=json.loads((BASE/'certificates/cm_coverage_certificate.json').read_text())['prime_nodes']
    checkpoint=ROOT/'inputs/prime_nodes.json'
    if checkpoint.exists():nodes.update(json.loads(checkpoint.read_text()))
    def build(n):
        if str(n) in nodes:return
        factors=sorted((int(q),int(e)) for q,e in sp.factorint(n-1,limit=2000).items())
        if not all(sp.isprime(q) for q,e in factors):
            code=f'm=factor({n-1});print("FACTORS=",vector(matsize(m)[1],i,[m[i,1],m[i,2]]));quit;\n'
            r=subprocess.run([str(GP),'-q','-f'],input=code,text=True,capture_output=True,timeout=30)
            lines=[line[8:] for line in r.stdout.splitlines() if line.startswith('FACTORS=')]
            if len(lines)!=1:raise RuntimeError('UNKNOWN prime-factor proposal')
            factors=sorted(map(tuple,ast.literal_eval(lines[0])))
        if not all(sp.isprime(q) for q,e in factors):raise RuntimeError('unfactored cofactor')
        witnesses=[]
        for q,e in factors:
            build(q)
            for a in range(2,10000):
                if pow(a,n-1,n)==1 and gcd(pow(a,(n-1)//q,n)-1,n)==1:witnesses.append(a);break
            else:raise RuntimeError('No Lucas witness (not NO norm)')
        nodes[str(n)]=dict(factors=factors,witnesses=witnesses)
        checkpoint.write_text(json.dumps(nodes)+'\n')
    for j,p in enumerate(sorted(targets)):
        print('PRIME',j+1,len(targets),p,flush=True);build(p)
    arithmetic.check_primes(nodes,targets)
    return nodes

def main(P):
    with (OLD/'lowp_orbit_norm_certificate.csv').open() as f:legacy=[r for r in csv.DictReader(f) if int(r['penalty'])==P]
    with (OLD/f'p{P}_survivor_full_factorization.csv').open() as f:factor_map={r['support']:r for r in csv.DictReader(f)}
    x=sp.Symbol('x');phi=sp.Poly(sum(x**i for i in range(67)),x)
    rows=[];cases=[];targets={67}
    for index,old in enumerate(legacy):
        support=[list(map(int,s.split(':'))) for s in old['support'].split(';')]
        R=int(old['norm']);row=dict(support=support,norm=R,kind=old['status'])
        if old['status']=='obstructed':
            row.update(prime=int(old['prime']),valuation=int(old['valuation']),gcd_degree=int(old['gcd_degree']))
            targets.add(row['prime']);rows.append(row);continue
        fr=factor_map[old['support']];fs=[list(map(int,s.split('^'))) for s in fr['prime_factorization'].split(';')]
        if not all(e==1 and p%67==1 for p,e in fs):raise RuntimeError('non-simple ideal decomposition: new coverage required')
        alpha=17+sum(z*(x**k+x**(67-k)) for z,k in support)
        root_data=[]
        for p,e in fs:
            g=sp.gcd(phi.set_modulus(p),sp.Poly(alpha,x,modulus=p)).monic()
            if g.degree()!=2:raise RuntimeError('nonquadratic gcd: not covered by CRT template')
            a,b,c=[int(v)%p for v in g.all_coeffs()]
            square=int(sp.sqrt_mod((b*b-4*c)%p,p));r=(-b+square)*pow(2,-1,p)%p
            roots=sorted((r,pow(r,-1,p)));root_data.append(dict(prime=p,roots=roots));targets.add(p)
        residues=[]
        for bits in product((0,1),repeat=len(fs)):
            rho=sum(q['roots'][bit]*(R//p)*pow(R//p,-1,p) for (p,e),q,bit in zip(fs,root_data,bits))%R
            residues.append(rho)
        pairs=sorted((r,pow(r,-1,R)) for r in residues if r<pow(r,-1,R))
        row.update(factors=fs,roots=root_data,all_rho=sorted(residues),conjugate_pairs=pairs)
        for j,(rho,conj) in enumerate(pairs):
            cases.append(dict(case_id=f'p{P:02}_s{index:03}_i{j}',P=P,support=support,norm=R,rho=rho,conjugate_rho=conj))
        rows.append(row)
        print('SUPPORT',index,len(legacy),len(pairs),flush=True)
    nodes=prime_certificate(targets)
    doc=dict(schema='lowp-layer-coverage-v1',P=P,rows=rows,prime_nodes=nodes)
    (ROOT/'certificates'/f'p{P:02}_coverage.json').write_text(json.dumps(doc,indent=2)+'\n')
    cases.sort(key=lambda r:(len(str(r['norm'])),r['case_id']))
    (ROOT/'inputs'/f'p{P:02}_cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    print('COVERAGE PROPOSED',P,len(rows),len(cases),'representatives')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('P',type=int,choices=(3,5));a=ap.parse_args();main(a.P)
