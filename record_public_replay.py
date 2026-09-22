"""Record a privacy-clean replay transcript for release auditing."""
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
start = time.monotonic()
result = subprocess.run([sys.executable, 'replay_all.py'], cwd=ROOT,
                        capture_output=True, text=True)
record = {
    'command': ['python', 'replay_all.py'],
    'python': platform.python_version(),
    'os': platform.platform(),
    'exit_code': result.returncode,
    'runtime_seconds': time.monotonic() - start,
    'stdout': result.stdout,
    'stderr': result.stderr,
}
(ROOT / 'logs' / 'PREPUBLISH_REPLAY.json').write_text(json.dumps(record, indent=2) + '\n')
sys.stdout.write(result.stdout)
sys.stderr.write(result.stderr)
raise SystemExit(result.returncode)

