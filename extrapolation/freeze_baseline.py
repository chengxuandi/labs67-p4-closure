"""Replay the frozen theorem without writing anywhere outside extrapolation."""
from pathlib import Path
import hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
for name in ('signatures','inputs','certificates','verifier_logs','hashes'):
    (ROOT/name).mkdir(exist_ok=True)
paths=[p for p in BASE.rglob('*') if p.is_file() and
       'extrapolation' not in p.relative_to(BASE).parts and
       '.git' not in p.relative_to(BASE).parts and '__pycache__' not in p.parts]
before={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
cmd=[sys.executable,'-B',str(BASE/'verify_p4_closure.py'),'--output',str(ROOT/'verifier_logs/p4_replay.json')]
t=time.monotonic();r=subprocess.run(cmd,capture_output=True,timeout=120,cwd=BASE)
(ROOT/'verifier_logs/p4_replay.stdout').write_bytes(r.stdout)
(ROOT/'verifier_logs/p4_replay.stderr').write_bytes(r.stderr)
if r.returncode or b'P4_CLOSED' not in r.stdout:raise RuntimeError('Frozen theorem did not replay')
after={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
if before!=after:raise RuntimeError('Frozen baseline changed')
(ROOT/'hashes/FROZEN_P4.json').write_text(json.dumps(before,indent=2)+'\n')
record=dict(status='P4_CLOSED',command=cmd,seconds=time.monotonic()-t,frozen_files=len(before),unchanged=True)
(ROOT/'verifier_logs/p4_replay.run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
