"""New checker controls, including false-NO and altered membership rejection."""
from pathlib import Path
import copy,json,sys
from verify_norm_chain import verify
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
inp=json.loads((BASE/'certificates/cm_inputs/positive67.json').read_text())
general=dict(P=0,support=[],positive_control=True,conductor=67,
             involution=inp['involution'],alpha=inp['alpha'],basis=inp['basis'])
doc=json.loads((BASE/'certificates/cm_outputs/control_certificate.json').read_text())
positive=verify(general,doc)
scaled=copy.deepcopy(doc);M=1+doc['prime'];last=scaled['steps'][-1]
last[1]=[M*a for a in last[1]]
last[2]=[M*M*a for a in last[2]]
last[3]=[[M*a for a in q] for q in last[3]]
last[4]=[[M*a for a in g] for g in last[4]]
scaled_control=verify(general,scaled)
if scaled_control['trace']!=M*M*positive['trace'] or scaled_control['coset_min_trace']!=positive['coset_min_trace']:
    raise RuntimeError('scale countermechanism failure')
results=[]
for name in ('fake_NO','wrong_alpha','wrong_membership','missing_step','composite','wrong_involution'):
    i=copy.deepcopy(general);d=copy.deepcopy(doc)
    if name=='fake_NO':d['status']='NO_CHAIN'
    if name=='wrong_alpha':i['alpha'][0]+=1
    if name=='wrong_membership':d['steps'][0][3][0][0]+=1
    if name=='missing_step':d['steps'].pop()
    if name=='composite':d['prime']=268
    if name=='wrong_involution':i['involution']='identity'
    try:verify(i,d)
    except ValueError as e:results.append(dict(test=name,status='REJECT',reason=str(e)))
    else:raise RuntimeError('accepted mutation '+name)
out=dict(status='PASS',positive=positive,scaled_positive=scaled_control,scale=M,mutations=results)
(ROOT/'verifier_logs/general_chain_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
