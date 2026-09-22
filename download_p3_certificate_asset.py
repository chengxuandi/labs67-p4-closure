"""Download, hash-check, and install the v1.1.0 P=3 certificate asset."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
ASSET = "P3_CLOSURE_CERTIFICATE.zip"
URL = "https://github.com/chengxuandi/labs67-p4-closure/releases/download/v1.1.0/" + ASSET


def expected_digest() -> str:
    line = (ROOT / "hashes/P3_RELEASE_ASSET_SHA256.txt").read_text(encoding="ascii").strip()
    digest, name = line.split(None, 1)
    if name.strip().lstrip("*") != ASSET or len(digest) != 64:
        raise ValueError("invalid release-asset digest file")
    return digest.lower()


def safe_members(archive: zipfile.ZipFile):
    for info in archive.infolist():
        path = Path(info.filename)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("unsafe archive member: " + info.filename)
        yield info


def main() -> None:
    digest = expected_digest()
    with tempfile.TemporaryDirectory(prefix="labs67-p3-") as temporary:
        target = Path(temporary) / ASSET
        print("Downloading", URL, flush=True)
        with urllib.request.urlopen(URL) as response, target.open("wb") as output:
            shutil.copyfileobj(response, output)
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f"SHA-256 mismatch: {actual} != {digest}")
        with zipfile.ZipFile(target) as archive:
            manifest = json.loads(archive.read("P3_CLOSURE_CERTIFICATE/manifest.json"))
            certs = [name for name in manifest if name.startswith("extrapolation/certificates/p03_s")]
            if len(certs) != 192:
                raise ValueError("release asset does not contain exactly 192 P=3 chains")
            for info in safe_members(archive):
                prefix = "P3_CLOSURE_CERTIFICATE/"
                if info.filename.startswith(prefix + "extrapolation/certificates/p03_s"):
                    destination = ROOT / info.filename[len(prefix):]
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source, destination.open("wb") as output:
                        shutil.copyfileobj(source, output)
        for relative, wanted in manifest.items():
            if relative.startswith("extrapolation/certificates/p03_s"):
                actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                if actual != wanted:
                    raise ValueError("installed certificate hash mismatch: " + relative)
    print("P3 certificate asset installed: 192 chains, SHA-256 verified")


if __name__ == "__main__":
    main()
