# Independent proof certificates for the bounded 22-wall minimum

[done] All **31 marked-support cases have independently verified UNSAT proofs**. Final receipts: `compose-check.json` and `summary.json`, status VERIFIED, 31/31. No new optical witnesses were generated.

## Exact result and scope

For a slit-free strictly simple room formed from the fixed canonical 45-degree triangle tiling, with two distinct dark interior A marks and **at most four noncorner B/C lattice points**, at least **22 maximal straight walls** are required. The already certified 15-square room attains 22.

This is a computer-assisted result: the geometry-to-Boolean encoding and finite support theorem have written proofs; each Boolean contradiction has a DRAT trace checked by a separate verifier. Claude independently accepted the encoder source and support proof, regenerated every formula, and checked every contradiction. Codex then independently reproduced all 31 formulas byte for byte from frozen reviewed source and freshly checked all 31 adopted traces. The result does not claim a global minimum, arbitrary marked locations, arbitrary angles.

The new model uses at-most-four exceptions throughout. It therefore includes the zero-, one-, two- and three-exception cases at W<=21, without assuming the earlier solver-only minimum-24 results. It does not replace those older results at W22 or W23.

## Evidence chain

1. L5/L6 counting and local-fan arguments give I<=3 and N<=36 at W<=21,k<=4. The existing connected-cell argument gives complete finite supports; the independent rebuild matches 14 two-full-cell cases plus eight three-full-cell shapes, with 31 nonadjacent marked pairs. All adjacent marked pairs have a direct segment.
2. A fresh CNF encoder imports no Claude enumeration/model code. It encodes legal local fans, marked full stars, wall/exception/tile budgets, the disk turning identity and necessary connectivity bounds. Each eligible dark room would induce a satisfying assignment. `encoding-proof.md` states the implication and its trust boundary.
3. Only the already independently validated U/Z witnesses are used. A dark room must avoid every sufficient lighting premise. Grid isometries and even-even translations transport the guards to each case's marked pair.
4. Every one of the 31 CNFs is UNSAT. A separately compiled **drat-trim** checks every frozen formula/proof pair. Final composition is **31 direct DRAT proofs**; it does not rely on the incomplete experimental fan-partition trees.
5. Input, source, CNF and proof hashes are recorded. The final proof payload totals 238,133,791 bytes, with 2,692,369 CNF clauses across the 31 cases. These count proof artifacts, not distinct rooms or physical rays.

## Validation

| Check | Result |
| --- | --- |
| Necessary support reconstruction | 22 supports, 31 marked pairs; 138 rooted triples before the neighbor cap, 120 after: PASS |
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

Some initial necessary relaxations hit caps. Their UNKNOWN receipts and partial fan trees are retained as inconclusive history. The final two cases required exact triangle connectivity rather than only occupied-cell connectivity. No capped run or incomplete partition contributes to the final 31-proof conclusion. The earlier formulas are retained only as historical artifacts under `provenance/original-final/`. Their association with unpreserved encoder versions was not established; they no longer support the final theorem.

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

## Reviewed-source provenance repair

Claude correctly identified that 29 original formulas could not be regenerated from the preserved current encoder. A DRAT proof establishes unsatisfiability of its formula; it does not establish that the formula follows from room geometry. The original statement that regeneration was unnecessary was incorrect as a claim about this evidence chain.

All 31 final pairs now use Claude's uniformly regenerated CaDiCaL 1.9.5 proofs. Codex independently regenerated their CNFs from the exact reviewed encoder, obtaining byte-identical files in every case, then ran its separate drat-trim on all 31 adopted pairs. Every case uses zero optional component cuts. Frozen source, geometry helper, complete witness inputs, support list, dependency pins, generation driver, and hash locks are retained under `provenance/`. Original final artifacts remain archived.

Receipt: `provenance-repair.json`; detailed per-case regeneration receipts: `provenance/adopted.json`; source/input digests: `provenance/source-input-lock.json`. Reproduce any formula comparison with:

    venv/bin/python -B provenance/regenerate.py <case-tag>

This reads only the Codex-owned frozen bundle after adoption and checks the existing proof receipt and hashes. Use `verify.py <case-tag>` for a fresh DRAT replay. Both source-to-formula association and Boolean proof checking are required for the final claim.

## Remaining work

[done] Independent Claude source review, 31 regenerated contradictions, Codex byte-exact regeneration and fresh proof replay. The 138/120 rooted-triple discrepancy is exactly the before/after b<=9 filter; `provenance/root-count.json` records the counts.

[waiting on Claude] The unbounded-exception branch remains unresolved. Net charge is exactly redistributed ordinary corner-angle mass. Zero-net cells cannot simply be deleted, and scalar-gcd normalization does not remove independent axis stretches of orthogonal dark rooms. See `../proofs/zero-charge-reduction.md`.

[waiting on Monteil and Tokarsky] Historical comparison. No outward messages, publication, sharing or git mutation occurred in this verification.

**Next move:** preserve the bounded theorem and its reproducible evidence in the research note. Pursue an optical invariant or proved normalization for the unbounded-exception problem separately.
