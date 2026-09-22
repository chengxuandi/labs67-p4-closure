"""Package existing P=3 certificates; never discovers or changes them."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release/P3_CLOSURE_CERTIFICATE.zip"
PREFIX = "P3_CLOSURE_CERTIFICATE/"

STATIC = [
    "LICENSE",
    "verify_cm_coverage.py",
    "verify_cm_result.py",
    "certificates/cm_inputs/positive67.json",
    "certificates/cm_outputs/control_certificate.json",
    "extrapolation/audit_general_chain.py",
    "extrapolation/audit_layer_coverage_mutations.py",
    "extrapolation/audit_p03_composition.py",
    "extrapolation/verify_layer_coverage.py",
    "extrapolation/verify_new_lemmas.py",
    "extrapolation/verify_norm_chain.py",
    "extrapolation/verify_p03_closure.py",
    "extrapolation/certificates/p03_coverage.json",
]


def members():
    paths = [ROOT / name for name in STATIC]
    paths += sorted((ROOT / "extrapolation/signatures").glob("P*.json"))
    paths += sorted((ROOT / "extrapolation/inputs").glob("p03_s*.json"))
    paths += sorted((ROOT / "extrapolation/certificates").glob("p03_s*.json"))
    if len(list((ROOT / "extrapolation/certificates").glob("p03_s*.json"))) != 192:
        raise ValueError("expected exactly 192 P=3 chain certificates")
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    return sorted(set(paths))


def add_bytes(archive, name, data):
    info = zipfile.ZipInfo(PREFIX + name, (2026, 9, 22, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compresslevel=6)


def main():
    files = members()
    payload = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in files}
    payload["README.md"] = (ROOT / "release/P3_ASSET_README.md").read_bytes()
    payload["replay_p3_asset.py"] = (ROOT / "release/replay_p3_asset.py").read_bytes()
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())}
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", allowZip64=True) as archive:
        for name, data in sorted(payload.items()):
            add_bytes(archive, name, data)
        add_bytes(archive, "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(json.dumps({"asset": str(OUT), "sha256": digest,
                      "bytes": OUT.stat().st_size, "files": len(payload),
                      "p03_chains": 192}))


if __name__ == "__main__":
    main()
