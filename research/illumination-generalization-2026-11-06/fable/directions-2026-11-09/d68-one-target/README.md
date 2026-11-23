# d68: the one-B-target sub-case (OL1) of lemma OL

Date: 2026-11-18. Theory plus a check on existing data only (`covers.json`,
`pair_level.json`). No room, ray, direction, or reflection-word search.
Tags: **PROVED** (argument here), **COMPUTED** (script and log here), **CITED** (file),
**GUESSED** (judgment).

## Answer

- **OL1 is empty (PROVED).** A room with two Q classes has area `n <= 2r + 2`. For
  `r <= 8` that's `n <= 18`, but OL needs area at least 21. So no room in OL's range has a
  class `a` with exactly one B target.
- **The claim holds in every room of the sub-case anyway (CITED).** Every such room has
  `W <= 20` and area at most 18. The d9 census finds no dark same-class pair at `W <= 21`
  and area at most 20 (`d9-census-w22/README.md`, result (a)). Q targets light nothing, so
  a lit pair is lit at the one B target `x`.
- **OL reduces to OL2 (PROVED).** Within OL2, rooms with a Q class (BBBQ) are a finite set:
  one Q class `y` forces `n = 3 r_y + v_y <= 4r + 4 = 36`. Only BBBB rooms are infinite.
  The bound 36 is attained in the d64 data (COMPUTED).
- **Tests (COMPUTED).** All 4,776 rooms in `covers.json` satisfy the counting identity for
  all four classes. Geometric Q agrees with the block-system type Q on 7,124 of 7,124
  classes. The 43 normalized rooms with two or more Q classes all have `n <= 2r + 2`, and
  `n <= 16`. d66's 15 OL1 pairs in 12 rooms all have area 14 or 16, none 21 or more.
- **CPU:** about 1.5 s, one process.

## 1. The counting identity

**Lemma A (PROVED).** Let `P` be a strictly simple lattice room with `n` cells. Fix a
parity class `y`. Then:

`n = cvx_y + 2 smooth_y + 3 rfx_y + 4 int_y`

Each term counts class-`y` lattice points by the number of cells around them: 1 (convex
corner), 2 adjacent (smooth wall point), 3 (reflex corner), or 4 (interior point).

Proof:

1. Each unit cell `[i, i+1] x [j, j+1]` has four corners, one in each parity class.
2. So the number of pairs (cell, class-`y` corner of that cell) is `n`.
3. Count the same pairs by the class-`y` point instead. A point with `k` cells around it
   contributes `k`.
4. Strictly simple rooms have no pinch, so two diagonal cells never occur. A point with
   4 cells is interior. So `k` is 0, 1, 2 (smooth), 3, or 4, as listed.

d64 section 2 step 5 uses the same count on the quotient `K`.

**Lemma B (CITED, COMPUTED).** Class `y` has type Q (`B_y` discrete, `N_y = Q`) exactly
when it has no interior point and no smooth wall point (d66 section 1). The script checks
this against the block-system types in `pair_level.json`: 7,124 agree, 0 disagree.

**Corollary C (PROVED).** If class `y` has type Q, then `n = 3 r_y + v_y`. Here `r_y` and
`v_y` count the reflex and convex corners of class `y`.

## 2. The sub-case: what two Q classes force

Fix the pair's class `a`. The sub-case says that of the three classes `y != a`, exactly one
(`x`) has type B and two have type Q. Class `a` has interior points, so it's transparent.
In R* it has type B. So the room's type is BBQQ. d66's OL1 is exactly the BBQQ rooms.

**Theorem 1 (PROVED).** If a strictly simple room has two classes `y != y'` of type Q, then
`n <= 2r + 2`. With `r <= 8` (`W <= 20`), `n <= 18`.

Proof: add Corollary C for `y` and `y'`.

`2n = 3 (r_y + r_y') + (v_y + v_y') <= 3r + (r + 4) = 4r + 4`

This uses `v = r + 4` for a simple orthogonal polygon. Normalization isn't needed.

**Corollary 2 (PROVED).** OL1 is empty: OL requires area at least 21. COMPUTED: d66's 15
OL1 pairs lie in rooms of area 14 and 16.

**Corollary 3 (CITED).** In every room of the sub-case with `W <= 20`, every same-class
interior pair is lit at the one B target `x`. Proof:

1. By Theorem 1, the room has area at most 18.
2. The d9 census covers every strictly simple room with area at most 20 and `W <= 22`. At
   `W <= 21` it finds no dark same-class pair (d9 result (a)). d9 uses explicit billiard
   paths. They agree with x-lit by d61 FC and the d62 review.
3. A Q target has no regular point, so it lights nothing (d66 section 5). So the lit
   target is `x`.

So the sub-case needs no new lighting argument. Item 2 of the brief, a direct path, isn't
load-bearing. Section 4 records what the data shows about direct paths.

