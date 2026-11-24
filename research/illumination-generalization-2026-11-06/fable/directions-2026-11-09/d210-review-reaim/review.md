# D210: review of one-row re-aiming and the all-pair cap thresholds

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [snapshot.md](snapshot.md).
Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
25.4 CPU-seconds, single process, under `nice -n 10`, and reports 0 FAIL.

To rerun it, use `nice -n 10 python3 -B checks.py`.

The tracer in `checks.py` is new and independent of the d209 tracer. It steps
the ray from grid line to grid line in integer coordinates scaled by |p||q|.
At every lattice point it classifies the four incident cells. It reflects on
straight walls and stops on any corner. Only the two named rooms were used:
a21 rank 11 (shard 48, room 1156563) and rank 18 (shard 21, room 4136869),
with row 1 (y ∈ [1,2]) stretched to height 1+E. No search over rooms was run.
The only direction search was for rank 11 at E = 1..6, as the brief allows.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Re-aim identity, error formula e(t), 2wN invariance on every traversal | CORRECT |
| 2 | Gate: integer-level clearance suffices; strictly-lower/higher sharpening | CORRECT, with two presentation gaps |
| 3 | \|δ\| ≤ w/(E+D/k); every E > wvM − D/k, all residues | CORRECT |
| 4 | Cap tables, upper-pair windows, last missed E, K = 7 and K = 151 | CORRECT |
| 5 | Exact verification on the named rooms | CORRECT. Rank 11 is also lit at E = 1..6 |
| 6 | D ≤ 4·area·v and the "first open general step" | CORRECT WITH GAPS |
| 7 | Scope and overclaim | CORRECT WITH GAPS. The rank-11 row of the gap table is now closed |
| | **Overall** | **CORRECT WITH GAPS** |

No error was found. Every gap is presentational, or it is a statement this
review now settles.

## Claim 1: identity, error formula, and traversal invariance

**Algebra.** With s = (Ds₀ + 2wkN)/(D+kE), you get (D+kE)s − Ds₀ = 2wkN.
That gives kEs − 2wkN = −Dδ, so Es − 2wN = −(D/k)δ. At old level t the new
developed coordinate is s(t + E·b(t)). Subtract 2wN·b(t) and the base value
s₀t. The remainder is δt + b(t)(Es − 2wN) = (t − D·b(t)/k)δ. At t = D,
b = k, so e(D) = 0. The log checks this exactly on a grid of D ≤ 12, all
k ≤ D, w ∈ {1,2,3}, E ≤ 8, N ∈ [−2,3], and three values of s₀.

**Invariance on the doubled circle.** In the selected row the walls x = a and
x = a+w are full height, so the transfer is a translation on the circle of
length 2w. Use the circle coordinate U = x − a for rightward motion and
U = 2w − (x − a) for leftward motion. U increases with transverse travel,
whatever the vertical direction. Adding 2wN fixes both the folded x and the
sign. A developed error e maps to a circle error +e on both up and down
traversals.

**Measured.** All 8 crossing seeds of both rooms were re-aimed at E = 1..60
(rank 11) and E = 1..160 (rank 18), for the nearest N and its two neighbors.
At each old level the review compares the new crossing x with the base
crossing x, signed by the base horizontal direction. It skips levels where a
wall falls between them. The measured error equals (t − D·b(t)/k)δ at all
1,158 (rank 11) and 10,866 (rank 18) level visits. The rank-18 seeds from
(3,3) traverse the row down, up, down, up, so downward traversals are
covered.

## Claim 2: the gate

**The argument holds.** A unit row's open slab splits into rectangles
[c,d] × (t, t+1). Their vertical sides are full height, so between two
integer levels the ray can only reflect regularly off those sides. All
vertices are lattice points at integer levels. In the developed chart,
reflections in integral lines map the lattice to itself. So every point where
the itinerary can change has an integral transverse coordinate. The base
coordinate X₀(t) = X₀(0) + (u/v)t has X₀(0) integral. Its distance to a
distinct integer is at least 1/v. The stretched row has no structure strictly
between its two interfaces.

