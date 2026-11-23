# d185 review: DB55 at odd corridor lengths coprime to 5

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
`d95-review-queue/snapshots/2012/l1-db55-odd-lengths.md`. It extends
`l1-dbas55-top-phase.md` in the same snapshot directory, which
[d183](../d183-review-db55top/review.md) reviewed as Sound. Context read: d183,
the d112 review, and the whole-room and A′ statements in
`qclass-closure/bbbb/resonant-gluing.md`.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
14.7 CPU seconds with exact `Fraction` arithmetic. It logs 168 PASS lines and
0 failures. `trace()` and `dumbbell()` are copied verbatim from d183. The
level-stepping `flow()` and the cylinder `chord()` are d183's, generalized
from span 13 to span C = L + 10. Every room is d110
`dumbbell(5,0,H1,5,0,H2,2,1,L)` at a named L and named heights. Every traced
velocity is one that the note prescribes. No room, ray, direction, or word
search was run.

## Bottom line

**Sound.** For every odd L coprime to 5 and all integer heights H1, H2 ≥ 4,
every two distinct real interior points are lit. Unequal heights are included.
The even-L reduction to a discrete grid is also correct. I found no High or
Medium gaps, and five Low ones about wording and one unstated step.

| Claim | Verdict |
| --- | --- |
| Room: boxes [0,5]×[0,H1] and [C−5,C]×[0,H2], corridor [5,C−5]×[2,3] | Matches d110's constructor at all 32 tested settings. Area is 5H1 + 5H2 + L |
| t = 5 return u ↦ u + 10 mod 2C; two cycles iff 5 ∤ L | Sound for every L and both heights. 4,448 traced adversarial returns pass. The traced permutation has gcd(10, 2C) cycles at 7 named rooms |
| t = 10 return u ↦ u + 20; two cycles iff L odd and 5 ∤ L | Sound. Traced: 2 cycles at L = 1, 3, 7, 21; 4 at L = 2, 4; 10 at L = 5 |
| Invariant ±x ± ty (mod 2) at section y = 2 | Sound. 384/384 lifts match at six rooms; negation swaps cylinders every time |
| t = 5 survivors: x and 5y integral, equal x − 5y parity | Sound. Half-integer survivors have lifts on both rim parities (3/3 traced) |
| t = 10 survivors (odd L): equal x parity | Sound |
| Case split: same box, band, corridor and mouth, far-box band, opposite banks, same bank | Sound and exhaustive |
| Bank shots at speed (50k, ±1) | Sound. 1,152/1,152 shots reach the target on 24 named rooms |
| Corner test a + εb ≢ 0, ±10 (mod C), and the C = 11, 13 sign fixes | Correct. Controls stop at the predicted corner |
| The note's four replays | Reproduced exactly: same k and contact counts 94, 610, 571, 1,778 |
| Even-L reduction and the L = 2 example | Correct, including the failed congruence for (2,1)–(8,1) |
| Remaining normalized lengths 2, 4, 6, 8, 12, 14, 16, 18 | Correct, given d112 at L > 20. See "What remains" for L ≡ 0 (mod 5) |

## Cylinder return map

**Return.** Take direction (t, 1) with t a positive multiple of 5. Use the
upward section y = 2 across (0, C). Over the corridor this is the outgoing
side of the floor reflection. In one band crossing the phase advances by t.
Each box excursion returns to the same abscissa and sense:

- Upper excursion into box i: horizontal travel 2(Hi − 3)t, a multiple of 10.
- Lower excursion: 4t, a multiple of 10.
- Over the corridor: an immediate reflection at its roof or floor.

So the upward return is u ↦ u + 2t mod 2C, for any integer heights. The
heights enter only through the vertical period of the cylinder. Every corner
has an integral abscissa, and all phase shifts are integers. So a nonintegral
u never meets a corner, and the itinerary is constant on unit intervals.

**Cycle count.** The return permutes the 2C unit intervals in gcd(2t, 2C)
cycles. The log tabulates this for L = 1 to 40 and checks it for L up to 1,000:

| Direction or modulus | Two classes exactly when |
| --- | --- |
| t = 5, gcd(10, 2C) | 5 ∤ L (any parity) |
| t = 10, gcd(20, 2C) | L odd and 5 ∤ L |
| same-bank shot, gcd(100, 2C) | L odd and 5 ∤ L |
| opposite-bank shot, gcd(50, 2C) | 5 ∤ L |

So the "controlled cycle structure" in the brief holds exactly on odd L
coprime to 5. At even L, t = 10 gives 4 cycles. At 5 | L, t = 5 already gives
10 cycles of length C/5.

