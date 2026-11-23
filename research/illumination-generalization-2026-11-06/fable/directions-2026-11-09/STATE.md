# State of the problem: 22-wall minimality

Last updated: 2026-11-23
`coordinator-log.md` in this directory. Research led by Peyton; this
directory holds the coordinator's 2026-11-09 to 2026-11-11 programme.

## Target

The minimum wall count of a strictly simple room on the square lattice
(axis-parallel and 45-degree walls) with a dark pair of interior points is
22. A 22-wall orthogonal room with exactly one dark pair is known. Daniel
set this scope on 2026-11-09; general polygons are out of scope.

Status: **conjecture**. The orthogonal case (W <= 20, so r <= 8 reflex
corners) is the core.

## Proved (AI-reviewed, not refereed)

| Result | Where |
| --- | --- |
| Every pair is lit in rooms with at most 8 walls, any real side lengths. | `d15-small-r/`, `d15-review/` |
| In a lattice room, all rational pairs lit implies all real pairs lit. | `d16-real-to-rational/`, `d16-review/` |
| Rooms with k <= 6 transparent points and W <= 21 are lit (computer-assisted). | `preprints/restricted-minimum-k6/` |
| No common parity factor separates interior pairs at r <= 8. Per-class and rigid factors stay open. | `d2-review/` |
| Triangle bounds: (1,2,5) exact 32; 30-60-90 exact 27; 45-45-90 at least 22. | `d7-review/` |
| Full families over a whole base stratum contain no dark room pair. | `d19-23-review/` |

## Proved, not yet reviewed

- Band lemma: inserting a row of height a multiple of 2 L p / gcd(q, 2L)
  preserves a lighting path (`d28-band-stabilization/`; Astra confirmed).
- Covering certificates prove whole one-row families lit (`d28`).
- Theorem R: a run 3 or more rows tall admits no parity factor (`d30`).
- One-parameter families satisfy the integrality constraints of Theorem X
  (`d24-one-parameter/`).
- Wall formula for glued rooms: W(P) = d (W(R) - 4) + 4 + 2 n3 (`d31`).

## Computed

- Census: no dark pair at W <= 21 among all rooms of area <= 20
  (945 million rooms); W <= 24 at area <= 19 has only the known room (`d9`,
  `d29`). Diagonal census to 32 half-tiles (`d11`).
- Adversarial search: about 892,000 rooms to area 900, no dark room at
  W <= 20 (`d26`).
- Smallest dark room with a run, glued-copy class: W = 28, unique (`d30`,
  `d31`).

- Thickenings of Monteil's dark slit room (19/20 sides, 45-degree walls):
  2,245 strictly simple variants, 2,076 with W <= 21, 468 million lattice
  pairs, none dark (`d42-slit-thickening/`). Lighting paths reflect off
  the thickened wall.

- Resolutions of Monteil's pinched dark 22-gon (slide 4, 45-degree
  walls): 5,867 strictly simple variants at scales 1 to 12, 500 with
  W <= 21 and 666 with W = 22, 1.54 billion lattice pairs, none dark
  (`d53-unpinch/`). Lighting paths reflect off the new wall.

