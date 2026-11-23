# D110: review of qclass-closure/bbbb/length-periodicity.md

Date: 2026-11-20. Reviewer: independent referee. All computation is exact
(`fractions.Fraction`), Python with `-B`, about 5 CPU-minutes in total. Only
named rooms are used: DBas, DB55 and DBw2 from `d69-bbbb/decomp.py`, with the
corridor length L changed. No room, direction or witness search was run.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Period-one tail for rectangular chambers | Sound. Every step checks. The w = 1 lattice corollary is correct. Two presentation gaps: the note never prints K for its named rooms, and the corollary was already implied, without an explicit K, by the README theorem. |
| 2. Insertion period and DBas unbounded order | Sound. The formula is exact. Directions (7+1040j, −2), j = 1, 2, 3, trace exactly from (1,3) to (11,3) in DBas. |
| 3. DBas marked pair at every L ≥ 2 | Sound. Both phase intervals check. Exact traces at L = 2, 3, 10, 45, 47 agree with d109's tracer. A scan over L = 1..300 traces every admissible slope. L = 1 is the only length with no slope on the second branch. |
| 4. Finite residual list and conditional AP | Sound, with one presentation gap: "such length" should say L* ≥ L₀ explicitly. The conditional statement is stated correctly. |
| 5. Scope | It removes only the tail L ≥ K(d₁,h₁,d₂,h₂) of each fixed rectangular unit-door dumbbell (r = 4), plus one DBas pair at every L ≥ 2. The BBBB core at r ≤ 8 stays open. |

## Claim 1: the period-one tail

**Constants.** The note gives no value of K for any named room. `tail.py`
computes them from the note's formulas.

| Room | Chambers (d, h) | w | η | X | N | K |
| --- | --- | --- | --- | --- | --- | --- |
| DBas | (5,4), (4,6) | 1 | 1/40 | 530 | 7,047 | 1,127,680 |
| DB55 | (5,5), (5,5) | 1 | 1/40 | 450 | 4,600 | 736,160 |
| DBw2 | (5,5), (5,6) | 2 | 1/20 | 290 | 3,720 | 595,360 |

So "for DBas the unit-door corollary applies" means L ≥ 1,127,680. The
earlier DB55 bound L ≥ 450 is about 1,600 times sharper. K grows on the order
of 4096·d·h²/w.

**Door within X.** At slope s ≤ 2η = w/(4d), consecutive portal-wall visits
rise by 2dᵢs ≤ w/2 < w. The door's unfolded copies have period 2hᵢ, so a
copy's lower end lies within 2hᵢ above the first visit. An arithmetic
progression with step at most w/2 enters that open copy before rising w/2
past its lower end. The visit occurs at horizontal travel at most
x₀ + (2hᵢ+w)/η ≤ X. The extra 2d in X also covers a mouth start, whose
first return comes at travel 2dᵢ. This is correct.

**Slope exclusion.** Every chamber corner and door endpoint lies on a
vertical wall at an integral height. So a corner hit, or a change of door
copy, needs y₀ + sx ∈ ℤ at a vertical-wall visit. The visits up to X number
at most ⌈X/dᵢ⌉ + 1, and each excludes at most ⌈ηX⌉ + 1 slopes in [η,2η].
The note's per-factor bounds of ⌈X/dᵢ⌉ + 2 and ⌈2ηX⌉ + 2 are conservative.
At most N excluded points leave a gap of length at least η/(N+1). On a
closed subinterval of that gap, no visit up to X crosses an integer, so both
itineraries and first doors are constant. The sampled runs found at most
1,588 exclusions against N = 7,047.

**Phase.** On a fixed itinerary each signed door phase is the unfolded
height minus a constant. Its s-derivative is the leg's horizontal travel, a
for the forward leg and b for the backward leg. With
F = Ls + ε₁y₁ − ε₂y₂ and ε₂y₂ = −(backward phase), F′ = L + a + b. This is
correct for both door-copy branches (direct and reflected). Since
F(s₁) − F(s₀) ≥ Lδ ≥ 2w at L ≥ 4w(N+1)/η, the range contains a multiple of
2w. There the corridor phases match in height and sign. Both crossings lie
strictly inside the doors, so every corridor reflection hits a smooth wall.

