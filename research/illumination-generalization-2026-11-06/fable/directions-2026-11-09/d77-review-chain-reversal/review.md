# D77: Referee review of the chain criteria and the reversal extension

Date: 2026-11-19. Targets: `.context/qclass-closure/bbbb/chain-criteria.md` and `reversal.md`.
Own code: `verify.py`, log `verify.log`. The script uses its own exact `Fraction` polygon tracer
with maximal walls, so a contact at a wall endpoint counts as a corner hit. It reads only
`d64-finite-case/data/covers.json` (cov2929 cells) and `d72-cylinder-test/cyl_H40.json` (saved
directions). Every traced path comes from the construction stated in the reviewed proofs. There's no
search over rooms, rays, directions, or reflection words. CPU: 2.2 s per run, under 15 s in total.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d77-review-chain-reversal && python3 -B verify.py > verify.log`

## Verdict

- **chain-criteria.md: sound, with minor fixable presentation gaps.** The DBw2 theorem holds at
  ℓ = 11, 12, 13, 17, and 25 for every pair of distinct interior lattice points: 6,851 pairs, 0 failures.
- **reversal.md: sound, with minor fixable presentation gaps.** The DB55 interval, the ℓ > 5
  threshold, and both cov2929 contact lists reproduce exactly.

No fatal finding.

## 1. Width test (a) and the signed extension

- **Lattice.** Substituting s into y_i gives
  y_i = S + A_i(T−S)/X + Σ_j m_j P_j(A_i/X − 1_{j≤i}). So G is correct, and the endpoints enter
  only through the translate.
- **Full row rank.** With real indices, choose s freely and then m_i from each prescribed rise.
  The last index absorbs the remainder. So G maps ℝⁿ onto ℝᵏ, and every projected lattice Λ_i has
  rank i.
- **Induction.** det Λ_i is the gcd of the i×i minors of the first i rows (Smith form). The fiber
  of Λ_i → Λ_{i−1} is t·e_i with t = det Λ_i / det Λ_{i−1} = h_i/h_{i−1}, by the index product
  formula. The fiber over a placed prefix is a coset of that progression, so a strictly wider open
  window always contains a point. Correct for any seam order.
- **Instance check.** I checked one DBw2 instance (ℓ=11, travels 4, 11, 3), with D = 9. The direct
  first-coordinate gcd is 2 = h₁. The direct kernel step over |m| ≤ 40 is 54 = h₂/h₁. The spacings
  are 2/9 and 6.
- **Signed extension.** E_{j,e}(y) = l_j + e(y − l_j) is the correct image map: images y + Pk carry
  velocity sign(s), and images 2l − y + Pk carry the opposite sign. With z_i = e_i y_i, the bottom
  terms l_j(e_{j−1} − e_j) are constants, so the generators are the same G. The windows e_i·I_i keep
  their widths. At a crossing, the shared e_i makes the vertical velocities agree. At a turn, the
  horizontal velocity flips and the developed slope continues. Open windows exclude wall endpoints,
  and folding happens only inside full runs, so no corner contact or escape occurs.

## 2. Three-column test (b) and the length test

- **Iff.** With x = S + as − Pm and y = T − bs + Rn, you get bx + ay = bS + aT − bPm + aRn, which is
  the lattice gℤ. The converse recovers s and the signs. The open set {bx + ay : x ∈ I, y ∈ J} has
  half-width (bu+av)/2, which gives 2e < bu + av exactly.
- **Erosion.** Eroded widths are u − aδ′ and v − bδ′. The congruence still has a solution when
  2e < bu + av − 2abδ′, which is the third term of δ. The closed slope interval of width δ′ around
  the center keeps x and y strictly inside. F has slope a + ℓ + b, and the inequality must be
  strict because δ is not attained. Using g in place of 2e is valid because e ≤ g/2.
- **Constructive replay.** My code builds the center point, the Bézout indices, and the matching
  slope for each pair, then traces it. See section 3.

## 3. DBw2 (independent, all pairs)

- **Table.** It reproduces exactly, and max(4/δ − a − b) = 10 at (a, b) = (2, 4).
- **Interior points.** The family has 16 left, 20 right, and ℓ+1 points on y = 2 from x = 5 to
  x = 5+ℓ, including both mouths. Each of those points has four cells around it. At ℓ = 4 the
  same-class count is 190, which matches D72's 190. **The center line y = 2 is included.**

| ℓ | Points | Pairs | L–R (three-column) | Chamber–corridor | Direct | Failures | Max reflections |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11 | 48 | 1128 | 320 | 396 | 412 | 0 | 174 |
| 12 | 49 | 1176 | 320 | 432 | 424 | 0 | 188 |
| 13 | 50 | 1225 | 320 | 468 | 437 | 0 | 202 |
| 17 | 54 | 1431 | 320 | 612 | 499 | 0 | 256 |
| 25 | 62 | 1891 | 320 | 900 | 671 | 0 | 364 |

"Direct" covers same-chamber pairs, corridor pairs, and mouth pairs with c = 0.

**Short lengths (proof coverage only, not truth).**

| ℓ | g-test failures | Exact-e failures |
|---|---:|---:|
| 10 | 20 pairs, all (a, b) = (2, 4) | 4 |
| 9 | 20 | 4 |
| 8 | 60 | 18 |
| 5 | 140 | 40 |

At ℓ = 10, the 4 exact-e failures include (3,1)–(19,2). So **ℓ = 10 fails the proof**, even with
exact heights. Whether those pairs are lit was not checked.

**BBBB claim.** The room has 12 walls and r = 4. Its horizontal edge lengths are {5, ℓ}, which are
normalized iff 5 ∤ ℓ. Its vertical edge lengths are {5, 1, 2, 3, 6}, with gcd 1. Its area is
55 + 2ℓ, which exceeds 4r+4 = 20 (no Q class) and 8r = 32 (no proper factor). So the claim
follows from D69/D70's cited bounds. I didn't re-review those cited bounds.

## 4. DB55 reversal

- **Re-derivation.** 1 + 4s₀ = −35/2 ≡ 5/2 (mod 10), and 1 − 9s₀ = 341/8 ≡ 21/8. The window
  4t ∈ (−1/2, 1/2) intersected with −9t ∈ (−5/8, 3/8) gives t ∈ (−1/24, 5/72), with width 1/9.
- **Mirror.** The mirror height is 39/2 − 4t ∈ [173/9, 59/3], which lies inside (15, 20).
- **Placement.** The ℓ = 3 placement is −14, and the threshold is (13+ℓ)/9 > 2.
- **ℓ = 3 witness.** It reproduces the table: contacts 4 + 14 + 5 + 3 = 26 horizontal, the mirror
  at y = 1/2, and the corridor exit at 21/8.
- **Traced lengths.** These all reach (6+ℓ, 1) with exactly one vertical contact, strictly inside
  x = 10+ℓ:

| ℓ | Slope s | Mirror contact y |
|---|---|---|
| 11/2 | −172/37 | 15/37 |
| 6 | −88/19 | 9/19 |
| 63/10 | −880/193 | 147/193 |
| 7 | −23/5 | 3/5 |
| 20 | −152/33 | 19/33 |
| 51/10 | −840/181 | 79/181 |

At ℓ = 5 the open phase image is (−24, −22), which contains no even integer. This branch fails
there, so the strict inequality is sharp.

## 5. cov2929

- **Cells.** The cells from covers.json match D69's diagram. The room has 20 walls.
- **Path (3,1) → (5,3), V = (−2, 3).** Contacts are (2, 5/2), (3, 4), and (13/3, 2). The first is
  on wall x = 2, y ∈ (2, 4), strictly inside.
- **Path (3,3) → (5,5), V = (2, 3).** Contacts are (11/3, 4), (5, 2), and (6, 7/2). The last is on
  wall x = 6, y ∈ (2, 4), strictly inside. The contact (5, 2) is a smooth lattice point inside the
  wall y = 2, x ∈ (4, 6).
- **Saved directions.** Both match D72's saved directions. The midpoint residue argument
  (2y ≡ 0, 2, 4 mod 8) also checks by hand.

## Findings

1. **Minor, fixable.** In chain-criteria (a), "the projected integer lattice" should name DGℤⁿ
   restricted to the first i coordinates. It should also state that the rank-i fact from the
   real-index argument is what makes det Λ_i = h_i and the fiber rank 1.
2. **Minor, fixable.** reversal.md's width test should say that at a turn, runs j and j+1 are the
   same physical run, with the same l and P. It should also say that the turn window must face that
   run. Both are implicit now.
3. **Informational.** DBw2's ℓ > 10 is the proof's exact boundary. The exact-e variant leaves only 4
   uncovered pairs at ℓ = 9 and 10, so one sentence could extend the stated coverage.
4. **Informational.** The BBBB membership rests on cited bounds (D68, D63/D66). The text could quote
   the r = 4 thresholds (20 and 32) instead of 64.
5. **Not independently tested.** I checked the shrinking-last-travel test (c) by hand only, and found
   no gap. Clearances, L-periodicity, and the gcd of rationals all hold.
