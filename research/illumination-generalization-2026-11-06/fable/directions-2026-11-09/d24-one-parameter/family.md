# One-parameter dark families in orthogonal lattice rooms

Date: 2026-11-10. Direction d24. Nobody has reviewed this document.

Status tags: **PROVED** (complete proof here), **CITED** (read in the project
files d16, d16-review, d19, lit-tokarsky; not re-read at the source),
**COMPUTED** (output of `search.py` and `recheck.py` in this directory),
**OPEN**.

## 1. Answer

The question stays **OPEN**: this document doesn't exclude a half-rational
family in every room, and it doesn't produce one. It does three things.

1. **Theorem X (PROVED).** Every family is *homogeneous*: the rational constant
   of each of its four relations is `0` in `R^2/Z^2`. In room terms, a dark pair
   with an irrational point is, after exchanging axes,
   `S = (x, y0)`, `T = ((k - a x)/b, v0)` with `a`, `b` coprime nonzero
   integers, `k` an integer, and `a y0 + b v0`, `a y0 - b v0` integers. So
   `2 a y0` and `2 b v0` are integers. For `rho = ±1`: `T = (k ∓ x, v0)`,
   `y0` and `v0` are both integers or both half-integers.
2. **No abstract obstruction exists (PROVED, Section 4).** Square-tiled
   surfaces branched over one point carry dark two-dimensional families of
   every homogeneous type, including families with no blocking point at all.
   A proof that rooms have no family must use the Klein group action. Twists
   and orbit closures alone can't give it.
3. **No family in small rooms (COMPUTED, given Theorem X and d16 Theorem 1).**
   No family with `rho = ±1` exists in any of the 13,384 strictly simple
   polyomino rooms of area 2 to 9, or in any of 256 "plus-tree" rooms (up to
   25 cells). No family with `max(|a|, |b|) <= 3` exists in the 90 rooms of
   area 2 to 5.

## 2. Setting

Notation is that of d16 (`reduction.md`, Sections 2 to 6). `pi : M -> T =
R^2/Z^2` is branched over `0` only, `L = pi^-1(0)`, `M° = M \ L`, `VM ⊂ L`.
For a dark pair `(S, T)` with `S` irrational, Theorem 1 of d16 (CITED,
confirmed by d16-review) gives `S = (x, y0)`, `T = (u, v0)`,
`u = rho x + c`. For each `e` in `K` the lift pair `(s, t_e)` lies on the dark
surface `F°_0(e)` of Lemma F, with primitive relation `(a, e1 b)`, where
`rho = -a/b`. Because `x` is irrational, the primitive relation is unique up
to sign.

## 3. Theorem X: the constant is zero

**Theorem X. PROVED.** Let `(s, t)` in `M° x M°`, `z = pi(s)` irrational,
`(a, b)` primitive with `a b != 0` and `a z + b pi(t) = c0` in `Q^2/Z^2`. If
`(s, t)` is M-dark, then `c0 = 0`.

*Proof.* Suppose `c0 != 0`. By Lemma F every pair of `F°_0` with distinct
points is M-dark.

*Step 1, the torus `T_M`.* Let `Lambda ⊂ Z^2` be the image of `pi_1(M)` in
`pi_1(T)`, `T_M = R^2/Lambda`, and `q : M -> T_M` the lift of `pi`. Let `N` be
the kernel of `pi_1(T \ 0) -> pi_1(T)`. `N` is the normal closure of the loop
`c` around `0`. Two points of one `pi`-fibre in `M°` have the same `q`-image
iff the monodromy of some element of `N` maps one to the other. (If
`q(s1) = q(s2)`, a path `sigma` from `s1` to `s2` projects to a class in
`Lambda`. A loop `beta` in `M°` at `s1` has the same class, because
`pi_1(M°) -> pi_1(M)` is onto. `beta^-1 sigma` projects into `N`.)

*Step 2, saturation.* `F_T = {(z', w') : a z' + b w' = c0}` is one torus with
chart `xi`: `(z', w') = (z + b xi, w - a xi)`. `F° -> F_T \ B` is a covering.
`B = B_z ∪ B_w`, where `B_z` is the set with `z' = 0` and `B_w` the set with
`w' = 0`. Because `c0 != 0`, `B_z` and `B_w` are disjoint. Take a path `delta`
in `T \ 0` from `w` to a point near `0`. Lift it through the isogeny
`pr_2 : F_T -> T`. Move it off the finite set `B_z`. It ends near a point of
`B_w`. Add a small loop around that point and return. The loop `l` lies in
`F_T \ B`. `pr_2(l) = delta c delta^-1`. `pr_1(l)` is null-homotopic in
`T \ 0`, because the small loop encloses no point of `B_z`. So the monodromy
of `F° -> F_T \ B` contains `(1, n)` for every `n` in `N`. With Step 1: if
`(s', t')` is in `F°_0`, `pi(t'') = pi(t')` and `q(t'') = q(t')`, then
`(s', t'')` is in `F°_0`.

