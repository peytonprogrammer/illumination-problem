# d52: fold enumeration, a second proof of the d46 result at r <= 8

Opus 5.5 subagent, 2026-11-15. No room enumeration, ray search, direction search, or
reflection-word search was run. All code is new and shares nothing with d4, d6, d10,
d44, or d46.

Tags: **PROVED** (argument here), **CITED** (file and line), **COMPUTED** (script and
log here), **GUESSED**.

## Summary

- **Result: the independent proof succeeds at r <= 8.** It has the same cited
  hypotheses as d46 (F\* and the d39/d43 reduction). It finds 0 positives, matching
  d46. It covers every area and every immersed disc W-set, not only areas 21 to 40
  and embedded rooms.
- **The brief's premise was wrong, and the method was changed.** F\* forces only
  *one* class quotient to have delta >= 3. The other two can have delta = 1
  (N_y = DP itself) or delta = 2. The 22-wall room has delta_c = 1. So no finite
  list of quotient triples exists a priori. Instead, the search enumerates the one
  small quotient N_x and then all of its degree-delta covers DP. That is the bounded
  "search over common covers" the brief allowed for.
- **Quotient shapes (task 2), COMPUTED.** At r <= 8, 106 admissible shapes K_x have
  the target class fixed to x = (0,0). That's 56 shapes modulo the V <-> H mirror.
  They have d from 3 to 9 and z in {1, 2}. Of the 106, 63 have an interior pi-cone.
- **Covers (task 3), COMPUTED.** The search covers 185 (K, delta) cases. It finds
  4,710 genus-0 covers (W-set discs) with r <= 8, and 4,541 of them have corners in
  >= 3 classes. Up to lattice isometry that's 1,744 discs, of which 1,113 are
  strictly simple rooms. **0 positives.** No mark pair is separated in all three
  classes. The best is 2 of 3 (8 pairs).
- **Sanity (task 5), COMPUTED.** At r = 9 the method classifies all positives that
  have a delta >= 3 class. There's exactly one room up to lattice isometry: the
  22-wall room, with its one known pair. At r = 12, P6 appears over its own quotient
  (delta = 4). The only other positive cover of that quotient is a slit ring, which
  is not a room.
- **Compute:** about 30 CPU-minutes in total, at most 2 processes at once, under
  200 MB of RAM, and 0.8 MB of files.

## 1. Constraints on a class quotient N_x (task 1)

The setup: P is a strictly simple orthogonal lattice room with r reflex corners and
corners in >= 3 parity classes. S and T are interior lattice marks of one class a.
"Positive" means each of B_b, B_c, B_d separates all four lift pairs.

| # | Constraint | Status and source |
| --- | --- | --- |
| C1 | N_x is a sphere. Points over corners are poles (cycle 1), regular (2), or zeros (3). p = z + 4. | CITED: `d36-amalgamation/astra.md:66-71`; Fact L, `d10-mechanisms/theory.md:47-62` |
| C2 | N_x = DP / B_x has no regular point over x. Par(x) holds for some factor iff B_x separates. B_x is iota-invariant, so N_x is the double of a fold target K_x = N_x / iota. | CITED: R3, `d10-mechanisms/theory.md:316-326`; Par definition `:182` |
| C3 | Zeros of N_x lie on the seam. | CITED: `d43-review-d39/review.md:88-91`, `d39-mixed-class/astra.md:67` |
| C4 | There's at most one off-seam conjugate pair of poles (an interior pi-cone of K_x). A cone forces delta even. | PROVED: the argument of `d39-mixed-class/astra.md:69`, which uses only Fact L and Riemann-Hurwitz, so it applies to B_x |
| C5 | Each zero of N_x has exactly delta preimages, all reflex corners of its parity class. So delta * z <= r. | CITED: `d45-review-fstar/review.md:79-95`, `d36-amalgamation/astra.md:94` |
| C6 | F\*: a positive at r <= 8 has some class x with delta_x >= 3. | CITED: `d44-cert-check-sizing/README.md:67-80`, verdicts `d45-review-fstar/review.md:20-27, 64-73`. Rests on d36.3 and d2 claim 4 (`d2-review/review.md:20-27`). d2 claim 4 uses the computer-assisted k <= 6 theorem. |
| C7 | A full ordinary certificate triple reduces to three Par separations. | CITED: `d39-mixed-class/astra.md` claims 2-4; `d43-review-d39/review.md:169-182`. Uses the d9 census (area <= 20) for essential Rig. |
| C8 | B_x separates all four lift pairs iff S and T have distinct images in K_x. | PROVED: lifts of distinct points of K_x are disjoint. One point's two lifts cover both lifts of every point that maps to it. |
| C9 | Every <V_i, H_j>-orbit of K_x is one of 5 types: convex corner, smooth boundary point, reflex corner, interior pi-cone, or interior regular point. "No regular point over x" means class x has only convex corners, reflex corners, and the cone. | PROVED from C1 to C3. A dihedral path of length L gives a g-cycle of length L, so L <= 3. A cycle of 2k cells gives two k-cycles. k = 3 is an off-seam zero pair, excluded by C3. |
| C10 | d = p_x + 3 z_x + 2 cone_x <= p + 3z = 4z + 4. | PROVED from C2 and C9. The search uses this, not d36.4's d <= 4z + 1. |
| C11 | Singular points of N_x lie in >= 3 classes (filter K2). | PROVED: corners of P map to poles or zeros (Fact L). |
| C12 | Two distinct non-reflex class-a points are needed in K_x (filter K4). | PROVED from C8. Reflex points of K have no regular preimage. |

