# D83: stress test of the open reachability lemma on single edits of R22

Opus 5.5 subagent, 2026-11-20. Exact integer and Fraction arithmetic. Not independently reviewed.

## Result

- **The lemma held in all 11 tested rooms.** Every tested room has at least one off-class regular coincidence that is the midpoint of a legal path from S to T. In the 4 rooms where the saved witness has a source-class midpoint, every off-class candidate is reached, 26 of 26.
- **R22 control behaves as recorded.** n = 15, r = 9, d = 12, 6 regular coincidences, all in the source class, no off-class candidate, no witness.
- **Every saved midpoint is a listed coincidence.** For every saved witness, the midpoint carries a regular coincidence of the marked union. This holds at sheet level: the 2-cycle at the midpoint that contains the arrival cell lies in the union.
- **The test is weak in three ways.** Every tested room is lit, so none is a dark pair. In every tested room d = n − 1, so the marked union is all off-diagonal pairs. The counting bound 2⌈2n/3⌉ − 16 − ⌊n/2⌋ is negative for n ≤ 17, so it doesn't apply here. The off-class candidates exist anyway: 5 to 9 per room.
- **Two rooms are direct.** In `R22-L1-008` and `R22-L1-010` the saved witness is (2, 2), a direct segment from S to T. The lemma's "nondirect" hypothesis excludes them. They are kept in the table for completeness.

## Rooms tested

Source: `d8-perturbation-test/results.jsonl`, base `R22`, level 1 (all 29 saved single modifications). Kept: strictly simple, both marks interior, and r ≤ 8 (W ≤ 20). 11 rooms qualify. Seven are one-cell adds or removes. Four (`008`, `010`, `026`, `028`) push a two-cell wall in or out. All 29 single edits are strictly simple with interior marks; the other 18 have r ≥ 9.

## Table

Classes are relative to S = (0, 0): a (source), b = (1,1), c1 = (1,0), c2 = (0,1).

| Room | Moves | n | r | d | Off-class regular coincidences | Saved witness | Witness midpoint (class) | Step 4 |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `R22-base` | none | 15 | 9 | 12 | 0 | none (dark) | none | not applicable |
| `R22-L1-003` | add(-1,-2) | 16 | 8 | 15 | 7 | (-6,-8) | (1,0) smooth (c1) | not needed |
| `R22-L1-004` | add(-1,1) | 16 | 8 | 15 | 7 | (-4,2) | (0,1) interior (c2) | not needed |
| `R22-L1-005` | add(0,-3) | 16 | 8 | 15 | 7 | (-24,-16) | (0,-2) smooth (a) | 7 of 7 reached |
| `R22-L1-006` | add(0,2) | 16 | 8 | 15 | 7 | (-4,8) | (0,0) = S (a) | 7 of 7 reached |
| `R22-L1-008` | push-out (1,-1)(1,1) | 17 | 8 | 16 | 9 | (2,2), direct | (1,1) interior (b) | not needed |
| `R22-L1-010` | push-out (1,1)(3,1) | 17 | 8 | 16 | 9 | (2,2), direct | (1,1) interior (b) | not needed |
| `R22-L1-021` | remove(4,0) | 14 | 8 | 13 | 5 | (-8,14) | (2,3) smooth (c2) | not needed |
| `R22-L1-022` | add(3,2) | 16 | 8 | 15 | 7 | (20,8) | (0,0) = S (a) | 7 of 7 reached |
| `R22-L1-024` | add(4,1) | 16 | 8 | 15 | 7 | (12,18) | (4,1) interior (c2) | not needed |
| `R22-L1-026` | push-in (3,0)(5,0) | 13 | 7 | 12 | 5 | (8,6) | (2,1) smooth (c2) | not needed |
| `R22-L1-027` | remove(1,-3) | 14 | 8 | 13 | 5 | (-28,-16) | (0,0) = S (a) | 5 of 5 reached |
| `R22-L1-028` | push-in (2,-3)(2,-1) | 13 | 7 | 12 | 5 | (10,-6) | (1,-1) smooth (b) | not needed |

Saved witnesses are shown as the signed vector that both tracers accept. The per-class coincidence lists are in `stress.log`.

## Method

1. **Coincidences.** `stress.py` loads `d82-review-necessity/indep.py` unmodified (its `monodromy`, `orbit_partition`, `marked_union`). It computes n, r, d, and every regular coincidence of the marked union with its point, kind, and class. It asserts 2d = R + J, and that r, W and n match `results.jsonl`.
2. **Witness midpoints.** Each saved witness is certified with `d8-perturbation-test/tracer.py`. The half vector u = D/2 is traced from S to get the midpoint M. `ref/surface.py` from d3 independently confirms both S + u = M and S + 2u = T.
3. **Sanity check.** M must carry a coincidence in the union. At an interior M the check uses the 2-cycle that contains the arrival cell. At a flat-wall M it uses the single 2-cycle.
4. **Targeted check** (`step4.py`, only the 4 rooms with source-class midpoints). For each off-class coincidence (M, {a, b}), a path with midpoint M is S + u = M, continued straight by the same u to T. Lifts of M satisfy u ≡ M − S (mod 2). The check tries those u with max(|u_x|, |u_y|) ≤ 32 in order of length. It accepts u only when all of these hold:
   - `tracer.py` reaches M with no corner hit, arriving in a cell of {a, b}.
   - `tracer.py` reaches T from S + 2u with no corner hit.
   - `surface.py` agrees on both endpoints.

   The check can confirm candidates. It can't refute them, but it didn't need to: every candidate was reached.

## Observations

- **Three saved witnesses pass through S at their midpoint** (`006`, `022`, `027`). The second half of such a path is itself a path from S to T of half the length. Its midpoint has a different class. A source-class midpoint at S is therefore an artifact of a non-shortest saved witness.
- **Sharpest case.** `R22-L1-005`, the c2 candidate at (2, 3): the shortest confirming half vector is u = (-10, 31), which is close to the bound of 32. Every other candidate needed max |u| ≤ 17.
- **Interior candidates count twice.** For interior off-class points (`005` at (1,−2), `006` at (1,2), `022` at (3,2)), both 2-cycles were reached separately, each by a path arriving through the matching diagonal.

## Limits

- No dark pair with r ≤ 8 exists in this family. The lemma's real content, that darkness with r ≤ 8 is impossible, is not exercised.
- d = n − 1 in every tested room, so the union-membership sanity check is automatic there.
- The search is bounded: only u with max(|u_x|, |u_y|) ≤ 32, and only for the 4 rooms that needed it.
- Total CPU time: under 1 second.

## Reproduce

Run from this directory:

```
python3 -B stress.py > stress.log
python3 -B step4.py > step4.log
```

## Files

- `stress.py`, `stress.log`: steps 1 to 3 and the table.
- `step4.py`, `step4.log`: the targeted per-candidate check.
