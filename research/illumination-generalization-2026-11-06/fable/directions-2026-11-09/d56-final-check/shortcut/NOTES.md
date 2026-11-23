# d56 shortcut: Rig-quotient fold enumeration for residue D20

Opus 5.5 subagent, 2026-11-17. Tags: PROVED, CITED, COMPUTED, GUESSED.

## Verdict

The d52 machinery adapts to Rig quotients, and the residue D20 check runs in about 2 CPU-s.
It finds 1 room up to lattice isometry and 0 certified pairs.

## Method

1. `enum_rig.py`, stage 1: brute force over all 26^4 tuples of involutions (V0, V1, H0, H1)
   on 5 cells. It keeps transitive W-sets K whose double is a sphere with z = 2 zeros
   and only `cvx` or `cone` orbits in some class y. Classes stay labelled, with no symmetry
   reduction, and shapes are deduplicated by `fold.canon`.
2. Stage 2 runs every degree-4 cover P -> K through d52's model-free enumerator
   (`validate_generic.generic_covers`, copied verbatim). The arc model is not used.
3. Stage 3 keeps covers with r = 8 that pass `fold.is_room` and have corners in >= 3
   classes. It then deduplicates them up to lattice isometry.
4. `check_rig.py` runs d48 item 2 steps 2-6 on each room with the d10 tools
   (`roomtools.room_tuple`, `closure_partition`, `unified_test.Factor`):
   - It recomputes W and area from the cells.
   - R_y merges every g_y-cycle. Each y outside {a, t} is tested on all 4 lift pairs.
   - The live rule is Factor's: a regular point, or a pole that receives a 2-cycle of g_a
     or g_t. This is d48's rule.
   - `reach` is Factor.live_component with the target on the t side.

## What carried over (PROVED unless tagged)

- **C1 (sphere, cycle lengths 1 to 3).** This carries over. A block's g-cycle length
  divides the length of any of its sheets' cycles, and DP's lengths are 1, 2, or 3. Genus
  can't increase under a quotient.
- **C9 orbit types.** The five types are complete at d = 5. Paths of 4 or more cells give
  cycle lengths of 4 or more. A cycle of 6 cells needs 6 cells.
- **C3 (zeros on the seam).** Not needed at d = 5.
- **C2 is replaced by a new condition.** "No regular point over x" becomes "class-y orbits
  are only `cvx` or `cone`" (identity monodromy at y).
- **C4 and C5.** These are not imposed. They come out of the search: every 2-cone shape has
  0 covers, and delta * z = 8 = r.
- **C11 and C12.** Applied after the search on P itself, not on K.
- **(delta, d, z) = (4, 5, 2) and n = 20.** CITED from d48 `review.md` lines 135-149.
- **Branching over poles only (Fact L).** This holds for any quotient of DP. In any case,
  the enumerator is model-free and doesn't use it.
- **R_y is iota-invariant (PROVED).** V_i g_y V_i = g_y^-1, so V_i preserves the
  g_y-cycle relation E. It also normalizes G = <g_x>. So V_i R_y is a G-congruence that
  contains E, which gives V_i R_y = R_y. G and V_i generate the W-image, because
  V_{1-i} = (V_{1-i} H_j)(H_j V_i) V_i. So R_y is a W-congruence, and N_y is the double of
  K = P / R_y. COMPUTED check: the closure under W equals the closure under G for all 4
  classes of the room found.
- **Completeness (PROVED, given the d48 citation).** Any lift pair certified by y forces
  R_y to have shape (4, 5, 2). So P is a fibre-4 W-cover of some K from stage 1, and the
  generic search lists every such cover.

## Results (COMPUTED, `logs/enum_rig.log`, `logs/check_rig.log`)

| Item | Count |
| --- | --- |
| Quotient shapes K (labelled classes, up to relabelling) | 12; each has exactly one Rig class y |
| Shapes up to symmetry | 2 cone types: 4 shapes with 1 cone, 8 shapes with 2 cones |
| Covers with genus 0, room local types, r <= 8 | 8 W-sets, all from the 4 shapes with 1 cone |
| Strictly simple rooms, W = 20, area 20, >= 3 classes | 8 W-sets, 1 room up to lattice isometry |
| Different-class interior pairs tested | 14 (16 lift-pair tests use the (4,5,2) R_y) |
| Certified pairs | **0**; no lift pair is separated by any y |
| Separations with shape other than (4,5,2) | 0 |

The room, rows top to bottom, with x running 0 to 3:
`##.. / ###. / .### / ..## / ..## / .### / ###. / ##..`.

Validation (COMPUTED):

- `roomtools.ledger` gives area 20, r = 8, and W = 20. The room is strictly simple.
- The R_y computed on the room through roomtools has (delta, d, z) = (4, 5, 2) at the class
  of (0, 0). The other three classes give (20, 1, 0), which is N_y = B.

Not done: no positive control for `reach`. It's a 10-line variant of d10's
`live_component`.

## Compute

- `enum_rig.py`: 1.8 CPU-s, peak RSS 18 MB.
- `check_rig.py`: under 0.1 CPU-s per run, run twice.
- Total, including the failed first launch: under 3 CPU-s. Each run used one process.
- RLIMIT_AS can't be set on macOS, so peak RSS is reported instead.

## Files

| File | Role |
| --- | --- |
| `enum_rig.py` | Stages 1-3; writes `rooms.json` |
| `check_rig.py` | W/area recheck, R_y shapes, W-invariance, live Rig test |
| `fold.py` | Copied from d52 |
| `roomtools.py`, `unified_test.py` | Copied from d10, with sys.path pointed here |
| `d4_monodromy.py`, `hurwitz.py` | Copied from d6 |
| `logs/` | Run logs |
