# d47: scope of the certificate-side theorem

Opus 5.5, 2026-11-14. Theory only. The only computation was a rerun of the
two existing checkers on the named rooms (about 0.05 CPU-s total, see the
last section). No room, ray, direction, or reflection-word search was run.

Tags: **PROVED** (argued here, proof or sketch below), **CITED** (taken from
the named file, not rechecked), **GUESSED** (belief only).

## 0. Summary

- Gap 1 (coarser pillowcases): **closed for odd index, open for even
  index.** Admissible bases are exactly the pillowcases `P_Lambda` for
  lattices `Lambda` containing `Z^2` and the marks (Section 1). Rectangular
  bases reduce to ordinary certificates of an axis-rescaled room, for any
  `a`, `b` (Section 2). Non-rectangular bases occur for every room. When the
  index is odd and both marks lie in the largest rectangular sublattice, a
  transfer lemma pushes every certificate up to that rectangular base
  (Section 3). Odd-index sheared bases where the marks are outside that
  sublattice remain. They reduce to a finite check unless a Cut certificate
  is involved.
- Gap 2 (at most 2 corner classes): **reduced to its exact form, not
  closed.** Corners occupy at least 3 classes if and only if both axis gcds
  are odd. Over any base `P_Lambda`, the corners occupy at most 2 classes if
  and only if `[Lambda : Z^2]` is even. A room with at most 2 corner classes
  is never normalized, and its coarser rectangular base always reduces to
  an ordinary presentation. The residue is the certificates over
  even-index bases. Every room has such bases, and no bound is known for
  them.
- Gap 3: **(a) different-class lattice marks are reduced to one finite
  check** of W = 20, area-20 rooms. Only Rig can certify them, and I show
  that Rig forces area at most 16, or area exactly 20 at r = 8. **(b)
  Rational marks fold into Sections 1 to 3**, because the marks only enter
  through `Lambda_0`. Irrational marks never have a base (d16 handles
  them).

## 1. Definitions and the classification of bases

Fix a strictly simple orthogonal polygon `R` with integer vertices whose
horizontal and vertical vertex differences each have gcd 1 (**normalized**).
Put one vertex at the origin. Every lattice room is `P = diag(g, g') R` plus
a translation, for exactly one such `R`. Here `g` and `g'` are the gcds of
the vertex differences of `P` (PROVED, by definition). `DP` and `DR` are the
same flat surface up to this affine map. Darkness is invariant under affine
maps of the double, because straight segments go to straight segments and
cone points go to cone points (PROVED).

For a lattice `Lambda` in `R^2`, let `P_Lambda = R^2 / <2 Lambda, -1>`. Its
corners are the images of `Lambda`, in the four classes `Lambda / 2 Lambda`.

**Proposition 1.1 (classification, PROVED).** The pillowcases that `DR`
covers by a half-translation map (a local isometry away from the cone
points) are, up to isometry, exactly the `P_Lambda` with `Lambda` a lattice
containing `Z^2`. Each such `P_Lambda` is a quotient of `B_R = P_{Z^2}`.

Proof sketch. Normalize the chart of the front face to the identity. The
back face then has a chart `p -> +-(x, -y) + t`. On a horizontal edge at
height `y0`, gluing forces `(0, y0)` into `Lambda` up to a fixed coset. On a
vertical edge at `x0`, it forces `(x0, 0)` into `Lambda`. A pillowcase
corner contains the origin vertex, so the coset is `Lambda` itself. So
`Lambda` contains `(x0, 0)` and `(0, y0)` for all vertex coordinates. By
normalization these generate `Z^2`. Conversely, the identity and the
reflection `(x, y) -> (x, -y)` glue correctly for every
`Lambda >= Z^2`. This refines d10's R1 (`d10-mechanisms/theory.md` lines
126 to 137). R1 is the special case "factors of `DR -> B_R`" =
`{Z^2}`. ∎

