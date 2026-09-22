# Certified exclusion of P=3 at N=67

## Result

For every binary sequence `S` of length 67,

```text
P(S) != 3
P'(S) != 3.
```

This is a complete layer exclusion with no skew-symmetry or other structural restriction.

## Coverage

The independent checker reconstructs 166 support orbits. Exactly 100 are removed by local arithmetic obstructions. The remaining spectra produce 384 polarized ideal cases, paired into 192 conjugacy representatives. Every representative has a finite exact certificate, and every certificate is replayed rather than accepted from a stored status label.

## Method

The proof reuses the P=4 route: the `alpha_z` norm/binary-word equivalence, polarized CM ideal interface, conjugacy pairing, finite-field exponent recovery, exact module-inclusion recurrence, and trace-residue bound. The new contribution is a signature-parameterized checker rather than a checker tied to the fixed P=4 inputs.

The exact coset minimum-trace bound `M_67(r,p)` is also a new rigorous lemma. It is stronger than the earlier scalar-coordinate relaxation, but it contributed zero exclusive exclusions in this P=3 batch; every accepted P=3 chain was already closed by the older scalar inequality.

## Scaling

The chain depths remain 8 or 10 steps. The main growth is the case count:

```text
P=4:  27 conjugacy representatives
P=3: 192 conjugacy representatives
```

Thus the observed bottleneck is the number of independent cases, not the depth of an individual chain.

## Why extrapolation stopped

The P=5 scaling audit estimates at least 431 simple conjugacy representatives and finds two repeated-prime inputs. No sufficiently strong shared or batched certificate mechanism is currently available, so no P=5 full batch was started.

## What this does not prove

LABS(67) global optimality remains open. The repository does not prove `E_min(67)=241` and does not provide a complete certificate excluding `E<=237`.
