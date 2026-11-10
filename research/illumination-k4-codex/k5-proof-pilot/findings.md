# Five-exception proof pass

> **Completed continuation:** all ten originally unresolved cases are now excluded. The combined result is 31/31 accepted proofs for k≤5,W≤21. See `../k5-proof-continuation/findings.md` and `certified-summary.json`. The text below preserves the initial-pass record.

Status: **21 of 31 marked support cases excluded by checked DRAT proofs; 10 unresolved.** No complete five-exception lower bound is claimed.

## Scope and support coverage

The class consists of strictly simple, slit-free rooms in the canonical 45-degree triangle tiling, with two distinct interior even-even A marks, at most 21 maximal walls and at most five transparent non-A vertices. Transparent vertices include full interior non-A vertices and smooth non-A wall vertices. This does not cover arbitrary polygon angles, arbitrary mark positions or unbounded exception counts.

The counting reduction is in `../global-route-review/findings.md` §4. At five exceptions, I≤4 and the partial-or-missing caps for I=2,3,4 are 11,9,7. Four full cells have at least eight external axis neighbors, excluding I=4. Thus the earlier 22 supports and 31 nonadjacent marked pairs suffice. Claude independently accepted the four-cell lemma and support reuse, using translation-normalized connected-set growth rather than our radius-box proof. Adjacent full-cell marks have a direct connection and were removed in the prior support reduction.

The model is regenerated with `wmax=21,kmax=5`, giving the necessary triangle cap N≤38. It does not reuse the smaller four-exception cell budgets. The frozen encoder retains the earlier audited per-vertex truth tables, cell and triangle reachability, and disk Gauss–Bonnet constraints.

## Completed finite pass

`pass.py` loads frozen guards and regenerates each necessary model. Each UNSAT result has its CNF, DRAT proof and independent `drat-trim` receipt. One previously independently replayed pilot proof is reused. All other 30 cases were run in this pass. There were zero timeouts. A fixed known 22-wall dark room remains satisfiable at the relaxed 22-wall bound, including the new guards.

|Case|Outcome|Residual walls|Residual triangles|
|---|---|---:|---:|
|I2_1_1-pair0|unresolved residual|19|32|
|I2_2_0-pair0|unresolved residual|20|30|
|I2_2_1-pair0|unresolved residual|21|33|
|I2_3_0-pair0|unresolved residual|21|30|
|I2_2_2-pair0|unresolved residual|21|34|
|I2_3_1-pair0|unresolved residual|21|32|
|I2_4_0-pair0|excluded; checked proof|—|—|
|I2_3_2-pair0|unresolved residual|21|32|
|I2_4_1-pair0|excluded; checked proof|—|—|
|I2_5_0-pair0|excluded; checked proof|—|—|
|I2_3_3-pair0|excluded; checked proof|—|—|
|I2_4_2-pair0|excluded; checked proof|—|—|
|I2_5_1-pair0|excluded; checked proof|—|—|
|I2_6_0-pair0|excluded; checked proof|—|—|
|I3_0-pair0|excluded; checked proof|—|—|
|I3_0-pair1|excluded; checked proof|—|—|
|I3_0-pair2|excluded; checked proof|—|—|
|I3_1-pair0|excluded; checked proof|—|—|
|I3_1-pair1|excluded; checked proof|—|—|
|I3_2-pair0|excluded; checked proof|—|—|
|I3_2-pair1|excluded; checked proof|—|—|
|I3_2-pair2|excluded; checked proof|—|—|
|I3_3-pair0|excluded; checked proof|—|—|
|I3_3-pair1|excluded; checked proof|—|—|
|I3_4-pair0|unresolved residual|21|31|
|I3_4-pair1|unresolved residual|21|33|
|I3_5-pair0|excluded; checked proof|—|—|
|I3_5-pair1|excluded; checked proof|—|—|
|I3_5-pair2|excluded; checked proof|—|—|
|I3_6-pair0|excluded; checked proof|—|—|
|I3_7-pair0|unresolved residual|21|34|

