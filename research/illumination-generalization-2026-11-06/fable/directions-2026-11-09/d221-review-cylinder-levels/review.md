# d221 referee review: cylinder levels and open saddle connections

Note: `note-snapshot.md`. Checks: `checks.py`, log in `checks.log`. The run takes 2.0 s of CPU at nice 10 and ends with 0 failures. It uses only cov446, cov4181, and R22, built through d72's `rooms()`. It runs no room enumeration, and no ray, direction, word, or room-size search. The only directions it uses are a fixed list of 8 slopes and the named rooms' own SL₂(ℤ) orbits. It makes no network calls.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | Exact criterion (I) or (II); Γ(2) with three representatives; finite marked orbit | CORRECT WITH GAPS (minor) |
| 2 | cov446 (1,2),(3,2): no (I) over the complete orbit, lit by (II) | CORRECT (recomputed exactly) |
| 3 | 4n−2r sites, M=4n−4r−4, E=4r+4, Σℓ=L, L−2r critical sites, pair-count formula | CORRECT (verified in 24 room-direction states) |
| 4 | cov4181 class-b type-(I) witness in direction (−3,8) | CORRECT; "reflected room" wording is wrong |
| 5 | Area 22 primitive branch: 2d=42, J=16, R=26, 26−tₐ ≥ 15 | CORRECT WITH GAPS (imported inputs) |
| 6 | Full-twist formula and CRT test | CORRECT WITH GAPS (convention, affine realization) |

Overclaim: none found. The note says plainly that the counts give no lower bound for the specified pair and that the twist test is only sufficient.

## 1. Exact criterion: CORRECT WITH GAPS

The proof is sound. A legal chord unfolds to a segment on X that avoids F. After straightening, it lies on the horizontal leaf through S̃, which is an integer level. A regular row's leaf is a closed circle in the interior of a cylinder of height ≥ 2. A critical row's leaf is cut at F, and a segment that avoids F stays inside one open saddle connection. The converse folds the circle arc or the subinterval. Folding preserves coordinate parity, because reflection in a lattice line sends x to 2L−x. So the parity bookkeeping is right: m is even for equal classes, an off-class midpoint needs m ≡ 2 (mod 4) and v ≡ x−a, and distinct classes need m odd with v ≡ b−a.

Checks:

- Γ(2) has three cusps, so it's transitive on unoriented primitive vectors of each parity class. Γ(2) shears reduce all 3,920 primitive vectors with |p|,|q| ≤ 40 to their class representative.
- The marked orbits close: 9,072 states (cov446), 2,592 (R22), and 3,888 (cov4181).
- On every orbit state, "joined horizontally without passing F" equals "(I) or (II)", and (I) implies a common open cylinder (assertions in `orbit_scan`).

Gaps (minor):

- "Compatible lifts" is never defined in one place. It means S on one fixed copy and T on any copy when all directions are allowed, and the sheet signs of the prescribed direction otherwise. The text states both pieces, but in different paragraphs.
- The remark that two distinct levels in one open cylinder give a slanted chord makes d72's CC sufficient for lighting. That's correct and worth saying outright, because it means CC sits strictly between (I) and lit.
- The Γ(2) paragraph isn't used by the criterion, which quantifies over the full SL₂(ℤ) orbit. It matters only for prescribed-class tests.

## 2. cov446: CORRECT

`orbit_scan` reruns the complete coloured orbit with all four S lifts coloured. It closes at 9,072 states, matching d72. There is no state with (I) and no state with a common open cylinder. Type (II) holds in 2,160 states. In the identity state, (1,2), (2,2), and (3,2) are interior, the row is critical, and (4,2) is a reflex corner. The proper-factor statement is cited from d72 (type 01 = proper(5)) and not rechecked.

## 3. Counts: CORRECT

The identities were checked in directions (1,0), (0,1), (±1,1), (2,1), (3,2), (−3,8), and (1,4), on cov4181, R22, and cov446:

- Sites: 4n−2r distinct sites, with exactly r triple sites (96, 42, and 46). |F| = 2r+4, and M = 4n−4r−4 (76, 20, and 28).
- Every cylinder has exactly one critical row, which is its bottom row. Σwh = 4n. There are E = 4r+4 saddle connections, and Σℓ = L.
- Regular sites split into 4n−L on circles and L−E on intervals. There are L−2r sites on critical rows.
- A brute-force count of unordered regular-site pairs in the same horizontal component equals Σ(h−1)C(w,2) + ΣC(ℓ−1,2) in all 24 states. For example, cov4181 at (−3,8) has L = 96 and 208 pairs.

