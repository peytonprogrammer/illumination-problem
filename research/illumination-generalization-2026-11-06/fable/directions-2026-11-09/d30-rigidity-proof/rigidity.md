# Rigidity for rooms with a run: what holds, what fails

Date: 2026-11-10. Direction d30. Nobody has reviewed this document.

Tags: **PROVED** (proof here, one session, unreviewed), **CITED** (project
files, not re-derived), **CHECKED** (exact computation, scope stated),
**OPEN**.

## 1. Answer

- The rigidity conjecture for `W <= 20` is **OPEN**. This document doesn't
  prove it and doesn't refute it.
- Without the wall bound the conjecture is false. Room `P6` (Section 3) is a
  strictly simple orthogonal lattice room with `W = 28`, `r = 12`, a run of
  height 2, and a dark same-class interior pair strictly outside the run
  rows. **PROVED**, with a bounded trace as a sanity check (**CHECKED**).
- So a run of height 2 alone never implies lit. A proof for `W <= 20` must
  use `r <= 8` quantitatively. Soft versions of attacks 1 and 3 can't work.
- Two sub-claims of attack 2 are false: "a run forces `k >= 7`" (`P6` has
  `k = 6`), and "a run is incompatible with the factor-cover mechanism"
  (`P6` is a 4-fold cover of the staircase double, the factor of the 22-wall
  room).
- Partial theorem (Theorem R, Section 4, **PROVED**, no wall bound): a
  non-trivial parity factor forces reflex corners next to the run. A run of
  height `g >= 3` has no parity factor other than the unit pillowcase `PC`.
  Height 3 is sharp: `P6` has height 2.
- For `r <= 8`, rigidity equals the same-fibre conjecture restricted to rooms
  with a run (Section 5). That lit-side statement is the exact obstruction.

## 2. Conventions

These follow `d2-factor-audit/audit.md`. `DP` is the double of `P`. A
*parity factor* is a factorisation `DP -> N -> PC` of the fold map, by
branched covers that are local isometries off cone points, in which no
lattice point of `N` of a non-A class is regular. A is the class of `S` and
`T`. `N` has cone angles `pi` (pole), `2 pi`, `3 pi` (zero) only. Over a zero
every point of `DP` is a reflex corner with local degree 1. Over a pole a
point of `DP` is a convex corner, a transparent point (local degree 2), or a
reflex corner. **CITED** (audit 1.1).

Fold-back lemma (**CITED**, audit 1.3; the review re-checked it): if
`phi: DP -> N` is a parity factor and `phi(S~)` is not in `phi(lifts of T)`,
the pair is dark. Reason: a witness passes lattice points `x_0 = S~, x_1,
...` in steps of one primitive vector. Odd-index points have a non-A class,
so their images are poles (a zero would make `x_j` a reflex corner). A
geodesic through a pole folds back, so `phi(x_2j) = phi(S~)` for every `j`,
and `T~` sits at an even index.

## 3. The obstruction: a dark room with a run, W = 28

### 3.1 Mirror doubling

**Lemma M (PROVED).** Let `R` be a strictly simple orthogonal lattice room,
`e` a wall of `R` on a line `l`, with `R` on one side of `l` and
`R ∩ l = e`. Let `rho` be the reflection in `l` and `P = R ∪ rho(R)`. Then:

1. `P` is strictly simple. The two cell rows next to `l` are identical, and
   `l` meets no vertex of `P`. So `P` has a run of height 2 on `l`.
2. The fold `P -> R` induces a degree-2 branched cover `DP -> DR`, branched
   at the two ends of `e`.
3. Every parity factor `DR -> N` gives a parity factor `DP -> DR -> N`. If it
   separates `S` from `T` in `R`, the pair `(S, T)` is dark in `P`.

*Proof.* (1) `R` and `rho(R)` meet in `e` only. The ends of `e` are convex
corners of `R` (`R` lies on one side of `l`), so they are flat points of `P`.
No other point of `P` lies on `l`. Rows next to `l` are mirror images of each
other and each is the single chord over `e`. (2) Send the front of `R` to the
front of `DR`, the front of `rho(R)` to the back by `rho`, and the reverse
for the back sheet. This is a local isometry except at the ends of `e`, where
angle `2 pi` covers angle `pi`. (3) The parity property concerns `N` only.
The fold-back lemma gives darkness. ∎

