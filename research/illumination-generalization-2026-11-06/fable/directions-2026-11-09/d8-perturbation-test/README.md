# D8: perturbation test of the same-fibre conjecture

Opus 5.5 subagent, 2026-11-09. Exact integer, Fraction, and permutation
arithmetic only. Not independently reviewed. Owner approval for this room
search was relayed by the coordinator.

## Result

- **Validation passes for orthogonal rooms.** The decider reproduces the
  22-wall room's dark set exactly. It agrees with the reference decider on
  every pair and every orbit state. It lights all 31 orthogonal lit controls
  with doubly certified paths. It can't complete the 34-wall room: the orbit
  exceeds 40,000,000 states. That room's darkness rests on the proved
  separation lemma (k = 0), not on the orbit.
- **The decider is orthogonal-only.** Tokarsky 26, Castro 24, and the census
  rooms were not perturbed.
- **1,027 rooms, enumerated exhaustively, no sampling.** That's 2 bases, 60
  single modifications, and 965 double modifications. They hold 1,464 pairs
  of interior lattice points of one class: 1,313 of class A, 151 of
  classes B, C1, and C2.
- **No counterexample and no contradiction.**

  | N_min | LIT (certified) | DARK (complete orbit) | DARK (separation lemma) | UNDECIDED |
  | --- | --- | --- | --- | --- |
  | separates | 0 | 1 | 2 | 0 |
  | does not separate | 1,461 | 0 | 0 | 0 |

- **Every perturbed room with k >= 1 lights the marked pair.** The only dark
  perturbed room is `R34-L2-0346` (add (6,-3), remove (7,-3)). It keeps
  k = 0, so N_min = DP and it is dark by the lemma.
- **Smallest W among dark perturbed rooms: 34.** No dark room has
  W <= 21.
- **A single added transparent point lights the pair every time.** All 10
  single modifications of the 34-wall room with k = 1 are lit.

## Definitions used

- Room: a strictly simple orthogonal lattice polygon, stored as its set of
  unit cells (named by lower-left corner). Strictly simple means
  edge-connected, no pinch point, and a boundary that is one closed curve.
- Class of a lattice point: coordinate parity relative to an origin. A pair
  of the same class is tested with that class as A.
- k: number of transparent (interior or flat-wall) lattice points not in
  class A.
- N_min: the quotient of the double DP by the smallest monodromy-invariant
  partition that contains each 2-cycle of the C1, B, and C2 corner
  permutations (`d2-factor-audit/audit.md`, section 3.1). It "separates" p
  and q when no DP lift of p has the same image as a DP lift of q.

## Decision procedure (`orbit.c`, `decider.py`)

The model is the 4-fold unfolding X of the room: one unit square per
(cell, sheet), right and up neighbour permutations `h`, `v`. Each square
carries its lower-left lattice point: blocked (a polygon vertex), a numbered
source, or free. A billiard path between lattice points is a segment in X of
primitive rational direction that meets no blocked point.

- `orbit` explores the full SL(2,Z) orbit of the decorated X by breadth-first
  search with the shears `U: v' = v o h^-1`, `L: h' = h o v^-1`, and their
  inverses. A square keeps its lower-left point under these moves, so
  decorations are fixed. States are stored up to decoration-preserving
  relabelling.
- In each state the horizontal ray from every source lift runs until it
  returns or meets a blocked point. Every primitive direction is horizontal
  in some state, so an exhausted orbit (`DONE`) is a complete decision: an
  unreached pair is DARK.
- The program tracks the matrix `M` with state = M · X. A ray of `s` steps is
  the developing vector `s · M^-1 (1,0)` in X. That vector is the lit
  witness.
- Runs on the perturbed rooms stop early (`EARLY`) once every non-separated
  pair is lit. Separated pairs are then DARK by the proved lemma (audit 1.3),
  and the verdict is labelled `separation`, not `orbit`.

**Lit certificate (`certify.py`).** A witness counts only when two
independent exact tracers both accept the same signed vector:

