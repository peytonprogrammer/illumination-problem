# D10: one theorem for the darkness mechanisms, and what survives for rooms

Fable subagent, 2026-11-09. Author-proved in one session. No second review.

Status tags: **PROVED** (argument written here), **CHECKED BY COMPUTATION** (with
the bound), **CONJECTURAL**, **OPEN**.

## Summary

- Observations (i) and (iii) are correct. Observation (ii) has the right
  conclusion and an incomplete reason. Section 1 gives the proofs.
- One theorem contains the parity factor and A, G1, G5, G6, G7 (Theorem U,
  section 2). Its "if" direction is proved. The census never contradicts it:
  0 of 12,425 LIT pairs get a certificate, and all 439 DARK pairs get one.
- For normalized rooms, G1, G7, class A, and the cut route are excluded by
  proof. The per-class parity route and the rigid route are neither excluded
  nor realized. No new dark room was found.
- The same-fibre conjecture splits into a lit-side statement (D2) and a purely
  algebraic statement about block systems (D3). D3 needs no decider.
- The weakest point is D3. Section 5 says why.

Files in this directory:

| File | Purpose |
| --- | --- |
| `unified_test.py`, `unified_test.json` | Certificates of Theorem U on the saved census, n <= 10 |
| `check_stretched_staircase.py` | Observation (i) |
| `roomtools.py`, `room_certs.py`, `check_room22.py` | Certificates for one given room |
| `check_saved_rooms.py`, `check_saved_rooms.json` | Certificates on the 1,027 rooms saved by `d8-perturbation-test` |
| `immersed_flag.py` | Splits the d6 involution flag into its two cases |
| `design_two_tilings.py` | One failed design for a second kind of dark room |

No script enumerates rooms or covers. Each one reads saved data or one fixed
polygon.

## 0. Conventions and three local facts

`Q -> B` is a genus-0 pillowcase cover with cycle lengths 1, 2, 3 (pole,
regular point, zero). `sigma` and `tau` are distinct regular points over
corner `a`. A factor is a quotient `phi : Q -> N = Q / Pi` by a block system.

For a simple arc `alpha` from `a` to a corner `x`, `Gamma_alpha(Q)` is the
bipartite graph of lifts of `alpha`. The light component `K_Q(alpha, sigma)` is
the component of `sigma` in the subgraph induced on regular vertices. The pair
is LIT when `tau` lies in `K_Q(alpha, sigma)` for some `x` and some `alpha`.

**Fact L (PROVED).** Let `q` lie over `p = phi(q)` with local degree `e`. Then
`len(q) = e * len(p)`. So:

- `p` regular: `q` is regular and `e = 1`.
- `p` a zero: `q` is a zero and `e = 1`.
- `p` a pole: `q` is a pole, a regular point (`e = 2`), or a zero (`e = 3`).

So `phi` is branched only over poles of `N`.

**Definition.** A point of `N` is **live** when some regular point of `Q` lies
over it. Regular points of `N` are live. Zeros are never live. A pole is live
exactly when it has a preimage with `e = 2`. `K_N(alpha, u)` is the component
of `u` in the subgraph of `Gamma_alpha(N)` induced on live vertices.

**Lemma 1, projection (PROVED).** `phi(K_Q(alpha, sigma))` lies in
`K_N(alpha, phi(sigma))`.

Proof. `phi` maps lifts of `alpha` to lifts of `alpha`, so it is a graph map.
Regular vertices go to live vertices. The image of a connected set is
connected.

**Lemma 2, lifting (PROVED).** Suppose every vertex of `K_Q(alpha, sigma)` maps
to a regular point of `N`. Let `C` be the component of `phi(sigma)` in the
subgraph of `Gamma_alpha(N)` induced on regular vertices.

- If `C` is a path, `phi` is injective on `K_Q(alpha, sigma)`.
- If `C` is a cycle whose lift through `sigma` is a closed curve, `phi` is
  injective on `K_Q(alpha, sigma)`.