### 3.2 The room P6

`Q` is the five-square staircase: cells `(0,0), (1,0), (1,1), (2,1), (2,2)`
(cell `(i,j)` is `[i,i+1] x [j,j+1]`). `W = 10`, `r = 3`. Its 12 lattice
points are 10 corners plus `S0 = (1,0)` and `T0 = (3,2)`, both of class
A = (odd, even). So every non-A lattice point of `Q` is a corner and `DQ` has
the parity property. **PROVED** (by listing). `DQ` is the factor of the
22-wall room (**CITED**, d4).

`Q` has four walls that join two convex corners: `e_B` (bottom, length 2,
midpoint `S0`), `e_R` (right, length 2, midpoint `T0`), `e_L` and `e_T`
(unit length). Gluing a reflected copy across such a wall keeps the fold map
to `Q` well defined.

`P6` is the union of four copies:

| Copy | Definition | Cells |
| --- | --- | --- |
| `Q0` | `Q` | `(0,0) (1,0) (1,1) (2,1) (2,2)` |
| `Q1` | `Q0` reflected in `y = 0` (across `e_B`) | `(0,-1) (1,-1) (1,-2) (2,-2) (2,-3)` |
| `Q5` | `Q1` reflected in `x = 3` (across its `e_R`) | `(5,-1) (4,-1) (4,-2) (3,-2) (3,-3)` |
| `Q0'` | `Q0` reflected in `y = 3` (across `e_T`) | `(0,5) (1,5) (1,4) (2,4) (2,3)` |

**Proposition 1 (PROVED; CHECKED by `mirror_check.py`).**

- `P6` is strictly simple, with 20 cells, `W = 28`, `r = 12`, `k = 6`.
- The rows `2 < y < 3` and `3 < y < 4` are both the single cell
  `2 < x < 3`. The line `y = 3` meets `P6` in the flat points `(2,3)` and
  `(3,3)` only. So `P6` has a run of height 2 (a width-1 corridor).
- `S = (1,0)` and `T = (3,-2)` are interior points of class A. They lie at
  distance 2 or more from the run rows.
- The fold map `DP6 -> DQ` is a degree-4 parity factor with `phi(S) = S0`,
  `phi(T) = T0`. `S0` and `T0` are boundary points of `Q`, so each is one
  point of `DQ`, and they differ. By the fold-back lemma `(S, T)` is dark.

Checks run (`python3 mirror_check.py 30`, under 1 minute, 1 process):
strict simplicity, wall count, fold-map consistency, the run, and an exact
trace of every lattice chain from `S` with `|q|, |p| <= 30`: no witness.
The trace is a sanity check; the proof is the fold-back lemma.

### 3.3 The gap line through P6 (CHECKED, same script)

Vary the height `g` of the run (`g = 2` is `P6`):

| `g` | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Witness `(q, p)` | `(5,6)` | `(5,14)` | none, dark | `(3,-20)` | `(6,11)` | `(3,28)` | `(3,8)` |

So the dark locus on this line contains the isolated gap `g = 2`, and the
all-gaps-1 specialisation is lit. Consequences:

- "Dark implies dark after shrinking every gap to 1" is false at `W = 28`.
  No argument that ignores the wall bound reduces minimality to a box of
  bounded size.
- By Proposition 3 of d28, no witness with `p <= P` exists at
  `g = 2 (mod Q_P)` on this line. Witness numerators are unbounded there.
- Lemma B of d28 transports a witness between `g` and `g - 2` only for
  directions `(L m, 1)` and the vertical one. That is why attack 4 gives
  nothing at `g = 2`: the witnesses at `g = 0` and `g = 4` above have
  `p = 6` and `p = 11`.

