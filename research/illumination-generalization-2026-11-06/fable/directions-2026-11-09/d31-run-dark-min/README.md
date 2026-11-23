# d31: smallest glued dark room with a run

Opus 5.5 subagent, 2026-11-11. Daniel approved this construction search
today. Nobody has reviewed it. Tags follow d30: **PROVED** (one-session
hand proof), **CHECKED** (exact computation, scope stated).

## Result

- Within the class below, the minimum is **W = 28**. The only room at
  W = 28, up to the 8 symmetries, is `P6` of d30. **W = 24 and W = 26 are
  not achieved**, and neither is any W <= 26.
- In found.json coordinates, the room is the 20 cells
  `(-3,2) (-3,3) (-2,1) (-2,2) (-2,3) (-2,4) (-1,0) (-1,1) (-1,4) (-1,5)
  (0,0) (0,1) (1,1) (1,2) (2,2) (3,2) (4,1) (4,2) (5,0) (5,1)`. It has
  `r = 12`, a run on the line `x = 3`, and the dark pair `(-2,3), (0,1)`.
  Both points lie 3 or more columns from the run line.
- The next values are W = 34 (3 rooms, one only in the weak position) and
  W = 36 (7 rooms). The W = 34 weak room matches d30's five-copy remark.
- Consistency check: the d=3 gluings of `Q` contain the known 22-wall room,
  which has no run.

## Class searched

- **Base R.** A strictly simple polyomino and a parity class A, such that
  every non-A lattice point of R is a corner and R has two or more A points.
  This is the parity property, so the fold `DP -> DR` is a parity factor.
- **Glued room P.** A union of d copies `g(R)`, where g runs over the
  reflections in integer lines (`x -> +-x + even`, `y -> +-y + even`). The
  copies are connected by shared edges and have disjoint cells. The fold
  `P -> R` is single-valued on lattice points. `glue.py` generates every such
  set by reflecting one copy across the line of any boundary edge. That
  covers every gluing tree and every gluing with cycles.
- **Kept.** P is strictly simple and has a run: two adjacent identical
  non-empty cell rows or columns. S and T are interior A points with
  `fold(S) != fold(T)`, and neither lies on the run line. Such a pair is dark
  by the fold-back lemma. "Strong" means both points lie 2 or more rows from
  the run line; "weak" allows the boundary rows.

## Coverage (CHECKED)

- Bases: every strictly simple polyomino with area <= 10, every class: 29
  bases. With area <= 8 there are 4 shapes: `Q`, the F-like pentomino
  `(0,0) (0,1) (1,1) (1,2) (2,1)` (W 10), the plus pentomino (W 12, all four
  classes), and one 8-cell shape (W 16).
- Gluings: d = 2..9 for all 29 bases (`glue_a10_d9.log`, 97 s). Every base
  gives the same counts of copy sets: 4, 6, 24, 63, 232, 760, 2777, 9910.
  Only `Q` ever produces a separated pair.
- Distinct dark rooms with a run, by W: 28: 1, 34: 3, 36: 7, 40: 9,
  42: 25, 44: 12. The full table is in the log; `found.json` keeps W <= 40.

## Why nothing below 28 (PROVED, CHECKED)

1. **Wall formula.** `W(P) = d (W(R) - 4) + 4 + 2 n3`. Here `n3` counts the
   reflex corners of P over convex corners of R. Proof: `DP -> DR` is a
   degree-d local isometry, so a preimage of an angle-`a` point has angle
   `e a <= 2 pi`. Over a reflex corner, `e = 1`, giving `d r(R)` reflex
   corners. Over a convex corner, reflex means `e = 3`. Over flat or interior
   points, a preimage is never reflex. Then `W = 2r + 4`. The formula holds
   on all 38,902 strictly simple gluings with area <= 8 bases and d <= 7
   (`check_formula.py`).
2. **Base size.** Each cell has 3 non-A corners, all corners of R, so
   `3 area <= (r + 4) + 3 r`. So `W(R) <= 16` forces area <= 9, inside the
   exhaustive base list. That list has no base with `W(R) < 10`.
3. **d = 1 fails.** A run line holds 2 or more consecutive transparent
   lattice points, so one of them is non-A. That breaks the parity property.
4. **Conclusion.** `W(P) <= 26` needs `d (W(R) - 4) <= 22` with `d >= 2`.
   That leaves `W(R) = 10` with d <= 3, or `W(R) = 12` or 14 with d = 2. All
   these cases are enumerated, with no dark room with a run. W = 28 needs
   `(W(R), d)` in `{(10, 3), (10, 4), (12, 2), (12, 3), (16, 2)}`, all
   enumerated. Only `P6` appears.

## Verification (CHECKED)

`verify_w36.log`: all 11 rooms with W <= 36, 13 pairs (176 s).

- orbitc (d9, complete) calls every pair DARK. `P6`: 62,208 states.
- The d30 `mirror_check.py` tracer, imported unchanged, finds no witness
  with `|q|, |p| <= 20`.
- The fold-back lemma gives the same verdict. All three methods agree.

## Outside the class

- Parity factors `DP -> N` that aren't a gluing of whole copies of one base.
- Targets N that aren't the double of a lattice room.
- Dark rooms with no separating parity factor (none known).
- So W = 24 and W = 26 remain open for dark rooms with a run in general.

## Files

- `glue.py`: base search and gluing enumeration. `python3 glue.py 10 9`.
- `verify.py`: orbitc plus the d30 tracer. `python3 verify.py 36 20`.
- `check_formula.py`: wall formula and the `P6` identity.
- `found.json`: rooms with W <= 40, with copies, runs, and pairs.
