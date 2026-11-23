# Audit of direction 2: parity factors and the r <= 8 count

Independent auditor, 2026-11-09. Part 1 was derived before reading the
coordinator's memo. Nothing here is reviewed by a second party.

Every claim carries one of three tags:

- **PROVED**: this file contains the argument. It is a one-session hand proof.
- **CHECKED BY COMPUTATION**: an exact script in this folder confirms it.
- **CONJECTURAL**: no proof and no complete check.

No room search was run. The scripts enumerate abstract targets `N` and
analyse two rooms already in the record.

## Verdicts

| Item in the memo | Verdict |
| --- | --- |
| `r = delta * z_N + #(reflex corners over poles)` | CORRECT. PROVED in section 1.2. Add `0 <= t <= delta - 1` and `s + 2t = 2 delta - 2`. |
| `Z' = p_a + (3/2) R_a + 2 z_a - 1` | CORRECT once the definitions are fixed. PROVED in section 1.4. Add `R_a` even, `z_N = d - 1 - R_a/2`, and `3 z_X <= d` per class. |
| Conjecture as written | WRONG as written. It omits `phi(S) != phi(T)`, so `N` = unit pillowcase satisfies it for every room. "Midpoint-class" is UNDERDETERMINED; it must mean all three non-A classes. |
| Case list `{(2,2),(2,3),(2,4),(3,2),(4,2)}` plus `delta = 1` | CORRECT. PROVED in section 1.6. It needs `z_N >= 2`, which needs `phi(S) != phi(T)`. |
| "Area is bounded" | CORRECT. Area is at most 16. PROVED in section 1.6. |
| "`delta = 1` is covered by the `k <= 6` theorem" | CORRECT, and incomplete. The same theorem covers all five other cases, because `k <= 2 delta - 2 <= 6`. Section 1.8. |
| "Bases that are not polygon doubles are the open part" | WRONG. Every case closes for every target `N`. Section 1.7 gives a hand proof. Section 1.8 gives the cross-check. |
| "Restricted to `W <= 21` the conjecture is equivalent to the main theorem" | CORRECT for orthogonal rooms, given section 1.7. |

For orthogonal lattice rooms, no finite check remains for `r <= 8`.
The open part is the implication "dark implies separating parity factor".

## Conventions

- `P` is a strictly simple orthogonal polygon with vertices in `Z^2`.
  `n` is its area, `r` its number of reflex corners. `W = 2r + 4`.
- `DP` is the double of `P`. It is a flat sphere. Its cone angles are `pi`
  at the `r + 4` convex corners, `3 pi` at the `r` reflex corners, and
  `2 pi` elsewhere.
- Lattice classes: `A = (even, even)`, `C1 = (odd, even)`, `B = (odd, odd)`,
  `C2 = (even, odd)`. The origin is at the source `S`.
- The pillowcase `PC` is the double of `[0,1]^2`. Its four corners are the
  four classes. The fold map `pi_P: DP -> PC` has degree `n`.
- A **lattice factor** is a pair of branched covers `phi: DP -> N`,
  `psi: N -> PC` with `pi_P = psi o phi`. Both are local isometries off the
  cone points. `delta = deg phi`, `d = deg psi`, `n = delta * d`.
- A **pole** has cone angle `pi`. A **zero** has cone angle `3 pi`. A
  **regular** point has cone angle `2 pi`.
- `N` has the **parity property** when no lattice point of class `C1`, `B`,
  or `C2` in `N` is regular.
- A lattice point of `P` is **transparent** when it is not a corner. It is
  then interior, or it lies on an open wall segment (smooth).
- `e(x)` is the local degree of `phi` at `x`.

## Part 1: independent derivation

### 1.1 Cone angles of N and ramification of phi (PROVED)

`psi` branches only over the four corners of `PC`, which have angle `pi`.
So a lattice point of `N` has angle `k pi`, and every other point has
angle `2 pi`.

For `x` in `DP`, `angle(x) = e(x) * angle(phi(x))`. The angles in `DP` are
`pi`, `2 pi`, `3 pi`. `phi` is onto. So:

- `N` has cone angles `pi`, `2 pi`, `3 pi` only. `N` has no zero of angle
  above `3 pi`.
- Over a non-lattice point, `e = 1`.
- Over a regular lattice point, `e = 1` and the preimage is regular.
- Over a zero, `e = 1` and the preimage is a reflex corner.
- Over a pole, `e` is 1, 2, or 3. The preimage is a convex corner, a
  regular point, or a reflex corner, in that order.

`N` is a sphere, because a branched cover cannot raise the genus.
Gauss-Bonnet on `N` gives `p_N - z_N = 4`.

