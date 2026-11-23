# d72: common-cylinder test (CC) on existing rooms

Date: 2026-11-18. Exact direction and cusp checks on named, hand-built, and saved d64 rooms. No
new rooms. Tags: **PROVED**, **COMPUTED** (script and log here), **CITED**, **GUESSED**.

## Verdict

- **CC survives on every N_x-BBBB pair tested: 747 of 747 (COMPUTED).** The 9 rooms are dumb12
  plus the 8 d69 hand-built rooms, st279b included. Each witness direction has max(|p|,|q|) <= 39.
- **CC is refuted when "BBBB" means only "every parity class has a regular lattice point"
  (COMPUTED, exact over all directions).** 11 lit pairs in 9 saved d64 rooms lie in no common
  open cylinder in any rational direction. Every one of these rooms has a proper factor
  (types like B5BB). D64 closes those rooms, so the open BBBB case is untouched.
- **The two definitions differ (COMPUTED).** Among normalized d64 rooms with `r <= 8`, 2,466
  have a regular point in every class, yet none is N_x-BBBB. The geometric condition only
  excludes Q classes. The prompt's "equivalently" holds only after D64 removes proper factors.
- **Probes (COMPUTED).** cov2929 (QBBB), cov4181 (BBQB), cov4269 (BQBB): all 33 pairs have
  CC. This includes cov2929's turning pairs `(3,1)-(5,3)` in direction (4,3) and
  `(3,3)-(5,5)` in direction (-4,3). R22's dark pair has no CC; its orbit closes at 2,592.

## Method

- X is the translation surface, 4 reflected copies of P, an origami with 4n unit squares.
  Marked points are lifts of every polygon vertex: convex corners, which are regular on X,
  and reflex corners, which are 6 pi cone points.
- For direction v, `M in SL2(Z)` (Euclid word in T and V) sends v to horizontal. Under
  T, `u' = u o r^-1`; under V, `r' = r o u^-1`. Each square keeps its lower-left corner.
- Rows are r-cycles. A row is regular when no square has a marked LL corner. A regular row
  is glued to the row below. A lattice-point lift lies in an open cylinder iff its row is
  regular (PROVED: the row's bottom leaf is the leaf through the point).
- CC(S, T) asks for some lift pair in one cylinder. S is fixed on one sheet; the deck group
  maps v to (+-p, +-q), and both signs are enumerated.
- **Completeness (PROVED).** BFS of the coloured origami (marked, S lifts, T lifts) under T
  and V, up to relabelling, enumerates the SL2(Z) orbit. Every primitive direction is
  `M^-1 (1,0)` for some orbit element. So "no CC on the whole orbit" is exact (`orbit.py`).
  The H-bounded run (`cyl.py`, H = 40) is exact for positives only.
- **Validation (COMPUTED).** Cylinder-interior verdicts match direct closed-orbit tracing with
  the probe's `vertex_step`: 18,446 lifts in dumb12, R22, and DB55, 0 mismatches. dumb12
  rows have lengths 4, 4, 14, 14 at (7,2), (7,9), (4,1), (4,3), as the probe found.

## Smallest refutation (of the geometric form)

`cov446`, n = 15, r = 7, W = 18, normalized, types 00 B, 01 proper(5), 10 B, 11 B. Every
class has a regular point. The pair is `S = (1,2)`, `T = (3,2)`, class 10.

```
y=3 .#......
y=2 ####....
y=1 ########
y=0 .#....#.
```

- The pair is lit: the horizontal segment is visible.
- No lift pair shares an open cylinder in any direction; the coloured orbit closes at 9,072.
- Each mark alone does lie in open cylinders.
- `cov449` is a variant with the same data.

The other refutations are cov2536, cov3401 (2 pairs), cov3688 (2), cov4368 (2), and
cov4432 (2). All are axis-parallel pairs at distance 2 with a visible witness.

## Weakened forms

- **W2, a chain of two cylinders through a regular lattice-point lift Z (COMPUTED, H = 20).**
  It holds for all 11 refuted pairs, and also for the dark R22 pair. So W2 doesn't imply
  light and carries no content.
- **Half-turn relay (PROVED).** Let `delta` be a half-turn with fixed point C and
  `delta S = T`. If C~ and S~ share an open cylinder, then `delta` maps that cylinder to
  itself. So T~ lies in it too, and the relay form is a special case of CC.

## What a proof would need (GUESSED)

- CC must use "no proper factor" essentially, because the geometric form fails.
- The step would link the block structure of the monodromy to cylinder incidence.
  Plausible link: a proper block system yields an intermediate translation cover. That
  cover's cylinders could separate S~ from T~ in every direction.
- No statement from `r <= 8` to cylinder incidence is visible. TR does not apply directly:
  CC asks for some direction, not a fixed combinatorial family.
- Evidence is 9 hand-picked rooms. Estimate: CC for BBBB about 25% true, proof about 3%.

## Files and CPU

`cyl.py` (H-bounded test and validation), `orbit.py` (exact orbit test), `chain.py` (W2),
logs `run_H12.log`, `run_H40.log`, `orbit_controls.log`, `orbit_nocc.log`, `chain_H20.log`,
`smallest.log`, `summary.log`, and `cyl_H*.json`. Total CPU about 35 s, one process at a
time. Run with `python3 -B`.