**Definition 1.2.** Let `S != T` be interior points of `R`, with each lift
`sigma`, `tau` in `DR`. A lattice `Lambda` is **admissible** for `(S, T)`
when `Lambda >= Lambda_0 := Z^2 + Z S + Z T`. Equivalently, `Lambda` is
admissible when both marks lie over corners of `P_Lambda`, which Theorem U
requires. `(S, T)` is **certified dark** when, for some admissible
`Lambda`, every lift pair has a Par, Cut, or Rig certificate
(d10 Theorem U) at every target over `P_Lambda`.

Remarks.

- Theorem U's proof (d10 lines 196 to 231) never uses `B`. So it is sound
  over every admissible base, including bases finer than a presentation's
  unit pillowcase (PROVED, by inspection).
- An admissible base exists if and only if `S` and `T` are rational
  (PROVED: `Lambda >= Z^2` forces `Lambda` into `Q^2`). So "certified dark"
  makes sense exactly for rational pairs. The definition is
  presentation-free. For a presentation `P = diag(g, g') R` with lattice
  marks, the factors of `DP -> B_P` are the `Lambda` with
  `Z^2 <= Lambda <= (1/g) Z x (1/g') Z`. The bases coarser than `B_P` are
  the ones d43 considered. Bases finer than `B_P` are the factors of finer
  presentations `kP`.
- The brief's `D([0,a] x [0,b])` is `P_Lambda` with
  `Lambda = (1/a') Z x (1/b') Z` in `R`-coordinates. "Rectangular" means
  `Lambda = (Lambda ∩ Q e1) + (Lambda ∩ Q e2)`.

**Lemma 1.3 (corner classes, PROVED).** Let `g`, `g'` be the axis gcds of
a lattice room `P`. The corners of `P` occupy at least 3 parity classes if
and only if `g` and `g'` are both odd. They occupy 1 class if and only if
both are even, and 2 classes if and only if exactly one is even.

Proof. Consecutive vertices share a coordinate, so a horizontal edge
joins vertices with the same y-parity. If only two diagonal classes, such
as `(0,0)` and `(1,1)`, occur, every edge joins equal classes. Then one
class occurs. If `g` is odd, both x-parities occur, and likewise for `g'`.
Two classes that cover both parities on both axes are diagonal, which is
impossible. So at least 3 classes occur. If `g` is even, all x-parities
agree, so at most 2 classes occur, both in one column. ∎

This confirms d36's normalization claim (`d36-amalgamation/astra.md` line
99) and d46's description (`d46-cert-check/README.md` lines 35 to 36).

**Lemma 1.4 (base corner classes, PROVED).** The vertices of `R` lie in
`Z^2 <= Lambda`. Their classes in `Lambda / 2 Lambda` number at least 3 if
and only if `m = [Lambda : Z^2]` is odd. If `m` is odd, the map
`Z^2 / 2Z^2 -> Lambda / 2 Lambda` is a bijection.

Proof. The kernel is nontrivial if and only if some `v` in `Z^2 \ 2Z^2`
lies in `2 Lambda`, that is, `v/2` is in `Lambda`. That happens if and
only if `Lambda / Z^2` has an element of order 2, that is, `m` is even.
With a trivial kernel, the map is a bijection of 4-element groups, and
Lemma 1.3 applies to `R`. If `m` is even, the image has at most 2
elements. ∎

So "at most 2 corner classes" is a property of the pair (room, base), and
it means "even index".

## 2. Rectangular bases (gap 1, rectangular case)

**Proposition 2.1 (rectangular reduction, PROVED).** Let
`Lambda = (1/a) Z x (1/b) Z` be admissible for `(S, T)`, with `a` and `b`
any positive integers. Put `A = diag(a, b)`. Then
`R_{a,b} := A R` is a strictly simple orthogonal lattice room with the same
`W` and `r`, and area `ab * n_R`. `A S` and `A T` are lattice points. A
certificate system over `P_Lambda` for `(S, T)` is the same thing as an
ordinary certificate system over the unit pillowcase for
`(R_{a,b}, AS, AT)`.

