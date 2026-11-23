# D140: review of half-turn-fibers (snapshot 2026-11-22-0020)

Date: 2026-11-21. Reviewer: adversarial referee. Reviewed file: `../d95-review-queue/snapshots/half-turn-fibers.2026-11-22-0020.md`, SHA-256 prefix `cb4ce8ecb91b90d8`, unchanged before and after review.

**Verdict: sound with gaps.** The theorem holds as stated for abstract marked square-tiled surfaces. Every computation reproduces. None of the gaps breaks the result. Two gaps change how the result should be read for rooms.

Files: [checks.py](checks.py), [checks.log](checks.log). Re-run: `python3 -B checks.py > checks.log`, about 5 CPU-seconds. The checks use exact integer arithmetic, named examples only, and no searches.

## 1. The midpoint argument

Each step checks.

- **Uniqueness.** A straight segment on a translation surface is determined by its start point and velocity until it reaches a cone point. The only cone point is the double zero, and it's forbidden, so every legal segment avoids it.
- **Half-turn.** In genus 2, ι acts by −1 on H⁰(K), so ι\*ω = −ω and the derivative is −I in every chart. The construction confirms this. σ(i) = 1 − i mod p is the unique square permutation with σhσ⁻¹ = h⁻¹ and σvσ⁻¹ = v⁻¹. It is an involution.
- **Fixed points.** ι has exactly 6 fixed points: C((p+1)/2), R(0), T(0), T(1), T((p+1)/2), and the zero. By Riemann–Hurwitz, the quotient has genus 0, so ι is the hyperelliptic involution. Its fixed points are the 6 Weierstrass points. Here C is a square centre, R a right-edge midpoint, and T a top-edge midpoint.
- **Reversal.** Let γ be a segment from x to y = ιx with velocity u. Then t ↦ ι(γ(L − t)) starts at x with velocity (−I)(−u) = u. So it equals γ, and γ(L/2) is fixed by ι.
- **Other forbidden points and multiple segments.** The argument applies to each segment separately and uses only the midpoint. Other forbidden points along a segment don't matter. The check confirms the mechanism. Every enumerated segment from x to y has a forbidden midpoint, and no segment is legal.

## 2. Degree-p examples, p = 7 and 11 (checks.log, Part A)

The permutation pair is h = (0 1 … p−1) and v = (0 1).

| Check | p = 7 | p = 11 |
| --- | --- | --- |
| Connected, genus | yes, 2 | yes, 2 |
| Vertex cone angles (units of 2π) | 3,1,1,1,1 | 3,1×8 |
| Commutator v⁻¹h⁻¹vh | one 3-cycle | one 3-cycle |
| h^k v h^−k = (k k+1) for all k, so the group is S_p | yes | yes |
| Index of the absolute period lattice in ℤ² | 1 | 1 |
| ι-fixed points | 6 | 6 |
| Search bound max(\|a\|,\|b\|) | 60 | 50 |
| Segments enumerated per source | 14,640 | 10,200 |
| Segments that reach y | 2,310–2,783 | 1,001–1,421 |
| Legal segments to y | 0 | 0 |
| Reaching segments with a forbidden midpoint | all | all |

Every vertex lies over the origin, so the origin is the only branch value. Each nonfixed centre x sees every other unforbidden centre, itself included, except y. So the darkness is specific to the pair. A second, independent Fraction-sampling tracer agrees with the main tracer on all 2,016 (p = 7) and 3,168 (p = 11) segments with \|a\|,\|b\| ≤ 8.

## 3. Genus-9, degree-8p version (checks.log, Part B, p = 7)

The cocycle χ is algebraic intersection with the closed vertical edge on the left of square 2. The upstairs surface has 56 sheets: h′(i,k) = (h i, k + [i = 1]) and v′(i,k) = (v i, k).

- It's connected and has genus 9. It has 8 cone points of angle 6π, so it's unramified over X, and its absolute period lattice is ℤ².
- It has exactly 48 forbidden points.
- 29,760 segments run from the 8 lifts of x with max(\|a\|,\|b\|) ≤ 30. Of these, 6,008 reach a lift of y, all have forbidden midpoints, and none is legal. 312 of the 320 possible pairs of a source and a non-target, unforbidden centre are lit.
- The upstairs monodromy has exactly these block systems: 28×2, 14×4, 7×8, and the trivial ones. Every proper intermediate cover has at least p = 7 blocks. This matches the note's Riemann–Hurwitz and period-lattice argument, which I also checked by hand.

## 4. R22 block claim (checks.log, Part C)

The claim is confirmed. Re-running d93's `systems.py R22-base` gives G-block systems [(1,15), (5,3)]: a unique nontrivial system of 5 blocks of size 3. It is W-invariant. |G| = 233,280 comes from d93's `blocks.log` (line 14), because `systems.py` doesn't print it. The note describes this as an action on the 15 room cells over the pillowcase, which matches d93.

## 5. Scope

- **Not a room unfolding.** X does carry a full D₂ reflection action. r_x permutes squares by σ, and r_y is the identity on squares because v = v⁻¹. But X/D₂ is not a polygon. The pair {T(0), T(1)} is fixed by ι, is on no mirror, and becomes an **interior cone point of angle π** in X/D₂. The other four fixed points become boundary corners: three convex and the zero as a reflex corner. Gauss–Bonnet balances: 3·π/2 − π/2 + π = 2π. A 90° rotation is impossible because h and v have different cycle types. So no room, including a room with 45° walls, unfolds to X with these marks.
- **Rooms in general.** In a room unfolding, any automorphism with derivative −I is ι∘τ for a translation automorphism τ. If τ = 1, the fixed points are exactly the corner lifts, and x, ιx are the same physical point. If τ comes from a point symmetry ρ of the room, the fixed points include the lifts of the centre of ρ. By Brouwer, that centre lies in the room, and in a strictly simple room it is an interior point. So it is not forbidden, and the argument yields nothing. A dark distinct physical pair can come from this mechanism only through a hidden translation automorphism τ with Fix(ιτ) inside the corner lifts.
- **W ≤ 20.** The note doesn't touch it, and it says so correctly. The estimate is unchanged.

## Gaps

1. **Medium.** The scope reason is misstated. The note says the examples have "no asserted physical room reflection action". In fact X has the D₂ action. The real obstruction is the interior π-cone point of X/D₂: two of the six marks are not corner lifts. State this, and add the room criterion from section 5, so later work doesn't retry room versions of this family.
2. **Medium.** The bound being refuted is never written down. Its terms (degree over which base, whether n counts endpoints, whether the site must carry no forbidden lift) aren't fixed. The site s = (1/2,1/2) carries the forbidden centre C((p+1)/2). If the intended hypothesis needs a forbidden-free site, only the s, −s variant applies, and it uses two different sites.
3. **Low.** "Prime" and "p ≥ 7" aren't needed. The adjacent-transposition argument gives S_p, hence primitivity and a ℤ² period lattice, for every p ≥ 3. The bound "at most six preimages are fixed" is loose: exactly one centre is fixed for odd p, and none for even p.
4. **Low.** The note cites no prior work for the midpoint mechanism. Points swapped by a −I involution are a standard source of non-illumination. I didn't fetch a citation, so the note should mark the mechanism as standard rather than new.
5. **Low.** The genus-9 χ is defined only abstractly. Add the explicit cocycle from section 3, so the 64-pair example can be reproduced.
