# Audit of direction 3: two mechanisms of darkness

Independent audit, 2026-11-09. Scope: Claim 1, Claim 2, and Target 3 of
direction 3 in `fable/research-directions-2026-11-09.md`.

Every statement carries one of four labels:

- **PROVED**: the argument is in this file.
- **CITED**: an outside theorem, with source and theorem number.
- **CHECKED BY COMPUTATION**: exact integer computation, with the command.
- **CONJECTURAL**: not proved here or elsewhere.

This audit ran no search for rooms. All computations use the 22-wall room of
the record and four textbook shapes. Nothing here is independently reviewed.

## Verdicts

1. **Claim 1 is false as stated and true after one correction.** The "only if"
   half holds. The "if" half fails for the 12-wall cross. The correct statement
   is Lemma 1. The sieve sketch does not prove either half.
2. **Claim 2 is a classification by fold class, not by mechanism.** Torus-level
   blocking alone never proves darkness when the room has a transparent lattice
   point. "Sheet-arrival failure" is the whole illumination problem for
   non-corner pairs, renamed.
3. **The record has a real gap for non-A pairs.** The `W <= 21`, `k <= 6`
   theorem covers interior A pairs only. Outside the family theorems, rational
   non-A pairs are unproved for `9 <= W <= 21`. The record states this limit
   itself.
4. **Target 3 is proved for the 22-wall room and open in general.** The
   22-wall room has one dark pair among all real interior pairs: `(0,0)`,
   `(2,2)` (Theorem Q22). The proof uses a one-cylinder lemma (Lemma A) that
   needs no outside theorem.
5. **The cylinder method has a proved limit.** The cross has no one-cylinder
   direction (Proposition X). Symmetric rooms need a different lemma.

## Setting and notation

- `P` is a simple orthogonal polygon with vertices in `Z^2`. The vertex
  x-coordinates have gcd 1 after translation, and so do the y-coordinates.
- `K = (Z/2)^2` acts by sign changes. `M` is the unfolding: four copies
  `(P, eps)`, `eps` in `K`, glued along walls.
- The map `(x, eps) -> eps x` sends `M` to the torus `E = R^2 / 2Z^2`. It is a
  translation cover. Lattice points of `P` map to `E[2] = Z^2 / 2Z^2`.
- `F : P -> [0,1]^2` is the fold. `F(S) = F(T)` holds exactly when `T` lies in
  `gamma S + 2Z^2` for some `gamma` in `K`.
- `tau` is the element `-1` of `K` acting on `M`. Its fixed points are exactly
  the corner lifts. `DP = M / tau` is the double of `P`, a sphere.
- `Sigma` is the set of corner lifts in `M`. A geodesic of `M` that avoids
  `Sigma` projects to a legal billiard path.
- `C` is the set of **corner classes**: the classes in `E[2]` of the corners of
  `P`.
- A **candidate** for `(S, T)` is a segment from `s = S` to a point `t'` in
  `gamma T + 2Z^2`, with `t' != s`. A candidate is **C-blocked** when its open
  segment contains a lattice point whose class is in `C`. A candidate is
  **clean** when its open segment contains no lattice point.
- A pair is **dark** when no legal billiard path joins `S` to `T`.

**Fact 0 (PROVED).** `C` has at least three elements.

Proof. Walk around the boundary. Each wall changes one coordinate. The vertex
classes form a closed walk in `E[2]` whose steps change at most one coordinate
parity. Both x-parities occur, because the x-coordinates have gcd 1. Both
y-parities occur for the same reason. A connected walk that sees both x-values
and both y-values visits at least three classes.

Both cases occur. The cross has `|C| = 3`. The 22-wall room has `|C| = 4`.

## Claim 1: the torus-level lemma

### Lemma 1 (PROVED)

Fix a point `s` in `R^2` and one image class `u + 2Z^2`, where `u = gamma t`.