### 1.2 Formula for r (PROVED)

Each zero of `N` has exactly `delta` preimages, all reflex corners. Every
other reflex corner lies over a pole with `e = 3`. Let `t` count those. Then

    r = delta * z_N + t.

Let `s` count the regular points of `DP` with `e = 2`. Riemann-Hurwitz for
`phi` between spheres gives total ramification `2 delta - 2`. Ramification
occurs only over poles, so

    s + 2t = 2 delta - 2,   0 <= t <= delta - 1,   s = 2 (delta - 1 - t).

`s` counts points of `DP`. An interior lattice point of `P` has two lifts.
A smooth boundary point has one.

**Budget rule.** Assume the parity property. A transparent non-A point of
`P` maps to a non-A lattice point of `N`, which is a pole. Each lift is
regular, so each lift has `e = 2`. An interior transparent non-A point
costs 2 of `s`. A smooth one costs 1. A regular A point over an A pole
also costs 1 per lift.

### 1.3 Darkness criterion (PROVED)

**Claim.** Let `phi: DP -> N` be a lattice factor with the parity property.
Let `S`, `T` be transparent A points of `P`. Fix one lift `S~` of `S`. If
`phi(S~) != phi(T~)` for every lift `T~` of `T`, no billiard path joins `S`
to `T`.

**Proof.** A billiard path lifts to a geodesic `gamma` in `DP` from `S~` to
a lift of `T`. Apply the sheet swap if needed, so the path starts at the
fixed lift. `gamma` avoids cone points in its interior. Its fold image
develops to a straight segment from `0` to a vector `v` in `2 Z^2`. Write
`v = m w` with `w` primitive. `w` is not in `2 Z^2`, so `m` is even.

The lattice points on `gamma` are `x_j` at `j w`, `j = 0..m`. For odd `j`,
`x_j` has the class of `w`, which is not A. `x_j` is regular in `DP`. Its
image is a non-A lattice point of `N`, so a pole with `e = 2`. Near `x_j`,
`phi` is `z -> z^2`. The image path enters the pole and returns along the
same segment. So `phi(x_{j+1}) = phi(x_{j-1})` for every odd `j`. Because
`m` is even, `phi(x_m) = phi(x_0)`. That contradicts the hypothesis.

**Consequences.**

- The condition `phi(S) != phi(T)` carries the whole content. "The images
  are A-class" is automatic.
- All three non-A classes must be non-regular. If class B is allowed to be
  regular, the proof fails for `w = (1,1) mod 2`.
- A certifying `N` needs two distinct A points that are poles or regular:
  `p_A + R_A >= 2`.

### 1.4 Class counts and Gauss-Bonnet (PROVED)

For a class `X`, let `p_X`, `R_X`, `z_X` count the points of `N` over
corner `X` by angle. The local degree of `psi` at an angle-`k pi` point is
`k`. So

    p_X + 2 R_X + 3 z_X = d   for each of the four classes.

Assume the parity property, so `R_X = 0` for `X != A`. Let `p'` and `Z'`
count the non-A poles and zeros. Summing three classes gives
`p' + 3 Z' = 3d`. Gauss-Bonnet gives `p_A + p' - z_A - Z' = 4`. Eliminate
`p'` and use `d = p_A + 2 R_A + 3 z_A`:

    Z' = p_A + (3/2) R_A + 2 z_A - 1.

Corollaries:

- `R_A` is even.
- `z_N = Z' + z_A = d - 1 - R_A / 2`.
- `R_A <= (2/3)(z_N + 1)` and `d <= (4/3)(z_N + 1)`.
- For each non-A class, `3 z_X <= d`.

If `R'` non-A regular points are allowed, the formula becomes
`Z' = p_A + (3/2) R_A + 2 z_A - 1 - R'/2`. So the memo's formula depends on
the parity property covering all three non-A classes.

**CHECKED BY COMPUTATION.** `enum_targets.py` lists every parity target of
degree `d <= 6`. Both displayed formulas hold on all of them.

### 1.5 Sanity checks

**Five-square staircase (PROVED by inspection, CHECKED BY COMPUTATION).**
`N = DP`, `delta = 1`, `d = 5`. With `a = (0,0)`:

- A class: `(0,-2)` is a convex corner. `a` and `b = (2,-2)` are smooth
  boundary points. So `p_A = 1`, `R_A = 2`, `z_A = 0`.
- `Z' = 1 + 3 - 1 = 3`. The three reflex corners are `(1,-1)` in B,
  `(1,-2)` in C1, and `(0,-1)` in C2.
