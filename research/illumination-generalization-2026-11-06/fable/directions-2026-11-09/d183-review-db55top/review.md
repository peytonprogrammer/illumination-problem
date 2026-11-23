# d183 review: the length-three DB55 top-line stretch

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
`d95-review-queue/snapshots/1952/l1-dbas55-top-phase.md`. It is identical to
`qclass-closure/bbbb/l1-dbas55-top-phase.md`. Context read: d181 (which named
this family as the first open no-corridor case), d182, d112 (review of the
chamber-to-strip lemma), and the linked notes `stretch-stability.md` and
`resonant-gluing.md`.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
6.2 CPU seconds with exact `Fraction` arithmetic and logs 106 PASS lines and 0
failures. `trace()` is copied verbatim from d181, which copied it from d175.
The only room is the d110 `dumbbell(5,0,H,5,0,H,2,1,3)` at H = 4, 5, 7, 15,
31, 101. Every traced velocity is one the note's construction prescribes.
Marks and section phases are named adversarial points that I chose at the
proof's case boundaries. No room, ray, direction or word search was run.

## Bottom line

**Sound.** The theorem holds as stated: every two distinct real interior
points are lit, for every integer H ≥ 4. I found no High or Medium gaps, and
five Low ones, all about wording or citation.

| Claim | Verdict |
| --- | --- |
| Room definition | Matches d181/stretch-stability DB55 top-line stretch at L = 3. The note covers all integer H ≥ 4, a superset of d181's odd H ≥ 5 |
| Cylinder step: return u ↦ u + 2t mod 26, two 13-cycles, invariant ±x ± ty | Sound for every H. 312 adversarial returns and 216 lift-class checks pass |
| Lighting from an off-rim lift; opposite-rim chords | Sound. 7/7 explicit cylinder chords reach the target |
| Survivor set: integer x of equal parity, y in tenths | Sound. The algebra is correct |
| Case split for survivors (same box, middle band, corridor/mouth, three opposite-box cases) | Sound and exhaustive |
| Exceptional-grid shots, speed (100k, ±1) | Sound. 90/90 adversarial shots reach the target at six heights; the note's ε = −1 obstruction is confirmed |
| Chamber-to-strip citation | Correct. d112 reviewed it as Sound at every length, L = 3 included. 12/12 traces pass |
| Note's exact-check table | Reproduced exactly: same speeds, same contact counts (1490, 167, 807, 964, 150) |
| What it closes for L1 | The (NC) target d181 named: the DB55 top-line ray at L = 3. It doesn't close growth-mode row 1 in general |

## Room definition

The note's room is the interior of [0,5]×[0,H] ∪ [8,13]×[0,H] ∪ [5,8]×[2,3].
For each tested H, the d110 constructor gives the same 12 vertices in the same
order. The area is 10H + 3, and the wall gcds are 1. At H = 5 it equals d181's
`ROOMS['DB55']` at L = 3.

d181 and stretch-stability state the family for odd H ≥ 5. The note claims
every integer H ≥ 4. Strict simplicity needs only H > 3, and the proof uses H
only through integrality of excursion lengths. So the wider claim is valid.
The log includes the even case H = 4.

## Case analysis

I checked that the proof covers every real pair for every H, not just the
tested ones.

### Cylinder step (all H)

**Return map.** Take direction (t, 1) with t = 10k and 13 ∤ k. On the upward
section y = 5/2, write u for the band phase mod 26. Each excursion returns to
the same abscissa and sense, because its horizontal travel is a multiple of
10, the doubled box width:

- Upper excursion into a box: 2(H − 3)t = 20k(H − 3).
- Lower excursion into a box: 4t = 40k.
- Over the corridor: the ray reflects at once on the corridor roof or floor.

So the return is u ↦ u + 2t. This holds for every integer H. Seam, cap and
floor abscissas differ from u by integers (t/2 = 5k). Every corner has
integral x, so a nonintegral u never meets a corner.

**Two cylinders.** gcd(20k, 26) = 2 gives exactly two 13-cycles of unit
intervals. Each integral-u leaf eventually reaches a seam phase of 5, 8, 18
or 21, which is a corner. So the rims are singular. The note correctly says
maximality isn't needed.