Nothing in the list is GUESSED. The step a referee should check first is the cover
model in section 3. It's PROVED below and validated two ways.

Not imposed: "non-Galois". The search takes every cover with delta >= 3. That's a
superset.

## 2. The quotient shapes (task 2)

`enum_K.py` runs a low-index search for transitive W-sets K (W = free product of the
four edge reflections V0, V1, H0, H1). It imposes C9, the class-x restriction, z <=
zmax, at most one cone, and d <= 4 zmax + 4. Leaves must have genus 0 (p - z = 4).
`analyze_K.py` applies C11, C12, and "some delta >= 3 with delta * z <= r, delta
even if there's a cone" (C4, C5).

COMPUTED (`logs/K_z2_d12.log`, `logs/analyze_K_r8.log`, `logs/mirror_count.log`):

- z <= 2, d <= 12: 127 genus-0 shapes in 9.5 CPU-s. 106 are admissible at r <= 8.
  The 21 rejected shapes include all 6 with z = 0. So z >= 1 needs no citation.
- No admissible shape violates d36.4's d <= 4z + 1 (d <= 4z if d is even). The
  largest d with >= 3 singular classes is 9. At z = 3 it's 13. This independently
  reproduces d36.4 and d44's "z <= 2, d <= 9".

Admissible shapes at r <= 8, modulo the V <-> H mirror (56 in total):

| d | z = 1, no cone | z = 1, cone | z = 2, no cone | z = 2, cone |
| --- | --- | --- | --- | --- |
| 3 | 2 | 2 | - | - |
| 4 | 1 | 1 | 2 | 5 |
| 5 | 1 | 1 | 4 | 6 |
| 6 | - | - | 6 | 8 |
| 7 | - | - | 4 | 6 |
| 8 | - | - | 2 | 3 |
| 9 | - | - | 1 | 1 |

Allowed delta: 3 to 8 for z = 1 (only even delta with a cone), and 3 or 4 for
z = 2 (only 4 with a cone). The full table with orbit types per class is in
`logs/analyze_K_r8.log`. The 12-wall cross's quotient is shape 0: the L-tromino,
with d = 3, z = 1.

## 3. Compatibility: why triples fail, and the cover search (task 3)

**What fails (PROVED).** Only one class needs delta >= 3 (C6). The 22-wall room has
(delta_b, delta_c, delta_d) = (3, 1, 3) (`logs/sanity.log`, matching
`d49-even-index/check_even.log`). A delta = 1 class has N_y = DP, of degree n. So
the other two quotients aren't drawn from any small list. Degree divisibility
(n = delta_y d_y), zero counts per class (C5), and Riemann-Hurwitz are only
necessary conditions. They can't decide existence. Compatibility needs DP itself.

**What works (PROVED).** Build DP as a cover of the one small quotient. Fix x =
(0,0) by translation and K = K_x. The map P -> K is a W-set map with fibres of
size delta.

- *Branching.* By Fact L, DP -> N_x branches only over poles of N_x. Over every
  other point the fibre has delta copies of the same local type.
- *Arcs.* The convex corners of K cut its boundary into arcs. Smooth points and
  reflex corners don't cut it. Over the interior of K (minus a slit when there's a
  cone), the cover is trivial. So it's given by one involution rho_A in S_delta per
  arc A. A sheet fixed by rho_A has a wall there. A swapped pair is glued across it.
- *Reflex arcs.* If rho_A swaps sheets on an arc through a reflex corner of K, the
  preimage of that corner is an interior point of angle 3 pi. A polygon has no such
  point. So rho_A = id on every arc that contains a reflex corner.