1. `tracer.py`: a room-level billiard tracer with reflections and Fractions.
   It does not use the unfolding.
2. `ref/surface.py`, copied unmodified from `d3-review/`: its own unfolding
   and `Surface.segment` for non-axis vectors. For axis-parallel vectors, a
   walk along its own `r`/`u` edge permutations.

**Second dark decider.** `ref/room_model.py`, copied unmodified from
`d2-factor-audit/`, is an independent implementation of the same orbit
method. It was used on the 22-wall room. No counterexample arose, so no
other dark verdict needed a second decider.

## Validation (`validate.py`, `validate.json`, `validate.log`)

| Check | Input | Outcome |
| --- | --- | --- |
| V1 | 22-wall room, all 8 regular lattice points | `DONE`, 5,184 states. Dark pairs: exactly (0,0)–(2,2), (0,0)–(2,-2), (4,0)–(2,2), (4,0)–(2,-2), as in the record. Lit relation equals `room_model.illumination`. All 48 ordered lit witnesses certified by both tracers. |
| V2 | Same orbit, per state | In all 5,184 states the horizontal scan equals the room tracer's rays in the 4 sign variants of `M^-1 (1,0)`. 0 mismatches. |
| V3 | 34-wall room, marks (2,0), (6,0) | `CAP` at 40,000,000 states, 722 s, no lit witness found. k = 0, N_min = DP (degree 19) separates the marks. |
| V4 | 30 k7 models + W18 control (W 18–20, k = 7) | 31 of 31 lit, at most 228 states. All witnesses certified. N_min has degree 1 and doesn't separate. |
| V5 | First 5 controls of V4, per state | 0 mismatches. |

V2 and V5 check the shear formulas and the matrix bookkeeping directly
against an unfolding-free tracer. Two of the 8 regular points in V1 lie on
flat walls; V2 starts rays at interior points only.

## Perturbations (`room.py`, `perturb.py enumerate`, `rooms.json`)

Base rooms: `R22`, the 22-wall room with marks (0,0), (2,2); `R34`, the
34-wall orthogonal room with marks (2,0), (6,0).

Single modifications, all generated, then filtered:

- add one cell outside the room that shares an edge with it;
- remove one cell;
- push one wall (maximal boundary segment) out or in by one unit along its
  whole length.

A result is kept when it is strictly simple and both marks stay interior.
Rooms are deduplicated by cell set.

| Base | Single (distinct, valid) | Double (new rooms only) |
| --- | --- | --- |
| R22 | 29 | 445 |
| R34 | 31 | 520 |

"Double" means every valid single modification applied to every
single-modified room, minus rooms already at level 0 or 1. All were
decided. Nothing was sampled.

## Results (`results.jsonl`, `summary.json`)

Each line of `results.jsonl` holds one room: cells, vertices, W, r, area,
interior points, k and transparent points for the marks' class, |G| and its
method, primitivity, per class the N_min degree and k, the orbit status and
state count, and per pair: separated, verdict, method, witness.

### Computed facts

- W ranges over 14 to 38. k for the marks' class ranges over 0 to 11.
- Orbit status: `EARLY` 1,024 rooms, `DONE` 1 (R22 base), `CAP` 2 (R34 base
  and `R34-L2-0346`; both have only separated pairs and were run with a
  300,000-state cap to look for a contradicting witness).
- Before all non-separated pairs were lit, a room needed at most 5,234 orbit
  states (median 108). The largest witness coordinate is 104 (median 10).
- N_min degree for the marks' class: 1 in 1,024 rooms, 5 in R22 base, 19
  (= DP) in the two k = 0 rooms.
- Monodromy: 1,023 rooms primitive, 4 imprimitive. The imprimitive ones are
  R22 base (|G| = 233,280) and `R22-L2-0034`, `R22-L2-0207`, `R22-L2-0232`
  (|G| 33,592,320 or 16,796,160). In those three, N_min has degree 1 and the
  pair is lit.