Proof. At each vertex `e = 1`, so the two edges at a vertex of `K_Q` go to the
two distinct edges at its image. A locally injective map from a connected
graph of degree at most 2 to a path is injective. In the cycle case, `K_Q`
lies in the lift of `C` through `sigma`, which maps bijectively to `C`.

**Lemma 0, change of base (PROVED).** Let `Q -> P' -> B` with `P'` a
pillowcase. Then `Q -> P'` is branched only over the four corners of `P'`, and
the light rule over `P'` gives the same LIT pairs as the light rule over `B`.

Proof. A point of `P'` over a corner of `B` that is not a corner of `P'` is
regular, so by Fact L every point of `Q` above it is regular with `e = 1`.
Both rules describe the straight segments of `Q` from `sigma` to `tau` that
pass only regular points. They differ only at those extra points, which never
stop a segment.

## 1. Verdicts on the coordinator's observations

### (i) The flagged n = 10 "room": CORRECT

**CHECKED BY COMPUTATION** (`check_stretched_staircase.py`, one polygon).

- The five-square staircase stretched by 2 in `x` has 10 cells, 10 walls, and
  cycle types `a [3,2,2,1^3]`, `b [2^5]`, `c [2^5]`, `d [3,3,1^4]`. These equal
  the flagged class.
- Its vertex x-coordinates are 0, 2, 4, 6. Its corners occupy two parity
  classes. So the lattice is not normalized.
- The marks `(2,0)` and `(6,2)` are smooth wall points. The decider says DARK
  (24 states). The only certificate is G1 over a pillowcase of degree 2.
- In its own unit lattice the same polygon is the staircase with marks `(1,0)`
  and `(3,2)`, and it has one ordinary parity factor.

So the flagged case is the known base in a doubled lattice, with both marks on
walls. It is not a new room.

### (ii) G1 and normalized rooms: conclusion CORRECT, stated reason INCOMPLETE

The stated reason is "G1 needs every point of `Q` over two corners to be
regular". That holds only when `deg(P' -> B)` is even.

- Write `P' = R^2 / <2 Lambda', -1>` with `Lambda'` a sublattice of `Z^2` of
  index `m`. The corners of `P'` map onto the image of `Lambda'` in
  `Z^2 / 2 Z^2`.
- If `m` is even, that image has at most two classes. Two corners of `B` then
  carry only regular points. This is the coordinator's statement.
- If `m` is odd, the image is all four classes, and the statement fails. The
  census has only `m = 2`. A G1 example with `m = 3` needs `n >= 12`, so the
  census can't show one. No such example is verified here.

The conclusion needs no parity count:

**Proposition R1 (PROVED).** Let `P` be a normalized orthogonal lattice room.
The only pillowcase factor of `DP` is `B`.

Proof. Let `DP -> P' -> B` with `P'` a pillowcase. The front face of `P` is
simply connected, so its map to `P' = R^2 / <2 Lambda', -1>` lifts to a map
`D` into the plane. `D` commutes with the projections to `B`, so
`D(p) = +-p + 2v`. Take `D` to be the identity. A vertex of `P` is a pole or a
zero of `DP`. By Fact L its image in `P'` is a pole, so it lies in a coset of
`Lambda'`. Edge vectors of `P` are differences of vertices, so `Lambda'`
contains `(h, 0)` and `(0, w)` for every horizontal edge length `h` and
vertical edge length `w`. Normalization gives gcd 1 in each direction. So
`Lambda' = Z^2` and `P' = B`.

Consequences for normalized rooms:

- G1 and G7 never occur. No certificate relative to an intermediate pillowcase
  exists.
- Every factor `N != B` of `DP` has a zero, because a factor without zeros is
  a pillowcase.
- The proof uses a simply connected face and normalization only. It also holds
  for immersed rooms.

### (iii) Class A and interior marks: conclusion CORRECT, one detail corrected

Class A needs a class `y` whose points are all convex corners.

