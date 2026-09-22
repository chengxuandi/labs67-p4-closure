"""Read-only mathematical results; verify dependency hashes, then refresh inventory."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
closed=json.loads((ROOT/'verifier_logs/p03_closure.json').read_text())
if closed['status']!='P3_CLOSED':raise ValueError('No accepted closure')
for relative,value in closed['sha256'].items():
    if sha(BASE/relative)!=value:raise ValueError('Changed P3 proof dependency: '+relative)
frozen=json.loads((ROOT/'hashes/FROZEN_P4.json').read_text())
for relative,value in frozen.items():
    if sha(BASE/relative)!=value:raise ValueError('Changed frozen P4 dependency: '+relative)
files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='EXTRAPOLATION_SHA256.json']
manifest={p.relative_to(BASE).as_posix():sha(p) for p in sorted(files)}
target=ROOT/'hashes/EXTRAPOLATION_SHA256.json';target.write_text(json.dumps(manifest,indent=2)+'\n')
for relative,value in manifest.items():
    if sha(BASE/relative)!=value:raise ValueError('Inventory hash mismatch')
print(json.dumps(dict(status='SEALED',new_files=len(manifest),frozen_files=len(frozen),
                      P3_dependency_hashes='UNCHANGED',manifest_sha256=sha(target))))