- **(a) Generic class.** Suppose `u + s` is not in `2Z^2`. Suppose also that
  `s` is not a lattice point or `u - s` is not in `2Z^2`. Then the class
  contains a clean candidate.
- **(b) Antipodal class.** Suppose `u + s` is in `2Z^2` and `s` is not a
  lattice point. Then every candidate in the class has a lattice midpoint.
  Every candidate in the class is C-blocked if and only if `C = E[2]`.
- **(c) Lattice class.** Suppose `s` is a lattice point and `u - s` is in
  `2Z^2`. Then every candidate in the class is C-blocked if and only if `C`
  contains the three classes other than the class of `s`.

**Corollary 1 (PROVED).** Every candidate over all four image classes is
C-blocked if and only if both conditions hold:

1. `S` and `T` are lattice points with `S = T` mod 2. Equivalently,
   `F(S) = F(T)` is a pillow corner.
2. `C` contains the three classes other than the class of `S`.

By Fact 0, condition 2 fails exactly when `|C| = 3` and the class of `S` is a
corner class.

### Proof of Corollary 1

This short proof does not need parts (a) and (b).

The four image classes of `T` form one orbit of the reflection group of the
unit-square tiling. Let `Q` be a closed unit square that contains `S`. Exactly
one image `T*` of `T` lies in `Q`.

- If `T* != S`, the segment from `S` to `T*` lies in `Q`. The lattice points of
  `Q` are its four vertices. A vertex of a convex set is not interior to a
  segment of that set. The candidate is clean.
- If `T* = S` and `S` has a non-integer coordinate, say `s2`, reflect `S`
  across a vertical side of `Q` that does not contain `S`. The segment from `S`
  to its mirror image is horizontal at a non-integer height. The candidate is
  clean. The case of a non-integer `s1` is the same with a horizontal side.
- If `T* = S` and `S` is a lattice point, the candidates are `t' = s + 2m`,
  `m != 0`. Write `m = g m0` with `m0` primitive. The lattice points of the
  open segment are `s + k m0`, `0 < k < 2g`. For `g = 1` the only lattice point
  is `s + m0`. Its class is the class of `s` plus the class of `m0`. Primitive
  vectors realize all three nonzero classes. So all candidates are C-blocked
  exactly when `C` contains the three other classes. Conversely, when `C`
  contains them, the point `s + m0` blocks every candidate.

### Proof of Lemma 1 (a) and (b)

**(b).** Each candidate is `t' = -s + 2m`, with midpoint `m` in `Z^2`. Fix a
class `e`. Let `m` be the vertex of class `e` of a unit square that contains
`s`. The half segment from `s` to `m` lies in that square, so it has no lattice
point before `m`. The other half is the point reflection through `m`, which
preserves `Z^2`. So this candidate meets `Z^2` only at `m`. If `C` omits `e`,
this candidate is not C-blocked. If `C = E[2]`, the midpoint blocks every
candidate.

**(a), first case.** If `u - s` is in `2Z^2`, then `s` is not a lattice point.
Use `s + (2,0)` when `s2` is not an integer, and `s + (0,2)` otherwise.

**(a), second case.** Suppose `u - s` is not in `2Z^2`. Choose `t'` in the
class with `|t'_i - s_i| <= 1` for both coordinates. If the candidate is clean,
stop. Otherwise a lattice point `z` lies on the open segment. Translation by
`z` preserves all hypotheses, so take `z = 0`. Reflect so that
`s = (-a, -b)` with `a, b >= 0`. Then `t' = (mu a, mu b)` with `mu > 0`,
`(1 + mu) a <= 1`, and `(1 + mu) b <= 1`. The antipodal condition is
`mu = 1`, which the hypothesis excludes.

- If `b > 0`, use `t'' = t' - (2, 0)`. The open segment meets a vertical
  integer line only at `x = -1`. There
  `y = b (mu - 1) / (2 - (1 + mu) a)`. The denominator is at least 1, so
  `|y| <= b |mu - 1| < b (1 + mu) <= 1`. Also `y != 0`. So `y` is not an
  integer and the candidate is clean.
