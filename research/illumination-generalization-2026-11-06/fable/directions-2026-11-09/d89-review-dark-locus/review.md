# D89: review of dark-locus.md (snapshot)

Date: 2026-11-20. Reviewer: independent referee. Reviewed file: `dark-locus.snapshot.md`. SHA-256 `e2ddedc7…bc4e3c` matches the coordinator's record. (The SHA-1 is `1c0280a5…`; the live `qclass-closure/bbbb/dark-locus.md` is byte-identical.)

Context read: d80 review, `high-valency-geometry.md`, `shadow-budget.md`, d86 review. EMM, Filip, Wright, Eskin–Filip–Wright (EFW) and Apisa–Wright statements are from memory. I had no web access and couldn't check theorem numbers.

Own code: `dims.py`, log `dims.log`. It checks the dimension and rank arithmetic for r = 1–8. It doesn't touch any room. CPU under 0.1 s.

## Verdicts

| Claim | Verdict | Reason |
| --- | --- | --- |
| Setup (space, EMM, Filip) | Sound with fixable gaps | The four-label dark set is closed and invariant in a fixed marked stratum that depends only on r. The marked-quadratic forms of EMM and Filip are standard, but the note doesn't state them precisely. |
| Key step (mirror and d80) | Sound | σ is an antiholomorphic involution of the labeled stratum. It fixes every physical tuple. A nonzero fiber tangent gives a real arc of physical dark pairs in one room, and d80 forbids that arc. |
| Theorem: uniform D(r) | Sound with fixable gaps | The argument is complete given d80. Two fixes: say that the regular locus of N is connected, and say that the result is conditional on d80 and its inputs. |
| Corollary: ranks 2–5 at r = 8 | Sound with fixable gaps | k ≥ 2 and the high-rank exclusions hold. Two steps are written more loosely than needed, and the citations come from memory. |
| Relevance statements | Accurate | The note says the result gives nothing for integral marks and gives no area bound. Both statements are correct. |

## 1. The space

- **Which locus.** The note doesn't use the closure of physical examples or a square-tiled orbit. It uses the full set D₄ of surfaces in the labeled stratum Q(1^r, −1^(r+4)) with four regular labels s±, t± where all four cross pairs are dark. D₄ is closed in the stratum because a legal segment persists, and it's GL⁺-invariant. It contains every physical tuple. Each physical tuple lies on a closed orbit, but N is a component of D₄ chosen to hold infinitely many such tuples, so N isn't one orbit. This is well defined.
- **Corners and darkness.** Convex corners are poles and reflex corners are zeros. Both are singularities of the stratum and both block segments. On the orientation cover the poles become regular marked points that must still block. The d86 review already accepted this convention. Darkness of all four cross pairs on the double is equivalent to physical darkness.
- **Finite union.** The note cites EMM Theorem 2.2. I recall that EMM state a finite-union theorem for closed P-invariant sets in §2, but I can't confirm the number. Apply it on the orientation-double locus with eight upstairs labels. That locus is itself an affine invariant manifold, so this is legitimate.
- **Fix.** Name the precise statements used for marked strata: EMM finite union, Filip algebraicity, and the forgetful map being algebraic with affine invariant image.

## 2. The mirror step

- **Involution.** σ is complex conjugation of q combined with swapping s₊↔s₋ and t₊↔t₋. It normalizes GL⁺ through conjugation by diag(1, −1). On a physical double, the mirror is an antiholomorphic isomorphism from Q to its conjugate. It preserves every corner label and swaps the mark labels. So every physical tuple is a σ-fixed point. Labeled corners leave no automorphisms (2r + 4 ≥ 6 fixed points on a sphere), so the moduli space is a manifold at these points.
- **σ-stability and smoothness.** If σN ≠ N, then N ∩ σN is a closed invariant proper subset of N. It's a finite union of lower-dimensional loci that would carry the unbounded examples, which contradicts minimality. The same holds for the singular locus. Both steps are correct.
- **Real arc in one room.** σ preserves the fiber of N over the fixed underlying Q. If its tangent K is nonzero, the fixed set of the antiholomorphic involution on the fiber germ has real dimension dim_C K ≥ 1. On that arc the antiholomorphic identification fixes every corner label, so it is the physical mirror. Every tuple on the arc is two mirror pairs off the seam, so the arc gives interior physical points. Each tuple lies in N ⊂ D₄, so all four cross pairs are dark. Darkness is preserved along the fiber because the whole fiber lies inside D₄. Closedness plays no role there. The map from the arc to ordered physical pairs is nonconstant: if s₊ and t₊ were fixed, their mirrors would be fixed too.
- **d80's hypotheses.** The room is the same room: strictly simple, normalized, lattice, r ≤ 8, n ≥ 120. The pairs are distinct and interior. So d80 applies and allows only countably many dark pairs. A continuous nonconstant arc can't lie in a countable set. K = 0 follows.

## 3. From K = 0 to a uniform D(r)

The coordinator asked whether arithmetic loci break uniformity, since square-tiled loci are full of rational points with arbitrary denominators. They don't, for this reason:

- In the unmarked genus-0 quadratic stratum there are no relative directions. All 2r + 4 singularities have odd order and are fixed by the deck involution, so H¹(X, Σ)⁻ = H¹(X)⁻. `dims.py` checks dim = 2r + 2 = 2g for r = 1–8.
- K = 0 says that the marks add no directions. So N maps injectively to absolute periods, and dim N = 2k.
- Rational points of arbitrary denominator in an arithmetic locus come from relative directions, such as a freely moving point over a torus cover. Those directions are exactly the ones that K = 0 and rel = 0 remove. If k = 1, N is a single closed orbit, and the same inclusion bounds its denominators.