*Step 3, a lit pair.* Take `(s', t')` in `F°_0`. Choose lifts `z~`, `w~` in
`R^2` of `q(s')`, `q(t')`. Then `c~ = a z~ + b w~` is a lift of `c0`, so `c~`
isn't in `Z^2`. A point `(1 - mu) z~ + mu w~` of the segment is a lattice
point for an open set of `xi` only when `mu = b/(a + b)`, and then the point
is `c~/(a + b)`, which isn't in `Z^2`. For any other `mu` and any lattice
point, the bad `xi` form a curve. So for `xi` off a null set the segment from
`z~` to `w~` misses `Z^2`. Its lift from `s'` is a geodesic of `M` that
misses `L`. It ends at a point `t''` with `q(t'') = q(t')`, and `t'' != s'`.
`(s', t'')` is M-lit and lies in `F°_0` by Step 2. Contradiction. ∎

**Corollary X. PROVED, given d16 Theorem 1.** In a half-rational family,
`a x + b u`, `a y0 + b v0` and `a y0 - b v0` are integers. (Apply Theorem X to
the four lift pairs. The relation for `e` is `(a, e1 b)` applied to
`(x, y0)` and `(e1 u, e2 v0)`.)

What Theorem X leaves: both puncture types meet at `xi = 0` when `c0 = 0`.
Only loops around the other punctures give saturation. For `|a| = |b| = 1`
there are none.

## 4. What survives: the invariant structure (attack lines 1 and 3)

**The twist argument isn't a contradiction. PROVED.** `v s` has two
irrational coordinates, and `(v s, v t_e)` is M-dark for each `e`. But
`v k_e = k_e v^-1` for the two reflections (d16 Proposition 2). So the four
images are lift pairs of two room pairs: `(S', T'_+)` under `v t`, dark in
class par, and `(S', T'_-)` under `v^-1 t`, dark in class cross. Theorem 1,
item 2 needs four dark classes of one room pair. `T` also moves differently:
its column and its multiplier `-a/b` differ from those of `S`. No class
changes its relation, so nothing contradicts Theorem 1.

**Orbit closure. PROVED, given Lemma F and Theorem X.** A family is a real
line in `P x P`. Its four lifts lie on four surfaces in `M x M`:

- `F(1,1)`, `F(1,-1)`: components of `{a pi(s') + b pi(t') = 0}`;
- `F(-1,1)`, `F(-1,-1)`: components of `{a pi(s') - b pi(t') = 0}`.

Each is the closure of the `G`-orbit of one lift pair, and each is M-dark. On
`F(e)` both coordinates of `s'` vary, and `p_1 : F(e) -> M` is onto. `k_e`
maps `F(1,1)` to a surface that meets `F(e)` only along the family, because
the two slopes agree only on `dy = dv = 0`. So a room family is exactly a
common line of four dark homogeneous surfaces. No room family has two real
parameters; that's Theorem 1, item 2.

**Mechanisms on one surface. PROVED.** Normalize `a z~ + b w~ = 0`. The
segments from `s'` to the fibre of `w` are indexed by `n` in `Z^2`.

- A fixed blocking point exists only if `a`, `b` have the same sign, at
  parameter `b/(a + b)`, and only for `n` in `(a + b) Z^2`. It's the
  Hubert-Schmoll-Troubetzkoy and Lelievre-Monteil-Weiss mechanism (CITED).
- Every other segment misses `L` for generic `s'`. It must end at a lift of
  `w` outside the component. This is a monodromy condition, with no blocker.
- So in every family two classes are dark by monodromy alone.

**Abstract examples. PROVED (short; unreviewed).**

- *Same sign.* The LMW Example 1 surfaces (CITED) have `c0 = 0` after
  rescaling the torus so that the branch locus is one point.
