# Review: band-chain-characters.md (snapshot 2026-11-22 1332)

**Verdict: sound with gaps.** The construction and both relation statements are correct, and every constructed shot replays exactly. The result is a true, word-independent *sufficient* test for one beam in one chain. It doesn't imply that every W ≤ 20 room is lit, and it doesn't certify the named residuals on its own. On lattice data it reduces to the d168/d170 terminal-strip test at a single depth.

Checks: `checks.py`, output in `checks.log`. Result: 31 PASS, 0 FAIL, 24 CPU-seconds, `python3 -B`, exact `Fraction` arithmetic. `trace()` is copied verbatim from d170. Named rooms only: U1, U2, U2b, T1, V1-761, V2-8051, V3-5111, the 761 V=384 room, R22, and one added control S8. No room or direction search, no network.

## 1. The construction

**Verified steps.**

- **Anchoring and period subtraction.** Adding kP to the slope changes the crossing of middle run j by kPdⱼ ∈ 2uⱼℤ. That is a whole number of fold periods, including reflection parity, so every gate position and outgoing velocity is unchanged.
- **Endpoints.** Going back a from gate 1 gives A − kPa. Going forward gives B + kPb after the middle periods are removed. The errors are err₁ = X − (A − kPa) mod 2w and err₂ = Z − (B + kPb) mod 2V. |errᵢ| < δ is exactly kα ∈ θ + (−ε₁, ε₁) × (−ε₂, ε₂). The check confirms this on 60 pairs.
- **Interpolation.** The slope σ = kP + (err₂ − err₁)/D is constant. The gate offset is ℓ(tⱼ) = err₁ + (err₂ − err₁)tⱼ/D, a convex combination, so |ℓ(tⱼ)| ≤ max|errᵢ| < δ. The bound is uniform in the number of gates. The check confirms it on 2,000 random gate lists of up to 40 gates.
- **Physical launch.** The physical transverse velocity is ±σ, with the sign set by the parity of the source lift's copy. The replay code uses exactly this rule.
- **Corners.** Middle-run corners lie on gate levels, at fold positions 0 or uⱼ. Strict windows exclude uⱼ. Position 0 is a smooth point only under the shared-smooth-side hypothesis. Endpoint runs have no interior corners between the mark level and the gate.
- **Floor corners (Ferrers).** A floor return aimed exactly at (0,0) or (W,0) still reaches T first. This is deep-terminal-band's stop-earlier argument, and the replay code implements it. No case needed it.

**Replays.** Each passing pair was traced with the smallest |k| solution.

| Room | Gates | Pairs | Test passes | Traced to T |
|---|---|---|---|---|
| S8 (W = 18, widths 1,2,4,6,8,10,12,16) | 7 = W/2 − 2 | 12 | 11 | 11/11 |
| U1, U2, U2b, T1 (direct or floor) | 3 | 218 | 205 | 205/205 |
| V1-761, V2-8051 (3 pairs), V3-5111 | 2 | 65 | 64 | 64/64 |
| 761 V=384, perpendicular chart | 2 | 1 | 1 | 1/1 (198 reflections) |

Every replay had all gate offsets below δ. S8 shows that the uniform bound holds with the maximum gate count for W ≤ 20.

## 2. Short relations and the rank-one test

**The Fourier bound is correct.**

- The kernel's coefficient is sinc(πmεᵢ/2)⁴ ≤ min(1, 2/(πεᵢ|mᵢ|))⁴.
- Surviving scaled frequencies are pairwise ≥ 2 apart in sup norm, because L is a group. That gives at most (2j+3)² points in shell j.
- The tail is at most 25/(6π²) = 0.422 < 1.
- Failure therefore requires a nonzero m ∈ L with |m₁| < 4w/δ and |m₂| < 4V/δ.

The check found 415 failures in 1,500 random rational instances. Each had such an m. The largest least value of max εᵢ|mᵢ| was 0.490. The 1-D example α = (1/7, 0) fails with t just below 1/2. So the note's constant 2 is sound, but up to 4 times larger than needed.

**The rank-one test is correct.** The orbit closure is the annihilator {x : m·x ∈ ℤ}. The image of the open rectangle under x ↦ m·x is the interval of half-width |m₁|ε₁ + |m₂|ε₂. The check compared it with float orbits (k ≤ 40,000) on 397 instances, with generators (3,0) and the non-primitive (2,2). All agreed.

**The ranks that occur.** With rational room data and rational marks, α is rational, so L always has rank 2. The L = 0 and rank-one clauses never apply to lattice pairs. The exact test is then a finite orbit check over N = lcm of the two denominators of α.

## 3. Named rooms

**Ferrers residuals.** Beam: the common left side, δ = w, A = B = 0.

- **The source phase is free.** ε₁ = 1/2 and θ₁ = ±x/(2w) with 0 < x < w, so one source sign always works (check 3b). The test becomes 1-D: with q = den(Pb/(2V)), the pair passes iff dist(z, (2V/q)ℤ) < w. That is the terminal-strip test at depth b.
- **Floor returns.** They replace b by 2h − b. The two rotations sum to Ph/V. When Ph/V is an integer (U1: 15, U2: 6), both rotations have the same denominator, and the floor adds nothing.