Each residual has `cases/<tag>/vertices.json` and `residual-room.json`. The first current I2_1_1 residual has 19 walls. It differs from the earlier 21-wall pilot. The earlier packet and receipts are preserved in `inputs/pilot/`; bind classifications to packet SHA-256, not just case name. Current packet hashes are in `guards-check.json`.

Claude has been asked to classify all ten stable packets and independently replay the exclusions. Only the distant I2_6_0 pilot has a live peer DRAT replay so far. The local checker has verified all 21 proofs; peer verification of the remaining exclusions is pending.

## Fixed path guard

Claude supplied a 44-reflection path for the original 21-wall pilot. `witness-check.py` independently checks all 945 segment/wall incidences, strict segment containment, corner avoidance and the exact reflection law. It explicitly permits the two smooth lattice-vertex bounces. The exact tiling audit derives a universal implication requiring 20 used triangles and 12 absent triangles. This guard was added in all compatible D4/source-target orientations.

`guards-check.py` checks the implication under 24 prescribed D4/even-translation isometries and their reversed paths. It also binds all frozen guard-source hashes to the previously completed universal-path audit, verifies encoder/geometry hashes, checks complete 31-case coverage, and binds each CNF/proof to its saved checker receipt. This checks the current receipt chain; it does not repeat the old exhaustive path audit.

## Orbit proof to a connecting path

`orbit-witness.py` carries an exact 2×2 matrix along the labeled-origami traversal. For the permutation conventions in the supplied decider:

- `(R,U R^-1)` contributes the map to old coordinates `[[1,-1],[0,1]]`.
- `(R U^-1,U)` contributes `[[1,0],[-1,1]]`.
- Right-multiply these into B. A successful horizontal state gives original developed direction `B e1`; apply the inverse initial source frame to get the physical direction.

The sole builder instrumentation exposes that initial derivative frame. `inputs/origami_frame.py` is checked to differ from the frozen original only by recording and returning it. A LIT orbit verdict is accepted as a usable witness only after the prescribed direction physically reaches the target and exact tiling requirements agree with the room.

For the old 21-wall pilot, the successful L^6 state gives direction (−1,6), yielding a valid 14-reflection connection. This replaces a direction scan with a direction supplied by the symbolic orbit proof. Three fixed rectangle controls and four prescribed mixed-shear matrix controls pass, including composition order. This is a useful proof-producing implementation step, not a general new illumination theorem. Long orbit traversals can still exceed their cap; that returns UNDECIDED, never DARK.

The additional 14-reflection universal guard requires 18 used and nine absent triangles. It is saved in `orbit-guard.json` and has not been used in the 31-case exclusion pass. Its compatible transforms cover none of the ten current residual packets, so it does not improve their status by itself.

## Reproduction

Run with the existing interpreter `.context/illumination-k4-codex/bounded-proof/venv/bin/python -B`:

- `k5-proof-pilot/cases/I2_1_1-pair0/witness-check.py`: one frozen 44-reflection path and its guard.
- `k5-proof-pilot/guards-check.py`: guard transformations, source hashes, support coverage and proof receipt bindings.
- `k5-proof-pilot/orbit-check.py`: fixed orbit-to-direction controls.
- `k5-proof-pilot/guard-coverage.py`: fixed 14-reflection guard and current residual coverage.

Use full paths beneath `.context/illumination-k4-codex/`. Each checker writes its own adjacent receipt; independent reviewers must use their own output copy. To independently replay one UNSAT receipt, use `bounded-proof/drat-trim cases/<tag>/formula.cnf cases/<tag>/proof.drat`, with correct full paths and an own output log.

`pass.py` regenerates formulas and residuals, so do not rerun it over the stable classification packets. Reproduce in a separate copy or preserve the current packets first.

## Next move

Obtain exact classifications and fixed witnesses for the ten remaining packets. Independently replay each supplied witness, derive its universal guard and only then resume the affected SAT branches with preserved generations. Neither a geometric SAT residual nor a capped orbit run establishes darkness. The unrestricted 22-wall minimum and the global isolation/degeneration reduction remain open.
