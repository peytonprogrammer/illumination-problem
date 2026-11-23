# Adversarial review of direction 3 (`d3-two-mechanisms/audit.md`)

Reviewer: independent agent, 2026-11-09. The reviewer read every proof line by
line, re-derived each step, wrote a separate exact-arithmetic model of the
unfolding, and re-ran the author's certificate. The reviewer didn't import or
read the author's tracer before writing `surface.py`.

## Verdicts

| Claim | Verdict |
| --- | --- |
| Fact 0 (`|C| >= 3`) | ACCEPT, under the stated normalization |
| Lemma 1 and Corollary 1 (corrected Claim 1) | ACCEPT |
| Cross counterexample to the "if" half | ACCEPT |
| Lemma A | ACCEPT |
| Theorem B | ACCEPT |
| Theorem Q22 | ACCEPT, with two small completions |
| Theorem A | ACCEPT, with one correction to the remark after it |
| Proposition X | ACCEPT; the proof covers every rational direction |

No claim is rejected. No counterexample was found.

## Notes per claim

### Fact 0

The proof is correct. It needs the normalization that the x-differences and
the y-differences of the vertices each have gcd 1. Without it, the claim is
false: the room `[0,2]^2` has one corner class. The normalization is free,
because the map `diag(a, b)` commutes with reflections in axis-parallel lines
and so maps billiard paths to billiard paths. Rescaling changes which points
count as lattice points, so state the normalization with every use of `C`.

Checked: the 22-wall room has `C = E[2]`. The cross has
`C = {(0,1), (1,0), (1,1)}`.

### Lemma 1 and Corollary 1

Every step re-derives.

- Corollary 1: the closed unit square `Q` is a fundamental domain for the
  reflection group, so exactly one image `T*` lies in `Q`. The three cases are
  exhaustive and each one is correct. In the lattice case, every candidate
  contains `s + m0` because `k = 1 < 2g`.
- Lemma 1 (a), second case: the reviewer re-derived
  `y = b (mu - 1) / (2 - (1 + mu) a)` at `x = -1`. In the case `b = 0`, the
  open segment meets only `x = 0`, where `y = 2 / (1 + mu)`. Both are correct.
- The three cases (a), (b), and (c) cover every `(s, u)`. When `s` is a
  lattice point, `u + s` and `u - s` are congruent mod 2.
- The author's brute-force check reproduces: `45500 ... cases agree`.

These are torus statements only. The author says this correctly. A clean
candidate doesn't give a legal path, because the developed segment can end on
another sheet over the same torus point.

### Lemma A

The proof is complete. The reviewer checked each edge case.

- **Cylinders on `DP` versus `M`.** `tau` has derivative `-1`. An isometry of
  an open flat cylinder with derivative `-1` is `(x, y) -> (a - x, h - y)`. It
  has two interior fixed points. The fixed points of `tau` are corner lifts,
  which lie outside every open cylinder. So `tau` pairs the cylinders, and
  `DP` has one cylinder exactly when `M` has two.
- **Poles.** Convex corners have cone angle `2 pi` on `M` and `pi` on `DP`.
  They're in `Sigma`, so they count as singular. The author's tracer and the
  reviewer's model both mark them.
- **Two lifts.** The four lifts of `S` to `M` form two `tau`-orbits, which are
  the two lifts to `DP`. The sufficient condition tests all four `L` values,
  `+-(q s1 - p s2)` and `+-(q s1 + p s2)`.
- **Target on the cylinder boundary.** This case is allowed. The source must
  lie in the open strip, so the open segment lies in the open strip.
- **Target equal to a singularity.** This case can't happen, because an
  interior `T` has no corner lift.
- **Regular lattice points and flat boundary points.** These are unmarked
  points of cone angle `2 pi`. A geodesic through them projects to a legal
  path: it passes straight through an interior lattice point or reflects at a
  flat wall point.
- **Paths along walls.** A geodesic in `M` that avoids `Sigma` can't run along
  a wall. Reaching a wall end-on means reaching a vertex.

### Theorem B

The proof is correct. One caution belongs to the remark after Theorem A, not
to Theorem B. That remark says that pairs with two irrational endpoints
"follow from Theorem B when a one-cylinder direction exists". That's false
when the only direction is axis-parallel. For `(p, q) = (1, 0)`, the set `X`
is `R x Z`, which contains irrational points. **Correction:** require a
one-cylinder direction with `p q != 0`, as the "Consequence" paragraph already
does.

### Theorem Q22

The proof is complete, given the certificate. The reviewer re-verified each
input.