**w = 1 lattice corollary.** With integral door endpoints and w = 1, the open
corridor and open mouths have y in an open unit interval, so they contain no
lattice point. Interior lattice sites lie in the two open rectangles.
Same-chamber pairs are joined by a segment in a convex open rectangle.
Cross-chamber pairs are covered by the theorem. So D_lat(L) is false for
L ≥ K, with P = 1. The README theorem, together with the same two remarks,
already implied this with an unspecified threshold. The new content here is
the explicit K.

**Exact traces** (`tail.py`, `lattice.py`). The scripts follow the proof
literally:

1. Compute the exclusions and the largest gap.
2. Take a subinterval of length exactly δ = η/[2(N+1)].
3. Check that both legs have the same itinerary at its two ends.
4. Check that F′ = L + a + b exactly and that the range is at least 2w.
5. Solve F(s*) = 2wk.
6. Trace the glued path from S on the full polygon.

| Room and lengths | Pairs | Result |
| --- | --- | --- |
| DBas, DB55, DBw2 at L = K and K+1 | 16 real cross-chamber pairs per room and length (96 in total) | All reach T with no vertex hit |
| DBas at L = K | All 180 cross-chamber interior lattice pairs | 180/180 reach T |

The real pairs include lattice marks and marks 1/1009 from a door corner.
They also include marks 1/1013 from the portal wall at door height. Paths
make 19,800 to 56,300 wall reflections. At L = K the phase range is
2.0000 to 2.0005 times w, so the final inequality has almost no slack once δ
is fixed.

## Claim 2: insertion period and unbounded order

For primitive (p,q), inserting Δ shifts the corridor phase by Δ|q|/|p|.
Matching position and velocity needs 2w|p| | Δ|q|, with least solution
T = 2w|p|/gcd(|q|, 2w|p|). This is correct, and T = 1 when q = 0.

The horizontal cylinders of DBas, from d109, are (10,1), (10,2), (26,1),
(8,2) and (8,3). The least common twist needs λh/C ∈ ℤ for each, so
λ = lcm(10, 5, 26, 4, 8) = 520. The derivative [[1,−520j],[0,1]] sends the
holonomy (14,−4) to (14+2080j, −4), primitive (7+1040j, −2). With w = 1,
T = 2(7+1040j)/gcd(2, 2(7+1040j)) = 7+1040j.

`dbas.py` traces these directions from (1,3) in DBas (L = 4). Its own
tracer and d109's `path.shoot` give the same counts.

| j | Direction | Reaches (11,3) | Corridor crossings | Insert T, 2T | Insert 1 |
| --- | --- | --- | --- | --- | --- |
| 1 | (1047, −2) | yes, 316 hits | 162 | both reach the translated mark | vertex hit |
| 2 | (2087, −2) | yes, 630 hits | 322 | both reach | vertex hit |
| 3 | (3127, −2) | yes, 944 hits | 482 | both reach | vertex hit |

No sign ambiguity arose: the initial chart already gives these j. At j = 3
the non-multiples Δ = 2 and Δ = 3125 also reach the translated mark, by
another itinerary. This matches the note's caveat that T is exact for
replaying crossings, not for lighting. The quantifier paragraph that follows
it is correct.

## Claim 3: DBas marked pair at every L ≥ 2

**First branch** (rightward start, odd L). The interval is
((L+11)/4, 2(L+11)/7). Its length (L+11)/28 exceeds 2 exactly when L > 45.
At L = 45 it is (14,16). The endpoint slopes 1/4 and 2/7 hit the vertices
(5,1) and (50,2), as traced. At L = 47, k = 16 gives m = 8/29, which traces
to T.

**Second branch** (leftward start). The left door height above the floor is
2 − 6m, and the right one is 2 − bm with b = 8 − c. The window is
max(1/6, 1/b) < m < min(1/3, 2/b), which equals 1/6 < m < 2/b for b = 6, 7.
Neither leg meets a horizontal wall. Entry is at phase −(2−6m) and exit at
+(2−bm), so (L+6+b)m ∈ 2ℤ. The interval lengths are (L+12)/6 for even L and
5(L+13)/42 for odd L. Both exceed 2 at every even L ≥ 2 and every odd L ≥ 5.
At L = 3 the interval is (8/3, 32/7), which contains 4.