**Proposition R2 (PROVED).** Let `P` be a lattice room with an interior point
`S` of class `a`. If every lattice point of some class `y != a` is a convex
corner, then `P` is the 2 x 2 block around `S`.

Proof. Let `K_S` be the four cells around `S`.

- `y` adjacent to `a`: two mid-side points of `K_S` have class `y`. Each lies
  in two cells of `K_S`, so it isn't convex. Contradiction.
- `y` diagonal to `a`: the four corners of `K_S` have class `y`. A convex
  corner belongs to one cell, so both edges of that cell at the corner are
  walls. Each cell of `K_S` then has walls on its two outer edges, so
  `P = K_S`.

The 2 x 2 block has one interior point, so it has no interior pair.

Correction: the mid-side points of `K_S` can be flat, reflex, or interior. The
coordinator's note listed only flat and interior. The conclusion is unchanged.

## 2. The unified statement

### 2.1 Theorem U

Fix a pillowcase factor `P'` of `Q`, with `P' = B` allowed, such that `sigma`
and `tau` lie over corners `c_s` and `c_t` of `P'`. All notions below are taken
relative to `P'` (Lemma 0). The **targets** are the three corners other than
`c_s` when `c_s = c_t`, and the single corner `c_t` when `c_s != c_t`.

A factor `N` with `Q -> N -> P'` is a **certificate at the target `x`** when
one of the following holds.

- **Par(x).** `c_s = c_t`, `phi(sigma) != phi(tau)`, and `N` has no regular
  point over `x`.
- **Rig(x).** `N -> P'` has identity monodromy at a corner `y` outside
  `{c_s, x}`. `phi(tau)` lies outside `K_N(alpha, phi(sigma))` for one arc
  `alpha` from `c_s` to `x`.
- **Cut(x).** `c_s = c_t` and `phi(sigma) = phi(tau)`. Every regular point of
  `Q` over `c_s` and over `x` maps to a regular point of `N`. The monodromy of
  `N` at a corner outside `{c_s, x}` is a single cycle.

**Theorem U (PROVED).** If some pillowcase factor `P'` has a certificate at
every target, the pair is DARK.

Every hypothesis is a finite check in one basis.

### 2.2 Proof

A light path projects to `P'` as a straight path from `c_s`. It runs back and
forth along one saddle connection from `c_s` to a corner `x`, and it meets only
the fibres over `c_s` and `x`. So `x` is a target, and it suffices to show that
`tau` is outside `K_Q(alpha, sigma)` for every arc `alpha` from `c_s` to `x`.

Par. A live vertex of `Gamma_alpha(N)` over `x` is a pole, because `N` has no
regular point over `x`. A pole is a leaf. So `phi(sigma)` is the only vertex
of `K_N(alpha, phi(sigma))` over `c_s`. Lemma 1 finishes.

Rig. `N -> P'` is unbranched over `y`, so `N` covers the sphere minus the
other three corners. All simple arcs from `c_s` to `x` are isotopic there, and
the isotopy lifts with fixed end points. So `Gamma_alpha(N)`, with its
vertices labelled by points of `N`, is the same for every `alpha`. Liveness
depends only on the point. So one arc decides all arcs, and Lemma 1 finishes.

Cut. Let `C` be as in Lemma 2. The hypothesis on regular points gives the
assumption of Lemma 2. If `C` is a path, Lemma 2 finishes. Let `C` be a cycle.

- `C` is a simple closed curve in the sphere `N`, and it is a whole component
  of `Gamma_alpha(N)`.
- Let `beta` be the arc between the other two corners that is disjoint from
  `alpha`, and `T` its preimage in `N`. One corner has a single point of `N`
  above it, so `T` is connected. `T` is disjoint from `C`.
- `N` minus both graphs is a union of open annuli. Each annulus has one end on
  `Gamma_alpha(N)` and the other on `T`.
