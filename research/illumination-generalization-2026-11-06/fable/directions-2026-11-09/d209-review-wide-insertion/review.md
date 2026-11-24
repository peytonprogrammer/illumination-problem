# D209: review of the wide-insertion and terminal-cap collar note

Date: 2026-11-23. Reviewer: independent referee. All tracing is exact
(`fractions.Fraction`). `checks.py` runs in about 32 CPU-seconds under
`nice -n 10`, single process, and prints every number quoted here. Only the two named
rooms (a21 ranks 11 and 18) and one hand-built probe room for the lemma were
used. No search over rooms or directions was run. The only slopes traced for
new pairs are the integers n with |n/L − u/v| < 1/(vD), which is the note's
own window.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Replay period and retained-pair replay | CORRECT |
| 2. E(w−1) new marks; new-new pairs see each other directly | CORRECT |
| 3. Terminal-rectangle collar lemma | CORRECT, with two presentation gaps |
| 4. Ranks 11 and 18 at E = 80k and 1,440k | CORRECT, with one gap: the explicit example omits its signs, and the wrong sign hits a corner |
| 5. Scope and "first open case" | CORRECT WITH GAPS: "first open case" overstates |
| Overall | CORRECT WITH GAPS |

## Claim 1: replay period

A crossing of the cut with primitive direction (p,q) gains transverse phase
E|p|/|q| on a circle of length 2w. Full-state replay needs E|p| ∈ 2w|q|ℤ.
The least such E is 2w|q|/gcd(|p|, 2w|q|). The formula is right, gives 1 for
p = 0, and reduces to d110's formula at w = 1. The strip is bounded by two
straight walls and has no corners, so translating the upper piece preserves
every corner miss. A crossing that coincides with a side reflection at the
cut is handled correctly by continuation.

Recomputed from the archived words (`extract` on shards 48 and 21):

- Rank 11. Crossing seeds (1,1)→(4,3) with (7,4), 5 crossings, period 16.
  (1,1)→(3,6) with (−24,5), 1 crossing, period 5. (4,3)→(3,6) misses the
  cut. **P = 80.**
- Rank 18. Six crossing seeds with periods 8, 32, 18, 20, 20, 20. The other
  four miss the cut. **P = 1,440.**

Every retained pair was replayed exactly with time m + cE/|q|, where c is the
number of crossings. All 3 rank-11 pairs replay at E = 80 and E = 160. All 10
rank-18 pairs replay at E = 1,440, with up to 3,341 reflections. Every
endpoint is exact and no trace hits a corner.

## Claim 2: new marks

The inserted rows are copies of row j, so the points (x, j+1..j+E) with
a < x < a+w have four incident cells. Old points at y ≥ j+1 shift by E. The
count E(w−1) is right. Mark enumeration of the enlarged rooms gives
83 = 3 + 80 (rank 11, E = 80) and 1,445 = 5 + 1,440 (rank 18). The open strip
is convex and contains all new marks, so new-new pairs see each other
directly. 1,980 direct segments were traced (lower cap mark to every new
mark, and 100 random new-new pairs per room). All are legal with zero
reflections.

## Claim 3: terminal-rectangle collar lemma

**Persistence window.** The argument is right. In the unfolding of the
fixed itinerary, every wall endpoint and mouth endpoint is an integer point.
Its axial distance from the lattice start is an integer t with 1 ≤ t ≤ D.
The itinerary can change only when the line passes such a point, at slope
i/t. If i/t ≠ u/v, then |i/t − u/v| ≥ 1/(tv) ≥ 1/(vD). A segment that the
line newly meets must first be met at an endpoint, so it is covered too.
uD ≥ 1 keeps the window inside s > 0.

**Phase sweep.** The endpoint at axial distance L is X_U ± sL, so the open
window maps to an open interval of length 2L/(vD). Target images form two
cosets of 2w, which merge into one coset of w at the center column. This is
right.

**Floor corners.** The floor point is X_U + (F/L)(X_end − X_U). Two images
2w apart give floor points 2wF/L apart. Since F/L = F/(F+y) ∈ (1/2, 1) for
0 < y < H ≤ F, the gap is in (w, 2w) and cannot be a multiple of w. Floor
corners form one coset of wℤ, so at most one of the two floor hits is a
corner. The center-column version, with gap in (w/2, w), is also right.
Between entry and target the path stays strictly below the entrance line,
so the floor corners are the only corners it can meet.

**Attempts to break it.**

- Rank 11 at E = 80. For all 160 new-to-upper pairs, every integer slope in
  the window was traced: 2,675 rays. Every ray first enters through the open
  mouth at exactly axial distance D, with no earlier corner. Every pair has
  at least 4 legal seeds. 4 rays hit a floor corner, and each of those pairs
  still has another legal seed.
- Rank 11 at E = 160 (k = 2). 84 sampled pairs and 2,660 rays. No
  persistence failures, and each pair has at least 8 legal seeds.
- Rank 18 at E = 1,440. 248 pairs (4 upper marks × 62 new marks, including
  y = 2 and y = E+1) and 145,686 rays. No persistence failures. 102 rays hit
  a floor corner, and each pair has at least 12 legal seeds.
- Probe room, rows [7,7,1,15,15], w = 3, mouth (0,1). This tests the
  off-center 4w criterion, which the named rooms never reach. Upper mark
  (1,4) uses entry direction (−1,−3), so s₀ = 1/3 and D = 2. For E = 1..30
  and both new columns there are 930 cases. All 450 cases that meet
  2L/(vD) > 4w have a legal seed. Every window ray in all 930 cases
  persists. 476 of the 480 cases that fail the criterion are also lit, so
  the criterion is sufficient but loose.

