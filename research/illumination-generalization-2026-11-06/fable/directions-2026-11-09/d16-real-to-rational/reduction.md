# Reduction from real pairs to rational pairs in square-lattice rooms

Date: 2026-11-10. Direction d16. Status tags used in this document:

- **[PROVED HERE]**: a complete proof is in this document. Nobody has reviewed it.
- **[CITED, READ]**: published, and I read the statement and proof in the source.
- **[CITED, SUBAGENT]**: published; a literature subagent read it from the arXiv
  source. I didn't re-read it.
- **[COMPUTED]**: output of the scripts in this directory.
- **[OPEN]**: not proved and not refuted.

## 1. Results

1. **The reduction theorem holds. [PROVED HERE]** Let `P` be a strictly simple
   orthogonal lattice room. If every pair of distinct rational interior points
   is lit, then every pair of distinct interior points is lit. The proof is
   elementary. It doesn't use Ratner, Eskin–Mirzakhani–Mohammadi, or any
   cited orbit-closure theorem. See Theorem 1 and Corollary 1 in Section 6.
2. **Shape of an irrational dark pair. [PROVED HERE]** If `(S, T)` is dark and
   `S` has an irrational coordinate, then after exchanging the axes
   `S = (x, y)` and `T = (rho x + c, v)` with `y`, `v`, `c` rational, `rho`
   rational and nonzero, and `x` irrational. The pair lies on a one-parameter
   family of dark pairs. The family slides both points along horizontal lines
   and contains rational dark pairs arbitrarily close to `(S, T)`.
3. **Remaining gap. [OPEN]** I can't exclude these one-parameter families
   ("half-rational families") for a general orthogonal room. The only published
   claim that excludes them is Wolecki's Theorem 1.2(i). I read its proof.
   Lemma 2.9 of that paper has a gap in exactly this case. See Section 6.4.
   The gap doesn't affect result 1.
4. **Rooms with a 45-degree wall. [PROVED HERE]** If a lattice room has both an
   axis-parallel wall and a diagonal wall, every dark pair of interior points
   is a pair of rational points. See Section 7.
5. **The 11 open rooms. [COMPUTED, on top of results proved here]** In each of
   the 11 rooms that d13 left open, every pair of distinct interior points is
   lit. This includes the Proposition O' room and the `W = 20` area-12 room.
   The result depends on the correctness of `dpcover.c`, which I checked by
   sampling, not by proof. See Section 8.
6. **Correction to the multi-twist argument of the brief.** The twists don't act on room
   pairs. They act on pairs of points of the doubled room `DP`. A room-level
   Theorem C certificate isn't valid after a twist. Section 8 uses a
   class-aware certificate on `DP` instead.

The single weakest step is the correctness of `dpcover.c` (Section 9).

## 2. Setting and notation

`P` is a strictly simple orthogonal polygon that is a union of unit lattice
cells. `V` is its vertex set. A trajectory stops at a vertex. It reflects at a
flat boundary lattice point and passes through an interior lattice point.

- `K = {±1}^2` is the Klein group. `M` is the four-copy unfolding. A point of
  `M` is `(S, e)` with `S` in `P` and `e` in `K`. Sheets `(e1, e2)` and
  `(-e1, e2)` are glued along vertical walls. Sheets `(e1, e2)` and
  `(e1, -e2)` are glued along horizontal walls.
- The chart of sheet `e` is `(e1 x, e2 y)`. These charts make `M` a translation
  surface tiled by unit squares.
- `pi : M -> T = R^2/Z^2`, `pi(S, e) = (e1 x, e2 y) mod Z^2`. It's a covering
  branched over `0` only. `L = pi^-1(0)` is the set of lifts of lattice points.
- `VM` is the set of lifts of vertices. A convex corner has one lift. It's a
  regular point of the flat metric. A reflex corner has one lift, with cone
  angle `6 pi`. Both kinds block trajectories.
- A point of `M` or `P` is *rational* when both coordinates are rational, and
  *irrational* otherwise.
- `tau = (-1, -1)` in `K`. Its fixed points are exactly the points of `VM`.
  `DP = M/tau` is the doubled room. `S+` is the image of `(S, (1, 1))` and
  `S-` is the image of `(S, (1, -1))`. `S+ = S-` exactly when `S` is on a wall.
- For distinct `s`, `t` in `M \ VM`, the pair `(s, t)` is *M-lit* when a
  geodesic segment from `s` to `t` avoids `VM`. *DP-lit* is defined the same
  way on `DP`, avoiding the images of the corners.

**Unfolding lemma. [CITED, READ: Wolecki, arXiv:1905.09358v3, Lemma 2.1,
stated there without proof as standard]** Let `S != T` be points of `P \ V`,
`s = (S, (1, 1))`, and `t_e = (T, e)`. Then `(S, T)` is lit if and only if
`(s, t_e)` is M-lit for some `e` in `K`.

Because `tau` is free off `VM`, segments that avoid the corners lift from `DP`
to `M`. So:

- class **par**: `(S+, T+)` is DP-lit iff `(s, t_e)` is M-lit for `e = (1, 1)`
  or `(-1, -1)`;
- class **cross**: `(S+, T-)` is DP-lit iff `(s, t_e)` is M-lit for
  `e = (1, -1)` or `(-1, 1)`;
- `(S, T)` is lit iff class par or class cross is DP-lit.

## 3. Openness of illumination (task 1)

**Proposition 1. [PROVED HERE]** The set of M-lit pairs is open in
`(M \ VM)^2` minus the diagonal.

*Proof.* Let `gamma : [0, l] -> M` be a segment from `s` to `t` that avoids
`VM`. `gamma` is compact, so its distance `d` to `VM` is positive. Take
`eps < d/2`. The map `Phi(u, w) = exp_{gamma(u)}(w n)`, with `n` the unit normal,
is defined on the rectangle `[-eps, l + eps] x [-eps, eps]`. It's a local
isometry into `M \ VM`, because no geodesic shorter than `d` from `gamma`
reaches a cone point or a corner lift. The rectangle is convex. For `p` near
`(0, 0)` and `q` near `(l, 0)`, `Phi` maps the segment `pq` to a geodesic
segment that avoids `VM`. `Phi` is a local homeomorphism at `(0, 0)` and at
`(l, 0)`, so these endpoints fill neighbourhoods of `s` and `t`. ∎