- A pole of `N` over `c_s` or `x` lies in a component of `Gamma_alpha(N)`
  other than `C`. An adjacent annulus joins it to `T` without meeting `C`.
  Poles over the other two corners lie on `T`.
- So one of the two discs bounded by `C` contains no pole. By Fact L, `phi` is
  unbranched over that closed disc. The lift of `C` through `sigma` is closed.

Lemma 2 gives injectivity, and `tau != sigma` has the same image as `sigma`.

Remark. Cut forces `deg(N -> P') <= 3`.

### 2.3 The known mechanisms as special cases

| Mechanism | Base `P'` | Certificates |
| --- | --- | --- |
| Separating parity factor | `B` | Par at `b`, `c`, `d` with one `N` |
| G1 | proper pillowcase, `c_s = c_t` | Par at all three targets with one `N` |
| G5 | `B` | Par or Cut at each corner, `N` may change |
| G6 | `B` | `N` with identity at `y`: Par(y), Rig at the other two corners |
| A | `B` | G6 with `N = Q` |
| G7 | proper pillowcase, `c_s != c_t` | Rig at `c_t` with `N = Q` |

Three corrections to the d6 README come out of the proofs:

- **G6 edge rule.** `rigid_factor.py` adds an edge of `N` only when some sheet
  of `Q` joins two regular points in the given basis. That rule depends on the
  basis, so the README proof doesn't cover it. Theorem U uses live vertices.
  On the census the two rules give the same verdict for every pair, corner,
  and factor (0 differences).
- **G6 union.** G6 asks for separation in the union of two graphs. Separation
  per corner is enough.
- **G7.** The hypothesis "sigma and tau are the only regular points over
  `P'`-corners" is not needed. The README's G7 hypotheses alone don't prove
  DARK. The check of one graph is part of the certificate. The script performs
  it for the three G7 pairs.

### 2.4 The "only if" direction

**Conjecture U\* (CONJECTURAL).** If a pair is DARK, some pillowcase factor
`P'` has a certificate at every target.

**CHECKED BY COMPUTATION** for every orbit pair of the saved census, degrees 4
to 10 (`unified_test.py`):

| n | LIT pairs | LIT with a full certificate | DARK pairs | DARK with a full certificate |
| --- | --- | --- | --- | --- |
| 4 | 9 | 0 | 3 | 3 |
| 5 | 22 | 0 | 1 | 1 |
| 6 | 210 | 0 | 6 | 6 |
| 7 | 345 | 0 | 12 | 12 |
| 8 | 1,522 | 0 | 84 | 84 |
| 9 | 2,766 | 0 | 175 | 175 |
| 10 | 7,551 | 0 | 158 | 158 |
| Total | 12,425 | 0 | 439 | 439 |

- The test is not vacuous. At `n = 10`, 948 LIT pairs have certificates at two
  of the three corners.
- Every certificate kind is needed. Without Rig, 51 DARK pairs lose their
  certificate. Without Cut, 54 do. Without a proper `P'`, 12 do.
- For 3 pairs at `n = 9`, Par holds at every corner and no single factor gives
  it at all three. The factor must change with the corner.

Limits. The script implements Par relative to a proper `P'` when
`c_s = c_t`, and Rig relative to a proper `P'` when `c_s != c_t`. It doesn't
implement mixed towers. None was needed. U\* is weaker evidence than it looks:
with `N = Q` and all arcs, the general principle behind Theorem U is a
tautology. The content of U\* is that three finite shapes suffice. Expect new
shapes at larger degree.

## 3. Rooms

`P` is a strictly simple, normalized orthogonal lattice room. `S != T` are
interior lattice points of class `a`. Each has two lifts in `DP`. The pair is
dark when all four lift pairs are dark.

### 3.1 Dictionary

- Sheets are cells. `g_x` rotates by `pi` about the class-`x` points. Its
  cycles are the stars of those points: one cell (convex), two cells (smooth),
  three cells (reflex), or two pairs of opposite cells (interior).