Proof. `A` conjugates `<2 Lambda, -1>` to `<2 Z^2, -1>`, so it induces an
isometry-up-to-affine-map `P_Lambda -> B` and `DR -> D(R_{a,b})`. The
tower `Q -> N -> P_Lambda`, the monodromy, cycle types, live vertices,
arcs, and lifted graphs are topological or combinatorial data that `A`
carries over unchanged. Corners of `P_Lambda` go to corners of `B`.
`A R` has axis-parallel edges and integer vertices, and strict simplicity
is affine invariant. Isotropy is not used, so `a != b` is allowed. This
agrees with d40's axis-scaling remark. ∎

Consequences.

- If `a` and `b` are odd, `R_{a,b}` has at least 3 corner classes by Lemma
  1.3. Then the d46 theorem applies, as in Section 4.
- Classes are preserved by odd coarsening. If `T - S` is in `2 Z^2` (fine
  coordinates) and `[Z^2 : Lambda']` is odd, then `T - S` is in
  `2 Lambda'` (PROVED: `2 Z^2 ∩ Lambda' = 2 Lambda'` for odd index, by
  the argument in Lemma 1.4). So same-class marks stay same-class over odd
  coarser bases. Over even coarser bases they may not. d43 item 2
  (`d43-review-d39/review.md` lines 196 to 202) omits this point.
- If `a` or `b` is even, `R_{a,b}` has at most 2 corner classes. That is
  gap 2 (Section 5).

## 3. Non-rectangular bases (gap 1, remaining case)

**Proposition 3.1 (they always exist, PROVED).** Every room `R` has
non-rectangular admissible bases for lattice marks, for example
`Lambda = Z^2 + Z (1/2, 1/2)` with index 2. Its affine image is `R`
rotated by 45 degrees: a lattice room with 45-degree walls. Odd-index
non-rectangular bases between `Z^2` and `(1/g) Z x (1/g') Z` exist if and
only if `gcd(g, g') > 1`. Example: the 22-wall room scaled by 3 has
`Z^2 + Z(1/3, 1/3)`. A subgroup of `Z/g x Z/g'` that isn't a product is
the graph of an isomorphism between nontrivial subquotients (Goursat), and
those exist only when `gcd(g, g') > 1`.

For a non-rectangular `Lambda`, write
`Lambda_r = (Lambda ∩ Q e1) + (Lambda ∩ Q e2)`. This is the largest
rectangular sublattice. It contains `Z^2`, and `Lambda / Lambda_r` is
cyclic, because it injects into `pi_1(Lambda) / (Lambda ∩ Q e1)`, a
quotient of a cyclic group (PROVED).

**Lemma 3.2 (transfer, PROVED, sketch).** Let `Lambda' <= Lambda` be
admissible lattices, with `[Lambda : Lambda']` odd and `Lambda / Lambda'`
cyclic. Then every full certificate system over `P_Lambda` yields a full
certificate system over `P_{Lambda'}`.

Proof sketch.

1. *Corners.* By the odd-index argument of Lemma 1.4, each corner of
   `P_Lambda` has exactly one corner of `P_{Lambda'}` above it, with local
   degree 1. The other preimages are regular points. So targets correspond
   one to one, and `c_s = c_t` holds over one base exactly when it holds
   over the other.
2. *Factor.* Given `Q -> N -> P_Lambda`, let `N'` be the component, through
   the image of `Q`, of the normalized fibre product `N x P_{Lambda'}` over
   `P_Lambda`. Then `Q -> N' -> P_{Lambda'}` and `N' -> N`. At a corner
   `x'` over `x`, `P_{Lambda'} -> P_Lambda` is a local isomorphism. So near
   the fibre over `x'`, `N' -> N` is a local isomorphism onto part of the
   fibre over `x`.
3. *Par.* `N` has no regular point over `x`, so `N'` has none over `x'`.
   `phi(sigma) != phi(tau)` implies `phi'(sigma) != phi'(tau)`.
