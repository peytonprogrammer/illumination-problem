# D118: review of the eight-stop consult note

Date: 2026-11-20. Reviewer: independent referee. Subject:
`eight-stop-consult.snapshot.md` in this directory. Named room `R34-base` only,
exact `Fraction` arithmetic, under 0.1 CPU-seconds in total. No searches over
rooms, rays, directions, or reflection words.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Removing the convex-corner labels: physical shot exists iff some lift pair is joined in X avoiding zeros | Sound with fixable gaps (low) |
| 2a | Criterion, necessity | Sound |
| 2b | Criterion, sufficiency (cone-link minimality) | Sound with fixable gaps (medium, presentation) |
| 2c | Finite test for a fixed marked room | Sound |
| 3a | R34: the criterion forces (3,−1), (4,−1), (5,−1) | Sound, conditional on 2b; certificates replayed exactly |
| 3b | R34: ten reflexes are accessible at S's first primitive step, so eight stops can't trap S there | Sound |
| 3c | R34: class counts and the relay bound (at most 6 primitive intervals) | Sound; counts replayed exactly |
| 4 | Decision section | Not overclaimed. No bearing on the W ≤ 20 goal |

## Claim 1: removing the convex-corner labels

### What the argument needs

A convex corner has four lifts of angle π/2 each, so it glues to one regular
point of X. A reflex corner glues to one zero of angle 6π. A straight line in
X through a convex lift projects to an exact reversal, because the two
perpendicular reflections compose to −I (`checks.log`, last section).

The trimming argument is the one in the staircase manuscript, Lemma
"Reversals do not help" (`manuscript.tex`, lines 219–227). I checked it in
full for a segment in X:

1. Let t_T be the first time the projection γ reaches T. Let t_S be the last
   time before t_T that γ reaches S.
2. Let t₁ be the first convex hit in (t_S, t_T). Then γ(t₁ + s) = γ(t₁ − s)
   for 0 ≤ s ≤ t₁ − t_S. The retraced arc has no corner, so the X segment
   continues through it without obstruction.
3. If t_T ≤ 2t₁ − t_S, then T = γ(2t₁ − t_T) with 2t₁ − t_T in [t_S, t₁).
   That contradicts the choice of t_T. So γ(2t₁ − t_S) = S occurs before
   t_T, which contradicts the choice of t_S.

So [t_S, t_T] has no convex hit, no zero, and projects to a legal shot. The
endpoint lifts can change under trimming. The note says so.

### Axial travel along a wall

