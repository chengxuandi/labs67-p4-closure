"""One template-matched proposal; fixed120s, no bare NO accepted."""
import argparse,ast,hashlib,json,math,subprocess,sys,time
from pathlib import Path
from verify_norm_chain import alpha_for,verify
ROOT=Path(__file__).resolve().parent
UP=Path('D:/ai4sc/LABS_N67/reopen_20260919/cm_inputs')
sys.set_int_max_str_digits(100000)

def run(row):
    cid=row['case_id'];R=row['norm'];rho=row['rho'];p=68
    while not (R%p and all(p%d for d in range(2,math.isqrt(p)+1))):p+=67
    inp=dict(row,conductor=67,involution='zeta -> zeta^-1',alpha=alpha_for(row['support']))
    ip=ROOT/'inputs'/f'{cid}.json';ip.write_text(json.dumps(inp)+'\n')
    poly='17'+''.join(f'+({z})*(\'x^{k}+\'x^{67-k})' for z,k in row['support'])
    script=ROOT/'inputs'/f'{cid}.gp'
    script.write_text('default(parisizemax,1000000000);default(realprecision,100);\n'
         'read("Gentry_Szydlo.gp");\n'+f'read("{(UP/"certificate_kernel.gp").as_posix()}");\n'
         f'nf=nfinit(polcyclo(67));R={R};rho={rho};alpha=Mod({poly},nf.pol);\n'
         f'id=idealhnf(nf,R,\'x-rho);make_cert(id,alpha,[R,Mod(\'x-rho,nf.pol)],{p});quit;\n')
    cmd=[str(UP/'gp64-gmp-git-latest.exe'),'-q','-f',str(script)];start=time.monotonic()
    try:
        process=subprocess.run(cmd,cwd=UP/'module_lip_upstream/attack/Gentry_Szydlo/gp',capture_output=True,timeout=120)
        stdout,stderr=process.stdout,process.stderr;code=process.returncode
    except subprocess.TimeoutExpired as e:stdout,stderr=e.stdout or b'',e.stderr or b'';code='TIMEOUT'
    prefix=ROOT/'verifier_logs'/cid
    prefix.with_suffix('.stdout').write_bytes(stdout);prefix.with_suffix('.stderr').write_bytes(stderr)
    rec=dict(case_id=cid,command=cmd,solver_exit=code,seconds=time.monotonic()-start,
             limit=120,status='OPEN',input=str(ip.relative_to(ROOT)))
    lines=[line[5:] for line in stdout.decode(errors='replace').splitlines() if line.startswith('CERT=')]
    if len(lines)==1:
        doc=dict(status='NO_CHAIN',prime=p,base_generators=[[R]+[0]*65,[-rho,1]+[0]*64],steps=ast.literal_eval(lines[0]))
        cp=ROOT/'certificates'/f'{cid}.json';cp.write_text(json.dumps(doc)+'\n');rec['certificate']=str(cp.relative_to(ROOT))
        # A fresh independent process checks each proposed proof.
        vc=[sys.executable,'-B',str(ROOT/'verify_norm_chain.py'),str(ip),str(cp)]
        check=subprocess.run(vc,capture_output=True,timeout=60)
        (ROOT/'verifier_logs'/f'{cid}.verify.stdout').write_bytes(check.stdout)
        (ROOT/'verifier_logs'/f'{cid}.verify.stderr').write_bytes(check.stderr)
        rec.update(verifier_command=vc,verifier_exit=check.returncode)
        if check.returncode==0:
            rec['result']=json.loads(check.stdout);rec['status']=rec['result']['status']
            rec['certificate_bytes']=cp.stat().st_size
            rec['certificate_sha256']=hashlib.sha256(cp.read_bytes()).hexdigest()
        else:rec['reason']='No accepted finite contradiction; not a NO claim'
    prefix.with_suffix('.run.json').write_text(json.dumps(rec,indent=2)+'\n')
    return rec
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('case_id');a.add_argument('--P',type=int,default=3);args=a.parse_args()
    rows=json.loads((ROOT/'inputs'/f'p{args.P:02}_cases.json').read_text())
    row=next(r for r in rows if r['case_id']==args.case_id)
    print(json.dumps(run(row)))