Lifts of interior lattice points and of flat wall points are regular points of
`M` outside `VM`. So the proof covers paths through them with no extra case.

**Corollary 1a. [PROVED HERE]** The set of dark pairs is relatively closed in
`(P \ V)^2` minus the diagonal. The same holds on `DP`.

*Proof.* If `(S, T)` is lit, some lift pair `(s, t_e)` is M-lit. The lifts
depend continuously on `(S, T)`. Apply Proposition 1. ∎

Behaviour at the edges of this set:

- **Diagonal, off the vertices.** A point `S0` of `P \ V` has a convex
  neighbourhood in `P` (a disc or a half-disc). Two distinct points of it see
  each other. So dark pairs don't accumulate at `(S0, S0)`.
- **Convex corner.** Near a convex corner `c`, `P` is a quarter-disc. Two
  distinct points of it, other than `c`, see each other. So dark pairs don't
  accumulate at `(c, c)`.
- **Reflex corner.** Near a reflex corner `c`, `P` is a three-quarter disc.
  Two points in opposite quadrants don't see each other directly. Local
  arguments don't control accumulation of dark pairs at `(c, c)`.
- **A vertex and another point.** Nothing local controls accumulation at
  `(c, T)` with `c` a vertex.
- **Walls.** A limit of dark pairs in `(P \ V)^2`, off the diagonal, is dark,
  even when a limit point is on a wall.

The reduction in Section 6 never takes a limit of room pairs. So the
uncontrolled cases don't enter its proof.

## 4. Invariance under twists (task 2)

For each row of the room of length `n`, the two matching rows of `M` form
horizontal cylinders of circumference `2n` and height `1`. Let
`Lh = lcm of 2n over the rows` and `Lv = lcm of 2n over the columns`.

- `h` is the affine homeomorphism of `M` with derivative `[[1, Lh], [0, 1]]`
  that fixes `L` pointwise. On a row strip it's `(x, eta) -> (x + Lh eta, eta)`
  in the chart of the sheet.
- `v` has derivative `[[1, 0], [Lv, 1]]` and fixes `L` pointwise.
- `G = <h, v>`. On the torus, `pi h = A_h pi` and `pi v = A_v pi` with
  `A_h (x, y) = (x + Lh y, y)` and `A_v (x, y) = (x, y + Lv x)`.

**Proposition 2. [PROVED HERE]**

1. Each `g` in `G` maps `VM` to itself pointwise and maps segments to
   segments. So M-illumination is `G`-invariant.
2. `h` and `v` commute with `tau`. So `G` acts on `DP`, and DP-illumination
   is `G`-invariant.
3. For each of the two reflections `k = (-1, 1)` and `k = (1, -1)` in `K`,
   `k h k^-1 = h^-1` and `k v k^-1 = v^-1`.
4. `G` doesn't act on room pairs. The four lift pairs of one room pair map to
   lift pairs of up to four different room pairs.

*Proof.* 1 is immediate. For 2 and 3: `k h k^-1` is affine, fixes `L`
pointwise, and has derivative `D_k [[1, Lh], [0, 1]] D_k`. Two affine
homeomorphisms with the same derivative that agree on `L` differ by a
translation automorphism with a regular fixed point (a convex corner lift).
That automorphism is the identity. For `tau`, `D_k = -I` and the derivative
is unchanged. For a reflection, the off-diagonal entry changes sign.

For 4: the lift pairs of `(S, T)` are `(s, k_e t)` with `t = (T, (1, 1))`.
Then `g (k_e t) = k_e (k_e^-1 g k_e) t`. For a reflection `k_e`, the room
point under `g k_e t` is the room point under `g' t`, where `g'` is `g` with
every exponent inverted. In general it differs from the room point under
`g t`. ∎

**Consequence.** After a twist, "class par is lit" and "class cross is lit"
refer to two different room pairs. You must track the class. The M-level and
DP-level dark sets are the invariant objects. A room pair is dark iff both of
its DP classes are dark.

A general affine automorphism of `M` permutes `L`. It can move a convex corner
lift to the lift of an interior lattice point, because both are regular
points. Such an automorphism doesn't preserve illumination. This document
only uses automorphisms that fix `L` pointwise.

## 5. Orbit closures (task 3)

### 5.1 Published results

| Source | Statement | Use here | Status |
| --- | --- | --- | --- |
| Lelièvre, Monteil, Weiss, arXiv:1407.2975, Thm 2 | For any translation surface `M` and any `x`, the set of points not illuminated by `x` is finite. The non-illuminating pairs form a finite set plus finitely many translation surfaces embedded in `M x M`, with both projections finite covers. | Shows that two-dimensional dark families in `M x M` are the expected exceptional objects. Not used in proofs. | [CITED, SUBAGENT]. Rests on Eskin–Mirzakhani–Mohammadi. |
| Same paper, Thm 1 | `M` is a torus cover iff every pair of points is finitely blocked. | Context. | [CITED, SUBAGENT] |
| Same paper, Section 6, Example 1 | A square-tiled surface with a two-dimensional family of dark pairs `{(-a x, b x)}`. | Shows that Lemma F families can be dark on `M`. | [CITED, SUBAGENT] |
| Wolecki, arXiv:1905.09358v3, Thm 1.2(i) | For a rational polygon, only finitely many pairs of points don't illuminate each other. No torus-cover exclusion. | Would exclude half-rational families. | [CITED, READ]. The proof of Lemma 2.9 has a gap for orthogonal polygons; see Section 6.4. |
| Wolecki, Prop 2.7 (from LMW Thms 2 and 11) | The blocking sets `M_k` are finite unions of points, sets `F x M`, `M x F`, and affinely embedded translation surfaces `a x + b y = u`, `a, b` real. | Same structure as Lemma F. | [CITED, READ] for the statement |
| Hubert, Schmoll, Troubetzkoy, arXiv:math/0602394, Thms 1, 2, 3, 5 and Section 8 | Veech surfaces: finitely many non-illuminable pairs per point; `Aff` orbit closures in `X^n` are real-linear; arithmetic surfaces have infinitely many invariant subspaces lifted from `T^4`. | Context. Thm 5 is the published form of Lemma F, stated without detail. | [CITED, SUBAGENT] |
| Eskin, Marklof, Morris, arXiv:math/0408090, Thms 2.1 to 2.6, Cor 7.13 | Orbit closures of tuples on non-arithmetic Veech surfaces. | None. The paper excludes arithmetic surfaces. | [CITED, SUBAGENT] |
| Eskin, Masur, Schmoll (arithmetic case) | Referenced by Eskin–Marklof–Morris for the arithmetic case. | None. | Not read by anyone in this project. |
| Gutkin, Hubert, Schmidt, Ann. Sci. ENS 2003, Thms 1, 2 | Arithmetic iff infinitely many periodic points; periodic points are the preimage of `Q^2/Z^2`; the only closed infinite `Aff`-invariant subset of `S` is `S`. | Published form of Lemma D for the full affine group. | [CITED, SUBAGENT] |
| Apisa, Wright, arXiv:1708.03411v3 | Finite blocking results. Section 3 assumes that the surface isn't a torus cover. | None. | [CITED, SUBAGENT] |