**Invariant.** X − tY is conserved mod 2 by reflections in integer lines.
That gives u ≡ ±x ∓ ty + 5t/2 mod 2. Negating both signs maps c to −c, so it
swaps the two open cylinders off the rims.

**Coverage.** A point whose invariant isn't an integer can't lie on a leaf
through a corner, because corners give integral invariants. That point is in
an open cylinder. A point with integral invariant is a limit of both
cylinders. So every interior mark is in the closure of both cylinders.

**Corners in the open cylinders.** Convex corners become regular points in
the four-copy surface. The leaves through them still have integral invariant,
so they lie on rims. The open cylinders therefore contain no physical corner
lift, which is the note's "all physical corners forbidden". A chord in an open
cylinder can't run along a wall, because a wall segment ends at corners.

**Reduction.** A pair survives only if both marks have all four lifts on rims
at t = 10 and at t = 20. That means x ± 10y and x ± 20y are integers, which
gives x ∈ ℤ and 10y ∈ ℤ. At t = 100, 100y and 5t/2 = 250 are even, so
u ≡ x mod 2. Marks of different parity sit on opposite rims of one cylinder
and are lit. This algebra is correct.

### Survivor pairs

The survivors are integer abscissas of equal parity with ordinates in tenths.
The cases are exhaustive:

- **Same box.** The open box is convex.
- **Both in the open middle band (0,13)×(2,3).** The band is a convex open
  rectangle, mouths included.
- **One corridor or mouth mark (x ∈ {5,…,8}, 2 < y < 3) with a box mark.** The
  d112 A′ lemma covers this at every L. Use the chamber that holds the box
  mark; z is the depth from that chamber's portal wall. The other mark in the
  band is the previous case.
- **Opposite boxes.** Here a ∈ {1,…,4}, b ∈ {9,…,12}, and b − a is even.
  Points at y = 2 and y = 3 are bank points. Points with 2 < y < 3 are band
  points.
  - **Both in banks, opposite.** a + 100k ≡ ±b mod 26.
  - **Both in banks, same side.** a + 200k ≡ εb mod 26, with the intermediate
    phase z off 0 and ±5 mod 13. The note's residue argument is right. ε = −1
    fails only at (1,11) and (2,12), and there ε = +1 gives sums 12 and 1 mod
    13, both good. Section 7 of the log checks all 8 (a,b) pairs.
  - **Exactly one band mark.** a + 10jk ≡ ±b with gcd(10j, 26) = 2 for
    j = 1,…,9. Mirroring x ↦ 13 − x keeps a and b of equal parity.
  - **Both band marks.** Direct chord.

Every bank leg has horizontal travel 100k·(tenths) ∈ 10ℤ. A same-bank
intermediate excursion has one-way travel 200k or 100k(H − 3) ∈ 10ℤ. Each
returns the same integral abscissa, never 0, 5, 8 or 13. So floor and cap
contacts are regular, and wall contacts can't hit the seam-level corners.
Nothing here depends on H beyond integrality. Seam-level marks use zero-length
legs, as the note says.

## Exact checks

All checks use the verbatim d181 tracer. Section numbers refer to
`checks.log`.

| § | What | Named marks or phases | Result |
| --- | --- | --- | --- |
| 1 | Room vertices, area, gcds | H = 4, 5, 7, 15, 31, 101 | 7/7 |
| 2 | One return, at u = c ± 1/1000 next to every integer u whose upper or lower seam abscissa is 5 or 8, and next to the outer walls | t = 10, 20, 100 on all six H | 18 × 12–20 phases: every return lands at u + 2t with the predicted vertical travel |
| 2 | Full 13-return cycle, u = 5 − 1/1000 | H = 101, t = 100 | Closes exactly; period vertical travel 2026 |
| 3 | First section class for all four lifts of six marks near (5,3), (0,H), (8,2), the corridor roof, (13,0), and the mouth x = 5 | H = 4, 7, 31; t = 10, 20, 100 | 216/216 match ±x ∓ ty + 5t/2 mod 2; negation swaps cylinders in all cases |
| 4 | Explicit cylinder chord: unroll the cylinder, take m returns, transverse offset δ, chord (tΔY + δ, ΔY) | 5 off-rim pairs near reflex, cap and floor corners and the mouth; 2 opposite-rim pairs at t = 100 | 7/7 reach the target. (4,3) sits on short saddle connections, so its leaf was followed backward to the section |
| 5 | Grid shots, k from the note's congruences | 15 pairs per H: seams beside the reflex corners, tenths off the lips, near caps and floors, both ε-exceptional pairs, j = 1, 5, 9, mirrored cases | 90/90 reach the target; at H = 101 up to 19 678 smooth contacts |
| 5 | Control: (1,11) with ε = −1 | H = 7, 101 | z = 21, trace stops at corner (5,2), as the note predicts |
| 6 | Note's table | 5 rows | Same speeds and same contact counts |
| 8 | d112 A′ corridor and mouth shots | 4 pairs × H = 4, 31, 101, including lips at 1/1000 and depth 3 to the far mouth | 12/12 |