- If `b = 0`, use `t'' = t' + (0, 2)`. The open segment meets a vertical
  integer line only at `x = 0`, where `y = 2 / (1 + mu)`. This value lies in
  `(0, 2)` and equals 1 only for `mu = 1`. The candidate is clean.

**(c)** is the third case of the proof of Corollary 1.

**CHECKED BY COMPUTATION.** `lemma1_check.py` compares Lemma 1 with brute force
for all `s` in `(1/N) Z^2`, all image classes, and all admissible `C`, for
`N <= 6`. Output: `45500 (s, image class, C) cases agree`.

### Counterexample to the "if" half

**PROVED and CHECKED BY COMPUTATION.** Take the cross: the union of
`[0,4] x [1,3]` and `[1,3] x [0,4]`. Its 12 corners have classes `(1,0)`,
`(0,1)`, and `(1,1)`. Take `S = (1,2)` and `T = (3,2)`. Both are interior
lattice points of class `(1,0)`, so `F(S) = F(T)` is a pillow corner.

The straight segment from `S` to `T` meets `Z^2` only at `(2,2)`. That point is
interior and its class `(0,0)` is not a corner class. The pair is lit by the
direct segment. `leafcheck.py cross 1 20` reports 5 interior lattice points and
0 unjoined pairs.

So "`F(S) = F(T)` is a pillow corner" does not imply torus-level blocking.

### The sieve sketch does not work

The sketch equates "blocked" with "not primitive in `L = Z^2 + Z s + Z beta`".
That equivalence is false.

**PROVED.** Take `s = (sqrt 2, 0)` and `t' = (3, 0)`. Then
`L = Z^2 + Z (sqrt 2, 0)` has rank 3, and `d = t' - s` is primitive in `L`.
The segment from `s` to `t'` passes through `(2, 0)`.

A lattice point on the segment means `z - s = lambda d` for a real `lambda`.
That is a statement about a real multiple of `d`, not about `d / p` in `L`.
The sketch also ignores which lattice classes are corner classes.

## Claim 2: the two mechanisms

**Verdict.** Keep the fold-class split. Drop the claim that the two classes
are two mechanisms.

- **PROVED (Corollary 1).** If `F(S) = F(T)` is not a pillow corner, a clean
  candidate exists. So torus-level blocking never explains darkness there.
  This holds for every pair, rational or not. The phrase "generic rational
  position" in the memo is too narrow.
- **PROVED (Corollary 1).** If `S` and `T` are lattice points of different
  classes, a clean candidate also exists.
- **Torus-level blocking is not a darkness proof.** A C-blocked candidate can
  pass through a transparent lattice point on `M` and miss every corner. The
  22-wall room has `k = 4` transparent lattice points. Its darkness proof in
  `illumination-k4-codex/restricted-theorem-note/` uses the fold onto the
  five-square staircase, which is sheet data.
- So every dark pair needs a sheet-level argument. "Sheet-arrival failure" for
  non-corner pairs has no extra content: it restates "dark although clean
  candidates exist".

**Heuristic, not a proof.** A deck involution `iota` with derivative `-1`
blocks the pair `(x, iota x)` when all its fixed points are singular. On a
room unfolding the only such involution is `tau`. For a non-corner point,
`tau` removes only the antipodal lift class, which is Lemma 1 (b). Three other
classes keep clean candidates. A non-corner dark pair therefore needs an
obstruction that is not an involution. The Heisenberg control has that kind of
obstruction. This paragraph explains why no planar example is known. It does
not exclude one.

## Literature and record coverage for non-A pairs

### Literature (CITED)

Theorem numbers follow the arXiv versions read during this audit.

- **Lelièvre, Monteil, and Weiss, arXiv 1407.2975, Theorem 2.** On any
  translation surface, each point fails to illuminate at most finitely many
  points.
