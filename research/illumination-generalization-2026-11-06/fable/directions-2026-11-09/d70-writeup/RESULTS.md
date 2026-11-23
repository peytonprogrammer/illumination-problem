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
- Status: PROVED, reviewed d101. Translate a corner to the origin before scaling; the map conjugates each wall reflection to the reflection in the image wall. Lattice marks may become non-lattice (handled by G2). Where: `d66-pair-level/README.md` section 2.

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
- The `z = 4` part of `enum_K.c` (3,663 of 4,475 cases) is now independently checked
  (d98): a different enumerator matches it object by object for every `d <= 18`.
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
- Status: PROVED, reviewed d101 (needs strict simplicity; the midpoint may equal S or T).

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

## 11. Addendum, 2026-11-18 to 2026-11-20: current status

This section records work done after sections 1 to 10 were written. Where it
conflicts with earlier sections, this section takes precedence. Paths under
`qclass-closure/` are relative to `.context/`.

### Current status

Target: 22 walls is minimal for a dark pair among strictly simple
square-lattice rooms. Working goal: every pair is lit in every such room with
W ≤ 20. Rooms with a corner-only parity class are closed for lattice pairs,
and for real marks at 15 cells. Lattice pairs of either class are settled
except in BBBB rooms: every parity class has an interior or smooth-wall
point, r ≤ 8, area ≥ 21. That set is infinite, and computation can't reach
it. Reviewed large-area results: condition (i) from n ≥ 49, irrational marks
from n ≥ 120. The core is one open lemma: some off-class candidate is reached
by a real path. G2, different-parity pairs and 45-degree rooms remain open.

### Proved and reviewed

- **Q-class closure** (COMPUTER-ASSISTED; d102: enumerator complete, lit side
  fully replayed by an independent tracer). Let `P` be a strictly simple orthogonal lattice room
  with a parity class whose points are all corners. If `P` has a dark pair of
  distinct interior lattice points, in any classes, then `P` has at least 22
  walls. R22 attains the bound, so 22 is exact for this class.
  - Finite reduction (PROVED; d97: sound): the d68 counting identity gives
    area at most `(r + 4) + 3r <= 36` for `r <= 8`. Needs strict simplicity
    (pinches add a `2·pinch_y` term).
  - Computation: 780,565 rooms (261,564 above area 20) and 3,933,192 pairs
    (907,567 same-class, 3,025,625 different-class), all lit. A separate exact
    tracer replays every witness. An independent cell-by-cell census matches
    the enumeration in all 144 (area, alignment) counts.
  - A side run lights all 43,524 lattice pairs in 3,889 d64 covering rooms,
    which (with d64, d67) closes the proper-factor branch for both classes.
  - d71 reproduces the audit counts. d67's tracer (no shared code) lights all 141,882 pairs in 20,200 sampled rooms at
    `max(p, q) <= 20`. R22's dark pair gets no witness at `max(p, q) <= 40`.
  - d102 (full review): the block enumerator is complete by a line-by-line
    read; an independent polyomino count matches at every area 1–13. d67's
    tracer replays all 3,933,192 witnesses in 780,565 rooms with 0 failures
    (72 CPU s); the corruption control rejects all wrong-target and off-by-one
    witnesses.
    Enumeration completeness was checked by reading only.
  - This supersedes the BBBQ entries in sections 1 and 5, and closes gap G1
    for every room with a corner-only class. Where: `qclass-closure/README.md`,
    `audit.log`, `compare.log`, `reproduce.sh`.
- **Area-15 off-grid theorem** (COMPUTER-ASSISTED; independent check d74).
  Every 15-cell room with a corner-only class and fewer than 22 walls lights
  every pair of distinct interior points, real marks included. R22 has 15
  cells, so 22 is exact in this family. The coordinator reran Astra's audits.
  d74's separate certifier confirms all 6 hard rooms and leaves only R22's
  known pair in R22. d13's Lemma A', Theorem C and cover.c were reviewed
  sound in d96 (1,620/1,620 certified pairs traced legal). Where: `qclass-closure/off-grid.md`,
  `offgrid/`, `d74-continuum-check/`.
- **Long-corridor theorem** (PROVED by hand by Astra; d75: sound, one minor
  fixable gap). Two fixed orthogonal chambers have doors of equal width `w`,
  joined by an empty straight corridor. Above a length threshold, every
  interior point of one chamber lights every interior point of the other.
  Real marks are included, with one threshold for all pairs. First result for
  unbounded area. DB55: all 496 lattice pairs are lit at
  every corridor length of at least 450. Where: `qclass-closure/bbbb/README.md`.
- **D58 placement** (`placement.md`; d76: sound). All 8 position types of
  D58's double-resonance builder are lit for every door width 2^-k, k ≥ 2.
  These are ten-wall rooms with no dark pair.
- **Chain criteria and reversals** (`chain-criteria.md`, `reversal.md`; d77:
  both sound). Lattice width tests cover chains of full rectangular columns;
  turns off vertical walls fit the same test. In the DBw2 dumbbell (5×5 and 5×6
  chambers, width-2 corridor), every interior lattice pair is lit for every
  integer corridor length ℓ > 10. d77 traced all 6,851 pairs at 5 lengths.
  DB55 (1,1)–(9,1) is lit for every corridor length ℓ > 5.
- **Condition (i)** (d ≥ 2n/3 unless directly visible). For n ≥ 120 and
  r ≤ 8, every same-parity interior lattice pair is directly visible or has
  d ≥ n − 8 (`low-valency.md`, `three-sheet.md`: d78; `eight-sheet.md`: d79).
  d81 extends (i) to n ≥ 49 (d82: sound with fixable gaps), using the
  Burness–Guralnick fixed-point-ratio bound, Corollary 2.
- **Counting lemma** (`midpoint-necessity.md`; d82: sound as an algebraic
  lemma). Take a same-parity lattice pair with (i) d ≥ 2n/3 and (ii-alg) no
  regular sheet coincidence at all outside the source parity class. Then
  r ≥ 9 (from n ≥ 19 with d ≥ ⌈2n/3⌉). Equivalently, if r ≤ 8 and d ≥ 2n/3,
  there are at least 2⌈2n/3⌉ − 16 − ⌊n/2⌋ such candidates (26 at n = 49).
  Darkness doesn't imply (ii-alg); see "Open core".
- **Irrational marks** (`high-valency-geometry.md`; d80: sound). For n ≥ 120
  and r ≤ 8, any interior pair with an irrational coordinate is lit.
  Wolecki's finiteness theorem plus d16 would give this at every area. But
  d16 §6.4 records a gap in Wolecki's Lemma 2.9 for this case.
- **Cylinder tests** (d84). Two-cylinder rim test (`adjacent-cylinders.md`,
  sound with fixable gaps): suppose M has exactly two cylinders exchanged by
  the half-turn. If the rims pass the interval test, every real pair is lit. This
  closes U2 and all its stretches (areas 46 + 8k). One-cylinder test
  (`convex-cylinder.md`, sound): the same holds when reflex corners occupy at
  most 2 parity classes. All 747 saved BBBB pairs have off-class midpoints.
- **Cover gap** (`shadow-budget.md`; d86: sound, one fixable citation gap).
  Being lit on Q is weaker than reaching the coincidence on the ordered-pair
  cover U (exact cov4181 example). A uniform room-level bound B(r) on hidden
  points follows from EMM, Filip and Lelièvre–Monteil–Weiss, with no explicit
  constant. "Finite union" needs EMM's theorem on closed invariant sets, not
  the orbit-closure classification. On U, the sum of genera is at least
  d − r − 16, unbounded at r = 4 (DB55 stretches).
- **Every-direction limit** (`every-direction.md`; d87: sound). The 12-wall
  crosses [−b,b]×[−2,2] ∪ transpose (odd b ≥ 7, r = 4) fail both whole-room
  cylinder tests in every rational direction (parity counts (−4,4,4,0); no
  level sums to 2). The note proves one pair lit, (6,0)–(0,6), for all odd b.
  "All pairs lit" is only finite evidence: d87 lit all same-parity interior
  lattice pairs at b = 7, 9, 11; d85 lit everything from 2 sources per cross.
- **Blocking set of R22** (`corner-support.md`; d87: sound, one fixable gap
  in a side paragraph on cov4181). Each of the 9 reflex corners is the sole
  obstruction of a distinct relaxed route from S to T, so all 9 are needed.
  A filled square of side ≤ 1/12 at any one corner lights the pair. d87
  replayed all 9 rows with its own tracer.
- **Bounded denominators** (`dark-locus.md`; d89: sound with fixable gaps;
  conditional on d80). For each r ≤ 8 there is an integer D(r), with no
  explicit value, such that in every room with n ≥ 120, dark-pair
  coordinates have denominators dividing D(r). An unbounded counterexample
  sequence must lie in a proper rank 2–5 family with four periodic marks.
  No gain for same-parity lattice pairs (denominator already 1).
- **18-wall Q-class closure** (`qclass-closure/off-grid.md`, `two18/`;
  COMPUTER-ASSISTED; shear step independently checked in d90). Every 18-wall
  room with a corner-only class, all areas, lights every pair of distinct
  interior points, real marks included. 141,885 of 141,887 rooms clear by
  cylinders (d74). The last two (18 cells each) close by an
  endpoint-dependent shear: d90's own exact checker accepts all 144 trees
  and 853 boxes and traced 240 random pairs (K up to 171). Gaps: labels are
  compared up to the half-turn (implicit in the README). d100 re-derived
  the residual with independent code: the same 36 open tile pairs, every
  vertex within 1/17 of its grid point (the shear-covered box), 300/300
  sampled pairs inside census products, 100 large-K traces (K up to 98)
  lit, and a B = 8 negative control that fails as expected.
- **Route B bookkeeping** (`stabilizer-orbits.md`, `axial-stabilizers.md`;
  d91: both sound). Affine maps fixing a source lift carry dark target lifts
  to dark target lifts. On the 12-wall cross, the two axial cusp stabilizers
  act only through the derivative kernel (|orbit| ≤ 4), so the axial version
  of route B is dead. The full affine stabilizer does grow: |G_s·t| = 36 at
  b = 7 and 52 at b = 9 (d91 exact Veech-group enumeration; n/2 − 12 is a
  fit, not a theorem). Open: universal growth, and B(r) is non-effective.
- **Mirror suborbit, route B′** (`mirror-suborbit.md`; d92: sound, one
  fixable gap in the finiteness reason). If S has a dark partner, its mirror
  orbit e(S) under the full stabilizer satisfies 2e(S) ≤ B(r)(B(r)−1).
  e(S) ≥ max(u,v)/gcd(u,v) from mirror-conjugate shear periods. Axis marks
  have e ≤ 3; off-axis cross marks reach e = 40–44 at b = 7. In R22 the
  points hidden from (0,0) are exactly the stabilizer orbit {t, ιt, (2,−2)}.
  No area cutoff: B(r) has no value, and no growth theorem exists.