No published theorem states the orbit-closure trichotomy for pairs of points on
a square-tiled surface in the form that the reduction needs. Lemmas D, G, and F
supply it with elementary proofs. Nothing in Sections 5.2 to 6.3 depends on a
citation except the unfolding lemma.

### 5.2 Lemma D: single points

**Lemma D. [PROVED HERE]** Let `X` be a compact connected translation surface
tiled by squares of side `1/N`, with every cone point at a tile vertex. Let
`p : X -> R^2/Z^2` be the tiling map, with the vertices over `(1/N) Z^2`. Let
`H` and `Vt` be affine homeomorphisms of `X` with derivatives
`[[1, a], [0, 1]]` and `[[1, 0], [b, 1]]`, `a` and `b` nonzero integers, that
fix every tile vertex. Then every point `x` with `p(x)` irrational has a dense
`<H, Vt>`-orbit.

*Proof.* `H` fixes each horizontal tile edge pointwise, because it fixes the
end vertices and its derivative fixes the horizontal direction. The complement
of the horizontal edges is a disjoint union of open row cylinders. Each has
height `1/N` and a circumference `c` in `(1/N) Z`. `H` preserves each row
cylinder `R`, because `H` is the identity on the edges that bound `R` and
preserves the upper side. On `R`, `H(x, eta) = (x + a eta, eta)`. The same
holds for `Vt` on column cylinders.

Write `p(x) = (x1, x2)`. Suppose that `x2` is irrational. Then `x` lies in a
row cylinder at an irrational height `eta`, and `a eta / c` is irrational. `H`
rotates the closed leaf `l` through `x` by an irrational angle. So the orbit
closure `Y` contains `l`.

The leaf `l` avoids the vertices. So it crosses each tile that it meets from
the left edge to the right edge. Let `C` be a column cylinder that `l` meets.
Every vertical leaf of `C` meets `l`. For a point of `l` with irrational first
coordinate, the `Vt`-orbit closure contains its vertical leaf. These leaves
are dense in `C`. So `Y` contains the closure of `C`.

Call a row or column cylinder *full* when `Y` contains its closure. If a full
cylinder `C1` and a cylinder `C2` of the other direction share a tile, `C2` is
full. Proof: `Y` contains the tile. Its points with an irrational transverse
coordinate have orbit closures that contain their leaves in `C2`, and these
leaves are dense in `C2`.

Two tiles that share a vertical edge lie in one row cylinder. Two tiles that
share a horizontal edge lie in one column cylinder. `X` is connected, so every
tile is joined to a tile of a full cylinder by a chain of shared edges. So
every tile lies in `Y`, and `Y = X`. If `x1` is irrational and `x2` is
rational, exchange the roles of `H` and `Vt`. ∎

### 5.3 Lemma R: a rational point and an irrational point

**Lemma R. [PROVED HERE]** Let `s != t` be points of `M \ VM` with `pi(s)`
rational and `pi(t)` irrational. Then `(s, t)` is M-lit.

*Proof.* The `G`-orbit of `s` lies over the finite orbit of a torsion point,
so it's finite. Choose `n` with `h^n s = s` and `v^n s = s`. By Lemma D for
`H = h^n`, `Vt = v^n`, the orbit of `t` under `<h^n, v^n>` is dense. `s` is a
regular point, so a flat disc around `s` contains no point of `VM`. Choose `g`
with `g t` in that disc and `g t != s`. The radius from `s` to `g t` avoids
`VM`. So `(g s, g t) = (s, g t)` is M-lit, and so is `(s, t)`. ∎

This is Theorem A of d3 at the level of `M`. d3-review accepted Theorem A.

### 5.4 Lemma G: generic pairs

Call `(z, w)` in `T^2` *generic* when no `(a, b) != (0, 0)` in `Z^2` has
`a z + b w` in `Q^2/Z^2`.

**Lemma G. [PROVED HERE]** Let `(s, t)` be in `M x M` with
`(pi(s), pi(t))` generic. Then the diagonal `G`-orbit of `(s, t)` is dense in
`M x M`.

*Proof.* Write `pi(s) = (x, y)` and `pi(t) = (u, v)`. Work in the rational
vector space `R/Q`. Let `r1` be the rank of the classes of `x`, `u` and `r2`
the rank of the classes of `y`, `v`. A relation `(a, b)` must cancel both
`(x, u)` and `(y, v)` modulo `Q`. Genericity leaves three cases.

*Case A: `r2 = 2`.* Then `1, y, v` are independent over `Q`. `h x h` rotates
the torus `l_s x l_t` of the two horizontal leaves by `(Lh y, Lh v)`, up to
rational shifts. By Kronecker's theorem the orbit closure `Y` contains
`l_s x l_t`. Pairs `(s', t')` on it with `1, x', u'` independent are dense. For
these, `v x v` fills the product of the two vertical leaves. So `Y` contains
`closure(C) x closure(C')` for every column `C` met by `l_s` and every column
`C'` met by `l_t`.

Call a pair of cylinders of the same direction *full* when `Y` contains the
product of their closures. Suppose `(C1, C2)` is full, `C1'` shares a tile
with `C1`, `C2'` shares a tile with `C2`, and `C1'`, `C2'` have the other
direction. Then `(C1', C2')` is full, by the Kronecker argument on the product
of the two tiles. A chain argument as in Lemma D, moving one factor at a
time, shows that `Y` contains every product of two tiles. So `Y = M x M`.

