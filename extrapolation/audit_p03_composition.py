"""Check complete input binding, and reject missing/misbound coverage."""
from pathlib import Path
from unittest.mock import patch
import copy,json
from verify_p03_closure import bind_records
ROOT=Path(__file__).resolve().parent
cov=json.loads((ROOT/'verifier_logs/p03_coverage.json').read_text())
batch={'records':[dict(case_id=r['case_id'],
                       input=f"inputs/{r['case_id']}.json",
                       certificate=f"certificates/{r['case_id']}.json")
                  for r in cov['cases']]}
bound=bind_records(cov,batch);need_count=len(cov['cases'])
if len(bound)!=need_count:raise ValueError('missing original cases')
tests=[]
d=copy.deepcopy(batch);d['records'].pop();tests.append(('missing_record',d,None))
d=copy.deepcopy(batch);d['records'][-1]=copy.deepcopy(d['records'][0]);tests.append(('duplicate_record',d,None))
d=copy.deepcopy(batch);d['records'][0]['case_id']='not_in_layer';tests.append(('wrong_case',d,None))
first=bound[0];input_path=first[1];inp=json.loads(input_path.read_text())
for field in ('rho','norm','P'):
    d=copy.deepcopy(inp);d[field]+=1;tests.append(('wrong_'+field,batch,d))
original=Path.read_text;out=[]
for name,mutated,data in tests:
    def altered(path,*args,**kwargs):
        return json.dumps(data) if data is not None and path.resolve()==input_path.resolve() else original(path,*args,**kwargs)
    try:
        with patch.object(Path,'read_text',altered):bind_records(cov,mutated)
    except (ValueError,KeyError) as exc:out.append(dict(test=name,status='REJECT',reason=str(exc)))
    else:raise RuntimeError('accepted composition mutation '+name)
(ROOT/'verifier_logs/p03_composition_mutations.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(out),'composition mutations rejected')