- `d = 1 + 4 = 5` and `z_N = 5 - 1 - 1 = 3`.

**22-wall room (CHECKED BY COMPUTATION).** `delta = 3`, `N` = double of the
staircase, `z_N = 3`, `t = 0`, `r = 9`. `s = 4`: the four seam endpoints
`(-1,0)`, `(1,0)`, `(2,1)`, `(2,3)` are smooth non-A points. The budget is
used exactly.

### 1.6 Cases compatible with r <= 8 (PROVED)

**No target has `z_N <= 1`.** `z_N = p_A + (3/2) R_A + 3 z_A - 1`.

- `z_N = 0` forces `(p_A, R_A, z_A) = (1,0,0)`, so `p_A + R_A = 1 < 2`.
- `z_N = 1` forces `(2,0,0)`, so `d = 2` and `Z' = 1`. That needs
  `3 <= d`.

**Targets with `z_N = 2`.** The sum `p_A + (3/2) R_A + 3 z_A` is 3.

- **Type I**: `(3,0,0)`, `d = 3`. Three A poles. Two non-A classes have one
  zero each. The third class `X` has three poles.
- **Type II**: `(0,2,0)`, `d = 4`. Two regular A points. Two non-A classes
  have one pole and one zero each. The third class `X` has four poles.
- `(0,0,1)` has `p_A + R_A = 0`.

**Case list.** `r >= 2 delta`, so `delta <= 4`. `t <= delta - 1`, so
`delta * z_N <= 8` leaves

    delta = 1,  or  (delta, z_N) in {(2,2), (2,3), (2,4), (3,2), (4,2)}.

**Area bound.** `n = delta * d` and `d <= floor((4/3)(z_N + 1))`.

| `(delta, z_N)` | `d` at most | `n` at most |
| --- | --- | --- |
| (2,2) | 4 | 8 |
| (2,3) | 5 | 10 |
| (2,4) | 6 | 12 |
| (3,2) | 4 | 12 |
| (4,2) | 4 | 16 |

**CHECKED BY COMPUTATION.** The enumeration finds no parity target for
`d = 2`, and exactly types I and II for `z_N = 2`, three of each.

### 1.7 Every case is excluded (PROVED)

**Theorem.** Let `P` be an orthogonal lattice room with `r <= 8`. No lattice
factor with the parity property separates two interior A points of `P`.

The value `r = 9` is attained by the 22-wall room with
`(delta, z_N) = (3,3)`.

The proof uses three lemmas. Place `S` at the origin. `T - S` is in
`2 Z^2`.

#### Lemma 1: blocks

An interior lattice point has all four surrounding cells in `P`. So the
block `K_S = S + [-1,1]^2` lies in `P`. Its four **mid-sides** `S +- e_i`
have class C1 or C2. Its four **block corners** have class B.

Each side of `K_S` has two **outer cells** across it. Let `x` count the
outer cells of one side that lie in `P`.

- `x = 0`: the mid-side is smooth. Cost 1.
- `x = 1`: the mid-side is a reflex corner. Cost 0.
- `x = 2`: the mid-side is interior. Cost 2.

A block corner touches two outer cells, one from each adjacent side, and
one diagonal cell. Let `j` count the adjacent outer cells in `P`.

- `j = 0`: convex corner. A diagonal cell alone would pinch `P`.
- `j = 1`: smooth (cost 1) without the diagonal cell, reflex with it.
- `j = 2`: reflex without the diagonal cell, interior (cost 2) with it.

Blocks of two interior A points never share a cell. They share a side only
when `T - S` is `+-(2,0)` or `+-(0,2)` (**adjacent**). They share one corner
only when `T - S = (+-2, +-2)` (**diagonal**). Otherwise call them **far**.

#### Lemma 2: mid-side inequality

Let `c = n - 8` count the cells outside both blocks.

- A cell is outer for at most one side of each block.
- A cell is outer for both blocks only in the diagonal position. For
  `T = S + (2,2)` the two such cells are `u = [1,2]x[0,1]` and
  `v = [0,1]x[1,2]`. Let `c2` count those in `P`.

In the far and diagonal positions the 8 mid-sides are distinct. At most
`c + c2` of them have an outer cell. The others are smooth. So

    8 - (c + c2) <= s        (far or diagonal).

In the adjacent position the shared mid-side is interior and costs 2. The
six others have disjoint outer cells. So

    2 + (6 - c) <= s         (adjacent).

Both proofs are direct counts from lemma 1 and the budget rule.

#### Lemma 3: local structure of type II targets

Let `alpha`, `beta` be the two regular A points of a type II target.