*Case A': `r1 = 2`.* Exchange the axes.

*Case B: `r1 = r2 = 1`.* Then `(y, v) = q + eta alpha` and
`(x, u) = q' + xi beta`, with `q`, `q'`, `alpha`, `beta` in `Q^2`, `eta` and
`xi` irrational, and `alpha`, `beta` nonzero. If `det(alpha, beta) = 0`, a
nonzero integer vector is orthogonal to both, which gives a relation. So
genericity gives `det(alpha, beta) != 0`. Some multiple of the rotation vector
`(Lh y, Lh v)` is `eta' alpha` modulo the period lattice, with `eta'`
irrational. Its multiples are dense in the closed circle `{r alpha}`. So `Y`
contains the pairs `(s_r, t_r)` obtained by moving `s` by `r alpha_1` and `t`
by `r alpha_2` along their horizontal leaves, for every real `r`. Choose `r`
with `1, xi, r` independent over `Q`. A rational relation
`a (x + r alpha_1) + b (u + r alpha_2) in Q` forces `(a, b) . beta = 0` and
`(a, b) . alpha = 0`, so `(a, b) = 0`. So `(s_r, t_r)` is in case A', and its
orbit closure is `M x M`.

If `r1 = 0` or `r2 = 0`, genericity forces the other rank to be 2. ∎

### 5.5 Lemma F: relation families

**Lemma F. [PROVED HERE]** Let `(s, t)` be in `M x M`, `z = pi(s)`,
`w = pi(t)`, with `z` irrational. Let `(a, b)` be a primitive integer vector
with `a b != 0` and `a z + b w = c0` in `Q^2/Z^2`. Let `M° = M \ L` and

`F° = {(s', t') in M° x M° : a pi(s') + b pi(t') = c0}`.

Let `F°_0` be the connected component of `F°` that contains `(s, t)`. Then:

1. `F°` is a closed two-dimensional submanifold of `M° x M°`. Locally
   `(pi(s'), pi(t')) = (z + b xi, w - a xi)`, and `xi` is a translation chart.
2. The metric completion of `F°` is a compact surface tiled by squares of side
   `1/N` for some `N`.
3. The `G`-orbit of `(s, t)` is dense in `F°_0`.
4. If `(s, t)` is M-dark, every pair `(s', t')` in `F°_0` with `s' != t'` is
   M-dark.

*Proof.* 1. Choose integers `m, n` with `m b + n a = 1`. Then
`xi = m (pi(s') - z) - n (pi(t') - w)` is well defined modulo `Z^2` and is a
local chart, because `M° -> T \ {0}` is a covering.

2. `xi : F° -> T \ B` is a local homeomorphism with fibres of constant finite
size `(deg pi)^2`. Here `B` is the finite set where `z + b xi` or `w - a xi`
is `0`. So it's a covering, and the completion is a branched cover of `T`.
The points of `B` are `xi = -z/b` modulo `(1/b) Z^2` and `xi = w/a` modulo
`(1/a) Z^2`. Their differences are rational, because
`w/a + z/b = c0/(a b)`. Use the chart `zeta = xi + z/b`. Then `B` lies over
rational points, and the completion is tiled by squares of side `1/N`.

3. `h x h` acts on `F°` when `A_h c0 = c0`, which holds for a power of `h`.
In the chart `zeta` it's affine with derivative `A_h`. It permutes the
punctures, which lie over rational points. So a power of it acts on the
`zeta`-torus as a power of `A_h`, preserves the component, and fixes every
tile vertex. The same holds for `v x v`. `zeta(s, t) = z/b` is irrational.
Lemma D gives a dense orbit in the completed component.

4. If some `(s', t')` in `F°_0` with `s' != t'` is M-lit, a neighbourhood of
it in `M x M` is M-lit (Proposition 1). The orbit of `(s, t)` enters it by
item 3. So `(s, t)` is M-lit (Proposition 2). ∎

## 6. The reduction (task 4)

### 6.1 Theorem

**Theorem 1. [PROVED HERE]** Let `(S, T)` be a dark pair of distinct interior
points of `P`, and suppose that `S` is irrational. Then:

1. `T` is irrational.
2. Exactly one coordinate of `S` is irrational. After exchanging the axes if
   necessary, `S = (x, y)` and `T = (rho x + c, v)` with `y`, `v`, `c` in `Q`,
   `rho` in `Q \ {0}`, and `x` irrational.
3. For every small real `delta`, the pair
   `S_delta = (x + delta, y)`, `T_delta = (rho x + c + rho delta, v)` is dark.
   For `x + delta` rational it's a dark pair of distinct rational interior
   points.

*Proof.* Let `s = (S, (1, 1))` and `t_e = (T, e)`. Write `z = pi(s) = (x, y)`,
`w = (u, v)` for the coordinates of `T`, and `D_e = diag(e1, e2)`. Then
`pi(t_e) = D_e w`. Every lift pair `(s, t_e)` is M-dark.

*Item 1.* If `T` is rational, Lemma R makes `(t_e, s)` M-lit.

*Relations.* The M-lit pairs form a nonempty open `G`-invariant set. So a pair
with a dense orbit is M-lit. By Lemma G, no `(z, D_e w)` is generic. So for
each `e` there's a primitive `(a_e, b_e)` with `a_e z + b_e D_e w` in `Q^2`.
`a_e = 0` makes `w` rational, and `b_e = 0` makes `z` rational. So
`a_e b_e != 0`.

*Item 2.* Suppose that `x` and `y` are both irrational. For `e = (1, 1)`, put
`r = -a_e/b_e`. Then `u = r x` and `v = r y` modulo `Q`. For `e = (-1, 1)`,
put `r' = a_e/b_e`. Then `u = r' x` and `v = -r' y` modulo `Q`. So
`(r - r') x` and `(r + r') y` are rational. That gives `r = r'` and `r = -r'`,
so `r = 0`, a contradiction. So exactly one coordinate is irrational. Take it
to be `x`. The relation for `e = (1, 1)` gives `a y + b v` in `Q`, so `v` is
rational, and `u = rho x + c` with `rho = -a/b` and `c` rational.