- **Small orbit blocks** (`small-orbit-blocks.md`; d93: sound). Darkness
  bounds mirror orbits at both endpoints (non-effective). An exact test
  recognizes an intermediate cover from two point blocks: on R22 it
  recovers the staircase fold (block sizes 15, 3, 15, 15; the 5×3 system is
  the only nontrivial block system of the order-233,280 monodromy group).
  The K_{3,3}/cube graph lemma doesn't use darkness; the cubic single-orbit
  hypothesis is verified only for R22.
- **Fold transport** (`canonical-transfer.md`, `fiber-transport.md`; d94:
  sound). Recovered folds need not give a proper canonical factor: the odd
  cross (b = 7, 9, 11) is BBBB with a proper deck quotient Q/K (|K| = 4).
  Darkness upstairs forces conditions downstairs (degree-3 pigeonhole,
  degree-4 cube matching); the converse lifting fails through poles.
- **Primitive/imprimitive split** (`primitive-stabilizer.md`,
  `bbbb-split.md`; d99: no error, little new). Primitive BBBB rooms with
  n ≥ 49 have sheet group ⊇ A_n (Burness–Guralnick on g_x², supp ≤ 24).
  The n ≥ 73 step reduces to d92's mirror-suborbit question. Bounded
  orbits descend to every intermediate quotient (a sphere with ≤ 8 poles;
  degree-2 loss ≤ 56). The degree-2 constraint excludes nothing without a
  growth theorem. Neither half closes.
- **Small P1 lemmas** (d101: sound, wording fixes only). Normalization
  (Q07) needs a translation first. Lemma MP (Q08) needs strict
  simplicity; the midpoint can equal S or T. Checks: 200 saved
  witnesses and 1,089 lit paths in R22 and 29 edits, 0 violations.
  d81 findings 5–6 (Q09) are wording; the n ≥ 49 threshold stands.
- **Large dark-pair profile** (`large-dark-profile.md`; d104: rows sound,
  counts 26 and 148 exact). No combination of reviewed conditions gives a
  contradiction. Its "minimal missing statement" restates the core at
  n ≥ 120 only; it is not a reduction. Rows 4–5 depend on d80.
- **Single-fixed-corner converse to Tokarsky: false** (`tokarsky-converse.md`,
  unreviewed, Q47). In R22, different paths are blocked at different
  corners for every lift choice; the obstruction is collective.
- **Fold mechanism needs r ≥ 9** (`fold-converse.md`; d105: sound with one
  fixable gap). An R22-type parity fold (inner degree k ≥ 2, outer m > 1,
  all three off-classes corner-only in N) forces r ≥ 9. Gap: the
  hypothesis must include separation of the S-images from the T-images
  (the certificate supplies it). Proper-fold necessity is false: R34-base
  is dark by parity on its own prime-degree-19 double. Scope: a BBBB room
  admits no such fold at any r, so this adds nothing to the open core; at
  r ≤ 8 it reproves, without the census, what d102 plus d64 already close.
- **Chain map** (`chain-map.md`; d106: sound, removes nothing). The
  sublattice count is right (n > 2r + 2 gives a cell with ≥ 3 regular
  corners), but excluding R34-type parity darkness is already the
  definition of BBBB. Twist-overlap criterion: one multitwist lights the
  pair iff the two visit times overlap mod gcd(u, v) (CRT; 40,000 brute
  cases agree). It is a certificate format with no witness yet. Any dark
  BBBB pair must be dark for positional, not residue, reasons.
- **Axial band reachability is false** (`band-reachability.md`; d109:
  sound). DBas (strictly simple BBBB, W = 12, r = 4, n = 48): both axial
  twists fix every lift of (1,3) and (11,3), so no twist word reaches a
  band pair; yet the pair is lit by a two-reflection shot (7,−2) (exact).
  The lengthened family stays twist-fixed at all 64 primes n = 44 + ℓ ≤ 400
  and stays lit (doorway slope for n > 89; n = 67, 73, 89 lit leftward).
  Kills axial-only reachability; nonaxial twists and itinerary criteria
  remain open.