No counterexample was found. None is expected, since every step is an
elementary inequality.

**Gaps.**

1. The lemma needs a nonvertical first-entry itinerary for every upper mark.
   The note states this hypothesis ("whenever ... available"). It gives no
   way to produce one when the base cap has no lattice mark (H₀ = 1), or
   when the only archived entry is vertical.
2. "Fix its initial signs" is essential, but the worked example never
   states them (see claim 4).

## Claim 4: ranks 11 and 18

Both caps meet the lemma's hypotheses. Rank 11 has cap [0,2]×[0,2] and
mouth (0,1). Rank 18 has cap [1,3]×[0,2] and mouth (2,3). Each cap has one
lower mark, (1,1) and (2,1) respectively, and no mark lies on the entrance
line.

To get each entrance itinerary, negate the *final* velocity of the archived
seed from the lower mark and trace back until the first downward crossing
of the open mouth.

| Rank | Upper mark | Reversed direction | s₀ | D actual (note bound) | (2v−1)D | E+3 |
| --- | --- | --- | --- | --- | ---: | ---: |
| 11 | (4,3) | (−7,4) | 7/4 | 3 (12) | 21 | 83 |
| 11 | (3,6) | (−24,−5) | 24/5 | 4 (5) | 36 | 83 |
| 18 | (3,3) | (−1,−2) | 1/2 | 1 (2) | 3 | 1,443 |
| 18 | (1,5) | (3,8) | 3/8 | 15 (24) | 225 | 1,443 |
| 18 | (4,6) | (−14,−9) | 14/9 | 8 (9) | 136 | 1,443 |
| 18 | (5,6) | (−23,−5) | 23/5 | 12 (15) | 108 | 1,443 |

The note's bounds, its rank-11 D values (3 and 4), and its maximum of 360
for rank 18 all check. For rank 11 the bound D ≤ 12 would fail at k = 1,
since 7·12 = 84 > 83. So the note is right to use the actual D = 3. The
inequality follows from L > 2vD (center column, w = 2) and L ≥ D + E + 3.
It is monotone in E, so it holds for every k ≥ 1.

**Explicit example.** At E = 80, from (3,86) to (1,2) with slope 211/44:
D = 4, H = 82, L = 88, F = 86, and |211/44 − 24/5| = 1/220 < 1/20. The exact
trace with velocity (−422, −88) for unit time is legal, with 213
reflections. It enters at x = 2/11 at axial distance 4, hits the floor at
x = 31/22, and ends at (1,2). Its replay period is 4·44/gcd(211,176) = 176,
as stated. **Gap:** the note does not give the signs. The reversed archived
seed starts in direction (−,−). With +x instead, the ray from (3,86) hits
the corner (6,86) at t = 1/2. The example is correct only with the
reversed-seed signs, so the note should print them.

**Conclusion.** The entire rank-11 room is lattice-lit at E = 80k, and the
entire rank-18 room at E = 1,440k, for all k ≥ 0. Retained pairs follow
from replay, lower-cap and new-new pairs from direct segments, and
new-to-upper pairs from the lemma. The exact traces cover all pair types:
every rank-11 pair at E = 80, and a sample of more than 200 pairs of each
type at the larger lengths.

## Claim 5: scope

**What is proved.**

- (a) Retained-pair replay at any single-interval horizontal cut of any
  integral width, for E ∈ Pℤ≥0.
- (b) New-new pairs at any width.
- (c) New-to-retained pairs, but only for a **terminal rectangular cap**.
  The component below the entrance line must be exactly a rectangle with a
  flat floor, and must contain the cut. Every upper mark needs a nonvertical
  first-entry itinerary. E must exceed an explicit threshold:
  2L/(vD) > 4w in general, or > 2w on the center column.
- (d) The two named progressions in claim 4.

The general reduction is stated as conditional, which is correct.

**"First open case" overstates.** The note calls the width-two bridge
between two nonrectangular ends the first open case. A strictly simpler
configuration is still open. Take a terminal end with one irregular end
below the cut, such as a stepped or notched floor or an L-shaped foot. The
lemma needs a flat floor, and d110's collar argument needs a long corridor.
The return from that end has the same unknown signed phase that the note
cites for the bridge, but it involves only one irregular end. Terminal
rectangles with no lower cap mark, or with only vertical entries, also sit
outside the proof. Replace "first open case" with "an open case". Alternatively,
name the terminal nonrectangular end as the smallest open configuration.

## Surviving statement

Let a strictly simple polyomino room have a single-interval horizontal cut
y = j + ½ of integral width w inside a terminal rectangle [a,a+w]×[0,H₀].
That rectangle is the whole component below an integral entrance line and
has a flat floor. Suppose the room is lattice-lit at E = 0, and every upper
mark has a nonvertical first-entry seed into the open mouth with data
(u/v, D). Let P be the lcm of the crossing-seed periods
2w|q|/gcd(|p|, 2w|q|). Then the room is lattice-lit at every E ∈ Pℤ≥0 with
2(D+E+H₀+1)/(vD) > 4w for all upper marks. On the center column, or when
w = 2, the threshold is 2w instead of 4w. Ranks 11 (P = 80) and 18
(P = 1,440) are fully lit at every E = kP, k ≥ 0. Some open cases remain:
nonrectangular terminal ends, two-ended short bridges, and caps without a
usable first-entry seed.
