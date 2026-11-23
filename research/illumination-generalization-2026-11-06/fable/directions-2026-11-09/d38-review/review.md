# Referee report on d35, d36, and d37

Independent referee, 2026-11-12. Targets: `../d35-aw-torus/astra.md`,
`../d36-amalgamation/astra.md`, `../d37-visibility/astra.md`. I read STATE.md
for definitions only and formed the verdicts below before reading the
coordinator's summaries of d35 to d37. Nothing here is refereed or formalized.

Computation: `check_named.py` and `check_named.log` in this directory. It runs
on the 22-wall room, P6 (both the d36 construction and `found.json[0]`), and
the d37 L-room only. Total CPU time is under 0.01 seconds. It computes the
canonical partitions and the three basic arc graphs. It runs no ray,
direction, or reflection-word search and no decider. One further check, on the
12-wall cross, was done by hand from the cell permutations (section 4).

## Verdict table

| Claim | Verdict |
| --- | --- |
| d35.1 Apisa-Wright conclusion is vacuous on lattice pairs | CORRECT |
| d35.2 Rational points are dense and periodic, so no finite exceptional set | CORRECT |
| d35.3 Finite modular orbit reduces illumination to horizontal tests | CORRECT |
| d35.4 Two distinctions (invariant partition vs. cover; fibre tracking) | CORRECT |
| d35.5 `DP / B_x` has no regular point over `x`; `B_*` is the join | CORRECT |
| d35.6 `u = 2n - 2r - 2` | CORRECT |
| d35.7 Cylinder certificate | CORRECT, wording gap |
| d35.8 Amalgamation needs geometry (`12|34` vs `13|24`) | CORRECT |
| d36.1 `Deck(DP/PC) <= V4` | CORRECT |
| d36.2 No two classes with different canonical double covers | CORRECT (duplicates d10 R6) |
| d36.3 Galois amalgamation | CORRECT, narrow |
| d36.4 Area bound `n <= 5r` with corners in at least 3 classes | CORRECT |
| d36.5 Normalization gives at least 3 corner classes | CORRECT WITH GAP (scope) |
| d36.6 Checks on the two dark rooms | CORRECT (reproduced) |
| d37.1 Regular lift graph characterizes directional joins | CORRECT WITH GAP (wall marks) |
| d37.2 Affine averaging lemma | CORRECT WITH GAP (wall marks) |
| d37.3 Consequences of the averaging lemma | CORRECT |
| d37.4 Every regular x-component lies in one fibre of `phi_x` | CORRECT (paths and cycles) |
| d37.5 Conditional theorem under joint majority | CORRECT as an implication; hypothesis is FALSE at r = 4 (12-wall cross) |
| d37.6 L-room example | CORRECT |
| d37.7 Cone-count bound on path components | CORRECT |
| d37.8 Any proper `N_x` gives `n <= 5r`; area > 5r is certificate-free | CORRECT WITH GAP (same scope gap as d36.5) |
| d37.9 Checks on the two dark rooms | CORRECT (reproduced) |

## Most serious problem

The d37 "classwise joint-majority hypothesis" is not a weaker hypothesis. It is
the per-class same-fibre statement in disguise, and that statement is false at
`r = 4`.

1. The hypothesis lets you choose the subgroup. Choose the trivial subgroup.
   Its orbits are singletons, and the density inequality for `{p}, {q}` says
   that one component contains both `p` and `q`. So the hypothesis holds if and
   only if, for every class `x`, every two regular A points in one fibre of
   `phi_x` are joined by a trajectory of class `x`. The averaging lemma only
   makes that statement cheaper to verify. The conditional theorem is then the
   contrapositive of a definition.
2. The 12-wall cross refutes that statement. Take `S = (1,2)`, `T = (3,2)` with
   class origin `S`, as in d10 R4. By hand, `B_c` is the one-block partition:
   the seed `B1 ~ C2` (star of `(2,1)`) gives `B1 ~ R2` under `g_a` and
   `B2 ~ R1` under `g_b`, and three more steps merge all 12 cells. So all four
   lift pairs share the one `phi_c` fibre. But all four lift pairs carry a Cut
   certificate at `c` (`../d10-d12-review/room_r4.log`: certificates
   `['', 'C', 'P']`), and Theorem U (confirmed in d10-d12-review) makes them
   c-dark. The cross is strictly simple, normalized, `r = 4`.
3. The d10 census already pointed this way: 51 abstract dark pairs need Rig
   and 54 need Cut (`../d10-mechanisms/theory.md`, section 2.4). Those
   certificates live inside one `B_x` fibre.

