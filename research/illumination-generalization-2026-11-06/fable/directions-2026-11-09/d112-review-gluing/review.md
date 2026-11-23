# D112: review of qclass-closure/bbbb/resonant-gluing.md

Date: 2026-11-20. Reviewer: independent referee. This review covers the
revision saved at 14:35, which adds the L > 4d whole-room theorem and the
polynomial bound. All computation is exact (`fractions.Fraction`), Python with
`-B`, about 6 CPU-minutes in total. Only named rooms are used: DBas, DB55 and
DBw2 (d110's `geom.room`), with the corridor length L changed. Some tests also
absorb corridor stubs into the chambers. No room, direction or witness search
was run. Slopes are either listed constants or are solved from the note's
equations.

## Verdicts

| Claim | Verdict |
| --- | --- |
| A. L > 4d lights every real pair in a rectangular dumbbell (monotone-jump argument) | Sound. Every step checks by hand. The construction, run literally, lights 2,676 constructed cross pairs at 9 room and length settings. All 20,824 thresholds crossed are downward jumps. |
| A'. Chamber mark to corridor or mouth point, at every length | Sound. 900/900 traced at L = 1, 2, 3, 5, 21. |
| A''. The two printed DBas paths at L = 21 | Correct. F(1/13) = 0, and three tracers agree on both paths and both door heights. |
| B. Polynomial bound L ≥ 8d(N+1) for expanding approaches | Sound for cross pairs. 4/4 traced on DBas with stubs. Scope is narrower than the verdict line suggests (see below). |
| 1. Gluing equation, both directions | Sound. Scope (one traversal, nonaxial) is stated correctly. |
| 2. Common period lemma | Sound. 2,160/2,160 exact translate comparisons agree. Both negative controls fail as expected. One wording gap: K depends on the mark abscissas, so no single K serves every real mark. |
| 3. Fixed aperture, large L | Passes, but the period lemma adds nothing here. At integer L every lattice case has g = 2w. Now superseded by A for rectangular ends (threshold 21 against d110's 595,360 to 1,127,680). |
| 4. r = r_A + r_B + 4, induction limits | Sound. Counts check on all three rooms. The stated limits are correct and needed. |
| 5. Reflex-corner normal form and global return | Sound by hand, and conditional as stated. No computation. |
| 6. Scope | Closes every rectangular dumbbell at L > 4d, for all real pairs and every w. The BBBB r ≤ 8 core stays open. See "Scope". |

## A. The L > 4d theorem (top priority)

**Leg phase.** Measure height from the door floor, so the door is (0, w). Take
a mark below the door at depth h, with horizontal distance x to the portal
wall. Its upward ray visits the portal wall at travel A_j = x + 2Dj. Height
rises monotonically from −h to below w, so no horizontal wall or chamber
corner is touched. Every earlier portal visit lies strictly below the lip,
unless s = h/A_j. With j the first index such that sA_j > h:

- if j ≥ 1, then p ≤ s(A_j − A_{j−1}) = 2Ds < w;
- if j = 0, then p < sD < w/2.

So entry is legal. Marks above the door are symmetric, with f = −w + p. Marks
at door height start toward the farther lip, so f = εy + sx with sx < w/2. All
of this checks.

**Jumps.** As s rises through h/A_j, the first index drops from j+1 to j. No
smaller index can qualify, because sA_i < h still holds. Penetration falls
from 2Ds to 0+, so the jump is downward. The two legs' jumps are both downward,
including simultaneous ones. f(0+) exists and f(s) > f(0+). `linear.py`
evaluates both one-sided branch values exactly at every threshold it crosses.
All 20,824 are strict downward jumps.

**Sign of the backward leg.** φ_B = −f₂, because the forward sign is the
negated backward sign at the same height. So F = Ls + f₁ + f₂ is the gluing
mismatch of claim 1. This is correct.

**Root.** F(s) > Ls + B, and Ls₁ can exceed 2w ≥ M − B with s₁ < w/(2d)
exactly when L > 4d. Thresholds accumulate only at 0, so [s₀, s₁] holds
finitely many. Take the first open piece on which F exceeds M. Its left limit
is strictly below the previous piece's right-end value, which is at most M. So
F crosses M inside that open piece, at a regular slope. The corridor entry and
exit heights lie in (0, w), so corridor reflections are smooth. The argument
uses no rationality and no bound on w. Exact resonance plays no role. I found
no gap.

**Other pair types.** Same-chamber pairs, and pairs in the closed strip, see
each other directly in a convex open set. For chamber to corridor, p > 0 is
equivalent to A > hz/t. The preceding visit is below the floor exactly when
A < hz/t + 2D(1 + h/t). That window is longer than 2D, and its lower end is at
least 0, so some A = x + 2Dj lies in it. Penetration is t − zs ∈ (0, t). These
cases cover every pair, including marks on both open mouths.

**Exact checks** (`linear.py`, `linear.log`):

| Check | Result |
| --- | --- |
| DBas L = 21, S = (1,3), T = (27,3), slope 1/13 | Indices j = 1, 2 with A = 14, 17; F = 0. Velocity (13, −1) reaches T. Door heights are 25/13 and 22/13. The own tracer, d110 `geom.shoot` and d109 `path.shoot` all agree. |
| DBas L = 21, S to (6, 3/2), velocity (10, −3) | Reaches the target after crossing (5, 9/5), on all three tracers. |
| Constructed witnesses, all lattice cross pairs plus 44 real pairs per room | DBas L = 21, 22: 224/224 each. DB55 L = 21, 25, 30, 35, 105: 300/300 each. DBw2 L = 21, 40: 364/364 each. The d110 tracer agrees on every one. |
| Real pairs | These include 40 random marks with large denominators, plus 4 marks 1/10007 off each lip and 1/9973 from the portal wall. |
| Chamber to corridor, 60 random real pairs per room and length | 900/900 reach the target at L = 1, 2, 3, 5, 21. |

DB55 at L = 25, 30, 35 and 105 has L ≡ 0 (mod 5), the resonant case that d108
left open. The theorem closes it for L ≥ 21.

**Below the threshold (outside the claim).** The same construction still lit
every lattice cross pair of DB55 and DBas at L = 19 and 20. It fails for some
pairs at L ≤ 18: for DB55, 8 pairs at L = 18 and 256 at L = 1. So 4d is
sufficient but not sharp for these rooms. This proves nothing for L ≤ 18.

## B. Polynomial bound for expanding approaches

The proof checks:

- On t = 1/s ∈ (2d/w, 4d/w), the unfolded abscissa at height distance h_j is
  x + σh_j t. Reflection in integer vertical lines preserves integrality, so a
  corner contact at a listed level needs this abscissa to be integral.
- Each level excludes at most ⌈2dh_j/w⌉ values of t.
- Expansion means every other ray passes each level and reaches the lip.
- After the lip, the next portal visit rises by less than 2ds < w.
- The widest remaining slope component has width at least w/[4d(N+1)].
- F′ > L, so L ≥ 8d(N+1) gives a range longer than 2w.

**Test** (`poly.py`). DBas with 3 corridor units absorbed into the left
chamber and 2 into the right: runs [0,5] to [0,8] and [0,4] to [−2,4], d = 8.
Four pairs were tested, including real marks and door-height marks. In each
pair the exclusions were within N and the widest component met the bound.
The sealed tracer confirmed both words constant across the component.
F = 2wm was solved inside it. The full DBas polygon at corridor length
5 + 8d(N+1) reaches T (N = 32, 0, 32, 51).

**Scope gap (wording).** The theorem covers only cross-chamber pairs whose two
approaches both satisfy run containment. It says nothing about the following:

- same-chamber pairs in a nonconvex chamber;
- collar pairs;
- chambers whose approach contracts.

The note says so in its last paragraph. The verdict line "Expanding stepped
approaches admit a polynomial threshold" should say "for cross pairs".

## Claim 1: gluing equation

The phase convention is right. In the corridor, φ = (vertical sign)·y on
ℝ/2wℤ advances by s per unit of horizontal travel. So exit = φ_A + Ls, and a
match with φ_B fixes height and sign.

- **If.** Entry and exit heights lie in (0, w), so no lip is touched. The
  corridor has vertices only at its mouths, so every reflection in it is
  smooth.
- **Only if.** Horizontal velocity never reverses inside a straight corridor.
  So "one traversal" means each mouth is visited once, and cutting there gives
  first-hit legs.

Checks (`glue.py`):

- Slopes with F = 2wm, solved on verified charts: 135/135 reach T in one
  traversal (DBas L = 4, DB55 L = 7, DBw2 L = 6). Two DBas cases reach T even
  earlier, by a direct segment. This is still lit, and consistent with the
  claim.
- 900 random-slope trials: the criterion agrees with the traced outcome in all
  900. All of them were non-hits, so this half is weak evidence.
- d109's witness (7, −2) in DBas gives F = 0 exactly.

## Claim 2: common period lemma

`period.py` uses six sealed chambers:

- the four DBas and DB55 rectangles;
- two nonrectangular chambers with corridor stubs (DBas-A+3, DB55-B+2).

It uses 3 marks per chamber, including off-lattice marks. It uses 10 slopes
and all 4 sign pairs, with k = 1, 2, 3. It compares every recorded item: the
signed state at each cut crossing and vertical-wall contact, the exit height
and signs, and regular or irregular.

| Test | Result |
| --- | --- |
| s + kK | 2,160/2,160 agree (436 regular base legs). The horizontal-reflection count changed in 1,308, as the note allows. |
| s + K/2 (control) | 387/436 regular legs change |
| Period of uncut slabs, no mark cut (control) | 331/331 change |

K values are 10 (DB55, lattice marks); 8, 12 and 6 (DBas); and up to 30 for
the mark (7/3, ·). So the mark cuts are necessary.

**Wording gap.** "A common slope-translation period works simultaneously for
every first-hit itinerary in the two chambers" is true for fixed marks. K
depends on the mark abscissas, and for an irrational abscissa no K exists. The
lemma's last sentence says this; the verdict line should too.

The gcd and Bézout step checks. On DB55 with rational L = 21/10, S = (1,1)
and T at local (4,1), K = 10, LK = 21, g = 1 and q = 2. In 152 cases s₁ had
F(s₁) ∈ ℤ \ 2ℤ and did not glue. The translate s₁ + K satisfied
F ≡ F(s₁) + LK (mod 2), glued, and traced to T.

## Claim 3: fixed aperture, large L

The argument passes: a common open chart J with F′ ≥ L gives a match once
L|J| > 2w. That threshold depends on the pair through J. As the note says, the
period lemma isn't needed for it.

At every integer L from 1 to 40, with lattice mark abscissas, all three rooms
give LK ∈ 2wℤ, so g = 2w. Translation therefore gains nothing for integral
data. For rectangular ends the effective threshold is now L > 4d = 20, uniform
over real marks and w. d110's uniform thresholds were K = 1,127,680 (DBas),
736,160 (DB55) and 595,360 (DBw2).

## Claim 4: interface and induction limits

`misc.py` gives r = 4 and W = 12 for each room, and r = 0 and W = 4 for each
sealed chamber. So r = r_A + r_B + 4 holds. The flush-mouth caveat is right:
a flush lip drops a reflex corner.

The limits are correct:

- A sealed-chamber theorem gives neither a mouth velocity nor a path that
  avoids the mouth as a mirror.
- The Q-class and proper-factor closures don't supply the hypothesis for
  arbitrary smaller real-mark chambers.

The DB55 truncation example checks exactly. The first hit is at 11/5, and
after five more visits the developed height 86/5 folds to 14/5 going down.
None of the developed heights for j = 0..10 is a multiple of 5.

## Claim 5: reflex-corner limit

Checked by hand.

- **Cone.** The least separation is |θ − ψ|, because 3π − θ − ψ ≥ |θ − ψ|
  whenever max(θ, ψ) < 3π/2. Chords at separation below π stay in the sector
  and within radius max(ρ, σ).
- **Return.** The half-turn about V* is right.
- **SW departure.** Departure strictly southwest from NW, SW or SE points, or
  from points on the negative axes, never meets the east or north ray.
- **Excluded pairs.** A pair with separation ≥ π must be strictly NW and
  strictly SE, so the line through it has negative slope. V* is strictly below
  and to the left of both marks, so it can't lie on that line.

The result stays conditional on a southwest convex-corner itinerary, as the
note states.

## Scope

**Removed from the open core** (BBBB, r ≤ 8):

- Every rectangular-chamber dumbbell (r = 4, W = 12) with L > 4d is closed for
  all real pairs, at any door width, including exact resonance.
- For DBas, DB55 and DBw2 this means every L ≥ 21. That covers the DB55
  ℓ ≡ 0 (mod 5) family that d108 left open, from ℓ = 25 on.
- It supersedes d110's K tails and d110's gap 2 (collars at w ≥ 2) for
  rectangular ends.
- Chamber-to-corridor pairs are lit at every L.

**Exact remaining gap.**

1. Rectangular dumbbells at L ≤ 4d. The range is finite for each chamber pair,
   but chamber pairs are unbounded. For DB55, ℓ = 5, 10, 15 and 20 remain
   under the reviewed results; coprime ℓ are covered by d108. The construction
   happens to light every DB55 lattice pair at ℓ = 19 and 20, but this review
   proves nothing below 21.
2. Nonrectangular chambers. The polynomial bound covers only cross pairs with
   expanding approaches. Contracting approaches, same-chamber pairs in
   nonconvex chambers, and collar pairs remain open.
3. Rooms without a single separating straight corridor, or with several. Most
   of the BBBB r ≤ 8 set is of this kind. The induction interface gives no
   mouth data there.
4. Multiple-traversal paths, which the gluing criterion does not describe.

## Re-run

From this directory:

    python3 -B -u linear.py > linear.log   # A, A', A'': L > 4d construction, ~6 s
    python3 -B -u poly.py   > poly.log     # B: polynomial bound on DBas with stubs, <1 s
    python3 -B -u glue.py   > glue.log     # claims 1 and 3: gluing iff, gcd translates, ~8 s
    python3 -B -u period.py > period.log   # claim 2: period lemma, ~330 s
    python3 -B misc.py      > misc.log     # claim 4 counts, DB55 truncation example

`chamber.py` holds the exact tracers (own code). `linear.py` imports d110's
`geom.py` and d109's `path.py` and `room.py` for cross-checks.
