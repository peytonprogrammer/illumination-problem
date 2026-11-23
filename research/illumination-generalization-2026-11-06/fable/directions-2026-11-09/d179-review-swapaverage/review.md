# d179: review of l1-swap-pole-averaging.md

Note: `../d95-review-queue/snapshots/1650/l1-swap-pole-averaging.md`.
Checks: `checks.py`, log in `checks.log` (`python3 -B checks.py`, 0.01 CPU-seconds). The script loads d146's `Double` model the same way d178 does. It uses one named room (DB55 stretch, p = 53), 8 named primitive directions, 2 named mark pairs and 4 named straightening instances. It runs no room, ray, direction or word search. Source check: arXiv 1003.5887 (Marchese), pages 3–6.

## Bottom line

**The note is correct. It doesn't move L1, and its proposed next statement is not weaker than the open reachability lemma.**

- The counting lemma, the 24/1378 figure, the zero-cross-edge example and the straightening lemma all check. No step has a gap that breaks a claim.
- The straightening lemma has almost no leverage. By Hurwitz's theorem, every irrational launch direction already passes within 1/(√5|v|) of infinitely many primitive lattice points v. So the reciprocal-scale, primitive-address conditions hold automatically, infinitely often, on every ray. The only open condition is which Y-point over the site the ray is near. The note's "sufficient next statement" therefore says that some primitive chord from a marked start ends at a swap pole. That's the first-step form of the reachability lemma itself.
- The Marchese descriptions are accurate. They omit 2 limits that strengthen the note's own conclusion (see Low 5).
- "No N₀ follows" is correct.

## Verified items

1. **Counting lemma (check 1).** DB55 p = 53 has n = 53, N = 1378, and q_x = 24 at each of the 4 sites. So 24/1378 = 0.01742 ≤ 1/(n−1) = 0.01923. The script transports all 53 front labels along each named primitive segment. The directions are (1,0), (0,1), (1,1), (1,2), (2,1), (1,−1), (−1,2) and (3,2). It starts from each of the 4 sites, for 32 cases. It then checks all 1378 unordered pairs by brute force.
   - In all 32 cases exactly 24 pairs end at a swap pole, and they form a matching.
   - That matching equals the pullback of the 24 two-cycles of g_b.
   - Transport is a bijection, and reversing a segment gives the inverse transport, checked for (1,2) and (3,2).
   - The argument is also correct in general. Transport in the open arc is a bijection, and a pair ends at a swap pole exactly when its terminal labels are the 2 sheets of one 2-cycle Q-point. The open primitive segment has no lattice point, so neither projection meets a corner. The axis directions run along a pillowcase edge and need the edge-label convention used in the script, but the count is the same.
   - The marked set is right too. For one developed launch direction, the 8 starts (2 copies of S, 2 of T, 2 orbits) give 16 germs. They are exactly the 4 × 4 pairs of S-sheets and T-sheets. That's the "two disjoint four-letter sets" of the example.
2. **Zero-cross-edge example (check 2).** The logical point is correct. Edge-hit probabilities sum to q_b, but nothing forces mass onto the 16 specified cross edges. Within-set matchings have zero cross mass, and averages keep it zero. The script shows this for an abstract 8-letter example. On DB55 the 8 named directions give 0 cross S–T edges for both named pairs, S = (2,2) with T = (10,2) and S = (2,2) with T = (12,4). The only within-set edges are (51,52) at (1,0) and (47,52) at (0,1), both inside T = (12,4). The baseline expectation is about 16 · 24/1378 ≈ 0.28 cross edges per direction, so these zeros are not evidence of darkness. The note rightly limits the example to the mass identity. It blocks any proof that uses only the marginal count. It doesn't block a proof that uses the distribution of transports, which the note names as missing.
3. **Straightening lemma (check 3).** Each step holds.
   - *Determinant bound.* For u = αy + βv in the triangle, det(v,u) = α·det(v,y−v), so |det(v,u)| ≤ |v||y−v| < |v|ε < 1. ✓
   - *Lattice points.* An integral u has det(v,u) ∈ ℤ, so det(v,u) = 0. In the nondegenerate case the triangle meets that line only in the edge [0,v], and primitivity leaves only 0 and v. The vertex y isn't a lattice point. ✓
   - *Lifting.* All branch values and forbidden points of Y lie over lattice sites. So the developing map sends T∖{0,v} into the pillowcase minus its 4 corners. That set is contractible, the cover is trivial over it, and the lift through the broken path is unique. The limits at the 2 vertices are the same start Y-point and the same terminal Y-point. No branch point lies in the triangle. ✓
   - *Labels.* Y-points are preserved, but individual terminal labels can change. Instance 1, with v = (2,1) and y = (2.1, 1.15), has y past v. The chord and the broken path then arrive at v from opposite quadrants. Their terminal front labels differ by g_b, but every sheet keeps its Q-point and every pair keeps its Y-point. Instances 2 and 3 arrive from the same quadrant and agree label for label. ✓
   - *Necessity of the hypothesis.* Instance 4 has v = (2,1), y = (1.7, 1.8) and |v||y−v| = 1.91. Its triangle contains (1,1), and the broken path and chord end at different Q-points and Y-points.
   - *Collinear case.* It's correct. The radius-1 cone discs around distinct Y-points over one site are disjoint, because the radius-1 disc around a pillowcase corner is embedded. So "the pole" near y is unique, and a clean segment through v passes through that same Y-point. The note uses this fact without stating it.