| L | Even k on branch 2 | Traced (own and d109) | Door heights |
| --- | --- | --- | --- |
| 2 | 4 | yes | 9/7, 9/7 |
| 3 | 4 (m = 1/4) | yes | 3/2, 5/4 |
| 10 | 4, 6 | yes | in (1,2) |
| 45 | 10, 12, 14, 16 | yes | in (1,2) |
| 47 | 12, 14, 16 | yes | in (1,2) |

The phase integers 8, 8 and 10 at L = 23, 29 and 45 give developed
displacements (−36,−8), (−42,−8) and (−58,−10). These match d109. A scan over
L = 1..300 traces every admissible k to T. Only L = 1 has an empty interval,
(7/3, 4), which the note excludes.

## Claim 4: localization and the conditional AP

**Localization.** The README cover gives a uniform δ over real starts,
including inward mouth starts. With depth K₁ > 2w/δ, a chamber or mouth mark
of end A lights every corridor point at depth z ≥ K₁ from A. The phase slope
is z + a, and the path stops at the target before the far mouth. Points in
the open strip and on its open mouths have y strictly inside (p, p+w), so
their segment avoids the long walls. Checking every type of pair leaves the
following residual pairs:

- chamber A, including mouth A, with chamber A;
- chamber A, including mouth A, with collar A;
- the same two cases for end B.

The other pairs are covered as follows:

- Mouth A with collar B is covered, because collar B lies at depth at least L − K₁ ≥ K₁ from A.
- Mouth A with chamber B is covered by the two-leg theorem.

The residual list is finite and independent of L. For rectangular ends the
note's δ = η/[2(N+1)] and the 2dᵢ mouth allowance both check.

**AP propagation.** Lattice endpoints unfold to lattice points, so each
witness has a rational direction. Each crossing of the cut shares |p| and
|q|, so one T serves every crossing of a path. A noninteger cut between the
collars that avoids wall-hit abscissae exists. Paths that miss the cut
translate unchanged. New lattice marks in the inserted strip lie outside both
collars and are covered by the long-corridor bounds. The statement is
correct as a conditional: if L* ≥ L₀ is fully lit, then L* + kP* is fully lit
for all k ≥ 0. Here P* depends on L* and on the chosen witnesses.

**Gap (presentation).** "At one such length" should name the threshold. L₀
must exceed the opposite-end threshold and 2K₁, so that the collars are
disjoint and every pair outside them is covered.

The closing caveats are correct:

- The nonsquarefree integers form a union of progressions without being eventually periodic.
- No finite list of real collar marks follows from localization.

## Claim 5: scope

**What this removes from the open core** (BBBB, r ≤ 8, lattice pairs).
Explicit thresholds K(d₁,h₁,d₂,h₂) cover each fixed two-rectangle
unit-door dumbbell, a 12-wall family with r = 4. For example, DBas has
K = 1,127,680, DB55 has 736,160 and DBw2 has 595,360. Above K, every lattice
pair is lit. For any integral w ≥ 1, every real cross-chamber pair is lit
above K. The note also proves that the single DBas pair (1,3)–(5+L+c,3) is
lit at every L ≥ 2.

**Exact remaining gap.**

1. Rectangular unit-door dumbbells at 1 ≤ L < K. That range is finite for
   each chamber pair, but the chamber pairs are unbounded, and no
   computation covers them.
2. Width w ≥ 2. The collar residual pairs are finite per room but unproved.
3. Nonrectangular ends. Same-chamber and collar residual pairs remain.
4. Rooms without a separating straight corridor, or with several parallel
   ones.
5. A shortening move that preserves the existence of some dark pair. It must
   hold uniformly in the other gaps, with marks allowed in the removed
   material. The note itself names this gap, and nothing in the note closes
   it.

The note's own verdict line, that room-level periodicity is still open, is
accurate. The DB55 "where five enters" section and the W = 2m rank-count
paragraph were read but not checked numerically. They were not among the
review targets.

## Re-run

From this directory:

    python3 -B tail.py    > tail.log      # claim 1, 96 real pairs, ~85 s
    python3 -B lattice.py > lattice.log   # claim 1, 180 DBas lattice pairs at L=K, ~185 s
    python3 -B dbas.py    > dbas.log      # claims 2 and 3, cross-checked with d109, ~5 s

`geom.py` holds the dumbbell polygons and the exact edge tracer. `dbas.py`
imports `../d109-check-dbas/path.py` and `room.py` for the cross-check.
