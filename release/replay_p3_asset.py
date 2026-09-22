"""Self-contained replay entry point embedded in the P=3 release asset."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    [sys.executable, "-B", "extrapolation/verify_new_lemmas.py"],
    [sys.executable, "-B", "extrapolation/verify_layer_coverage.py", "3"],
    [sys.executable, "-B", "extrapolation/verify_p03_closure.py"],
    [sys.executable, "-B", "extrapolation/audit_layer_coverage_mutations.py"],
    [sys.executable, "-B", "extrapolation/audit_p03_composition.py"],
]


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for relative, expected in manifest.items():
        path = ROOT / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("asset manifest mismatch: " + relative)
    (ROOT / "extrapolation/verifier_logs").mkdir(exist_ok=True)
    for command in COMMANDS:
        print("RUN:", " ".join(command[1:]), flush=True)
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode:
            return completed.returncode
    print("P3_RELEASE_ASSET_REPLAY: PASS")
    print("GLOBAL OPTIMALITY: NOT CLAIMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
