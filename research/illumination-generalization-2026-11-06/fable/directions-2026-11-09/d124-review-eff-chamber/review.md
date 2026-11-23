# D124: review of qclass-closure/bbbb/effective-chamber.md

Date: 2026-11-20. Reviewer: independent referee. The reviewed text is
`effective-chamber.snapshot.md`, identical to the live note at review time.

All computation is exact. It uses `fractions.Fraction` and a small exact field
Q(√5) for the slope α = 1/φ². Python ran with `-B`, about 2 CPU seconds in
total. Only the named DBas, DB55 and DBw2 chambers from d110 `geom.ROOMS` are
used. No room, ray, direction or reflection-word search was run. Every slope
traced is either α itself or the root the note's construction prescribes.
Files: [checks.py](checks.py), [checks.log](checks.log).

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Lattice cross-pair theorem, L ≥ 4wT², T = 1+F_(3m−1) | Sound |
| 1a | Fibonacci phase, block recurrence, three-step growth | Sound. Replayed on all six sealed chambers |
| 1b | Common slope interval α ± 1/(4T²) and exact gluing | Sound. 756/756 cross lattice pairs glue at L = 4wT² exactly |
| 2 | All-real cross-pair bound, L ≥ 36wH², H = 2F_(3m)+1 | Sound |
| 2a | Capped arm on a fixed junction, ℓ ≥ 36w[1+2F_(3m)]² | Sound with fixable gaps (low) |
| 3 | Large rectangles, crosses, local coincidence count, 16-midpoint bound | Sound. One low wording gap |
| 4 | No universal cutoff; H_sync implication; census arithmetic | Sound. No universal cutoff is claimed |
| — | Note as a whole | Sound with fixable gaps. All gaps are low |

## Section 1: explicit cross-pair theorem

**Where the Fibonacci bound comes from.** The ray starts at a lattice point
with developed slope α = (3−√5)/2. Its unit-step letters are
floor((k+1)α) − floor(kα). Each letter acts on the four-copy square-tiled cover
as R (letter 0) or R∘U (letter 1). A portal hit happens only on an R move. So
the hit test is a finite automaton on M = 4·area squares. The prefixes Wₖ of
the Fibonacci word give the recurrences Pₖ₊₂ = Pₖ₊₁ ∪ gₖ₊₁⁻¹Pₖ and
gₖ₊₂ = gₖgₖ₊₁. If four consecutive Pₖ agree, the common set is invariant under
two consecutive block permutations. Those generate ⟨R, U⟩, which is transitive,
so the set is full. Hence |Pₖ| grows every three indices, and P_(3(M−1)) is
full. The travel bound is 1 + |W_(3(M−1))| = 1 + F_(3M−1). I checked every step
by hand.

**Common slope interval.** The cutting word through step T changes only at
p/q with q ≤ T. The identity |α − p/q| = |p²−3pq+q²| / (q²|α′−p/q|) is correct,
and |α′ − p/q| < 3 on [0,1]. So no such fraction lies within 1/(3T²) of α. The
closed interval α ± 1/(4T²) keeps both first-hit words. On it the mismatch is
affine with slope L+a+b, so its range exceeds L/(2T²) ≥ 2w. All lattice contacts
are excluded because kα is irrational for k ≥ 1. The interval is one common
interval for every corner switch, because the proof never leaves the fixed
words.

**Hypotheses.** Strict simplicity of each sealed chamber gives a connected
cover, hence transitivity. Integral mouth width with lattice endpoints makes
the portal a union of unit edges. The straight corridor with physical long
sides makes every corridor contact smooth. The theorem needs no parity,
reflex-count or monotonicity hypothesis; this matches the proof.

**Replay (section 5 of the brief).** See "Replay" below. Every claim in this
section checks.

## Section 2: real marks and the capped arm