- *Opposite sign, no blocker.* Let `X` be the 27-square surface with monodromy
  group the Heisenberg group mod 3 acting on itself, `A`, `B` the generators,
  `c = [A, B]`. A closed geodesic through a generic point is `g^k` with `g`
  primitive in `F_2`. Its image has nonzero class in `(Z/3)^2` and order 3, so
  no power is `c`. So `(s, c s)` is dark for every `s`: relation `(1, -1)`,
  `c0 = 0`. The order-32 group `<A, B : A^4, B^4, [A,B]^2, [A,B] central>`
  gives the same with a central involution.

So Theorem X is sharp on abstract surfaces. The hidden structure is a
correspondence on `M` that no cylinder core curve detects.

**Hubert-Schmoll-Troubetzkoy slice (attack 3).** An HST family is a surface
with `(a, b) = (1, 1)`, `c0 = 0`. A room family with `rho = -1` would be a
line on such a surface for `e1 = 1`, with the lattice midpoints that occur all
at vertices. The other two classes are of type `(1, -1)` and need the
monodromy mechanism. Rooms with every lattice point a vertex exist ("plus
trees": plus-shaped pentominoes joined at arm tips, centres on `(2Z)^2`
forming a tree). In them the first half is automatic for pairs
`T = S + (2i, 2j)` on integer heights of equal parity. The second half fails
in every case computed (Section 5).

**Mirror rooms. PROVED.** For a room with mirror `R`, the graph of the
translation automorphism `mu(S, e) = (R S, (-e1, e2))` isn't dark: a row
that crosses the axis joins `s` to `mu s`.

## 5. Rational members and the search (attack lines 2 and 4)

**No arithmetic contradiction from blocking. PROVED.** For rational `x` the
pair is a dark lattice pair of a scaled room. In the two monodromy classes no
segment of the family needs a lattice point: the segments are unblocked and
end at the wrong lift. So large denominators and primitive segments give no
contradiction. The 22-wall room has no family (CITED: one real dark pair).

**Search. COMPUTED.** `search.py` lists every family that Corollary X allows:
all heights `y0`, `v0`, all `k`, one rational sample `x = i + (r + 37/101)/|a|`
in each interval where no lift meets `L`. A family that is dark at one
irrational `x` is dark on the whole interval (d16 Theorem 1, item 3 and its
remark), so one lit sample kills the interval. The tracer uses exact integers
and treats a path through any lattice point as blocked, so "lit" is sound.

| Rooms | Slopes `(a, b)` | Samples | Unlit at radius 8 | Unlit at radius 14 |
| --- | --- | --- | --- | --- |
| 13,384 fixed polyominoes, area 2 to 9 | `(1, ±1)` | 2,289,494 | 0 | not needed |
| 256 plus trees, 1 to 6 centres | `(1, ±1)` | 333,996 | 650 (96 rooms, all 6 centres) | 0 |
| 90 fixed polyominoes, area 2 to 5 | 12 slopes, `max <= 3` | 571,452 | 0 | not needed |

Radius `R` means images `D_e T + 2(m, n)` with `|m|, |n| <= R`. Fixed
polyominoes include all transposes, so "after exchanging axes" is covered.
Tracer checks: three paths found by hand (a square, two plus trees).

Commands, from this directory:

```sh
python3 search.py poly 9
python3 search.py plus 6 > run_plus6.txt
python3 recheck.py run_plus6.txt 14
python3 search.py polyother 5
```

## 6. Exact obstruction that remains

**OPEN.** Does a strictly simple orthogonal lattice room have a real line of
pairs on which two components of `{a pi(s') + b pi(t') = 0}` and two of
`{a pi(s') - b pi(t') = 0}` are all M-dark? Two of the four must be dark by
monodromy alone. Abstract surfaces allow each surface separately. The
unused hypothesis is that `M` is a room unfolding: `M/K` is a disc, `tau`
fixes exactly `VM`, and convex corner lifts are regular blockers.

Not covered: rooms of area above 9 (except plus trees), and slopes with
`max(|a|, |b|) >= 2` in rooms of area above 5. No bound on `(a, b)` for a
given room is known, so the search can't be made exhaustive per room.

## 7. Weakest steps

1. Theorem X is unreviewed. Check Step 2 first (the loop around a `B_w` point
   projects trivially on the first factor) and the claim that `N`-orbits are
   the `q`-fibres.
2. The search trusts a tracer checked on three hand cases. A wrong "lit"
   would hide a family.
3. The abstract examples in Section 4 are proved in a few lines and
   unreviewed. Nothing else depends on them.