- `kappa_E` crosses the edge of type `E`, and fixes a cell with a wall there.
  Each `g_x` is a product of two `kappa`. A block system is invariant under
  the reflection `iota` of `DP` exactly when every `kappa_E` preserves it.
- An `iota`-invariant factor `N` carries a reflection. `N / iota` is a flat
  disc `K`, and `P -> K` is a fold. `K` need not be embedded, and it can have
  interior cone points.
- By Proposition R1 the base is always `B`. The targets are the classes `b`,
  `c`, `d`.

### 3.2 Canonical certificates

Let `B_x` be the finest block system that merges every 2-cycle of `g_x`. Let
`R_y` be the finest block system that merges every cycle of `g_y`.

**Proposition R3 (PROVED).**

1. `DP / B_x` has no regular point over `x`. Par(x) holds for some factor
   exactly when `B_x` separates the lift pair.
2. `DP / R_y` has identity monodromy at `y`. Rig(x) holds for some factor with
   identity at `y` exactly when it holds for `DP / R_y`.
3. `B_x` and `R_y` are `iota`-invariant. So `DP / B_x` and `DP / R_y` are
   doubles of fold targets of `P`.

Proof.

1. A block of `B_x` that contains a fixed cell or a 2-cycle of `g_x` is fixed.
   Any other block holds only cells of 3-cycles, so its induced cycle has
   length 1 or 3. A factor without regular points over `x` must merge each
   2-cycle of `g_x`, so it is coarser than `B_x`. A coarser factor separates
   less.
2. A factor with identity at `y` is coarser than `R_y`. Apply Lemma 1 to
   `DP / R_y -> N`: separation in `N` gives separation in `DP / R_y`.
3. The two `kappa` whose edges meet at a class-`x` point permute the cells of
   each star, and they map 2-cycles of `g_x` to 2-cycles. So they preserve the
   generating pairs. The other two `kappa` differ from these by elements of
   `G`.

So a room has six partitions to compute by union-find: `B_b`, `B_c`, `B_d`,
`R_b`, `R_c`, `R_d`. Each ordered pair `(x, y)` then gives one Rig check, six
in total. `room_certs.py` computes them for one room.

### 3.3 The cut route never yields a dark room

**Proposition R4 (PROVED).** Suppose Cut(x) holds for a lift pair of `(S, T)`
and class `x` has a transparent point. Then `x` is the class diagonal to `a`,
`P` is the 12-wall cross, and the pair is LIT.

Proof.

1. `deg N <= 3`. Degree 1 has no regular point. Degree 2 is a pillowcase,
   which R1 excludes. So `N` is the tromino double: types `[3]`, `[1^3]`,
   `[2,1]`, `[2,1]`. `a` has type `[2,1]`. The cycle sits at `y`. If `x` had
   type `[1^3]`, class `x` would have no transparent point. So `x` has type
   `[2,1]`.
2. The partition `Pi` of `N` is `iota`-invariant. Suppose not, and let `Pi'`
   be its image. Both quotients are the same cover of `B`. `G` acts on
   `Pi x Pi'`, and the pairs that intersect form one orbit of size 3, 6, or 9.
   Size 3 means `Pi = Pi'`. Size 9 gives a connected cover of degree 9 with
   branching index 14, which has genus -1. Size 6 makes the regular
   `S_3`-cover `M` a factor of `DP`. One of the three `a`-points of `M` maps
   to the pole of `N` with `e = 2`. By Fact L every point of `DP` above it is
   regular. That contradicts the Cut hypothesis.
3. The tromino double has trivial deck group, so its reflection is unique.
   `P` folds onto the planar tromino `K`. The flat points of `K` have classes
   `a` and `x`, and they are adjacent mid-sides. So `x` is diagonal to `a`.
4. Each copy of `K` in `P` is a whole copy. Neighbouring copies are mirror
   images in a side line of `K`. `P` is embedded, so `K` must lie on one side
   of that line. `K` has four such lines. Mirrors in the two short ones create
   a smooth point of class `a` or `x` over a pole, which the Cut hypothesis
   forbids. Mirrors in the two long ones meet at one corner of `K`.
