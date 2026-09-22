"""Build a deterministic, self-contained release ZIP from tracked public files."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent
EXCLUDE = {'.git', '__pycache__', 'release', 'logs'}
files = []
for path in ROOT.rglob('*'):
    relative = path.relative_to(ROOT)
    if (path.is_file() and not any(part in EXCLUDE for part in relative.parts)
            and relative.as_posix() != 'hashes/RELEASE_ASSET_SHA256.txt'):
        files.append(path)
target = ROOT / 'release' / 'P4_CLOSURE_CERTIFICATE.zip'
target.parent.mkdir(exist_ok=True)
with ZipFile(target, 'w', ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(files):
        relative = path.relative_to(ROOT).as_posix()
        info = ZipInfo(relative, date_time=(2026, 9, 22, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())
with ZipFile(target) as archive:
    if archive.testzip() is not None:
        raise ValueError('release ZIP failed CRC check')
digest = hashlib.sha256(target.read_bytes()).hexdigest()
(ROOT / 'hashes' / 'RELEASE_ASSET_SHA256.txt').write_text(
    digest + '  P4_CLOSURE_CERTIFICATE.zip\n')
print(json.dumps({'file': str(target), 'bytes': target.stat().st_size,
                  'sha256': digest, 'members': len(files)}))
