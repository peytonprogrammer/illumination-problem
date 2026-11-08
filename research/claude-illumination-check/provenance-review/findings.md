# Review: Codex's clause-provenance packet (item B)

[done] Claude Opus, 2026-11-02. Codex requested this on the board, and Daniel relayed Codex's recommendation to close the proof audit first. The inputs are `illumination-k4-codex/lower-bound-proof-audit/provenance/{checker.py,findings.txt,frozen-inputs.json,summary.json,clause-witnesses.jsonl.gz}`.

**Verdict: ACCEPT, no corrections.** Every clause in each of the 61 frozen I2/I3 formulas has one of two sources:
- the frozen encoder's `geometry(case, 21, 6)` output, exact and in order (9,063,300 clauses);
- one sound instance of a saved path guard (875,332 clauses).

There are no other clauses. 13 cases have no guard clauses.

Method:
- **Hand review** of `checker.py` against the frozen `encode.py` and `illumination_geometry.py`. Section 1 gives the soundness argument for each transformation.
- **Independent witness check.** I wrote `witness_check.py` instead of rerunning Codex's code. It uses a different algorithm and a different source for the variable map (Section 2).

## 1. Hand review

### Guard meaning

A saved guard record has these fields:
- a target vector q, which is even and nonzero;
- a path from (0,0) to q;
- required tiles U and absent tiles Z.

Its physical claim is this: in any room that contains U and avoids Z, the path is a legal light path between its endpoints. The clause ∨_{u∈U} ¬x_u ∨ ∨_{z∈Z} x_z excludes exactly that tile pattern. Every dark room for the marked pair must satisfy it. The checker gives U negative literals and Z positive ones. That's the correct polarity.

### Transformations (D4 plus translation)

- **Instance form.** Each instance applies one of the 8 signed permutation matrices m, then translates by an endpoint o. The checker's `MATS` lists exactly those 8 matrices. Its `transform` matches the encoder's `map_guard`.
- **Endpoints.** The endpoint o is 2·S or 2·T, which is even-even. The instance must map q onto the other endpoint minus o.
- **Tiles map to tiles.** Signed permutations and even translations keep each coordinate's parity class: A is even-even, B is odd-odd, and C is mixed. They also map each A-centered eight-triangle fan onto another such fan.
- **Paths map to paths.** These maps are Euclidean isometries, so they map legal paths to legal paths and corners to corners.

So each instance is a sound guard for the case's mark pair.

### Reversal (o = T)

An instance with o = T places the guard's start at T and its end at S. A light path from T to S, traversed backward, is a light path from S to T. Mutual darkness is symmetric, so the reversed clause is just as necessary.

436,856 of the 875,332 clauses have a reversed witness. This argument carries all of them.

### Universe truncation

The encoder's universe `ts` contains every triangle of every eligible room in the case. This is finite support, proved as C5 in `../encoder-necessity-audit/findings.md`.
- **Required tile outside `ts`.** The premise fails in every eligible room, so the instance implies nothing. Skipping it is sound, and the encoder's own `guards()` skips identically.
- **Absent tile outside `ts`.** Its "absent" condition holds in every eligible room, so its literal is constantly false. Dropping it gives an equivalent clause.

52,964 clauses drop at least one out-of-universe absent tile, 88,238 tiles in total. This argument carries all of them.

### Variable map and matching

- **Variable map.** `encode.py` sets ts = sorted(fan triangles of the allowed cells) and allocates ('t', t) first from a fresh `IDPool`. So triangle t is variable index(t) + 1.
  - `checker.py`'s `variable_map` uses the same radius ⌊(33 − 4I)/2⌋ − b around R_F, the same fan triangles in sorted-tuple form, and the same numbering.
  - My check used the encoder's own `x`, which settles the point.
- **Matching.** A DIMACS clause is a set of literals, so normalizing with sorted(set(·)) loses nothing.
  - The SHA-256 digest only locates a candidate, and the packed literals are then compared exactly.
  - Suffix literals must be triangle variables, so no auxiliary variable can enter.
  - Tautologies are rejected.

### Minor notes (no effect on the verdict)

- `checker.py` takes the base-prefix length from `encoder-binding.json` rather than regenerating it. My check regenerates it, and the lengths agree.
- `checker.py` doesn't require the `p` line to come before the first clause. My check does, and every file passes.
- The acceptance controls exercise the lookup predicate only. Codex already says so.

## 2. Independent witness check (`witness_check.py`)

The script checks each witness rather than searching guards. It imports the frozen encoder (hash-bound) for `geometry`, `x`, and `patch`, and runs no solver, tracer, or path search.

| Check | Result |
|---|---|
| Base prefix equals `geometry(case,21,6)` clauses, exact and in order | 61/61 cases, 9,063,300 clauses |
| Suffix clauses: distinct, triangle-only, and not tautological | 875,332 |
| Witness recomputed from the cited record, matrix, and endpoint, with the encoder's `x` | 875,332/875,332 equal the formula clause |
| Each suffix clause witnessed exactly once | yes. 13 cases have no suffix. |
| Every guard tile is an encoder `patch` tile, U ∩ Z = ∅, m ∈ D4, o ∈ {2S, 2T}, and m·q = end − o | all witnesses |
| Path record starts at (0,0) and ends at q | all witnesses |
| Guard file hashes: current = provenance freeze = full-replay manifest | 52/52, before and after |
| Formula hashes: current = provenance freeze = full-replay manifest | 61/61 |

Witness sources:
- `learned.jsonl`: 314,816;
- `peer-guards.json`: 202;
- `orbit-guard.json`: 35;
- k6 guard files: 560,279.

The run took 74.5 seconds. Output is in `witness_check.json` and `.log`.

## 3. Remaining dependencies

The hash binding in Section 2 ties this review to these other results:
- **Physical soundness of the 193,480 guard records.** Codex's full replay passed all 193,480 records. Its manifest hashes equal the files checked here.
- **Contradiction certificates.** Codex's full replay passed all 61 I2/I3 DRAT proofs.
- **Necessity of the base clauses.** See `../encoder-necessity-audit/` (task A) and `../arithmetic-review/`.
- **Census completeness and normalization (obligation 1).** The proof is in `k6-support-census/findings.md`. It isn't re-proved here.
- **The I4 branch.** It has its own 3/3 replay and isn't part of these 61 formulas.

This review proves nothing about arbitrary polygons, unrestricted exceptions, or arbitrary mark positions.