- **Same paper, Theorem 11 (journal Theorem 10).** On a square-tiled surface
  the non-illuminating pairs form a finite set plus finitely many embedded
  translation surfaces. The record uses this theorem for rationality.
- **Wolecki, arXiv 1905.09358v3, Theorem 1.2 (i) and Lemma 2.1.** A rational
  polygon has finitely many dark pairs.
- **Hubert, Schmoll, and Troubetzkoy, arXiv math/0602394, Theorem 1 and
  Theorem 2.** The dark pairs are countable on a prelattice surface and finite
  on a Veech surface.
- **Same paper, Theorem 8.** Non-illuminable configurations are the involution
  pairs and "some pairs of periodic points". The paper states that those pairs
  need a case-by-case check.
- **Same paper, Lemma 30.** Non-periodic points illuminate themselves.
- **Same paper, Lemma 32.** On staircase covers of `R^2 / 2Z^2` branched over
  `Z^2 / 2Z^2`, a point `z` does not illuminate the fibre over `-pi(z)`. This
  is the antipodal class of Lemma 1 (b) with `C = E[2]`.
- **Apisa and Wright, arXiv 1708.03411, Corollary 3.8 and Proposition 3.11.**
  Finite blocking is classified for surfaces that are not torus covers.
  Proposition 3.11 lists the torus-cover cases.

**Gap in the literature.** No cited theorem classifies dark pairs of periodic
(rational) points on a torus cover. Hubert, Schmoll, and Troubetzkoy leave
those pairs to case-by-case checks. Two web searches during this audit found
no later paper that closes the case. That is a bounded search, not a proof of
absence.

### Project record

- **Irrational endpoints are covered.**
  `review/dark-endpoint-rationality.md` and its supplement prove that both
  endpoints of a dark interior pair are rational. The proof imports the
  theorems of Lelièvre, Monteil, and Weiss and of Wolecki. Label: PROVED in the
  record, dependent on CITED theorems.
- **Interior A pairs are covered for `W <= 21` and `k <= 6`.** Source:
  `illumination-k4-codex/restricted-theorem-note/theorem.txt`. The statement
  quantifies over "distinct interior A points" only.
- **All real pairs are covered for `W <= 8`** and for the listed family
  theorems. Source: `codex-proof-verification/results-inventory-2026-11-07.md`,
  result 2.
- **Rational non-A pairs are not covered for `9 <= W <= 21`.** Scaling a
  rational pair to an A pair multiplies the lattice and can raise `k` past 6.
  The record says so in `review/dark-endpoint-rationality-supplement.md` and in
  `review/bridge.md`, items B1 and B6. A grep of the record for "non-A",
  "rational mark", and "periodic point" finds no theorem that fills the gap.

**Verdict on the "sharp restricted minimum".** The theorem is correct as
stated. It is a statement about A pairs. It does not show that a room with
`W <= 21` has no dark pair. The gap is acknowledged in the record. It is not an
error in the theorem, but the summary line in the directions memo hides it.

## Target 3: results

**Precise form of Target 3 (CONJECTURAL).** In a simple orthogonal lattice
room, every dark interior pair consists of two lattice points of the same class
mod 2.

The results in this section prove it for three rooms and isolate what the
general case needs.

### Cylinders

Fix a rational direction `theta = (p, q)`. A leaf through a point of `Sigma` is
singular. The other leaves are closed. `M` minus the singular leaves is a
finite union of open cylinders.

`tau` never maps a cylinder to itself. A half-turn of a cylinder has two fixed
points in its interior, and the fixed points of `tau` lie in `Sigma`. So the
cylinders of `M` come in pairs, and `#cyl(DP) = #cyl(M) / 2`.

`theta` is a **one-cylinder direction** when `M` has exactly two cylinders,
`Cyl` and `tau Cyl`.

