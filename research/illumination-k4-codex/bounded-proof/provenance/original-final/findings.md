# Independent proof certificates for the bounded 22-wall minimum

[done] All **31 marked-support cases have independently verified UNSAT proofs**. Final receipts: `compose-check.json` and `summary.json`, status VERIFIED, 31/31. No new optical witnesses were generated.

## Exact result and scope

For a slit-free strictly simple room formed from the fixed canonical 45-degree triangle tiling, with two distinct dark interior A marks and **at most four noncorner B/C lattice points**, at least **22 maximal straight walls** are required. The already certified 15-square room attains 22.

This is a computer-assisted result: the geometry-to-Boolean encoding and finite support theorem have written proofs; each Boolean contradiction has a DRAT trace checked by a separate verifier. The new encoder still awaits Claude's independent source review. The result does not claim a global minimum, arbitrary marked locations, arbitrary angles.

The new model uses at-most-four exceptions throughout. It therefore includes the zero-, one-, two- and three-exception cases at W<=21, without assuming the earlier solver-only minimum-24 results. It does not replace those older results at W22 or W23.

## Evidence chain

1. L5/L6 counting and local-fan arguments give I<=3 and N<=36 at W<=21,k<=4. The existing connected-cell argument gives complete finite supports; the independent rebuild matches 14 two-full-cell cases plus eight three-full-cell shapes, with 31 nonadjacent marked pairs. All adjacent marked pairs have a direct segment.
2. A fresh CNF encoder imports no Claude enumeration/model code. It encodes legal local fans, marked full stars, wall/exception/tile budgets, the disk turning identity and necessary connectivity bounds. Each eligible dark room would induce a satisfying assignment. `encoding-proof.md` states the implication and its trust boundary.
3. Only the already independently validated U/Z witnesses are used. A dark room must avoid every sufficient lighting premise. Grid isometries and even-even translations transport the guards to each case's marked pair.
4. Every one of the 31 CNFs is UNSAT. A separately compiled **drat-trim** checks every frozen formula/proof pair. Final composition is **31 direct DRAT proofs**; it does not rely on the incomplete experimental fan-partition trees.
5. Input, source, CNF and proof hashes are recorded. The final proof payload totals 1,205,145,342 bytes, with 2,679,665 CNF clauses across the 31 cases. These count proof artifacts, not distinct rooms or physical rays.

## Validation

| Check | Result |
| --- | --- |
| Necessary support reconstruction | 22 supports, 31 marked pairs, 138 rooted triples: PASS |
| Completed direct contradictions | 31/31 |
| Independent DRAT verification | 31/31 VERIFIED |
| Formula/proof hash readback | 31/31 PASS |
| Known dark 22-wall room at cap 22 | SAT, as required |
| Same fixed room at cap 21 | UNSAT, as required |
| Saved lit room without/with lighting clauses | SAT / UNSAT, as required |
| Cardinality encoder truth checks | 2,304 PASS |
| Signed-literal weighted equality checks | 192 PASS |
| Independent proof-checker controls | valid contradiction accepted; SAT/empty-proof control rejected |
| New optical directions, paths or dark-decider calls | zero |

The guard audit remains separately available at `../persisted-replay/findings.md`: 34,897 precomputed records and 12,679 learned records pass exact universal-completion checks. Guard record counts are not distinct-room counts.

## Why this strengthens the earlier computation

The historical search reported 20 normalized mark placements and zero surviving simple rooms, but did not retain a complete branch-execution trace. The new proof uses a separate geometry encoding and checkable Boolean contradiction traces. Its finer 31 cases distinguish full-A-cell shapes and marked pairs; they are not additional mark placements.

Node and closed-leaf counts depend on branching and when guards are loaded. This method deliberately substitutes checked contradictions for reproducing the historical counts. It reaches the same bounded exclusion through different implementation and execution evidence.

Some initial necessary relaxations hit caps. Their UNKNOWN receipts and partial fan trees are retained as inconclusive history. The final two cases required exact triangle connectivity rather than only occupied-cell connectivity. No capped run or incomplete partition contributes to the final 31-proof conclusion. Earlier successful CNFs that omit later redundant constraints are weaker necessary relaxations; their verified contradictions remain sufficient.

## Files and reproduction

- `support-proof.md`, `support-check.py`, `support-check.json`: finite geometric reduction.
- `encoding-proof.md`, `encode.py`: independent encoding and soundness argument.
- `cases/<case>/formula.cnf`, `proof.drat`, `verify.log`, `verification.json`: the 31 final contradiction certificates and receipts.
- `verify.py`: runs the separate checker and validates optional component cuts; every final case uses zero optional cuts.
- `compose-check.py`: checks final coverage and rehashes the formula/proof pairs. It also supports independently checking the archived fan partitions and unit-reason traces; those are not needed for the final result.
- `controls.json`, `encoder-check.json`: controls and finite encoder truth checks.
- `inputs-manifest.json`, `proof-manifest.json`, `source-lock.json`, `dependencies.lock`: provenance.

Quick final readback:

    .context/illumination-k4-codex/bounded-proof/venv/bin/python -B \
      .context/illumination-k4-codex/bounded-proof/compose-check.py

For fresh independent Boolean verification, run `verify.py <case-tag>` for each tag in `proof-manifest.json`. It invokes the bundled independently compiled `drat-trim` on the exact frozen CNF and proof. `compose-check.py` rehashes already checked artifacts; it does not silently rerun every DRAT verification.

Generating new proofs with the current encoder can produce different CNFs and traces because later models include additional necessary propagation/connectivity constraints. The frozen proof pairs are the exact reproducible evidence for this run. Regeneration is not needed for verification.

## Remaining work

[waiting on Claude] Independently review `encode.py`, `encoding-proof.md` and `support-proof.md`, and rerun the final Boolean checks in a separate copy. L5/L6 and the earlier net-charge derivation were already accepted by Claude; the new CNF source review is a separate obligation.

[waiting on Claude] The unbounded-exception branch remains unresolved. Net charge is exactly redistributed ordinary corner-angle mass. Zero-net cells cannot simply be deleted, and scalar-gcd normalization does not remove independent axis stretches of orthogonal dark rooms. See `../proofs/zero-charge-reduction.md`.

[waiting on Monteil and Tokarsky] Historical comparison. No outward messages, publication, sharing or git mutation occurred in this verification.

**Next move:** peer-review the new encoding, then incorporate the precisely bounded result into the research note. Pursue a genuinely optical invariant for the unbounded-exception problem separately.
