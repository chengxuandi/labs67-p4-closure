"""Verify every public extrapolation file, including release-asset chains."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "extrapolation/hashes/EXTRAPOLATION_SHA256.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    for relative, expected in manifest.items():
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError("manifest file missing: " + relative)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError("manifest hash mismatch: " + relative)
    chains = sum("/certificates/p03_s" in name for name in manifest)
    if chains != 192:
        raise ValueError(f"expected 192 chain entries, found {chains}")
    print(f"EXTRAPOLATION_MANIFEST_PASS: {len(manifest)} files, {chains} P3 chains")


if __name__ == "__main__":
    main()