The function `q x - p y` is constant on leaves and well defined mod 2 on `E`.
Corner lifts have integer values. So a leaf with a non-integer value is
regular. The four lifts of `S` have values `+-(q s1 - p s2)` and
`+-(q s1 + p s2)`.

### Lemma A (PROVED)

Let `theta` be a one-cylinder direction of `DP`. Let `S` be an interior point
with a lift on a regular `theta`-leaf. Then `S` illuminates every other
interior point `T`, with real coordinates allowed.

Proof.

1. Choose the lift `s^` of `S` on a regular leaf. It lies in an open cylinder.
   Replace `s^` by `tau s^` if needed, so that `s^` lies in `Cyl`. Both are
   lifts of `S`.
2. `M` is the union of the closures of `Cyl` and `tau Cyl`. Choose a lift `t^`
   of `T`. Replace `t^` by `tau t^` if needed, so that `t^` lies in the closure
   of `Cyl`.
3. The closure of `Cyl` is the image of a closed strip `R x [0, h]` under a map
   `phi` that is a local isometry on the open strip. Write `s^ = phi(xs, ys)`
   with `0 < ys < h`, and `t^ = phi(xt, yt)` with `0 <= yt <= h`.
4. The straight segment from `(xs, ys)` to `(xt, yt)` has its interior in the
   open strip. Its image has its interior in `Cyl`, which contains no point of
   `Sigma`. The endpoint `t^` is not in `Sigma`, because `T` is interior.
5. The image is a geodesic of `M` from `s^` to `t^` that avoids `Sigma`. It
   projects to a legal billiard path from `S` to `T`.

**Sufficient condition.** A lift of `S` lies on a regular leaf when
`q s1 - p s2` or `q s1 + p s2` is not an integer.

**Lemma A' (PROVED, same proof).** Fix any rational direction and an open
cylinder `Cyl` of `M`. If a lift of `S` lies in `Cyl` and a lift of `T` lies in
the closure of `Cyl`, then `S` illuminates `T`.

### Theorem B (PROVED)

Let `theta_i = (p_i, q_i)` be one-cylinder directions of `DP`. Define

    X = { s in R^2 : q_i s1 - p_i s2 and q_i s1 + p_i s2 are integers for all i }.

Then every interior point outside `X` illuminates every other interior point.
Both endpoints of every dark pair lie in `X`.

`X` contains `Z^2`. For one direction with `p0 q0 != 0`, `X` lies in
`(1 / (2 q0)) Z x (1 / (2 p0)) Z`.

Proof. Apply Lemma A with its sufficient condition. Darkness is symmetric, so
both endpoints lie in `X`. For the bound, add and subtract the two conditions:
`2 q0 s1` and `2 p0 s2` are integers.

**Consequence.** A room with one one-cylinder direction that is not
axis-parallel has finitely many dark pairs, all rational, with an explicit
denominator bound. This proof does not use the cited theorems.

**Remark (PROVED).** An affine automorphism that preserves `Sigma` maps
one-cylinder directions to one-cylinder directions. Horizontal and vertical multi-twists therefore shrink `X` further.

### Theorem Q22 (PROVED, given two computed certificates)

The 22-wall room is the room of
`illumination-k4-codex/restricted-theorem-note/attainment-check.txt`: 15 unit
cells, marks `(0,0)` and `(2,2)`.

**Statement.** Among all real interior pairs of the 22-wall room, the pair
`(0,0)`, `(2,2)` is the only dark pair.

Proof.

1. **CHECKED BY COMPUTATION.** The directions `(4,7)` and `(7,4)` are
   one-cylinder directions of `DP`. Command:
   `python3 onecyl_verify.py q22 4 7 7 4`. Output for both: `components=2`,
   `ONE cylinder on DP (certified)`. `cylcount.py q22 14` gives the same answer
   by a different count.