Smaller examples with a weaker position hypothesis exist: five copies with
`W = 34` where `S` lies on the boundary line of the run. Whether a dark room
with a run exists for `22 <= W <= 26` is **OPEN** (three copies of `Q` never
give one; other targets `N` were not examined).

## 4. Theorem R: what a run forces on a parity factor

Setting. `P` has a run on `y = c` (any `W`). Fix a chord `[a, a+w]` of the
run rows. Let `phi: DP -> N` be a parity factor. Unfold the chord's band:
`Sigma = R x (c-1, c+1)` maps to the band cylinder of `DP` by folding `x`
at the chord walls, and `Phi: Sigma -> N` is the composite. Integer points
of `Sigma` are lifts of lattice points; folding preserves the parity of `x`.
Every lattice point on `y = c` is transparent.

**Lemma 1 (continuation, PROVED).** If `x` in `Sigma` is a lift of a
transparent non-A point, `Phi(z) = Phi(rho_x z)` for all `z` in
`Sigma ∩ rho_x(Sigma)`, where `rho_x` is the rotation by `pi` about `x`.

*Proof.* `Phi(x)` is a pole with local degree 2, so the two germs agree at
`x`. The set where the germs of `Phi` and `Phi o rho_x` agree is open. It is
closed: at a point over a regular point of `N` both maps are `+-z + const`
in a chart and agree on a sequence of open sets; at a point over a pole a
local isometry of degree 2 that respects the horizontal foliation is unique.
The domain is convex. ∎

**Theorem R (PROVED).** Suppose `N != PC`.

- (O) If `y = c` carries no A point: `Phi` factors through the half-pillow
  `H_1` (a disc of circumference 2 and radius 1 with two poles). Its
  boundary loop carries one A point and one point `p_C` of the other class
  of the lines `y = c +- 1`. `p_C` is a zero of `N`. So every non-A lattice
  point on the closed segments `[a, a+w] x {c-1, c+1}` is a reflex corner
  of `P`.
- (E) If `y = c` carries A points: `Phi` factors through `H_2`
  (circumference 4). The loop carries four non-A points `b_0..b_3`. At most
  one is a pole of `N`; the others are zeros. So the lattice points on
  `[a, a+w] x {c-1, c+1}` are reflex corners, except possibly those over one
  `b_i` (one residue class modulo 4 in the unfolded coordinate, mirrored
  between the two lines).
- (Height 3) If the run has height `g >= 3`, `P` has no parity factor other
  than `PC`. So `N_min = PC`, with no wall bound.

*Proof.* (O) Every integer point of the line `y = c` is a lift of a
transparent non-A point. By Lemma 1, `Phi` is invariant under all `rho_j`,
so under translation by 2, and factors through `Sigma / <rho_j> = H_1`. The
map `H_1 -> N` is a local isometry on the open disc. The loop is the image
of `y = c + 1` (identified with `y = c - 1` by `rho`); it has length 2 and
two lattice points, of classes A and non-A. `p_C` is non-A, so it's a pole
or a zero. Suppose it's a pole. The band side of `p_C` is a sector of angle
`pi` in a cone of angle `pi`, so its two boundary rays coincide. The two
loop arcs from `p_C` are unit geodesics from one point in one direction with
no cone point inside, so they coincide up to the A point. There the band
sector has angle `pi` with both rays identified, so the cone angle is `pi`
and the sector fills it. The image of the closed band is then open and
compact, so it equals `N`, and `area(N) <= 2 = area(PC)`. Then `N = PC`, a
contradiction. So `p_C` is a zero, and points of `DP` over a zero are
reflex corners.

(E) Only the points `x_0 + 2Z` of the line are known poles. `Phi` factors
through `H_2`; the loop has length 4 with `b_i = Phi(x_0 + i, c + 1)`, all
non-A. If `b_0` is a pole, zipping as above gives `b_1 = b_3`. If that point
has angle `pi`, the sectors wrap, the next arcs coincide, `b_2 = b_0`, and
the image closes up with area at most 2: `N = PC`. Otherwise `b_1 = b_3` is
a zero. Then if `b_2` were also a pole the image would close up with
`b_1 = b_3` regular, against the parity property. The cases starting from
`b_1`, `b_2`, `b_3` are the same up to relabelling.

