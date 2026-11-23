# Illumination in strictly simple orthogonal lattice rooms: results record

Date: 2026-11-18. Directory: `directions-2026-11-09/` (paths below are relative to it).
Audience: Peyton, and any future research session on this problem. This is an internal
record. It isn't a paper, and nothing in it has been refereed by a human mathematician.

Every claim carries a status tag. Every number is copied from the cited memo or log. If a
number here disagrees with its source, the source wins. Section 10 lists the places where
the sources disagree with each other.

## Status tags

| Tag | Meaning |
| --- | --- |
| **PROVED (reviewed)** | An agent wrote the proof. At least one independent AI referee read it and signed it, possibly with fixes. |
| **PROVED (unreviewed)** | An agent wrote the proof. No referee has read it. |
| **PROVED (coordinator-checked)** | Unreviewed, but the coordinator re-derived the key step by hand. |
| **COMPUTED (independent)** | A computation whose result a second, independent implementation reproduced. |
| **COMPUTED** | A computation that only the coordinator reran, or that only one implementation checked. |
| **COMPUTER-ASSISTED** | A proof whose finite part is a computation. The status of each input is listed. |
| **REFUTED** | A stated claim that an explicit, checked counterexample breaks. |
| **OPEN** | Neither proved nor refuted. |
| **GUESSED** | A judgment or estimate. It carries no weight. |

"AI-reviewed" never means "refereed". Each referee was one agent, usually on the same model
family as the author.

## 1. Summary

**Target.** Consider strictly simple rooms on the square lattice, with axis-parallel and
45-degree walls. The minimum wall count of such a room with a dark pair of interior points
is 22. A 22-wall orthogonal room with exactly one dark pair is known (Theorem Q22). The
target is a **conjecture**. Daniel set this scope on 2026-11-09. General polygons, slit rooms, and
pinched rooms are out of scope.

**Working goal (since 2026-11-17).** Every pair of interior points is lit in every strictly
simple orthogonal lattice room with `W <= 20` walls. The 45-degree case stays in the target
but isn't worked.

**What is proved.**

- Small rooms. Every pair is lit when `W <= 8`, for any real side lengths. PROVED (reviewed).
- Real to rational. In a lattice room, if every rational pair is lit, every real pair is
  lit. PROVED (reviewed).
- The fold side. No strictly simple orthogonal lattice room with `W <= 20` has a rational
  interior pair certified dark by a Par, Cut, or Rig certificate over any pillowcase base.
  COMPUTER-ASSISTED. The runs checked about 14.4 billion rooms and at least 59.4 billion
  pairs, with 0 positives. Each of its lemmas has one AI referee. A second proof by fold
  enumeration (d52, refereed in d54) reproduces the core case without enumerating rooms.
- The finite case of the lit side. In every normalized room with `W <= 20` that has a class
  with a proper canonical factor (2,800 rooms), all 6,680 same-class interior lattice pairs
  are lit. COMPUTED (independent: d67 reproduced it with its own billiard code).
- The census. No dark same-class pair exists at `W <= 21` and area at most 20. COMPUTED
  (independent tracer).
- A set of structural lemmas that cut the open lit side down to one infinite family. These
  are the fold-converse lemma FC, Lemma M, the Relay lemma, the counting identity, and the
  midpoint lemma. Statuses vary; see section 3.

**Update.** Section 11 records the Q-class closure theorem and later checks; it supersedes the BBBQ part below.

**The exact open statement.** For same-class interior lattice pairs, everything reduces to
lemma OL on the rooms R\*:

> **OL.** Let `P` be a strictly simple, normalized orthogonal lattice room with `r <= 8`
> reflex corners and area at least 21. Suppose each of its four parity classes has
> canonical factor `N_x = B` (type B) or `N_x = DP` (type Q). Let `S != T` be interior
> lattice points of one class `a`. Then some lift pair of `(S, T)` is x-lit for some
> target `x != a` of type B.

OL is open in two parts:

1. **BBBB rooms** (all four classes of type B) with area at least 21. This set is
   infinite. Every normalized room with area greater than `4r + 4` belongs to it.
2. **BBBQ rooms** (exactly one class of type Q) with area 21 to `4r + 4 <= 36`. This set
   is finite, but it hasn't been enumerated.

Two further gaps stand between OL and the working goal. **G1**: different-class lattice
pairs. **G2**: pairs with a non-lattice rational mark. Both have closed certificate sides
and open lit sides. With OL, G1, and G2 proved, the working goal follows by the chain in
section 5. Without them, it remains a conjecture. The full target also needs the
**45-degree rooms**, which have only a census to 32 half-tiles.

**Kind of argument.** The lit side can't be closed by any finite set of lighting paths
(Lemma U, d57). So the remaining proof needs an argument that works for unbounded room
size. No published theorem covers genus-0 square-tiled surfaces with two marked points
(d27, d59).

## 2. Setup and notation

### 2.1 Rooms

- A **room** `P` is a finite union of closed unit lattice squares (cells). Its interior is
  connected, and it has no hole. It has no **pinch**: a lattice point with exactly two
  diagonally opposite cells. So the boundary is one simple closed curve. This is
  "strictly simple" (d9 README, "Scope and definitions").
- `W` is the number of maximal straight walls. It equals the number of corners. With `r`
  reflex corners, `W = 2r + 4`, so `W <= 20` means `r <= 8`. The room has `v = r + 4`
  convex corners.
- The **area** `n` is the number of cells.
- `P` is **normalized** when its horizontal edge lengths have gcd 1, and so do its vertical
  edge lengths. This is d10 R1 as corrected in `d10-d12-review/review.md`.
- Classify a lattice point by the number `k` of cells around it. It's a convex corner
  (`k = 1`), a smooth wall point (`k = 2`), a reflex corner (`k = 3`), or interior (`k = 4`). A **transparent**
  point is interior or smooth.

### 2.2 Light

A **lighting path** for `S != T` is a billiard path from `S` to `T` that reflects off walls
and never meets a corner. The pair is **lit** when such a path exists, and **dark**
otherwise. Corner avoidance applies to every corner, convex ones included, even after
unfolding (d56 `verify_plane.c` enforces it; recorded in the 2026-11-17 log entry).

### 2.3 The double as a cover of the pillowcase

- `B` is the **unit pillowcase**: two unit squares glued along their boundary. Its four
  corners are the classes of `Z^2 / 2Z^2`.
- The **double** `DP` is two copies of `P` glued along the boundary. It is an `n`-sheeted
  square-tiled cover `DP -> B`, branched over the four corners. Sheets are cells.
- Each corner `x` of `B` has a monodromy permutation `g_x`. It rotates by pi about the
  class-`x` points. Its cycles are the stars of those points:
  - a 1-cycle (**pole**) is a convex corner;
  - a 2-cycle (**regular point**) is a smooth wall point, or one half of an interior point;
  - a 3-cycle (**zero**) is a reflex corner.

  An interior point gives two 2-cycles. So it has two **lifts** in `DP`, and a pair
  `(S, T)` has four **lift pairs** (d10 section 3.1).
- `DP` has genus 0. The tuple `(g_a, g_b, g_c, g_d)` with group `G` determines it.
- Room corners are exactly the non-regular points of `DP`. Corner avoidance means a light
  path passes only through regular points.

### 2.4 Parity classes and targets

- The four **parity classes** are the cosets of `2Z^2` in `Z^2`, after translating so that
  the pair's class is `a = (0, 0)`. The other three are `b`, `c`, `d`.
- A light path from `S` to `T` in class `a` unfolds to a segment of primitive slope
  `(p, q)`. Its image in `B` runs back and forth along one saddle connection `a -> x`.
  Here `x` is the class of `(p, q)` mod 2. So `x` is one of the three other classes. This
  is the **target** of the path (d62 section 1).
- For a same-class pair, the targets are the three other classes. For a different-class
  pair, the only target is the class of `T`.
- **x-lit**: some lift pair is joined by a path with target `x`. It is decided exactly by
  the pure-braid orbit of the tuple (d0 dictionary, PROVED; d61 FC; d62 review). A pair is
  **x-dark** when it isn't x-lit.

### 2.5 Factors and certificates

- A **factor** is a quotient `DP -> N = DP / Pi` by a block system `Pi` of `G`. `N` is
  again a genus-0 pillowcase cover. Its degree over `B` is `d`, and `delta = n / d`.
- **Fact L** (d10, PROVED (reviewed)): `DP -> N` branches only over poles of `N`. A point
  of `N` is **live** when a regular point of `DP` lies over it.