**`X = B`.** Exactly one of the four mid-side neighbours of `alpha` is a
pole, and the same holds for `beta`. One has its pole on the east-west
axis, the other on the north-south axis.

Proof. Class C1 has one pole and one zero. `N` has 4 edges of type A-C1.
The pole takes 1 edge end and the zero takes 3. `alpha` and `beta` take 2
each. So one of them has east-west neighbours (pole, zero), the other
(zero, zero). The same holds for C2 on the north-south axis. Suppose
`alpha` gets both poles `p1`, `p2`. The quadrant face `F` between the two
edges has corners `alpha`, `p1`, `b`, `p2`. All of `p1`, `p2`, `b` are
poles. A pole has two faces, which share both edges at it. So one back
face `G` shares all four edges of `F`. Then `F` and `G` close up and
`d = 1`. Contradiction.

**`X = C1`.** Both east-west neighbours of `alpha` and of `beta` are C1
poles. One point, say `alpha`, has both north-south neighbours at the C2
zero. Its two diagonal neighbours on one vertical side sit at the B pole.
Its other two sit at the B zero. The other point `beta` has north-south
neighbours (pole, zero) and all four diagonals at the B zero.

Proof. The four C1 poles take the four A-C1 edges, so all east-west
neighbours are poles. The B pole `b` has two faces `F`, `G` sharing edges
`b-c1` and `b-c2`. `c1` is a pole, so `F` and `G` also share the edge from
`c1` to an A point. So both faces sit at one A point, `alpha`, on either
side of one east-west edge. If `c2` is a pole, `F` and `G` share all four
edges and `d = 1`. So `c2` is the C2 zero and is both north-south
neighbours of `alpha`. The remaining counts follow: `beta` gets the C2
pole, and six of eight face corners at A points lie at the B zero.

`X = C2` is the mirror image under `(x,y) -> (y,x)`.

**CHECKED BY COMPUTATION.** `python3 enum_targets.py 4 -v` prints the same
local structures.

Because `phi` is a local isometry at an unramified lift of `S`, the eight
neighbours of `S` map to the eight neighbours of `phi(S~)`. The map may
rotate by a half-turn. A neighbour over a zero is a reflex corner. A
neighbour over a pole is a convex corner, a transparent point, or, when
`t > 0`, a reflex corner. When `t = 0`, a neighbour is reflex exactly when
it lies over a zero. The patterns of `alpha` and `beta` differ, so both
lifts of `S` then map to the same point of `N`.

#### Case delta = 1

`N = DP` and `s = 0`. No non-A point is transparent.

- Every mid-side is reflex. So each side has exactly one outer cell.
- No block corner is transparent. Two neighbouring corners of a block
  cannot both be convex, because the side between them has an outer cell.
  So each block has at least 2 reflex corners.
- The adjacent position has an interior mid-side, so it is excluded.
- Two blocks share at most one corner.

So `r >= 4 + 4 + 2 + 2 - 1 = 11`.

#### Case delta = 2: (2,2), (2,3), (2,4)

`e <= 2`, so `t = 0` and `s = 2`. Apply lemma 2 with the area bound.

- (2,2): `c <= 0`. Far or diagonal: `8 <= 2` fails. Adjacent: `8 <= 2`
  fails.
- (2,3): `c <= 2`. Far or diagonal: `8 - 4 <= 2` fails. Adjacent:
  `2 + 4 <= 2` fails.
- (2,4): `c <= 4`. Adjacent: `2 + 2 <= 2` fails. Far: `8 - 4 <= 2` fails.
  Diagonal needs `c2 = 2`. Then `(1,1)` is interior and costs 2. The two
  remaining cells cover at most 2 of the 4 far mid-sides. The other two
  cost 2 more. Total 4 > 2.

#### Case (3,2)

`s = 4 - 2t`, `r = 6 + t`.

**Type I**, `n = 9`, `c = 1`. Every A point of `N` is a pole. The four
lifts of `S` and `T` have `e = 2` and cost 4. So `s = 4` is spent. Lemma 2
then needs `6 <= 0` or `7 <= 0`.

**Type II**, `n = 12`, `c = 4`.

- **Adjacent**, `T = S + (2,0)`. Lemma 2 gives `4 <= s`. So `s = 4`,
  `t = 0`, and the count is tight. Exactly four non-shared mid-sides are
  reflex and no other non-A point is transparent. With `t = 0` each non-A
  class has 0 or 3 reflex corners, and two classes have 3. C1 has at most
  2 mid-sides here, so C2 has at least 2 reflex mid-sides, hence exactly
  3 reflex corners. Then C1 has at least 1, hence 3. So B has none. But
  `(1,1)` touches a cell of each block, so it is not convex. It is B-class,
  and it is neither reflex nor budgeted. Contradiction.
