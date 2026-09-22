# Extrapolation public-release audit

```text
REPOSITORY_URL = https://github.com/chengxuandi/labs67-p4-closure
BRANCH = main
COMMIT_SHA = ba7f62d1aae8165b583c716f32b43c2cb18c1123
RELEASE_TAG = v1.1.0
RELEASE_URL = https://github.com/chengxuandi/labs67-p4-closure/releases/tag/v1.1.0
REPOSITORY_VISIBILITY = PUBLIC

P4_REPLAY = P4_CLOSED (exit 0, fresh clone, 21.851 s)
P3_REPLAY = P3_CLOSED (exit 0, fresh clone, 73.371 s)
MUTATION_AUDIT = PASS: 8/8 coverage mutations rejected (exit 0, 5.073 s)
COMPOSITION_AUDIT = PASS: 6/6 composition mutations rejected (exit 0, 1.236 s)
UNIFIED_REPLAY = PASS (exit 0, 109.097 s)

P3_RELEASE_ASSET = https://github.com/chengxuandi/labs67-p4-closure/releases/download/v1.1.0/P3_CLOSURE_CERTIFICATE.zip
P3_RELEASE_ASSET_SHA256 = a25bbdad08d56d2d0f690d4313412f58a6d6f679e49e4ba909abd0af77b0168d
RELEASE_ASSET_REPLAY = PASS

FRESH_CLONE_PATH = D:/tmp/labs67-public-replay-20260922-175917
PYTHON_VERSION = 3.12.10
OS = Microsoft Windows 10.0.26200

P3_SUPPORT_ORBITS = 166
P3_LOCAL_EXCLUSIONS = 100
P3_IDEALS = 384
P3_CONJUGACY_REPRESENTATIVES = 192

P5_STATUS = NOT_ATTEMPTED_BEYOND_SCALING_AUDIT
GLOBAL_OPTIMALITY = NO

FINAL_RESULT = PUBLIC_RELEASE_AND_FRESH_CLONE_REPLAY_PASS
```

## Fresh-clone command record

| Command | Exit | Runtime (s) | Final verdict |
|---|---:|---:|---|
| `python -B verify_p4_closure.py` | 0 | 21.851 | `P4_CLOSED` |
| `python -B extrapolation/verify_new_lemmas.py` | 0 | 1.259 | `PASS` |
| `python -B extrapolation/verify_layer_coverage.py 3` | 0 | 2.759 | `166 / 100 / 384 / 192` |
| `python -B extrapolation/verify_p03_closure.py` | 0 | 73.371 | `P3_CLOSED` |
| `python -B extrapolation/audit_layer_coverage_mutations.py` | 0 | 5.073 | `PASS 8` |
| `python -B extrapolation/audit_p03_composition.py` | 0 | 1.236 | `PASS 6` |
| `python -B replay_certified_layers.py` | 0 | 109.097 | certified P=3 and P=4; global optimality not claimed |

The release asset was downloaded again from GitHub into
`D:/tmp/labs67-release-asset-replay-20260922-1803`, independently hashed,
extracted, and replayed using its internal command. It ended with
`P3_RELEASE_ASSET_REPLAY: PASS` and `GLOBAL OPTIMALITY: NOT CLAIMED`.

The 192 chain files total 402,544,197 uncompressed bytes. Their per-certificate
maximum integer bit lengths range from 9522 to 34021. No chain file was placed
in ordinary git history; the public ZIP is 188,495,098 bytes and is bound by
the digest above.

## Publication exclusions

No proof dependency was withheld. Machine-local discovery stdout/stderr,
run-command metadata containing private absolute paths, Python caches, and the
locally built ZIP were excluded from git. The exact chain data are public in
the release asset, whose package includes the MIT license, a file-level SHA-256
manifest, and a self-contained replay entry point. No secret was found in the
published diff.

The online repository, P3 summary, extrapolation report, release page, and
asset links returned HTTP 200 after publication. The README states that the
known `E=241` word is only an incumbent and that no complete `E<=237`
certificate or LABS(67) global-optimality proof is claimed.