- Relaxed-room laboratory (`d55-relaxed-lab/`): 8.3 million orthogonal
  rooms with slits and pinches, area <= 15; 5 dark pairs (the 22-wall
  room's and 4 in slit rooms, 3 of those by hand proof), all certified
  by Par. No uncertified dark pair. Corpus too small to count as strong
  evidence for "dark implies fold".

- Certificate check (`d46-cert-check/`): no room with W <= 20 and corners
  in >= 3 parity classes has same-class interior lattice marks certified
  dark by Par, Cut or Rig over the unit pillowcase. 13.3 billion rooms and
  52.7 billion pairs at W = 20 (areas 21 to 40, after the refereed filter
  F*), plus 471 million rooms at W <= 18; 0 positives. Scope after d47 and
  its d48 referee: holds for rational marks over every odd-index
  pillowcase P_Lambda (Lambda >= Z^2 + ZS + ZT, normalized room), except
  possibly different-class marks at W = 20 with coarse area 20 (residue
  D20, a finite check, not run). The (2,4,4) triangle base adds nothing.
  Open: even-index pillowcases (rooms with an even axis gcd, half-integer
  marks, the 45-degree base); d49 with its d50 referee closes lattice
  marks there (n_R <= 16, then the censuses) and odd sheared bases. The two
  remaining finite checks ran on 2026-11-17 (`d56-final-check/`): D20
  (169.7 million rooms, 285 million pairs) and non-lattice marks over
  index-2 and index-4 bases (945,884 rooms, 5.24 billion pairs). Every
  pair is lit by a verified path; 0 certified. So no strictly simple
  orthogonal lattice room with W <= 20 has a rational pair certified
  dark over any pillowcase base (computer-assisted; d47-d50 lemmas have
  one referee each).

## General polygons (2026-11-12)

- Wall formula for any rational fold base: n = 2 + d (k - 2) minus the
  regular points over vertices with p_i = 1 (Astra, `d32-fold-minimum/`).
- Apisa-Wright Thm 3.6 (read at source): off torus covers, dark pairs fold
  to one point of Q_min or are periodic points. Lattice rooms are torus
  covers, so the square-lattice core is untouched.
- Weak spots below 22: (1,3,4) pi/8 triangle, proved W >= 17; finite (F <= 50); no dark room at W <= 19 (`d34`), W = 20, 21 open; earlier: no dark room
  to k = 8 extra tiles; (1,4,5) pi/10, proved W >= 21, no dark room to
  k = 10 (`d33-134-rooms/`).

## Second proof of the certificate theorem (2026-11-15)

Fold enumeration (`d52-fold-enumeration/`, refereed in
`d54-review-d52/`): 106 quotient shapes and 4,710 disc covers at r <= 8,
0 positives, at every area, about 30 CPU-minutes, no room enumeration.
Independent of d46's code, of F*, and of the k <= 6 theorem; shares
Theorem U, R3, Fact L and the d39/d43 reduction (with the d9 census for
essential Rig). At r = 9 the only room certified by three Par
certificates is the 22-wall room with its one pair; Rig-certified rooms
at r = 9 are not covered.

## 45-degree rooms (2026-11-15)

Certificates over the (2,4,4) triangle base exist (Par, Rig; no Cut), but
the area bound is 8W - 8 tiles (160 at W <= 21) against a census bound of
32, so no certificate-side theorem follows (`d51-triangle-base/`,
unreviewed). Cause: cone points of angle 3 pi/2. The 45-degree half of
the target is compute-only (`d11`).

## The open core

Plain statement: on the square grid, the d2 audit excludes one fold type at
W <= 20: a common parity factor that separates the pair. It doesn't exclude
per-class factors (a different factor in each direction class) or general
rigid factors (`d2-review/review.md`, lines 57-84; corrected 2026-11-12).
Every dark room ever found comes from a fold. Off the lattices,
Apisa-Wright Thm 3.6 proves "dark implies fold"; it excludes torus covers,
which is exactly our case.

Why AW fails here (Astra, `d35-aw-torus/`): its proof needs a finite set
of periodic points and shortest saddle connections. On a torus cover,
rational points are dense, so that input is empty. The finite replacement
is the SL(2,Z) orbit of the marked square-tiled surface, which turns
illumination into finitely many horizontal visibility tests. The missing
step is compatibility across directions. First lemma to try,
**per-class amalgamation**: if each class partition B_b, B_c, B_d
separates the pair, so does B_* = B_b v B_c v B_d. Pure combinatorics
can't prove it (12|34 against 13|24 is a counterexample), so it needs the
geometry. Astra's estimate: 35% that this programme yields "dark implies
a separating parity factor" at r <= 8.

d36 (`d36-amalgamation/`, unreviewed): amalgamation is proved when the
class quotients are Galois (not the case for the known dark rooms). A
one-class separating quotient forces area <= 5r, so any amalgamation
counterexample at r <= 8 has area 21 to 40: a finite check, not yet run.
The hard step is still open: turning "B_x identifies a lift pair" into an
actual ray in class x.

d37 (`d37-visibility/`, unreviewed): conditional theorem. If, in every
fibre of every class quotient, one visibility component holds a strict
majority of the affine-return orbits ("joint majority"), a dark pair
yields per-class certificates. The hypothesis is not derived from r <= 8.
Structural fact: normalized rooms with area > 5r have no canonical
certificate at all, so they must be proved lit directly. Astra's next
step: the degree-three one-class fibre lemma. Estimate 30%.

d38 review (`d38-review/review.md`): d35 and d36 hold, with a scope gap
(the 5r bound needs corners in at least 3 parity classes). d37's
joint-majority hypothesis is FALSE at r = 4: in the 12-wall cross, one
class fibre holds a pair that is dark in that class (Cut certificate)
while the room is lit through another class. So the d37 theorem is not
progress, and a class-by-class visibility route can't work alone.

d39 (`d39-mixed-class/`, unreviewed): Cut never appears in a fully
certified dark triple, and essential Rig at r <= 8 forces area <= 20
(already censused). So, within scope, certified dark pairs reduce to
three per-class Par certificates over the unit pillowcase B: the d36 amalgamation problem (d43 review: correct, but only for certificates over B; coarser-pillowcase certificates and rooms with <= 2 corner classes are not covered). Per-class
completeness ("x-dark implies a certificate") stays open; it fails for
non-normalized presentations (cross scaled by 3). Estimate 25%.

d40 (`d40-thick-thin/`): a size reduction must map integer-marked dark
rooms to integer-marked dark rooms inside a fixed box, and must work
after gcd normalization. The obstruction is slope conservation: one slope
must fit every doorway's phase. Next lemma if resumed: two-door shadow.

Every route reduces to the **lit side of the same-fibre conjecture**: a
pair with no separating factor cover is lit. Equivalently, an
SL(2,Z)-orbit classification of square-tiled surfaces with two marked
points. No published theorem covers it (`d27-free-group-lit/`).

The most concrete reduction: **rigidity** (a pair is lit whenever two
identical adjacent rows or columns avoid it) at W <= 20 would confine
counterexamples to an 11 x 11 box. It holds for every known dark room below
28 walls and fails at 28.

## Thin-corridor obstruction (2026-11-18)

Witness mining at W = 10 (`d57-witness-mining-r3/`): 0 of 578 open
pairs closed for all real sizes. Lemma U (unreviewed): a point at depth h
in a corridor of width w needs at least 2 sqrt(dh/(Hw)) - 2 reflections,
and 563 of 578 pairs have such a corridor. So no finite set of lighting
paths proves the target at any W >= 10, lattice rooms included. Any proof
needs a limit argument at thin corridors (corridor -> slit), the same
degeneration as Monteil's slit room.

Corridor-limit lemma (`d58-corridor-limit/`, unreviewed): for the 10
door pairs at W = 10, thin corridors are lit except on a non-empty
double-resonance set (all 10 instances built there are lit by short
paths). Chains: a density argument works when every strip is a full
channel and breaks at other hubs. Lattice rooms sit on resonance sets,
so the resonance analysis is the crux.

## Q-class closure (Astra, 2026-11-18)

`.context/qclass-closure/` (computer-assisted; coordinator sample check in
`d71-check-qclass/`): every strictly simple orthogonal lattice room with
W <= 20 that has a parity class with only corner points lights every pair
of interior lattice points, same or different class (780,565 rooms,
3,933,192 pairs). So 22 walls is exact for that class. Open: BBBB rooms
(all four classes have an interior or smooth wall point), area >= 21;
non-lattice marks; 45-degree rooms.

`d72-cylinder-test/`: Astra's common-cylinder criterion holds on all 747
pairs in the 9 known true BBBB rooms (exact SL2(Z) orbit test). Its only
failures (11 pairs in d64 rooms with a proper factor, smallest cov446) are
visible axis-parallel pairs on a cylinder boundary, so a closed-cylinder
variant survives everything tested. No proof route from r <= 8 seen.

## Results record

Start with `d70-writeup/RESULTS.md` (2026-11-18): theorems with status,
counterexamples, the reduction chain, the open statement OL, dead ends.

## Strategy step-back and tower test (2026-11-18)

`d59-strategy/`: no published result applies. Candidates (a) few
directions, (b) surgery induction and (d) orbit closure are dead; (c) an
effective bound restates the target. Best route was the tower branch of
the group route (FH*, lift-or-certify up the block lattice). Estimate
(GUESSED): about 5% provable with current tools.

`d60-fh-star-test/` (COMPUTED, rerun by the coordinator): on cross12,
dumb12, R22 and P6, distinct images lit in a minimal factor always lift
(weak reading, 0 violations); the strong reading is false. Equal images
fail: no lift exists when the factor has no regular point over the target
class (PROVED for the R22 5-block factor). At the pillowcase every pair has
equal images, so the tower only relocates the target to "equal images,
uncertified => lit", which needs a fold-converse lemma about paths through
factor poles. Route 1's group half carries no hard content.

## Fold converse (2026-11-18)

`d61-fold-converse/` (lit direction PROVED, reviewed sound with fixable gaps in d62;
tests COMPUTED and rerun): for equal images in a factor N, light comes from
the live component K of the image point: at most two pole-end partial
involutions (path K) or the monodromy around K (cycle K), restricted to
2-cycles for corner avoidance. 0 disagreements with ground truth on 405
named-room rows. The open step is the realization lemma over the canonical
factor N_x = Q/B_x (degree <= 36): equal images, no Rig or Cut => some
basis joins S~ and T~. That lemma plus d46/d52/d56/d16 gives the W <= 20
orthogonal target.

`d62-review-d61/`: d61 lit direction sound with fixable gaps (state maps
on sheets; quantify the realization hypothesis); independent billiard check
0 mismatches. `d63-realization/`: the realization lemma equals "x-dark =>
certificate" for same-class pairs and needs room hypotheses (d14 n = 10,
cross scaled by 3). Case N_x != B is finite (area <= 8r; enumeration not
run, needs approval). Case N_x = B is per-class Lemma H, the old dead end.
0 counterexamples on 722 test pairs.