*Item 3.* Fix `e`. The relation for `e` reads `a_e x + b_e e1 u` in `Q`. With
`u = rho x + c` and `x` irrational, this gives `a_e + e1 b_e rho = 0`. So
`a_e pi(s_delta) + b_e pi(t_{e,delta})` doesn't depend on `delta`. The lift
pair of `(S_delta, T_delta)` moves continuously in the set `F°` of Lemma F
for `(s, t_e)`, so it stays in the component `F°_0`. For small `delta` the two
points are distinct and off `L`. Lemma F, item 4, makes all four lift pairs
M-dark. So `(S_delta, T_delta)` is dark. ∎

**Corollary 1 (reduction theorem). [PROVED HERE]** If every pair of distinct
rational interior points of `P` is lit, every pair of distinct interior points
of `P` is lit.

**Remarks.**

- Hypotheses: `P` is a strictly simple orthogonal lattice polygon. The points
  are interior. No hypothesis on cylinders or directions.
- The proof takes no limit of room pairs. The family of item 3 stays at a
  fixed positive distance from the diagonal, the walls, and the vertices for
  small `delta`. So nothing escapes.
- The slide continues along the horizontal billiard flow for all `delta`
  until a lift meets `L`. If `y` and `v` aren't integers, no lift meets `L`.
  `S` moves at speed 1 and `T` at speed `|rho|`, each reflecting at the ends
  of its row. Every pair of the continued family with two distinct room
  points is dark.
- In the family, `S_delta` and `T_delta` never lie in one rectangle inside
  `P`, and never in one cylinder of any rational direction (Lemma C in
  Section 8).

### 6.2 What Theorem 1 adds to Theorems A and B

- Theorem A decides pairs with one rational and one irrational point. Item 1
  is Theorem A.
- Theorem B needs a one-cylinder direction `(p, q)` with `p q != 0`. It then
  decides every pair with a point off the singular leaves of that direction.
- Theorem 1 needs no special direction and applies to every room. It doesn't
  decide irrational pairs. It reduces a dark irrational pair to dark rational
  pairs and gives its exact shape.

### 6.3 A sufficient condition that removes the families

**Proposition U. [PROVED HERE]** Suppose that `DP` has a nonempty open set `U`
such that every point of `U` illuminates every other non-corner point of `DP`.
Then every irrational point of `DP` illuminates every other non-corner point.
So every dark pair of interior points of `P` is a pair of rational points.

*Proof.* Let `a` be irrational and `b != a`. By Lemma D the `G`-orbit of a
lift of `a` is dense in `M`. Choose `g` with `g a` in `U`. `g b` isn't a
corner, because `g` fixes `L` pointwise. So `(g a, g b)` is DP-lit, and so is
`(a, b)`. ∎

The hypothesis holds in these cases:

- A room for which `DP` is a single cylinder in some rational direction: `U`
  is the open cylinder, by Lemma C.
- Each of the 12 rooms of Section 8 and the 22-wall room: `dpcover` finds open
  source cells with an empty uncovered set. [COMPUTED]

### 6.4 The remaining gap

**Question H. [OPEN]** Does some strictly simple orthogonal lattice room have
a dark pair `S = (x, y)`, `T = (rho x + c, v)` with `x` irrational?

Equivalent form, by Theorem 1 and Lemma F: four M-level families `F°_0`, one
for each `e`, are dark at the same time. Two of them have slope `(a, b)` and
two have slope `(a, -b)`.

What is known:

- Dark two-dimensional families exist on square-tiled surfaces (LMW,
  Section 6, Example 1). The graph of `tau` is one on `M`: a segment from
  `s` to `tau s` has its midpoint at a fixed point of `tau`, which is a corner
  lift. That family only describes pairs `(S, S)`.
- LMW Theorem 2 doesn't exclude a half-rational family. In the family, each
  `S` has one dark partner.
- Wolecki's Theorem 1.2(i) excludes it. I read the proof in arXiv v3,
  pages 9 to 12. **The proof of Lemma 2.9 has a gap. [CITED, READ; the gap is
  my reading, not a published erratum]** The lemma takes an affinely embedded
  surface `S`, given by `a x + b y = u`, with infinitely many points of the
  lifted polygon set `M_{Q,k}` in a ball `U`. It applies one reflection `R_h`
  and gets a second equation `a' R_h x + b' y = w` on the same infinite set.
  It then asserts that the two equations hold on a "2-dimensional
  sub-domain", so the 4 x 4 real coefficient matrix has rank 2. The
  hypothesis only gives an infinite set. An infinite set in two distinct
  affine planes of `R^4` only forces rank at most 3. The reduced matrix has
  the diagonal entries `a, a, b' - b a'/a, b' + b a'/a`. Rank 3 happens
  exactly when `b' = ± b a'/a`. The common solutions then form a real line on
  which `Im x` and `Im y` are constant, or `Re x` and `Re y` are constant.
  That line is the family of Theorem 1, item 3.
- For a polygon whose reflection group is the Klein group, the other
  reflections give compatible lines. So the argument of Lemma 2.9 doesn't
  exclude the family for orthogonal polygons. For a lattice room with a
  45-degree wall, Section 7 excludes it by a different proof.
- I don't claim that Theorem 1.2(i) is false. I didn't find a counterexample
  and didn't search for one.

So for orthogonal rooms, "all dark pairs are rational" is known only under the
hypothesis of Proposition U.

## 7. The 45-degree case (task 6)

Let `P` be a strictly simple lattice polygon whose walls are axis-parallel or
diagonal (slope `±1`). Let `Gamma` be the group generated by the linear parts
of the wall reflections. `Gamma` is a subgroup of the dihedral group `D4` of
order 8, and `D4` preserves `Z^2`.

- The unfolding `M` has `|Gamma|` copies of `P`. The map
  `pi(S, g) = g S mod Z^2` is a covering of `T` branched over `0` only, because
  every wall line maps `Z^2` to itself. So `M` is tiled by unit squares.
- The twists `h`, `v` and the group `G` are defined as in Section 4. Lemmas D,
  R, G, and F and Proposition 1 use only `pi : M -> T`. They hold unchanged.
- `Gamma = D4` exactly when `P` has an axis-parallel wall and a diagonal wall.
- If every wall is diagonal, the map `(x, y) -> (x + y, y - x)` turns `P` into
  an orthogonal polygon with vertices in `Z^2`. It preserves rationality.
  Theorem 1 applies to the image.

