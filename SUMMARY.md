# Certified exclusion of the P=4 layer for LABS at N=67

## Result

For every binary sequence `S` of length 67,

```text
P(S) != 4  and  P'(S) != 4.
```

This covers the complete length-67 binary space and does not assume skew symmetry.

## What this does not prove

This does not prove that the minimum LABS energy at `N=67` is 241. The supplied incumbent has `E=241`, but global unsatisfiability of `E<=237` remains unproved.

## Method

The unresolved `P=4` cases are represented as polarized ideal generator problems over the conductor-67 cyclotomic order. Finite Fermat--norm contradiction chains replace any inference from failed lattice enumeration. Accepted certificates contain only exact, finitely checkable data: integer module-membership identities, relative-norm recurrences, finite-field exponent recovery, complete CRT assignments, recursive primality certificates, and a terminal violation of the coordinate bound

```text
67 r_j^2 <= 2 Tr(eta).
```

## Coverage

There were 54 unresolved polarized ideals. Complex conjugation reduces them to 27 representatives, each of which has an accepted exact contradiction chain. The coverage checker reconstructs all 32 `P=4` support orbits and verifies that all 54 ideals are covered. The final composition checker prints `P4_CLOSED`.

## Verification

The closure replay uses Python 3.12 and the standard library only. It does not invoke GP, Sage, Gentry--Szydlo code, LLL, SAT, or PB solvers. Floating-point and lattice computations used while discovering candidate chains are not part of the accepted conclusion.

## Replay

```bash
python replay_all.py
```

Expected final lines:

```text
LABS N=67 P=4 CLOSURE: VERIFIED
GLOBAL OPTIMALITY: NOT CLAIMED
```