`d65-nx-equals-b/`: the per-lift-pair lemma is false (S10, 12 walls,
half-turn symmetric: delta-pairs dark and uncertified at x = b, d; room pair
lit). Lemma M: such pairs are swapped by a room symmetry. `d64-finite-case/`
(approved enumeration, 27 CPU-min, completeness checked): in all 2,800 rooms
with W <= 20 and some class with 1 < deg N_x < n, every same-class interior pair is lit, so the
finite case is closed by computation. But per-target realization fails on
830 rows (smallest room 1843, W = 12). The usable form is pair-level:
"dark at every target => certified". Open: that form when N_x = B.

`d66-pair-level/`: pair-level chain written. The one open lemma OL:
in rooms R* (r <= 8, area >= 21, every class has N_x = B or Q), any two
interior same-class lattice points are lit at some target with N_x = B. No
certificate can exist there, so OL is a pure lit statement; it is infinite
(every normalized room with area > 8r is in R*). Per-target forms fail
inside R* too (cov4181, cov4269). Relay lemma handles symmetric pairs.
Remaining: asymmetric rooms (Lemma H territory). Also open: different-class
pairs (G1), non-lattice rational marks (G2); d64 unreviewed.

`d67-review-d64/`: d64 sound with fixable gaps; independent billiards
light all 6,680 pairs; own brute force to n <= 16 matches. `d68-one-target/`:
OL's one-target sub-case is empty (two Q classes force area <= 2r + 2 <= 18).
Rooms with one Q class have area <= 4r + 4 = 36 (finite; closable by an
approved bounded search). Open: all R* rooms with area 21-36 (BBBB and BBBQ; finite, never
enumerated) and BBBB rooms with area > 36 (infinite). Corrected 2026-11-18
after d70: d68 shows area > 4r+4 forces BBBB, not that BBBB needs it.