**Traced evidence.** §2 starts at 1/1000 on either side of every integer
phase in [0, 2C). This covers every phase whose seam, floor, roof, or section
abscissa is a corner. It runs at L = 1, 3, 7, 9, 11, 21, 2, and 5, at heights
(5,5), (5,9), (7,15), and (31,4), for t = 5 and 10. Each return lands at
u + 2t with the predicted vertical travel. A full 31-return cycle at
(L, H1, H2) = (21, 31, 4), t = 10, closes exactly.

**Invariant and coverage.** The transverse invariant of a lift is
sx·x − t·sy·y + 2t (mod 2). The reference shift 2t is even, so this is the
note's ±x ± 5y. §3 checks it on 8 marks near corners and mouth lips at six
rooms. The d183 covering argument carries over unchanged. A nonintegral
invariant puts a lift in an open cylinder. Negating both signs puts another
lift in the other cylinder. An integral invariant puts the regular mark in
both closures.

**Survivors.** All four lifts on rims at t = 5 means x ± 5y ∈ ℤ. Then x and
5y are both integers or both strict half-integers.

- Half-integers: flipping sx changes the rim parity by 2m + 1, which is odd.
  So the mark has rim lifts of both parities, and an opposite-rim chord
  reaches any other rim mark. §3 traces three such marks. §4 traces two such
  chords to grid marks, at L = 7 and at L = 3 with unequal heights.
- Integers: all four lifts share the parity of x − 5y.

At odd L, the t = 10 invariant on this grid is x (mod 2), because 10y is even.
So different x parities are on opposite rims and are lit. §4 traces two t = 10
rim chords at L = 9 and L = 11 with unequal heights.

## Case analysis

The survivors are integer x of equal parity with 5y integral, at odd L. The
cases cover every pair:

- **Same box.** The closed box is convex.
- **Both marks in the band (0, C)×(2, 3).** This is a convex open rectangle.
  It includes mouths and corridor points.
- **Box mark and corridor or mouth mark.** d112 A′ covers this at every L.
- **Box mark and a band mark in the far box.** The note extends the d112 A′
  path. The A′ window for A doesn't depend on the target depth z. After the
  portal, the ray's height moves monotonically between the target height and
  the entry height, both in (2, 3). Its horizontal travel z is less than L + 5,
  so it never reaches the far outer wall. §7 traces 36 such shots at six
  rooms. These include targets 1/1000 from the far outer wall and from both
  lip levels, and L = 2 and 5.
- **Both marks in opposite-box banks.** A bank point has y ≥ 3 or y ≤ 2, so
  seam points are bank points. Write a for the left abscissa and b = C − d for
  the right one. The bank legs have depth in fifths, so at speed 50k their
  horizontal travel is a multiple of 10. The leg reaches its seam at the
  mark's own abscissa, which is never 0, 5, C − 5, or C.
  - **Opposite banks.** One crossing: 50k ≡ b − a (mod 2C), solvable because
    gcd(50, 2C) = 2.
  - **Same bank.** Two crossings: 100k ≡ εb − a (mod 2C), solvable because
    gcd(100, 2C) = 2 at odd C. The intermediate phase z satisfies
    2z ≡ a + εb (mod C). The folded z avoids {0, 5, C − 5, C} exactly when
    a + εb ≢ 0, ±10 (mod C). The note's analysis holds. ε = +1 works for
    C ≥ 17. At C = 11 it fails exactly at |a − d| = 1, and at C = 13 exactly at
    |a − d| = 3. In both cases ε = −1 works. §6 confirms this for every odd C
    coprime to 5 up to L = 989.
  - The intermediate excursion has one-way travel 100k or 50k(Hi − 3), both
    multiples of 10. So the cap or floor contact is at the integral abscissa z,
    which isn't a corner.

## Exact checks

Section numbers refer to `checks.log`.