A straight line in X that contains a subsegment of a wall lift stays on wall
lifts. Through a convex regular point it continues along the same physical
wall, reversed. It leaves the wall only at a zero. So a segment from an
interior lift S̃ can't run along a wall without passing a zero. The note's
sentence ("cannot start on a smooth wall from an interior mark and tangent
velocity") reaches the right conclusion but doesn't state this reason.

### Counterexample search by reasoning

I looked for a segment through a convex lift whose trimmed projection is
illegal. Step 2 rules it out: the trimmed window contains no convex hit at
all, so nothing illegal survives. A segment through a convex lift whose
*untrimmed* projection is illegal does exist, for example any ray from S that
hits a convex corner and returns. The equivalence is about existence over
lift choices, as stated, so this isn't a counterexample.

### LMW Theorem 2

I read arXiv 1407.2975 v1, pages 1–3. Theorem 2: "For any translation surface
M, and any point x ∈ M, the set of points y which are not illuminated by x is
finite." Section 2 allows singularities of cone angle 2π, "sometimes referred
to as marked points". Corollary 3 states finiteness for rational polygons
directly.

So finiteness of the physical dark set already follows from LMW with the
convex lifts kept as marked points. Section 1 is correct, but finiteness
doesn't need it. Its real gain is that you can work on the unmarked X,
whose zeros are the reflex corners only.

### Gaps

- **Low.** Write out step 3: why T can't occur during the retrace. The note
  compresses it to "encountering no new physical point".
- **Low.** Give the wall-line reason for the axial case.
- **Low.** Say that Section 1 isn't needed for LMW finiteness, which already
  allows marked points (LMW §2, Corollary 3).

## Claim 2: the indispensability criterion

### Setup

The label stabilizer K is the group of affine automorphisms of X that lift
torus maps and fix the fiber over the grid vertex pointwise. That fiber
contains every corner lift and every lift of a lattice mark. The lifts of
the cover's stabilizer form a finite extension by deck maps. Fixing a finite
fiber pointwise costs finite index. So D(K) = Γ has finite index in SL₂(ℤ),
as the note says. This is correct.

### Necessity

If C is indispensable, a relaxed route with only C transparent exists. Its
first and last arms are corner-free legs from C to S and from C to T.
Reflections and straight passages keep |v_x| and |v_y|. Each physical leg
can be started in any of the four copies at C̃, which realizes all sign
changes. So the two legs share an unoriented developed direction. Correct.

### Sufficiency

The steps hold:

1. V_C(S) is Γ-saturated, because K fixes C̃, S̃ and all corner lifts. So a
   shared cusp yields a shared direction.
2. The copy involution with derivative −I fixes C̃ and rotates its 6π link by
   3π. It turns an oriented gap of 0, 2π or 4π into 3π, 5π or π. The note
   says "if necessary apply the involution" without the 3π rotation. That
   rotation is what makes the remaining gaps odd multiples of π.
3. The link fold is a triangle wave of period 3π. A 3π gap means the same
   physical ray. Billiard uniqueness then lights the pair, which darkness
   excludes.
4. Minimality. Γ acts minimally on RP¹ (parabolic powers lie in Γ). The 6π
   link is a 6-fold cyclic cover of RP¹. K's link action lifts Γ's action and
   commutes with rotation by π. A minimal set M projects onto RP¹, so its six
   rotations cover the link. They are pairwise equal or disjoint and closed.
   The link is connected, so M is the whole link. This is correct.
5. Choose k ∈ K that puts the S-leg direction in the first π/2 of some
   sector. The π-arc to the T-leg then lies in one open sector, so the
   projected passage is physically straight. k fixes S̃, T̃ and all corner
   lifts, so both legs stay corner-free.

### A simpler equivalent statement

Steps 1 and the necessity proof together show this: C is indispensable iff
there are corner-free billiard legs from C to S and from C to T whose launch
velocities have equal absolute components. The cusp language is needed only
inside the sufficiency proof. The R22 table in `corner-support.md` already
uses equal-magnitude velocities, so this form matches existing practice.

### Finite test

From a zero on an origami, the map from lattice germ to next lattice germ
is injective. An unabsorbed run would return to the starting germ, which is
a corner. So every rational run is finite. One direction per cusp suffices
by Γ-saturation. Correct.

### Gaps

- **Medium.** State the relaxed route model in the note, or cite
  `corner-support.md`. The criterion is only meaningful relative to it.
- **Medium.** No explicit route certifies any R34 stop. The R34
  indispensability rests entirely on the minimality argument. The R22 stops
  have explicit, replayed routes. To make the R34 result checkable, add one
  explicit relaxed route for (4,−1), for example via the parabolic in
  direction (2,1). This is a fix to the evidence, not to the proof.
- **Low.** Spell out the −I link rotation by 3π (step 2 above).
- **Low.** Say that the criterion needs lattice marks. Real marks give
  irrational directions, and the cusp argument doesn't apply.
- **Low.** The relative links to the staircase manuscript and to
  `fold-converse.md` don't resolve from the snapshot location.

## Claim 3: R34 replays

All data comes from `R34-base` in `../d8-perturbation-test/rooms.json`.
`checks.py` confirms 19 cells, 19 convex and 15 reflex corners, W = 34, and
no pinches. S = (2,0) and T = (6,0) are interior.

### 3a. Three forced stops

The strip cells (1..6, −1) are all present, and x = 1 and x = 7 are walls on
(−1, 0). Each leg below reaches its mark as its first lattice point:

| C | Class | S-leg | Bounce | T-leg | Bounce |
| --- | --- | --- | --- | --- | --- |
| (3,−1) | (1,1) | (−3,1) | x = 1 at y = −1/3 | (3,1) | none |
| (4,−1) | (0,1) | (−2,1) | none | (2,1) | none |
| (5,−1) | (1,1) | (−3,1) | none | (3,1) | x = 7 at y = −1/3 |

In each row the absolute components match. The vertical mirror of the
S-leg is the negative of the T-leg, and the physical rays differ, which
excludes the 3π case. At (3,−1) the π-arc after mirroring contains the
sector boundary, so the note's affine move is genuinely needed.

Darkness of the pair is d105's parity argument, reviewed sound. The
conclusion "every blocking set contains these three" is correct, given 2b.

### 3b. Ten accessible reflexes

All ten listed points are reflex and distinct. Each is the first lattice
point of the ray from S toward it: (1,0), (3,0), (2,1), (2,−1), (1,1), and
(j,−1) for j = 3..7. The four axial rays run between two present cells. The
unlisted reflexes are (5,0), (6,1), (7,−2), (7,0), (7,1).

The passage step uses the same minimality argument as 2b. K fixes the
fiber, so the moved leg still has no intermediate lattice point. With eight
stops, at least two of the ten stay transparent. The note states the
limitation: this names no eventual target.

### 3c. Classes and relays

| Class | Reflex | Convex | Regular sites |
| --- | --- | --- | --- |
| (0,0) | 0 | 7 | S, T, (4,0) smooth, (8,−2) smooth |
| (1,0) | 5 | 4 | none |
| (0,1) | 5 | 4 | none |
| (1,1) | 5 | 4 | none |

This matches the note. The relay bound follows. Intermediate source-class
visits must be (4,0) or (8,−2), each at most once on a simple path. Each
pair of consecutive source-class visits has one off-class visit between
them. So a route has at most 6 primitive intervals and 3 off-class visits.
I checked this bound by reasoning only, not by code. The note is correct
that this doesn't bound the velocity size.

## Claim 4: Decision and bearing on the goal

The Decision section doesn't overclaim. "Nine such reflexes would suffice"
is correct, because indispensable stops are in every blocking set. The
caveat about several-corner routes is correct. An eight-stop blocker in R34
would refute the stop-count route, not the 22-wall target. The note says so.

None of this bears on the open core:

- R34 has a corner-only class, so it isn't BBBB. Q-class closure (d102)
  already settles rooms like it.
- R34 has r = 15. The goal concerns r ≤ 8.
- The relay bound in 3c uses the fact that the source class has only two
  extra regular sites. In a BBBB room every class has interior or
  smooth-wall points, so that bound doesn't transfer.
- "Accessible" corners say nothing about darkness.

What would bear on the goal: a proof that every dark lattice pair forces at
least nine reflexes with equal-magnitude legs to both marks. The note
doesn't attempt this. The criterion is a usable tool for that program, and
the equal-magnitude form in 2b makes it cheaper to test.

This review moves no goal estimate.

## Re-run

```
cd d118-review-eight-stop
python3 -B checks.py > checks.log
```