The arithmetic for n=22 and r=8 is right: 72 sites, 20 forbidden lifts, 52 regular sites, and 36 ≤ L ≤ 88. The many states with L = 4n (no regular circle at all, for example cov4181 at (1,1)) show that the note is right to claim no positive lower bound on 4n−L. The shear remark is also correct. T keeps every horizontal leaf, so it can't move a mark to another level.

## 4. cov4181 witness: CORRECT

`vertex_step` from (2,3) with velocity (−3,8) on the **d66 cell rows as given** reproduces the nine positions and nine sign pairs exactly:

- All listed sites are regular.
- The ray reaches T = (4,3) at step 4 with the starting signs, and S at step 8 with the starting velocity.
- gcd(3,8) = 1, so no internal crossing is a grid vertex.

The origami state for word(−3,8) puts S̃ and T̃ (sheet (1,1)) on one regular row of length 8. That row is inside a cylinder with (w,h) = (8,2). The midpoint (4,1) is in the source class. The class-b horizontal chord through (3,3) is on a critical leaf that ends at the reflex corner (6,3).

Gap (wording): "on the reflected room" is wrong. No reflection is needed. Mirroring the cells in x or y gives a different trace, which `checks.log` shows. Delete the word "reflected".

## 5. Area-22 counts: CORRECT WITH GAPS

Given G ∈ {A₂₂, S₂₂} (d220), G is 2-transitive, so U is all ordered distinct pairs and d = 21. Each reflex is one 3-cycle with two non-diagonal germs, so J = 16. Then R = 42−16 = 26, which also equals 2n−2−2r, the number of 2-cycles by Riemann–Hurwitz. tₐ ≤ 11 gives 26−tₐ ≥ 15. As a consistency control, the cov4181 tuple has 8 three-cycles and 38 two-cycles (= 2n−2−2r). The 2-cycles also double to M = 76 on X, which matches the note's Q-versus-X distinction (2·26 = 52 at n=22).

Gaps: the inputs are imported. These are d220's group verdict (CFSG-based), the identity 2d = R+J from midpoint-necessity, and the local degrees 1, 2, and 3. They weren't re-derived here. The bound tₐ ≤ ⌊n/2⌋ is crude but sufficient.

## 6. Twist formula and CRT test: CORRECT WITH GAPS

The tuple is (V₀H₀, H₀V₁, V₁H₁, H₁V₀) at poles (0,0), (1,0), (1,1), (0,1), composed right to left. Its product is 1.

- **Twist formula.** For each of the three adjacent pairs, j applications of σ² (σ:(g,h) ↦ (h, h⁻¹gh)) give k⁻ʲgk ʲ on both entries, for every j ≤ 2·ord k. The other entries and the product stay fixed.
- **CRT test.** For S = (2,3), T = (4,3), all 16 incidence-sheet pairs, and every admissible (x,y), the CRT test agrees with a brute-force check over all j < ord k (0 mismatches).
- **Control.** At the d-dark class (pole (0,0)), no incidence pair passes, which is consistent with d66. At class b (pole (1,1)), 2 of 16 pass, which matches the known horizontal witness.

The equivalence "two traversals ⇔ (s t) is a 2-cycle of gₓ" is right, because the only legal straight passage through a pole preimage is at a 2-cycle point.

Gaps:

- **Convention.** The family {k⁻ʲgₓkʲ} depends on the composition order. Under left-to-right composition, the analogous family equals gₓ⁻¹(family)gₓ, which has different 2-cycles. The test is valid only when k = gₓg_y, the tuple, and the incidence sheets use one convention. The note defers to "the Hurwitz convention of the monodromy note" but doesn't fix the composition order.
- **Affine realization.** The note asserts that the full twist is geometric. This is true because a Dehn twist about a curve enclosing two poles is a parabolic in the affine group, but the note gives no argument. The note correctly says that the tested arc changes.

## Lemma advanced and first open case

**Lemma advanced: L1, as a reformulation.** The exact lit test now includes open saddle connections, and cov446 shows that this addition is necessary under the all-direction quantifier. The count identity and the CRT test are exact, but neither gives a positive lower bound for a specified pair. No bound on W moves.

**First open case.** At area 22 on the primitive branch (G ∈ {A₂₂, S₂₂}, r = 8), take a nondirect same-parity interior pair in a positive normalized BBBB chart. Show that one marked orbit state puts compatible lifts on the same interior cylinder level (I) or the same open saddle connection (II). The CRT twist test is a sufficient two-traversal route. The off-class midpoint form also needs m ≡ 2 (mod 4). The imprimitive degree-20 branch remains a separate obligation.