A ray can't switch branch between integer levels. In particular a vertical
wall has no corner inside a row. A bounce exactly at a lattice point on a
vertical wall that continues straight through the level is regular. Perturbing
it moves the bounce into the row below or the row above. Both rows have the
wall at the same x, so the charts agree. That is the note's "vertical-side
bounce may move from one row to the next" case, and it is right.

**Sharpening.** At a level with integral X₀(t) the base point is regular. It
is either an interior lattice point or the interior of a straight wall. Then
the open interval (X₀−1, X₀+1) contains no other lattice point, and both sides
give the same continuation. The sharpened window is right. This step needs
strict simplicity, since a diagonal pinch vertex would be a two-cell lattice
point. The note should say so.

**Attempts to break it.**

- Every window-predicted re-aim was traced: 182 (rank 11) and 1,185
  (rank 18). All are legal and end exactly at the target.
- The sharpening is exercised. In the window-predicted cases, the error at
  integral base levels is nonzero 426 times for (3,3)→(4,6), on both sides
  (212 positive, 214 negative). All of those traces are legal.
- The window edges are real. For (3,3)→(4,6) and δ outside the window,
  472 of 477 traces fail. The first is E = 1, N = 0, δ = −4/65. It hits the
  corner (1,4) at time 2. For (3,3)→(1,5), 264 of 311 fail.
- Outside the window, 233 of 1,679 rank-18 re-aims are still legal. The
  window is sufficient, not necessary, which matches the note's wording.

**Gaps.**

1. Low. The paragraph that interpolates increments from base to proposed
   values is unnecessary and reads as a homotopy argument. Replace it with
   induction on t: if the itinerary agrees through level t−1, the new
   coordinate at level t is X₀(t) + e(t) in the base chart. The window then
   carries the itinerary through level t.
2. Low. State that strict simplicity rules out a regular-looking lattice point
   with two diagonal cells.

## Claim 3: the bound and the threshold

δ = (2wN − Es₀)/(E + D/k). With N the nearest integer to Es₀/(2w),
|2wN − Es₀| ≤ w, so |δ| ≤ w/(E + D/k). N ≥ 0 and s₀ > 0 give s > 0. Then
|e(t)| ≤ Mw/(E + D/k) < 1/v exactly when E + D/k > wvM. The strict
inequality covers the tie |2wN − Es₀| = w. No residue condition enters.

In the log, every case with E > wvM − D/k and the nearest N satisfies the
bound and traces legally: 59 cases (rank 11) and 313 cases (rank 18). The
crossing seeds give these generic thresholds:

| Room | Seed | s₀ | D | k | M | Generic E > |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 11 | (1,1)→(4,3) | 7/4 | 12 | 5 | 18/5 | 132/5 |
| 11 | (1,1)→(3,6) | 24/5 | 5 | 1 | 4 | 35 |
| 18 | (2,1)→(3,3) | 1/2 | 2 | 1 | 1 | 2 |
| 18 | (2,1)→(1,5) | 3/8 | 24 | 5 | 15 | 1176/5 |
| 18 | (2,1)→(4,6) | 14/9 | 9 | 1 | 8 | 135 |
| 18 | (2,1)→(5,6) | 23/5 | 15 | 1 | 12 | 105 |
| 18 | (3,3)→(1,5) | 3/5 | 20 | 4 | 9 | 85 |
| 18 | (3,3)→(4,6) | 3/5 | 35 | 4 | 18 | 685/4 |

The note relates this correctly to d197. The d197 obstruction concerns a
fixed slope. Here the slope changes with E, and N is a free integer.

## Claim 4: the tables

**Cap table.** Every row matches. The review recomputes it by reversing the
archived lower-to-upper seed. It picks the unique sign choice whose level list
is the forward list reversed. Then it finds the first downward crossing of
y = 2 inside the mouth.