**All-real bound.** The block decomposition of the Fibonacci word into
W_(k+1) and Wₖ is correct, so every length-N factor contains Wₖ. The N+1
rotation points −jα stay distinct on I = α ± 1/(12H²), since
‖qα‖ > 1/(3q) ≥ 1/(3H) and each point moves by at most N/(12H²). So every
tie-free length-N word at a slope in I occurs at α and contains Wₖ. The
vertex-contact estimate is also right. Positions at crossings h+j are pairwise
more than 1/(3H) apart at α and move by at most 1/(12H). So at most one
exceptional slope per leg exists. Removing two points leaves a component of
width at least 1/(18H²). There (L+a+b)/(18H²) > 2w at L = 36wH². The argument
is independent of the mark coordinates, as claimed.

**Capped arm.** The arithmetic is consistent. Two junction marks use passage
length 2ℓ, which needs only ℓ ≥ 18wH². A junction mark and an arm mark use the
one-door phase with depth at least ℓ, which needs ℓ ≥ 36wH². The stated
threshold covers both. The d114 projection lemma handles a cap-endpoint
crossing, since each construction crosses the old cap line once.

## Section 3: large rectangles and the synchronized count

- With r ≤ 8, a decomposition into at most r+1 rectangles gives a piece of
  area at least n/9. Correct.
- In the odd crosses P_b the arms have width 4 about [−2,2], so every contained
  rectangle has a side of length at most 4. Correct; `checks.py` confirms it at
  b = 7, 9, 11.
- The complement of U among all off-diagonal components has valency
  n−1−d ≤ 7. The budget 2d′ = R+J gives R ≤ 14 there. Each regular lattice lift
  is one coincidence. So all but 14 lie on U. Correct.
- The source parity class has at most ⌊u/2⌋⌊v/2⌋ interior sites in a u-by-v
  rectangle. Checked for u, v ≤ 30.
- With fixed outside words, the midpoint abscissae are (sₓ ± tₓ)/2 + ku. These
  fold to at most four physical values, and likewise for ordinates. So at most
  16 positions and 32 lifts. Correct.

Nothing in this section claims a deficit. The note says plainly that the area
and valency counts don't supply external itineraries. The H_sync deficit is
still open.

## Section 4: effective consequence and census scale

- The reviewed lower bound at n ≥ 120 is 2(n−8)−16−⌊n/2⌋ ≥ 3n/2−32. With
  H_sync ≤ (3/2−ε)n+K this gives n ≤ (K+32)/ε. Correct.
- 3,933,192 witnesses / 72.5 s = 54,250.9 per second, matching d102.
  1/(54,251·3600) = 5.12×10⁻⁹ CPU-hours per witness. 10¹¹ and 10¹² rooms give
  512 and 5,120 CPU-hours. These match d73's GUESSED range.
- The note states there is no ε, K or universal n₀(r). It doesn't claim a
  universal area cutoff.

## Replay on named chambers

Data: DBas chambers 5×4 and 4×6 with w = 1. DB55 chambers 5×5 and 5×5 with
w = 1. DBw2 chambers 5×5 and 5×6 with w = 2.

| Room | m | T = 1+F_(3m−1) | 4wT² | H = 2F_(3m)+1 | 36wH² |
| --- | ---: | --- | --- | --- | --- |
| DBas | 96 | 1+F₂₈₇, 60 digits | 120 digits | 61 digits | 122 digits |
| DB55 | 100 | 1+F₂₉₉, 63 digits | 125 digits | 63 digits | 127 digits |
| DBw2 | 120 | 1+F₃₅₉, 75 digits | 151 digits | 76 digits | 153 digits |

The exact values are in `checks.log`. For example, DBas has
T = 426547842461739379460149980002442288124894678853713953114434.

**No stand-in was needed.** The corridor is traced analytically by the
d112 phase fold, so L = 4wT² itself is feasible. For each pair the script does
the following:

1. Trace both first-hit legs at α exactly in Q(√5). Launch the source right and
   up, and the target backward left and up.
2. Confirm the first-hit step against the cover automaton.
3. Write F(α) = c + κα, and confirm κ = L+a+b with c rational.
4. Take M nearest F(α)/(2w) and set s* = (2wM − c)/κ. Confirm
   |s*−α| < 1/(4T²) exactly.