- Every primitive room with k >= 1 has N_min of degree 1, as the audit
  predicts.

Marked-pair verdict against the change in k from the base (dk):

| Rooms | dk | LIT | DARK |
| --- | --- | --- | --- |
| R22 single | -1 to +3 | 29 | 0 |
| R22 double | -1 to +7 | 445 | 0 |
| R34 single | +1 to +5 | 31 | 0 |
| R34 double | 0 | 0 | 1 |
| R34 double | +1 to +9 | 519 | 0 |

Single modifications of R22 that keep k = 4 (4 rooms: add (-2,-1),
(-2,0), (1,3), (2,3)) move one transparent point. Each is primitive with
|G| = 20,922,789,888,000 = 16!, and each is lit.

### Interpretation

- The 22-wall room's darkness is fragile. No single or double modification
  keeps a proper parity factor, and every modification lights the pair.
- Rooms that stay dark keep k = 0, so the surviving factor is DP itself. No
  perturbed room keeps a proper parity factor.
- On this family the same-fibre conjecture holds on all 1,461 non-separated
  pairs, and each is lit by a short path. The test is weak on the dark side:
  the only dark rooms are separated cases the lemma already covers. The
  family produced no dark room with k >= 1 other than R22 itself.

## Limits and open doubts

- **No complete dark decision for primitive rooms.** The orbit of the
  34-wall room has more than 40,000,000 states. Had a non-separated pair
  resisted the early search, it would have been reported UNDECIDED, not
  DARK. None did.
- **Diagonal-wall rooms are not covered.** Tokarsky 26, Castro 24, and the
  census rooms have 45-degree walls. This directory has no validated decider
  or tracer for them. Those rooms are k = 0 with symmetric or alternating
  monodromy, so their complete orbits are likely as large as the 34-wall
  room's.
- **Perturbations are local and near the boundary.** The audit's annex and
  one-defect mechanisms (a transparent point that S cannot reach on a
  primitive segment) need larger, targeted changes. This test did not build
  them.
- **Shared assumptions.** Both orbit deciders and `surface.py` use the same
  4-fold unfolding construction (it's the standard one). `tracer.py` doesn't.
  V2 compares the decider with `tracer.py` state by state.
- **N_min code is reused.** `nmin.py` calls the copied
  `room_model.pillow_model` and `closure_partition`. It asserts that the
  corner permutations' cycle types match the point statuses in every room.
  Its N_min degrees match the record on both bases (5 and 19).

## Reproduce

Run from this directory. `cc` compiles `orbit.c` on first use.

```
python3 -B validate.py 40000000    # V1-V5; about 15 min; needs about 11 GB for V3
python3 -B perturb.py enumerate    # rooms.json, under 1 s
python3 -B perturb.py run 3000000 10   # results.jsonl, a few minutes on 10 workers
python3 -B analyze.py              # summary.json and printed tables
```

`perturb.py run` appends to `results.jsonl` and skips rooms already there.
Delete the file for a fresh run.

## Files

- `room.py`: cell-set geometry, strict simplicity, walls, single modifications.
- `orbit.c`, `orbit`: the SL(2,Z) orbit decider (C).
- `decider.py`: builds the unfolding and calls `orbit`.
- `tracer.py`: room-level billiard tracer.
- `certify.py`: two-tracer lit certificate.
- `nmin.py`: monodromy, |G|, primitivity, N_min, separation.
- `validate.py`, `validate.json`, `validate.log`: task 1.
- `perturb.py`, `rooms.json`, `results.jsonl`, `run.log`: tasks 2 and 3.
- `analyze.py`, `summary.json`: tasks 4 and 5.
- `ref/`: unmodified copies. `room_model.py` and `enum_targets.py` from
  `d2-factor-audit/`, `surface.py` from `d3-review/`, `d4_monodromy.py`
  (= `monodromy.py`) and the room inputs from `d4-monodromy-blocks/`.
