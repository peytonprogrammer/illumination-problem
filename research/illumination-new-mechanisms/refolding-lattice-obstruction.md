# A lattice obstruction to refolding the contact surface

[done] Conditional deduction, 2026-10-31. Exact gluing and lattice facts pass. A read-only Opus mathematical challenge accepted the argument conditionally; a separate peer code/data verification remains pending. This supersedes the recommendation to enumerate quarter-turns on the existing 22-wall surface if the reduction is accepted. No new dark room is claimed.

## Conditional proposition

Under the SAME marked-surface, free source/target orbit, faithful affine reflection action, invariant metric, and simple injective planar development hypotheses in `refolding-bound.md`, the reconstructed 22-wall contact surface has no admissible simple quotient.

The final contradiction uses our previously established computer-assisted strict canonical-family minimum of 24. Thus this is conditional on that model and its verified finite exclusions, as well as the earlier local quotient lemmas. It is not a general 24-wall lower bound.

## Exact facts about the 22-wall surface

The new `literature-lattice-probe.py/json` reconstructs the square gluing without optical trajectories.

1. The absolute holonomy lattice is exactly 2Z². All spanning-tree cycle generators have even coordinates; the gcd of their 2×2 determinants is 4. In fact (2,0) and (0,2) occur among the generators.
2. All eight source and all eight target lifts project to the SAME point of R²/2Z². Choose its image as 0.
3. There are 26 regular square vertices. Exactly ten are fixed by the unique derivative −I map rho. The remaining sixteen are EXACTLY the source and target lift sets. This checks set equality, not just cardinality.
4. Every genuine cone and every old absorbing regular vertex belongs to C = Fix(rho), as established in `refolding-bound.md`. There are no additional fixed square centers or edge midpoints.

The unique m=7 cone projects to (1,1), NOT the source fiber. An initial attempted anchor-at-source assertion failed and was discarded. It is unnecessary: preservation of the source set fixes the source fiber directly. The 24-wall control is deliberately retained as a comparison: it has twenty regular nonfixed square vertices, so the sixteen-point equality fails there. The argument is specific to the 22-wall surface.

## Reduction to the strict canonical family

Assume an admissible quotient exists.

**A. Normalize the full reflection group.** The previous cone gate forces an order-eight dihedral action H. Every affine automorphism preserves the absolute holonomy lattice 2Z², so its derivative is in GL(2,Z). Every order-eight dihedral subgroup of GL(2,Z) is integrally conjugate to the square symmetry group K = <J,F>, where J(x,y)=(-y,x), F(x,y)=(x,-y). See Jones–Pinto, *Hypermap operations of finite order*, Section 3, Remark 3. Apply the integral change of coordinates. An invariant positive definite metric for K is a scalar multiple of the Euclidean metric; thus this normalization describes the actual quotient geometry up to similarity.

**B. The torus action has no translation part.** In the normalized coordinates, the source and target sets still project to 0 modulo 2Z². Each h in H preserves each set, because a free eight-point orbit contained in an eight-point set equals that whole set. The induced affine torus map therefore fixes 0. Its translation part lies in 2Z².

**C. All corners lie on the canonical integer grid.** The earlier corner correspondence gives corner preimage = Fix(rho), with rho = r². The induced torus map of rho is x ↦ −x, so its fixed points lie over Z²/2Z². To specify the development, restrict X → P to the interior of the assumed simple polygon. It is an unramified eight-sheeted cover of a disk, hence is trivial. Choose one sheet D, containing exactly one source lift, and put that lift at the origin. The developing map on its closure agrees with the period map modulo 2Z². Consequently every developed polygon corner has integer coordinates.

**D. Every side lies on a canonical grid edge line.** Its stabilizing reflection has linear part one of K's four reflections and translation in 2Z². The fixed lines are therefore x = integer, y = integer, x−y = even integer, or x+y = even integer. These are exactly the lines supporting edges in our canonical 45–45–90 triangle grid. The complete arrangement of these lines partitions the plane into exactly those canonical triangles. A simple polygon whose boundary follows the arrangement is therefore a finite union of whole triangles at this scale. The source and target have even-even coordinates and, by hypothesis, are distinct interior A points.