4. *Cut.* `phi(sigma) = phi(tau)` lies over `c_s`, where step 2 gives a
   local isomorphism, so `phi'(sigma) = phi'(tau)`. Regular points of `Q`
   over `c_s'` and `x'` go to regular points (local isomorphism). One point
   of `N` over a corner `w` gives at most one point of `N'` over `w'`, so a
   single cycle stays a single cycle.
5. *Rig.* Identity monodromy at `y` transfers to identity at `y'` (step 2).
   For the arc, take a primitive `w` in `Lambda'` that is also primitive in
   `Lambda`, in the class of the target. It exists because
   `Lambda / Lambda'` is cyclic of odd order: in a Smith basis
   `(u1, u2)` of `Lambda` with `Lambda' = Z u1 + Z m u2`, take `u1`,
   `2 u1 + u2'`, or `u1 + u2'`, where `u2' = m u2`. The segment `0 -> w` is
   a saddle connection in `P_Lambda`, so it is a simple arc avoiding the
   other corners. It lifts to a saddle connection `alpha'` in
   `P_{Lambda'}` between the corners over `c_s` and `x`. `N' -> N` maps
   `Gamma_{alpha'}(N')` to `Gamma_alpha(N)`, sending live vertices to live
   vertices (a regular `Q`-preimage persists). So `K_{N'}` maps into
   `K_N`, which misses `phi(tau)`. Theorem U's Rig step then covers all
   arcs. ∎

**Corollary 3.3 (PROVED).** Suppose `[Lambda : Z^2]` is odd and both marks
lie in `Lambda_r`. Then certificates over `P_Lambda` reduce to ordinary
certificates of `R_{a,b}`, where `Lambda_r = (1/a) Z x (1/b) Z`, with `a`
and `b` odd. Apply Lemma 3.2 with `Lambda' = Lambda_r`, then Proposition
2.1.

Lattice marks of `R` always satisfy the hypothesis, since
`Z^2 <= Lambda_r`. So do rational marks with a rectangular `Lambda_0`.

**Residue G1-odd (sheared bases).** The remaining case is `Lambda`
non-rectangular with odd index and a mark outside `Lambda_r`. This forces
`Lambda_0` itself to be non-rectangular. Example: `R` = any room,
`S = v0 + (1/3, 1/3)`, `T = v0 + (2/3, 2/3)`, and `Lambda = Lambda_0`. No
rectangular cover of `P_Lambda` has the marks over corners, because every
rectangular sublattice lies in `Lambda_r`. The affine image `A_Lambda R` is
a non-orthogonal parallelogram-lattice polygon. Its double carries no
isometric seam reflection: `(x, y) -> (x, -y)` preserves `Lambda` only for
reflection-symmetric `Lambda`. So R4 and the seam steps of d39 Claim 3 do
not apply. What still applies (PROVED, since these steps are pure
cover combinatorics plus Lemma 1.4):

- d36's bound `deg(Q -> P_Lambda) = m n_R <= 5r <= 40` for any separating
  Par quotient. With `m >= 3`, this gives `n_R <= 13`.
- The seam-free part of the Rig analysis (Section 4, steps z = 0 and z = 1,
  and `delta z <= r`, `d <= z + 4`) gives `m n_R <= 24`.

So the systems without Cut form a finite check: rooms with `W <= 20` and
`n_R <= 13`, lattices `Lambda >= Z^2` of odd index `m >= 3` with
`m n_R <= 40`, and marks in `Lambda`. The systems with a Cut certificate
have no known bound. They need a sheared analogue of R4.

## 4. Marks

### 4a. Same-class marks over an odd rectangular base

This is the existing chain, applied to `R_{a,b}`. CITED: d10 Theorem U and
R3; R4 as patched in d43 (Cut forces the cross, which is lit); d39 Claim 3
as checked in d43 (essential Rig forces area <= 20); d36 (Par forces area
<= 5r); the d9 census (no dark same-class pair at W <= 21, area <= 20); and
d46 (no Par triple at W <= 20, area 21 to 5r, at least 3 corner classes).