| Rank | Upper | Reversed direction | s₀ | D₁ | Interval | Width | E threshold |
| --- | --- | --- | --- | ---: | --- | --- | ---: |
| 11 | (4,3) | (−7,4) | 7/4 | 3 | (5/3, 2) | 1/3 | 5 |
| 11 | (3,6) | (−24,−5) | 24/5 | 4 | (19/4, 5) | 1/4 | 7 |
| 18 | (3,3) | (−1,−2) | 1/2 | 1 | (0, 1) | 1 | 1 |
| 18 | (1,5) | (3,8) | 3/8 | 15 | (4/11, 5/13) | 3/143 | 127 |
| 18 | (4,6) | (−14,−9) | 14/9 | 8 | (3/2, 11/7) | 1/14 | 33 |
| 18 | (5,6) | (−23,−5) | 23/5 | 12 | (55/12, 37/8) | 1/24 | 59 |

The interval is between the nearest distinct ratios i/t with t ≤ D₁. That is
the exact set of slopes with no lattice event at axial distance 1..D₁ other
than the regular ones at s₀. It is wider than d209's |s − s₀| < 1/(vD), and
it is valid.

The two-leg test is right. A direct-leg failure gives (D₁+H−y)Δ ≤ 2. A
floor-leg failure gives (D₁+H+y)Δ ≤ 4. Adding them gives (D₁+H)Δ ≤ 3. Floor
points of consecutive center images differ by 2F/L ∈ (1,2), and floor corners
form a coset of 2ℤ, so at most one of the two is a corner. The direct leg
never reaches the floor. Neither leg reaches the mouth line again.

**Upper-pair windows (rank 18).** Upper-to-upper seeds: rank 11 has one, with
k = 0. Rank 18 has six. Four have k = 0, and one of those is horizontal. Two
start at (3,3) with direction (3,−5) and traverse the selected row at
t = 10, 13, 14, 17. These values all match the note.

| Target | D | M | Window | Last missed E, brute force over N | Residue formula |
| --- | ---: | ---: | --- | ---: | --- |
| (1,5) | 20 | 9 | (−1/35, 1/40) | 57 | 57 (residue 17) |
| (4,6) | 35 | 18 | (−1/85, 1/90) | 150 | 150 (residue 10) |

The brute force tries every N for each E in 0..399. It agrees with the note's
nearest-two-N residue formula.

**All-pair K.** Rank 11: max(5, 7) = 7. Cap-cap pairs are direct, and the
only upper-upper seed misses the cut. Rank 18: max(1, 127, 33, 59, 58, 151)
= 151. Both are right.

## Claim 5: exact verification on the named rooms

Each pair is traced with the note's own construction:

- Cap-cap pairs: a vertical segment.
- Cap-upper pairs: every slope n/L in the persistent interval, for both the
  direct leg and the floor leg, with the reversed seed's signs.
- Upper-upper pairs with k = 0: replay at the archived slope.
- Upper-upper pairs with k > 0: the re-aimed slope for the two nearest N.

| Room | E | Area | Pairs lit | Rays | Persistence failures | Witness kinds |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| 11 | 7 | 35 | 45/45 | 125 | 0 | 28 direct, 14 cap direct leg, 2 cap floor leg, 1 replay |
| 11 | 8 | 37 | 55/55 | 155 | 0 | 36, 16, 2, 1 |
| 11 | 9 | 39 | 66/66 | 189 | 0 | 45, 18, 2, 1 |
| 11 | 10 | 41 | 78/78 | 227 | 0 | 55, 20, 2, 1 |
| 11 | 13 | 47 | 120/120 | 358 | 0 | 91, 26, 2, 1 |
| 18 | 151 | 323 | 12,090/12,090 | 64,499 | 0 | 11,476, 548, 60, 4 replay, 2 re-aim |
| 18 | 152 | 325 | 12,246/12,246 | 65,346 | 0 | 11,628, 552, 60, 4, 2 |
| 18 | 157 | 335 | 13,041/13,041 | 69,668 | 0 | 12,403, 572, 60, 4, 2 |