5. So `P` is a union of at most four copies around that corner. Only the union
   of all four has two interior points of class `a`. It is the 12-wall cross,
   and the segment between the two points is a legal path.

**CHECKED BY COMPUTATION** (`room_certs.py`): the 12-wall cross with
`S = (1,2)`, `T = (3,2)` has Cut in one class, Par in a second, no certificate
in the third, and the decider says LIT. This matches the counterexample to
Claim 1 in the d3 audit.

Step 4 uses embeddedness. The other steps don't.

### 3.4 The rigid route: planar targets excluded, general case open

**Lemma F (PROVED).** Let `P -> K` be a fold onto an embedded lattice polygon.
If an interior point of `P` maps to a convex corner `v` of `K`, then `K` lies
in the quadrant at `v` spanned by its two edges.

Proof. The four copies of `K` around the point are mirror images in the edge
lines at `v`. If `K` had cells on both sides of one line, two adjacent cells of
`K` across that line would give a cell in two copies. `P` is embedded.

**Proposition R5 (PROVED).** If `P / R_y` is an embedded lattice polygon, Rig
with identity at `y` holds for no interior pair.

Proof. Every class-`y` point of `K = P / R_y` is a convex corner. Each cell has
one `y`-corner, and both edges there are walls. So all cells of `K` share
their opposite corner, and `K` is a cell, a domino, an L-tromino, or a 2 x 2
block. The cell gives `N = B`. The domino and the block give pillowcases,
excluded by R1. For the tromino, the class-`a` points of `K` are one flat point
and one convex corner that fails Lemma F. So both `S` and `T` map to the flat
point, and Rig can't separate them.

**OPEN.** `P / R_y` can be a disc that is not embedded or has interior cone
points. Nothing here excludes Rig in that case. Bookkeeping for such an `N`
with `d` sheets and `R` regular points: `z_N = d - 1 - R/2`, and
`r >= delta * z_N` with `delta >= 2` by R2.

Evidence. `R_b`, `R_c`, `R_d` are the one-block system for the 22-wall room.
No Rig certificate occurs for any class of any pair in the 1,027 saved d8
rooms.

### 3.5 The per-class parity route: open

Per-class blocking is sound for rooms. A direction of class `x` meets only
points of classes `a` and `x`. So the provable criterion is:

    B_b, B_c, and B_d each separate every lift pair   =>   DARK.

`N_min = DP / (B_b v B_c v B_d)` separates less than each `B_x`. A room where
each `B_x` separates and the join doesn't would be dark without a separating
parity factor. Call that a **second kind** of dark room.

**Proposition R6 (PROVED).** In a room with two interior points, two distinct
classes can't have different congruences `B_x` that both have block size 2.

Proof. A block system of block size 2 is the orbit partition of a deck
involution `j`. `B_x` is `iota`-invariant, so `j` commutes with `iota` and
comes from a symmetry of `P`: the rotation by `pi` about a lattice point, or a
mirror in a lattice line followed by `iota`. Two different ones make `P`
symmetric under both mirrors, with centre `O`. Every transparent point of
class `x_i` is a fixed point of `j_i`. The fixed points are `O` for the
rotation and the two boundary points of the axis for a mirror. The points `O`,
`O +- (1,0)`, `O +- (0,1)` are regular and have three different classes. A case
check on which of these classes are `x_1` and `x_2` leaves two outcomes: all
eight outer edges of the block around `O` are walls, or one `B_{x_i}` has no
generating pair. Both contradict the hypotheses.

**Corollary (PROVED).** A second kind of dark room by the parity route has two
classes with transparent points and different `B_x`. One of them has
`delta >= 3` and at least 3 blocks. So `n >= 9` and `r >= 3`.

