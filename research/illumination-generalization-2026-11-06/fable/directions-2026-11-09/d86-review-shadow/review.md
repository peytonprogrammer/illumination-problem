# D86: review of shadow-budget.md (snapshot)

Date: 2026-11-20. Reviewer: independent referee. Reviewed file: `shadow-budget.snapshot.md`, SHA-256 `74722ed2…5f968d` (checked before review).

## Verdicts

| Claim | Verdict | Reason |
| --- | --- | --- |
| 1. Proposition B(r) | Sound with fixable gaps | Closedness, invariance, LMW and the quasi-finite step hold. "Finite union" needs EMM's closed-invariant-set theorem, which the note doesn't name. |
| 2. Genus lemma | Sound | Riemann–Hurwitz, fixed points, R = 2d − J and k ≤ 16 all check. The DB55 bound g ≥ 47 is correct but weak: the archive records genus 197. |
| 3. cov4181 control | Sound | Replayed exactly. m = (4,2) is visible from S and from T; its two coincidence lifts are unrealized. The Q/U distinction is stated correctly. |
| 4. What would suffice | Sound | Both inequalities check. The budget it asks for is a quantitative restatement of the open bridge lemma, not a reduction of it. |

## 1. Proposition (uniform downstairs bound)

**Setting.** M has genus r + 1, r order-two zeros and r + 4 regular forbidden marks, so the stratum is H(2^r, 0^(r+4)) with two more labeled points x, y. Hidden Q targets inject into hidden M points from a fixed source lift, because distinct Q points have disjoint lift sets and legal M segments project to legal Q paths. This step holds.

**Closedness.** The complement of D is open. A legal segment from x to y is a compact path whose interior avoids a finite set: the zeros, the forbidden marks and, if required, x and y. It keeps a positive distance from that set, and it persists under small changes of period coordinates and endpoints. Forbidden convex marks and reflex lifts both sit in that finite set, so neither breaks openness. D is closed in the stratum, which is what is needed. It is not closed in any compactification, and nothing requires that.

**Invariance.** GL⁺(2,R) maps straight segments to straight segments and preserves every label. D is invariant.

**The finite-union step: the gap.** The note says "By Eskin–Mirzakhani–Mohammadi it is a finite union of affine invariant submanifolds." The orbit-closure theorem alone doesn't give this. A closed invariant set is a union of orbit closures. EMM also give only countably many affine invariant submanifolds. Countability plus closedness still doesn't force finiteness: Z ⊂ C is closed and a countable union of subvarieties. Noetherian induction over the countable family fails for the same reason.

The missing input is EMM's limit theorem. For a sequence of affine invariant submanifolds N_i, some subsequence lies eventually inside one affine invariant N, with N in the closure of their union. Apply it to the inclusion-maximal members of D. If there were infinitely many, some N would contain infinitely many of them and lie in D, which contradicts maximality. From memory, EMM state the consequence directly: any closed SL(2,R)-invariant subset of H_1(α) is a finite union of affine invariant manifolds (Theorem 2.3 in arXiv 1305.3015, I believe). I couldn't check the numbering offline. Intersect D with the area-one locus to apply it. **Fix:** cite that theorem by number, or give the two-line maximal-element argument above.

**Marked points.** EMM and Filip are routinely applied to strata with order-zero marked points. The note cites a GT 2020 paper for this. From memory, I accept this as standard. A precise statement for Filip's algebraicity with several marked points would still be better.

**LMW.** As I recall LMW's conventions, marked points count as obstacles. That is exactly what their billiard application needs, because polygon vertices with regular unfoldings must block. Keeping the convex lifts as forbidden order-zero marks is therefore within their theorem. The fiber of forget-y over a point of the base is the set of y hidden from x, which is finite.

**Uniformity.** D is a finite union of algebraic subvarieties, and forget-y is a morphism of finite type. With LMW, it is quasi-finite. For such a morphism the number of geometric points per fiber is constructible, hence bounded (EGA IV 9.7.9, or the stratification argument in the note). Strata have finitely many components. This step holds.

**Conclusion.** A correct proof is available. It uses EMM's closed-invariant-set theorem, which is the finite-union statement. Pure Noetherian induction over the countable family doesn't suffice. The constant B(r) is non-effective, as the note says.

## 2. Genus lemma