### Structure of rooms with two Q classes (PROVED)

There are two shapes, depending on the difference `y - y'` of the two Q classes.

**Column (or row) type, `y - y' = (0, 1)`.** Then `y` and `y'` are all the lattice points
on the lines `x = e mod 2` for one `e`. The case `(1, 0)` is the transpose.

- The room meets each line `x = e (mod 2)` only in open windows of length 1.
  - An integer point inside such a window lies in the room's interior, so it has 4 cells.
  - Points of a Q class can't have 4 cells, so a window contains no integer point.
  - Windows have integer ends, so each has length 1.
- Vertical walls on these lines have length 1.
- Horizontal walls have length 1, or length 2 with both ends on these lines.
- So the room is a chain or tree of width-2 vertical slabs, centred on the lines
  `x = e + 1 (mod 2)`, joined through unit doors.
- All interior points lie on the slab mid-lines. By d66 Prop. 1, class `a` has at most
  `r_y / 2 <= 4` of them.

**Checkerboard type, `y - y' = (1, 1)`.** The Q points are `a + (1, 0)` and `a + (0, 1)`.

- Every Q point has 0, 1, or 3 cells.
- Every wall has length 1, or length 2 with its midpoint in class `a` or `c = a + (1, 1)`.
- Only classes `a` and `c` have interior points. By d66 Prop. 1, each has at most
  `r / 4 = 2`. So class `a` has exactly one pair, and `X_B(a) = {c}`.

In both types, the reflex corners of the Q classes surround every interior point of the
pair's class (d66 Prop. 1). Area is fixed by the corner counts: `2n = 3 r_Q + v_Q`.

## 3. What this leaves of OL (PROVED)

- **OL = OL2.** Every class with an interior pair has at least two B targets.
- **BBBQ rooms are finite.** If exactly one class `y` has type Q, then
  `n = 3 r_y + v_y <= 3r + (r + 4) = 4r + 4`. For `r <= 8` that's `n <= 36`. So OL2
  rooms with a Q class have area 21 to 36. Only finitely many normalized rooms exist there.
  COMPUTED: the bound is attained. `covers.json` has 885 one-Q rooms with area at least 21,
  with maximum area 36.
  - Both known per-target failures, `cov4181` and `cov4269`, are BBBQ with area 28. So
    they lie in this finite part.
- **BBBB is the only infinite part of OL.** Every normalized room with area greater than
  `4r + 4` has no Q class, so it's BBBB. This sharpens d66's "area > 8r".
- GUESSED: the finite BBBQ part (area 21 to 36, `r <= 8`) could be closed by a bounded
  enumeration, as d9 did at area 20 or less. That's a new search, so it needs Daniel's
  approval. The Q-class constraint (`n = 3 r_y + v_y`) would prune it hard. This note
  doesn't estimate the cost.

## 4. Tests (COMPUTED)

Script `one_target.py`, log `one_target.log`. It reads all 4,776 rooms in `covers.json`
(4,581 normalized) and the types in `pair_level.json`.

| Check | Result |
| --- | --- |
| Lemma A, all 4 classes of all 4,776 rooms | 0 failures |
| Geometric Q against block type Q (rooms in `pair_level.json`) | 7,124 agree, 0 disagree |
| Normalized rooms with two or more Q classes | 43: 42 with two, 1 with three. 35 are in R*. |
| Q-pair difference | `(0, 1)`: 17, `(1, 0)`: 13, `(1, 1)`: 13 |
| Area of those rooms | 8 to 16. `max (n - 2r - 2) = -2` among normalized rooms, `0` over all 4,776 rooms |
| OL1 pairs (from `pair_level.json` R* types) | 15 pairs in 12 rooms, areas 14 and 16, `r = 8`. None at area 21 or more. |
| d66 pair verdicts on those 12 rooms | all pairs lit |
| Straight segment `ST` in the room interior | 12 of 15 |

The 3 pairs without a direct segment are in `cov732` (S `(2,2)`, T `(6,2)`) and `cov813`
(two pairs). d66's orbit verdict lights them, and d9 covers them.

Named rooms: none of the d66 named rooms has two Q classes (types in `pair_level.log`). So
none is in the sub-case.

The d64 data files `dark_pairs.json` and `rl_*.json` hold only rooms with a proper factor,
so they're outside R*. Their rooms are in `covers.json`, so the bound check above includes
them.

## Files and CPU

| File | Content | CPU |
| --- | --- | --- |
| `one_target.py`, `one_target.log` | Counting identity, Q check, two-Q area bound, OL1 pair list, straight-segment test | 0.25 s |
| (inline check, not saved) | One-Q rooms: `n = 3 r_y + v_y` on all 2,217, max area 36 | about 1 s |

Run with `python3 -B one_target.py` from this directory. Nothing was written outside this
directory, and nothing in git changed.