- **Wall-width test and DB55 stretches** (`twist-overlap.md`; d108: sound
  with fixes). If twisted marks sit in two bands across a seam (same
  vertical sheet), darkness requires (a + b)w ≤ gcd(2bW₀, 2aW₁). DB55
  witness confirmed exactly. Corollary (repaired: choose the second
  mark's horizontal lift freely): in every DB55 stretch with corridor
  length ℓ coprime to 5, every same-class interior lattice pair is lit
  (all 64 cross-chamber pairs at ℓ = 3, 7, 9, 21, 451, 457). These rooms
  are BBBB with r = 4: the first infinite open-core family closed for
  lattice pairs. ℓ ≡ 0 (mod 5) stays open.
- **Corridor length** (`length-periodicity.md`; d110: sound). Bounded-order
  partial shears fail (DBas directions (7 + 1040j, −2) need insertion
  period 7 + 1040j). Explicit period-one tail: two rectangular chambers
  joined by a corridor of length L ≥ K light every real cross pair; K =
  1,127,680 (DBas), 736,160 (DB55), 595,360 (DBw2); with unit door every
  lattice pair (180/180 DBas pairs traced at L = K). DBas's marked pair is
  lit at every L ≥ 2. Open: L < K, collars for w ≥ 2, nonrectangular
  chambers, rooms without one separating corridor, and a shortening move
  that keeps a dark pair.
- **Thin-door theorem** (`thick-thin.md`; d111: sound). Rectangular
  dumbbells with L ≥ 2d: if the aspect ratios have irrational quotient (or
  one mark's offset is an irrational fraction of its depth), every real
  cross pair is lit at every door width (Kronecker; 25/25 Q(√2) witnesses).
  Some lit pairs need unboundedly many reflections as w → 0, so finite word
  covers fail at that boundary. The thick-part reduction is a sound
  conditional (openness holds since rays die at corners). Removes nothing
  from the core: lattice pairs are the triply rational exception.
- **Rectangular dumbbells, L > 4d** (`resonant-gluing.md`; d112: sound).
  Two rectangular chambers joined by a straight corridor longer than 4×
  the larger depth light every pair of real interior points, at any door
  width, resonance included (monotone first-hit mismatch, only downward
  jumps; 2,676 cross pairs and 900/900 chamber–corridor pairs traced).
  Threshold 21 for DBas, DB55, DBw2 (was 595,360–1,127,680). Covers DB55
  ℓ ≡ 0 (mod 5) from ℓ = 25. Also: exact gluing equation for arbitrary
  orthogonal chambers, common slope period, and a polynomial bound for
  expanding chambers (cross pairs). Open: L ≤ 4d, contracting chambers,
  rooms without one separating corridor, multi-traversal paths.
- **One-launch monotonicity fails** (`general-gluing.md`; d113: correct).
  In a strictly simple BBBB room (W = 20, r = 8, n = 142) the first-door
  mismatch for (2,47)–(10,3) jumps 130/33 → 136/33 at slope 43/33 (graze
  at corner (3,4)), skipping 4; it persists at every corridor length. The
  pair is still lit (4 of 12 candidate rays, e.g. slope 31/23 upward).
  The corridor-or-compact dichotomy also fails: odd crosses (BBBB, r = 4)
  have unbounded gap ratios with capped arms, not corridors. The compact
  covering problem (≤ 20 real variables) still needs ε, a word bound and
  near-wall handling. Multi-launch counting arguments remain open.
- **Cap doubling; no local cancellation** (`degree-gluing.md`; d114:
  sound, one wrong number). A long capped arm on a fixed hub reflects to a
  corridor in the unfolding, so the corridor theorems apply (18 folded
  paths on P_7, P_9 legal; needs strict simplicity of the joined room;
  threshold not yet computable). At a reflex graze the 3π cone gives two
  distinct germs, so there is no local cancellation lemma; the degree
  identity with its jump term is correct. The 43/33 pair is lit at every
  L = 4 + 66k (traced k ≤ 1000; corrected root 6 + 86k). Nothing in the
  BBBB core closes.
- **Accumulation** (`accumulation.md`; d115: sound, conditional on d89 and
  through it on d80). If dark same-parity lattice pairs occur at unbounded
  n with r ≤ 8, then dark pairs occur in rooms of one fixed integer height.
  They sit on a rational one-axis dark deformation line through a strictly
  simple room. The note proves darkness for small |t|; the whole physical
  component is dark by an argument the note omits. Nonproportional strip
  routes are excluded at transcendental t. Open crux: find a lit parameter
  on every nonradial one-axis dark line in a d89 locus. Literature inputs
  (EMM, Filip, Apisa–Wright) are from memory (Q11).
- **Generic line** (`generic-line.md`; d116: sound with fixable gaps). On a
  rational one-axis deformation line with fixed rational ordinates, every
  irrational parameter's marked orbit closure contains the whole strictly
  simple component. So a component is wholly dark, or its dark parameters
  are a locally finite set of rationals. EMM 2.1–2.2 and LMW §2 were checked
  against the papers. Fixes: define the dark set in the marked stratum and
  show lit is open; the Decision section should say "rational", not
  "algebraic". Remaining crux: rule out a wholly dark component.
- **Component ends** (`component-ends.md`; d117: sound with fixable gaps).
  Lighting is open, and limiting witnesses persist. A single-point pinch
  sealing both marks in one chamber transfers darkness to that chamber.
  cov279 (BBBB, r = 6) needs unboundedly many reflections as its opening
  closes; exact shots at t = 3/(12m+4) use 4m reflections (replayed m ≤ 8).
  Opposite-lip theorem: no wholly dark component when the access legs share
  no proportional width (at most one leg may use a constant-width run).
  Open: shared width class, marks hidden from the contact, slit or
  simultaneous contacts, scar-only wall collapses, mark-at-boundary cases.
- **Convex corners are regular; indispensable stops** (`eight-stop-consult.md`;
  d118: sound with fixable gaps). A legal physical shot exists iff some
  pair of lifts is joined in the four-copy unfolding by a segment avoiding
  reflex zeros; convex-corner lifts may be crossed (trimming argument). A
  reflex C is an indispensable stop iff corner-free legs C→S and C→T have
  launch velocities with equal absolute components. R34 forces three stops
  (existence only; no explicit route). No bearing on BBBB: R34 has a
  corner-only class.
- **Minimal quotient** (`minimal-quotient-rigidity.md`; d119: sound with
  fixable gaps). At an irrational parameter on a wholly dark component, the
  room double maps to its minimal quadratic quotient with degree 1 or 2;
  degree 2 occurs only at r = 6 or 8 (Riemann–Hurwitz matches d22). Mark
  motion is always a rational combination of three periods, so rigidity
  gives no contradiction. Excluding z ≤ 2 (d121: established with fixable
  gaps): the enumeration is complete; 20 saved slices replay with
  identical verdicts; d23 Lemma 2 is correct but not needed here, since
  the three dark families have c₂ = 2 < 4. Open (high): no LIT witness
  segment is saved, and independent code checked only (k, z) = (4, 1).
  Smallest open case: a proper rank-two locus in Q(1³, −1⁷).
- **Rank-two periodic marks** (`rank-two-periodic.md`; d120: sound with
  fixable gaps). Over a rank-two locus, a periodic mark is a persistent
  torsion branch in an associated abelian surface (Filip Thm 5.2), and the
  surface varies in three dimensions. In the degree-two branch, a dark
  pair needs a regular periodic image distinct from its mirror. The
  referee supplied the one-interval axis proof that d99 had only asserted.
  The real question is whether a proper rank-two locus exists in these
  genus-zero strata at all; Apisa expects not.
- **Three zeros, partial** (`three-zero-boundary.md`, `-divisor.md`,
  `-recognition.md`; d122: sound with fixable gaps). For a hypothetical
  rational rank-two M in Q(1³, −1⁷): every boundary is cylinder rigid
  (Apisa); there is no isolated zero–pole divisor (one-cylinder tree
  argument); a synchronized hexagon of two matchings with equal periods
  forces a degree-3 cover of genus 2 (6-vs-9 singularity count; sharp on an
  explicit model). Open: a minimal M must have a coupled zero–pole
  degeneration (codimension-two Apisa Prop. 4.3), the periods must be
  equal, and the second matching must be disjoint. z = 3 parked.
- **Three-zero monodromy** (`three-zero-monodromy.md`; d123: sound with
  fixable gaps). Two hexagonal triple collapses give weights (1,1,1) or
  additive weights. The pole count inside the hexagon decides the form:
  even gives I−R (additive needs distinct weights, e.g. (1,2,3)/(1,4,5));
  odd gives I+R (the 1:1:2 family lives here). In Q(1^s, −1^(s+4)), rel = 0,
  so a rank-h boundary has rank ≤ h−1 (Mirzakhani–Wright Cor. 1.2): no
  same-rank induction. Citation fix: Wright is arXiv:1302.4108.
- **Effective corridor for arbitrary chambers** (`effective-chamber.md`;
  d124: sound, low gaps). Two strictly simple lattice chambers with equal
  vertical mouths of width w, joined by a straight corridor of length
  L ≥ 4wT² (T = 1 + F_(3m−1), m = 4·max area), light every cross-chamber
  interior lattice pair, with no parity, reflex or monotonicity hypothesis.
  All real cross pairs are lit at L ≥ 36wH². A capped arm needs ℓ ≥ 18wH²
  (two junction marks) or 36wH² (one door). Replayed at exact L: 180/180
  DBas, 256/256 DB55, 320/320 DBw2 pairs. Thresholds are 120–151 digits
  (219,024 / 32,400 / 168,200 with direct indices). The census at about
  54,000 witnesses per second is 512–5,120 CPU-hours for the conditional
  n ≤ (K+32)/ε. No universal cutoff yet.
- **Large-rectangle access** (`large-rectangle-access.md`,
  `rectangle-windings.md`; d125: sound with fixable gaps). Opposite doors:
  explicit H₀ = 8wPQ^d (independent of W and door heights). Perpendicular
  doors: torus-winding lemma sound; thresholds explicit only for rational
  normalized door positions, so none in lattice rooms. Shared-corner
  "obstruction" is to normalized clearance only: a one-winding legal path
  exists at H = 10³, 10⁹, 2²⁰⁰. H₀ ≥ 2⁷⁹·w, so any n₀ built this way is far
  beyond census reach. Missing (high): a decomposition theorem for large
  rooms, and perpendicular doors at fixed physical distance from corners.
- **Whole-room decomposition** (`whole-room-decomposition.md`; d126: sound,
  one medium gap). Parallel cuts give a tree of ≤ r+1 rectangles with one
  door per attachment. A piece deeper than Z = 4HT² with one closed end
  lights the whole room (area cutoff n ≥ rB + 4D²T²). Obstruction to the
  method, not to the problem: the cov279 stretch (BBBB, r = 6, 16 walls,
  area 13q+3, height 6, width 6q) has no piece meeting any such threshold,
  even with the computed k*, for all q ≥ 522. A new lemma must replace the
  single common slope interval. Only one cov279 pair is known lit (d117).
- **cov279 stretches, all pairs** (`thin-room.md`; d127: sound, low gaps).
  In every cov279 stretch with q ≥ 4 and 3 ∤ q (BBBB, r = 6, 16 walls,
  height 6, width 6q), every same-parity interior lattice pair is lit.
  Certificates: Bézout two-band shots plus a four-band crossing whose final
  gcd is gcd(12q, 4q+6) = 2. Independent tracer, all pairs, 0 failures:
  2,182 (q = 16), 6,922 (28), 52,522 (76), 91,306 (100). When 3 | q the
  certificates fail on some pairs (62/267 at q = 6); lighting open there.
  First infinite open-core family inside W ≤ 20 closed for all lattice pairs.
- **Band absorption** (`band-absorption.md`; d128: sound, low gaps). Exact
  test: with leg-preserving shift P = lcm(2uᵢ/dᵢ), a middle band of width u
  and depth d absorbs an even mismatch F iff F ∈ gcd(dP, 2u)ℤ. The choice of
  band matters (cov279: g = 2 versus g = 2q). CRT places legs on chains with
  pairwise coprime widths; slope ≤ 2U⁹ for ≤ 9 bands (traced on a 16-wall
  staircase). Odd crosses keep every contained rectangle's short side ≤ 4,
  so band height does not split thin from fat.
- **No fixed direction menu** (`thin-gap-periods.md`; d129: sound, medium
  gap on scope). In the τ = 5, r = 4 dumbbell, for every B some lit pair has
  every direction with |p| ≤ B stopped at a reflex lip, yet (a+1, 1) lights
  it with one reflection. So no width-independent finite menu proves the thin
  theorem for τ₀ ≥ 5 (τ₀ < 5 unproved). Fixed-menu visibility is periodic in
  long gaps (period 2|p|·lcm(1..⌊τ₀⌋)).
- **No reflection bound** (`reflection-complexity.md`; d130: sound, gaps).
  In cov279 (τ = 3, r = 6) some lit pairs need R+1 ≥ √q/12 reflections on
  every legal path (observed about q/3); in st279 fat pairs need Ω(√m)
  (explicit only from k ≈ 128, about √m/384). Refutes any R(τ₀, r) with
  τ₀ ≥ 3. Replay: 62 thin and 6 fat witnesses, determinant identities exact,
  no shorter path up to 8–10 reflections.
- **No passage bound, horizontal decomposition** (`passage-complexity.md`;
  d131: sound, gaps). In st279 end-square stretches, Ω(√m) targets at one
  height are lit (all but B(6)) and each needs Ω(√m) horizontal-band
  passages; a slope shift by 24 compresses k passages to ≤ 26k reflections.
  Vertical or mixed decompositions are open (witnesses with 5–9 vertical
  passages at m ≤ 128). The bound beats k ≥ 4 only for m ≳ 1.1×10⁸.
- **Primitive dark flats** (`primitive-dark-flats.md`; d133: sound, gaps;
  conditional on the finite-flat theorem under review in d132). Axis
  stretching preserves darkness, so a maximal dark flat splits into x and y
  factors. Primitive same-parity witnesses are decidable per factor (finite
  in rank one; Smith form gives a progression in rank ≥ 2). A coefficient
  bound H would reduce primitive same-parity lattice marks to finitely many
  tests. Not covered: non-primitive or half-integer marks, different-parity
  pairs, small-area irrational marks, and 45° walls (stretching fails).
- **Finite-flat theorem** (`parametric-orbits.md`; d132: sound logic, one
  HIGH citation gap). On each rational polyhedral cell the dark set is a
  finite union of affine flats (o-minimal finiteness), so integral darkness
  is Presburger definable; the flats need not be rational. Existence only:
  no bound, no equations, no decision. HIGH gap: Filip Thm 5.4 covers strata
  with zeros only; algebraicity with regular marked points has no located
  source (affects the d86/d116 uses too). Replay: cov279 lit iff
  gcd(u, v) = 1; st279 lit iff p ≡ ±4 (mod m).
- **Marked-stratum algebraicity** (`marked-algebraicity.md`; d134: sound,
  medium gaps, none high). A cyclic triple cover turns regular marks into
  zeros; Filip 5.4 upstairs and finite descent make each marked invariant
  locus a whole component of an algebraic image. Closes d132 gap 1. No
  published statement of this case exists (LMW asserts it in one sentence).
  Still open: d132 gap 2 (semialgebraic parameter map); d116's marked
  quadratic stratum also needs Filip's Remark 1.6 double cover.
- **Finite-flat theorem for 45° walls** (`parametric-orbits.md` revision;
  d135: sound, gaps, none high). The doubled mixed room carries a quartic
  differential whose fourth-root cover is the 8-copy unfolding; cells have
  denominator 2 and linear periods, so the o-minimal and Presburger steps
  carry over. Cone data and genus replayed on 4 named rooms. 135° convex
  corners lift to order-2 zeros, so "convex corners are regular" fails there.
  The cyclic-cover family is sketched (same as d132 gap 2).
- **Reciprocal resonance** (`reciprocal-resonance.md`; d136: algebra sound,
  HIGH gap). The conditional height bound H (given a uniform resonance bound
  M and factor dimensions) is correct, but the rank test is only sufficient
  and unattainable: it needs ab − jₓjᵧ identities, and two tree routes give
  at most 72 at W ≤ 20 (named rooms: 4 against 38–40). M is not uniform
  (> 1.8×10⁷ at cov279 q = 16, growing). Even granted, the census is about
  10^(4.3×10⁵) pairs per cell. The explicit-H census route is not viable.
- **Corner-orbit rigidity** (`corner-orbit-rigidity.md`; d137: sound, HIGH
  scope gap). A first-order transverse motion of an unfolded forbidden corner
  opens a path for one sign, so dark flats satisfy linear corner equations;
  Veech orbits make the test finite. Replayed on L, dumbbell (U = 4), R22 and
  a mixed V-notch: kernels are translations plus scalings (anchored dim 2
  axial, 1 mixed). Rigidity is generic (3 of 4 rigid seeds are lit), so it
  gives no area bound; all weight falls on bounding rigid dark rooms.
- **Rigidity and area** (`rigidity-area.md`; d138: sound, gaps, none high).
  d39's area-20 bound covers only essential-Rig certificates. A dark flat
  with a primitive seed and two rational wall motions gives unbounded-area
  dark rooms converging to a thick strictly simple room. Area = c·d/8 for
  mixed rooms (c·d/4 for orthogonal ones). **Census coverage gap:** the
  canonical45 census (d11) cannot represent mixed rooms whose two diagonal
  intercepts have different parities, at any N; e.g. M = (0,0),(3,0),(4,1),
  (4,2),(2,4),(0,4), area 27/2, is covered by neither d9 nor d11.
- **Diagonal periods** (`diagonal-periods.md`; d139: sound, gaps, none
  high). (x,y) → (x−y, x+y) maps mixed-parity diagonal rooms to canonical45
  rooms of twice the area (minimal for scalar-primitive rooms) and preserves
  legal paths. So d11 covers this class only through original area 8; area
  20 needs A/B pairs at N = 34–80, plus A–B pairs at every N. Absolute
  periods form the checkerboard lattice (index 2) in this class; canonical
  rooms with one corner colour have no single degree formula.
- **Half-turn fibers** (`half-turn-fibers.md`; d140: sound, gaps, none
  high). On abstract marked square-tiled surfaces there is no bound
  d ≤ f(g, n): with h = (0 1 … p−1), v = (0 1) (genus 2, S_p monodromy), a
  point and its half-turn image are dark because every joining segment has
  a forbidden midpoint; an 8×8 genus-9 version is all-64-dark with every
  intermediate cover of ≥ p blocks. Not a room: two marks fold to an
  interior non-corner point. In rooms this needs a hidden symmetry.
- **Free half-turns** (`free-half-turns.md`; d141: sound, gaps, none high).
  On a mixed room's 8-copy unfolding X, free −I involutions are exactly lifts
  of physical reflections across vertex-to-vertex symmetry axes; the
  midpoint argument blocks at most 1 of 8 target lifts. Checked on 6 named
  rooms, including hidden symmetries (V-notch: translation group S3, 4
  non-physical −I maps, none a free involution). Holds on X only: quotients
  of X by hidden translations can carry free half-turns (V-notch, octagon).
- **No common-quotient midpoint fold** (`two-image-midpoints.md`; d142:
  sound, gaps, none high). No single translation quotient blocks all
  source–target lift pairs by half-turns, even with a different half-turn
  per pairing; the proof actually works through W ≤ 23 and first fails at
  W = 24. It covers the hidden-translation quotients (V-notch X/C₃ forces
  coinciding images; the octagon quotient is elliptic). Replay: in 61 cases
  no quotient blocks more than 8 of 64 lift pairs. R22's darkness is a
  path-dependent 2-adic parity argument, not a midpoint fold.
- **Dyadic classes** (`dyadic-classes.md`; d144: sound, low gaps). In
  cov4181 (W = 20, r = 8, 28 cells) the lit pair (2,3)–(4,3) realizes only
  primitive class (1,0): (1,1) has no regular site (all 14 parity-(1,0)
  lattice points are corners), and (0,1) is excluded by the complete orbit
  (3,888 states, independent replay). So "every class is realized" is false
  at W = 20. R22's halved displacement D/2^j is an odd multiple of v. The
  halving depth of a witness is ≤ ⌊log₂(4n)⌋ in an n-cell room.
- **Per-class midpoint relay** (`per-class-relay.md`; d143: sound, gaps,
  none high). Two-site blocking lemma correct (3,360 lattice cases); in fact
  one site per class suffices (holonomy mod 2Λ). V-notch and octagon checked
  over every translation quotient: none carries more than one involution
  whose fixed points are all forbidden. R22 is not explained by any midpoint
  test (only 4 of 16 cases blocked, by a site carrying only corners); its
  proof is a developed-path argument.
- **Clean-site cost** (`clean-site-cost.md`; d145: sound, gaps, none high).
  In R22 a corner-only site (6 convex, 3 reflex) blocks 4 of 16 cases, and
  each of R22's 6 axial reflexes is indispensable for the rest (routes
  replayed independently; they certify only 4 of the 12 residual cells). A
  corner-only site costs a full fiber, n = f_x + 3r_x (d68 Cor. C). Fold
  ramification budget Σ(q_x + 2(r_x mod k)) ≤ 2k − 2. BBBB rooms have no
  corner-only fiber (d68 Lemma B). No wall lower bound for BBBB follows.
- **d146 (exclusion-descent, sound with gaps).** cov4181's (0,1) exclusion factors through its unique
  proper quotient N (4 blocks of 7). The S/T images are the two singletons of A, the S4 lemma holds in all
  1,728 product-relation solutions, and all 10 class-(0,1) arcs separate S from T in Q, so corner-continued
  routes are excluded too. The 7 c-zero reflexes are exactly the parity-c reflexes. Five named BBBB rooms
  have no factor of outer degree 2-4; the odd cross b=7 has degree-24/48 factors with mixed 2/3-cycle sites.
  MEDIUM gap: claim (4) needs every canonical relation B_x universal (the project's BBBB definition), not just
  'no corner-only site'. Degree >= 5 stays open; counting doesn't exclude a degree-5 sphere factor.
- **d147 (cross-factor-arcs, sound with gaps).** Independent code reproduces every count on the b=7 odd
  cross. The twist-residue dictionary and label closure are exact; the 2-cycle-only identity-cover slices
  equal billiard reachability along explicit slopes (3 witnesses unfolded). The reviewer lit all 16
  identity residuals in their specified class via out-of-pencil slopes, e.g. (-2,5), so all four factors
  connect 1,722/1,722, and all 2,346 interior pairs of the cross (incl. 1,772 mixed-parity) are lit.
  Gaps: twist-power-to-slope map unstated (medium); 'Riemann-Hurwitz' bound is Euler V-E (low).
  Named-room result only; no degree bound for general factors.
- **d148 (deletion-invariance, sound with gaps).** The DB55 counterexample is correct but pencil-only:
  direction (3,2) lights S=(2,2) -> T=(10,2), and 128 horizontal-class lines with |p|,|q|<=25 reach T. So
  DB55 refutes only the pencil-restricted deletion-invariance implication. The single-arc <A^3,D^3>
  theorem matches direct ray unfolding in 79,724 rows over 4,496 residue slices, 0 mismatches. All 272
  same-parity pairs on DB55, DBas, U2 and stretched cov4181 (c4181s, 41 cells) are lit in all 3 classes.
  The class-level deletion-invariance statement remains open; the formal statement is in review.md.
- **d149 (cyclic-separation, sound with gaps).** The all-slope cyclic criterion (L = A^3X^3 per slope)
  matches direct billiard on all 336 DB55 reference-slope rows, 0 disagreements; 52 rows connect only with
  corner continuation. For (2,2)-(10,2), no cusp mixes lit and unlit slopes: 720 slopes up to height 24 in
  the review run, and 1,960 slopes in the coordinator re-run. The checker's coverage depends on timing, so the
  counts differ while the conclusion matches; the re-run log is in checks.rerun.log. Finiteness holds per
  room but is impractical: index > 100,000, cusp widths up to 702. No illumination theorem; two-class stays open.
- **d150 (class-repair, sound with gaps).** Both repair criteria are exact: fixed-crossing iff in 483,296
  exhaustive cases; sliding test agrees with the billiard tracer on 5,720 residues and equals visibility of
  the target through the developed open seam windows. DB55 cylinder data confirmed (height 1, circumference
  26; all 119 other-class shots to h=40 cross it). Sliding along a fixed route does repair class on DB55
  (e.g. (-32,12) and (-42,12) share 8 legs). Existence gap unchanged: nothing bounds h.
- **d151 (local-global, sound with gaps).** One legal shot gives positive lower density in its marked affine
  orbit; needs finite index only, so it holds for noncongruence Veech groups. DB55 S=(2,2), T=(4,4): (1,2j)
  lit iff 5 does not divide j for |j|<=60, refuting direction-mod-N tests with N coprime to 5 (incl. 2^k). The 5
  is the side of the left 5x5 box. Schmithuesen citation supports noncongruence. Proof covers exact legality only.
- **d152 (uniform-tail, sound with gaps).** Dilation lemma correct: a uniform period-one cutoff for real
  marks forces corridor-length invariance from L=1. HIGH: the uniform hypothesis is already false at W=22.
  R22 is dark at arm length 1 and fully lit at long arms (d114/d124), and lattice darkness flips at arm
  length 2 (R22-L1-007, -012, -025). The 20-wall three-chamber room (W=20, strictly simple, BBBB for k>=6)
  defeats the corridor-induction thresholds. One-way descent (dark long => dark short) is not contradicted.
- **d153 (parity-shortening, sound with gaps).** Independent tracer confirms: in the 20-wall three-chamber
  room, line (2,1) hits a corner at X=Y=28 but reaches T at X=26, both mark parities kept; least period 4
  (12 keeps normalization). Shortening by 2 drops q 37->36 and n 83->81 at each site, corners fixed, so the
  monodromy changes. Refutes only fixed-direction monotonicity; the pair is lit at both lengths, so darkness
  descent stays open.
- **d154 (r22-arm-descent, sound with gaps).** Both gap lemmas are correct for normalized orthogonal rooms:
  a corner-only parity fiber forces wall-line gaps <= 2, and a proper clean quotient forces gaps <= 4r-2. The R22
  arm claims hold. HIGH: the known certificate types are already closed below 22 walls (corner-only by the
  all-area theorem, proper factors by d64), so 'known-certificate dark rooms with W<=20' is empty. The open
  problem is exactly certificate completeness. HIGH: the lemmas fail with 45-degree walls (V-notch B: r=1, gap 4,
  four clean torus sites).
- **d155 (all-factor-first-shot, sound with gaps).** The 45-degree clean-site area bound holds exactly in 12
  named mixed rooms on the d135 8-copy torus; V-notch attains equality. In integral-room units, one clean site at
  W=20 gives area <= 36 and span <= 37 (the note's 72/73 is in doubled units). The bound applies only if a clean site
  exists; d11's first clean room is at W=24, and a W=20 clean-room census needs N <= 144, beyond d139's N=34-80
  gap, so it doesn't shrink that gap. The dumbbell defeats only preset direction menus. No completeness progress.
- **d156 (multitwist-first-shot, sound with gaps, all low).** Exact tracer on dumbbell a=10,20,60: at 2a=20,
  cylinders (40,2),(42,2),(86,1), c=18,060; (kc,1) misses, (a+1+kc,1) hits. The stabilizer proof is complete. Stronger:
  holonomy multiplicity (2 or 10 vertical vs 2*area in the witness direction) rules out any affine map from vertical to
  the witness family. Refutes only the vertical-seed method, not BBBB completeness.
- **d157 (doorway-word-bound + terminal-cap, sound with gaps).** Two-rectangle theorem holds for every pair
  of distinct interior lattice marks, any door width, no parity condition (D = span along the door, H = across);
  all 539 pairs on 4 explicit rooms lit within 16 reflections (bounds 185-365). Terminal-cap lemma correct as a
  conditional. DB55 slope -37/8 and the R22 top-cap exclusion reproduce exactly. HIGH: neither note constructs
  the slope interval clearing every earlier door, which both lemmas assume. MEDIUM: localization needs the whole
  slab between the marks to have the two-rectangle profile, so the theorem doesn't compose along chains alone.
- **d158 (simultaneous-door-fractions, sound with gaps).** Both counterexamples hold exactly: dumbbell
  L=12,22,32 (no monotone slope reaches T; the far-cap repair works), and R22 at D=8,16,32 (one word per D, dark
  for that word only). The real mechanism is denominator-free: aiming at T pairs the visits at times t and D-t by
  a fixed reflection or identity that sends one window off the other. Works for any D divisible by 4 with D>=8.
- **d159 (time-pairing, sound with gaps).** Exact: in R22, I_S=(7/4,2), I_T=(2,9/4), chord slope 2 returns to S
  and stops at reflex (1,2); the same chart fails in lit R22-L1-005 (lit via (-24,-16)). Overlap matched the tracer in
  1,787 cases. MEDIUM: overlap is equivalent to 'chord slope in I_S', i.e. ordinary unfolding legality, so the
  two-sided test adds nothing. MEDIUM: strict open gates omit legal reflections at smooth wall points ending a cut
  or door, so the charts don't cover all legal shots. Refutes the converse of window pairing only.
- **d160 (skeleton-decidability + chart cover, sound with gaps).** Chart cover correct: the R22 (2,3) launch
  reflects at cut endpoints (2,3), (4,0) and reaches (14/3,1). On the 6-wall L, lit with <=1 reflection iff zy<3x in
  all 448 grid rooms, so bounded-word lighting (length <=1) is non-Presburger (boundary y^2<3x). Kills the
  Presburger route only; doesn't contradict d132 (all-word darkness). Real closed fields don't rescue it,
  because integrality sits on the shared variables.
- **d161 (adjacent-arm illumination, sound with gaps).** Every pair of distinct real
  interior points is lit in a rectangular hall with full-side rectangular arms; all
  constructed shots replay exactly (80,459 lattice/half-lattice, 6,000 random, 1,500 seam
  pairs on an L, T, plus and uneven plus; 0 failures); arm reversal is necessary (479 pairs).
  The class is exactly rectangles, L, T and plus (4/6/8/12 walls), so it adds no W 14-20
  room and no new BBBB room. The one-interval-per-line condition is necessary, not
  sufficient (S-tetromino, staircase).
- **d162 (parallel-mouth combs, sound with gaps).** Half-turn dumbbells: every half-turn
  pair is lit through both mouths (223 pairs, 3 dumbbells; DB55 (4,1)-(9,4) replays
  exactly). Stacked halls (nested roof attachments, 8Ah <= cu): every pair of distinct real
  interior marks is lit with one floor bounce (203,790 pairs, 5 members, 0 failures). The
  class is BBBB at W <= 20 (two 14-wall members, one 20-wall), but only tall-hall members;
  the constant 8 isn't sharp. MEDIUM: DB55 is a two-sided stacked hall, so it lies in the
  note's second class and fails only its size and mouth conditions.
- **d163 (pattern ledger, computed, review d165).** 4,574 orthogonal turn words with
  W <= 20 up to rotation and reversal (1, 1, 4, 8, 29, 79, 280, 912, 3,260 for W = 4..20;
  Burnside cross-check), each realized and checked. COVERED for all lengths: 6 (W <= 8,
  d15). PARTIAL by a word-specific theorem: 4 (plus, DB55 word, U2 spiral, cov279 band).
  OPEN: 4,564. Largest OPEN groups: dents in one direction only (1,020 words, includes
  two-sided stacked halls and cov4181/cov4269/cov2929/cov446), one dent per direction
  (944, R22's profile), one-bank stacked halls (266, now PARTIAL by d162).
- **d164 (attacker on stacked halls, named rooms).** 10 edge rooms (bound violations 2x-80x,
  overhanging and flush children, two-sided, DB55, 8 levels at W=20): no dark pair. The
  one-floor-bounce family first fails at 8x the bound; all failures are lit by multi-bounce
  hall paths or, for overhanging children and DB55, bounces on attachment walls (bounded
  per-pair check, height <= 60, <= 40 reflections; a miss would not prove darkness).
- **d165 (ledger review, sound with gaps).** Independent enumeration, all 4,574 realizations
  and both family counts reproduce; reversal alone is the right mirror equivalence; d15
  covers exactly the W <= 8 words. HIGH: d162 moves all 266 one-bank histogram words to
  PARTIAL. Corrected split 6 COVERED / 270 PARTIAL / 4,298 OPEN (d163-pattern-ledger/STATUS.md).
  296 of the 935 dented target-1 words have no full-width hall.
- **d167 (overhang escape + nonspanning entry, both sound with gaps).** In d164's room B,
  every path from (4,67/2) into the hall first uses an attachment wall (exact; x > 3+2d sharp).
  L(B) > 2A lights every target row (8,985/8,985 half-lattice targets on 3 rooms). In the
  W=12 LLLRLLLRLLRR realization, every pair on resonance-free rows y=1-a, y=4+b of the two tips
  is lit without a spanning hall (exact replays, one 173,106-reflection trace). No ledger
  word moves; the other-realizations condition lacks a patch size (medium).
- **d166 (parallel-dent frontier, sound with gaps).** The exact one-joint criterion for
  height-monotone shots and its all-abscissa corollary are correct: 0/581 tracer disagreements on
  6 joints, corollary matched at 188 level pairs. Local tool only; no ledger word moves. Re-run
  matches except the --extra supplement, which the default run doesn't append.
- **d168 (Ferrers terminal strip, sound with gaps).** For LLLLLRLRLR, condition (1) is empty on
  lattice rooms (all ratios rational). The denominator test covers a lattice room iff
  W/gcd(W, P0 h) > floor(W/w)^2, e.g. widths (2,3,4,5) with 5 not dividing h; 66/66 replays
  exact. The reduction to opposite terminal cells rests on d15 Theorem 3's r=3 table, which
  the d15 review left out of scope (review d169). Ledger: PARTIAL, provisional on d169.
- **d169 (d15 Theorem 3, r=3 table, sound with gaps).** No certificate error; Lemma D proved
  and traced. "Certified" = every real interior pair of the two position types, all real lengths.
  No W=10 word is fully closed; 578 position-type pairs remain open (per word: Ferrers 1,
  pyramid 7, 3-4 corners 21, stacked hall 33, staircase band 52, stacked hall 67, spiral 99,
  two-bank 298). The d168 reduction holds exactly. Work list: d169-review-d15r3/checks.log.
- **d170 (Ferrers two windings, sound with gaps).** LLLLLRLRLR: every real pair is lit if
  w(e+h) <= ud and (u+w)h(e+h) <= ve(d+e+h), any resonance (22 exact replays, including the
  5,490-reflection pair on grid (0,2,10,23,230)). With d168 it covers the ledger realization and
  both d168-uncovered rooms. Outside all four tests: grids (0,10,11,13,100), (0,2,3,4,6) and
  widths (2,3,4,5) heights (1,1,1,5). The transpose is unproved (medium).
- **d172 (pyramid column, sound with gaps).** One-middle-winding lemma: if wb <= ud, every real
  placement at those levels is lit (29 PASS, 9 named rooms). All 7 open pyramid pair types fit it,
  covering rooms with wV <= u^2 or w h_T <= u d per type. 91/91 replays; the 49 marks outside the
  lemma in 3 failing rooms are lit by the same construction. Ledger: LLLLRLLRLR PARTIAL (d172);
  LLLRLLRLLR PARTIAL by d169's 3 fully certified order types.
- **d171 (Ferrers residual + d17 chord lemma, sound with gaps).** d17's chord lemma holds for the
  staircase's open pair when d(v-u) <= e(u-w) (592 exact paths on 4 rooms). The RES certificate is
  correct (78/78). HIGH: the union of d17, d168, d170 and transposes leaves an infinite lattice
  region, e.g. widths;heights (2,3,5,6; 7,1,1,3), (1,2,3,4; 13,2,1,4), (1,2,3,5; 1,2,1,4); without
  d170's unproved transpose also (3,4,12,13; 1,1,1,1). LLLLLRLRLR stays PARTIAL.
- **d174 (deep terminal band, sound with gaps).** Ferrers W=10 is lit when
  h >= max{d(W-u)/(u-w) - e, (d+e)(W-v)/(v-w)} (floor return, equality included), and under a
  prime-power terminal test that covers T1 directly. 48 PASS. HIGH: still not COVERED; V1 =
  (2,3,5,9; 3,1,1,3), V2 = (1,2,3,6; 3,2,1,4) and the family (2,3,5,90m; 40n-5,1,1,3) fail all
  nine tests.
- **d173 (band-chain characters, sound with gaps).** Word-independent two-phase winding test:
  construction, Fourier relation bound and exact rank-one test are correct (292/292 replays). It
  certifies U2b, T1 and 64/65 pyramid marks; R22's dark pair fails the rank-one test at exact
  equality. HIGH: no implication for all W <= 20 rooms; on lattice data alpha is rational and the
  relation box grows with the lengths; delta has no lower bound and no beam-existence proof.
  MEDIUM: one delta for all gates discards the wider deep windows that light U1 and U2.
- d175 (review of cap-character-lock, simultaneous-strip-misses, per-gate-rank-one; 86 PASS, 0 FAIL, 63 CPU-s, re-run SAME): arithmetic correct in all three.
  The uniform-delta common strip fails strictly on lit W=10 pairs (stair N=6, V1, V2, family). The same k=0 chart with full per-gate windows lights every one by a sloping line.
  HIGH: the per-gate-rank-one pair (eta=sqrt2/10, W=450) has no lighting proof; 'R22 equality is not diagnostic' does not follow yet.
- d176 (review of l1-primitive-subset-action; 4,332 cycle-type cases m<=14, re-run SAME): SOUND, no High gaps. L1 branch closed: a proper k-subset sheet action makes every reflex site corner-only, so no dark pair at W<=20.
  MEDIUM (inherited): real-point corner-only closure is confirmed only with gaps (d103, d107: 11 of 24 shear-box rooms re-derived).
  Remaining L1: natural action incl. A_n; primitive non-Burness-Guralnick with 21-48 squares; imprimitive; d81 d>=2n/3 to area bound.
- d177 (shear-box residual re-derivation, d107 procedure; spot re-run of 1-244 SAME): 6 more rooms PASS (1-244, 5-252, 6-213, 6-219, 7-234, 8-220); 17 of 24 now independently confirmed.
  2-300 RESOLVED (follow-up, spot re-run 7-15 SAME): cap artifact. With no piece cap, 0 skipped directions and all 1,550,080 products of the 16 boxed pairs lie in saved boxes (max displacement 2/17). 2-300's 273 unboxed pairs not re-run (~10 CPU-min).
  Not run: 4-244, 7-241, 8-239, 8-240, 9-240, 4-49. Bug: d107 compare.py line 88 uses undefined k (only after an unreached box).
- d178 (review of l1-natural-four-sites + l1-natural-marked-poles; 5 named rooms, 0.03 CPU-s): both SOUND, no High gaps.
  DB55 stretch gives A_p/S_p at every prime p>=53 with regular points at every site: cycle-type/block arguments cannot close the natural branch.
  Same-parity lattice pair lit iff a clean segment reaches a swap pole (with midpoint-necessity). MEDIUM: this restates the open reachability lemma; it is not progress on it.
- d179 (review of l1-swap-pole-averaging; DB55 p=53, 32 named site-direction cases): SOUND. Counting lemma (q_b=24 of 1378, a matching) and straightening lemma verified.
  MEDIUM: by Hurwitz the reciprocal-scale condition is free, so the proposed next statement equals the reachability lemma. No L1 movement.
- d180 (review of l1-swap-cylinders + l1-marked-cusp-frequency; DB55 p=53 and U2, 0.05 CPU-s): both SOUND, no High gaps, no L1 movement.
  DB55 pair annuli j=1..6 all 26x1; j<=5 pole-free, j=6 poles on both rims: cylinder size does not decide incidence. Cusp frequency positive iff lit (restatement); index unbounded, no N0.
  Equal/unequal-depth crossing congruence verified (already in adjacent-cylinders.md); self-glued edges need both side assignments.
- d181 (review of l1-open-collar-gluing + l1-remote-wall-return; named DBas/DB55/L(3,3,3), 0.1 CPU-s): both SOUND, no High gaps. L1 large=>lit tool moved.
  Long-corridor tail for two fixed chambers reduces to a per-chamber open-end condition (every pair with a point in the chamber lit when its mouth opens onto a half-infinite strip). New ends covered: L/T/plus with full-arm mouths.
  Remote-wall return: 18/18 traces past threshold reach target. MEDIUM: threshold not stated (DB55 example needs L>1087).
  Remaining for L1: open-end lemma for every chamber; W-dependent corridor threshold; no-corridor rooms (smallest named open case: DB55 top-line stretch at L=3, W=12).
- d182 (review of l1-growth-modes; DBas exact traces, 38 PASS, 0 FAIL, 0.74 CPU-s): SOUND, no High gaps. L1 moved (qualitative).
  Finite chart/scale classification at W<=20 (<=18 gaps; 4 exhaustive rows). Ray transfer: lit at one length => lit for all large t along a fixed integral gap ray (15/15 traces above threshold).
  Corollary: darkness at unboundedly many points of a ray => every member dark, down to the minimal one; row-1 unbounded dark sequences descend. Qualitative only: no N0, nothing uses W<=20 (R22 dilates are a fully dark ray at W=22).
  MEDIUM: corridor cut must meet only the corridor; no explicit threshold (gate-margin form gives t>84 for the control).
- d183 (review of l1-dbas55-top-phase; H=4,5,7,15,31,101 + adversarial marks, 106 PASS, 0 FAIL, 6.2 CPU-s): SOUND, Low gaps only.
  DB55 top-line stretch at corridor length 3 fully lit (every real pair) for every integer H>=4: closes d181's first named no-corridor case as a whole family (row 1, two-interval cross-section).
  Still open in row 1: other corridor lengths (modulus 26 depends on L=3, width 5).
- d184 (review of l1-gap-hyperplanes; DBas exact traces, 39 PASS, 0 FAIL, 0.43 CPU-s): SOUND, no High gaps. L1 moved.
  Explicit lattice threshold t > XPq - X/M (margin 1/(2q)). One seed fails only on finitely many affine slices (DBas: 95 lines in 9 directions). Disjoint perpendicular strips also covered.
  For a fixed chart, lattice marks, parallel or disjoint-perpendicular family: lit/dark sets semilinear, finitely many seeds, universal illumination decidable. Unbounded darkness forces a whole dark ray.
  CORRECTION to d182 review: its (n,n+c) offset rule is wrong (DBas seed lights (500,501); failing offsets c=-4,-5,-6).
  MEDIUM: fixed-sheet requirement adds avoidable exceptions (95 vs 24 lines); many families have no area<=20 member, so L2 cannot seed them.
  Open: meeting perpendicular strips (row 4), fixed gaps unbounded across sequences, real marks (L3), no N0.
- d185 (review of l1-db55-odd-lengths; 168 PASS, 0 FAIL, 14.7 CPU-s): SOUND, Low gaps only. DB55 two-box layout fully lit (all real pairs) at every odd L coprime to 5, all heights H1,H2>=4.
  With d112 (L>=21): DB55 open only at even L in {2..18} (dark pair confined to integer x, integer 5y, opposite-box banks) and L in {5,10,15,20}.
- d186 (review of l1-crossing-gap-transfer + l1-cross-cap-budget; 53 PASS, 0 FAIL, 0.04 CPU-s): both SOUND, no High gaps. Row 4 moved.
  Nonsemilinear failure confirmed for the direct-ascent route class only. Qualitative row-4 descent (conditional on d132/d134): one lit point => dark part of a 2-parameter slice is finitely many points plus finitely many lines with one gap frozen; K not computable.
  DBas t1=10 lit for every real corridor length. Single-mouth crossing: effective residual; st279 lit for a>93 or D>376.
  Assembly: 'unbounded dark area in a chart => dark room with all gaps <= G' holds assuming finite-flat, but G is not computable. Explicit G needs a height bound on dark flats (d133) or an all-ratio multi-mouth crossing theorem, plus seeds above area 20.
- d187 (review of l1-chart-descent + l1-seed-normal-bound; 45 PASS, 0 FAIL, 0.08 CPU-s): both SOUND, no High gaps. L1 assembly done modulo finite-flat.
  Bounded-witness theorem: any dark lattice room has a dark witness in the same chart with area <= 81 G(C)^2 (W<=20, <=9 wall gaps/axis). No isolated dark rooms: flats are linear, dimension >= 2.
  One lit seed bounds a dark factor's normal (K ~ 7.5e10 on DBas two-gap). Doubly-proper products can miss both seed slices.
  L1 now reduces to ONE estimate: factor-height bound H(C) (d133's H), e.g. via seed bound qMP <= Q(C) giving H <= 1+ceil(88(32Q)^12/pi^2).
  MEDIUM (inherited): finite-flat (d132/d134) and the classifying-map completion (d186: sketch).
- d188 (review of l1-mixed-seed-normals; 42 PASS, 0 FAIL, 0.73 CPU-s): SOUND, no High gaps. L1 H(C) moved.
  Fixed-period mixed seed bounds at least one axis equation of any dark product (van der Corput on u, 1/u); needs no slice through the product, removing d187's probe obstruction. Model span(1,m)^2 excluded for m>K.
  st279: seed route fails to transfer on a=7+2n, D=3a, but the floor gate (spacing 6) lights every n>=0; the ray is lit.
  MEDIUM: transfer hypothesis proved only for disjoint insertions (d184). Missing: fixed-period mixed transfer at occupied crossings with explicit seed constants, or a version accepting bounded-modulus gate congruences.
- **d189** (2026-11-22, bbbb/l1-crossing-gate-resultants.md, snapshot sha256 5a2e76a1) PASS WITH CORRECTIONS (~85%). Route switching through a fixed upper chamber at an occupied crossing: periodic first-hit approach, explicit finite box for dark gap pairs given one upper first-hit interval; extends d186 cap budget to several mouths in [0,R]. checks.py 134 PASS, re-run by coordinator.
  MEDIUM: open-case list must add growing source depth d and d188's two-gaps-per-axis product. LOW: P over all upper runs (30 at st279, example uses 6); far-wall bound loses factor 2; state R≤D, positive-sheet routes, one gap per axis. No FPT, no K(C)/G(C); estimate unchanged.
- **d190** (2026-11-22, bbbb/l1-crossing-scale-step.md, sha256 835be639) PASS WITH CORRECTIONS (~85%). With a stretched upper template (ux,ty), a dark placement forces a/gcd(a,2d) ≤ 16PC²/η³, uniform in u,t and growing floor depth d. So any dark linear family fixes the ratio a:2d. checks.py 48 PASS, re-run by coordinator.
  MEDIUM: 'uniform first-hit interval impossible at separated scales' needs w/b→0 (with u=t the theorem gives width η). LOW: template has no openings beyond labelled mouths; open list should add far roof opening outside D=O(a), t=o(a), fixed d. First open: fixed-ratio growth (e.g. a=2d), d188 two-gap product, two growing upper depths. Estimate unchanged.
- **d191** (2026-11-22, bbbb/l1-fixed-ratio-corner.md sha 36ba40d2 + l1-lower-period-coupling.md sha 7346a98d) both PASS WITH CORRECTIONS (~85%). Fixed-ratio corner: at a fixed depth ratio with fixed upper template, only finitely many dark placements (explicit bound, uniform in c, D, u; ~1e95 at st279). Coupling: a dark rational product forces a width proportionality or two depth proportionalities. checks.py 38 PASS, re-run by coordinator.
  MEDIUM: corner threshold not uniform in ratio, blows up as ratio→1; a=1, d→∞ escapes d190 and d191. When t grows with h only finitely many κ values. LOW: use (m+1,m) not (m,m+1) (clips mouth). Scale-step v2 applied d190 Medium only partly. First open: fixed template, ratio drifting to 1 (a=1, d→∞); then fixed ratio with h/t bounded. Estimate unchanged.
- **d192** (2026-11-22, bbbb/l1-shallow-roof-return.md sha ac833ca2) PASS WITH CORRECTIONS (~85%). Roof-floor-roof route: explicit H* (template constants only) with h/t>H* lighting every source depth, uniform in D,c,u,t; closes d191's a=1, d→∞ case. With d190/d191: a fixed upper template at an occupied crossing has only finitely many dark placements. H* is astronomically large (ratio denominators ~1e37). checks.py 23 PASS, re-run by coordinator.
  MEDIUM: scale-step note's open-case list still says growing d survives with bounded a/gcd(a,2d) (stale). LOW x5 incl. state the fixed-template finiteness corollary; identity (1) holds at every placement; d191 Lows 2-4 unapplied in fixed-ratio v2. First open: comparable-scale product with u or t growing with the lower box (D/u, h/t bounded, high-denominator axis ratios). Estimate unchanged.
- **d193** (2026-11-22, bbbb/l1-overlap-phase.md 0ff49116, l1-projective-crossing.md 19909ad5, l1-comparable-width-bound.md 92402b95) all PASS WITH CORRECTIONS (~80-90%). Overlap-column crossing forces q≠0 with K=1+⌈16/(π²ρ³)⌉; integrality eliminates the source (L | Pqw); with wall-gcd normalization Dh+Vut ≤ (Aβ²+VB)S², S=KP|Δ|: first bound on both stretch factors u,t in the occupied-crossing chain, anchored overlap class, non-rectangular templates. checks.py 34 PASS, re-run by coordinator.
  MEDIUM (note 3): bound is per pair type (lower-wing source, target with transverse approach); sources inside a template-width column uncovered (ε=j≥1 ≫ Bη/P). Add hypothesis: lower roof solid between source and column. LOW: Δ≠0 automatic for 0<w<D; 'odd m≥5' unnecessary; bound ≥ power of H*; u-absorbs-L family miscited (correct: w=u, c=m, (p,q)=(1,2)); symbol reuse. First open: source inside the template-width column; then target in column cap, independent horizontal offset, changing upper shape. Estimate unchanged.
- **d194** (2026-11-23, bbbb/l1-grounded-component-transfer.md sha 220ff73a) PASS WITH CORRECTIONS (~80%). First entry: target outside the grounded union has a transverse first entry into an attached column (irrational slope, minimal flow). Column heights eliminated: T | P C_b p_last (jB₀−iAb). Two-return area bound AT²+VB₀(T/b)² for an inside-column source when (i) opposite side solid above roof or (ii) H≥b; closes d193's inside-column gap under (i)/(ii). checks.py 12 PASS, re-run by coordinator.
  MEDIUM: write q₀ ≤ 2(H*+b_max)/(B_min η) to show independence from the lower box. LOW: state K tail target, b≥1, connectedness step in first entry, rank open case. First open: H<b with non-target side opening into another upper component (both virtual contacts in open gates). Estimate unchanged.
- **d195** (2026-11-23, bbbb/l1-two-component-return.md sha 800033b9, partial) PASS WITH CORRECTIONS (~85%). Conditional return: an excursion into a neighbouring component replaces the virtual reflection iff l+|Av|<y<r−|Av| (exact); period-shift version needs solid strip walls and kPA≡0 mod 2(r−l). Limit of method correctly stated: no decreasing parameter from the finite component count. checks.py 8 PASS, re-run by coordinator.
  MEDIUM: Advances line must state period-shift hypotheses. LOW x5 (speed radius includes A; residual wording 'S_b=0'; H* constant; modulus; notation); d194 partial-terminal-width residual missing. Reviewer: the crossing line (d194–d195) is fragmenting, not converging to K(C). First open: contacts within |Av| of a strip end. Estimate unchanged.
- **d196** (2026-11-23, bbbb/l1-crossing-reduction.md sha 3eeee9e8) PASS WITH CORRECTIONS. Stopping-rule test (PROGRAM.md): LLLRLLLRLR has ≤4 wall gaps per axis, so d187 sharpens to ≤15·G(C)² (G=2 would give ≤32). But no reviewed result bounds G(C) or H(C): NO numerical N0. Rank-one example: normals of height ≥((n+3)/6)^(1/3) needed. checks.py 27 PASS, re-run by coordinator.
- **d197** (2026-11-23, bbbb/l1-shrink-primitive-test.md + l1-shrink-dark-transfer.md) CORRECT WITH MINOR GAPS. Shrink-descent first test, L1 method limit only. Admissible 1–2 unit shrinks exist for (n,n+1,n+2,n+3), n ≥ 3; they leave the rank-one product on either axis. Terminal-cap path transfer works iff s·r ∈ hZ; it fails whenever v2(h) > v2(s) + v2(Δy) (e.g. 4 | h, odd Δy). Forward darkness transfer also fails locally; exact one-visit gluing criterion (A_d + 2dr) ∩ B_T ≠ ∅ holds. No illumination failure is claimed. Open: changed-exit compensation, vertical shrinks, cap avoidance. checks.py 28 PASS, re-run by coordinator.
- **d198** (2026-11-23, bbbb/l1-shrink-exterior-induction.md) CORRECT WITH MINOR GAPS. The 8-wall closed exterior matches first mouth arrivals. A lit symbolic family breaks the fixed-slope one-visit implication: empty at d=w, nonempty at d=w−1, w−2. The k-visit recurrence is exact, but C_d must also exclude return corners. The visits needed at fixed slope are unbounded (q=2mL), so finite-return induction needs a slope-denominator bound, which the stopping rule excludes. Shrink-descent route STOPPED under its early-stop clause. Follow-on bbbb/l1-shrink-cap-avoidance.md (unreviewed): avoidance holds for one or two adjacent exterior columns. Separated columns need unboundedly many vertical legs; open. Summary: bbbb/l1-shrink-route-limits.md. checks.py 25 PASS, re-run by coordinator.
- **d199** (2026-11-23, bbbb/l1-route-dark-structure.md + l1-dark-structure-test.md) CORRECT WITH GAPS. The dark-structure lemma's conclusion (r ≥ 3d ≥ 9) can't hold at W ≤ 20, so in scope it restates the goal. Its first step, darkness ⇒ proper factor, is certificate completeness. Facts kept: (a) d152 three-chamber family X=Y=3k+1 has sheet count N=29+6k; (b) d154 §2 corollary: a proper factor's block size divides N and is ≤ r. So the family's monodromy is primitive unless k ≡ 1 mod 5 or 7 (202 of k=6..300), and no factor-type certificate exists there. First open case k=6 (area 65). Route STOPPED early on the reviewer's recommendation. Follow-on bbbb/l1-primitive-family-lit.md (unreviewed): horizontally monotone shots are excluded for one explicit pair. A connection needs a horizontal reversal; primitivity doesn't supply one. checks.py all pass, re-run by coordinator.
- **d200** (2026-11-23, bbbb/l1-three-chamber-lit.md) CORRECT. THEOREM (lighting tail, L1): in d152's three-chamber family X=Y=3k+1 (three 3×3 chambers, unit corridors, D=3k+4, W=20, area 29+6k), every pair of distinct interior lattice points is lit for all k ≥ 1. Equal-offset outer pairs need ≥ 2 horizontal reversals and are joined by an upper-pocket path of slope 1/(D−1/2). Other pairs need ≤ 1 bounce or a seam-matched fold. It uses no W ≤ 20 inequality. Minor gaps: two one-line justifications in the reversal-impossibility part. checks.py traces 2,310 prescribed rays for k=6..40 with 0 failures, re-run by coordinator. Open: X=Y=1, X=Y ≢ 1 mod 3, unequal corridors. Ledger: word LLLLRRLLRRLLLLRRLLRR OPEN → PARTIAL (recorded with d201).
- **d201** (2026-11-23, bbbb/l1-pocket-lemma.md + l1-pocket-general.md) CORRECT. Pocket lemma: the roof-excursion return map is a phase shift of 2hc mod 2w. Exact matching criterion: max(0,M−w,U) < a < min(w,M) and (2+2h/g)a ≡ M+(2h/g)U (mod 2w); solutions are spaced wg/(g+h). THEOREM: every aligned three-chamber room (3×3 chambers, unit corridors at 1<y<2, independent D₁, D₂ ≥ 4) is fully lit for lattice marks. R22 control: the dark base room has 9 odd–odd corners and no qualifying pocket. Follow-up: word dictionary F L^j F L^(4−j) is correct, and the displaced-aperture obstruction is limited to straight legs (sharp form (δ+1)L ≥ w). checks: 48,114 prescribed rays over 729 rooms, 0 failures, re-run by coordinator. Ledger 6/273/4,295 → 6/274/4,294. First open area corrected by d202: 21 (e.g. chambers 2×3, 2×3, 2×3 with necks 1, 2), not 32.
- **d202** (2026-11-23, bbbb/l1-neck-phase.md) CORRECT WITH GAPS. Neck phase map for legs reflecting inside unit necks, with coupled tests for displaced mouths. THEOREM: two 3×3 end chambers with a 3-wide, 4-tall middle chamber and unit necks at 1<y<2, any lengths X, Y ≥ 1, are fully lit (91 pairs per room; 56,875 pairs for X, Y ≤ 25). The height condition (2H₀vm ≡ ±y−1 mod 2H, m a positive integer) is sufficient only; 3×5 middle with a row-4 target fails it. Status error: the first open area in the word is 21, not 32 (also wrong in d201). Next: 2×3 triples (area 21), a 1-wide middle (area 23), the 4×3 middle. checks: 57,657 prescribed rays, 0 failures, re-run by coordinator. Ledger unchanged.
- **d203** (2026-11-23, bbbb/l1-chamber-general.md) CORRECT WITH GAPS. Group-ring arithmetic test J > 0 is exact for prescribed strip transits in aligned rectangular chambers with unit necks. Dimension-only lighting holds under gcd(P, lcm(w)) = 1 (opposite-side pairs, and opposite-parity same-side pairs). Width-2 and width-1 results hold. The ledger follow-on lists two OPEN two-neck words. 55,000+ prescribed rays; checks.py passed in full, 269 CPU-s, in the reviewer's final run. Area-21 and area-23 example rooms are fully lit; area 21 remains the first open area. The aligned layout isn't closed. Last review on this word: the per-word work was stopped as busy work.
- **d204** (2026-11-23, bbbb/decide-path-bound.md) CORRECT WITH GAPS. WRONG PREMISE RETIRED: "linear reflection bound ⇒ per-word Presburger sentence" (d159, STATE 'Per-itinerary test') is false. On the one-neck word with affine family (m,u), zero-reflection legality is u > m(m+1), so even one fixed itinerary isn't Presburger-definable. All 29,000 pairs were checked; at u = m(m+1) the segment hits corner (0,0). There's a finite witness bound 2N·2^F+2 for every room via the finite SL(2,ℤ) orbit (method of Hubert–Schmoll–Troubetzkoy, arXiv:math/0602394), but it depends on area. A 2m+4 linear witness lights the family (31,276 rays checked). Surviving forms: per-word parametric certificates (proofs, not a decision procedure), or a new eventual-periodicity theorem for the lit set per word. checks.py re-run by coordinator.
  MEDIUM: invariant is dim E + dim F (one axis per seed); subsequence step non-effective; proposed 'actual-area witness' route not distinct (area between max(m(U),m(V)) and 15·m(U)m(V)); a new route needs a geometric darkness-preserving shrink that bypasses heights. Crossing chain STOPPED per stopping rule. Estimate 9-11% → 8-10%.

- **d206** (2026-11-23, d205-census-a21 + parity-gap, review of Astra's run) CORRECT WITH GAPS. L2 census, W ≤ 20, interior lattice pairs: all 1,604,242,406 pairs at exact area 21 (538,025,823 rooms) and all 726,251,893 different-parity pairs at areas 17–20 are lit; 0 survivors. Independent exact tracer replayed 3,985 sampled witnesses from shards 17/83/42 (0 failures; coordinator re-ran); 3 area-21 and 8 backfill shards rerun byte-identical; fuzz of verify_plane vs independent tracer 0/30,867 disagreements; R22 control rejected; own enumerator matches all 57 buckets through area 11; fixed-polyomino node counts match OEIS A001168 through area 21. Gaps: pair reconciliation counts shot pairs, not lit pairs (lit follows from code structure + 0 survivors); the 2,471,412,511 through-21 total reuses unaudited d9 same-parity data. L2 is now complete through exact area 21. Where: `d206-review-census-a21/review.md`.

- **d207** (2026-11-23, bbbb/l1-bbbb-area-bound.md sha 0fdeb3c8) CORRECT WITH GAPS. Per-class identities n = c_y + 2m_y, Σc_y = 4r+4, Σm_y = 2(n−r−1) hold. Dark same-class pair at n ≥ 49 has hidden branches H ≥ 2⌈2n/3⌉−16−⌊n/2⌋ ≥ 26, so "H ≤ 25" is equivalent to no dark pair at n ≥ 49: a necessary condition, not a reduction (as d86). Two-class estimate n = U(I) − ⌊v_out/2⌋ exactly; its "area-25 condition" is a room-only property, unrelated to darkness. New: for different-parity marks the twisted curve f(x)=τ(f(y)) gives exactly 2d_e distinct regular midpoint candidates, none at a corner; every legal path's midpoint is one; only d_e ≥ 1 is known. No unconditional BBBB area bound. Where: `d207-review-bbbb-area-bound/review.md`.

### Proved, not yet reviewed

- **Doorway lemma** (`offgrid/doorway.md`). Dead-end door pairs are lit at
  door width ≥ 1/2 the channel width (one cap) or ≥ 1/4 (both back walls).
- **Shrinking doors** (`shrinking-door.md`). Slope width on one itinerary ≤ w/D.
- **Perpendicular bridges** (`perpendicular-bridges.md`). Two long
  perpendicular corridors force every pair lit; a 2-parameter family of
  20-wall rooms.
- **20-wall Q-class run.** All 913,622 rooms cleared for real marks (912,728
  whole-room, 894 tile-level; 620 shear boxes). d103 (confirmed with gaps):
  independent code passes all 3,652 shear trees (246,639 leaves) at W = 20
  and 122,865 leaves below 18 walls, 0 failures; a mutation control fails
  232,884 leaves. Samples clear: 300/300 whole-room, 200/200 below 18,
  tile-level 74/100 (21 timeouts, 5 with boxes skipped; coordinator re-run).
  d107: all 3 bin-pair rooms (5-0, 2-266, 7-230) pass, 295,323 receipts,
  0 failures; independent residual re-derivation matches in 11 of 24 box
  rooms (64 of 458 boxes); three mutation controls fail as intended.
  Open: residual for 13 rooms (394 boxes) not re-derived; bin-pair lists
  for 5-0 and 2-266 come from the census; no end-to-end trace of the
  fixed-phase mode.
- **Rim refinements** (`persistent-gaps.md`, `rim-quotient.md`). Sharper rim
  condition; R22's period-10 mechanism can't recur at large area.
- **Supporting notes** in `qclass-closure/bbbb/` (home of the notes above): `two-class.md` (cylinder
  winding changes midpoint parity iff one of u, h, C ≢ 0 mod 4);
  `shortest.md` (one corner can block shortest routes in two classes);
  `fixed-wall.md`; `bottom-step.md`; `short-escape.md`; `denominator.md`.
- **Pair-specific notes** (Astra, 2026-11-18).
  `illumination-ninth-corner.md`: replacing one R22 cell with a strip of width
  `w` gives lit widths `w = 4k/7` on both sides of the dark width 1.
  `staircase4991-*.md`: in a 12 by 12 staircase, the pair (1,10) and (10,1) is
  lit for every real middle corner, by explicit routes of at most 8 bounces.
  This survives moving each mark up to 1/40.

### Computed evidence

- **Common-cylinder test** (d72; method PROVED exact). It covers the full
  SL2(Z) orbit of the marked origami and matches direct tracing on 18,446
  lifts. In the 9 true BBBB rooms (every `N_x = B`), 747 of 747 pairs satisfy
  CC. Its only failures are 11 visible axis-parallel pairs in d64 rooms with a
  proper factor, smallest `cov446` (`W = 18`). The marks lie on a cylinder
  boundary; a closed-cylinder variant covers them, and d64 closes these rooms. R22's dark pair fails CC in every direction, as it must.
  Where: `d72-cylinder-test/README.md`.
- **BBBB range, area 21 to 36** (d73; `d73-bbbb-21-36/README.md`, `enum.c`).
  It holds about `1e11` to `1e12` rooms with `r <= 8` (GUESSED from d9 growth
  ratios); exactly 92,657,242 at `W <= 12`. Corner-only-class rooms (780,565)
  and proper-factor rooms (2,800) are a small fraction. So the open case is
  the generic case. Pipeline slice (COMPUTED, not a sample): 31,612 rooms and
  1,001,339 pairs, all lit, every witness replayed by a second tracer.
- **Lemma stress** (d83; coordinator re-ran). The open lemma held in all 11
  saved single R22 edits with r ≤ 8. Weak: every room is lit and d = n − 1.
- **Shadow kill test** (d85; coordinator re-ran). From 2 sources each, every
  point is lit in the crosses b = 7..17 (areas 96–256) and U2 k = 0..6. R22
  control: H(0,0) = {(2,2), (2,−2)}.

### Open core

- **Open lemma.** In a room with r ≤ 8 and d ≥ 2n/3, one of the
  2⌈2n/3⌉ − 16 − ⌊n/2⌋ off-class candidates is reached by a real path.
  Unreached candidates exist (R22's source class; cov4181's class d). This is
  the current form of condition (ii) for rational pairs.
- **Numeric form.** On U, show the hidden coincidence count is at most
  αn + K, with known constants. It needs α < 5/6, or any α < 3/2 for n ≥ 120.
  Reaching one off-class coincidence also suffices for the large same-parity
  cases. d86: for a dark pair this budget restates the open lemma
  numerically; it doesn't reduce it.
- **Condition (i) for 21 ≤ n ≤ 48.**
- **Candidate CC** (d72). In a BBBB room, some lifts of two distinct
  same-class interior marks lie in one open flat cylinder of the doubled
  surface. The cylinder has a rational direction and no vertex lift inside. No argument
  links `r <= 8` to cylinder incidence. Agent estimate (GUESSED): CC true
  about 25%, provable about 3%.
- **Other gaps.** General BBBB rooms; shrinking doors (d58); turning pairs
  with no straight corridor (cov2929 type); different-parity pairs;
  non-lattice rational marks (G2); 45-degree rooms.

- **Bridge to d64** (d93, corrected by d94). The proposed bridge lemma BL
  is not a reduction. At r ≤ 8 every class is discrete (Q-class closure),
  universal, or proper (d64), so BL says exactly that no BBBB room with
  r ≤ 8 has a dark same-class interior pair: the open core itself. Open
  parts: BBBB area 21–36 (finite, never enumerated); primitive BBBB area
  > 36; imprimitive BBBB area > 36. Fold transport (`fiber-transport.md`)
  gives only necessary conditions.

### Dead ends

- **Bounded search** (`search-plan.md`): no finite reduction exists, so none
  can prove the W ≤ 20 goal. Census paused.
- **Exhaustive area 21–36 run** (d73): 1,000 CPU-hours or more; not run.
  A single slice is proposed in `search-plan.md`: area 21, W = 10, 34,501
  rooms, cap 2 CPU-hours. It awaits Daniel's decision.
- **Span alone for D58's double resonance** (`shrinking-door.md`): the w/D
  bound on slope width rules it out.
- **Named-route tests** (d76, d77): they don't show some route works in every room.
- **Whole-room cylinder certificates** (`every-direction.md`; d87: sound): the
  12-wall crosses defeat them in every direction.
- **Per-corner route charging** (`shared-reflex.md`, unreviewed): one reflex
  corner can block routes with midpoints in all 3 off-classes.
- **Bounded-length shadows** (d85): at L = 0.5·diam the unreached count grows
  from 20 to 60, so short paths aren't enough.
- **Fixed-stratum finiteness on U** (d86): the genus of U is unbounded.
- **Shortest-path clearance** (`midpoint-clearance.md`, unreviewed): it can
  succeed only for directly visible pairs. A lit area-501 room has ≥ 228
  candidates per class, and every one fails the test.
- **Area bound from corner alignments** (`arithmetic-rigidity.md`): none exists.

### Corrections log

- **Darkness and (ii-alg)** (d82). Earlier text implied darkness gives
  (ii-alg). It only gives that no candidate is the midpoint of a real path.
- **d81 status** (d82). Earlier text listed areas 21–119 open with d81
  unreviewed. The open range for condition (i) is now 21 ≤ n ≤ 48.
- **Area-15 independence** (d74). Earlier text said the continuum step had no
  independent implementation. d74 now confirms it; d96 reviewed d13's lemmas (sound).
- **Two 18-cell rooms** (Astra `two18/`). Earlier text called them
  unresolved. The shear closes them; d90 checked it independently (confirmed with gaps).
- **Shadow-budget claims** (d86). Earlier text marked B(r) and the genus
  bound "Claimed". d86 found them sound, with one citation fix.
- **"No proof idea has survived"** (2026-11-18). d75–d84 now cover named
  families, but no proof covers all BBBB rooms.