**Theorem 2. [PROVED HERE, given the unfolding lemma for these rooms]** Let
`P` have an axis-parallel wall and a diagonal wall. Then both points of every
dark pair of interior points are rational.

*Proof.* Let `(S, T)` be dark with `S` irrational, `z = pi(s)`, and `w` the
coordinates of `T`. The lifts of `T` project to `g w`, `g` in `D4`. By Lemma R,
`T` is irrational. By Lemma G, for each `g` there's a relation
`a_g z + b_g g w` in `Q^2` with `a_g b_g != 0`. Write `[z]` for the class of
`z` in the rational vector space `(R/Q)^2`. `D4` acts on it linearly. Then
`g [w] = r_g [z]` with `r_g` rational and nonzero. With `g = 1`:
`[w] = r_1 [z]`. So `g [z] = (r_g / r_1) [z]` for every `g`. Take `g` the
rotation by 90 degrees: `(-[y], [x]) = lambda ([x], [y])` with `lambda`
rational. Then `(1 + lambda^2) [x] = 0`, so `[x] = 0` and `[y] = 0`. So `z` is
rational, a contradiction. ∎

For these rooms the reduction is trivial: no dark pair has an irrational
point. The second, non-perpendicular reflection removes the line that
survives in the Klein case. Theorem 2 doesn't cover polygons with vertices
off the lattice.

## 8. Twist escape and the 11 rooms (task 5)

### 8.1 Cylinder certificate on DP

Cylinders are taken relative to all corner lifts. Let `C` be an open cylinder
of `M`. If `tau C = C`, `tau` acts on `C` with derivative `-I`, so it fixes a
point of the core curve. The fixed points of `tau` are corner lifts, and `C`
contains none. So `tau C` and `C` are disjoint, and `C` embeds in `DP`.

**Lemma C. [PROVED HERE; it's Lemma A' of d13 in DP form]** Let `C` be an open
cylinder of `DP` in a rational direction. Let `a` be in `C` and `b != a` a
non-corner point of the closure of `C`. Then `(a, b)` is DP-lit.

*Proof.* Develop `C` as the strip `R x (0, w)` modulo a translation. The map
extends to the closed strip. `a` lifts to a point at height in `(0, w)`, and
`b` to a point at height in `[0, w]`. The segment between the lifts lies in
the open strip except possibly at the end point. The corners lie on the
boundary lines, and `b` isn't a corner. ∎

For a direction `(p, q)`, `cyl.py` labels each room point `S` with the
cylinder of `S+` (plus label) and the cylinder of `S-` (minus label). By
Lemma C and the reflection symmetry of `DP`:

- class par is lit when `plus(S) = plus(T)` or `minus(S) = minus(T)`;
- class cross is lit when `plus(S) = minus(T)` or `minus(S) = plus(T)`.

Here `S` must lie in the open cylinder, and `T` in a closed face with that
label. Either point can be the source, because illumination is symmetric.

### 8.2 The checker `dpcover.c`

`dpcover.c` is d13's `cover.c` with these changes:

- Each uncovered polygon carries a class. The subtraction uses the two rules
  of Section 8.1.
- Wall edges and flat boundary lattice points are source cells too. A twist
  can move a source onto a wall.
- No pole test. All directions `1 <= p, q <= B` are processed.
- It reports the live source cells. A source cell is *live* when its
  uncovered set `Q` isn't empty. A source in a dead cell illuminates every
  other non-corner point of `DP`, in both classes.

So a DP pair `(a, b)` is DP-lit whenever `a` or `b` lies over a dead room
point. [PROVED HERE given Lemma C; the implementation is checked by sampling
only]

### 8.3 Lemma T': twist escape

Let `|t|` be the distance from a real `t` to the nearest integer. For
`r < 1/3`, the *cross* is
`C(r) = {(x, y) in T : |x| <= r or |y| <= r}`. Let `Live*` be the image in
`T` of the live room points, closed under both sign changes. Let `Gamma0` be
the grid `{(x, y) : Lv x in Z, Lh y in Z}`. On `DP`, `pi` is defined up to
sign, which is enough here.

**Lemma T' (cross form). [PROVED HERE]** Suppose that `Live*` lies in `C(r)`
united with a finite subset `E` of `Gamma0`, with `r < 1/3`. Let `(a, b)` be a
dark DP pair of non-corner points. Then each of `pi(a)`, `pi(b)` lies in
`(1/D) Z^2`, where

- `D = lcm(Lh lcm(3, Lv), Lv lcm(3, Lh))` if `r < 1/4`;
- `D = lcm(Lh lcm(60, 2 Lv), Lv lcm(60, 2 Lh))` if `1/4 <= r < 1/3`.

Also, the orbit of `pi(a)` under `<A_h, A_v>` stays in `Live*`, and the same
holds for `pi(b)`.

*Proof.* For every `g` in `G`, `(g a, g b)` is dark, and `g b` isn't a corner.
So `g a` and `g b` lie over live points (Section 8.2), and `A_g pi(a)` is in
`Live*`. That's the last claim.

Let `(x, y)` be a point of the orbit of `pi(a)`. Let `b(y)` be the denominator
of `Lh y`, or infinity, and `b'(x)` the denominator of `Lv x`. The `A_h`-orbit
of `(x, y)` is `X x {y}` with `X = x + (1/b(y)) Z`, or `X` dense. The
`A_v`-orbit is `{x} x (y + (1/b'(x)) Z)`. Call `t` *far* when `|t| > r`.

Take `1/4 <= r < 1/3`. A coset of `(1/n) Z` with `n >= 3` contains a point at
distance at least `1/2 - 1/(2n) >= 1/3` from `Z`. So it contains a far point.

*Step 1.* If `x` is far, `b'(x) <= 2`. Otherwise the `A_v`-orbit contains
`(x, y'')` with `y''` far. That point is in `Live*` and not in `C(r)`, so
it's in `E`. Then
`Lv x` is an integer, a contradiction. In the same way, if `y` is far,
`b(y) <= 2`.