- *Cone.* Cut a slit from the cone to a reflex vertex along interior edges, through
  interior vertices only. Crossing the slit applies c, a fixed-point-free involution:
  interior points of P are regular, so every preimage has e = 2. Holonomy is c around
  the cone, c^2 = id around interior slit vertices, and trivial elsewhere. At the
  reflex end, rho = id, so the slit end is harmless.
- *Corners.* At a convex corner between arcs A and B, the <rho_A, rho_B>-orbits give
  P's points there. They must be convex, smooth, or reflex corners, or interior
  points (4-cycles with (rho_A rho_B)^2 = 1). Each reflex corner adds 1 to r.

Conversely, any such data builds a W-set over K. `enum_P.py` builds P and checks
every local type, transitivity, genus 0, r <= 8, and >= 3 corner classes directly.
It then computes B_y on P itself for all four classes, without assuming B_x = K. A
positive is any class a and interior pair S, T separated in all three y != a.

Euler's formula gives a structural remark (PROVED, not used by the code): the sheets
and the transpositions of all rho_A form a graph with delta - 1 + q edges. Here q is
the number of interior points of P over corners of K. So P is a tree of delta copies
of K, plus one 4-cycle per such point.

The search bound is delta <= 8 sheets and at most 5 free involutions. It runs as a
canonical low-index search on sheets, with each cover deduped by canonical form. The
r <= 8 run took 12 CPU-s.

**Validation of the cover model (COMPUTED).**

- `validate_generic.py` is a second, model-free enumerator. It has no arcs and no
  slit. It labels cells by K-cells and builds every W-set over K with fibres of
  size delta. It agrees exactly with the arc model on 149 cases: every case with
  delta <= 4 (all z = 2 and all cone shapes at delta 4), with 1,069 covers.
- A full pass in shape order ran until its CPU cap: 52 cases, 3,013 covers, 0
  mismatches, 1,231 CPU-s (`logs/validate_generic_all.log`). It covers every delta
  from 3 to 8 for z = 1 shapes 0, 1 (cone), 2, 6, and 18, plus shapes 3 to 17 at
  their allowed delta. Not cross-checked: delta 5 to 8 on z = 1 shapes 22, 29, 41,
  and 44. Shape 29's arc and corner structure matches shape 0's, and the arc model
  gave identical cover counts for both. Shapes 22, 41, and 44 are cone shapes, like
  shape 1, which was checked at delta 4, 6, and 8.
- `validate_brute.py` brute-forces all 13,876 immersed room W-sets with n <= 9 and
  r <= 8 with no quotient list. It recovers every (room, delta >= 3 quotient)
  incidence as a cover: 24 of 24, 0 missed. Every in-scope room whose quotient
  isn't admissible has d = 1 (`logs/validate_brute_n9.log`).
- Named rooms: both dark rooms are found over their own quotients (section 5).

**Triples that occur (COMPUTED, `logs/triples_r8.log`).** Over the 1,744 in-scope
discs, 67 distinct (delta, d, z) triples for the classes y != a occur, where a has
>= 2 interior points. Most pair one delta >= 3 class with two unit pillowcases
(d = 1), which separate nothing. Pairs by number of separating classes:

| Classes separating the pair | True rooms | Non-room discs |
| --- | --- | --- |
| 0 of 3 | 1,857 | 711 |
| 1 of 3 | 1,790 | 558 |
| 2 of 3 | 8 | 0 |
| 3 of 3 | 0 | 0 |

## 4. Result at r <= 8 (task 4)

**Theorem (COMPUTED; conditional on C6, C7, and the CITED d10 results).** Let P be
a strictly simple orthogonal lattice room with r <= 8 (W <= 20) whose corners lie in
at least 3 parity classes. Then no two distinct interior lattice points of one class
have all four lift pairs separated by each of B_b, B_c, B_d. With C7, no such pair
is dark by Par, Cut, or Rig certificates over the unit pillowcase B.

This is d46's statement. The two proofs share C6 and C7. They differ in these ways:

- d52 enumerates class quotients and their covers, not rooms. It uses neither the
  d44/d46 code, nor d36.4's area bound (it's reproduced), nor the d9 census for the
  Par step. It covers every area n = delta d, from 9 to 40.
- The no-positive part holds for every immersed disc W-set: overlapping, slit, or
  pinched, as long as its local types are room types. Only the existence of a
  delta >= 3 class comes from C6, which d2 states for strictly simple rooms.
- Same exclusions as d46: rooms with <= 2 corner classes, relative certificates,
  rational and different-class marks, and even-index bases.

No residual set remains in this certificate class.

## 5. Sanity at r = 9 and r = 12 (task 5)

COMPUTED (`logs/analyze_K_r9.log`, `logs/P_r9.log`, `logs/sanity.log`,
`logs/p6_family.log`):

