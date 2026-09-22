# Certified PB toolchain audit — 2026-09-19

`B_CAN_PRODUCE_CERTIFICATE = YES`

This is a toolchain compatibility result, **not** a LABS(67) result. No N=67 solving was performed by this audit. Five small OPB cases complete the chain RoundingSat → VeriPB → CakePB, including UNSAT, SAT, optimization, non-unit pigeonhole reasoning, and an input equality. Incorrect inputs/proofs are rejected. All files are local to this project; no system-wide environment or package installation was made.

## Selected, pinned tools

| Component | Source revision / version | Local executable |
|---|---|---|
| RoundingSat | `d4edbf7908a9bb951fd181940919e0f3ac7ab1ee`, banner `RoundingSat 2`, proof format 2.0 | `tools/roundingsat.exe` |
| VeriPB | `a08a1a7205816d02775b5de568b32fe278e5d55b`, package 3.0.2 | `tools/VeriPB/target/release/veripb.exe` |
| CakePB | `438b8f835f369014578223e0dd6c674e86733682`, three-line Windows exit-ABI wrapper patch below | `tools/cakepb/cake_pb.exe` |
| Rust | rustc 1.98.1, `48a229cea`, GNU Windows minimal toolchain | `tools/cargo/bin/cargo.exe` (local homes) |
| C compiler | existing MSYS2 UCRT64 GCC 13.2.0 | `<MSYS2-UCRT64>/bin/gcc.exe` |

RoundingSat was downloaded from the official Windows build artifact URL linked by its README:
`https://gitlab.com/MIAOresearch/software/roundingsat/-/jobs/artifacts/master/raw/build/roundingsat.exe?job=build-windows`.
The artifact itself prints commit `d4edbf7`, matching the pinned full source revision. Its SHA256 is pinned below; the moving artifact URL alone is not the pin. No solver source changes were made. The GitLab jobs metadata endpoint required authentication, so an individual CI job ID is not asserted.

VeriPB was built from the pinned unmodified Rust source using its committed Cargo.lock, `cargo build --release --locked --bin veripb`. Its v2 parser accepts the solver's format and elaborates to a v3 kernel proof. Build duration on this machine was about 3 minutes 26 seconds. This audit does not claim the source snapshot is identical to the historical 3.0.2 release tag: it is a later pinned source commit reporting package version 3.0.2.

CakePB README records upstream theorem/build references:
HOL4 `fac52534ceb43806d35b11f91dafd558266bcbb6`;
CakeML `14856fcfddeb3fdafdf8a1080e567a55d3102698`.
The supplied generated assembly was built locally rather than rebuilding HOL4/CakeML proofs.

## Exact commands

Run from the original PB research workspace (not distributed in this public P=4 replay repository):

```powershell
& ./tools/roundingsat.exe INSTANCE.opb --lp=0 --print-sol=1 --time-limit=10 --proof-log=PROOF.pbp
& ./tools/VeriPB/target/release/veripb.exe INSTANCE.opb PROOF.pbp --elaborate PROOF.kernel
& ./tools/cakepb/cake_pb.exe INSTANCE.opb PROOF.kernel
python ./toolchain_smoke/run_smoke.py
```

`--proof-log` writes the exact named file, without adding a suffix. `--lp=0` avoids numerical LP during these tests. The proof checker uses exact integer PB derivations regardless of solver heuristics. Timeout or UNKNOWN never counts as a successful conclusion.

The current solver's proof-aware OPB header parser requires:

```text
* #variable= N #constraint= M #equal= EQ intsize= BITS
```

Here M counts source constraint lines and EQ counts equality lines; internally each equality becomes two inequalities. This was tested by `equality.opb`. Older README examples omit the last fields and are rejected by this exact solver snapshot. Its `src/parsing.cpp` is authoritative for this integration detail. Only ordinary linear OPB constraints were tested; no nonlinear input or untested parser extensions are assumed supported.

The rebuild script `tools/build_checkers.ps1` uses task-local RUSTUP_HOME/CARGO_HOME and process-only PATH changes. The Rust installer was the official `rustup-init.exe`, invoked after inspecting its help with `-y --no-modify-path --profile minimal --default-host x86_64-pc-windows-gnu --default-toolchain stable`; the installed exact version is recorded above. No downloaded shell installation script was executed.

## Windows CakePB glue correction and trust boundary

The supplied assembly already has Windows calling-convention shims. However `cake_exit` directly called `cdecl(cml_exit)` with the exit argument in SysV `%rdi`, while Windows C expects `%rcx`. The unmodified executable produced correct-looking mathematical verdicts but a garbage process exit code. The final local patch is exactly:

```diff
 cake_exit:
+#if defined(__WIN32)
+     movq    %rdi, %rcx
+#endif
      callq   cdecl(cml_exit)
```

No generated CakeML machine-code byte, mathematical checker operation, parser rule, or inference rule was changed. A first experiment calling the existing `windows_cml_exit` shim created an extra-call stack/ABI failure and was discarded; it is not the delivered build. The final direct register move passes all positive and negative tests. The final patch is inspectable with `git -C tools/cakepb diff`.

Build command:

```powershell
& <MSYS2-UCRT64>/bin/gcc.exe basis_ffi.c cake_pb.S -o cake_pb.exe -DCML_HEAP_SIZE=1024 -DCML_STACK_SIZE=256
```

The compiler, OS/FFI/runtime, local three-line ABI fix, and correspondence of published generated assembly to the cited CakeML build remain part of the engineering trust boundary. This is not a fresh local replay of the HOL4 formal-development proofs. VeriPB is a separate, unmodified checker and checks the original high-level proof independently before elaboration.

**Important automation rule:** CakePB can exit with code 0 even when rejecting a mathematical proof. Acceptance requires an explicit matching `s VERIFIED SATISFIABLE`, `s VERIFIED UNSATISFIABLE`, or `s VERIFIED BOUNDS ...` line, no checking-failure diagnostic, and a normally completed process. Exit code alone is insufficient. VeriPB rejects tested invalid/truncated proofs with nonzero status.

## Test evidence

`toolchain_smoke/run_smoke.py` independently enumerates the tiny source OPB formulas and then runs all three tools. `smoke_results.json` stores every command, exit code, stdout and stderr; separate text logs are retained. `sha256.json` pins inputs, proofs, elaborated kernels, logs and binaries.

| Case | Independent tiny formula result | Verified result |
|---|---|---|
| sat | 2 models | SAT, both checkers |
| unsat | 0 models | UNSAT, both checkers |
| opt | 5 models, minimum 3 | exact bounds 3..3, both checkers |
| php (3 pigeons / 2 holes) | 0 models | UNSAT, both checkers |
| equality | 0 models | UNSAT, both checkers |

Mutation cases reuse a purported UNSAT proof after changing the formula to a satisfiable one, falsify a SAT witness, change the claimed optimum, or truncate the proof. These must be rejected. Separate CakePB mutations modify its elaborated optimum and truncate its kernel, ensuring that acceptance is not inferred from the elaborator alone.

### Identified emitter defect: explicit zero-coefficient contradiction

The primary encoding audit found a real boundary defect in this exact solver revision. It is preserved independently as `toolchain_smoke/zero_coeff_contradiction.opb`:

```text
* #variable= 1 #constraint= 1 #equal= 0 intsize= 64
+0 x1 >= 1 ;
```

This formula is unsatisfiable, but the solver's emitted proof derives a tautological row and then cites it as a contradiction. **VeriPB correctly rejects the proof.** Solver UNSAT text alone would have silently misrepresented certification. The smoke script requires this rejection and retains both the bad proof and checker diagnostic. The compatibility claim therefore concerns successfully checked canonical inputs, not every possible OPB log from this solver.

The primary LABS encoder handles constant contradiction as the exactly equivalent pair `+1 x1 >= 1 ;` and `-1 x1 >= 0 ;`, and omits constant true rows. These transformations are an encoder responsibility with independent equivalence checking; no checker or proof file is weakened or retroactively edited to hide the defective log.

## Other current tools and literature

The [official VeriPB repository](https://gitlab.com/MIAOresearch/software/VeriPB) now uses Rust, with a legacy v2 parser. Its Python/C++ `version2` branch was also inspected at `b0d55dc87b5aaf55b14747be564a8e9060c081f3`: direct Windows UCRT64 compilation fails a required `sizeof(long)==8` assertion. This arithmetic/platform assumption was **not** patched away. The unsuccessful source tree and an unused launcher remain only as audit artifacts; use the Rust executable above.

The [official RoundingSat repository](https://gitlab.com/MIAOresearch/software/roundingsat) supplies the tested Windows binary and supports proof logging. The [official CakePB repository](https://gitlab.com/MIAOresearch/software/cakepb) supplies the checked backend assembly. The [PB26 competition specification](https://www.cril.univ-artois.fr/PB26/) explicitly retains compatibility with v2 proofs while using the newer checkers; our compatibility claim nevertheless rests on the local tests, not just this statement.

[Koops et al., CP 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2025.21) presents the RoundingSat/Sat4j → VeriPB → CakePB chain, including optimization and proof-producing LP integration. The paper supplies historical source hashes. We use current pinned official revisions and test compatibility explicitly; no benchmark result in that paper implies a LABS lower bound.

HitPBO-PL appears in the [official PB26 certified run records](https://www.cril.univ-artois.fr/PB26/results/trace.php?idev=123&idjob=4795674) as version 2026-06-22 with `--proof-compatible --prooffile`. This establishes a certified variant exists, not local support: it was not installed or independently validated here. Sat4j was likewise not additionally installed once the selected full toolchain passed. No claim is made that every solver version with these names has compatible logging.

## Binary SHA256

```text
roundingsat.exe  12a98e4ca9e91cd0fe344e88760fe0eaced3c1e4cf377b5134379ef4fec9fedf
veripb.exe       85e417ccce3b7b47be8b1d1854cf6f9c78c62338de5a890841c01942bc0df59e
cake_pb.exe      612a1c876c708ca4624051014a96ffd6dc6a5bf5443b9b1f16e6b9b07d6a035e
```

These hashes identify this build, not a promise that a future rebuild has byte-identical compiler timestamps. All source revisions, the Cargo lockfile, compiler versions and the only source patch are separately recorded.