## Dead ends (don't repeat without a new idea)

Bounded reflections; Lemma H via monodromy groups; finite-blocking theorems
(lattice rooms are torus covers); EMM finiteness (ineffective); enumeration
by area; twisting one-parameter families; band stabilization with bounded
periods; rigidity without the wall bound; counting and rank bounds from the
Astra exchange (`d25-astra/`); absolute thick-thin size reduction (scaling makes it equivalent to the target; `d40-thick-thin/`). Multi-parameter covering certificates: work for two parallel bands (`d41-two-param-cover/`), but crossing row/column parameters aren't periodic and degenerations need unbounded P, so they don't scale to W <= 20.

## If you resume

Bring a new idea for the lit side, then test it first against P6 (`d30`)
and the 22-wall room. Searches need Daniel's approval and caps.

## Large-room route (2026-11-20)

Details: d70-writeup/RESULTS.md §11 (consolidated 2026-11-20, d88).
- Reviewed: condition (i) for n ≥ 120, r ≤ 8 (d78, d79); irrational marks lit
  for n ≥ 120 (d80); D58 placement, chains, reversals (d76, d77).
- Open core (superseded by the d82 line below): condition (i) for 21 ≤ n ≤ 48
  (d81 got n ≥ 49, reviewed in d82); different-parity pairs; 45-degree.
- d82: midpoint-necessity.md is a sound algebraic lemma, but dark ⇒ (ii-alg) is OPEN.
  Open core: show one of ≥ 2⌈2n/3⌉−16−⌊n/2⌋ off-class candidates is reached by a real path (r ≤ 8).
- 2026-11-20 update: d81 reviewed in d82, so (i) holds from n ≥ 49; open for 21 ≤ n ≤ 48.
  Cylinder certificates reviewed (d84) and close U2; the 12-wall crosses defeat them (d87: sound; one cross pair proved lit, the rest finite evidence).
  Shadow budget on Q: true without a constant (d86: sound, citation fix needed), but the gap is on the
  cover U, whose genus grows with area. Open target: hidden count on U ≤ αn + K, α < 5/6
  (α < 3/2 for n ≥ 120). Details: RESULTS.md §11.
- Dead end: per-corner route charging (shared-reflex.md); bounded-length shadows (d85).

## Effective route status (2026-11-21)

