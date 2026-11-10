# Five-exception exclusion: complete bounded result

[done] All 31 necessary marked support cases have machine-checked UNSAT proofs. Every accepted refutation is bound to its CNF. All 17,868 new optical guards pass exact universal-implication checks and a separate physical polygon replay.

## Result and exact scope

**Computed theorem.** A strictly simple, slit-free room in the canonical 45-degree triangle tiling, with two distinct interior A marks and at most five transparent non-A lattice vertices, cannot be dark with 21 or fewer maximal walls.

Equivalently, a sub-22-wall dark example in this tiling and mark class would need at least six transparent B/C exceptions. Combined with the previously independently verified 22-wall construction, this gives minimum 22 within the class with at most five exceptions. It does not establish an unrestricted minimum.

Fix the canonical tiling by splitting each unit lattice square along its even-even to odd-odd diagonal. A vertices are even-even; the two other parity types are B/C. A transparent non-A vertex means a lattice vertex inside the room or in the relative interior of a straight wall, rather than an actual corner. Count both kinds in k. W counts maximal walls, not atomic triangle edges. Marks must be interior A vertices; arbitrary interior mark positions are outside the theorem.

This is a computer-assisted bounded exclusion. It uses a finite room-support reduction and explicit connecting paths; no negative conclusion assumes a cutoff on ray direction or reflection count.

## Why the finite proof covers the stated class

1. The accepted counting reduction gives I≤floor((15+2k)/6), P+m≤floor((21−4I+2k)/2), and N≤floor(4(19+2k)/3), where I counts full A stars and N counts canonical triangles. At k≤5, I≤4 and N≤38.
2. Four full cells have at least eight external axis neighbors. At I=4 the partial-or-missing budget is at most seven, so I=4 is impossible. The independent peer grew all 391 translation-normalized overlap-connected four-sets and accepted the bound, independently matching our 1,564 rooted listings. I≥5 is already excluded by counting; two distinct interior A marks force I≥2.
3. The remaining I=2,3 budgets are 11 and nine. They coincide with the earlier conservative support reduction: 22 full-star supports and 31 nonadjacent marked pairs, up to translation and grid symmetry. Adjacent marked full stars have a direct connection.
4. For each marked case, the necessary CNF includes legal local fans, precisely the fixed full A stars, wall and exception caps, the regenerated N≤38 cap, finite cell and triangle connectivity, and the disk angle identity. The earlier four-exception area/cell budgets are not reused.
5. A checked connecting path gives a universal implication: if all triangles U are present and all triangles Z are absent, the marks illuminate each other. A dark room therefore satisfies the clause saying at least one U triangle is absent or one Z triangle is present. Such clauses remain valid regardless of how many other exceptions a completion contains.
6. Every one of the 31 necessary CNFs, augmented only by these valid optical implications, is UNSAT. Independent DRAT checking validates each refutation. `proof-input-audit.json` also regenerates all ten continuation formulas from necessary geometry and the exact guard prefixes, and matches every premise clause. The initial 21 proofs retain their prior complete audit and receipt chain.

The finite-support proof is in `../global-route-review/findings.md` §4 and the earlier support audit. The encoder is the frozen audited `../k5-proof-pilot/inputs/encode.py`. Its local fan rules and bounded reachability are necessary conditions, so using this relaxation cannot omit a hypothetical room in the stated class.

## Exact witnesses, rather than bounded-ray non-findings

The first pass closed 21 cases and left ten geometries. The peer independently classified all ten as lit and supplied exact paths. All ten supplied paths were replayed independently here and converted into guards (`peer-check.json`, `peer-guards.json`); their packet hashes match the peer's frozen hashes.

The continuation carries an integer matrix through the labeled-origami traversal. A successful horizontal orbit state supplies one rational physical direction. That one direction is replayed, and its exact path must pass the physical and universal tile checks before a clause is accepted. The orbit engine is a discovery aid: neither its LIT verdict nor its correctness is trusted as a proof premise. Failed, capped or interrupted classifications cannot exclude a room. Only independently verified paths enter the refutations.

The learned library contains 17,868 records, in addition to ten peer-supplied guards and the one earlier orbit-derived guard. It covers 326,437 reflections, including 16,470 smooth lattice-vertex bounces; the longest saved path has 117 reflections. These are certificate statistics, not a reflection bound assumed in the theorem. A separate replay performs 8,944,660 exact segment-versus-atomic-boundary-edge checks. It checks strict containment, actual-corner avoidance and the reflection law. The universal checker independently checks sufficient U/Z conditions for every saved path.

The known 22-wall dark room remains satisfiable at W=22,k=5 with the complete applicable guard library. This is a control against over-excluding the known construction, not an independent darkness proof; that construction's hand proof was verified previously.

## Accepted certificate table

`manifest.json` lists the accepted CNF/proof hashes and their directories.