2. **PROVED.** For these two directions `X = Z^2`. The four conditions are
   `7 s1 +- 4 s2` in `Z` and `4 s1 +- 7 s2` in `Z`. Sums and differences give
   `14 s1`, `8 s1`, `8 s2`, `14 s2` in `Z`. So `2 s1` and `2 s2` are integers.
   Write `s1 = a / 2`, `s2 = b / 2`. Then `7a + 4b` even forces `a` even, and
   `4a + 7b` even forces `b` even.
3. **CHECKED BY COMPUTATION.** The interior lattice points are `(0,0)` and
   `(2,2)` only. This agrees with the record (`I = 2`).
4. By Theorem B, every interior point other than `(0,0)` and `(2,2)`
   illuminates every interior point.
5. The record proves that `(0,0)` and `(2,2)` is dark.

**Consequence.** Target 3 holds for the only dark orthogonal room in the
record. The non-A gap is closed for this one room, for real pairs, with no
outside theorem.

**Direction 5 falsifier.** Lemma A and the darkness proof force both marks onto
singular leaves in every one-cylinder direction. **CHECKED BY COMPUTATION:**
for `max(p, q) <= 14` the one-cylinder directions are `(4,7)`, `(7,4)`,
`(4,9)`, `(9,4)`, `(8,11)`, `(11,8)`, `(8,13)`, `(13,8)`. In each one, both
marks lie on singular leaves. The room passes the falsifier test.

### Corollaries for two small rooms (PROVED, given computed certificates)

- **Plus pentomino (12 walls).** Directions `(1,1)` and `(1,2)` are certified. The
  conditions give `s1 = (2 s1 + s2) - (s1 + s2)` in `Z`, so `X = Z^2`. The room
  has no interior lattice point. Every real interior pair is lit.
- **Five-square staircase (10 walls).** Directions `(1,1)` and `(2,3)` are certified. The
  conditions give `s1 = (3 s1 + 2 s2) - 2 (s1 + s2)` in `Z`, so `X = Z^2`. The
  room has no interior lattice point. Every real interior pair is lit.

Neither room is in the `W <= 8` theorem. Whether the record's family theorems
cover them was not checked.

### Theorem A (PROVED): one irrational endpoint

Let `T` be a rational interior point. Let `S` be an interior point with an
irrational coordinate. Then `S` illuminates `T`.

Proof.

1. Fix a lift `t^`. Let `Sigma'` be `Sigma` plus the four lifts of `T`. All
   points of `Sigma'` are rational.
2. The horizontal cylinders relative to `Sigma'` have rational heights and
   circumferences. A horizontal multi-twist `h` fixes every cylinder boundary
   pointwise. A vertical multi-twist `v` does the same. Both fix `t^` and
   preserve `Sigma`.
3. `Lit(t^)` is the set of points joined to `t^` by a geodesic that avoids
   `Sigma`. It is open, it contains a punctured disk around `t^`, and it is
   invariant under `h` and `v`.
4. Let `Y` be the closure of the orbit of a lift `s^` under `h` and `v`.
   Suppose `s2` is irrational. The other case is symmetric. `h` rotates the horizontal leaf through `s^` by
   an irrational fraction of its length. So `Y` contains that leaf.
5. That leaf crosses each vertical cylinder that it meets from side to side.
   Its points with irrational `x` have dense `v`-orbits on their vertical
   leaves. So `Y` contains the closure of every vertical cylinder that the
   leaf meets.
6. Repeat with the roles exchanged. `M` is connected, so `Y = M`.
7. Some orbit point lies in `Lit(t^)`. Invariance gives `s^` in `Lit(t^)`.

Pairs with two irrational endpoints follow from Theorem B when a one-cylinder
direction exists. Without one, they depend on the record's rationality theorem
and its cited inputs.

### Proposition X (PROVED): the cross has no one-cylinder direction

Proof.

1. The cross has two mirror axes, `x = 2` and `y = 2`. Each reflection,
   combined with the matching element of `K`, acts on `M` as a translation
   automorphism. These generate a group `V = (Z/2)^2`. No axis meets a wall
   parallel to it, and the centre is interior. So `V` acts freely.
