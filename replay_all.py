"""One-command, standard-library replay of the public P=4 artifact."""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def fail(message):
    print('FAIL:', message, file=sys.stderr)
    raise SystemExit(1)

manifest_path = ROOT / 'hashes' / 'FINAL_SHA256.json'
manifest = json.loads(manifest_path.read_text())
for relative, expected in manifest.items():
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        fail('missing or unsafe manifest path: ' + relative)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        fail('hash mismatch: ' + relative)
print(f'HASHES: VERIFIED ({len(manifest)} files)')

def run(script, expected):
    start = time.monotonic()
    result = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT,
                            capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        fail(f'{script} exited {result.returncode}')
    if expected not in result.stdout:
        fail(f'{script} did not print the expected conclusion')
    print(f'{script}: PASS ({time.monotonic() - start:.3f}s)')

run('verify_sequence.py', '"energy": 241')
run('verify_p4_closure.py', 'P4_CLOSED: 32/32 support orbits excluded')
run('p4_closure_mutation_tests.py', '"mutations_rejected": 7')
print('LABS N=67 P=4 CLOSURE: VERIFIED')
print('GLOBAL OPTIMALITY: NOT CLAIMED')

