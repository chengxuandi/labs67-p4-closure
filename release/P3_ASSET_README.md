# P3 closure certificate asset

This archive is the self-contained exact `P=3` / `P'=3` replay bundle for LABS N=67 release `v1.1.0`.

Requirements: CPython 3.12 and its standard library. No GP, Sage, LLL, SAT, PB, or network access is used by the replay.

From the extracted `P3_CLOSURE_CERTIFICATE` directory, run:

```text
python -B replay_p3_asset.py
```

Success ends with:

```text
P3_RELEASE_ASSET_REPLAY: PASS
GLOBAL OPTIMALITY: NOT CLAIMED
```

`manifest.json` binds every included file by SHA-256. The replay checks this manifest before running the mathematical verifiers. The archive proves only the complete exclusion of `P=3` and `P'=3`; it does not prove LABS(67) global optimality.