- **Quotients at z <= 3.** The search returns 677 genus-0 shapes with d <= 16 in
  219 CPU-s. 291 are admissible at r = 9 (154 modulo the mirror), with d up to 13.
- **r = 9.** The search covers 12,488 disc covers (12,291 in scope). It finds 3
  positive covers, over shapes 23, 39, and 41 (d = 5, z = 3, delta = 3). All three
  are the 22-wall room up to lattice isometry, with one pair each. The 22-wall
  room's quotients for classes b and d are exactly shapes 39 and 23. Its triple is
  (N_b, N_c, N_d) = (5-cell staircase double with delta 3, DP itself with delta 1,
  the same staircase with delta 3).
- **Classification at r = 9.** Take a strictly simple room with W = 22 and corners
  in >= 3 classes. Suppose some class has delta >= 3 and an interior same-class pair
  is separated by all three B_y. Then the room is the 22-wall room, up to lattice
  isometry. This holds for any area. It also holds for immersed disc W-sets.
- **Not covered at r = 9.** The C6 and C7 inputs need r <= 8, so two branches stay
  open: rooms whose three class quotients all have delta <= 2 (amalgamation gives a
  common separating parity factor, but d2 excludes one only at r <= 8), and
  essential Rig certificates (d39's area bound is for r <= 8). So this doesn't prove
  the 22-wall room is the only certified-dark room with 22 walls. It proves this
  for the delta >= 3, pure-Par branch.
- **r = 12, P6.** Each of P6's three non-mark classes has the 5-cell staircase
  double (d = 5, z = 3) as its quotient, with delta = 4. Over that quotient there
  are 14 disc covers, 4 of them positive. Those 4 are 2 W-sets up to isometry: P6
  (identical to `d31-run-dark-min/found.json[0]`) and a 6 x 6 ring with an internal
  slit. The ring passes the certificate test but isn't a room. This isn't a full
  r = 12 classification: z = 4 shapes were not enumerated.

## 6. Agreement with d44, d45, and d46

- **d46: agrees.** 0 positives at r <= 8, by a disjoint method and code base.
- **d45: agrees.** The zero-fibre count is tight on both dark rooms, and z <= 2,
  d <= 9 at r <= 8 is reproduced.
- **d44, two notes, no conflict.**
  - d44 judged design b to need a realizability procedure or a reflection-tiling
    lemma (`README.md:51-53, 101`). Section 3's arc model is that lemma. A negative
    result needs no realizability step, because the search covers all disc W-sets.
  - d44's 26,640 target tuples (`README.md:139-141`) are monodromy tuples without
    the reflection structure or the Par(x) condition. With both, 106 shapes remain.
- **The brief, not d44 to d46:** "each class quotient has z <= 2" holds only for the
  delta >= 3 class.

## 7. Compute used against caps

| Item | CPU-s |
| --- | --- |
| Quotients, z <= 2 and z <= 3 | 230 |
| Covers, r = 8 and r = 9 (each run twice, after a fix) | 130 |
| Generic cover validation (3 runs) | 1,282 |
| Brute-force validation, n <= 9 (twice) | 73 |
| Sanity, P6 family, triples, tests | about 60 |
| Total | about 1,775 (30 min); cap 60 min |

At most 2 processes ran at once. Python stayed under 200 MB. Files total 0.8 MB.
Nothing was written outside this directory. One scratch file went to `/tmp`, and I
deleted it.

One bug was found and fixed during the run. The first room test accepted slit
W-sets as "embedded". `fold.is_room` now also checks that walls sit exactly where
the neighbouring cell is absent. Positivity counts didn't change.

## 8. Files

| File | Role |
| --- | --- |
| `fold.py` | W-set model: orbit types, B_x, quotients, separation, developing map, room test |
| `named.py` | The 22-wall room, P6, and the cross through `fold.py` |
| `enum_K.py`, `analyze_K.py`, `mirror_count.py` | Quotient enumeration and filters |
| `enum_P.py` | Arc-model cover enumeration and positivity test |
| `validate_generic.py`, `validate_brute.py` | Model-free cross-checks |
| `sanity.py`, `p6_family.py`, `triples.py` | r = 9 and r = 12 sanity, triple statistics |
| `data/*.json` | Quotient lists, cover results |
| `logs/*.log` | Every run quoted here |

To reproduce, run from this directory: `python3 -B enum_K.py 2 12 data/K_z2_d12.json`,
`python3 -B analyze_K.py data/K_z2_d12.json 8 2 data/K_adm_r8.json`, then
`python3 -B enum_P.py data/K_adm_r8.json 8 data/P_r8.json`.