- **Certificates at a target `x`** (d10 Theorem U):
  - **Par(x)**: the images of the two lifts in `N` differ, and `N` has no regular point
    over `x`.
  - **Rig(x)**: `N -> B` has identity monodromy at a corner `y` outside `{a, x}`. Also, for
    one arc, the image of `T~` lies outside the live component of the image of `S~`.
  - **Cut(x)**: the images are equal, every regular point over `a` and `x` maps to a
    regular point, and the monodromy at a third corner is one cycle.
- **Certified**: a target is certified when all four lift pairs have a certificate there.
  A pair is **certified dark** when every target is certified. Theorem U says that a
  certified pair is dark.
- **Canonical factors** (d10 R3): `B_x` is the finest block system that merges every
  2-cycle of `g_x`, and `N_x = DP / B_x`. `R_y` is the finest system that merges every
  cycle of `g_y`. Par(x) holds over some factor exactly when `B_x` separates the lift
  pair. Rig(x) holds for some factor exactly when it holds over `DP / R_y`.
- **Class types** (d66 section 1):
  - **B**: `B_x` is one block, so `N_x = B`.
  - **Q**: `B_x` is discrete, so `N_x = DP`. This happens exactly when class `x` has no
    transparent point (d68 Lemma B).
  - **proper**: `1 < deg N_x < n`.
- **R\***: normalized rooms with `r <= 8` in which every class has type B or Q. A room's
  **type string** lists its four class types, for example **BBBB** or **BBBQ**.

### 2.6 Pillowcase bases

For rational marks the natural base is `P_Lambda = R^2 / <2 Lambda, -1>` for a lattice
`Lambda >= Z^2 + ZS + ZT`. Its **index** is `m = [Lambda : Z^2]`. Odd index keeps corners
in at least 3 parity classes. Even index includes rooms with an even axis gcd,
half-integer marks, and the 45-degree base `Z^2 + Z(1/2, 1/2)` (d47, d48, d49). For lattice
marks in a normalized room, `B` is the only pillowcase factor (d10 R1).

### 2.7 Named rooms

| Name | Walls | Area | Role | Data |
| --- | --- | --- | --- | --- |
| R22, the 22-wall room | 22 | 15 | The known dark room, one dark pair; `r = 9` | `d9-census-w22/README.md` "The dark pair" |
| P6 | 28 | 20 | Smallest dark room with a run, glued-copy class | `d30-rigidity-proof/`, `d31-run-dark-min/` |
| cross12 | 12 | 12 | Cut-certified class with a lit pair | `d10-d12-review/room_r4.log` |
| dumb12 | 12 | 20 | The one BBBB test room at area 20 | `d66-pair-level/pair_level.log` |
| S10 | 12 | 10 | Per-lift-pair counterexample | `d65-nx-equals-b/README.md` section 2 |
| room 1843 | 12 | 20 | Smallest point-level per-target counterexample | `d64-finite-case/README.md` section 5 |
| cov4181, cov4269 | 20 | 28 | Per-target counterexamples inside R\* | `d66-pair-level/README.md` section 7 |
| cov2929 | 20 | 22 | First failure of explicit path families in OL's range | `d69-bbbb/README.md` section 3 |
| DB55 | 12 | 53 | BBBB room with a unit corridor of length 3 | `d69-bbbb/README.md` section 1 |

## 3. Theorems

### 3.1 Foundations

**Theorem Q22 (the 22-wall room).** In the manuscript's 22-wall room, two distinct
interior points are joined by no billiard path if and only if they are `(0,0)` and `(2,2)`.
- Status: PROVED (reviewed). The darkness proof is the manuscript's; d3's referee accepted
  it. Two independent programs checked the lit-side certificates.
- Where: Peyton's Q22 manuscript (`preprints/twenty-two-wall/`), `d3-review/review.md`.
- Census confirmation: d9 finds it as the only dark room at `W = 22`, area at most 20.

**Theorem S (small rooms, d15).** Let `P` be a strictly simple orthogonal polygon with real
vertex coordinates and at most 2 reflex corners (`W <= 8`). Then a billiard path that
avoids vertices joins every two distinct interior points.
- Status: PROVED (reviewed). The proof uses no parity, so it holds for real points.
- Where: `d15-small-r/theorems.md`; review `d15-review/review.md` (no gap; two wording
  corrections, including Lemma C "same form").
- At `r = 3` and `r = 4` the same lemmas certify 13,030 of 13,608 and 503,328 of 564,629
  position-type pairs. COMPUTED.

**Theorem RR (real to rational, d16).** Let `P` be a strictly simple orthogonal lattice
room. If every pair of distinct rational interior points is lit, every pair of distinct
interior points is lit.
- Status: PROVED (reviewed). The proof is elementary. It uses no orbit-closure theorem.
- Where: `d16-real-to-rational/reduction.md` Theorem 1, Corollary 1; review
  `d16-review/review.md` (Lemma D corrected; Theorem 1 and Corollary 1 confirmed).

**Proposition R1 (base, d10).** In a normalized orthogonal lattice room, the only
pillowcase factor of `DP` is `B`.
- Status: PROVED (reviewed), with a correction. It needs gcd 1 per axis. It is false if
  "normalized" means "corners in three parity classes": the L-tromino stretched by 3 along
  `x` is a counterexample.
- Where: `d10-mechanisms/theory.md` section 1; `d10-d12-review/review.md`.

**Normalization step (d66 step 1).** Scaling by `(1/g_h, 1/g_v)` commutes with reflections
in axis-parallel walls. It keeps `W` and keeps rational points rational. So you may assume
`P` normalized and the marks rational.
- Status: PROVED (unreviewed; elementary). Where: `d66-pair-level/README.md` section 2.

**Theorem U and D1 (soundness of certificates, d10).** If some pillowcase factor has a
certificate at every target, the pair is dark. For rooms (D1): if `b`, `c`, `d` are all
certified, the pair is dark.
- Status: PROVED (reviewed). In an independent implementation, 0 of 12,425 lit pairs carry
  a full certificate.
- Where: `d10-mechanisms/theory.md` section 2; `d10-d12-review/review.md`.

**Proposition R3 (canonical certificates).** Par(x) for some factor holds exactly when `B_x`
separates the lift pair. Rig(x) with identity at `y` holds exactly when it holds over
`DP / R_y`. Both systems are invariant under the seam reflection.
- Status: PROVED (reviewed). Where: `d10-mechanisms/theory.md` section 3.2.

**Proposition R4 (Cut).** Cut(x) with a transparent target class forces the 12-wall cross,
and the cross is lit.
- Status: PROVED (reviewed), with a corrected step 3 and a scope note: R4 is false for
  smooth wall marks with the original conclusion. Where: `d10-d12-review/review.md`.

**Conjecture D2 (open).** If an interior same-class pair is dark, then `b`, `c`, and `d`
are all certified. This is the lit side of the problem in certificate language
(`d10-mechanisms/theory.md` section 4). OL is its restriction to R\*.

### 3.2 Census results

**Census C9.** Over all 945,070,200 strictly simple rooms with area at most 20 and at most
22 walls, the only dark same-class interior pair is the R22 pair. So:
- (a) no dark same-class pair exists at `W <= 21` and area at most 20;
- (b) at `W = 22` and area at most 20, R22 is the only dark room.

- Status: COMPUTED (independent). 217,900,348 pairs are lit by explicit paths. A second,
  independent tracer re-checked every path. Three complete deciders call the R22 pair dark.
- Where: `d9-census-w22/README.md`. Extended to `W <= 24` at area at most 19 (d29;
  STATE.md).
- d9 Part A (cited by d49): different-class lattice pairs are lit at area at most 16.

**Theorem K6.** Rooms with at most 6 transparent points and `W <= 21` are lit.
COMPUTER-ASSISTED. Where: `preprints/restricted-minimum-k6/` (8.75 GB of certificates;
STATE.md).

### 3.3 The fold-side theorem

**Theorem F (certificate theorem at `W <= 20`).** Let `P` be a strictly simple orthogonal
lattice room with `W <= 20`. Then no pair of rational interior points of `P` is certified
dark. This holds for Par, Cut, and Rig certificates over any pillowcase base `P_Lambda`.

At `W <= 20` there's no exception. The known dark rooms, R22 (`W = 22`) and P6 (`W = 28`),
lie outside the range. Both serve as positive controls in every run.

- Status: COMPUTER-ASSISTED. Each theory input has one AI referee. The referees' own
  repairs (d48, d50) are unreviewed.
- Where: assembled in `coordinator-log.md`, 2026-11-17 "d56 full run result".

