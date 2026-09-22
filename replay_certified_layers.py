"""Unified exact replay of the published P=3 and frozen P=4 layers."""
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    [sys.executable, "-B", "verify_extrapolation_manifest.py"],
    [sys.executable, "-B", "verify_p4_closure.py"],
    [sys.executable, "-B", "extrapolation/verify_new_lemmas.py"],
    [sys.executable, "-B", "extrapolation/verify_layer_coverage.py", "3"],
    [sys.executable, "-B", "extrapolation/verify_p03_closure.py"],
    [sys.executable, "-B", "extrapolation/audit_layer_coverage_mutations.py"],
    [sys.executable, "-B", "extrapolation/audit_p03_composition.py"],
]


def main() -> int:
    for command in COMMANDS:
        start = time.monotonic()
        print("RUN:", " ".join(command[1:]), flush=True)
        completed = subprocess.run(command, cwd=ROOT)
        elapsed = time.monotonic() - start
        print(f"EXIT={completed.returncode} SECONDS={elapsed:.3f}", flush=True)
        if completed.returncode:
            return completed.returncode
    print("LABS N=67 CERTIFIED LAYERS: P=3 AND P=4 VERIFIED")
    print("COMBINED EXCLUSION: P,P' NOT IN {1,2,3,4}")
    print("GLOBAL OPTIMALITY: NOT CLAIMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
