# LABS N=67: certified P=4 layer closure

This repository provides independently replayable exact certificates proving that, for every binary sequence `S` of length 67,

```text
P(S) != 4  and  P'(S) != 4.
```

The statement covers the full length-67 binary sequence space and does not assume skew symmetry.

> **This repository does NOT prove LABS(67) global optimality.**
>
> It excludes the complete `P=4` and `P'=4` layers only. No failure, timeout, LLL output, floating-point computation, or incomplete PB run is interpreted as a nonexistence proof.

## Status

The independent closure replay returns `P4_CLOSED`. It reconstructs all relevant support and ideal coverage and verifies every accepted exact contradiction chain.

The supplied incumbent is independently recomputed as

```text
E = 241,  P = P' = 26.
```

No sequence with `E <= 237` is supplied, and no certificate excluding every sequence with `E <= 237` is claimed. The remaining global implication is

```text
E <= 237  =>  P + P' <= 51  =>  min(P, P') <= 25.
```

This work removes the value 4 from those remaining possibilities; it does not remove the other layers.

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

The verifier establishes that no length-67 binary word has `P=4`. Applying the same result to the alternating-sign transform gives `P'!=4`.

## Scope and limitations

- The result is global with respect to the `P=4` layer: no skew, palindromic, or other structural restriction is imposed.
- It is not a lower bound of 241 for the full aperiodic LABS energy.
- The 27 finite chains represent 54 ideals by complex conjugation.
- Upstream floating-point and lattice computations were used only to propose certificate data; they are outside the accepted conclusion.

## Repository contents

- `verify_p4_closure.py`: composition checker and main entry point.
- `verify_cm_coverage.py`: reconstructs the 32 support orbits, old local exclusions, factorizations, CRT assignments, and 27 conjugate pairs.
- `verify_cm_result.py`: verifies positive controls and finite Fermat--norm contradiction chains.
- `verify_sequence.py`: recomputes the incumbent correlations and energy.
- `p4_closure_mutation_tests.py`: adversarial tests of the composition layer.
- `replay_all.py`: one-command hash and replay driver.
- `certificates/`: byte-identical core inputs and certificates plus a privacy-clean public index.
- `reports/`: mathematical derivations, audits, and the PB side-experiment report.
- `hashes/FINAL_SHA256.json`: SHA-256 manifest for all core certificate inputs.

## Verification

The core closure verifier requires Python 3.12 and the Python standard library only. It does not call GP, Sage, Gentry--Szydlo code, LLL, a SAT solver, or a PB solver.

The accepted checks consist of exact integer and polynomial arithmetic, module-membership identities, relative-norm recurrences, recursive primality certificates, finite-field exponent recovery, complete CRT assignments, and the exact coordinate bound

```text
67 r_j^2 <= 2 Tr(eta).
```

See [SUMMARY.md](SUMMARY.md) for a short research summary and [reports/CM_CHAIN_AUDIT.md](reports/CM_CHAIN_AUDIT.md) plus [reports/CM_COVERAGE_AUDIT.md](reports/CM_COVERAGE_AUDIT.md) for the proof interfaces.

## Reproduction

From the repository root:

```bash
python verify_sequence.py
python verify_p4_closure.py
python p4_closure_mutation_tests.py
python replay_all.py
```

The main command ends with:

```text
P4_CLOSED: 32/32 support orbits excluded; NOT a global LABS energy proof.
```

The all-in-one command ends with:

```text
LABS N=67 P=4 CLOSURE: VERIFIED
GLOBAL OPTIMALITY: NOT CLAIMED
```

## Trust boundary

The replay does not trust stored batch `PASS` labels. It binds all 27 representatives to their exact inputs, verifies each chain, reconstructs the full coverage, and requires two positive controls. The verifier itself is readable Python rather than a proof-assistant-generated kernel; Python 3.12 and the audited verifier sources remain in the explicit trust boundary.

## PB side experiment

A certified PB encoding was independently validated on small and control instances using VeriPB and CakePB. The `N=67, E<=237` target run terminated `UNKNOWN`, so it contributes no UNSAT conclusion. The large incomplete proof log and third-party solver/checker binaries are intentionally not distributed here; see [reports/REOPEN_PB_REPORT.md](reports/REOPEN_PB_REPORT.md).

## Citation and contact

Citation metadata are in [CITATION.cff](CITATION.cff). Questions and audit findings can be reported through this repository's GitHub issue tracker.