| § | What | Named instances | Result |
| --- | --- | --- | --- |
| 0 | Room vertices and area | L = 1, 3, 7, 9, 11, 21, 2, 5 at four height pairs | 8/8 logged, 32 checked |
| 1 | Cycle-count formula | L = 1 to 1,000 | Two classes exactly in the stated ranges |
| 2 | One return, 4C phases each | 8 lengths × 4 height pairs × t = 5, 10 | 64/64 rows pass |
| 2 | Traced permutation of unit intervals | L = 1, 3, 7, 21 (claim); 2, 4, 5 (controls) | Cycle counts 2, 2, 2, 2; 2 and 4; 10 |
| 3 | Four-lift invariant | 8 marks × 6 rooms × t = 5, 10 | 384/384 |
| 4 | Cylinder chords | 3 off-rim at t = 5, 2 half-integer rim at t = 5, 2 grid rim at t = 10 | 7/7 reach the target |
| 5 | Bank shots | L ∈ {1, 3, 7, 9, 11, 21} × heights (5,5), (5,9), (7,15), (31,4) × all 8 (a,d) × 6 height pairs | 1,152/1,152, up to 8,677 smooth contacts |
| 5 | Note's replays | 4 rows | Same k = 1, 9, 11, 17 and same contact counts |
| 5 | Corner controls | L = 1 and L = 3, rejected sign | Trace stops at (5,2) and (8,3), as the residue test predicts |
| 6 | L = 2 example | (2,1), (8,1) | Both are only on odd rims at t = 5; 100k ≡ 6 or 14 (mod 24) is unsolvable |
| 6 | L = 5 control | C = 15 | 50k ≡ b − a (mod 30) fails for 4 of the 8 (a,d) |
| 7 | Extended A′ | 6 shots × 6 rooms | 36/36 |

The bank-shot heights are: both seams, 1/5 outside both seams, 1/5 under both
caps, 1/5 over both floors, and cap-to-seam. These marks sit next to the
reflex corners, the cap corners, and the floor corners.

## Gaps

### High

None.

### Medium

None.

### Low

1. **State the far-box extension of A′ as a lemma.** The proof needs it for a
   bank mark and a band mark in opposite boxes. d112 reviewed A′ only for
   corridor and mouth targets. The extension is correct, and §7 checks it. The
   note gives one sentence. It should name the two facts it uses: the A′
   window doesn't depend on z, and the final leg stays strictly inside the
   band.
2. **Clean up the seam-level wording.** "A mark in the middle height span,
   2 ≤ y ≤ 3" includes the seams, but the A′ path needs a target strictly
   inside (2, 3). The note then reassigns seam marks to banks. Say "2 < y < 3"
   for the A′ case.
3. **Outer walls aren't corners.** The test excludes folded z = 0 and C.
   (0,2) and (C,2) are smooth wall points, so this is conservative. It's
   harmless, because a sign always passes. This repeats d183 Low 2.
4. **Note the unused parity.** After t = 10, the survivors also share the
   parity of 5y. The shots don't need it. One clause would prevent a reader
   from looking for where it's used.
5. **Name the length convention.** "Horizontally normalized" excludes
   L ∈ {5, 10, 15, 20}. d112 and d108 count those as the DB55 L ≡ 0 (mod 5)
   lengths. The note's list of remaining lengths is correct only under its
   convention. See the next section.

The closing "smallest ledger word still open" line is a ledger pointer, not a
claim proved here. d182 already checked that realization.

## What remains of the DB55 family

The family here is two width-5 boxes with bottoms at 0, the unit mouth at
heights 2 to 3, integer heights H1, H2 ≥ 4, and integer corridor length L.

**Closed for all real pairs and all heights:**

- Every odd L coprime to 5 (this note). This includes d183's L = 3.
- Every L ≥ 21 (d112 whole-room theorem, d = 5, unequal heights allowed).

**Still open:**

- **Even L ∈ {2, 4, 6, 8, 12, 14, 16, 18}.** Any dark pair has integer x and
  integral 5y, sits in opposite-box banks, and shares the parity of x − 5y.
  This set is finite for each height pair, but the height family is
  unbounded. The shot construction fails at L = 2 for (2,1)–(8,1). That is a
  failure of the construction, not a dark pair, as the note says.
- **L ∈ {5, 10, 15, 20}, if the ledger counts them as DB55.** These have
  horizontal gcd 5. An axis scaling maps them to boxes of width 1 with
  corridors 1 to 4, so the note excludes them. Neither this note nor d112
  covers them.

The cylinder method can't reduce the even-L grid further. On that grid,
t = 5m with m odd gives the same rim parity as t = 5. With m even, C even
gives at least 4 cycles. Any other integer t breaks the excursion periods for
general heights. So the even lengths need another mechanism, such as more
middle crossings or a different section. I didn't test any such mechanism.

**Net effect on L1.** The DB55 growth-mode row is now closed on all odd
lengths coprime to 5, for both heights growing independently. This removes
d181's mixed L-and-H family except at the 8 even lengths, and at the 4
lengths divisible by 5 if those count. No global area bound or ledger closure
follows.
