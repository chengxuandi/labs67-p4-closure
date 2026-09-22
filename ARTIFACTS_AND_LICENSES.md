# Artifact and license scope

The MIT license covers the original verifier code, documentation, and project-generated certificate data in this repository.

No third-party solver binary or third-party source tree is distributed. In particular, the discovery-stage PARI/GP executable, Gentry--Szydlo implementation, RoundingSat, VeriPB, and CakePB are omitted. They are not required for the standard-library closure replay.

The two CSV files under `certificates/legacy/` are project-generated arithmetic classification artifacts required by the coverage verifier. The JSON files under `certificates/cm_inputs/` and `certificates/cm_outputs/` are the exact project-generated inputs and certificates used by the final replay.

The public `certificates/cm_batch_results.json` is a privacy-clean index derived from the private execution record. It contains no machine paths or solver logs and is not itself a mathematical certificate; the composition verifier ignores status claims and rechecks every referenced file.