2. The quotient `N = M / V` is the unfolding of the three-cell L-shape. `Sigma`
   is the full preimage of three points of `N`: the lifts of `(0,1)`, `(1,0)`,
   and `(1,1)`. Their classes in `E[2]` are `(0,1)`, `(1,0)`, and `(1,1)`.
   Cylinders of `N` are taken relative to these three marked points.
3. Each cylinder of `M` covers a cylinder of `N`. Its stabilizer in `V` acts on
   it by rotations, so the stabilizer is cyclic and has order at most 2. Each
   cylinder of `N` therefore has at least two preimage cylinders.
4. Suppose `N` has exactly one cylinder in direction `(p, q)`. Then `tau`
   preserves it and exchanges its two boundary components. The function
   `L = q x - p y` mod 2 is constant on each boundary component, and `tau`
   sends `L` to `-L`. All marked points lie on the boundary and have integer
   `L`. So all three marked points have the same `L` mod 2.
5. The three values are `p`, `q`, and `q - p` mod 2. For coprime `p`, `q`, they
   are never all equal. So `N` has at least two cylinders.
6. `M` has at least four cylinders, and `DP` has at least two.

**CHECKED BY COMPUTATION.** `cylcount.py cross 12` gives the histogram
`{3: 124, 4: 58}` and no one-cylinder direction.

**Meaning.** Lemma A cannot start on the cross. Other rooms with two mirror
axes can fail the same way. Each one needs its own check of steps 1 and 4.
Those rooms need Lemma A' across several cylinders, or a monodromy statement
on the quotient.

### What stops a general proof

- **Existence.** Theorem B needs one-cylinder directions with `X = Z^2`. No
  theorem gives them for every asymmetric room. This is the open question of
  direction 5, with a concrete use.
- **Symmetric rooms.** Proposition X shows that existence fails for a whole
  class. The replacement lemma is not written.
- **Lattice pairs of different classes.** Theorem B says nothing about pairs
  inside `X`. When a room has many interior lattice points, Target 3 still
  needs those pairs lit. Lemma A helps there only when a lattice point lies on
  a regular integer leaf.
- **Counterexample mechanism.** None found. The heuristic in the Claim 2
  section says a counterexample needs a non-involutive obstruction on a
  sphere double. No such planar structure is known. Label: CONJECTURAL.

## The cleanest true statements

1. **Lemma 1 and Corollary 1 (PROVED).** Torus-level blocking of all candidates
   holds exactly for same-class lattice pairs in rooms where the three other
   classes are corner classes.
2. **Lemma A and Theorem B (PROVED).** One-cylinder directions confine every
   dark endpoint to an explicit lattice `X`.
3. **Theorem Q22 (PROVED, given certificates).** The 22-wall room has exactly
   one dark pair among all real interior pairs.
4. **Theorem A (PROVED).** An irrational point illuminates every rational
   point.
5. **Proposition X (PROVED).** The cross has no one-cylinder direction.
6. **Target 3 in general (CONJECTURAL).**

## Computations

All scripts are exact integer or `Fraction` code. They live in this directory.

| Script | Purpose |
| --- | --- |
| `leafcheck.py` | Traces every billiard leaf through interior `(1/N)`-grid points for directions up to a bound. |
| `deepen.py` | Runs `leafcheck` to bound `B0`, then extends only the unjoined pairs to `B1`. |
| `crosscheck.py` | Compares the tracer with an independent `Fraction` ray-caster. |
| `cylcount.py` | Counts cylinders of `DP` by the strip formula. |
| `onecyl_verify.py` | Certifies a one-cylinder direction by union-find over regular leaves. |
| `exceptional.py` | Computes `X` mod `Z^2` from certified directions. |
| `lemma1_check.py` | Brute-force check of Lemma 1. |

### Rational pairs joined by a legal path