- **Far.** Lemma 2 gives `4 <= s`, so the count is tight. All four extra
  cells are outer cells, on four distinct mid-sides. `P` is connected and
  no cell is outer for both blocks. So some cell next to `K_S` shares an
  edge with a cell next to `K_T`. Checking the positions leaves
  `T = S + (4,0)` up to symmetry, with connector cells `[1,2]x[0,1]` and
  `[2,3]x[0,1]`. The two cells above them are not outer cells, so they are
  absent. Then `(2,1)` is a smooth C2 point. It costs 1 above a spent
  budget.
- **Diagonal, `u` and `v` both in `P`.** `(1,1)` is interior, cost 2. Two
  cells remain for four far mid-sides, so at least two are smooth. Total
  cost is at least 4. So `s = 4`, `t = 0`, `r = 6`, and all is tight. The
  six reflex corners are the four near mid-sides and two far mid-sides.
  Take a far reflex mid-side, for example `(-1,0)` with outer cell `w`.
  If `w = [-2,-1]x[0,1]`, the corner `(-1,1)` has `j = 1`. The diagonal
  cell is not an outer cell, so it is absent. `(-1,1)` is smooth and
  unbudgeted. If `w = [-2,-1]x[-1,0]`, the corner `(-1,-1)` is smooth, or
  it is a seventh reflex corner. The other far mid-sides fail the same
  way by symmetry.
- **Diagonal, only `u` in `P`.** `(1,1)` is a reflex B corner. Lemma 2
  gives cost at least 3. `s` is even, so `s = 4`, `t = 0`. A side with
  `x = 2` would push the cost to 6. So `(1,0)` and `(2,1)` have `x = 1`
  and are reflex, in classes C1 and C2. Three non-A classes then hold
  reflex corners. With `t = 0`, reflex corners lie over zeros, and only
  two classes have zeros.
- **Diagonal, neither `u` nor `v`.** `(1,1)` is a pinch point.

#### Case (4,2)

`r = 8 + t <= 8` forces `t = 0`, `s = 6`. Reflex corners lie only over
zeros.

**Type I**, `n = 12`, `c = 4`. The lifts of `S`, `T` cost 4. Budget 2
remains. Far: `8 - 4 <= 2` fails. Adjacent: `2 + 2 <= 2` fails. Diagonal
needs `c2 = 2`. Then `(1,1)` costs 2, and four far mid-sides share two
cells. Total above 2.

**Type II, `X = B`**, `n = 16`. No block corner is reflex. Define the cost
of `S` as the cost of its eight neighbours. By lemma 1, a side with
`x = 0` adds 1. A side with `x = 1` adds 1 through the corner it touches.
A side with `x = 2` adds 4. So `cost(S) >= 4`, and `cost(T) >= 4`.

- Far: no shared neighbour. Total at least 8 > 6.
- Adjacent: the shared side has `x = 2` for both blocks. Total above 6.
- Diagonal, `T = S + (2,2)`: only `(1,1)` is shared. Its cost is at most
  2. So the total is at least 6, and equality forces `u`, `v` in `P`,
  `(1,1)` interior, and every side of both blocks with `x <= 1`. By lemma
  3, exactly one side of `K_S` has `x = 0`. East and north have `x = 1`.
  By the mirror `(x,y) -> (y,x)`, assume west has `x = 1` with outer cell
  `w`, and south has `x = 0`. The budget is spent.

  Type II has no A pole and no A zero, so no A point is a corner of `P`.
  Take `w = [-2,-1]x[0,1]`. `(-2,0)` is A-class with `w` present and the
  cell below `w` absent. So it is smooth, and `w2 = [-3,-2]x[0,1]` is in
  `P`. The corner `(-1,1)` must not be reflex, so `[-2,-1]x[1,2]` is
  absent. `(-2,1)` is C2-class with `w`, `w2` below it. It is unbudgeted,
  so it is reflex, and `w3 = [-3,-2]x[1,2]` is in `P`. Now `(-3,1)` is
  B-class with `w2` and `w3` on one side. It is smooth, reflex, or
  interior. All three are excluded.

  Take `w = [-2,-1]x[-1,0]`. The same chain runs downward: `(-2,0)` forces
  `[-3,-2]x[-1,0]`, `(-1,-1)` forces `[-2,-1]x[-2,-1]` absent, `(-2,-1)`
  forces `[-3,-2]x[-2,-1]`, and `(-3,-1)` is excluded.

