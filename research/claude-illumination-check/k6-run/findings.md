# k=6, I=2 and I=3: all 61 pair cases UNSAT

Claude, 2026-11-01. Daniel assigned k=6 to Claude. Codex owns the reduction proof.

**Result.** For W ≤ 21 and k = 6, every one of the 61 raw pair cases (I=2: 18, I=3: 43) is UNSAT. My own drat-trim prints `s VERIFIED` for each case. With the I=4 branch closed by geometry (`../k6-i4/findings.md`), no strictly simple, slit-free canonical-45° room with W ≤ 21 and k = 6 has a dark pair of interior A marks.

This is a bounded result for k = 6. It isn't a global minimum: k is unbounded under dilation, and only the reduction theorem would give a finite k.

## Cases
- `census.py` recomputes the case list independently: I2 18/18/18 and I3 18/43/38, matching Codex's census.
- `cases.json` holds the 61 raw pair cases. Tags look like `I2_00_11-pair0`. Marks are 2 × cell.

## Method
- **Encoder.** Codex's frozen `k5-proof-pilot/inputs/encode.py`, `geometry(case, wmax=21, kmax=6)`, with the allowed region set to a diamond of radius 14 around the full cells. The encoder asserts that the universe it builds lies inside that region.
- **Guards.** Each guard is a lit path with required tiles U and absent tiles Z, giving the clause OR(−U) ∨ OR(Z). `clauses()` maps each guard into a case through the 8 D4 symmetries, with origin s or t (reversal).
- **Loop (`run.py`).** Solve → build the room polygon → trace up to 6 short primitive directions and add a guard for each lit path. If none light, run BFS orbit extraction. Every new guard must pass `guard_audit.check` before it's added.
- **Shared library.** The k5 learned, peer, and orbit guards plus every k6 guard file are loaded into every case.
- **Cube split (guard generation only).** For I2_00_02 and I2_00_12, I fixed 3 free tiles near s (8 cubes), then split I2_00_12's cube 0 into 8 more using 3 more tiles. Cubes only produce guards. Each final certificate comes from one normal run over the full case, with no assumptions.
- **Certificate.** On UNSAT, `run.py` writes `formula.cnf`, re-solves it standalone with proof logging, and runs `../k5-residual/own-drat/drat-trim`. `result.json` records the SHA-256 of both files.

## Results
- 61 of 61 cases: `status UNSAT`, `drat VERIFIED`. Per-case records are in `results.jsonl` and `cases/<tag>/result.json`.
- 0 CANDIDATE_DARK, DISAGREE, UNDECIDED, EXTRACT_FAIL, or NONSIMPLE_MODEL outcomes.
- The three hardest cases:

| Case | Guards in case files | Final run |
| --- | --- | --- |
| I2_00_11 | 30,548 | 879 s, closed with 6 guards per model |
| I2_00_02 | 30,855 | 1,436 s, after 8 cubes |
| I2_00_12 | 63,927 | 2,107 s, after 15 cubes |

## Guard audit
- `audit.py` re-checks every guard in every `cases/*/guards*.jsonl` file with `guard_audit.check`, the exact checker with the normal-selection fix.
- 175,601 guards checked, 0 failures (`audit.{0,1,2,02,12}.out`).
- The k5 library guards were audited earlier: 17,868 learned and 10 peer, all ok (`../k5-residual/guard_full.out`).

## Clause provenance
- `provenance.py` regenerates each case's frozen-encoder base clauses and checks that they're an exact prefix of `formula.cnf`. It then checks that every added clause is one that `clauses()` derives from an audited guard.
- 61 of 61 cases match the prefix. Of the 875,332 added clauses, 0 are unexplained (`prov.*.out`).
- 13 cases have no added clauses: the encoder's geometry alone is UNSAT for them.

## Independent review (Codex)
Codex's sampled review passed (`illumination-k4-codex/k6-final-review/findings.md`). All 61 hashes and base prefixes match, and the case multiset matches. Codex replayed 3 DRAT proofs and checked 6 guards with 48 controls, and all pass. My provenance check closes the clause-provenance gap Codex left open.

Original request:
1. Replay DRAT on a sample of `cases/<tag>/{formula.cnf,proof.drat}` with your own checker, and confirm the hashes.
2. **Premise binding.** Confirm each `formula.cnf` contains the frozen encoder's base clauses for that case, and that `clauses()` translates guards correctly under D4 and reversal.
3. Re-check a sample of guards with your own tracer.
4. Confirm that the 61 cases plus the closed I=4 branch cover all of k=6 under the caps I ≤ 4 and P+m ≤ 12 / 10 / 8.

## Credit
The underlying dark-room research was led by Peyton Wang (16).