d46 enumerates compressed shapes with all integer widths and heights of
the right parities (`d46-cert-check/README.md` lines 59 to 83). So it
covers non-normalized rooms with odd gcds, as d43 requires (CITED).

### 4b. Different-class lattice marks (gap 3a)

**Proposition 4.1 (PROVED).** Let `R'` be a room with at least 3 corner
classes and `r <= 8`. Let `S` and `T` be interior lattice points in
different classes `a != t`. Then a certificate for a lift pair exists only
if `n <= 16`, or `n = 20` with `r = 8`, `delta = 4`, `z = 2`, and
`d in {3, 4, 5}`.

Proof.

- With `c_s != c_t`, Theorem U has the single target `t`. Par and Cut need
  `c_s = c_t`, so only Rig(t) can certify. By R3 part 2 (CITED), use
  `N = Q / R_y` for `y` outside `{a, t}`.
- *z = 0.* d36's colour argument uses only `w_y = d` (identity at `y`) and
  3 source classes, so `d = 1` and `N = B`. In `B`, both corners `a` and
  `t` are live (`sigma` and `tau` are regular preimages with `e = 2`). The
  single arc lift joins them. So there is no separation.
- *z = 1.* `d = p_y <= 5`, and a zero needs `d >= 3`. A regular point of
  `Q` can't lie over a zero of `N` (Fact L). So `a` and `t` are not the
  `(3)` corner.
  - `d = 3`: the profiles are `y = (1^3)`, `u = (3)`, and `a`, `t` =
    `(2,1)`. `g_a g_t` is a 3-cycle, so `g_a != g_t`, and the arc graph is
    the path `p - r - r - p`. Every live vertex is on it, so `phi(sigma)`
    and `phi(tau)` are connected.
  - `d = 4` and `d = 5`: impossible for the same reasons as in d43, which
    don't involve the marks.
- *z >= 2.* `delta z <= r`, `d <= z + 4`, and `delta` is even. The
  off-seam-pole step of d39 is CITED; its one-star sub-step is not needed,
  because cell, domino, and square have `z = 0` and the L-tromino has
  `z = 1`. Also, `d = 6` is impossible (seam argument, d43). These steps
  don't involve the marks. They leave `(delta, z) = (2, <= 4)` with
  `n <= 16`, and `(4, 2)` with `r = 8` and `d <= 5`. ∎

Combined with the d9 Part A census (CITED: every different-class lattice
pair is lit at W <= 22, area <= 16), this leaves one finite check.

**Residue D20.** Rooms with W = 20 (r = 8), area 20, and at least 3 corner
classes, and their different-class interior lattice pairs: check whether
`R_y` separates the lift pairs, for the two `y` outside `{a, t}`. That is
at most 169,672,127 rooms up to symmetry (d9 `census_totals.md`, row W = 20,
area 20). The cost is comparable to one d46 pilot cell: about 10 CPU-minutes
at d46's 3.4 µs per room, plus pairs (GUESSED estimate). It hasn't been run.
Odd rescalings add nothing, because `ab n_R = 20` with `ab` odd and
`ab > 1` would need a W = 20 room of area 4.

### 4c. Rational marks (gap 3b)

**Proposition 4.2 (PROVED).** Rational marks need no separate treatment.
The marks enter only through `Lambda_0`. The d16 lattice refinement `kR` is
the presentation whose unit base is `(1/k) Z^2`. Its coarser factors are
the admissible `Lambda` inside `(1/k) Z^2`. So "rational marks" equals "all
admissible `Lambda`", and the cases are as follows:

- **odd `[Lambda : Z^2]` and marks in `Lambda_r`**: covered (Sections 2, 3,
  and 4).
- **odd index, sheared**: Residue G1-odd.
- **even index**: Residue E (Section 5).

The d43 remark that refinement makes `k^2 n > 40` uncertifiable
(`d43-review-d39/review.md` lines 209 to 212) is right about the fine base
`(1/k) Z^2` only. Lemma 3.2 moves the certificate to the coarse
rectangular base, where the area is `n_R ab` with `a, b <= k`.