(Height 3) Two adjacent lines `y = c`, `y = c + 1` are vertex-free with
identical rows around them. One of them carries no A point; apply (O) to it.
The other line is adjacent, vertex-free, and its closed chord segment holds
`w + 1 >= 2` consecutive lattice points, so a non-A point that isn't a
reflex corner. Contradiction. ∎

Checks against known rooms (**PROVED** by inspection):

- `P6`, line `y = 3`, case (O): the non-A points on the adjacent segments
  are `(2,2)` and `(2,4)`, both reflex. Consistent, and it shows the reflex
  condition can't be dropped.
- `Q0 ∪ Q1` (10 cells, `W = 16`), line `y = 0`, case (E): `b_0 = (0,1)` is
  a pole (convex corner), `b_1 = b_3 = (1,1)` and `b_2 = (2,1)` are zeros.
  Case (E) with one pole occurs.

Corollary (**PROVED**): in case (E) with `w` even, case "all reflex" is
impossible (the cells above the segment would have to alternate and both end
cells be present, which needs `w` odd).

## 5. Status for W <= 20 and the exact obstruction

- **CITED** (d2 audit and review, with the computer-assisted `k <= 6`
  theorem): for `r <= 8` no parity factor separates two interior A points.
  So for `r <= 8`, every interior A pair is a same-fibre pair, and rigidity
  is the same-fibre conjecture restricted to rooms with a run.
- Theorem R removes the dependence on the `k <= 6` certificates for the
  factor side when `g >= 3` or when a non-reflex non-A point sits next to
  the run. It says nothing on the lit side.
- **OPEN, the exact obstruction:** a lit-side existence statement. You need
  a witness for every same-fibre pair, and at gaps congruent to a blocked
  specialisation the witness numerator `p` is unbounded (d28, Proposition
  3). `P6` shows the blocked specialisation can be `g = 2` itself once
  `r >= 12`. For `r <= 8` the only known blocked specialisations are slit
  degenerations (`g = 0`); no theorem excludes others.
- What a proof for `W <= 20` must use: `r <= 8` in a way that fails at
  `r = 12`. The only such inputs in the project are the Riemann-Hurwitz
  count `delta * z_N <= r` and the `k <= 6` census theorem.

## 6. Attacks tried

| Attack | Outcome |
| --- | --- |
| 1. Cylinder twist | No contradiction available: in `P6` the band cylinder has height 2 and the pair is dark. A twist argument would have to see `r`. |
| 2. Factor structure | "`k >= 7`" false; "run incompatible with factors" false for `g = 2`, true for `g >= 3` (Theorem R). Reduction to same-fibre holds (Section 5). |
| 3. Direct optics through a band point `X` | In `P6` every chain through the band points `(2,3)`, `(3,3)` folds back in `DQ`. Free horizontal visibility in the band gives no witness. |
| 4. Degeneration | Lemma B links `g` and `g - 2` in directions `(L m, 1)` only. `P6` is dark at `g = 2` and lit at `g = 0, 1, 3..6`. |

## 7. Weakest steps

- Theorem R and Lemma 1 are one-session hand proofs. The step most worth a
  second reader is the zip argument in case (E), where the map `H_2 -> N`
  need not be injective.
- Darkness of `P6` rests on the cited fold-back lemma and on the listing of
  lattice points of `Q`. The trace to `|q|, |p| <= 30` is not a proof.
- The tracer in `mirror_check.py` is new and has no second implementation.
  The lit verdicts at `g != 2` in Section 3.3 depend on it. A lit verdict
  can't be a false positive of a truncated search, but it can be a tracer
  bug.
- Section 5 inherits the unreplayed `k <= 6` certificates.

## 8. Files

- `rigidity.md`: this file.
- `mirror_check.py`: builds `P6` from copies of `Q`, checks simplicity,
  walls, the run, the fold map, and traces lattice chains.
  `python3 mirror_check.py 30`.