|Case|Status|Certificate source|
|---|---|---|
|I2_1_1-pair0|verified UNSAT|orbit-derived guards; standalone proof|
|I2_2_0-pair0|verified UNSAT|orbit-derived guards|
|I2_2_1-pair0|verified UNSAT|orbit-derived guards|
|I2_3_0-pair0|verified UNSAT|orbit-derived guards|
|I2_2_2-pair0|verified UNSAT|orbit-derived guards|
|I2_3_1-pair0|verified UNSAT|orbit-derived guards|
|I2_4_0-pair0|verified UNSAT|initial frozen guards|
|I2_3_2-pair0|verified UNSAT|orbit-derived guards|
|I2_4_1-pair0|verified UNSAT|initial frozen guards|
|I2_5_0-pair0|verified UNSAT|initial frozen guards|
|I2_3_3-pair0|verified UNSAT|initial frozen guards|
|I2_4_2-pair0|verified UNSAT|initial frozen guards|
|I2_5_1-pair0|verified UNSAT|initial frozen guards|
|I2_6_0-pair0|verified UNSAT|initial frozen guards|
|I3_0-pair0|verified UNSAT|initial frozen guards|
|I3_0-pair1|verified UNSAT|initial frozen guards|
|I3_0-pair2|verified UNSAT|initial frozen guards|
|I3_1-pair0|verified UNSAT|initial frozen guards|
|I3_1-pair1|verified UNSAT|initial frozen guards|
|I3_2-pair0|verified UNSAT|initial frozen guards|
|I3_2-pair1|verified UNSAT|initial frozen guards|
|I3_2-pair2|verified UNSAT|initial frozen guards|
|I3_3-pair0|verified UNSAT|initial frozen guards|
|I3_3-pair1|verified UNSAT|initial frozen guards|
|I3_4-pair0|verified UNSAT|orbit-derived guards|
|I3_4-pair1|verified UNSAT|orbit-derived guards|
|I3_5-pair0|verified UNSAT|initial frozen guards|
|I3_5-pair1|verified UNSAT|initial frozen guards|
|I3_5-pair2|verified UNSAT|initial frozen guards|
|I3_6-pair0|verified UNSAT|initial frozen guards|
|I3_7-pair0|verified UNSAT|orbit-derived guards|

**Closest-mark certificate.** Use `certified/I2_1_1-pair0/`, not the large original incremental proof under `cases/I2_1_1-pair0/`. The original incremental proof did not produce an accepted receipt in our run. A fresh solve of the identical final CNF produced a standalone 854,947-line refutation that passed checking. Its accepted CNF hash is `db55ec1429db84b5619ac7e97b68cedeee4610eef935e221319d8dbcd76ef25f`; proof hash is `ff0b2fa7dc858e193d39af011fff2214798869f613acb2c039afa9cab90c11c2`.

The raw solver `summary.json` preserves that original incremental outcome as UNSAT_UNVERIFIED. `certified-summary.json` is the authoritative combined total: 21 initial plus ten continuation exclusions, using the standalone replacement for that one case. No failed certificate is counted.

## Independent review status

The live peer independently accepted the four-cell bound/support reuse, replayed all 21 first-pass proofs, replayed the first three continuation I3 proofs, and accepted 360 sampled new guards with its own exact checker. Its 600 deliberately corrupted guard controls were rejected. The peer also independently accepted the 44-reflection guard and re-derived the orbit matrices/frame inversion; its separate breadth-first extraction and tracer passed 970 sampled rooms and 800 D4 images. The continuation uses breadth-first search; the preserved pilot DFS helper can return impractically large directions. The remaining I2 proof replays and final theorem-scope review have been requested through the coordination board; they remain pending unless a later board receipt explicitly records them. All 31 proofs have passed the local independent DRAT checker, and all new guards have passed the full separate polygon and tile audits.

## Reproduction and preserved history

Use `.context/illumination-k4-codex/bounded-proof/venv/bin/python -B` with these scripts:

- `k5-proof-pilot/guards-check.py`: initial 31-case coverage, frozen input bindings, 21 proof receipt bindings and the original path guard.
- `k5-proof-continuation/guards-audit.py`: append-safe full universal/physical guard replay. The saved prefix hash binds the complete 17,868-record library.
- `k5-proof-continuation/proof-input-audit.py`: regenerate every continuation formula's premise set and bind the accepted refutations, including the standalone replacement.
- `k5-proof-continuation/report.py`: verify the complete receipts and rebuild this report and the accepted-certificate manifest.

For an independent refutation replay, run `bounded-proof/drat-trim <formula.cnf> <proof.drat>` with the accepted paths listed in the manifest, and save the log in the reviewer's own directory. An empty proof file can be valid when the CNF itself refutes by unit propagation.

Each audit writes an adjacent receipt. Independent reviewers must use their own output copy. Discovery used successive finite tranches; earlier formulas/results and packet generations are preserved. Do not rerun the original discovery scripts over those artifacts. The original first-pass packets under `../k5-proof-pilot/cases/` remain stable for peer cross-checks.

The redundant area ledger `3N+E_A=4(W−2)+4k+4J`, with J the full interior non-A exception count, passed 247 fixed-room controls and a known-22 control. Its separate static near-diagonal trial remained SAT. It is not used in any of the accepted exclusion proofs.

## Remaining research

The next bounded frontier is k=6. The coarse bound then allows four full A stars with partial-or-missing budget eight. The four-cell lemma forces equality, reducing that new I=4 branch to the minimum-external-boundary configurations; the existing I=2,3 supports must also be enlarged appropriately. That is a proposed next task, not a completed exclusion.

The global classification and isolation/degeneration gaps remain open. This computation does not convert a general real polygon or arbitrary interior marks into the canonical lattice setting.