**E. No B/C exception is possible.** Lift a canonical B or C vertex that is interior or smooth on a side. It lies over one of the three NONZERO points of Z²/2Z². It is regular on X; smooth boundary doubling introduces no cone. It is not fixed by rho, since the corner correspondence forces every rho-fixed point to be a genuine polygon corner. But exact fact 3 says every regular square vertex outside Fix(rho) is a source or target lift, both over 0. Contradiction.

Thus the quotient is a strict canonical simple polygon, with no transparent B/C vertices. The previously verified strict-family result requires at least 24 walls. The fixed-corner mass formula in `refolding-bound.md` forces 22 walls on this surface. Contradiction.

## Why the lattice vertices in step E are the audited vertices

The original square vertices are the full inverse image of Z²/2Z² under the absolute-period torus map. The coordinate change is integral and invertible, so it preserves that four-point torus set and its full inverse image. No arbitrary finer grid is substituted. This is the essential extra content beyond merely citing that torus-cover billiards are Gaussian after some subdivision.

## References and reproduction

- [Jones–Pinto, finite integral subgroup classification](https://www.mat.uc.pt/preprints/ps/p0924.pdf), Section 3, Remark 3.
- [Apisa–Wright, Marked points on translation surfaces](https://public.websites.umich.edu/~alexmw/ApisaWright.pdf), Proposition 3.11 provides the related general torus-cover/Gaussian classification, but alone does not establish our fixed-scale, marked, zero-exception reduction.
- Local strict-family proof: `../illumination-analysis.md`, section “Complete exclusion below 24 in the strict simple 45-degree family”; its two independent integer formulations and frozen receipts remain unchanged.

Run `python3 -B .context/illumination-new-mechanisms/literature-lattice-probe.py`.

This checks the gluing facts and period generators. It does not execute the strict-family solvers or prove steps A–E by code. The supplied-data mathematical review accepts these steps after the sheet construction and line-arrangement explanation were made explicit. Independent code/data verification remains requested.

**Next move:** independently audit steps A–E and the applicability of the strict-family minimum. If accepted, retire SAME-surface refolding of all three existing controls; any construction advance must change the marked surface or the certificate-transfer assumptions.

## A necessary budget for a different canonical construction

This counting corollary uses the established three-exception exclusion, rather than asserting a new blocking mechanism. For any simple canonical quotient with A marks, let J be the number of interior B/C exceptions and s_N the number of smooth-boundary B/C exceptions. Their lift orbits are regular, not rho-fixed, and have respectively eight and four points. The two interior marked orbits contribute sixteen more. Therefore the number R of regular square vertices outside Fix(rho) satisfies

    R >= 16 + 8J + 4s_N.

A room below 24 walls needs J+s_N >= 4 under our existing family result. It consequently needs R >= 32. This count can include additional unmarked A fibers, so R >= 32 is necessary, not sufficient. The contact control has R=16; the simple 24-wall control has R=20.

For these faithful order-eight quotients, all genuine cones lie in Fix(rho). If X consists of n squares and has genus g, Euler gives V=n−2g+2. Writing F=|Fix(rho)| then gives R=V−F. Combined with the previous wall identity F+2g=4W−6:

    R = n + 8 − 4W = 4(N − W + 2),

where N=n/4 is the canonical triangle count downstairs. Thus a new sub-24 canonical construction must also satisfy N >= W+6. This does not make a candidate dark; it is a useful rejection condition before constructing or tracing one.

## Peer review receipt

`literature-peer.json` contains a read-only Opus challenge. Verdict: ACCEPT CONDITIONAL. It accepts the earlier stabilizer/corner gate and steps A–E on supplied exact data, and requested the sheet construction and corrected line-arrangement explanation now incorporated. It ran no code and did not independently audit the strict-family solvers. The later regular-vertex-budget appendix was not included in its frozen prompt. No formal proof or literature novelty is claimed.