*Step 2.* Let `n = b(y)` for the point `pi(a) = (x, y)`. If `n` is infinite,
`X` is dense and contains a far point `x'` with `2 Lv x'` not an integer,
against step 1. If `n >= 6`, the far arc has length `1 - 2r > 1/3 >= 2/n`. So
`X` contains two consecutive far points. By step 1 both are in
`(1/(2 Lv)) Z`. So `n` divides `2 Lv`. So `n` divides `lcm(60, 2 Lv)`, and
`y` is in `(1/(Lh lcm(60, 2 Lv))) Z`. The same argument with the axes
exchanged bounds `x`.

For `r < 1/4`, a coset of `(1/2) Z` also contains a far point. Step 1 gives
`b'(x) = 1` for far `x`. In step 2 the far arc is longer than `1/2`, so
`n >= 4` forces `n | Lv`. `Lv` is even. So `n` divides `lcm(3, Lv)`. ∎

**Lemma T (box form). [PROVED HERE]** Suppose that every point of `Live*`
has `|x| <= r` and `|y| <= r`, with `r < 1/4`. Then both points of a dark DP
pair project into `Gamma0`.

*Proof.* The `A_h`-orbit `(x + (1/n) Z) x {y}` stays in the box. A coset of
`(1/n) Z` with `n >= 2` contains a far point. So `n = 1`, and `Lh y` is an
integer. The same argument gives `Lv x` in `Z`. ∎

The scripts use the cross form, because lines 3 and 6 aren't box-localized
with `r < 1/4` at `B = 12`.

### 8.4 Pipeline

For each room, with `B = 12`:

1. `dpcover` writes its live cells. `orbitfilter.py` reads them and computes
   the cross radius `r`, `D`, the set `LiveGrid` of points of `(1/D) Z^2` in
   the closed live cells, and the largest subset `NE` of its torus image that
   is invariant under `A_h` and `A_v`. By Lemma T', a point of a dark DP pair is
   in `LiveGrid` and projects into `NE`. These points are the *candidates*.
2. `gridcheck.py` takes every pair of distinct interior candidates. It
   applies the certificate of Section 8.1 with either point as the source.
   It shoots the remaining pairs with the exact two-tracer shooter of d13.
3. `twistcheck.py` takes the pairs that are still undecided. For each class it
   walks the `G`-orbit of the lift pair and applies the certificate, or the
   class-restricted shooter, to each image.

A room pair is lit as soon as one class is lit. Step 3 is valid by
Proposition 2.

### 8.5 Room-by-room outcome [COMPUTED]

Rooms are numbered by their line in `runs/rooms12.txt` (d13's
`hard_a6to12.txt`). Line 5 is the area-11 room that d13 already closed.

| Line | Area, W | Lh, Lv | Box radius | Cross radius | D | Interior candidates | Pairs | Decided by | Undecided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8, 12 | 6, 6 | 1/11 | 1/21 | 36 | 1 | 0 | no pair to check | 0 |
| 2 | 8, 12 | 6, 4 | 1/11 | 1/19 | 72 | 1 | 0 | no pair to check | 0 |
| 3 | 10, 16 | 12, 6 | 3/11 | 1/10 | 72 | 5 | 10 | certificate 10 | 0 |
| 4 | 12, 12 | 4, 12 | 1/11 | 1/20 | 144 | 3 | 3 | certificate 3 | 0 |
| 5 | 11, 18 | 12, 12 | 5/11 | 1/22 | 144 | 1 | 0 | no pair to check | 0 |
| 6 | 12, 20 | 12, 12 | 78/155 | 7/26 | 1440 | 901 | 405,450 | certificate 400,190; shooter 5,052; twist then certificate 208 | 0 |
| 7 | 12, 12 | 8, 6 | 1/10 | 1/13 | 144 | 4 | 6 | certificate 6 | 0 |
| 8 | 12, 12 | 8, 8 | 1/11 | 1/20 | 192 | 3 | 3 | certificate 3 | 0 |
| 9 | 12, 12 | 8, 8 | 1/11 | 1/23 | 192 | 4 | 6 | certificate 6 | 0 |
| 10 | 6, 8 | 4, 8 | 1/11 | 1/23 | 96 | 1 | 0 | no pair to check | 0 |
| 11 | 6, 8 | 4, 6 | 1/11 | 1/21 | 72 | 1 | 0 | no pair to check | 0 |
| 12 | 12, 12 | 4, 16 | 1/11 | 1/21 | 192 | 3 | 3 | certificate 3 | 0 |

**Outcome.** In each of the 11 open rooms (lines 1 to 4 and 6 to 12), every
pair of distinct interior points is lit. No pair is undecided. This covers
real pairs, not only rational pairs: Lemma T' handles irrational points
directly.

