"""Hash public extrapolation sources plus the release-distributed P=3 chains."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXTRA = ROOT / "extrapolation"
OUT = EXTRA / "hashes/EXTRAPOLATION_SHA256.json"


def included(path: Path) -> bool:
    relative = path.relative_to(EXTRA).as_posix()
    if relative == "hashes/EXTRAPOLATION_SHA256.json":
        return False
    if relative.startswith("verifier_logs/"):
        return relative == "verifier_logs/.gitkeep"
    return "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}


def main() -> None:
    files = sorted(path for path in EXTRA.rglob("*") if path.is_file() and included(path))
    manifest = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in files
    }
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PUBLIC_MANIFEST_WRITTEN", "files": len(manifest),
                      "p03_chains": sum("/certificates/p03_s" in name for name in manifest)}))


if __name__ == "__main__":
    main()
