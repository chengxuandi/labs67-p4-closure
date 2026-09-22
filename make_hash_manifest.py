"""Regenerate the SHA-256 manifest for immutable replay inputs."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
files = sorted(p for p in (ROOT / 'certificates').rglob('*') if p.is_file())
manifest = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in files}
(ROOT / 'hashes').mkdir(exist_ok=True)
(ROOT / 'hashes' / 'FINAL_SHA256.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'WROTE {len(manifest)} SHA-256 entries')