Consequences. The hypothesis can't be derived from `r <= 8`. The "genuine
conditional solution" in d37 is not progress toward the target. Any repair
must read "joint majority, or a Cut or Rig certificate, at each class". The
proposed next step mentions Rig and omits Cut. The d37 probability estimate
rests on the unrepaired version.

## d35: notes per claim

**d35.1.** Lattice marks of one class map to the same pole of `PC`, which is a
fold of the required kind. Both endpoints are periodic. The conclusion is
vacuous, as stated.

**d35.2.** On a square-tiled surface, points with rational coordinates are
periodic (Gutkin, Hubert, and Schmidt, 2003). They are dense, so there is no
shortest saddle connection among periodic points.

**d35.3.** A segment between lattice lifts has an integer displacement. Some
matrix in `SL(2,Z)` makes it horizontal. The orbit of the marked half-translation
surface is finite because the square count and the marking denominators are
fixed. Straightness and corner avoidance are affine-invariant, so the walls
don't need to be tracked.

**d35.4, d35.5.** These are definitional. If `B_x` has a regular point `y`
over `x` in the quotient, its preimages have local degree 1 and are regular
upstairs, but `B_x` gives every regular `x` point local degree 2.

**d35.6.** Fibre sums over the four poles: `4n = (r+4) + 3r + 2u`. Riemann-Hurwitz
then gives genus 0 for `DP`, as it must.

**d35.7.** A straight segment between two points of an open flat cylinder stays
inside it, and the open cylinder has no cone points. The statement should say
"a lift of `S` and a lift of `T`". Two lifts of one endpoint prove nothing about
the pair. "C-free" is needed on the translation double cover, where convex
corners become removable points. On `DP` it's automatic.

**d35.8.** Correct as a remark. The example `12|34`, `13|24` is the regular
`V4` configuration, which d36 later excludes in rooms. So it shows only that
abstract invariance is not enough.

Notation: d35 uses `C` for the corner set and d36 uses `C` for the seam.

## d36: notes per claim

**d36.1.** Checked step by step. Deck transformations are holomorphic
isometries. The seam is the fixed circle of the antiholomorphic involution
`iota`. `j(C)` and `C` are circles that share all `2r + 4 >= 4` cone points, so
they are equal, and two antiholomorphic involutions with one fixed circle are
equal. The descended maps have the form `+-z + 2v` or `+-zbar + 2v`.
Boundedness leaves a half-turn and two reflections about one integer point.

**d36.2.** Checked case by case. For a Galois `phi_x`, local degree equals the
stabilizer order, so every regular `x` point is fixed by the involution. The
diagonal class has no fixed lattice point. The midpoints `O +- (1,0)` always
have fan size 2 or 4 by symmetry, so they are never corners. The two-class
cases reduce to the `2 x 2` block. This duplicates d10 R6, which
d10-d12-review confirmed.

**d36.3.** The join of orbit partitions is the orbit partition of the generated
group, and subgroups of `V4` with no two distinct order-2 members form a chain.
Scope: a proper Galois `B_x` needs a symmetry of `P` that fixes every
transparent `x` point. Asymmetric rooms satisfy the hypothesis only with every
`B_x` discrete, where amalgamation is trivial. So the result covers symmetric
rooms only.

**d36.4.** Rederived. Target cone angles are in `{pi, 2pi, 3pi}`, Gauss-Bonnet
gives `p = z + 4`, and `w_j = p_j + 3 z_j` satisfies `w_j = d (mod 2)`,
`sum w_j = 4z + 4`, and `w_x = d`. Corners map to singular points, so at least
two off-`x` weights are positive. That gives `d <= 4z + 1`, `z >= 1`, and
`delta z <= r`, so `n <= 4r + r / z <= 5r`. Separation is used only for `d >= 2`,
as d37 notes. The hypothesis is necessary: the d37 L-room has one corner class,
`n = 12 > 5r = 5`, and a proper `B_b` with `z = 0` and `delta = 6`
(`check_named.log`).

**d36.5.** The implication is correct: an odd horizontal wall and an odd
vertical wall give two corner pairs that one 2-element set can't hold. The gap
is scope. Normalization is not without loss of generality for lattice marks.
Halving a room moves marks off the lattice. d16 reduces real pairs to rational
pairs with unbounded denominators, and an even refinement of the lattice puts
every corner in one class, where the bound fails and d10 R1 fails. Odd
refinements keep the bound. So "a normalized counterexample has area 21 to 40"
is right, and it says nothing about marks with even denominators. The
STATE.md wording "any amalgamation counterexample at r <= 8" overstates d36.
The whole d35 to d37 programme also treats same-class marks only. Pairs of
different classes are left to Rig (d10, Theorem U) and are not discussed.