Unjoined pairs are candidates only. A finite direction bound never proves
darkness. Joined pairs are proved lit.

| Room | `N` | Interior points | Pairs | Unjoined pairs |
| --- | --- | --- | --- | --- |
| 22-wall | 2 | 33 | 528 | 1: `(0,0)`, `(2,2)` |
| 22-wall | 3 | 94 | 4,371 | 1: same pair |
| 22-wall | 4 | 185 | 17,020 | 1: same pair |
| 22-wall | 5 | 306 | 46,665 | 1: same pair |
| 22-wall | 6 | 457 | 104,196 | 1: same pair |
| 22-wall | 7 | 638 | 203,203 | 1: same pair |
| 22-wall | 8 | 849 | 359,976 | 1: same pair |
| 22-wall | 9 | 1,090 | 593,505 | 1: same pair |
| 22-wall | 10 | 1,361 | 925,480 | 1: same pair |
| 22-wall | 12 | 1,993 | 1,985,028 | 1: same pair |
| Plus, staircase, cross | 1 to 6 | up to 385 | up to 73,920 | 0 at bound 20 |

The largest direction bound needed for the 22-wall room is `max(p, q) = 77`,
at `N = 12`. No run covers `N = 11`.
Logs: `deepen-q22-large.log`, `textbook-rooms.log`.

These runs agree with Theorem Q22. The theorem does not depend on them.

### Cylinder counts on `DP`

Counts include both signs of `q`, so each direction appears twice.

| Room | Bound | Histogram of `#cyl(DP)` |
| --- | --- | --- |
| 22-wall | 14 | `{1: 16, 3: 98, 5: 100, 6: 40}` |
| Cross | 12 | `{3: 124, 4: 58}` |
| Plus | 10 | `{1: 66, 3: 44, 5: 16}` |
| Staircase | 10 | `{1: 50, 3: 76}` |
| L-shape | 8 | `{1: 26, 2: 60}`; one cylinder exactly when `p` and `q` are odd |

For the L-shape, `X` mod `Z^2` is `{(0,0), (1/2,1/2)}` from direction `(1,1)`.
Lemma A does not decide the cell centres there.

### Limits of the computations

- `cylcount.py` and `onecyl_verify.py` use different counting methods but share
  the tracer `leafcheck.forward`.
- `crosscheck.py` validates the tracer against an independent ray-caster. It
  reports 0 mismatches on 1,500 sampled leaves across three rooms.
- No second person or agent has re-run the certificates.

### Reproduce

Run from this directory.

    python3 lemma1_check.py
    python3 onecyl_verify.py q22 4 7 7 4
    python3 onecyl_verify.py plus 1 1 1 2
    python3 onecyl_verify.py stair5 1 1 2 3
    python3 cylcount.py q22 14
    python3 cylcount.py cross 12
    python3 exceptional.py
    python3 deepen.py q22 6 30 400
    python3 crosscheck.py q22 4 41 400

## Corrections to the directions memo

- Direction 3, candidate lemma: replace it with Corollary 1.
- Direction 3, consequence: clean candidates exist for every non-corner pair
  and for lattice pairs of different classes, not only for generic rational
  pairs.
- Direction 5, second usable fact: it holds for every interior `T`, not only
  for A lifts (Lemma A).
- Direction 5, falsifier: the 22-wall room passes for `max(p, q) <= 14`.
- Progress assessment, first bullet: add "A pairs only; non-A pairs are open
  for `9 <= W <= 21`".

## Most valuable next step

Have a reviewer re-derive Lemma A and re-run
`python3 onecyl_verify.py q22 4 7 7 4`. Acceptance upgrades the 22-wall result
to "exactly one dark pair among all real pairs".

After that, decide the existence question: does every room without two mirror
axes have one-cylinder directions with `X = Z^2`? Each certificate converts one
room into "all dark pairs are lattice points" by Theorem B. For rooms with two
mirror axes, write the quotient version that Proposition X calls for.
