# d67: referee report on d64 (the finite case)

Date: 2026-11-18. Adversarial review of `../d64-finite-case/`, limited to its load-bearing
claim as d66 uses it. No new discovery search: every run re-checks d64's approved room list or
enumerates polyominoes inside d64's scope. No d64 file was edited.
Tags: **PROVED** (argument here), **COMPUTED** (script and log here), **CITED** (file).

## Verdict: sound, with fixable gaps

The claim d66 uses holds:

> Every normalized strictly simple orthogonal lattice room with `W <= 20` in which some class
> `x` has `1 < deg N_x < n` is in d64's list (2,800 rooms). In all of them, every same-class
> interior lattice pair is lit (6,680 pairs), whatever the pair's class.

- The completeness argument is correct step by step (section 1). Two steps cite more than
  they need, and none is wrong.
- "Lit" no longer depends on the orbit model or the FC lemma. My own exact integer billiards
  find a witness path for **all 6,680 pairs**, with `max(p, q) <= 8` (section 2).
- My own code reproduces the counts: 4,581 normalized rooms, 2,800 in scope, and 6,680 pairs.
  A brute force over all fixed polyominoes with `n <= 16` matches d64's in-scope list at every
  area, which extends d64's own `n <= 14` check (section 3).
- No finding is fatal. The gaps are about evidence and wording (section 4).

## 1. Completeness argument (README section 2)

| Step | Claim | Verdict |
| --- | --- | --- |
| 0 | Translate so `x = (0, 0)` | CORRECT. A unit translation swaps `V0 <-> V1` or `H0 <-> H1`. Covers are deduped up to isometry. |
| 1 | `K = P / B_x` is a transitive W-set with fibres of size `delta >= 2` | CORRECT. `B_x` is W-invariant (R3.3). Own check: the W-closure and the rotation-only closure give the same block count on all 4 classes of all 4,581 rooms. |
| 2 | Orbit types of K; class x has only cvx, rfx, cone; at most one cone; genus 0 | CORRECT (PROVED here). The W-image of an int 4-cycle is int, cone, smooth, or cvx. A 3-path maps to a 3-path or a point. A block holding a 2-cycle of `g_x` is fixed, so `g_x` on blocks has only 1- and 3-cycles. Two cones would give ramification `2 delta > 2 delta - 2`. This doesn't need `delta >= 3`. |
| 3 | `z >= 1` | CORRECT, but the R1 citation isn't load-bearing. Class x has no smooth point, so the `z = 0` shapes are the unit square and five shapes with at most 2 singular classes. `shapes.py` rejects only the unit square (`d = 1`, `N_x = B`) for `z0` alone (`logs/shapes.log`). Step 4 rejects the other five. `delta z <= r` holds for any `delta`: a block 3-cycle lifts to `delta` reflex 3-paths. |
| 4 | At least 3 singular classes | CORRECT. Two odd edges give `{(p, q), (p+1, q)}` and `{(s, t), (s, t+1)}`. These can't be the same 2-set. Convex corners map to cvx. Reflex corners map to rfx or cvx in the same class. |
| 5 | `d <= 4z + 2 <= 18` | CORRECT. `d = cvx_x + 3 rfx_x + 2 cone_x = 4z + 4 - (cvx' + 2 cone' + 3 rfx')`, and at least 2 non-x classes are singular. |
| 6 | `enum_K.c` finds every such K | CORRECT by reading. The search and pruning match d52 `enum_K.py`, which d54 item 1 refereed. Buffers are safe: DM = 24 > 18, and partial chains stay under 10 cells against arrays of 64. Port parity: 127 = 127 and 677 = 677 shapes, with equal node counts. |
| 7 | The arc model finds every cover | CORRECT. d54 item 2's proof doesn't use `delta >= 3`. `ngen` counts the cone involution, so a `delta = 2` cover glued only by `c` isn't dropped. The model-free enumerator agrees on all 4,290 `delta = 2` cases (9,548 = 9,548). d54 checked the 185 `delta >= 3` cases. These are the same 106 shapes. |
| 8 | Room and normalization filters | CORRECT. `is_room` requires an injective development, walls exactly at absent neighbours, and no pinch. My own normalization agrees with d64's flag on all 4,776 rooms. My own simplicity and `r <= 8` checks pass on all 4,581 normalized rooms. |

