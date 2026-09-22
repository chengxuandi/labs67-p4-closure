"""Coverage mutation checks use in-memory replacements; original files unchanged."""
from pathlib import Path
from unittest.mock import patch
import copy,json
from verify_layer_coverage import verify
ROOT=Path(__file__).resolve().parent;path=ROOT/'certificates/p03_coverage.json'
doc=json.loads(path.read_text());original=Path.read_text
tests=[]
d=copy.deepcopy(doc);d['rows'].pop();tests.append(('missing_support',d))
d=copy.deepcopy(doc);d['rows'][1]=d['rows'][0];tests.append(('duplicate_support',d))
d=copy.deepcopy(doc);d['rows'][0]['norm']+=1;tests.append(('wrong_norm',d))
for name in ('missing_factor','wrong_root','missing_ideal','missing_pair'):
    d=copy.deepcopy(doc);r=next(r for r in d['rows'] if r['kind']=='survivor')
    if name=='missing_factor':r['factors'].pop()
    if name=='wrong_root':r['roots'][0]['roots'][0]=1
    if name=='missing_ideal':r['all_rho'].pop()
    if name=='missing_pair':r['conjugate_pairs'].pop()
    tests.append((name,d))
d=copy.deepcopy(doc);d['prime_nodes']['67']['witnesses'][0]=1;tests.append(('wrong_prime_witness',d))
out=[]
for name,d in tests:
    def altered(p,*args,**kwargs):
        return json.dumps(d) if p.resolve()==path.resolve() else original(p,*args,**kwargs)
    try:
        with patch.object(Path,'read_text',altered):verify(path)
    except (ValueError,KeyError,ZeroDivisionError) as exc:out.append(dict(test=name,status='REJECT',reason=str(exc)))
    else:raise RuntimeError('accepted mutation '+name)
(ROOT/'verifier_logs/p03_coverage_mutations.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(out),'coverage mutations rejected')
