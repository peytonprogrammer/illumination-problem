# D82: review of midpoint-necessity.md and d81

Date: 2026-11-20. Reviewer: independent referee.

## Verdicts

- **A. `qclass-closure/bbbb/midpoint-necessity.md`: sound as an algebraic lemma.** The downstream route that cites it is mis-stated. Condition (ii) must be algebraic, and darkness doesn't imply it.
- **B. `d81-lower-threshold/README.md`: sound with fixable gaps.** The group theory, the threshold table and N = 49 check out. Section 4's combination sentence is wrong and needs rewriting.

## The route, stated precisely

Let U be the marked union, d its valency, and a the class of S and T. Let R_other be the number of regular diagonal branches of U over the three other classes. Then:

- (ii-alg) means R_other = 0. This is what the budget uses.
- (ii-geo) means that no regular coincidence of U outside a is realized by a legal billiard path from S to T.

Darkness implies (ii-geo) trivially. It even rules out realized coincidences in class a. But (ii-geo) doesn't imply (ii-alg). R22's 6 class-a candidates are all unrealized because the pair is dark. cov4181's 7 class-d candidates are unrealized (D66).

So "dark ⇒ (i) and (ii) ⇒ r ≥ 9" fails as stated:

- With (ii-geo), the first arrow holds, but the second doesn't.
- With (ii-alg), the second arrow holds, but the first is unproved.

The correct proved statement is:

> For any strictly simple lattice room, 2d = R + J, J ≤ 2r, R_a ≤ ⌊n/2⌋. Hence if r ≤ 8 and d ≥ 2n/3, then R_other ≥ 2⌈2n/3⌉ − 16 − ⌊n/2⌋. This is ≥ 2 at n = 21 and ≥ 26 at n = 49.

With d81, a dark pair with r ≤ 8 and n ≥ 49 has at least 5n/6 − 16 algebraic candidates outside class a, and none is realized. Two things are missing:

- A bridge lemma: under these counts, some candidate is realized.
- Condition (i) for 21 ≤ n ≤ 48.

The later notes refute the specific tools for (ii-geo ⇒ lit):

- shortest.md: a single corner blocks candidates in two classes.
- midpoint-clearance.md: the distance test succeeds only for directly visible pairs.
- short-escape.md: candidates can't be charged to a class.

They don't refute the inequality or the route's conditional form. No named dark pair with r ≤ 8 has R_other > 0. DB55 has R_other = 72 and is lit.

## Findings

1. **Major, route statement.** RESULTS.md §11 says "(ii) no usable regular midpoint". The inequality needs (ii-alg). "Usable" suggests (ii-geo), which darkness gives free but which doesn't feed the inequality. Replace it with the algebraic wording, and record dark ⇒ (ii-alg) as the open bridge.
2. **Moderate, d81 §4.** The sentence "a counterexample with both of that note's features and r ≤ 8 has area 21 ≤ n ≤ 48" inverts the logic. Both features at n ≥ 21 force r ≥ 9, so no such counterexample exists there. The correct consequence: a dark r ≤ 8 pair at n ≥ 49 satisfies (i), so it fails (ii-alg). Pairs that fail (i) need 21 ≤ n ≤ 48 or n ≤ 20.
3. **Minor, A, thresholds.** With integer rounding (d ≥ ⌈2n/3⌉), (i) and (ii-alg) already force r ≥ 9 at n ≥ 19, not only at n ≥ 21. At n = 18 the bound gives only r ≥ 8.
4. **Minor, A, endpoints count.** S and T are themselves class-a coincidences. They account for 4 of R22's 6, through 2 lifts each. Class a is excluded, so the count isn't affected.
5. **Minor, B, product relation.** Prop P's κ = 2 bullet uses the product relation g₁g₂g₃g₄ = 1 to get at least two swap-type generators. That is a property of every cover of the 4-punctured sphere (D0). check.py's data check isn't the justification. Note also that exactly two are swap type, because g_x isn't.
6. **Note, B, swap-type reflex class.** The "z_y ≥ 2μ − 3" bullet and f + 3z = μ contradict each other directly. A swap-type generator can't carry reflex corners at all, so the next bullet is redundant but harmless.

## What was checked

**A.**

- Definitions: the bidegree (d, d) curve meets the (1,1) diagonal. The local branches y = ζx at e = 2, 3 have multiplicity one. These correspond exactly to g_p-cycles of pairs (s, g_p^k s).
- The midpoint argument: 2S + Lv ∈ 2Z², so the developments agree in the base for all t.
- The charge: each reflex corner is one degree-3 point of the double and gives at most 2 branches. Convex corners give 0. Interior lattice points give 2 regular lifts, and smooth-wall points give 1. Strict simplicity rules out degree ≥ 4. Every corner is a lattice point, so the internal grid lines add no case.
- The algebra: 4n/3 ≤ 2r + n/2 gives r ≥ 5n/12.

**B.**

- Corollary 2 of Burness–Guralnick, Adv. Math. 411 (2022), arXiv 2112.03967v2, read from the PDF. Statement: G is a finite primitive group and x ∈ G has prime order r. Then fpr(x) ≤ 1/√(r+1), or G ≤ S_μ ≀ S_κ contains A_μ^κ, with S_μ acting on ℓ-subsets in product action. Here u = g_x² has order 3, so fpr ≤ 1/2 and n ≤ 6z_x. The prime-order hypothesis holds.
- The product-action exclusion: the cases (κ, λ) = (1, 2), (2, 1), and κ ≥ 3 / λ ≥ 2. The μ = 7, n = 49 subcase of κ = 2 is ruled out correctly.
- T1: a section A_(m−2) of S_k × S_k forces m − 2 ≤ k. This gives m ≥ max(7, k + 3).
- T2: other class-x 3-cycles sit inside h_x-fixed blocks, because 2-cycle blocks give even lengths. The support meets at most 3 + z_x − k blocks. A 3-cycle in π(K_{D,E}) plus simplicity gives A_(m−2).
- Lemma B: (k, m) ∈ {(3,7), (3,8), (4,7)}.
- Every table row. The rows from 49 to 55 are empty: k = 4 has 48 and 52 only, and k = 8 has 48 and 56 only.

**Recomputed with my own code.** I didn't reuse the d78 step(). My code builds the monodromy from a quadrant walk on the double.

- R22: n = 15, r = 9, d = 12, R = 6 (all in class a, at (0,0)×2, (2,2)×2, (2,−2) and (4,0)), and J = 6 + 6 + 6 = 18. All 9 corners carry both branches, and 2d = 24.
- The d values for every pair in cov2493 (5 pairs, min 14 = 2n/3), cov3397 (10 pairs, min 6) and st279 (120 pairs, min 54) match d81's code exactly. My block computation gives (k, m) = (7, 3), (8, 3) and (2, 28).
- midpoint-orbits.py and check.py reproduce their saved output byte for byte, apart from the CPU time.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d82-review-necessity && python3 -B indep.py > indep.log` (0.1 s CPU). No search over rooms, rays, directions or words.