- At a regular coincidence, f = x² in a common coordinate, so the off-diagonal germ is y = −x. Swap maps (t, −t) to (−t, t) on the same germ. So the component is swap-invariant and the point is fixed.
- Swap isn't the identity on an off-diagonal component, so its fixed points are isolated.
- Riemann–Hurwitz for an involution: 2g − 2 = 2(2h − 2) + F, so F = 2g + 2 − 4h and g ≥ F/2 − 1. This is correct.
- Each regular coincidence is a distinct point of the normalization, at most one per Q point. Reflex germs y = ωx and y = ω²x are swapped, not fixed, so they aren't counted. F ≥ R_C, and summing gives Σg ≥ R/2 − k.
- R = 2d − J with J ≤ 2r matches d82 ("2d = R + J, J ≤ 2r"). So R/2 ≥ d − r.
- k ≤ 16: U is generated by 4 × 4 incident sheet pairs.
- DB55, n = 53: midpoint-orbits.txt gives d = 52, (24, 2) in each class, so R = 96 and J = 8. That gives g ≥ 47, and also d − r − k = 52 − 4 − 1 = 47. The same file records the actual genus as **197**, so the note could quote that.
- Stretches 451 + 80j: midpoint-clearance.md gives area 501 + 80j, r = 4, gcd 1 on each axis, and a nondirect same-parity pair. d81 (and d78 for n ≥ 120) gives d ≥ 2n/3. So Σg ≥ 2n/3 − 20, and the largest component genus is at least that over 16. It is unbounded at r = 4. The pair is lit, so this shows genus growth, not hidden-set growth. The note says exactly that.

## 3. cov4181 control

- `shortest.py` replay: the output is byte-identical to `shortest.txt` ([shortest-replay.log](shortest-replay.log), 0.4 s). Records 8 and 68 are the two class-(0,0) coincidences at physical (4,2).
- Independent exact check ([cov4181_control.py](cov4181_control.py), [log](cov4181_control.log)):
  - S, T and m are interior (status 4).
  - The chord S→m has D = (2, −1) and gcd 1. It crosses x = 3 at y = 5/2 between cells (2,2) and (3,2), both in the room. It is legal.
  - The chord T→m is the unit segment on x = 4 between cells (3,2) and (4,2). It is legal.
  - The legs have lengths √5 and 1 and meet at an angle, so they aren't the two halves of one straight S→T shot.
- Bounded sanity check of D66: no legal S→T path with |D| ≤ 40 has its midpoint in parity (0,0). There are 31 paths in parity (0,1) and 55 in parity (1,1), the shortest being the direct (2,0). This doesn't prove D66, which is exhaustive.
- The logic is correct. Hidden on Q means no legal path from a source lift to m. Unreachable on U means no legal S→T shot with midpoint m. Darkness gives the second, never the first. The R22 bullet agrees with d85: (4,0) is reached; (2,2) and (2,−2) stay hidden.
- The correction to d85's summary is right. The d85 table shows |H| = 2 at L = 25 for U2 k = 0, S = (6,6), but the summary says the only nonzero counts at 2·diam are R22 and R22-L1-005.

## 4. What would suffice

- For n ≥ 49 and r ≤ 8: R_other ≥ 2⌈2n/3⌉ − 16 − ⌊n/2⌋ ≥ 5n/6 − 16 (26 at n = 49). With R_other ≤ αn + K, this gives n ≤ (16 + K)/(5/6 − α). The arithmetic is correct.
- For n ≥ 120, d78 gives d ≥ n − 8, so R_other ≥ 2(n − 8) − 16 − ⌊n/2⌋ = 2n − 32 − ⌊n/2⌋ ≥ 3n/2 − 32. Any slope α < 3/2 gives n ≤ max(119, (32 + K)/(3/2 − α)). The arithmetic is correct. The range 49–119 stays a finite census under that weaker slope.
- **Caveat.** For a dark pair, H_sync = R_other by definition. So the required estimate is exactly "dark ⇒ R_other ≤ αn + K". That is a quantitative form of the open bridge lemma (dark ⇒ ii-alg, approximately). The section is correct, but it restates the gap rather than reducing it. The affine-stabilizer bridge in the next paragraph is logically sound as stated, and it is also unproved.

## Decision paragraph

Accurate. The ordinary budget exists non-effectively once the EMM citation is fixed. The synchronized budget is open. Ordinary shadows give no census cutoff without a transfer theorem.

## Re-run

```
cd d86-review-shadow
python3 -B ../../../../qclass-closure/bbbb/shortest.py | diff - ../../../../qclass-closure/bbbb/shortest.txt
python3 -B cov4181_control.py
```

Total CPU under 1 s. Named room only, exact arithmetic. EMM, Filip and LMW statements are cited from memory; no web access.