Mark counts equal 3 + E and 5 + E, and the pair counts are the full
C(marks, 2). Every window ray, about 160,000 in total, makes its first
downward crossing of the cap line inside the mouth at axial distance exactly
D₁. None of 151, 152, or 157 is a multiple of 1,440, and none of 7–10 or 13
is a multiple of 80.

**Rank 11 at E = 1..6.** Every lattice pair is lit at every one of these
lengths.

| E | Area | Marks | Pairs lit |
| ---: | ---: | ---: | --- |
| 1 | 23 | 4 | 6/6 |
| 2 | 25 | 5 | 10/10 |
| 3 | 27 | 6 | 15/15 |
| 4 | 29 | 7 | 21/21 |
| 5 | 31 | 8 | 28/28 |
| 6 | 33 | 9 | 36/36 |

The note's cap window already gives a legal slope for every cap-upper pair,
except one pair at E = 1. A direction search in that room finds a witness for
it. Each witness is re-traced as a full exact path ending at the target. With
E = 0 from the census and E ≥ 7 from the note, **the rank-11 family is
lattice-lit for every E ≥ 0.**

## Claim 6: D ≤ 4·area·v

In a fixed primitive direction (p,q), a ray from a lattice point sits at a
lattice point exactly at integer times. Its state there is a lattice point of
the four-sheet translation surface. Interior lattice points carry 4 states and
wall-interior points carry 2. By Euler's formula the surface has 4·area − 2r
vertices, where r is the number of reflex corners. The flow is invertible, so
the first repeated state is the start state. A first hit therefore takes at
most 4·area primitive steps, and D = m|q| ≤ 4·area·v.

Both base rooms have 48 nonsingular states against 4·area = 84. The
rank-11 witnesses at E = 1..6 use at most 6 steps.

**Gaps.**

1. Low. "before repeating its starting-square state or another state" should
   read "before returning to its start state", by invertibility.
2. Medium. "First open general step" is right only for retained pairs. The
   resulting box bound is E > wvM − D/k ≤ 4·w·area·v². It needs a polynomial
   bound on v for a first-hit seed of every crossing pair. The collar for new
   marks needs a separate, still-open argument except at flat terminal caps.
   The note says this in its last two sentences. The bold label should carry
   the qualifier "for retained pairs".

## Claim 7: scope

**Accurate.**

- The general result applies only to a whole unit row whose section is a
  single interval.
- Both K values are labelled sufficient.
- A missed window is not claimed to mean darkness.
- The d110 numbers match the d110 review: 595,360 to 1,127,680, and the
  first-hit threshold 21 from the length note.

**Needs updating.** The gap table lists rank 11, E = 1..6, as open. This
review closes it. Rank 18, E = 1..150 (areas 23–321), is still unverified.

## Surviving statement

Let a strictly simple polyomino room have a whole unit row [j, j+1] whose
section is one interval of width w. Replace it by a row of height 1+E.

1. Take a lattice seed for a retained pair with slope s₀ = u/v, vertical
   travel D, and k ≥ 1 traversals of the row. Then the slope
   (Ds₀ + 2wkN)/(D+kE) is legal for any N with
   max_t |t − D·b(t)/k|·|δ| below the integer-level clearance. In particular
   the pair stays lit for every integer E > wvM − D/k, for all residues.
2. Seeds with k = 0 carry over unchanged.
3. For the a21 rank-11 room with row 1 stretched, every lattice pair is lit at
   every E ≥ 0. Use the census at E = 0, this review at E = 1..6, and the
   note for E ≥ 7.
4. For rank 18, every pair is lit at every E ≥ 151.
5. A polynomial bound on the axial denominator of first-hit crossing seeds
   would give a polynomial threshold for retained pairs, because
   D ≤ 4·area·v. New collar marks outside flat terminal caps remain open.
