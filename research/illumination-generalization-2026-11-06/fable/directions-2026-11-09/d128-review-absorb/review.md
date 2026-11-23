# D128: review of the band-absorption note

Date: 2026-11-21. Reviewer: independent referee.

Reviewed file: `band-absorption.snapshot.md` in this directory (49 lines). Its predecessor, `thin-room.md`, is under separate review in `../d127-review-thin/`. I didn't edit it or evaluate it beyond the steps this note reuses.

Own code: [checks.py](checks.py), log [checks.log](checks.log), 9.0 CPU-seconds. It uses exact integers and `Fraction`. It doesn't import the author's replay. It has a generic billiard tracer for orthogonal lattice polygons. The tracer fails on any corner contact. Every traced path is a certificate built from the note's formulas. The script does no search over directions or reflection words. The only enumerations are the following:

- Integer congruence checks for claim 2.
- The note's own finite case rules: the three step-3 options, and the two-band sheet flips.
- Lattice rectangles in the cross for claim 5.

No information went to outside services.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | cov279: the width-(2q+3) band gives g = 2; the width-3q band gives g ≥ 2q at the least preserving period | Sound with fixable gaps (low) |
| 2 | P = lcm(2u_i/d_i); a middle band absorbs F iff F ∈ gcd(dP, 2u)ℤ; the p-adic form | Sound with fixable gaps (low) |
| 3 | CRT placement on a pairwise-coprime monotone chain; polynomial slope bound | Sound with fixable gaps (low) |
| 4 | cov279 replays at q = 8, 10, 14, 20 (6,430 pairs) | Sound. The construction justifies the claim, conditional on d127 |
| 5 | Odd cross: bands 4×(b−2), 2b×4, 4×(b−2); every contained rectangle has shorter side ≤ 4 | Sound |

## 1. Choice of absorbing band in cov279

The room has bands (0,2q), (2q−3, 2q+3), (2q, 3q) and (4q, 2q), written as (left end, width). The route has travels (1,2,1,1,1), with the bottom reflection.

**The arithmetic is exact.** For every even q coprime to 3 in {4, 8, 10, 14, 16, 20, 22, 28, 40, 52, 64}, the script finds:

- Middle band of width 2q+3: P = 12q and g = gcd(12q, 4q+6) = 2.
- Middle band of width 3q: P = lcm(4q, 2q, 4q+6, 4q) = 4q(2q+3) and g = gcd(P, 6q) = 2q exactly.

The proof is short. Because 3 ∤ q, gcd(4q+6, 3) = 1, so gcd(4q(2q+3), 6q) = 2q · gcd(2(2q+3), 3) = 2q. For 3 | q, gcd(12q, 4q+6) is 6 or 18 at q = 6, 12, 18, so 6 divides it as the note says.

**Gap 1a (low): the note shows only that the invariant fails, not that a match fails.** The note's outer placement comes from the proved shot. On that placement F is already solvable with k = 0. The note says this ("independently of whether that particular F is already solvable"). A reader still wants one legal placement on which the width-3q band fails. The script builds such placements from the note's own step-3 options. At each q = 8, 10, 14, 16, 20, every seam crossing is strictly inside its opening, yet F mod 2q is 4 or 10. Examples:

| q | S | T | Slope s | x₂, x₃, x₄ | F | F mod 2q |
| ---: | --- | --- | --- | --- | ---: | ---: |
| 8 | (1,1) | (33,5) | 14/3 | 15, 59/3, 107/3 | −28 | 4 |
| 10 | (1,1) | (41,5) | 6 | 19, 25, 45 | −36 | 4 |
| 14 | (1,1) | (57,5) | 26/3 | 27, 107/3, 191/3 | −52 | 4 |
| 20 | (1,1) | (81,5) | 38/3 | 39, 155/3, 275/3 | −76 | 4 |

On these placements no leg-preserving shift lets the width-3q band absorb F. *Fix:* add one such row.

**Gap 1b (low): the threshold q ≥ 16 isn't sharp.** On the uninterrupted upward route from (2q−1, 1) to (6q−1, 5), the first unit step forces s mod 4q into (−2, 4). The backward unit step from T then lands in (6q−5, 6q). That interval misses (4q, 5q) exactly when q ≥ 5. The script confirms this at q = 4, 5, 6, 8, 16, 28. *Fix:* write q ≥ 5, or keep q ≥ 16 and call it sufficient.