These bounds are weak. The d2 audit reached `r >= 9` for one parity factor
because that factor needs `z_N >= 2`. A per-class target can have `z_N = 1`
(the tromino double), so counting alone gives no more. The record's theorem
for `W <= 21`, `k <= 6` adds `k >= 7` below 22 walls. That theorem is not
re-verified here.

Designs that fail (PROVED, by the arguments above or by `design_two_tilings.py`):

- Both factors from symmetries of `P` (R6).
- A tromino target with `a` of type `[2,1]`: interior `a`-points share one
  image (Lemma F).
- A chain of four copies `m2 L - L - m1 L - m1 m2 L` glued along three waists.
  The fold for one class forces the fold for the other, and `B_d` equals the
  full partition onto `L`.
- A room that is a union of whole mirror copies of the S-tetromino in both
  orientations. No cell survives the closure for any of the six offsets.

### 3.6 Computed evidence on saved rooms

**CHECKED BY COMPUTATION** (`check_saved_rooms.py`, the 1,027 rooms and 1,464
same-class interior pairs saved by d8, with d8's traced verdicts):

| Pairs | Count | Classes certified |
| --- | --- | --- |
| DARK | 3 | 3 of 3 for all (Par, Par, Par) |
| LIT | 1,112 | 0 of 3 |
| LIT | 303 | 1 of 3 |
| LIT | 46 | 2 of 3 |
| LIT | 0 | 3 of 3 |

- `B_min` separates exactly the 3 DARK pairs. This agrees with d8 on every
  pair.
- No pair has `B_b`, `B_c`, `B_d` all separating while `B_min` doesn't.
- Every class certificate found is Par. Rig and Cut never occur.

The sample comes from two base rooms, so it is narrow.

### 3.7 Which planar hypothesis does the work

**CHECKED BY COMPUTATION** (`immersed_flag.py`, saved counterexample orbits,
n <= 10). Of 44 lifts of the seam reflection, 41 have a pole or zero off the
fixed circle, and 3 are the planar G1 polygon. None is an immersed disc with
all corners on its boundary. 28 orbit tuples have no lift.

So at `n <= 10` no extra mechanism lives on an immersed room either. The
obstruction there is "every pole and zero lies on one real circle", not
embeddedness. This corrects a possible reading of the d6 flag, which reports
"interior cone point or overlap" as one status.

### 3.8 Mechanisms for rooms

| Mechanism | Occurs for normalized rooms with an interior pair? | Status | Bound if it occurs |
| --- | --- | --- | --- |
| Separating parity factor | Yes (22-wall room) | Known | `r >= 9` (d2 audit) |
| G1, G7, any relative certificate | No | PROVED (R1) | |
| A | No | PROVED (R2) | |
| Cut (G5 cut route) | Only as a partial certificate; the one room is LIT | PROVED (R4) | |
| Rig (G6) with planar target | No | PROVED (R5) | |
| Rig (G6) in general | Unknown | OPEN | `r >= 2 z_N`, `z_N = d - 1 - R/2` |
| Par with different factors (G5 parity route) | Unknown | OPEN | `n >= 9`, `r >= 3`; `k >= 7` if `W <= 21` |

No non-parity mechanism was realized by a room. No new dark room is claimed.

## 4. Dark structure conjecture for rooms

Hypotheses: `P` is a strictly simple orthogonal lattice room in normalized
position. `S != T` are interior lattice points of one class, called `a`.

Say class `x` is **certified** when each of the four lift pairs has `B_x`
separating, or Rig(x) holding for `DP / R_y` with some `y` outside `{a, x}`.

- **D1 (PROVED).** If `b`, `c`, and `d` are certified, the pair is dark.
  This is Theorem U with R1, R3, and R4.
- **D2 (CONJECTURAL).** If the pair is dark, then `b`, `c`, and `d` are
  certified. This is the room form of U\*. It is a lit-side statement: an
  uncertified class has a legal path in a direction of that class.
- **D3 (CONJECTURAL).** If `b`, `c`, and `d` are certified, then `B_min`
  separates all four lift pairs.

**Proposition (PROVED).** The same-fibre conjecture ("dark exactly when
`N_min` separates") is equivalent to D2 and D3 together.

Proof. D1, D2, D3 give the conjecture, because `B_min` separating gives Par in
every class. Conversely, the conjecture gives D3 through D1, and D2 through
the last remark.

Evidence:

| Statement | CHECKED BY COMPUTATION |
| --- | --- |
| D1 | Proved. 0 of 1,461 LIT pairs on the d8 rooms are certified. |
| D2 | 3 of 3 DARK pairs on the d8 rooms. Abstract form: 439 of 439 at n <= 10. |
| D3 | 3 of 3 certified pairs on the d8 rooms. False for abstract covers (126 orbit pairs, n <= 10). |
| | Those 126 pairs have a certificate at `b`, `c`, `d` over `B` and no parity factor. |

Why the split matters:

- D3 uses no light and no decider. It needs six union-find runs per room and
  class origin, plus one graph search per Rig check. A room census can test it
  alongside its own work.
- A failure of D3 is a room that is dark by proof (D1) and has no separating
  parity factor. It would refute the same-fibre conjecture and be a second
  kind of dark room.
- The d9 census decides pairs by shooting. A second kind of room with
  `W <= 22` would appear there as a dark survivor that `B_min` doesn't
  separate. d9 was still pending when this was written, so it isn't cited.

Proof strategy:

1. Prove D3 first. By R3, each `B_x` and `R_y` is a fold of `P`. The abstract
   counterexamples all have a pole or zero off the real circle (section 3.7).
   So the hypothesis to use is that every corner of the fold target lies on
   its boundary.
2. First lemma to attempt (interlock lemma, CONJECTURAL): let `x != x'` be
   classes with transparent points, and suppose `B_x` separates an interior
   pair. Then every transparent point of class `x'` is folded by `B_x`, so
   `B_x'` refines `B_x`. With the symmetric statement this gives
   `B_x = B_x'` and D3 for the parity route. The 22-wall room and the chain
   design in section 3.5 both behave this way: a transparent `x'`-point sits
   opposite a wall corner in the mirror copy, which forces the fold.
3. Then treat Rig: show `R_y` is the one-block system whenever `P` has an
   interior point and is not the cross. R5 covers embedded targets.
4. D2 is the dynamical half. The one-cylinder method of the d3 audit (Lemma A
   and Theorem B) is the available tool. Apply it per class: a class that
   isn't certified should have a one-cylinder direction of that class.

## 5. Weakest point

D3 is undecided, and the evidence for it is thin.

- The proved exclusions cover G1, G7, A, Cut, and Rig with an embedded target.
  They don't cover two different fold factors for two classes, or Rig with a
  target that overlaps or has interior cone points.
- The bounds for those two cases are `n >= 9`, `r >= 3`. They don't reach the
  22-wall threshold. A room of the second kind below 22 walls is excluded only
  by the record's `W <= 21`, `k <= 6` theorem, and only when `k <= 6`.
- The computed support is 1,464 pairs from perturbations of two rooms, with 3
  dark pairs. The abstract analogue of D3 is false.
- The interlock lemma is a guess from two examples.

Other caveats:

- All proofs here are from one session and have no second reader. R4 step 2
  and the case check in R6 are the least routine.
- Theorem U assumes cycle lengths at most 3 (Fact L) and genus 0 (Cut).
- U\* is tested through degree 10 only, and the relative certificates are
  implemented for the two shapes the census needs.
- `check_saved_rooms.py` trusts d8's verdicts and witnesses. It doesn't rerun
  the decider.

Cheapest decisive experiment: add the D3 test to a room census. For each room
and each same-class interior pair, compute `B_b`, `B_c`, `B_d`, the six Rig
checks, and `B_min`, and flag certified pairs that `B_min` doesn't separate.
`room_certs.room_report` does this for one room. A census is a room search, so
it needs Daniel's approval.