## 5. At most 2 corner classes (gap 2)

**Proposition 5.1 (PROVED).** A room with at most 2 corner classes has an
even axis gcd (Lemma 1.3), so it is never normalized. Its ordinary
certificates are certificates over the even-index base
`(1/g) Z x (1/g') Z` of its normal form `R`. Its coarser odd rectangular
bases are covered by Section 2. Examples: the 22-wall room scaled by 2 has
the coarser base `Z^2`, of degree 4 over its unit pillowcase, and the
cross scaled by 2 likewise.

The question "does gcd normalization always give at least 3 classes?" has
the answer yes (Lemma 1.3). But it doesn't close the gap. Normalizing moves
the base, not the certificate: a certificate over an even-index base need
not induce one over `Z^2`. Lemma 3.2 fails there, because the corner map
`Z^2 / 2Z^2 -> Lambda / 2 Lambda` has a kernel (Lemma 1.4). So two corners
of the cover lie over one corner, and the targets don't match.

**Residue E (open).** Certificates over `P_Lambda` with even
`[Lambda : Z^2]`, for rooms with `W <= 20`. These include every
presentation with at most 2 corner classes, d10's G1 mechanism, even
denominators, and the 45-degree bases `Z^2 + Z (1/2, 1/2)`. No finite
bound is known. d36's colour bound needs 3 classes, and the cross scaled by
2 has zero-free Par and Rig targets of unbounded `delta`
(`d43-review-d39/review.md` line 141). One fact helps any future argument
(PROVED, by Gauss-Bonnet with `p = z + 4`): every zero-free target is a
pillowcase factor. So a `z = 0` certificate over `P_Lambda` is a separation
by a coarser base `P_{Lambda''}`, `Lambda'' <= Lambda`. Over that base the
marks may land in different classes, which points to a Rig analysis like
Proposition 4.1. I did not complete this (GUESSED that it closes the `z = 0`
part; the `z >= 1` part, with `delta` unbounded, has no idea yet).

## 6. Theorem statement

**Theorem (computer-assisted).** Let `R` be a strictly simple orthogonal
polygon with integer vertices, normalized, with `W <= 20` (`r <= 8`). Let
`S != T` be interior points of `R` with rational coordinates. Let `Lambda`
be a lattice containing `Z^2 + Z S + Z T` (origin at a vertex), with:

- (H1) `[Lambda : Z^2]` odd;
- (H2) `S` and `T` in `Lambda_r = (Lambda ∩ Q e1) + (Lambda ∩ Q e2)`;
- (H3) if `S` and `T` lie in different classes of `Lambda / 2 Lambda`,
  then `n_R [Lambda_r : Z^2] != 20`.

Then the four lift pairs of `(S, T)` are not all certified by Par, Cut, or
Rig over `P_Lambda`. In particular, `(S, T)` is not certified dark over any
such `Lambda`.

Status: PROVED reductions (Sections 1 to 4) on top of the CITED chain d10,
d36, d39 (via d43), d9 phase 1 and Part A, and d46.

**Presentation form (Corollary).** Let `P` be a lattice room with
`W <= 20` whose corners occupy at least 3 parity classes. Let `S != T` be
any interior lattice points. Then `(S, T)` is not certified dark over the
unit pillowcase `B`, or over any pillowcase factor of `DP -> B` whose
lattice holds both marks in its rectangular part. The exception is the
Residue D20 case: different classes, W = 20, coarse area 20. If corners
occupy at most 2 classes, the same holds for every odd-index coarser
factor, but not for `B` itself.

**What is still needed.**

| Residue | Kind | Size |
| --- | --- | --- |
| D20: different-class lattice pairs, W = 20, area 20, Rig via `R_y` | finite canonical-partition check | at most 1.7e8 rooms; about 10 CPU-min plus pairs (GUESSED) |
| G1-odd without Cut: sheared odd bases | finite check | rooms with `n_R <= 13`, odd `m >= 3`, `m n_R <= 40`; small (GUESSED: well under 1e6 room-lattice pairs, since 2r + 4 <= 20 walls at area 13) |
| G1-odd with Cut | new argument (sheared R4) | unbounded |
| E: even-index bases | new argument | unbounded; includes all presentations with at most 2 corner classes |