## 2. The exact absorption test

**Preserving group.** In one run of width u_i and travel d_i, the phase mod 2u_i fixes the folded position and sheet. Interior seam points and interior reflection points aren't band corners, so this map is one-to-one there. So Δs preserves the run's end event iff d_iΔs ∈ 2u_iℤ, that is, Δs ∈ (2u_i/d_i)ℤ. Runs chain, so preserving each end event preserves the next entry. The intersection of the rational lattices a_iℤ is lcm(a_i)ℤ, where v_p(lcm) = max_i v_p(a_i). This gives the stated P and the stated p-adic exponent. The target leg is traced backward from T. Its seam phase is E(T) − d·s, and kP preserves it as well. Inside an open band, extra vertical-wall bounces don't create corner contacts, because the band's corners lie on its top and bottom lines.

**Match.** With all outer events fixed, the shift s + kP changes the middle-band requirement to dPk ≡ F mod 2u. That holds for some integer k iff F ∈ dPℤ + 2uℤ = gcd(dP, 2u)ℤ. The script checks this against brute force on eight explicit systems. Six of them have g ∈ {14, 16, 20, 24, 30}. The other two have g = 2 and g = 2/3. In every case P equals a brute-force minimum. The p-adic formula holds for p ≤ 13. For every F tested, formula solvability agrees with direct solution of the congruence: between 25 and 281 values of F per system.

**Parity.** Across a seam on sheet e, the two band origins give phases that differ by (l′ − l)(1 − e) ∈ 2ℤ. Folding changes the phase by multiples of 2u_i. At a lattice mark, E ≡ X mod 2. So F ≡ Y − X − Ds mod 2, and Ds ∈ 2ℤ gives F ∈ 2ℤ. The script confirms F ∈ 2ℤ and 6s ∈ 2ℤ on all 113 (q = 8) and 365 (q = 14) four-band certificates. "Parity suffices iff 2 ∈ gℤ" is correct. The prime p > h remark is also correct: v_p(d_i) = 0, so v_p(g) ≥ 1 > v_p(2).

**Gap 2a (low).** The statement "Ds ∈ 2ℤ gives F ∈ 2ℤ" needs integral wall abscissas and a placement with Ds ∈ 2ℤ. The note assumes both but states neither in that paragraph. *Fix:* add "with integral walls, for a placement with Ds ∈ 2ℤ".

**Gap 2b (low).** The phrase "absorbs every parity-compatible mismatch" quantifies over all F ∈ 2ℤ, not over F values that legal placements realize. The note's own caveat ("a violating prime can be harmless for a particular F") covers this. *Fix:* state that it's the parity-only guarantee that fails, as gap 1a illustrates.

## 3. CRT placement

**The construction is correct.** On the positive sheet at every seam, entering band i at x_{i−1} gives phase x_{i−1}. After travel d_i the phase is x_{i−1} + 2kd_i. Exiting on the positive sheet at x_i needs 2kd_i ≡ x_i − x_{i−1} mod 2u_i, which is the note's congruence. Same horizontal parity makes the right side integral. If gcd(d_i, u_i) = 1 and the widths are pairwise coprime, CRT gives one k mod ∏u_i. Since x_i lies strictly inside the overlap, the fold returns x_i itself. A window of width greater than 2 contains integers of both parities. The generalized-CRT criterion k_i ≡ k_j mod gcd(m_i, m_j) is standard. The script checks it against brute force on four systems, two solvable and two not.

**Explicit chain.** The script uses a 16-wall staircase with the following bands:

| Band | x range | y range | Width |
| --- | --- | --- | ---: |
| 1 | [0,5] | [0,3] | 5 |
| 2 | [2,9] | [3,5] | 7 |
| 3 | [5,14] | [5,7] | 9 |
| 4 | [11,15] | [7,10] | 4 |

The widths are pairwise coprime. The openings are (2,5), (5,9) and (11,14). The script runs four prescribed pairs through the generic tracer. Each lands on T with the predicted vertical travel and no corner contact. Each crosses every seam at the chosen site on the positive sheet. For S = (1,1), T = (13,8) and sites 3, 7, 13, it gets k = 708 ≤ 1,260 = ∏u_i and slope 1,416.