4. **Other claims.** "Exact visits have rational developed direction, a measure-zero set" is correct. The 96 swap and 4 false poles match d178. q_b/N ≤ 1/(n−1) holds because q_b ≤ n/2.
5. **Marchese, arXiv 1003.5887.** Theorem 1.1(2): if ∫ϕ = ∞, then for almost every framed X̂ in the framed stratum, every bundle Hol^(p_j,p_i,m,l) has infinitely many solutions of |Re v| < ϕ(|v|). The note's "prescribed endpoint bundles for almost every framed surface" is accurate. A fixed arithmetic surface is a measure-zero set, so the theorem doesn't specialize to it. Theorem 1.6: for every flat torus with r punctures and almost every θ, at least 2r − 1 pairs (p_j,p_i) have infinitely many solutions. The note's "every flat torus, some endpoint pairs, not specified" is accurate.

## Gaps

### High

None.

### Medium

1. **The proposed next statement is the original problem.** The note says ordinary equidistribution "neither enforces the reciprocal scale nor specifies the lift." The reciprocal scale doesn't need enforcing. For an irrational slope α, Hurwitz gives infinitely many reduced p/q with |α − p/q| < 1/(√5 q²). The point v = (q,p) is then primitive, lies ahead on the ray, and is at distance less than (1+o(1))/(√5|v|) < 1/|v| from it. The ray never meets a lattice point, so [0,y] is clean, and the triangle argument applies. So every irrational ray from a marked start makes infinitely many reciprocal-scale, primitive-address near approaches to some Y-point over some site. The note's trichotomy for a hidden pair loses 2 of its 3 branches on these approximants. What's left is that every such Y-point is a non-swap point. Conversely, a primitive chord ending at a swap pole gives a positive-measure set of nearby near-approach directions. So "a clean reciprocal-scale near return with primitive address to a swap pole" is equivalent to "some primitive chord from a marked start ends at a swap pole." That's the first-step form of the reachability lemma, not a weaker target. The note should say this and drop the scale condition as a separate obstacle.
2. **The lemma's hypotheses are partly redundant.** The radius-1 disc is embedded, so ε < 1/2 isn't needed; |v|ε < 1 gives ε < 1. The clean hypothesis on [0,y] follows from the determinant bound. Stating the lemma with only primitivity and |v||y−v| < 1 would make item 1 visible.

### Low

3. **"Retaining … terminal sector at v" is inaccurate.** The chord can arrive in the opposite quadrant (instance 1). The terminal Y-point and Q-point are preserved, which is all the conclusion needs. The wording should say terminal point, not terminal sector.
4. **"The counting obstruction persists as q_b/N tends to zero" overstates.** The small ratio obstructs only arguments that use one arc's count, or the marginal over arcs. Infinitely many primitive arcs leave each start, and the heuristic expected number of M-hits diverges. The ratio is no evidence that a marked pair stays dark.
5. **2 Marchese limits are missing, and both support the note.** First, both theorems are about translation surfaces (abelian differentials). Y covers the pillowcase and is in general a half-translation surface, so it sits outside the stated strata unless you pass to its orientation double cover. Second, Theorem 1.6 holds for almost every direction θ, not for a fixed direction. Marchese's remark after Theorem 1.6 shows the pillowcase's own torus double cover, ℂ/(2ℤ)² punctured at ℤ²/(2ℤ)². There every Hol(p_i,p_i) is empty, so prescribed pairs fail on exactly this arithmetic surface. Citing that remark would make the note's point directly.
6. **The header overstates.** "Advances: L1" labels a correct but negative note: one averaging route fails, and one restatement of the reachability lemma is added. As in d178.

## What this means for L1

- The natural-action BBBB branch is where d178 left it. A same-parity lattice pair is lit if and only if some clean segment from one of the 8 starts reaches a swap pole. No mechanism yet produces one.
- Counting and averaging over primitive arcs can't close it. A single arc delivers q_b ≤ n/2 swap edges, but nothing places them on the 16 marked cross edges. On DB55 p = 53 the 8 named directions place none there for 2 named pairs, which is the expected low rate, not a sign of darkness.
- Near-approach and shrinking-target language adds nothing. Diophantine approximation gives reciprocal-scale primitive approaches on every ray for free. The open content is the sheet label at the approximants, that is, how transports along primitive chords from a fixed start distribute in G. A real step would be a statement about that distribution. One example is that the transports to approximants of one ray, or of a cone of rays, are not confined to a coset avoiding the marked cross edges.
- No ledger word moves, and no area bound or N₀ changes. The first open L1 case is still the marked primitive natural-action BBBB branch beyond the area-20 census.