**Type II, `X = C1`**, `n = 16`. Separation needs `phi(S) != phi(T)`, and
`N` has exactly two A points. So one of `S`, `T` has pattern `alpha` and
the other has pattern `beta`. Say `S` is `alpha`.

Class B has exactly 4 reflex corners. All four corners of `K_T` are reflex.
Two corners of `K_S` on one vertical side are reflex. So they are corners
of `K_T`, and `T = S +- (2,0)`. Assume `T = S + (2,0)`.

Count costs against `s = 6`:

- `(1,0)` is the shared mid-side. Interior, cost 2.
- `(-1,0)` and `(3,0)` lie over C1 poles. Cost at least 1 each.
- One of `(2,1)`, `(2,-1)` lies over the C2 pole. Cost at least 1.
- Top: `(1,1)` is reflex, so exactly one of `a0 = [0,1]x[1,2]`,
  `a1 = [1,2]x[1,2]` is in `P`. `(0,1)` is reflex, so exactly one of
  `a_ = [-1,0]x[1,2]`, `a0` is in `P`.
  - If `a0` is in `P`: `(0,2)` is A-class, so it is smooth, so
    `[0,1]x[2,3]` is in `P`. Then `(1,2)` is C1-class with two stacked
    cells beside it. It is not reflex, so it costs at least 1.
  - If `a1` is in `P`: `a_` is in `P`. The corner `(-1,1)` lies over the B
    pole and is not convex. It costs at least 1.
- Bottom: the same argument gives cost at least 1.

The points are distinct. The total is at least `2 + 1 + 1 + 1 + 1 + 1 = 7`.

**Type II, `X = C2`.** Apply the mirror `(x,y) -> (y,x)` to the previous
case.

This completes the proof of the theorem.

**Scope of the theorem.**

- It covers pairs of interior A points. It does not cover pairs with a
  smooth boundary point. The 22-wall room has dark pairs of that kind.
- It covers orthogonal rooms. See "Limits".
- It is a hand proof with many small cases. A machine confirmation is
  described under "Optional confirmation".

### 1.8 Cross-check through the baseline theorem

**PROVED.** For any parity factor, the weighted count of transparent
non-A points is at most `s <= 2 delta - 2`. With `r <= 8`, `delta <= 4`,
so `k <= 6`. Also `W = 2r + 4 <= 20`.

The baseline theorem states that `W <= 21` and `k <= 6` imply every
interior A pair is lit. Section 1.3 says a separating parity factor makes
the pair dark. So no such factor exists for `r <= 8`. This argument covers
all six cases at once. It relies on the project's computer-assisted
theorem, as stated in `review/baseline-review.md`. Section 1.7 does not.

### Optional confirmation

No finite check is needed. If you want a machine confirmation of section
1.7, run this check. It enumerates rooms, so it needs Daniel's approval.

- Enumerate strictly simple lattice polyominoes with area 8 to 16 and at
  most 8 reflex corners.
- Keep those that contain two blocks `K_S`, `K_T` with `T - S` in `2 Z^2`.
- Compute the congruence `B_min` of section 3.1 for the class origin `S`.
- Expected result: `B_min` never separates `S` from `T`.

## Part 2: comparison with the memo and with R21

### Formulas

- `r = delta * z_N + #(reflex corners over poles)`: **CORRECT**. The memo's
  justification matches section 1.1. The memo omits the bound
  `t <= delta - 1` and the companion identity `s + 2t = 2 delta - 2`. The
  case list needs the first. The budget rule needs the second.
- `Z' = p_a + (3/2) R_a + 2 z_a - 1`: **CORRECT** under three definitions.
  `N` covers the unit pillowcase compatibly with the fold. `p_a`, `R_a`,
  `z_a` count A-class points of `N` by angle. No B, C1, or C2 point of `N`
  is regular. The memo states none of the three.
- Both numerical checks in the memo are right.

### Conjecture statement