The proof has five parts.

| Part | Content | Status | Where |
| --- | --- | --- | --- |
| F1 | Reduction (d39, corrected in d43). Cut never appears in a fully certified dark triple. Essential Rig at `r <= 8` forces area at most 20, which the census covers. So, over `B`, a certified pair needs `B_b`, `B_c`, `B_d` all to separate all four lift pairs. Then `5 <= r <= 8` and area 21 to `5r`. | PROVED (reviewed by d43; two gaps filled there) | `d39-mixed-class/astra.md`, `d43-review-d39/review.md` |
| F2 | Filter F\*. A positive pair needs a non-Galois class quotient: `delta >= 3`, with a sum condition. Allowed areas at `W = 20`: 21, 24, 25, 27, 28, 30, 32, 35, 36, 40. | PROVED (reviewed by d45: "safe to use") | `d44-cert-check-sizing/README.md`, `d45-review-fstar/review.md`; inputs d2 section 1.7, d36.3, d36.4 |
| F3 | Room enumeration (d46). | COMPUTED | `d46-cert-check/README.md`, `runs/full_W20/aggregate.md` |
| F4 | Scope gaps: coarser bases, different-class marks, even index (d47 to d50). | PROVED (reviewed once each) | `d47-cert-gaps/opus.md`, `d48-review-d47/review.md`, `d49-even-index/memo.md`, `d50-review-d49/review.md` |
| F5 | The two residual finite checks (d56). | COMPUTED | `d56-final-check/README.md`, `runs/full/aggregate.md` |

**Counts (all 0 positives).**

| Run | Rooms | Pairs | CPU |
| --- | --- | --- | --- |
| d46 full, `W = 20`, areas in F\*'s list | 13,286,070,297 (passing F\*; 1,058,080,070 canonical shapes) | 52,725,865,264 | 87,830 s (24.4 CPU-h), 3.1 h wall on 8 processes |
| d46 pilot, `W <= 18` | 471,475,261 | about 1.15e9 | 1,606 s |
| d46 recheck, `W <= 20`, area at most 20 | 427 million | not stated | part of validation |
| d56 Set A (D20: `W = 20`, area 20, different-class lattice pairs) | 169,672,127 | 285,299,577 | 16,940 s (4.7 CPU-h) for d56 in total |
| d56 Set E (non-lattice marks; index 2 and 4, index 6 for one `W = 16` room) | 945,884 | 5,238,044,332 | (included above) |

In d56 every pair is lit by a verified path, so no certificate test is needed. Survivors,
path-verification failures, certified pairs, and tripwires are all 0. A 1% sample of 55.2
million pairs was also certificate-tested: 0 fully certified.

**Coordinator checks.** For d46, all 500 job files are present and all 5,500 per-cell lines
read "positives 0". For d56, 920 SUMMARY lines read OK, and the sums give 0 survivors.
`aggregate.py` crashed in its reconciliation step; the coordinator fixed an operator
precedence bug and reran it. No job was rerun.

**Scope of Theorem F.** It is a statement about certificates. It doesn't say that
uncertified pairs are lit. That is conjecture D2, the lit side.

### 3.4 The second proof (fold enumeration)

**Theorem F' (d52, refereed in d54).** Let `P` be a strictly simple orthogonal lattice room
with `r <= 8` and corners in at least 3 parity classes. Then no same-class interior pair is
certified dark by Par, Cut, or Rig over the unit pillowcase, at any area. Now take `r = 9`.
Suppose some target class `x != a` has `delta_x >= 3`, and all three targets are
Par-certified. Then the room is R22, with its one pair.

- Status: COMPUTER-ASSISTED; PROVED (reviewed) for the reduction. The referee fixed the
  wording ("some target class `x != a`") and wrote out two unstated cover-model steps.
- Method: enumerate the small class quotient `N_x` and all its degree-`delta` disc covers,
  instead of rooms. 106 admissible quotient shapes (56 up to mirror), `d` from 3 to 9, `z`
  in {1, 2}; 185 (shape, delta) cases; 4,710 covers; 1,113 strictly simple rooms up to
  isometry. 0 positives. About 30 CPU-minutes.
- Validation: a second cover enumerator agrees on 185 of 185 cases (10 finished by d54).
  The referee's own positivity code also finds 0 positives.
- Independence: independent of d46's code, of F\*, and of Theorem K6. The referee
  enumerated the branch "all targets have `delta <= 2`" directly (21 CPU s, 0 positives).
  That replaced d2 claim 4 and F\* with d36.3. Shared with d46: Theorem U, R3, Fact L, the
  d39/d43 reduction (with C9 for essential Rig), `delta z <= r`, and the scope.
- Not covered: Rig-certified rooms at `r = 9`. d54 didn't rerun d52's own enumerations.
- Where: `d52-fold-enumeration/memo.md`, `d54-review-d52/review.md`.

### 3.5 Lemmas on pillowcase bases (d47 to d50)

**Lemma Z (d49).** Let a certificate over `P_Lambda` have degree `n = delta d`, with `z`
zeros. If `z >= 1`, then `n <= 8r` for Par, `n <= 5r` for Rig, and `n <= 3r` for Cut. A
zero-free Cut forces `n <= 4r + 4` and a vertex-only class.
- Proof idea: `sum_j (p_j + 3 z_j) = 4z + 4` and `delta z <= r`.
- Status: PROVED (reviewed by d50, "correct with fix"). "Cut forces `d = 3`" holds only
  with a zero. A zero-free Cut has `d = 2`, and its vertex-only class is the target. The
  bounds stand.

**Lemma Z'.** At a target outside `V` (the image of `Z^2`), any certificate with a zero
has `n <= 4r`. PROVED (reviewed by d50).

**Lemma R0.** A zero-free Rig needs `d = 4`, `Lambda >= (1/2) Z^2`, and every vertex
regular. So no zero-free Rig exists for lattice marks or at `m = 2`. PROVED (reviewed by
d50, "correct").