5. Re-trace both legs at s* with Fraction. Confirm identical contact words.
6. Fold the corridor and confirm F(s*) = 2wM. Then trace forward in the
   sealed right chamber from the mouth to the target.

| Room | Cross lattice pairs lit by the prescribed path | Max leg travel at α |
| --- | ---: | ---: |
| DBas | 180/180 | 155 |
| DB55 | 256/256 | 74 |
| DBw2 | 320/320 | 123 |

Named cross pairs, with x₂ the right chamber's left wall:

| Room | Pair | a, b at α | 4T²·\|s*−α\| | Contacts before T (A, B) |
| --- | --- | --- | ---: | --- |
| DBas | (1,3)–(x₂+2,3), the d109 marked pair | 94, 58 | 0.2022 | 27, 18 |
| DBas | (4,1)–(x₂+3,4) | 1, 11 | 0.6774 | 0, 3 |
| DB55 | (1,1)–(x₂+3,1) | 4, 3 | 0.4128 | 0, 0 |
| DB55 | (2,4)–(x₂+1,2) | 23, 1 | 0.9062 | 6, 0 |
| DBw2 | (1,1)–(x₂+4,5) | 4, 14 | 0.1767 | 0, 3 |
| DBw2 | (3,2)–(x₂+2,2) | 2, 2 | 0.4971 | 0, 0 |

Each path also makes about 10¹²⁰ to 10¹⁵⁰ smooth corridor contacts. For the
DBas marked pair, all eight combinations of source sheet and backward sheet
glue. This supports "any signed launch works".

**Real marks.** At L = 36wH² I ran three rational marks per room, for example
(7/3, 13/5) and (x₂+5/7, 31/9). All 9/9 glue at the root nearest α. This is a
partial stand-in. The proof's step that removes the two exceptional slopes
would need ties out to N ≈ 10⁶⁰ crossings. I didn't compute them. Instead, I
traced the legs at s* directly and confirmed the α words.

**Cover replay.** For all six sealed chambers the script builds the four-copy
cover. It confirms transitivity and the Pₖ recurrence against direct reading
for k ≤ 10. It also confirms nestedness and three-step growth. The first full
index is k* = 9–11, against the proof's 3(M−1) = 237–357. Supporting checks
also pass. The tail equals the substitution fixed point on 10⁵ letters. The
ones fall at floor(mφ²). The bound |α−p/q| > 1/(3q²) holds for q ≤ 20,000. The
window property holds for k ≤ 10.

## Gaps

All gaps are low. None affects a proof.

1. **Low: planarity of the cap double.** The all-real theorem is stated for a
   strictly simple joined room. The d114 double may overlap in the plane and
   is kept abstract. *Fix:* state that the proofs in sections 1 and 2 use only
   the two sealed chambers and the abstract corridor gluing. Then the theorem
   applies to the abstract double without an embedding.
2. **Low: "no door alignment requirement".** A straight horizontal corridor
   forces the two mouths to share one height span. *Fix:* say the mouth
   position on each chamber side is arbitrary, but the two spans coincide.
3. **Low: "stronger than a whole-room lower count".** The rectangle count
   localizes the d104 bound; it is not numerically larger. *Fix:* say "a
   localized form of".
4. **Low: optional sharpening, not an error.** For a fixed pair of chambers, a
   computed first full index k* gives T* = 1+F_(k*+2). The Pₖ sets are exact
   finite objects. My replay gives T* = 234, 90 and 145. The resulting
   thresholds 4wT*² are 219,024 for DBas, 32,400 for DB55 and 168,200 for DBw2.
   These still exceed d112's 21 for rectangles. For nonrectangular named
   chambers this gives a cheap certified threshold. *Fix:* add one sentence.
   These numbers come from this review's computation, not from the note.

## Scope

The note proves effective thresholds for one-traversal cross pairs in fixed
chambers. It also proves an effective capped-arm whole-room theorem. These are
exponential in chamber area. The note correctly leaves open several cases:
same-side pairs, rooms without a separating corridor, chambers growing with L,
and the H_sync deficit. Nothing in the BBBB core closes.