1. **Certificate.** The reviewer's model gives two cylinders on `M` in
   directions `(4,7)`, `(7,4)`, `(4,-7)`, `(7,-4)`, `(-4,7)`, and `(-7,-4)`.
   The certificate is simpler than the author's. The strip permutation has
   exactly 2 cycles: 420 slots for `(4,7)` and 240 slots for `(7,4)`. Each
   strip lies in one cylinder, and `tau` forces at least 2 cylinders. So
   `strips = 2` proves `#cyl(M) = 2` with no leaf-regularity test.
2. **`X = Z^2`.** The reviewer re-derived it by hand and confirmed it by brute
   force over `(1/56) Z^2 mod Z^2`.
3. **Interior lattice points.** The reviewer rebuilt the room from the
   manuscript's copy formulas. The vertex cycle matches the manuscript's 22
   vertices, with 13 convex and 9 reflex. The interior lattice points are
   exactly `(0,0)` and `(2,2)`.
4. **Darkness of `(0,0)`, `(2,2)`.** See
   [Manuscript darkness proof](#manuscript-darkness-proof).

**Lattice pairs.** The parent brief asked about pairs of non-A lattice points
and pairs of different parity classes. The room has two interior lattice
points, both of class `(0,0)`. So the only pair of distinct interior lattice
points is the dark pair, and the other cases are empty. Every other pair has
an endpoint outside `X = Z^2`, and Theorem B covers it. The A/non-A
distinction plays no role.

**Completion 1: self-pairs.** Lemma A covers only "every other" point. Self
illumination is immediate in both cases:

- For `S` outside `X`, the closed regular leaf through `s^` is a legal loop.
- For the two marks, the reviewer's two tracers confirm explicit loops.
  `(0,0)` uses direction `(-2,-4)` with reflections at `(-1/2,-1)`, `(-1,0)`,
  and `(-1/2,1)`. `(2,2)` uses `(-4,2)` with reflections at `(1,5/2)`,
  `(2,3)`, and `(3,5/2)`.

Both loops reflect at a flat boundary lattice point (`(-1,0)` and `(2,3)`). If
contact with flat boundary lattice points were also forbidden, the parity
argument would show that neither mark illuminates itself. That convention
isn't the one the manuscript uses.

**Completion 2: convention robustness for distinct pairs.** The strips contain
no lattice point, and each cylinder equals one strip. So every Lemma A path in
Q22 avoids all lattice points, except possibly its endpoint `T`. The
distinct-pair statement therefore holds whether or not flat boundary lattice
points are forbidden. Forbidding them only makes `(0,0)`, `(2,2)` darker.

### Manuscript darkness proof

The proof in
`illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex`
is complete. The reviewer checked each step.

- The integer points of `P` are its 10 vertices plus `a` and `b`, which are
  flat. Computed: 7 convex, 3 reflex, and 2 flat.
- The copies meet only along `H` and `V`. The 30 corner incidences split into
  8 at the four seam endpoints `E_j` and 22 at the vertices of `Q`. So every
  smooth boundary point of `Q` other than the `E_j` folds to a smooth point of
  `P`. Interior seam points fold to the open top edge and the open right edge
  of `P`, which contain no vertex.
- The parity lemma: the point `z = B / 2^r` lies strictly inside the segment
  and has an odd coordinate. Its fold is an integer point of `P` other than
  `a` and `b`, so it's a vertex.
- Reversal at `E_j`: the velocity computation is correct for all four points.
- "Reversals don't help": the folded motion is deterministic away from convex
  corners. Crossing a seam and reflecting at a wall both fold to a reflection.
  After the first reversal, the path retraces to `a`. This contradicts the
  choice of the last visit to `a`. Retracing can't meet a corner before `a`,
  because the route before the reversal met none.
- Axis-parallel paths are excluded correctly, so no leg runs along a seam.

As a consistency check, all four lifts of each mark lie on singular leaves in
`(4,7)` and `(7,4)`. Lemma A requires this if the pair is dark.

### Theorem A

The proof is correct. It's a standard multi-twist orbit-closure argument, and
step 6 is brief. The step needs the following fact: the union `W` of the
cylinder closures reached is open, because the cylinders around any point,
including a cone point, chain through shared horizontal and vertical
cylinders. `W` is also closed, and `M` is connected. Q22 doesn't use
Theorem A.

### Proposition X

The proof covers every rational direction `(p, q)`, including the
axis-parallel ones. It isn't limited to `p, q <= 12`. The reviewer checked
each step.

- The mirror elements act on charts as translations by `-eps (4, 0)` and
  `-eps (0, 4)`, which lie in `2Z^2`. So they're translation automorphisms
  over `E`. They act freely because neither axis contains a parallel wall and
  the centre isn't a corner.
- A translation automorphism that stabilizes an open cylinder is a rotation.
  A free group of rotations is cyclic, so the stabilizer has order 1 or 2.
  Each `N`-cylinder therefore has at least 2 preimages.
- `tau` commutes with `V`, so it descends to `N`. If `N` has one cylinder,
  `tau` swaps its two boundary components. Each boundary component contains a
  marked point, so its `L` value is an integer `L1`. Then `-L1 = L1` mod 2.
  So all three marked points have equal `L` mod 2, which is impossible for
  coprime `(p, q)`.
- The unmarked convex corners of the quarter L-shape are fixed by `tau` on
  `N`. They're unmarked, so they don't conflict with the argument.

The reviewer's model gives a histogram of `{3: 30, 4: 13}` on `DP` for
`1 <= p, q <= 8`, with no one-cylinder direction. This matches the author.

## Independent computations

All scripts are in this directory and use exact `int` or `Fraction`
arithmetic.

| File | Content |
| --- | --- |
| `surface.py` | Square-tiled model of `M`: 4 sheets times the cells, with permutations `r` and `u`. It provides a strip-cycle cylinder counter and a developed-segment ray-caster. |
| `check_q22.py` | Room checks, cylinder counts, `X`, mark leaves, and controls. Output is in `check_q22.log`. |
| `pairs.py` | Explicit paths between `(1/N)`-grid points. A second room-coordinate tracer re-checks every path. |
| `paths-N*.txt`, `pairs-N*.log` | One explicit path per lit pair, with the search summaries. |

### Results

- `check_q22.py` reports the following:
  - The `q22` histogram for `max(p, q) <= 14`, both signs, is
    `{1: 16, 3: 98, 5: 100, 6: 40}`.
  - The one-cylinder directions are `(4,7)`, `(4,9)`, `(7,4)`, `(8,11)`,
    `(8,13)`, `(9,4)`, `(11,8)`, and `(13,8)`, each with both signs.
  - Both results match `cylcount.py` exactly.
  - Controls: the square has 1 cylinder in every direction. `L3` has 1
    cylinder exactly when `p` and `q` are odd. `stair5` and `plus` give 1
    cylinder in the directions that the author certifies.
- The author's `python3 onecyl_verify.py q22 4 7 7 4` prints
  `components=2 -> ONE cylinder on DP (certified)` for both directions. This
  agrees with the reviewer's result.
- `pairs.py` gives the following results.

  | `N` | Points | Pairs including `S = T` | Lit by explicit path | Not found |
  | --- | --- | --- | --- | --- |
  | 1 | 2 | 3 | 2 | `(0,0)`, `(2,2)` (2,304 candidates) |
  | 2 | 33 | 561 | 560 | `(0,0)`, `(2,2)` |
  | 3 | 94 | 4,465 | 4,464 | `(0,0)`, `(2,2)` |
  | 4 | 185 | 17,205 | 17,204 | `(0,0)`, `(2,2)` (2,304 candidates) |

  For every lit pair, the M-surface ray-caster and the room tracer agree on
  the endpoint, and neither tracer touches a vertex. These runs are
  consistency checks. The theorem doesn't depend on them.

## Theorem the reviewer signs

**Theorem.** Let `Q` be the polygon with the 22 vertices listed in
`manuscript.tex` (eq. `vertices`). It is the union of the 15 closed unit cells
`P0 ∪ P1 ∪ P2` of that manuscript. Make the following assumptions:

- "Interior" means the topological interior of `Q`, including the open seams.
- A billiard path is a finite polygonal path of positive length with specular
  reflection at boundary points that aren't vertices of `Q`. This includes the
  six flat boundary lattice points `(-1,0)`, `(1,0)`, `(2,-2)`, `(2,1)`,
  `(2,3)`, and `(4,0)`.
- Any path that meets one of the 22 vertices ends there and doesn't count.

Then, for distinct `S, T` in `int Q`, no billiard path joins `S` to `T` if and
only if `{S, T} = {(0,0), (2,2)}`. Every interior point also joins itself.

**Addendum.** The distinct-pair statement still holds if paths are also
forbidden to touch the six flat boundary lattice points. Under that stricter
rule, the marks don't illuminate themselves.

The proof uses no outside theorem. Its only computed input is the cylinder
count of `M` in directions `(4,7)` and `(7,4)`. Two independent programs
certify that count: the author's union-find and the reviewer's strip-cycle
count.

## What remains unverified

- The record's family theorems and the `W <= 21`, `k <= 6` theorem. The
  reviewer didn't open them.
- The cited literature, including theorem numbers. No network was used.
- The author's corollaries for the plus pentomino and the staircase: the
  reviewer confirmed only the cylinder counts, not that each room has no
  interior lattice point. The cell lists make that fact plain.
- The general Target 3 conjecture and the existence question for one-cylinder
  directions. Both remain open.
- The author's `N = 12` deepening run, which is still in progress. Q22 doesn't
  depend on it.
