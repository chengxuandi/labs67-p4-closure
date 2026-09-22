"""Adversarial checks of the composition layer, without touching original data."""
import contextlib
import copy
import io
import json
from pathlib import Path
from unittest.mock import patch
import verify_p4_closure as closure

ROOT = Path(__file__).resolve().parent
CERT = ROOT / 'certificates'
original_read = Path.read_text
reps_path = CERT / 'cm_representative_cases.json'
records_path = CERT / 'cm_batch_results.json'
reps = json.loads(reps_path.read_text())
records = json.loads(records_path.read_text())
first = next(r for r in records if r['case_id'] == 'b5_pair0')
input_path = (ROOT / first['input'].replace('\\', '/')).resolve()
cert_path = (ROOT / first['certificate'].replace('\\', '/')).resolve()
inp = json.loads(input_path.read_text())
cert = json.loads(cert_path.read_text())
tests = []
tests.append(('missing_representative', {reps_path: reps[:-1]}))
r = copy.deepcopy(reps); r[-1] = copy.deepcopy(r[0])
tests.append(('duplicate_representative', {reps_path: r}))
tests.append(('missing_result', {records_path: records[:-1]}))
r = copy.deepcopy(records); r[-1] = copy.deepcopy(r[0])
tests.append(('duplicate_result', {records_path: r}))
i = copy.deepcopy(inp); i['rho'] += 1
tests.append(('wrong_input_binding', {input_path: i}))
c = copy.deepcopy(cert); c['status'] = 'UNKNOWN'
tests.append(('unknown_as_proof', {cert_path: c}))
c = copy.deepcopy(cert); c['steps'].pop()
tests.append(('truncated_chain', {cert_path: c}))

results = []
for name, replacements in tests:
    replacements = {p.resolve(): json.dumps(v) for p, v in replacements.items()}
    def altered_read(path, *args, **kwargs):
        if path.resolve() in replacements:
            return replacements[path.resolve()]
        return original_read(path, *args, **kwargs)
    try:
        with patch.object(Path, 'read_text', altered_read), contextlib.redirect_stdout(io.StringIO()):
            closure.check()
    except (ValueError, KeyError) as exc:
        results.append(dict(test=name, status='REJECT', message=str(exc)))
        print(name, 'REJECT', str(exc), flush=True)
    else:
        raise RuntimeError('Accepted invalid composition: ' + name)
print(json.dumps({'status': 'PASS', 'mutations_rejected': len(results)}))
