# LABS N=67: certified exclusion of the P=3 and P=4 layers

This repository provides independently replayable exact certificates excluding the complete `P=3`, `P'=3`, `P=4`, and `P'=4` layers for binary sequences of length 67. Combined with previously known exclusions of `P=1` and `P=2`, the currently certified conclusion is

```text
P(S), P'(S) not in {1,2,3,4}.
```

The statement covers the full length-67 binary sequence space and does not assume skew symmetry.

> **This repository does NOT prove LABS(67) global optimality.**
>
> The known `E=241` sequence remains an incumbent. No complete certificate excluding `E<=237` is provided. In particular, `P=0` exists, so the result must not be paraphrased as “`P<=4` is impossible.” No failure, timeout, LLL output, floating-point computation, or incomplete PB run is interpreted as a nonexistence proof.

## Status

The independent closure replay returns both `P4_CLOSED` and `P3_CLOSED`. It reconstructs all relevant support and ideal coverage and verifies every accepted exact contradiction chain.

The supplied incumbent is independently recomputed as

```text
E = 241,  P = P' = 26.
```

No sequence with `E <= 237` is supplied, and no certificate excluding every sequence with `E <= 237` is claimed. The remaining global implication is

```text
E <= 237  =>  P + P' <= 51  =>  min(P, P') <= 25.
```

This work removes the values 3 and 4 from those remaining possibilities; it does not remove the other layers. The `P=1,2` exclusions predate the new `P=3` contribution.

## Main result

For `1 <= k <= 33`, let

```text
R_k = C_k + C_(67-k),
Q_k = (-1)^k (C_k - C_(67-k)),
z_k = (R_k + 1)/4,
w_k = (Q_k + 1)/4,
P   = sum_k z_k(2z_k-1),
P'  = sum_k w_k(2w_k-1).
```

The verifiers establish that no length-67 binary word has `P=3` or `P=4`. Applying the same results to the alternating-sign involution gives `P'!=3` and `P'!=4`.

## Scope and limitations

- The result is global with respect to the `P=3` and `P=4` layers: no skew, palindromic, or other structural restriction is imposed.
- It is not a lower bound of 241 for the full aperiodic LABS energy.
- For `P=3`, 166 support orbits reduce to 100 exact local exclusions and 192 conjugacy representatives (384 polarized ideals).
- The 27 finite chains represent 54 ideals by complex conjugation.
- Upstream floating-point and lattice computations were used only to propose certificate data; they are outside the accepted conclusion.

## Repository contents

- `verify_p4_closure.py`: composition checker and main entry point.
- `verify_cm_coverage.py`: reconstructs the 32 support orbits, old local exclusions, factorizations, CRT assignments, and 27 conjugate pairs.
- `verify_cm_result.py`: verifies positive controls and finite Fermat--norm contradiction chains.
- `verify_sequence.py`: recomputes the incumbent correlations and energy.
- `p4_closure_mutation_tests.py`: adversarial tests of the composition layer.
- `replay_all.py`: one-command hash and replay driver.
- `replay_certified_layers.py`: unified standard-library replay of the certified `P=3` and `P=4` layers.
- `verify_extrapolation_manifest.py`: checks the public extrapolation manifest, including all release-installed P=3 chains.
- `P3_SUMMARY.md`: concise statement, coverage, method, and scaling boundary for the new layer.
- `extrapolation/`: parameterized low-layer checker, exact coverage data, reports, and audits.
- `certificates/`: byte-identical core inputs and certificates plus a privacy-clean public index.
- `reports/`: mathematical derivations, audits, and the PB side-experiment report.
- `hashes/FINAL_SHA256.json`: SHA-256 manifest for all core certificate inputs.

## Verification

The core closure verifier requires Python 3.12 and the Python standard library only. It does not call GP, Sage, Gentry--Szydlo code, LLL, a SAT solver, or a PB solver.

The accepted checks consist of exact integer and polynomial arithmetic, module-membership identities, relative-norm recurrences, recursive primality certificates, finite-field exponent recovery, complete CRT assignments, and the exact coordinate bound

```text
67 r_j^2 <= 2 Tr(eta).
```

See [P3_SUMMARY.md](P3_SUMMARY.md), [the extrapolation final report](extrapolation/EXTRAPOLATION_FINAL_REPORT.md), [the method decomposition](extrapolation/METHOD_DECOMPOSITION.md), and [the P=4 template audit](extrapolation/P4_CERTIFICATE_TEMPLATES.md). The original P=4 interfaces remain documented in [SUMMARY.md](SUMMARY.md), [reports/CM_CHAIN_AUDIT.md](reports/CM_CHAIN_AUDIT.md), and [reports/CM_COVERAGE_AUDIT.md](reports/CM_COVERAGE_AUDIT.md).

## Reproduction

From the repository root:

```bash
python -B download_p3_certificate_asset.py
python -B replay_certified_layers.py
```

The download helper retrieves the public `v1.1.0` release asset, checks its SHA-256, and installs only the 192 expected chain files. The unified replay ends with:

```text
LABS N=67 CERTIFIED LAYERS: P=3 AND P=4 VERIFIED
COMBINED EXCLUSION: P,P' NOT IN {1,2,3,4}
GLOBAL OPTIMALITY: NOT CLAIMED
```

The large certificate asset and its digest are listed in [hashes/P3_RELEASE_ASSET_SHA256.txt](hashes/P3_RELEASE_ASSET_SHA256.txt). The release asset is also self-contained for P=3 replay; see its internal `README.md`.

## Trust boundary

The replay does not trust stored batch `PASS` labels. For P=3 it reconstructs the complete case index from independently checked coverage, binds all 192 representatives to exact inputs, and launches the exact verifier in fresh subprocesses. For P=4 it retains the frozen 27-representative composition proof. The verifier itself is readable Python rather than a proof-assistant-generated kernel; Python 3.12 and the audited verifier sources remain in the explicit trust boundary.

## PB side experiment

A certified PB encoding was independently validated on small and control instances using VeriPB and CakePB. The `N=67, E<=237` target run terminated `UNKNOWN`, so it contributes no UNSAT conclusion. The large incomplete proof log and third-party solver/checker binaries are intentionally not distributed here; see [reports/REOPEN_PB_REPORT.md](reports/REOPEN_PB_REPORT.md).

## Citation and contact

Citation metadata are in [CITATION.cff](CITATION.cff). Questions and audit findings can be reported through this repository's GitHub issue tracker.