**Polynomial bound.** k ≤ ∏u_i ≤ U^m with m bands. At r ≤ 8 a tree path has m ≤ 9, so the slope is at most 2U⁹. This is polynomial in the maximum width U, with degree at most 9.

**Gap 3a (low).** The end legs' travels depend on the mark heights. "gcd(d_i, u_i) = 1 for every run" is therefore a condition on each pair, not on the chain. For example, band 4 has width 4. A target at height 9 gives d = 2, which breaks the hypothesis. *Fix:* say "every same-parity pair whose end travels are coprime to their widths".

**Gap 3b (low).** A mark at a seam height has a zero-travel leg. The note doesn't say which run it belongs to. *Fix:* assign it to the next run and drop the empty congruence.

## 4. The cov279 replays

I wrote the certificates from the note's formulas: steps 1–4 of the four-band crossing, the two-band Bézout rule with its sheet flips, and the (3q,3)→(5q,5) cap shot. My own tracer traced them in the polygon.

| q | 3 ∤ q | Same-parity pairs | (1,5) pairs | Traced lit | Two-band rules used |
| ---: | --- | ---: | ---: | ---: | --- |
| 8 | yes | 502 | 113 | 502 / 502 | 218 plain, 14 source-flipped, 1 cap |
| 10 | yes | 811 | 181 | counted only | — |
| 14 | yes | 1,651 | 365 | 1,651 / 1,651 | 716 plain, 26 source-flipped, 1 cap |
| 20 | yes | 3,466 | 761 | counted only | — |

The total is 6,430, as the note says. Same-height pairs are direct chords inside one open interval, which the script checks. Every four-band shot has exactly one horizontal-wall event, at y = 0, and vertical travel 6. Every step assertion holds without change at q ≡ 2 mod 3: the nonzero phase in steps 2 and 3, 4q < x₄ < 5q, 2q < x₃ ≤ 3q, and g = 2.

**Justified by construction or only by replay?** By construction. The step that uses 3 ∤ q is gcd(12q, 4q+6) = 2. The two-band gcds gcd(2q, 2q+3) = 1 and gcd(2q+3, 3q) = 1 also use it. No step uses q ≡ 1 mod 3. The thin-room theorem states "even q ≥ 4 coprime to 3", and all four values qualify. So the claim holds, conditional on the d127 review of that proof. The replays are confirmations. I didn't check the DB55, DBas or DBw2 controls.

## 5. The odd cross

With the cross centered at the origin, the arms are |x| ≤ 2, |y| ≤ b and |y| ≤ 2, |x| ≤ b. The horizontal bands are 4×(b−2), 2b×4 and 4×(b−2). Here is the proof:

- A contained rectangle of width greater than 4 has points with |x| > 2 at every one of its heights.
- Those points lie in the horizontal arm, so the rectangle's height is at most 4.
- The same holds with x and y exchanged.

The script confirms that the maximum shorter side over contained lattice rectangles is 4 at b = 5, 7, 9, 11. The maximum band height b−2 exceeds h₀ once b > h₀+2. At b = 9 the tracer replays the shot from (6,0) in direction (−1,−1). It reflects at (4,−2) and (−2,4) and reaches (0,6), with vertical travel 10. I didn't verify the sentence on d124 access time. It's a sketch of the argument already accepted in the d126 review, gap 4a.

## Ranked gaps

| Rank | Gap | Fix |
| --- | --- | --- |
| Low | 1a: no legal placement shows an unsolvable F in the width-3q band | Add the q = 8 row: s = 14/3, F = −28 ≡ 4 mod 16 |
| Low | 3a: end-leg coprimality depends on the pair | Make the hypothesis per pair |
| Low | 2a: the parity paragraph omits integral walls and Ds ∈ 2ℤ | State both |
| Low | 2b: "every mismatch" means every F ∈ 2ℤ, not every realized F | Say that only the parity-only guarantee fails |
| Low | 1b: q ≥ 16 isn't sharp | q ≥ 5 suffices |
| Low | 3b: marks at seam heights | Assign them to the next run |

## Scope

The arithmetic core is correct: the exact preserving period, the gcd test, its p-adic form, and the CRT class. The cov279 example shows that the choice of absorbing band matters, with g = 2 against g = 2q. The script also exhibits legal placements where the width-3q band can't absorb F. The existential question at the end of the note stays open, as the note says.