The rest of the argument checks:

- **Rationality.** GL⁺(2, Q) images of the selected examples are dense in N by minimality. A real-linear subspace with dense rational points is defined over Q. The note doesn't assume that a plane through one rational point is rational, which is correct.
- **Denominator.** Injectivity over Q writes each relative period as a Q-combination of absolute periods. With a common denominator D, the inclusion D·Per(relative) ⊆ Per(absolute) holds modulo integral classes whose period vanishes on N. That set of classes is monodromy-invariant, so the inclusion holds without a choice of basis. At a physical example the absolute periods lie in 2Z² and a corner has integer coordinates, so every mark's denominator divides D.
- **Uniformity over area.** This comes from the fixed stratum: D₄ depends only on r. The proof by contradiction picks one minimal component that holds an unbounded-denominator subsequence. EMM's finite union is the finiteness step. No separate finiteness over components is missing.
- **Gap (low): connected regular locus.** The relations continue "throughout the connected immersed branch". State why the examples lie in one connected piece. N is the closure of an orbit Gy with y regular. Each component of N_reg is open in N, and the dense connected set Gy meets only one of them, so N_reg is connected.
- **Gap (medium): conditional status.** D(r) is exactly as strong as d80. d80 was reviewed as sound with fixable gaps, and it rests on d16 with corrections, three-sheet, low-valency, and the uniqueness of the maximal partition at n ≥ 120. The theorem should say that it is conditional on d80.

## 4. Rank exclusions at r = 8

- **k ≥ 2.** With rel = 0, k = 1 means complex dimension 2, which is one closed orbit. The ratio of area to absolute covolume is 4n/4 = n, so n is fixed. This is correct.
- **Non-torus generic surface.** For rank ≥ 2 this is correct.
- **Upper bound, component case.** The orientation-double locus of Q(1^r, −1^(r+4)) has dimension 2r + 2, and H(2^r) has dimension 3r + 1. For r ≥ 2 a component of H(2^r) can't fit inside the double-cover locus. For r = 1 the component is H(2), where periodic points are Weierstrass points. The note's hyperelliptic-component discussion reaches the right conclusion. The dimension count is shorter and needs no citation. `dims.py` tabulates it.
- **Upper bound, holonomy-double case.** I = J holds. Otherwise IJ is a nontrivial translation automorphism, and a translation cover of degree d ≥ 2 over genus h has rank ≤ h ≤ (g + 1)/2 < g/2 + 1. This checks independently of the cited lemma number. The full genus-0 stratum Q(1^r, −1^(r+4)) results. Its periodic points are singularities, by Apisa–Wright on marked points (from memory). So regular marks aren't periodic.
- **Fix (low).** The "no Möbius symmetry, therefore nonhyperelliptic" sentence is loose. Lanneau's hyperelliptic quadratic components are defined by a global involution, not by cross ratios. The conclusion holds either way, because the low cases (r = 1, H(2)) also have Weierstrass periodic points only. Cite the exact hypothesis of the theorem used.
- **Range.** g = 9 and k < 5.5 give k ∈ {2, 3, 4, 5}, which is correct. For r = 1 the allowed range is empty. The note could add that an unbounded r = 1 sequence is excluded outright.
- **Citation check.** I couldn't verify the Apisa–Wright high-rank theorem (rank ≥ g/2 + 1 gives a stratum component or a full holonomy-double locus), Lemma 2.1, Marked Points Theorem 1.4, or EFW finiteness. My memory of the high-rank theorem matches the note's use of it.

## 5. Relevance

- Same-parity lattice pairs already have denominator 1. The note says so: "the denominator assertion alone gives no information about the already integral marks in the midpoint problem." The coordinator's summary ("No gain for same-parity lattice pairs") is accurate.
- The corollary does constrain lattice pairs, but only as unbounded-area sequences. Such a sequence must lie in an unclassified proper rank 2–5 locus with four periodic marks. A single dark room at bounded area is untouched. Nothing is said for n < 120. The result is non-effective, and no D(r) value or area cutoff follows. The note states all of this.
- r ≤ 8 is W ≤ 20 for orthogonal rooms (W = 2r + 4). So the note addresses the current orthogonal target. The 45-degree case is outside it.
- **"22-wall minimum remains open" is accurate.** Nothing here proves that every pair is lit in any room with W ≤ 20.

## Findings

1. **Medium.** State that the theorem is conditional on d80 and on d80's inputs: d16 with corrections, three-sheet, low-valency, and partition uniqueness at n ≥ 120.
2. **Low.** Add the one-line proof that N_reg is connected, which the monodromy continuation uses.
3. **Low.** Replace the hyperelliptic-component discussion with the count 2r + 2 < 3r + 1 for r ≥ 2. Tighten the Möbius/hyperelliptic sentence, and give exact theorem hypotheses for the marked-quadratic EMM, Filip and Apisa–Wright statements.
4. **Info.** The arithmetic-locus concern is resolved by rel = 0 together with K = 0. Uniformity over area comes from EMM finite union in a stratum that depends only on r.

## Re-run

```
cd d89-review-dark-locus && python3 -B dims.py > dims.log
```