Reviewed tools: effective corridor (d124), large-rectangle access (d125), band absorption and CRT placement (d128). cov279 stretches are closed for all pairs when 3 ∤ q (d127). Reviewed obstructions: threshold methods fail on cov279 (d126), and no fixed direction menu works for τ₀ ≥ 5 (d129). No reflection bound, even at τ₀ = 3 (d130). No horizontal band-passage bound (d131; vertical and mixed decompositions open). Primitive dark flats split into axis factors (d133, conditional on d132). Finite-flat theorem: logic sound, but it needs Filip-type algebraicity for strata with marked points, which has no located source (d132). marked-algebraicity.md supplies it (d134, sound with medium gaps); the semialgebraic parameter map (d132 gap 2) remains. The finite-flat theorem extends to 45° walls (d135). An explicit-H census is infeasible (d136). Corner-orbit rigidity holds but is generic (d137), so it gives no area bound by itself. Current attempt: bound the covering degree d of rigid dark rooms by cylinder avoidance (area = cd/8 for mixed rooms; area 20 needs d ≤ 160 or 80). Correction: d39's area-20 bound covers only essential-Rig certificates, not d137 rigidity, and the mixed 45° census has gaps at 25–40 half-tiles (rigidity-area.md). Earlier attempt: parametric definability of the dark relation (Presburger via uniform interval-exchange acceleration). Estimate 10–12%.

**Census coverage gap (d138, 2026-11-22).** The d11 mixed census enumerates canonical45 rooms, whose diagonal walls lie on x ± y ∈ 2ℤ. Rooms with one diagonal intercept even and one odd (e.g. M, area 27/2) are not equivalent to any canonical45 room, and d9 doesn't cover them. So the 45° census claims hold only for canonical45 rooms. Closing this needs a census run, which needs Daniel's approval.
The 45° similarity maps these rooms to canonical45 rooms of twice the area (d139), so d11 covers them only through original area 8. Area 20 needs A/B pairs at N = 34–80 and A–B pairs at every N.

**Midpoint folds closed (d140–d142, 2026-11-22).** No translation quotient blocks all lift pairs by half-turns at W ≤ 23 (d142). R22's darkness is a path-dependent 2-adic parity argument, not a midpoint fold. Current attempt: the per-class fold converse via a reachability lemma (per-class-relay.md, in review as d143).
Per-class status (d144): at W = 20, two of the three primitive classes can be blocked for a lit pair (cov4181). Current attempt: a wall budget showing that blocking all three costs ≥ 22 walls.
Wall budget (d145): R22's darkness costs a corner-only site plus all 6 axial reflexes. BBBB rooms have no corner-only fiber, so a dark BBBB pair needs an obstruction with no clean fiber and no corner-only factor. Current attempt: prove that every developed-path exclusion factors through a corner-only quotient.

**Exclusion descent (d146, 2026-11-22).** Reviewed sound with gaps: cov4181's exclusion descends to its unique 4-sheet quotient with a regular blocked site, so only the some-site structure conjecture survives. BBBB rooms (universal-B_x definition) have no pillowcase factor of outer degree 2-4. Degree >= 5 is the open case.

**Cross fully lit (d147, 2026-11-22).** Reviewed: the b=7 odd cross is lit at all 2,346 interior lattice pairs, in the specified class for every same-parity pair (16 residuals closed by out-of-pencil slopes). Named-room evidence for reconnection on larger factors; not a general theorem.

**Deletion invariance (d148, 2026-11-22).** Reviewed: only the pencil-restricted form is refuted (DB55). Class-level form is open; evidence for it: all 272 pairs on 4 named rooms lit in all 3 classes. Single-arc <A^3,D^3> criterion verified (0 mismatches in 79,724 rows).

**Cyclic criterion (d149, 2026-11-22).** Reviewed sound with gaps: the per-slope criterion is exact on DB55, and the cusp reduction is finite but has index > 100,000 there, so it isn't a usable census. The open core is the existence of a first legal shot per orbit (Astra's local-global.md, Q97).


**Repair and density (d150, d151, 2026-11-22).** Both reviewed sound with gaps. Lighting a class reduces to one legal shot per marked affine orbit (d151), and a fixed route repairs by sliding crossings (d150). The open statement is unchanged: existence of a first legal shot per class in BBBB rooms, with no bound on its height.

**Uniform tail refuted at W=22 (d152, 2026-11-22).** No uniform corridor-length cutoff exists in general: R22 is dark at short arms and lit at long ones. Any finite reduction for W<=20 must be one-way descent (darkness survives shortening) or use W<=20-specific input. Descent is open (d153 running on its parity form).

**Open core restated (d154, 2026-11-22).** Every known darkness certificate type is already excluded below 22 walls. So W<=20 reduces exactly to certificate completeness: does every totally dark lattice pair in a BBBB room have a certificate of a known type? Gap bounds don't help with that. The orthogonal gap lemmas also don't extend to 45-degree walls.