| Room | P | Ph/W | Direct only | Direct or floor | Exact failing lines |
|---|---|---|---|---|---|
| U1 | 30 | 15 | 75/88 | 75/88 | b ∈ (2/5)ℤ (7 lines), every z |
| U2 | 6 | 6 | 88/88 | 88/88 | b ∈ {4/3, 8/3}, every z; b ∈ (4/9)ℤ \ (4/3)ℤ with z ≥ 11/3 |
| U2b | 6 | 24/5 | 27/29 | 29/29 | none: one of the two rotations has denominator ≥ 5 |
| T1 | 24 | 24/13 | 13/13 | 13/13 | none: the direct denominator is in {1,3} only at b = 13/36 or 26/36, where the floor denominator is 39 |

The (A) floor-return shot of deep-terminal-band lights the U1 and U2 failing pairs exactly. Its gate offsets exceed w, so it is not in the note's uniform-δ family. So the note's test certifies U2b and T1 with the floor return, but not U1 or U2. The note doesn't claim otherwise: it credits U1 and U2 to (A).

**Pyramid.**

- In V1-761, V2-8051, and V3-5111, 64 of 65 marks pass, and all 64 replay. One V1-761 mark fails. d172 lit it by another one-middle shot.
- In the 761 V=384 room, the forward test fails as the note says: α = (−1, 1/6), N = 6, no solution. The cap rotation 1/2 also fails.
- The perpendicular chart, with beam y = 33, δ = 32, and P = 66, has 7,460 solutions out of 9,200. Its k = −1 shot traces T → S exactly. So the test certifies this pair, but only in the other orientation.

**R22, pair (0,0)–(2,2).** The vertical sweep is a zero-middle-band chain:

- Source run (−1,1), a = 1.
- One gate at y = 1, opening (0,1), with vertices at both ends. So δ = 1/2.
- Target run (0,4), b = 1.

With no middle band, P is free. For generic P, L = ℤ(1,2). For every lift, dist(m·θ, ℤ) = 1/4 = |m₁|ε₁ + |m₂|ε₂. The strict test fails at exact equality. Every single-pass developed line crosses y = 1 at an integer x, and the direct segment stops at the vertex (1,1). This agrees with darkness. The nearby control pair (0,0)–(2,19/10), with P = 1/7, passes and traces exactly.

## Gaps

1. **High: this doesn't reach "every W ≤ 20 room is lit".** Lattice data always gives rank 2, so the content is a finite orbit check. The relation box 4V/δ isn't bounded over a word's lengths. The Ferrers grid gives 1144k, and U1 fails on 7 lines in both itineraries. The note says so. The PROGRAM goal still needs a condition that every W ≤ 20 chain satisfies, and this note doesn't give one.
2. **High: no lower bound on δ, and beam existence isn't proved.** With a shared smooth side through every gate, δ is the narrowest gate opening, which is at least 1 for lattice rooms. Without a shared side, δ is set by physical overlaps, as in 761-perp (32) and R22 (1/2). Nothing shows that a crossing beam exists for every open pair in every W ≤ 20 chain. Nothing bounds V/δ.
3. **Medium: the uniform δ discards wider deep windows.** The exact admissible set of endpoint errors is the polygon {|e₁(1 − tⱼ/D) + e₂tⱼ/D| < δⱼ for all j}, which contains the δ-square. The (A) shot lies in this polygon and outside the square, and lights U1 and U2. Kronecker applies unchanged to a convex symmetric window. That version should replace the rectangle.
4. **Medium: caps and floors are only gestured at.** A return changes b to 2h − b, and the two rotations sum to Ph/V. A return helps only when Ph/V ∉ ℤ. For a full far wall, deep-terminal-band's stop-earlier argument removes the corner condition. For a partial wall, such as the 761 tooth, the cap isn't a mirror. Its clearance is a third phase condition, which the note leaves to "verify separately".
5. **Medium: with δ = w the torus test reduces to known work.** The source phase is free, and the test equals the d168/d170 terminal-strip test at depth b. The note's "(1,0) survives" remarks (pyramid, Ferrers grid) concern a harmless relation in that case.
6. **Low.** The constant 2 in the relation bound can be lowered. The tests saw least t ≤ 0.49, and rank one gives t ≤ 1/2.
7. **Low.** The zero-middle-band case, where P is free, should be stated explicitly. R22 shows that the strict inequality is exactly where darkness sits, so equality cases need a separate argument, such as deep-terminal-band's closed interval.

## 4. Assessment

- **Is it word-independent?** Yes, as a sufficient test. It holds for any monotone chain with any number of gates.
- **Is it a theorem that every W ≤ 20 chain satisfies?** No.
- **What it would need:**
  - a crossing beam for every open pair, with δ bounded below relative to V,
  - window polygons in place of the rectangle,
  - cap and floor phases with their own clearance,
  - a proof that the finitely many residual lines of one chart are lit by another chart or itinerary.
- **Status.** The 761 example shows that no single orientation suffices. No ledger status changes.