**Boundary cases.**

- `delta = 2` is included. It's 3,663 + 521 + 93 + 13 = 4,290 cases.
- Non-normalized rooms are outside d64's statement. d66 step 1 reduces them, and lattice marks
  can become rational marks (G2). That's d66's job, not d64's.
- `W < 20` versus `W = 20`: every `r <= 8` is enumerated, and areas run from 6 to 40.
- `r <= 8` bounds the area through `delta z <= r` and `d <= 4z + 2`. No separate area cap is used.

**d66's extension, "whatever the pair's class": CORRECT.** `dark_pairs.py` marks a room in
scope when any of the four classes is proper. It takes the union over 4 origins of
`x in {1, 2, 3}`. It tests pairs in all four classes. The enumeration has no mark or pair
filter: d52's K4 filter isn't used. My independent count over all four classes gives the same
6,680.

## 2. Correctness of "lit" (COMPUTED, `indep.py`, `ctrl.py`)

**d64's decision procedure (by reading).** `dark_pairs.lift_pair_lit` walks the full
pure-braid orbit for each of the four lift pairs. It accepts the first state that joins the
lifts at any target `x in {b, c, d}`. A pair is dark only when all four orbits are complete
with no witness. There's no state cap. Its "lit" verdict equals billiard light only through
d61's FC lemma.

**Independent ground truth.** `indep.py` is my own exact integer billiard. It shares no code
with d62 `billiard.shoot` or with any d64, d52, d10, or d63 module.

- Coordinates are scaled to `(x q, y p)`, so both components move one unit per tick. Every
  wall crossing and lattice-vertex event is exact.
- At a lattice vertex, the path goes straight when 4 cells are present and reflects when 2
  are present (smooth wall). It's absorbed at 1 or 3 cells (convex or reflex corner).
- It searches every primitive `(p, q)` with `max(p, q) <= H`, all signs. A run stops at
  absorption or when the `(vertex, direction)` state repeats.
- A witness is a proof that the pair is lit. Pairs with no witness are only unresolved.

| Check | Result |
| --- | --- |
| All same-class interior pairs, 2,800 in-scope rooms, `H = 12` | **6,680 of 6,680 lit**. Ordered witnesses by `max(p, q)`: 1: 8,592; 2: 3,002; 3: 1,202; 4: 312; 5: 218; 6: 24; 7: 6; 8: 4. |
| Control, `H = 1` | 2,384 pairs unresolved, so the search depends on `H`. |
| Negative control, P6 (cells retyped from d52 `named.py`), `H = 20` | Its known dark pair `(1,0)-(3,-2)` has no witness. |
| The 37 point-level per-target-dark pairs (`logs/pointlevel.log`) | **37 of 37 lit** by a billiard witness. |
| Same 37 pairs, every direction at `H = 20`, grouped by direction parity class | 0 paths of the claimed dark class `x` reach `T`. This agrees with d64's per-target darkness. |

The 200-pair sample the brief asked for became the full set of 6,680. This removes the FC
lemma and the orbit model (d66 gap C3) from step 3a of d66's chain.

## 3. Independent counts (COMPUTED)

**From d64's room list, with own code** (`indep.py`): 4,776 rooms, 4,581 normalized, and
**2,800 in scope**. That gives **6,680 same-class interior pairs**. In-scope rooms by area:

| n | 6 | 8 | 9 | 10 | 12 | 14 | 15 | 16 | 18 | 20 | 21 | 22 | 24 | 25 | 26 | 27 | 28 | 30 | 32 | 34 | 35 | 36 | 40 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rooms | 3 | 6 | 4 | 20 | 80 | 116 | 51 | 236 | 436 | 402 | 87 | 292 | 408 | 33 | 149 | 5 | 218 | 119 | 33 | 3 | 72 | 10 | 17 |

**Brute force with no quotient list** (`polyo.c`, `polyo_n16.log`, `compare.py`,
`compare.log`). The C code does a Redelmeier enumeration of all fixed polyominoes with
`n <= 16`. Totals match OEIS A001168, for example 104,592,937 at `n = 16`. Per polyomino it
uses its own code for these checks:

- no hole (Euler characteristic);
- no pinch;
- `r <= 8`;
- normalized (maximal edge runs);
- `B_x` by congruence closure.

Fixed in-scope polyominoes per area match d64's in-scope rooms, counted as fixed images, at
every `n <= 16` with 0 mismatches. Examples: 369 at `n = 12`, 462 at 14, 376 at 15, and 996
at 16. Up to isometry that's 516 rooms, including d64's 229 at `n <= 14`.

**Quotient list consistency** (`kcheck.py`). Each in-scope room has some proper classes. That
gives 2,843 proper quotients `K_y`. I put each in enum_K.c's canonical form with my own code.
All 2,843 are in `K_z4_d18.txt` and in `K_adm.json`. All satisfy `d <= 4z + 2` and
`delta z <= 8`. This also confirms that the canonical forms agree. It's mostly
self-consistency, because 2,800 rooms give 2,843 quotients.

## 4. Findings

| # | Severity | Location | Finding |
| --- | --- | --- | --- |
| 1 | Fixable gap (evidence) | `enum_K.c` at `z = 4`; README section 2 step 6 | The `z = 4` part (3,663 of 4,475 cases, `d` up to 17) has no independent cross-check. The port matches d52 exactly at `z <= 3`. Brute force reaches only `d <= 8` at `delta = 2`. `kcheck` is self-consistency. The code reading (section 1, step 6) found no defect. To close it, run an independent quotient enumerator, or d52's Python `enum_K.py 4 18`, on the `z = 4` slice. |
| 2 | Fixable gap (independence), closed here | `validate.py` part A | d64's brute force shares `covers.iso_key` and `covers.edge_gcds` (normalization) with the pipeline. It also shares d52 `fold.B` and `from_cells`. One normalization bug would bias both sides the same way. d67's `polyo.c` and `indep.py` use none of these, and they agree (sections 2 and 3). |
| 3 | Fixable (wording) | README "Answer", bullet 3 | "no room with `W <= 20` and some `N_x != B` ... has a dark pair" overstates the claim. The test covers normalized rooms, same-class interior lattice pairs, and `1 < deg N_x < n`. Section 4 of the README states this correctly, and d66 reads it correctly. |
| 4 | Cosmetic | README section 2 step 3 | The R1 citation for `z = 0` isn't needed. The nontrivial `z = 0` shapes fail step 4. The only shape rejected for `z0` alone is the `d = 1` unit square. |
| 5 | Cosmetic | README section 2 step 7 | "proved in d54 item 2 for every delta" is right in substance. d54 wrote its proof for `delta >= 3`, but the argument never uses that bound. The `ngen == 0` remark also holds at `delta = 2`, because `ngen` counts the cone. |
| 6 | Cosmetic (dependency now removable) | README section 4; d66 gap C3 for step 3a | d64's lit verdicts rest on the orbit model and the FC lemma. Billiard witnesses now cover all 6,680 pairs, so step 3a no longer needs C3. |

**Not re-verified (not load-bearing for d66).** The RL-fin row statistics: 81,924 rows, 830
dark, and 0 certified. Only the 37 point-level pairs were checked, and they're consistent
(section 2).

## Files and CPU

| File | Role | CPU-s |
| --- | --- | --- |
| `indep.py`, `indep_H12.log` | Own geometry, `B_x`, scope, pair count, billiards for all 6,680 pairs and the 37 point-level pairs | 2.9 (two runs, `H = 1` and `12`) |
| `ctrl.py`, `ctrl_H20.log` | P6 negative control, per-target consistency of the 37 | 0.7 |
| `polyo.c`, `polyo_n16.log` | Brute-force fixed polyominoes, `n <= 16` | 130 (plus 0.8 for an `n <= 12` trial) |
| `compare.py`, `compare.log` | Brute force against d64's list, per area | 0.4 |
| `kcheck.py`, `kcheck.log` | Quotient-list membership and bounds | 0.5 |

Total: about 135 CPU-s (2.3 CPU-minutes), one process at a time. The `polyo` binary was built
in `/tmp` and deleted after the run. To rebuild it, run `cc -O2 -o polyo polyo.c` and then
`./polyo 16`. Run the Python scripts with `python3 -B` from this directory. No git changes.