The two t = 20 chords in §4 have δ = 0. They are core arcs, the note's
"equal transverse depth" sub-case. The other five chords have δ ≠ 0.

## Gaps

### High

None.

### Medium

None.

### Low

1. **State the covering fact.** "Every lift … is in at least one cylinder
   closure" relies on an unstated step. A non-integral invariant forces a
   regular leaf, hence an open cylinder. An integral invariant is a limit of
   both cylinders. Add one sentence. That also covers convex-corner lifts,
   which are regular points of the four-copy surface but are excluded because
   their invariant is integral.
2. **Outer walls aren't corners.** "Avoid the four physical abscissas
   0, 5, 8, 13" is conservative. (0,2), (13,2), (0,3) and (13,3) are smooth
   wall points. The extra exclusion is harmless, because one sign still
   works in every case.
3. **Name the cited review.** The note links the chamber-to-strip lemma to
   `resonant-gluing.md` and calls it "reviewed". The review is d112 A′, which
   is Sound at every length and traced at L = 3. Cite d112 directly.
4. **Name the H range against the brief.** The note says it covers "the
   entire normalized odd-height family" and states the theorem for all
   H ≥ 4. Both are true. Say explicitly that even H is new relative to d181
   and stretch-stability.
5. **The note's own cylinder check is generic.** It used phases j + 1/4 at
   H = 5, 7. The proof doesn't need more. This review adds phases 1/1000 from
   every corner-critical integer and heights up to 101.

The closing "smallest W ≤ 20 room this result does not cover" sentence is a
ledger pointer, not a claim proved here. d182 already checked that
realization's strict simplicity and turn word.

## What this means for L1

**What it closes.** This is the (NC) target that d181 named: "The DB55
top-line stretch, all odd H at L = 3, is the first concrete target for (NC)."

- In d182's growth-mode table, the family is row 1. There is one diverging
  gap, the y-gap between the seam y = 3 and the cap. Its cross-section is two
  disjoint intervals, (0,5) and (8,13). The growth-modes note itself calls
  out "DB55 top-line growth" as the case where two boxes deepen in one gap.
- The result covers the entire ray, from H = 4 upward, not only a tail. It
  holds uniformly over real marks. d182 noted that its transfer theorem
  can't supply that uniformity (L3).
- The ray is fully lit, so d182's dark-ray contrapositive has nothing to
  descend to here.
- The family still shows that chamber diameter is unbounded at W = 12, so
  (WT) still can't come from diameter-based thresholds. At L = 3 the family
  no longer needs any gluing threshold, because it's lit directly.

**What it doesn't close.**

- Row 1 in general. The modulus 26 depends on L = 3 and the box width 5. The
  note's L = 2 remark shows four transverse classes and an unproved step.
- d181's mixed family with L and H both growing. That needs (WT), or an
  extension of this phase argument to every L.
- Other no-corridor rooms (cov279 real pairs), rows 2–4, and any bound N₀(20)
  or ledger closure. The note says all of this in its Scope paragraph.

**Net effect on L1.** One named open (NC) family at W = 12 is now closed for
all real marks. The remaining L1 obligations from d181, which are (OE), (WT)
and (NC) beyond this family, are unchanged. The method extends to other fixed
corridor lengths only where the middle return has gcd 2 and the intermediate
residue test succeeds. The note says this too.