**Witness lemma.** For any lattice data (`Lambda`, mark classes mod `2Z^2`, lift pair), some
L-hexagon room lights the lift pair. So no certificate that depends only on lattice data
separates all targets of a lift pair. PROVED (reviewed by d50, with the fix "classes mod
`2Z^2`"). The per-target version is REFUTED (section 4).

**Odd-part reduction.** A certificate over `P_Lambda` transfers to the base
`Lambda' = Lambda_(2) + M_0 + rho M_0`, where `M_0 = Z^2 + ZS + ZT`. PROVED (reviewed by
d50; the term `rho M_0` is d50's fix). It rests on d47's transfer Lemma 3.2, which d48
corrected.

**Consequences.** Lattice marks over every even-index base are closed by theory plus C9 and
Theorem S. Non-lattice marks reduce to `n_R <= 16` and the finite Set E of d56. d48 signed
the odd-index case. Over odd-index `P_Lambda`, the four lift pairs aren't all certified.
The one possible exception, the D20 residue, is closed by d56 Set A. Different-class marks admit only
Rig, which forces area at most 16, or area 20 at `r = 8` (d47 Prop 4.1, corrected in d48).

### 3.6 The 45-degree base

**Proposition T (d51).** Over the `(2,4,4)` triangle base, Par and Rig certificates exist
and are sound, and no sound Cut exists. For normalized rooms with 45-degree walls, a
certificate allows up to `8W - 8` tiles for A/B and different-class pairs, and `14W - 12`
for C pairs. At `W <= 21` that's 160 and 282 tiles. The d11 census reaches only 32 and 24.
- Status: PROVED (unreviewed). Agent confidence: Par 90%, Rig sketch 75%, no Cut 80%.
- Consequence: no certificate-side theorem follows for 45-degree rooms. The cause is cone
  points of angle `3 pi / 2`, which have positive curvature.
- Narrow result (a'), census-backed, PROVED (unreviewed, 80%): no strictly simple room
  with `W <= 23` has an A/B pair of Tokarsky's type.
- Inequality: regular points over the certificate's class number at most `2 delta - 2`.
  PROVED (unreviewed, 90-98%). A peer (Codex) round found the equality case mostly vacuous
  on the named rooms; the coordinator didn't verify that round.
- d48's sketch shows every map from `DP` to `(2,4,4)` factors through a pillowcase for
  orthogonal rooms. So the triangle base adds nothing to Theorem F. PROVED (sketch, 80%).
- Where: `d51-triangle-base/memo.md`, `d48-review-d47/review.md`.

### 3.7 The fold converse (d61, d62)

**Lemma FC.** Fix a state of the pure-braid orbit and an arc `alpha: a -> x`. Let `S~`,
`T~` be regular points over `a` with the same image `u` in a factor `N`. Let `K` be the
component of `u` in the live subgraph of `Gamma_alpha(N)`.
1. `K` is a path or a cycle.
2. Cycle case: `S~` and `T~` are joined along `alpha` exactly when `T~` is in the orbit of
   `S~` under the monodromy `mu` around `K`.
3. Path case: they're joined exactly when an alternating word in at most two partial
   involutions `tau_p` carries `S~` to `T~`. Each `tau_p` is the local monodromy at a
   live-pole end `p` of `K`, transported to the fibre of `u` and restricted to its
   2-cycles. The restriction is corner avoidance.

- Status: PROVED (reviewed). d62 verdict: "sound with fixable gaps". G1 (review): state
  `tau_u` and `tau_p` on sheets of `u`'s block, since `u` can be a pole. G3 (review): give
  the realization hypothesis its quantifiers.
- Tests: 405 rows (992,988 instances), 0 disagreements with ground truth (d61). d62's own
  `check_fc.py` (969,372 instances) and an exact billiard `billiard.py` find 0
  disagreements. COMPUTED (independent).
- Negative parts (PROVED, d61): no group works. Using full local permutations, which
  ignores corner avoidance, lights dark pairs on R22 and P6.
- Degree bound: `deg N_x <= r + 4 + 3 r_x <= 4r + 4 <= 36`. PROVED (reviewed by d62).
- Where: `d61-fold-converse/README.md`, `d62-review-d61/review.md`.

**FH\* weak form (d60).** On cross12, dumb12, R22, and P6, a pair with distinct images lit
in a minimal factor always has a lifting witness: 0 violations. COMPUTED (coordinator
rerun reproduced `summary.log` exactly). The strong reading is REFUTED (section 4). In
R22's 5-block factor no regular point lies over `b`, `c`, or `d`, so equal-image lit pairs
can't lift. PROVED (unreviewed). Where: `d60-fh-star-test/README.md`.

### 3.8 The realization lemma and the case split (d63)

**Lemma 1 (d63).** Take a same-class pair with equal images `u` in `N_x`. The pair is x-lit
exactly when, in some state, the 2-cycles of `g_a` and `g_x` inside the blocks of `u`
join `S~` to `T~`. So the realization lemma is "x-dark implies a certificate at `x`".
- Status: PROVED (unreviewed). Independent of FC.

**Split.** The case `N_x != B` (proper factor) is finite: `delta z <= r` and area at most
`8r`. The case `N_x = B` contains a per-class form of d14's Lemma H. PROVED (unreviewed).
Special cases proved: degree 2, and Galois covers with deck group `C2`, `V4`, or `S3`.

- Where: `d63-realization/README.md`. Tests: 722 rows, 0 counterexamples (COMPUTED).

### 3.9 Lemma M (d65)

**Lemma M.** Take any dark pair of the d14 `n = 10` non-transitive relations. It has the
form `{s, delta s}`. Here `delta` is a deck involution (a room symmetry) with two regular
fixed points. If `delta` has no fixed point over `a` or `x`, such a pair is x-lit only by a light
loop that separates the two fixed points.
- Status: PROVED (unreviewed). The coordinator reran `rl_room.py`: identical output.
- Also COMPUTED: 4 of the 18 d14 relations are doubles of real rooms (Z12 and S10). All 18
  lack certificates (d63 had said 6).
- Where: `d65-nx-equals-b/README.md`.

### 3.10 The finite case (d64, d67)

**Theorem FIN.** Let `P` be a normalized strictly simple orthogonal lattice room with
`W <= 20` in which some class `x` has `1 < deg N_x < n`. Then every same-class interior
lattice pair of `P` is lit, whatever the pair's class.

- Status: COMPUTED (independent), with a PROVED completeness argument.
- Completeness (written before the run): `z >= 1`, `delta z <= r`, so `z <= 4`; at least 3
  singular classes; `d <= 4z + 2 <= 18`. `enum_K.c` (a C port of d52's search) finds every
  quotient, and the d52 arc model finds every cover, `delta = 2` included.
- Counts: 4,290 quotients, 4,475 (K, delta) cases, 4,776 rooms (4,581 normalized), 2,800 in
  scope, 6,680 same-class interior pairs, all lit. 27 CPU-minutes of an approved 120.
- Review (d67): "sound, with fixable gaps". d67's own exact billiards find a witness for
  all 6,680 pairs with `max(p, q) <= 8`. Its own C brute force over 104,592,937 polyominoes
  with `n <= 16` matches d64's in-scope list at every area. d64's own check went to
  `n <= 14` (9,800,041 polyominoes, 229 in-scope rooms). It reproduces 4,581 / 2,800 /
  6,680.
- Remaining gap: the `z = 4` part of `enum_K.c` (3,663 of 4,475 cases) has no independent
  cross-check. Reading found no defect.
- Where: `d64-finite-case/README.md`, `d67-review-d64/review.md`.

### 3.11 The pair-level chain and the Relay lemma (d66)

**Proposition 1 (Q-class geometry).** If class `y` has type Q, every edge on a line of
class `y` has length at most 2. Suppose `y = a + (1, 0)`. Then both horizontal neighbours of
every interior `a`-point are reflex corners. So class `a` has at most `r_y / 2 <= 4`
interior points. PROVED (unreviewed).

**Proposition 2 (no certificates in OL's range).** In R\* at area at least 21, no pair has a
certificate at any B target. At a B target Par fails (one block); Cut fails by R4, since
the cross isn't in R\*; essential Rig forces area at most 20 (d39, fixed in d43).
- Status: PROVED (unreviewed) from reviewed inputs. Consequence: OL is a pure lit
  statement. "Dark implies certified" and "every pair is lit" coincide there.

**Relay lemma.** Let `delta` be a deck involution of `DP -> B` with fixed points `F_1`,
`F_2`. If a light path joins `S~` to some `F_i`, then `S~` and `delta S~` are lit, at the
target of that path. Proof: `delta` is the half-turn about `F_i`, so the path followed by
its reversed image is one geodesic through a regular point.
- Status: PROVED (unreviewed). COMPUTED: 30 of 30 x-dark delta rows are lit at the
  fixed-point class.
- Corollary (PROVED, unreviewed): let `sigma` be a half-turn of `P` about `C`, in class
  `c != a`. If `{S, sigma S}` is dark, the different-class pair `{S, C}` is dark.
  So symmetric pairs reduce to G1.
- Where: `d66-pair-level/README.md` sections 5-6.

### 3.12 The counting identity and the one-target case (d68)

**Lemma A (counting identity).** For every strictly simple lattice room and every parity
class `y`:

`n = cvx_y + 2 smooth_y + 3 rfx_y + 4 int_y`

Each cell has one corner in each class, and you count (cell, class-`y` corner) pairs both
ways. Status: PROVED (coordinator-checked). COMPUTED on all 4,776 d64 rooms, 4 classes each,
0 failures.

**Theorem 1.** If two classes have type Q, then `n <= 2r + 2`, so `n <= 18` at `r <= 8`.
Proof: for a Q class, `n = 3 r_y + v_y`. Add two such identities and use `v = r + 4`.
Status: PROVED (coordinator-checked: the coordinator re-derived the bound by hand).

**Corollary 2 (one-target emptiness).** OL1, the case of exactly one B target, is empty:
it needs two Q classes, hence area at most 18 < 21. PROVED. In every such room with
`W <= 20`, every same-class pair is lit by C9. COMPUTED: d66's 15 OL1 pairs lie in rooms of
area 14 and 16, all lit.

**BBBQ bound.** If exactly one class is Q, then `n = 3 r_y + v_y <= 4r + 4 = 36`. PROVED.
The bound is attained in `covers.json`: 885 one-Q rooms there have area at least 21, with
maximum 36. So every normalized room with area greater than `4r + 4` is BBBB.

Where: `d68-one-target/README.md`.

### 3.13 The midpoint lemma and the transfer lemma (d69)

**Lemma MP (midpoint lemma).** Let `S`, `T` be lattice points of one class in a lattice
room, and `gamma` a lighting path. Then `gamma` passes through a lattice point at half its
length, and that point is interior or a smooth wall point. Proof: unfold by reflections in
integer lines, which preserve coordinates mod 2; so `T* = S (mod 2)`, and `(S + T*)/2` is a
lattice point.
- Status: PROVED (coordinator-checked).

**Corollary MO (midline obstruction).** An x-monotone lighting path crosses the line
`x = (s1 + t1)/2` once, at that midpoint. If the line has no interior or smooth lattice
point there, the x-monotone family is empty. PROVED (unreviewed). COMPUTED: MO explains 254
of 1,067 x-monotone failures and 160 of 727 y-monotone failures, with 0 false firings.

**Lemma TR (transfer, sketch).** If a combinatorial path family fails on a non-empty open
set of real (lengths, S, T), it fails for same-class pairs in infinitely many normalized
lattice rooms. Each of those rooms is BBBB, with area greater than 64. PROVED (unreviewed,
sketch).

**Rectangle step.** If the bounding box of `S` and `T`, or the segment `ST`, lies in the
open room, the pair is lit. PROVED (trivial).

**Door step.** For a unit-corridor dumbbell, the x-monotone family reduces to a finite
congruence problem. Its validity is periodic in the slope with period `2L`. PROVED
(unreviewed, reduction only). The dumbbell lemma DL itself is OPEN.

Where: `d69-bbbb/README.md`.

### 3.14 Thin corridors (d57, d58)

**Lemma U (d57).** Let `T` lie at depth `h` in a corridor of width `w`. Let `S` lie at
horizontal distance `d` from the corridor, and let `H` be the room's height. Then every
billiard path from `S` to `T` has at least `2 sqrt(dh / (Hw)) - 2` reflections.
- Status: PROVED (unreviewed). 563 of 578 open pairs at `W = 10` have such a corridor.
- Consequence: no finite set of lighting paths proves the target at any `W >= 10`. This
  holds for lattice rooms too, since a width-1 corridor in a large room has relative width
  tending to 0. Any proof needs a limit argument.
- Also COMPUTED: 0 of the 578 open position-type pairs at `W = 10` closed on the full real
  region; 6 collinear pairs closed on a compact truncated region.
- Where: `d57-witness-mining-r3/README.md`.

**Lemma P (d58).** A far-point image lights the pair unless its phase lies in a bad arc of
length `|1 - 2 beta| - kappa`. Failure needs `Lh / (wD)` to be an integer, among other
conditions. Midline points never fail.
- Status: PROVED (unreviewed). For the 10 door pairs at `W = 10`, thin corridors are lit
  except on a non-empty double-resonance set. All 10 instances built there are lit
  (COMPUTED). Lattice rooms sit on resonance sets, so these generic statements don't
  transfer to the target.
- Where: `d58-corridor-limit/memo.md`.

### 3.15 Earlier structural results (one line each)

| Result | Status | Where |
| --- | --- | --- |
| No common parity factor separates interior pairs at `r <= 8`. Per-class and rigid factors were left open. | PROVED (reviewed) | `d2-review/` |
| Triangle bounds: (1,2,5) exactly 32; 30-60-90 exactly 27; 45-45-90 at least 22. | PROVED (reviewed) | `d7-review/` |
| Full families over a base stratum contain no dark room pair. | PROVED (reviewed) | `d19-23-review/` |
| d35, d36: AW fails on torus covers; amalgamation holds for Galois quotients; a one-class separating quotient forces area at most `5r` (needs at least 3 corner classes). | PROVED (reviewed by d38, scope gap noted) | `d35-aw-torus/`, `d36-amalgamation/`, `d38-review/` |
| Band lemma; covering certificates for one-row families. | PROVED (unreviewed) | `d28-band-stabilization/` |
| Theorem R: a run of 3 or more rows admits no parity factor. | PROVED (unreviewed) | `d30-rigidity-proof/` |
| Wall formula for glued rooms: `W(P) = d (W(R) - 4) + 4 + 2 n3`. | PROVED (unreviewed) | `d31-run-dark-min/` |
| Smallest dark room with a run, glued-copy class: `W = 28`, unique. | COMPUTED | `d30`, `d31` |

## 4. Counterexamples and refuted statements

Each entry is a result. Don't re-propose these statements.

| Statement | Counterexample | Status | Data |
| --- | --- | --- | --- |
| d37 joint majority: in each class fibre a visibility component holds a strict majority, so a dark pair yields per-class certificates | cross12, `S = (1,2)`, `T = (3,2)`: dark in class `c` by Cut while the room pair is lit through another class | REFUTED (d38) | `d38-review/review.md`; `d10-d12-review/room_r4.log` |
| Per-target witness lemma: some room lights each target of a lift pair | `Lambda = (1/2)Z x Z`, lattice marks with `T_x - S_x` odd: `N = B` separates at the V target in every room | REFUTED (d49, PROVED) | `d49-even-index/memo.md` section 4 |
| d47 Definition 1.2 (all four lifts over corners) | Back lifts sit at `rho S`. Single-base Residue G1-odd is empty. | REFUTED (d48, 95%) | `d48-review-d47/review.md` |
| d52 premise: F\* forces `delta >= 3` for every class quotient, giving a finite list of triples | R22 has deltas (3, 1, 3) | REFUTED (d52) | `d52-fold-enumeration/memo.md` |
| R1 under the weaker hypothesis "corners in 3 classes" | L-tromino stretched by 3 along `x` | REFUTED (d10-d12 review) | `d10-d12-review/room_r1.log` |
| Realization lemma as an abstract cover statement | cross12 scaled by 3 (no certificate over `B`); d14's six `n = 10` relations | REFUTED (d63) | `d63-realization/README.md` |
| **Per-lift-pair RL**: with `N_x = B`, every pair of regular class-`a` points is x-lit unless Rig(x) or Cut(x) | **S10**: cells (0,2) (0,3) (1,1) (1,2) (1,3) (2,0) (2,1) (2,2) (3,0) (3,1); `W = 12`; marks (1,3), (3,1), class (1,1). At `x = b` and `x = d`, the delta-pairs are x-dark with no certificate. The room pair is lit. | REFUTED (d65, COMPUTED; `notch12.py` and the independent d12 verdict) | `d65-nx-equals-b/README.md` section 2 |
| **Per-target realization RL-fin** (proper-factor case) | 830 x-dark uncertified rows in 55 rooms; 37 point-level pairs dark on all four lift pairs at one target | REFUTED (d64, COMPUTED; billiards agree at `H = 120`) | `d64-finite-case/data/rl_*.json`, `logs/` |
| Same, smallest point-level instance | **Room 1843**: 20 cells, `W = 12`, `S = (1,2)`, `T = (3,2)`, `x = d`; `N_d` degree 5, `delta = 4`. Lit at `b` by the straight segment through (2,2). | REFUTED (d64; coordinator reran `example.py 1843` and `verify_billiard.py 60 1843`) | `d64-finite-case/logs/example_1843.log` |
| **RL-room** (all four lift pairs x-dark at one target implies a certificate) inside R\* | **cov4181** (cells listed in d66 section 7; `S = (2,3)`, `T = (4,3)`, class (0,1)): all lift pairs d-dark, uncertified, trivial deck group; b-lit through (3,3). **cov4269**: same pattern at `x = b`. Both `W = 20`, area 28, BBBQ. | REFUTED (d66, COMPUTED; billiards agree to `max(p, q) = 60`) | `d66-pair-level/pair_level.json`, `billiard_check.log` |
| **Strong FH\***: every lighting witness in a minimal factor lifts | dumb12 pair (1,1)-(1,2): 1,984 of 5,392 N-witnesses don't lift | REFUTED (d60, COMPUTED) | `d60-fh-star-test/log_strong_probe.txt` |
| FH\* "or equal" branch | R22 wall marks at its minimal factor (2); cross12 non-minimal 3-block factor (2); cross12 tower step 6 -> 3 (2). All lit, uncertified, equal images. | REFUTED (d60, COMPUTED) | `d60-fh-star-test/` logs |
| A group generated by full pole-loop monodromy decides light | Lights dark pairs: P6 12 of 12, R22 28 of 57 | REFUTED (d61, COMPUTED) | `d61-fold-converse/README.md` |
| x-lit is transitive | d14 section 4.3 relations | REFUTED (d14) | `d14-lemma-h/` |
| d14 obstruction is non-planar | Z12 and S10 realize 4 of the 18 relations | REFUTED (d65, COMPUTED) | `d65-nx-equals-b/d14_reality.log` |
| Per-class additivity of reflex corners | In R22, all three classes use all 9 reflex corners | REFUTED (coordinator, 2026-11-15) | `coordinator-log.md` |
| One-axis families (V, X, Y, B) light every pair in OL's range | **cov2929** (`W = 20`, area 22, BBBQ): pairs (3,1)-(5,3) and (3,3)-(5,5) lit by none; both are lit (d66) | REFUTED (d69, COMPUTED) | `d69-bbbb/decomp.json`, `symcheck.log` |
| BBBB rooms with area > 36 have no thin parts | **DB55**: two 5 x 5 squares joined by a unit corridor of length 3, area 53 | REFUTED (d69) | `d69-bbbb/verdicts.log` |
| A dark slit or pinched near-miss gives a strict dark room below 22 | Thickenings of Monteil's slit room (2,245 variants) and resolutions of his pinched 22-gon (5,867 variants): 0 dark | Not found (d42, d53, COMPUTED) | `d42-slit-thickening/results.tsv`, `d53-unpinch/results.tsv` |

## 5. The reduction chain

### 5.1 The chain

Target T20: in every strictly simple orthogonal lattice room with `W <= 20`, every pair of
distinct interior points is lit.

| Step | Statement | Status |
| --- | --- | --- |
| 0 | Real pairs reduce to rational pairs (Theorem RR). | PROVED (reviewed) |
| 1 | Normalize the room; marks stay rational. | PROVED (unreviewed, elementary) |
| 2 | Split pairs: (i) same-class lattice; (ii) different-class lattice (G1); (iii) at least one non-lattice rational mark (G2). | PROVED (exhaustive) |
| 3a | (i) in rooms with a proper class factor. | COMPUTED (independent): Theorem FIN |
| 3b | (i) in R\* with area at most 20. | COMPUTED (independent): C9 |
| 3c | (i) in R\* with two or more Q classes. | PROVED: area at most 18, so inside 3b (d68) |
| 3d | (i) in BBBQ rooms with area 21 to 36. | **OPEN, finite.** Not enumerated. |
| 3e | (i) in BBBB rooms with area at least 21. | **OPEN, infinite.** |
| 4 | (ii) G1: "x-dark implies Rig(x)" at the one target. | Certificate side closed (d46, d56 Set A, d47 Prop 4.1). Lit side **OPEN**. |
| 5 | (iii) G2: lit side over `P_Lambda0`, `Lambda0 = Z^2 + ZS + ZT`. | Certificate side closed (d46 to d50, d56 Set E). Lit side **OPEN**. |

The fold side isn't load-bearing for step 3. Steps 3a and 3b are direct lit verdicts. In
3d and 3e no certificate can exist (Proposition 2). The fold side matters only to turn a
"dark implies certified" form of G1 or G2 into a lit statement.

### 5.2 What is proved, and what isn't

Proved, under the stated statuses:

- Every pair is lit at `W <= 8` (Theorem S).
- No pair is certified dark at `W <= 20` (Theorem F, Theorem F').
- Every same-class interior lattice pair is lit in every room of steps 3a, 3b, and 3c.
- OL has no certificate in its range, has no one-target case, and its only infinite part
  is BBBB.

Not proved:

- **O1 (BBBB).** OL for BBBB rooms with area at least 21. Every normalized room with area
  greater than `4r + 4` is BBBB. BBBB rooms with area 21 to `4r + 4` also fall here; the
  only BBBB room ever tested at area at most 20 is dumb12. Evidence: 7 hand-built BBBB
  rooms with area 41 to 63, 726 pairs, all lit, 0 x-dark rows (d69, COMPUTED). The rooms
  are hand-picked, not a sample.
- **O2 (BBBQ).** OL for BBBQ rooms with area 21 to `4r + 4 <= 36`. Finite. Closable by an
  approved bounded enumeration (GUESSED). Evidence: 4,742 BBBQ pairs in `covers.json`, 0
  dark (d66). Both per-target failures (cov4181, cov4269) lie here.
- **G1 (different-class lattice pairs).** Lit side open in every room. Evidence: 27,190
  pairs in 4,592 rooms lit by exact billiards (d66); census to area 16 to 20.
- **G2 (non-lattice rational marks).** Lit side open in every room. The natural base is
  non-normalized, where per-target forms fail. Evidence: 8,025 half-integer pairs lit in
  11 named rooms. A larger R\* run hit its 300 s cap with 117 unresolved pairs (not dark,
  not decided); treat it as incomplete.
- **45-degree rooms.** Census to 32 half-tiles only (d11). No fold-side bound (d51) and no
  lit-side theory.

So the conditional statement reads: **if O1, O2, G1, and G2 hold, then T20 holds** (by
Theorem RR and steps 1 to 5). T20 plus the 45-degree case plus Theorem Q22 gives the target.

Within O1 and O2, symmetric pairs `{S, sigma S}` reduce to G1 by the Relay lemma. What's
left is non-symmetric pairs in rooms with at least two B targets. Rooms with trivial deck
group there are the old Lemma H territory.

### 5.3 Review debts in the proved part

| Item | Debt |
| --- | --- |
| d39 essential-Rig bound | One referee (d43), who filled two gaps. Load-bearing only for Proposition 2. |
| d47 to d50 lemmas | One referee each. The referees' repairs are unreviewed. |
| d52 enumerations | d54 didn't rerun them; logs quoted as written. |
| d64 `enum_K.c`, `z = 4` | 3,663 of 4,475 cases lack an independent cross-check. |
| d56 shortcut on D20 | Completeness rests on d48's (4, 5, 2) shape; unrefereed. Not load-bearing: the full run lit every D20 pair. |
| d61 FC | Reviewed. The review fixes G1 and G3 aren't written into d61. |
| d63, d65, d66, d68, d69 | Unreviewed. d68's Theorem 1 and d69's Lemma MP were re-derived by the coordinator. |

## 6. Dead ends

Don't repeat these without a new idea.

- Bounded reflections: Lemma U shows thin corridors need unbounded reflection counts (d57).
- Finite witness covering at `W = 10`: 0 of 578 pairs closed on the real region (d57).
- Lemma H via monodromy groups: x-lit isn't transitive, and no group decides light (d14,
  d61).
- Finite-blocking theorems: lattice rooms are torus covers, which they exclude.
- Apisa-Wright "dark implies fold": its proof needs finitely many periodic points, which
  torus covers lack (d35).
- EMM and orbit-closure finiteness: ineffective; for rational marks the orbit is closed
  (d59).
- Enumeration by area: OL is infinite; areas grow without bound at fixed `W` (d9).
- Twisting one-parameter families and band stabilization with bounded periods (d24, d28).
- Rigidity without the wall bound: fails at 28 walls (d29, d30).
- Counting and rank bounds from the Astra exchange (d25).
- Absolute thick-thin size reduction: scaling makes it equivalent to the target (d40).
- Multi-parameter covering certificates: crossing parameters aren't periodic (d41).
- Class-by-class visibility (joint majority): false at `r = 4` (d38).
- Per-class amalgamation by pure combinatorics: 12|34 against 13|24 is a counterexample
  (d35, d36).
- A full-scope fold theorem over the `(2,4,4)` base: area bound 160 against census 32
  (d51).
- Few directions, surgery induction, orbit closure: dead; effective bounds restate the
  target (d59).
- The group half of the FH\* tower: sound but carries no hard content (d60).
- Per-target or per-lift-pair realization lemmas in any form: false (d64, d65, d66).
- Decomposition into rectangles, doors, and chains with one-axis families: fails at turning
  routes such as cov2929 (d69).
- Lattice arithmetic as a tool for monotone families: Lemma MP makes it an obstruction
  (d69).
- Near-miss thickenings of Monteil's slit room and pinched 22-gon: no dark room; lighting
  paths reflect off the new wall (d42, d53).
- Relaxed rooms (slits and pinches) as evidence for "dark implies fold": 5 dark pairs in 8.3
  million rooms, too few (d55).

## 7. Reproducing

Run every Python script with `python3 -B` from its own directory. No script writes outside
its directory. All searches beyond named rooms need Daniel's approval and a cap.

| Result | Command | Cost |
| --- | --- | --- |
| C9 census | In `d9-census-w22/`: build `enum_rooms`, `shoot`, `orbitc` with `clang -O3`, then `./run_census.sh 20 26 40 16 runs/a20 0 12` and `... 13 25`; see README "Reproduce". | About 28 min wall for the two halves (README) |
| Theorem F, room part | In `d46-cert-check/`: `./run_full.sh 8 24`; results with `python3 aggregate.py runs/full_W20 --cells`. Don't rebuild `cert_check` mid-campaign. | 24.4 CPU-h (3.1 h on 8 processes); pilot 1,606 CPU s; validation about 1.4 CPU-h |
| Theorem F', fold enumeration | In `d52-fold-enumeration/`: `python3 -B enum_K.py 2 12 data/K_z2_d12.json`, then `analyze_K.py data/K_z2_d12.json 8 2 data/K_adm_r8.json`, then `enum_P.py data/K_adm_r8.json 8 data/P_r8.json`. | About 30 CPU-min (d52); referee 1,225 CPU s (d54) |
| Theorem F, residual checks | In `d56-final-check/`: `./run_full.sh 8 10`. Keep the shipped `check` binary. | 16,940 CPU s (4.7 CPU-h), 37 min on 8 processes |
| Lemma FC tests | `d61-fold-converse/fold_converse.py [--wall] [--tower] [room ...]`; review checks `d62-review-d61/check_fc.py ROOM CAP`, `billiard.py`. | About 2 min; review about 1.2 min |
| Theorem FIN | In `d64-finite-case/`: `cc -O2 -o enum_K enum_K.c; ./enum_K 4 18`, then `shapes.py`, `covers.py`, `dark_pairs.py start end out.json`. | About 1,630 CPU s |
| FIN review | `d67-review-d64/indep.py 12`; `./polyo 16`. | About 135 CPU s |
| Counterexample 1843 | `d64-finite-case/example.py 1843`; `verify_billiard.py 60 1843`. | Seconds |
| S10 | `d65-nx-equals-b/notch12.py`; `rl_room.py`. | Under 2 s |
| R\* tests, cov4181, cov4269 | `d66-pair-level/pair_level.py`; `billiard_check.py 60`. | About 28 s |
| Counting identity, BBBQ bound | `d68-one-target/one_target.py`. | About 0.3 s |
| Midpoint lemma, families | `d69-bbbb/decomp.py`, `midline.py`, `verify_b.py`, `symcheck.py`, `verdicts.py`. | About 25 s in total |
| Near-miss families | `d42-slit-thickening/`, `d53-unpinch/`, `d55-relaxed-lab/` READMEs. | About 1,150, 2,800, and 2,810 CPU s |

## 8. Computed evidence outside the theorems

These numbers support the conjecture. They prove nothing beyond their own range.

- Adversarial search: about 892,000 rooms to area 900, no dark room at `W <= 20` (d26).
- Diagonal (45-degree) census to 32 half-tiles (d11).
- Thickenings of Monteil's dark slit room: 2,245 strictly simple variants, 468 million
  lattice pairs, none dark (d42).
- Resolutions of Monteil's pinched dark 22-gon: 5,867 strictly simple variants (500 with
  `W <= 21`, 666 with `W = 22`), 1.54 billion lattice pairs, none dark (d53).
- Relaxed rooms: 8,303,245 orthogonal rooms with slits or pinches at area at most 15. All 5
  dark pairs are Par-certified at all three targets (d55).

## 9. Credits

**Peyton** is the lead investigator of this illumination research. He did most of the
original dark-room work with his father, Daniel. That work includes the 22-wall room and
the Q22 manuscript, which every later direction uses as its positive control.

Daniel set the target and scope on 2026-11-09, narrowed the working goal on 2026-11-17, and
approved every search and cap.

The agent programme (2026-11-09 to 2026-11-18) supported the research. A coordinator agent
ran directions d0 to d69. Opus, Fable, and Astra (Codex) sessions wrote memos, code, and
reviews. Each referee was an independent agent session. The coordinator reran key scripts
and recorded every decision in `coordinator-log.md`.

## 10. Discrepancies between sources

These are disagreements found while writing this record. The statements in sections 1 to 5
follow the more precise source.

1. **Open BBBB range.** `STATE.md` and the 2026-11-18 log entry for d68 give the open
   infinite core as "BBBB, area > 36". d68 itself proves only this: area greater
   than `4r + 4` forces BBBB. OL covers every R\* room with area at least 21, so BBBB rooms with
   area 21 to 36 are also open. No source enumerates or excludes them.
2. **d61 status.** `STATE.md` ("Fold converse") still tags d61's lit direction as
   unreviewed. The next paragraph, and d62, record the review.
3. **d69 room count.** `d69-bbbb/README.md` says "Hand-built (8 rooms)", 743 pairs, and
   "these 8 rooms are hand-picked". Its table of BBBB rooms lists 7, with 726 pairs, as
   does the log.
4. **N_x != B shorthand.** `STATE.md` describes d64's scope as "N_x != B". d64's actual scope
   is `1 < deg N_x < n`. Classes with `N_x = DP` (type Q) are excluded.
5. **d14 uncertified count.** d63 says 6 of the 18 d14 relations lack certificates. d65
   recomputes it as all 18.

## 11. Addendum, 2026-11-18: Q-class closure and later checks

This section records work done after sections 1 to 10 were written. Where it
conflicts with earlier sections, this section takes precedence.

### Q-class closure theorem (Astra)

**Theorem (COMPUTER-ASSISTED; lit side independently sampled).** Let `P` be a
strictly simple orthogonal lattice room. Suppose some parity class has no
interior point and no smooth-wall point in `P`, so all its points are corners.
If `P` has a dark pair of distinct interior lattice points, then `P` has at
least 22 walls. The marks may be in different classes. R22 attains the bound,
so 22 is exact for this class of rooms.

- Finite reduction (PROVED): the d68 counting identity gives area at most
  `(r + 4) + 3r <= 36` for `r <= 8`.
- Computation: 780,565 rooms (261,564 above area 20) and 3,933,192 pairs
  (907,567 same-class, 3,025,625 different-class), all lit. A separate exact
  tracer replays every witness. An independent cell-by-cell census matches the
  room enumeration in all 144 (area, alignment) counts.
- A side run lights all 43,524 lattice pairs in 3,889 d64 covering rooms.
  With d64 and d67, this closes the proper-factor branch for different-class
  pairs too.
- Coordinator check (`d71-check-qclass/`): the audit reproduces the counts.
  d67's tracer, which shares no code with Astra's, lights all 141,882 pairs
  in 20,200 sampled rooms at `max(p, q) <= 20`. R22's dark pair gets no
  witness at `max(p, q) <= 40`. Enumeration completeness was checked by
  reading only.
- Where: `.context/qclass-closure/README.md`, `audit.log`, `compare.log`,
  `reproduce.sh`.

This result supersedes the BBBQ entries in sections 1 and 5. It also closes
gap G1 for every room with a corner-only class.

### Common-cylinder criterion (d72)

**Candidate CC (unproved).** In a BBBB room, some lifts of two distinct
same-class interior marks lie in one open flat cylinder of the doubled
surface, in a rational direction, with no vertex lift inside the cylinder.

- Method (PROVED exact): the test covers the full SL2(Z) orbit of the marked
  origami. It matches direct tracing on 18,446 lifts.
- True BBBB rooms (every `N_x = B`): 747 of 747 pairs in 9 rooms satisfy CC.
- Failures: 11 visible axis-parallel pairs in d64 rooms with a proper factor,
  smallest `cov446` (`W = 18`). The marks lie on a cylinder boundary. A
  closed-cylinder variant covers them. d64 already closes these rooms.
- R22's dark pair fails CC in every direction, as it must.
- No argument links `r <= 8` to cylinder incidence. Agent estimate
  (GUESSED): CC true about 25%, provable about 3%.
- Where: `d72-cylinder-test/README.md`.

### Size of the remaining finite range (d73)

- BBBB rooms with `r <= 8` and area 21 to 36 number about `1e11` to `1e12`
  (GUESSED from d9 growth ratios). Exact: 92,657,242 such rooms at `W <= 12`.
  An exhaustive check would take about 1,000 CPU-hours or more. It wasn't run.
- Corner-only-class rooms (780,565) and proper-factor rooms (2,800) are a
  small fraction. Almost every room in this range is true BBBB, so the open
  case is the generic case.
- Pipeline slice (COMPUTED, not a sample): 31,612 rooms and 1,001,339 pairs,
  all lit, every witness replayed by a second tracer.
- Where: `d73-bbbb-21-36/README.md`, `enum.c`.

### Updated open statement

Same-class and different-class lattice pairs are settled except in BBBB
rooms: rooms where every parity class has an interior or smooth-wall point,
with `r <= 8` and area at least 21. That set is infinite. Computation can't
reach it, and no proof idea has survived. Non-lattice rational marks (G2) and
45-degree rooms also remain open.

### Other Astra notes (2026-11-18, pair-specific)

- `.context/illumination-ninth-corner.md`: replacing one R22 cell with a strip
  of width `w` gives lit widths `w = 4k/7` on both sides of the dark width 1.
- `.context/staircase4991-*.md`: in a 12 by 12 staircase, the pair (1,10) and
  (10,1) is lit for every real middle corner, with explicit routes of at most
  8 bounces. This survives moving each mark up to 1/40.

### Off-grid marks (Astra, 2026-11-19)

- Area-15 theorem (COMPUTER-ASSISTED, one implementation of the continuum
  step): every room of exactly 15 cells with a corner-only parity class and
  fewer than 22 walls lights every pair of distinct interior points, real
  marks included. R22 has 15 cells, so 22 is exact in this family.
- 18-wall rooms with a corner-only class, all areas: 141,885 of 141,887
  cleared for real marks; 2 rooms of 18 cells remain unresolved.
- Doorway lemma: dead-end door pairs are lit when the door width is at least
  half the channel width (one cap) or a quarter (both back walls).
- Where: `.context/qclass-closure/off-grid.md`, `offgrid/`, `offgrid/doorway.md`.
  Audits rerun by the coordinator; the continuum computation itself has no
  independent implementation yet.
- Independent check (d74, 2026-11-19): a separate certifier confirms the
  area-15 theorem on all 6 hard rooms and leaves only R22's known pair in
  R22. Soundness rests on d13's Lemma A' and Theorem C(2), still unreviewed.
- 18-wall closure (Astra, `qclass-closure/two18/`): the last two rooms are
  closed by an endpoint-dependent shear (853 boxes). The coordinator's
  replay reproduces it, but d74's plain cylinder method can't close them, so
  no independent check of the shear step exists yet.

### Long-corridor theorem (Astra, 2026-11-19; reviewed in d75)

- Statement: two fixed orthogonal chambers with doors of equal width `w`,
  joined by an empty straight corridor. Above a length threshold, every
  interior point of one chamber lights every interior point of the other,
  real marks included, with one threshold for all pairs.
- Status: PROVED by hand (Astra), reviewed sound with one minor fixable gap
  (d75). First result that handles unbounded area. DB55: all 496 lattice
  pairs lit at every corridor length of at least 450.
- Open: shrinking doors (d58), turning pairs with no straight corridor
  (cov2929 type), general BBBB rooms.
- Where: `.context/qclass-closure/bbbb/README.md`, `d75-review-corridor/`.

### Corridor follow-ups (Astra, 2026-11-19; reviewed in d76, d77)

- Shrinking doors (`shrinking-door.md`, unreviewed): usable slope width on one
  itinerary is at most w/D; span alone can't close D58's double resonance.
- D58 placement (`placement.md`, reviewed sound in d76): all 8 position types
  of D58's double-resonance builder are lit for every door width 2^-k, k ≥ 2.
  Ten-wall rooms, no dark pair.
- Chain criteria (`chain-criteria.md`, reviewed sound in d77): lattice width
  tests for chains of full rectangular columns. DBw2 dumbbell (5×5 and 5×6
  chambers, width-2 corridor): every interior lattice pair lit for every
  integer corridor length ℓ > 10 (d77 traced all 6,851 pairs at 5 lengths).
- Reversals (`reversal.md`, reviewed sound in d77): turns off vertical walls
  fit the same test. DB55 (1,1)–(9,1) is lit for every corridor length ℓ > 5.
- Limit: these test a named route. They don't show some route works in every
  room.

### Route to the 22-wall bound for large rooms (Astra, 2026-11-20; d78–d80)

- Counting lemma (`midpoint-necessity.md`, reviewed sound in d82 as an
  algebraic lemma): for a same-parity lattice pair with (i) marked valency
  d ≥ 2n/3 and (ii-alg) no regular sheet coincidence at all outside the
  source parity class, r ≥ 9 (from n ≥ 19 with d ≥ ⌈2n/3⌉).
  Equivalently, if r ≤ 8 and d ≥ 2n/3, there are at least
  2⌈2n/3⌉ − 16 − ⌊n/2⌋ such candidates (26 at n = 49).
- Correction (d82): darkness does NOT imply (ii-alg). It only implies that no
  candidate is the midpoint of a real path. Unreached candidates exist (R22's
  source class; cov4181's class d). The route needs an OPEN lemma: in a room
  with r ≤ 8, one of those candidates is reached by a real path.
- Condition (i) from n ≥ 49: d81, reviewed sound with fixable gaps in d82
  (Burness–Guralnick fixed-point-ratio bound, Corollary 2).
- Condition (i), reviewed sound: low-valency.md (d78), three-sheet.md (d78),
  eight-sheet.md (d79). For n ≥ 120 and r ≤ 8, every same-parity interior
  lattice pair is directly visible or has d ≥ n − 8.
- Irrational marks, reviewed sound (d80): `high-valency-geometry.md`. For
  n ≥ 120 and r ≤ 8, any interior pair with an irrational coordinate is lit.
  Wolecki's finiteness theorem plus d16 would give this at every area, but
  d16 §6.4 records a gap in Wolecki's Lemma 2.9 for this case.
- Unreviewed supporting notes: `two-class.md` (cylinder winding changes
  midpoint parity iff one of u, h, C ≢ 0 mod 4), `shortest.md` (one corner
  can block shortest routes in two classes), `fixed-wall.md`, `bottom-step.md`,
  `short-escape.md`, `arithmetic-rigidity.md` (no area bound from corner
  alignments).
- Search plan (`search-plan.md`): no finite reduction exists, so no bounded
  search can prove the W ≤ 20 goal. Census paused.
- Open: condition (ii) for rational pairs at n ≥ 120 (Astra, in progress);
  areas 21–119 (d81, unreviewed: condition (i) holds from n ≥ 49); different-parity pairs; 45-degree rooms.
- Where: `.context/qclass-closure/bbbb/`, `d76`–`d80` review directories.

### Cylinder certificates, shadows and the cover gap (2026-11-20; d83–d86)

- Status note: d81 is now reviewed (d82, sound with fixable gaps), so
  condition (i) holds from n ≥ 49. It stays open for 21 ≤ n ≤ 48.
- Two-cylinder rim test (`adjacent-cylinders.md`, reviewed in d84: sound
  with fixable gaps). If M has exactly two cylinders exchanged by the
  half-turn and the rims pass the interval test, every real pair is lit.
  This closes U2 and all its stretches (areas 46 + 8k). 747/747 saved
  BBBB pairs have off-class midpoints.
- One-cylinder test (`convex-cylinder.md`, reviewed in d84: sound). The
  same conclusion holds when reflex corners occupy at most 2 parity classes.
- Limit (`every-direction.md`, unreviewed). The 12-wall crosses
  [−b,b]×[−2,2] ∪ transpose (odd b ≥ 7, r = 4) fail both whole-room tests
  in every direction, yet are lit. Whole-room cylinder certificates can't
  cover all rooms. `persistent-gaps.md` and `rim-quotient.md` (unreviewed)
  sharpen the rim condition and show that R22's period-10 mechanism
  can't recur at large area.
- Route charging fails (`shared-reflex.md`, unreviewed). One reflex corner
  can block routes with midpoints in all 3 off-classes.
- Blocking set of R22 (`corner-support.md`, unreviewed). Each of the 9
  reflex corners is the sole obstruction of a distinct relaxed route from
  S to T, so all 9 are needed. A filled square of side ≤ 1/12 at any one
  corner lights the pair.
- Lemma stress (d83, unreviewed). The open lemma held in all 11 saved
  single edits of R22 with r ≤ 8. Weak: every room is lit and d = n − 1.
- Shadow kill test (d85, re-run by coordinator). From 2 sources each,
  every point is lit in the crosses b = 7..17 (areas 96–256) and U2
  k = 0..6. R22 control: H(0,0) = {(2,2), (2,−2)}. Short paths are not
  enough: at L = 0.5·diam the unreached count grows from 20 to 60.
- Cover gap (`shadow-budget.md`, reviewed in d86: sound with one fixable
  citation gap; "finite union" needs EMM's theorem on closed invariant
  sets, not the orbit-closure classification). Being lit on Q is
  weaker than reaching the coincidence on the ordered-pair cover U
  (exact cov4181 example). Claimed: a uniform room-level bound B(r) on
  hidden points, from EMM, Filip and Lelièvre–Monteil–Weiss, with no
  explicit constant. Claimed genus bound on U: sum of genera ≥ d − r − 16,
  unbounded at r = 4 (DB55 stretches), so fixed-stratum finiteness can't
  transfer to U.
- Sharpened open target. On U, show the hidden coincidence count is at
  most αn + K with known constants and α < 5/6 (any α < 3/2 for
  n ≥ 120). Reaching one off-class coincidence also suffices for the
  large same-parity cases. d86 notes that for a dark pair this budget
  restates the open lemma numerically; it does not reduce it.