**Proposition O' room (line 8, cells `0 0 3 0 0 1 1 1 2 1 3 1 0 2 1 2 2 2 3 2
0 3 3 3`).** The live cells sit within `1/11` of lattice points. The hosts
include the flat points `(2, 1)` and `(2, 3)` with 2,155 live cells each. That
matches the obstruction of Proposition O': no certificate covers a
neighbourhood of a corner and a flat point. The twists remove it. Of the 15
candidates, 12 are wall points. The interior candidates are the lattice
points `(1, 2)`, `(2, 2)`, `(3, 2)`. The certificate decides all three pairs.

**`W = 20` area-12 room (line 6, cells `0 0 1 0 3 0 1 1 2 1 3 1 0 2 1 2 2 2
0 3 2 3 3 3`).** This room isn't localized near lattice points at `B = 12`.
Its 1,262,969 live cells reach `78/155` from the lattice points. `dpcover`
assigns them to 17 lattice points:

- about 204,900 cells at each of the convex corners `(0, 1)`, `(1, 4)`,
  `(3, 0)`, `(4, 3)`;
- about 88,700 at each of the flat wall points `(0, 3)`, `(1, 0)`, `(3, 4)`,
  `(4, 1)`;
- about 20,100 at each of the reflex corners `(1, 1)`, `(1, 3)`, `(3, 1)`,
  `(3, 3)`;
- about 1,990 at each of the convex corners `(0, 0)`, `(0, 4)`, `(4, 0)`,
  `(4, 4)`;
- the single point `(2, 2)`.

The cross radius is `7/26`, between `1/4` and `1/3`. `orbitfilter.py` counts
8 exceptional live points of `Gamma0`; they include the centres of the four
corner cells. So Lemma T' applies with `D = 1440`. Of 1,544,385 live grid
points, 1,189 are candidates and 901 are interior. All 405,450 pairs are
decided. 208 pairs need a twist: 188 use `h`, 12 use `h^-1`, and 8 use `v`.
`dpcover` needs about 7 GB of memory for this room.

**Room 3 (line 3).** At `B = 12` the box radius is `3/11`, greater than `1/4`. The
cross radius is `1/10`, so Lemma T' applies at `B = 12`. At `B = 14` the box
radius is `2/13` (`runs/b14/room3.out`).

**Control: the 22-wall room.** The same pipeline leaves exactly one undecided
pair, `(0, 0)`, `(2, 2)`, which is the known dark pair. Its orbit under `G`
is a single point, because both points are lattice points. See `runs/q22/`.

### 8.6 Checks of the implementation [COMPUTED]

`validate.py` recomputes the certificates in Python from `cyl.py`, without
`dpcover.c`.

- **Dead cells outside the reported radius.** For sampled sources outside
  the box (cross, for line 6) and sampled targets, every triple
  `(source, target, class)` has a certificate with `p, q <= 12`. 13,940,310
  triples over the 11 rooms, 0 failures. Sources include wall points and
  points with small denominators. Targets include points at `1/1013` from
  every lattice point.
- **Dead grid points next to live cells.** For lines 1, 3, 6, 7, 8, and 12,
  `orbitfilter.py` writes a sample of grid points that `dpcover` reports as
  dead: up to 300 neighbours of live grid points and 300 random points.
  3,244,448 triples, 0 failures. For line 6 the sample has only 30
  neighbours.
- **Negative control.** With the radius lowered to `1/20` on line 10, 128
  triples have no certificate.
- **Soundness.** 300 certified triples for each room are confirmed by the
  class-restricted shooter, with two tracers that must agree on the end sheet.
- **Twists.** About 400 twisted paths for each room, spread over `h`, `h^-1`,
  `v`, `v^-1`: the twisted pair is joined by the path with the twisted vector,
  on the predicted sheet. 0 mismatches. This tests `dplib.twist`.
- **Wall points.** Plus and minus labels agree at every sampled wall point.
- **Shooter cross-check.** All 31 candidate pairs of lines 3, 4, 7, 8, 9, 12
  are also lit by the shooter alone.

One defect found: d13's `m_hits` tracer doesn't detect a corner on a path
that runs along a lattice line. The two tracers disagreed on such a path in
room 3. `dplib.shoot2` and `dplib.shoot_class` skip these directions.
Skipping can only lose witnesses. `shoot.py` itself is unchanged.

These checks are samples. They don't prove that `dpcover.c` is correct.

## 9. Status of each ingredient

| Ingredient | Status |
| --- | --- |
| Unfolding lemma (room pairs and lift pairs) | [CITED, READ], standard, stated without proof in the source |
| Proposition 1, Corollary 1a (openness) | [PROVED HERE] |
| Proposition 2 (invariance; twists don't preserve room pairs) | [PROVED HERE] |
| Lemma D (dense orbits of irrational points) | [PROVED HERE]; published for the affine group by Gutkin–Hubert–Schmidt [CITED, SUBAGENT] |
| Lemma R (rational and irrational point) | [PROVED HERE]; it's Theorem A, accepted by d3-review |
| Lemma G (generic pairs) | [PROVED HERE] |
| Lemma F (relation families) | [PROVED HERE]; compare Hubert–Schmoll–Troubetzkoy Thm 5 [CITED, SUBAGENT] |
| Theorem 1 and Corollary 1 (reduction) | [PROVED HERE] |
| Proposition U | [PROVED HERE] |
| Absence of half-rational families in every orthogonal room | [OPEN]; Wolecki Thm 1.2(i) claims it, with a gap in Lemma 2.9 |
| Theorem 2 (45-degree rooms) | [PROVED HERE], given the unfolding lemma |
| Lemma C (cylinder certificate) | [PROVED HERE]; d13's Lemma A' is unreviewed |
| Lemma T' (twist escape) | [PROVED HERE] |
| Live cells, candidates, pair decisions for the 11 rooms | [COMPUTED]; `dpcover.c` checked by sampling |
| Any statement recalled from memory without a source | None in this document |

**Weakest step.** The 11-room outcome relies on `dpcover.c` reporting every
live source cell. That program is a patched copy of an unreviewed program. The
checks of Section 8.6 are samples. A wrong dead cell near a corner can hide a
candidate. The room-6 result is the most exposed, because it uses the exact
shape of 1.26 million live cells, not only a radius.

The weakest step in the theory is the length of the unreviewed chain
Lemma D, Lemma G, Lemma F, Theorem 1. Case B of Lemma G and item 2 of Lemma F
(rational branch points) are the places to review first.

## 10. Files and commands

All paths are in this directory.

| File | Purpose |
| --- | --- |
| `reduction.md` | This document |
| `dpcover.c` | Class-aware checker on `DP` (patched copy of d13's `cover.c`) |
| `cyl.py`, `shoot.py` | Unmodified copies from d13 |
| `dplib.py` | Shared helpers: certificates, twists, class-restricted shooter |
| `orbitfilter.py`, `run_filter.sh` | Lemma T' filter on the live cells |
| `gridcheck.py`, `twistcheck.py` | Pair decisions |
| `validate.py`, `liveview.py` | Checks and summaries |
| `runs/rooms12.txt` | The 12 rooms |
| `runs/b12/` | `roomN_dpcover.txt`, `roomN_candidates.txt`, `roomN_pairs*.txt` |
| `runs/validate/`, `runs/q22/`, `runs/b14/` | Checks, the 22-wall control, room 3 at `B = 14` |

To reproduce a room, run these commands from this directory:

```sh
cc -O2 -o dpcover dpcover.c
./run_filter.sh 8 12
python3 gridcheck.py runs/rooms12.txt 8 12 runs/b12/room8_candidates.txt 6,12,24
grep UNDECIDED runs/b12/room8_pairs.txt | python3 twistcheck.py runs/rooms12.txt 8 12 6 200
python3 validate.py runs/rooms12.txt 8 12 1 11
```

For line 6, `gridcheck.py` ran in three parts with radii `8,16`
(`room6_pairs_part0.txt` to `part2.txt`), and `twistcheck.py` read their
undecided lines (`room6_pairs_twist.txt`).