## 7. Ingredients found narrower than stated

- d10 Theorem U (`d10-mechanisms/theory.md` line 174) says "pillowcase
  factor `P'` of `Q`", which reads as a factor of `Q -> B`. That makes
  "certified dark" depend on the presentation. The proof works over any
  pillowcase quotient. Definition 1.2 uses the presentation-free version.
- d10 line 141 ("No certificate relative to an intermediate pillowcase
  exists") is correct for intermediate covers. But finer admissible bases
  always exist, even for normalized rooms (Proposition 3.1). d43 item 2's
  "(`P' != B`, non-normalized only)" (`d43-review-d39/review.md` line 196)
  is therefore narrower than the full notion. The full notion is needed
  for presentation-invariance.
- d43 item 2 (line 199) says a rectangular relative triple has "the same
  r". That is true, but it omits that mark classes can change over even
  coarser bases (Section 2).
- d43 item 4 (lines 209 to 212) holds only for the fine base; see Section
  4c.
- d39 Claim 3's one-star step is redundant given its z-analysis (Section
  4b). That doesn't change any result.

No ingredient I relied on looked wrong.

## 8. Named-room tests

Run (0.05 CPU-s total, one process each): `d38-review/check_named.py` and
`d43-review-d39/check_cross.py`. The output matches their stored logs.

| Room | Base used | Result | Run or reasoned |
| --- | --- | --- | --- |
| 22-wall room | `Z^2` (own `B`) | Par at b, c, d (blocks 5, 15, 5); certified dark, `r = 9` (outside the theorem) | run |
| 22-wall room scaled by 2 | unit base `(1/2) Z^2`: even, Residue E | 1 corner class (Lemma 1.3). Coarser rectangular `Z^2` (degree 4) gives back the 22-wall certificate by Proposition 2.1, so it stays certified dark | reasoned |
| 22-wall room scaled by 3 | unit base: `n = 135 > 5r`, no ordinary certificate (d43) | Coarser `Z^2` is odd and rectangular; Proposition 2.1 gives back the 22-wall certificate. Certified dark. Odd sheared bases `Z^2 + Z(1/3, +-1/3)` exist (Proposition 3.1) | reasoned (unit-base claim CITED from d43) |
| P6 | `Z^2` | Par at b, c, d (5, 5, 5), `r = 12` | run |
| Cross | `Z^2` | `B_d` separates all four lift pairs, `B_b` and `B_c` don't; `R_y` don't. Uncertified | run |
| Cross scaled by 2 | `(1/2) Z^2` | No Par or Rig separation (blocks 2, 2, 2). Cut excluded (d43). Coarser `Z^2` = cross. Uncertified over the bases checked. Other even bases (Residue E) not checked | run |
| Cross scaled by 3 | `(1/3) Z^2` | All partitions one block. Coarser `Z^2` = cross. Sheared `Z^2 + Z(1/3, +-1/3)` reduce to `Z^2` by Lemma 3.2 (lattice marks). Uncertified | run (unit base); reasoned (sheared) |

The tests are consistent with every reduction. None of them exercises
Residue G1-odd with non-lattice marks, or Residue E beyond the bases
listed.

## 9. Confidence in PROVED claims (GUESSED)

| Claim | Confidence |
| --- | --- |
| 1.1 classification | 90% |
| 1.3, 1.4 corner classes | 97% |
| 2.1 rectangular reduction | 95% |
| 3.1 existence | 95% |
| 3.2 transfer | 75%. The fibre-product steps are standard; the Rig arc choice is the delicate part. |
| 4.1 different-class Rig bound | 75%. It rests on d39's seam steps. |
| 4.2, 5.1 | 90% |
| Theorem as stated | 70%. It inherits the cited chain. |