**WRONG as written.** The memo's two conditions hold for `N = PC` and
`phi = pi_P` in every room. `PC` has four poles, and `pi_P(S)` is the A
corner. The statement needs a third condition: `phi(S~) != phi(T~)` for
the lifts. `review/fold-route-contract.md` has it ("two distinct smooth
boundary A points").

**UNDERDETERMINED.** "Midpoint-class" must mean classes C1, C2, and B. In
canonical45 language C alone is the midpoint class. With C alone, the
darkness proof and the `Z'` formula both fail. "Compatible with the lattice
structure" must mean `pi_P = psi o phi`.

### Case list and the open part

- The list is **CORRECT**.
- "Area is bounded" is **CORRECT**: `n <= 16`.
- "The extension to bases that are not polygon doubles is the open part"
  is **WRONG**. Sections 1.7 and 1.8 close every case for every `N`.

### What goes beyond R21

R21 treats whole congruent copies of an embedded strict base polygon, with
`f(S)`, `f(T)` distinct smooth boundary A points. It allows diagonal walls.
The factor framework differs as follows.

- **Wider.** `N` is any flat sphere. Types I and II are not doubles of any
  polyomino. PROVED: no tromino has two reflex corners, and the T and S
  tetrominoes have smooth points of two classes. `phi(S)` may be a pole or
  an interior point of the base. The pieces need not be congruent copies.
- **Canonical.** Section 3.1 gives one factor `N_min` to test. R21 has no
  such object.
- **Narrower.** The formulas hold for orthogonal rooms only.
- **Independent proof.** Section 1.7 gives `r >= 9` without a computer.

The bound `k <= 2 delta - 2` is the same in both. R21 gets it for copies.
Section 1.2 gets it for every factor.

## Part 3: the W-independent conjecture

### 3.1 The finest parity factor N_min (PROVED)

Label the cells `1..n`. The fold cover has monodromy permutations
`sigma_A`, `sigma_C1`, `sigma_B`, `sigma_C2` on the cells. They generate
`G`. A cycle of length `k` in `sigma_X` is a point of angle `k pi`.

Lattice factors correspond to `G`-invariant partitions of the cells. The
points of `N` over corner `X` are the cycles of `sigma_X` on blocks.

A block cycle has length 2 only when a 2-cycle `(i j)` of cells joins two
different blocks. The 2-cycles of `sigma_X`, `X != A`, are the lifts of
transparent non-A points. So:

> Let `B_min` be the `G`-congruence generated by the pairs `{i, j}` over
> all 2-cycles of `sigma_C1`, `sigma_B`, `sigma_C2`. A partition has the
> parity property if and only if it contains `B_min`.

Consequences:

- `N_min = DP / B_min` is the unique finest parity factor. Every parity
  factor is a quotient of `N_min`.
- Some parity factor separates `S` from `T` if and only if `N_min` does.
- You compute `B_min` with a union-find closure in polynomial time.
- Two incompatible symmetries cannot produce a counterexample. All parity
  factors sit below one factor.

**Real structure (PROVED).** Let `kappa_b`, `kappa_l`, `kappa_r`, `kappa_t`
be the four edge-crossing involutions on cells. `G` is generated by their
pairwise products. `kappa_b` conjugates each `sigma_X` to a `G`-conjugate
of its inverse. So `kappa_b` maps generating pairs into `B_min`, and
`B_min` is invariant. The sheet swap of `DP` descends to `N_min`. Its fixed
set contains the image of the walls. So `N_min` is the double of a flat
disc `D_min`. That disc may have interior cone points and may not embed in
the plane.

**Triangle base (PROVED).** For an orthogonal room, factors over the
(2,4,4) triangle sphere add nothing. Let `N'` be the finest parity factor
over the triangle sphere. It exists by the same argument: a regular B
point is a 4-cycle of triangles, and the condition identifies its
half-turn pairs. `N_min` is a parity factor over the triangle sphere, so `N'`
covers `N_min`. Then `N'` covers `PC` and has the parity property over
`PC`. So `N_min` covers `N'`. Hence `N' = N_min`.

The construction of `N_min` works verbatim over the triangle sphere. Use
it for canonical45 rooms with diagonal walls.

### 3.2 Exact form of the conjecture

For interior A points `S != T`:

    S, T dark   <=>   phi_min(S~) != phi_min(T~) for the lifts.

The right-to-left direction is section 1.3 and is PROVED. The open
direction is:

> **Fibre claim (CONJECTURAL).** If `S` and `T` have lifts with the same
> image in `N_min`, a billiard path joins them.

This matches the corrected dichotomy in `coordinator-log.md`. The new
content is that one factor decides it.

### 3.3 Restatement or independent content

- **At `W <= 21` it is a restatement.** For orthogonal rooms, section 1.7
  shows `N_min` never separates when `r <= 8`. So the fibre claim at
  `W <= 21` says "every interior A pair is lit". That is the target
  theorem. Direction 2 does not reduce the target.
- **W-independently it has content.** It is falsifiable at `W >= 22`. It
  predicts the full dark set of every room from a polynomial-time
  invariant.
- **The open direction is a lit-side statement.** It asserts that light
  exists. The memo's diagnosis says lit-side arguments are what blocked.
  The conjecture relocates that difficulty and does not remove it.

### 3.4 Evidence

**CHECKED BY COMPUTATION** (`room_model.py`, `run_room_model.log`). Exact
illumination uses the full `SL(2,Z)` orbit of the 4-fold unfolding.

- 22-wall room, 2,592 orbit states. `B_min` has 5 blocks of size 3.
  `N_min` is the double of the staircase. `|G| = 233,280`.
- Regular A points: `(0,0)` and `(2,2)` interior, `(4,0)` and `(2,-2)`
  smooth. Fibres: `{(0,0), (4,0)}` and `{(2,2), (2,-2)}`.
- Same-fibre pairs are lit. All four cross pairs are dark. The equivalence
  holds, including the boundary points.
- With the class origin moved to `(1,0)` or `(0,1)`, `N_min = PC`. The two
  regular points of the new A class are lit. 576 states each.
- Staircase: `|G| = 60`, `B_min` trivial, `a` and `b` dark.

**Limits of the evidence.**

- The fibre claim was tested on 4 pairs in one room. Each pair includes a
  smooth boundary point. No interior-interior pair at `W >= 22` was
  tested.
- Rooms with `k = 0` have `N_min = DP`. Fibres are single points. The 327
  census rooms and the classic rooms do not test the claim.
- The baseline theorem confirms the claim for `W <= 21`, `k <= 6`.
- No evidence exists for `k >= 5` at `W >= 22`.

### 3.5 Attempts to break it (CONJECTURAL)

No counterexample was found. No room search was run. Three mechanisms
could produce one.

- **One-defect room.** Take a room where every non-A point is a corner
  except one asymmetric transparent point `X`. If `G` is primitive,
  `N_min = PC`. The claim predicts every interior A pair is lit. Every
  path must pass `X` at each odd lattice step. A room where `S` cannot
  reach `X` on a primitive segment would refute the claim.
- **Annex room.** Attach a hall with transparent points to a `k = 0` dark
  room through a one-cell door. If no primitive segment from `S` crosses
  the door to a transparent point, the pair stays dark while `N_min`
  collapses.
- **Origami analogue.** The Heisenberg 27-square surface is dark without a
  factor. So the analogue for general square-tiled surfaces is false. Any
  proof must use that `DP` is a sphere with a real structure. This audit
  found no proved statement in the record that uses that input.

Out of scope: pairs of different classes, and non-lattice rational points.

### 3.6 Assessment

- Not a restatement in W-independent form. A restatement at `W <= 21`.
- Truth: open. The claim is consistent with all data. The data on the open
  direction is thin, and the general origami analogue is false. This audit
  does not rate it "likely true".
- **Most promising proof strategy.** Work on `phi_min: DP -> N_min`. A
  path from `S` projects to a geodesic in `N_min` that reverses at poles.
  The fibre claim says these reversing geodesics act transitively on each
  A fibre. Use the affine group of the square-tiled pair `(DP, N_min)`
  and the real structure. One-cylinder directions (lemma A in
  `d3-two-mechanisms/`) give transitivity where they exist with a regular
  leaf through `S`.
- **For the abstract census in `d6-hurwitz-census/`.** `B_min` is defined
  for any cover. Test "dark iff `N_min` separates" there per pair. A
  failure on a cover without a real structure does not refute the room
  conjecture.

### 3.7 Most valuable next step

Test the fibre claim exactly on rooms with `k >= 1` that have two interior
A points in one `N_min` fibre. For each room, compute `B_min`, then decide
illumination exactly for every same-fibre pair.

- Without approval: run it on saved rooms with transparent points, such as
  the 43-wall beveled control over the triangle sphere.
- With Daniel's approval: one-defect perturbations of census rooms, then
  the orthogonal `W = 22` census.

One dark same-fibre pair refutes direction 2.

## Limits of this audit

- **Orthogonal rooms only.** `W = 2r + 4` and all formulas assume right
  angles. For canonical45 rooms with diagonal walls, nobody has derived
  the Riemann-Hurwitz bookkeeping over the triangle sphere. The bound
  `k <= 2 delta - 2` still holds there. The bound `delta <= 4` from
  `W <= 21` is not derived for factors that are not whole-copy folds.
- **Interior pairs only** in section 1.7.
- **Hand proof.** Section 1.7 was derived twice in this session by
  different case splits. No second person checked it.
- **Exact illumination code** was validated only on the two rooms above.

## Files

- `audit.md`: this file.
- `enum_targets.py`: lists parity targets of degree `d`. Run
  `python3 enum_targets.py 6 -v`.
- `room_model.py`: monodromy, `B_min`, block systems, and exact
  illumination for the staircase and the 22-wall room.
- `run_room_model.log`: output of `python3 room_model.py`.