**Constructive lemmas (d157, 2026-11-22).** Reviewed: every interior lattice pair in a two-rectangle room is lit within 6HD+5 reflections, and a terminal-cap lemma is proved conditionally. The open obligation is a slope interval clearing every mandatory door at once. d158's dumbbell shows large door denominators don't give one.

**Joint obstruction identified (d158, 2026-11-22).** The obstruction on a word aimed at T pairs the visits at times t and D-t (a time-reversal pairing). A far-cap reflection breaks the pairing in the dumbbell. The chain obligation: show that every W<=20 BBBB pair has an itinerary whose t <-> D-t pairing is broken, with a joint slope interval.

**Per-itinerary test (d159, 2026-11-22).** The joint-interval criterion is ordinary unfolding legality restated. The live question is an itinerary-length bound uniform or linear in the edge lengths, which would make each W<=20 skeleton a Presburger sentence (the decision run needs Daniel's approval).

- 2026-11-22 d161: adjacent-arm theorem sound with gaps; class = rectangle/L/T/plus only, no W 14-20 coverage. Estimate unchanged 10-12%.

- 2026-11-22 d162: stacked-hall theorem sound with gaps; first BBBB class at W 14-20 (tall halls only). DB55 is a two-sided stacked hall, so Astra's M2 (two-sided, all lengths) would cover it. Estimate unchanged 10-12% pending the d163 ledger.

- 2026-11-22 d163 ledger (computed; review d165): 4,574 W<=20 words; 6 COVERED, 4 PARTIAL, 4,564 OPEN. Astra's M3 target 1: rooms with dents in one direction only (1,020 words). Estimate 10-12%; report the ledger split beside it.

- 2026-11-22 d164 attacker: no dark pair in 10 stacked-hall edge rooms; extra mechanisms are multi-bounce hall paths and attachment-wall bounces (overhang, DB55). Estimate unchanged.

- 2026-11-22 d165: ledger reviewed sound with gaps; M1 done. Split 6 COVERED / 270 PARTIAL / 4,298 OPEN. Estimate 10-12%.

- 2026-11-22 d167: overhang-escape and nonspanning-entry sound with gaps; first non-hall mechanism, no ledger word moves. Split 6/270/4,298, estimate 10-12%.

- 2026-11-22 d166 (local joint criterion) and d168 (Ferrers W=10) sound with gaps. LLLLLRLRLR PARTIAL provisional on d169. Split 6/270+1/4,297, estimate 10-12%.

- 2026-11-22 d169: d15 r=3 table sound; W=10 has 578 open position-type pairs (Ferrers 1 ... two-bank 298). Split 6/271/4,297, estimate 10-12%.

- 2026-11-22 d170: Ferrers W=10 second region sound with gaps; residual is three named shapes outside all tests. Split 6/271/4,297, estimate 10-12%.

- 2026-11-22 d172: pyramid lemma sound with gaps. Split 6/273/4,295; W=10 now 0 COVERED, 4 PARTIAL, 4 OPEN. Estimate 10-12%.

- 2026-11-22 d171: d17 chord lemma reviewed sound; Ferrers union incomplete (infinite residual region, named rooms U1, U2, U2b). Split 6/273/4,295, estimate 10-12%.

- 2026-11-22 d174: floor-return tail sound; Ferrers still PARTIAL with an infinite residual (V1, V2, family). Split 6/273/4,295, estimate 10-12%.

- 2026-11-22 d173: word-independent winding test sound with gaps; R22 sits exactly at its rank-one equality. Missing: a delta lower bound, beam existence, and per-gate windows. Split 6/273/4,295, estimate 10-12%.
- 2026-11-22 17:15 d175 done: winding obstruction is strip-only; full per-gate windows light all named lit pairs. Astra parks winding (winding-assessment.md). Stopping rule fires: estimate 10-12% -> 7-9%. d176 opened on L1 subset-action branch.
- 2026-11-22 16:20 d176 SOUND: L1 subset-action branch closed. Open L1: natural action, primitive 21-48 squares, imprimitive, area bound. Estimate stays 7-9%.
- 2026-11-22 16:50 d177: 17 of 24 shear-box rooms confirmed; 2-300 unresolved (possible cap artifact, follow-up running).
- 2026-11-22 16:58 d178 SOUND: algebra cannot close the natural branch; L1 core = reachability of a swap pole. Estimate 7-9%.
- 2026-11-22 17:20 d177 done: 2-300 FAIL was a cap artifact. 17 of 24 shear-box rooms confirmed, plus 2-300's boxed pairs. Left: 4-244, 7-241, 8-239, 8-240, 9-240, 4-49, and 2-300 unboxed pairs.
- 2026-11-22 17:00 d179 SOUND, no L1 movement. Open L1 core: marked swap-pole reachability on the pair cover Y.
- 2026-11-22 19:20 d180 SOUND, no L1 movement. Y-cover line exhausted (d178-d180). Astra now on d112 end-chamber gluing + decomposition (large => lit).
- 2026-11-22 19:35 d181 SOUND: corridor tail = per-chamber open-end condition. L1 remaining: open-end lemma, W-dependent threshold, no-corridor rooms (DB55 top-line L=3 first). Estimate 7-9%.
- 2026-11-22 19:50 d182 SOUND: ray transfer and row-1 descent (qualitative). L1 now needs W<=20 input: a lit member on every single-gap ray, or a threshold bound. Estimate 8-10% (+1: first descent-type lemma).
- 2026-11-22 20:08 d183 SOUND: DB55 top-line L=3 fully lit for all H>=4 (first no-corridor family closed). Estimate 8-10%.
- 2026-11-22 20:25 d184 SOUND: semilinearity and per-family decidability for parallel/disjoint-perpendicular growth. Estimate 8-10% -> 9-11%. Open: row 4 (meeting perpendicular strips), bounded-gap drift, L3, N0.
- 2026-11-22 20:25 d185 SOUND: DB55 lit at odd L coprime to 5. Family-level; Astra stays on row 4.
- 2026-11-22 20:50 d186 SOUND: all four growth rows now have descent (row 4 qualitative). Qualitative L1 per chart assembled modulo finite-flat; explicit G open (dark-flat height bound). Estimate 9-11%.
- 2026-11-22 21:08 d187 SOUND: L1 = finite-flat (d132/d134 + classifying-map completion) + one estimate H(C). Estimate 9-11% -> 11-13%.
- 2026-11-22 21:30 d188 SOUND: mixed seed removes probe obstruction. H(C) needs occupied-crossing transfer (or bounded-modulus gate version). Estimate 11-13%.
- 2026-11-22 21:45 d189 PASS WITH CORRECTIONS: occupied-crossing route switching via fixed upper chamber (given one first-hit interval). Open: growing upper run, growing source depth d, two-gaps-per-axis. Estimate 11-13%.
- 2026-11-22 22:05 d190 PASS WITH CORRECTIONS: dark ⇒ a/gcd(a,2d) bounded (uniform in template scaling, growing d). Open: fixed-ratio growth a:2d, two-gap product, two growing upper depths, far roof opening. Estimate 11-13%.
- 2026-11-22 22:35 d191 PASS WITH CORRECTIONS (both): fixed ratio + fixed template ⇒ finitely many dark placements; dark product forces ratio proportionalities. Open: ratio→1 (a=1, d→∞), then fixed ratio with h/t bounded. Estimate 11-13%.
- 2026-11-22 23:05 d192 PASS WITH CORRECTIONS: h/t>H* lights all source depths. With d190/d191: fixed upper template at an occupied crossing ⇒ finitely many dark placements. Open: u or t growing with the lower box (comparable scales). Estimate 11-13%.
- 2026-11-22 23:30 d193 PASS WITH CORRECTIONS (3 notes): explicit area bound on both stretches u,t in the anchored overlap class, for lower-wing sources with transverse target approach. Open: source inside template-width column. Estimate 11-13%.
- 2026-11-23 05:38 d194 PASS WITH CORRECTIONS: first-entry lemma; inside-column source bounded when opposite side solid or H≥b. Open: H<b two-component return. Estimate 11-13%.
- 2026-11-23 07:05 d195 PASS WITH CORRECTIONS (partial, conditional strip return). Reviewer: crossing line fragmenting; Astra redirected to a crossing reduction theorem with a decreasing invariant. Estimate 11-13%.
- 2026-11-23 07:25 Daily audit (audits/2026-11-23.md): only L1 moved, qualitatively; ~25% busy work, ~40% fragmenting crossing chain. Resonance stopping rule fired: estimate 11-13% → 9-11%. New stopping rule in PROGRAM.md: numerical N0 for LLLRLLLRLR by 2026-11-24 20:00 or stop the crossing chain.
- 2026-11-23 08:55 d196 PASS WITH CORRECTIONS: stopping-rule test gives NO numerical N0 for LLLRLLLRLR (G(C) unbounded). Crossing chain stopped. Actual-area route judged not distinct; a real new route needs a darkness-preserving shrink. Estimate 9-11% → 8-10%. Awaiting Daniel on the next route.
- 2026-11-23 09:25 d197 CORRECT WITH MINOR GAPS: shrink-descent first test is a method limit for L1. Cap transfer works iff s·r ∈ hZ and fails in the parity class v2(h) > v2(s) + v2(Δy). The one-visit gluing criterion is exact. Estimate unchanged at 8-10%. Astra is on exterior induction (bbbb/l1-shrink-exterior-induction.md). Stop it if it needs a slope-denominator bound.
- 2026-11-23 09:40 d198 CORRECT WITH MINOR GAPS. Shrink-descent route stopped under its early-stop clause: transfer needs a slope-denominator bound. Cap avoidance is proved only for one or two adjacent columns. The route's limits are in bbbb/l1-shrink-route-limits.md. Both L1 descent routes (chart descent, shrink descent) are now stopped. Estimate 8-10% → 7-9%. Next route awaits Daniel; Astra is drafting a 1-page proposal.
- 2026-11-23 10:45 d199 CORRECT WITH GAPS: dark-structure route stopped (its lemma restates the goal at W ≤ 20). Kept facts: N = 29+6k for the d152 three-chamber family, which is primitive unless k ≡ 1 mod 5 or 7, so factor certificates are impossible there. Any L1 proof for such rooms needs a non-factor mechanism. Estimate unchanged at 7-9%. Next: lighting-tail form of L1 on the three-chamber family (the reversal problem), stopping 2026-11-26 20:00.
- 2026-11-23 11:00 d200 CORRECT: the d152 three-chamber family X=Y=3k+1 is fully lit for all k ≥ 1. This is the first positive L1 lighting tail on a family with no factor certificates (d199). Ledger unchanged at 6/273/4,295. Estimate unchanged at 7-9%: one family, and no W ≤ 20 mechanism yet. Astra is on the general pocket lemma (bbbb/l1-pocket-lemma.md).
- 2026-11-23 11:15 d201 CORRECT: pocket lemma and the aligned three-chamber theorem (any corridor lengths). Ledger split moves to 6/274/4,294: LLLLRRLLRRLLLLRRLLRR OPEN → PARTIAL. Estimate 7-9% → 8-10%: the first reusable lighting mechanism, which also separates R22 (no pocket). Astra is on neck phases (bbbb/l1-neck-phase.md). First open: a non-3×3 chamber, area 32.
- 2026-11-23 11:35 d202 CORRECT WITH GAPS: the 3×4 middle-chamber family is fully lit for all neck lengths. Correction: the word's first open area is 21 (e.g. three 2×3 chambers), not 32. Ledger unchanged at 6/274/4,294. Estimate unchanged at 8-10%. Astra is on the general chamber-size theorem (bbbb/l1-chamber-general.md).
- 2026-11-23 12:08 Long-neck lemma stopped at its 8-versus-9 step (bbbb/l1-long-neck.md, unreviewed). A 6-reflex room with arbitrarily long unit necks has no d201 pocket, so pocket absence can't distinguish R22. For unnormalized rooms, dilation makes an absolute-C tail equivalent to the whole problem. Six L1 routes today have found no 8-versus-9 mechanism. Estimate 8-10% → 6-8%. Strategy question sent to Daniel.
- 2026-11-23 12:45 d204 CORRECT WITH GAPS: the Presburger step of per-pattern decidability is false (quadratic gate conditions). Surviving form: eventual periodicity of the lit set per word (open). Estimate unchanged at 6-8%. Astra is writing the encoding assessment (bbbb/decide-encoding.md).
- 2026-11-23 12:55 One-neck cover test stopped (bbbb/one-neck-cover.md): the lighting-tail tools leave an unbounded parameter region uncovered even in the simplest word, LLLLRRLLLLRR. They don't scale to whole words. Estimate 6-8% → 5-7%. Theory routes have stalled. Astra is drafting a census-extension plan (design only) for Daniel's decision.
- 2026-11-23 13:00 d203 CORRECT WITH GAPS (chamber-general arithmetic test). The aligned layout stays open, and the ledger is unchanged. Final per-word review.
- 2026-11-23 13:12 WRONG CLAIM CORRECTED: L2 was recorded as "done to area 20", but d9/d29 tested only same-parity pairs at areas 17–20 (bbbb/census-parity-audit.md). Different-parity pairs are verified only through area 16. Gap fill (areas 17–20, different parity) is queued before area 21 in d205-census-a21.
- 2026-11-23 13:32 L2 MOVED (author claim, review d206 running): d205 lit all 1,604,242,406 pairs at exact area 21 (538,025,823 rooms, W ≤ 20) and backfilled 726,251,893 different-parity pairs at areas 17–20, 0 dark, 0 orbit referrals, every witness plane-replayed. 59 CPU-min total, far below the 0.7–3 core-day forecast. Area-22 forecast 2–4 CPU-hours (needs Daniel). Astra briefed on a BBBB area bound (target A ≤ 25).