**d36.6.** Reproduced: 22-wall room `B_b = B_d` with 5 blocks and
`delta = 3`, `B_c` discrete (class c has no transparent point); P6 all three
with 5 blocks and `delta = 4`; all separate; all `R_y` are one block; the
22-wall quotient has a `(2,1)` pole fibre, so it is not Galois. I did not
recompute the full deck groups.

## d37: notes per claim

**d37.1.** Correct for interior marks. At a regular vertex the two arc lifts
are opposite, so following edges is straight continuation. Gap: an edge can lie
on the seam (a trajectory sliding along a wall). A component that contains one
seam edge lies on one wall line between two corners, so it never contains an
interior lift. But `V` includes regular A points on walls, and d37 states
"every pair in `V` illuminates", which then includes wall-sliding paths. Fix:
restrict `V` to interior lifts or exclude seam edges.

**d37.2.** Correct. Affine automorphisms of `DP` preserve cone points, map
straight segments to straight segments, and map primitive directions to
primitive directions. Derivatives that fix the class keep the class. A pulled-back
segment with an interior endpoint can't run along the seam, because a geodesic
that overlaps the seam stays on it until a corner. The wall-mark gap from d37.1
carries over.

**d37.3.** The three corollaries and the orbital-graph refinement follow from
d37.2.

**d37.4.** Correct for paths and cycles. A regular `x` point maps to a pole of
`N_x`, local degree 2. A pole of `N_x` has one incident arc lift, so both
neighbouring A points map to its other end. Induction along consecutive A
vertices covers a cycle as well as a path. This is the Par soundness argument
of d2, section 1.3, read backwards. The log confirms it on the three basic
graphs of all named rooms.

**d37.5.** See "Most serious problem".

**d37.6.** Checked by hand. Horizontal cylinders have circumferences 8 and 4
and heights 2 and 2, so shear 4 is a multitwist. At height 1 it moves the
bottom cylinder by 4 of 8, giving `(s+ t-)(s- t+)`, and the top one by 4 of 4,
fixing `u+-`. The derivatives are congruent to `I` mod 2. The orbits are
`{s+, t-, u-}` and `{s-, t+, u+}`. The log confirms the horizontal component
of size 4. Example: `vh` sends `(s+, u-)` to `(t-, s+)`, both in `C`, and the
pull-back has direction `(17, -4)`, which has horizontal parity. The room is not
normalized (one corner class), so it does not test d37.8.

**d37.7.** Each path component has two missing incidences, and the corner
incidences over A and `x` total `w_A + w_x <= 4r + 4`. The bound is correct.
d37 uses `p_x` for both poles and path components.

**d37.8.** `R_y` is coarser than `B_y`, so a one-block `B_y` forces a one-block
`R_y`. With d10 R3 this excludes every Par and Rig certificate, not only the
canonical ones. Cut is excluded for interior marks by d10 R4. The fibre bounds
(at most 8 points, at most 4 over a pole) are correct. The scope gap is the one
in d36.5.

**d37.9.** Reproduced: 22-wall fibres `3 + 3`, P6 fibres `4 + 4`, basic
components of size at most 2.

## Other questions

**Is joint majority weaker than the target?** No. It is equivalent to the
per-class all-pairs statement in item 1 above. That statement is stronger than
the target in two ways: it requires illumination within class `x`, and it
covers every pair in a fibre, not only dark candidates. It is false on the
12-wall cross. Fixing a nontrivial subgroup in advance only makes it stronger.

**Contradictions with the dark rooms or earlier results?** None with the
22-wall room or P6: both have `n <= 5r` and per-class Par certificates, and the
fibre lemma holds on their basic graphs. d36.2 agrees with d10 R6. d35 to d37
agree with d2-review (`N_min = PC` in the open cases), d15 (`r <= 2` gives
`n <= 10`), and d16. The one conflict is d37 against d10 R4 and the confirmed
cross certificates: those show the d37 hypothesis fails. d37 never mentions
Cut.

## Not checked

- The d9 census totals that d36 cites.
- The deck groups of the two full pillowcase covers.
- The 12-wall cross by script; `B_c` there is a hand computation, and the Cut
  certificates come from the reviewed d10-d12 log.
