# Illumination literature and research judgment

[done] Literature review checked 2026-10-31. No rays or candidate-room searches. [done] The new lattice obstruction received conditional mathematical acceptance from a read-only Opus challenge; independent data/code verification remains requested.

## Research judgment

The next task is an obstruction theorem before another construction search. The literature suggests using covering maps, marked-point actions, and finite affine-group classification. Applying those tools here produced a proposed closure of our remaining SAME-surface 22-wall refolding route. See `refolding-lattice-obstruction.md` for the explicit proof and its dependencies. This is progress in eliminating a proposed mechanism, not a smaller dark room.

I did not locate a later primary-source construction that improves the relevant published 22-edge example or independently verifies a smaller simple Jordan room. This is a bounded literature-search finding, not a claim that the literature is exhaustive or that 24 is the global record under every definition.

## What the current sources establish

| Source and actual date | Verified content | Consequence for this project |
| --- | --- | --- |
| [Wolecki, revised November 30, 2024](https://arxiv.org/html/1905.09358v3) | Finitely many nonilluminating pairs in a rational polygon with connected interior; a 22-edge example; generalized triangle no-return lemma. The arXiv version note explicitly reports correction of a technical gap. | Use v3. Treat its 22-edge figure and our simple Jordan target as different topology requirements. Pair finiteness does not itself prove instability under room deformation. |
| [Lelièvre–Monteil–Weiss, 2016](https://msp.org/gt/2016/20-3/gt-v20-n3-p11-s.pdf) | For any translation surface, a fixed point fails to illuminate only finitely many others. Torus covers are precisely the surfaces with the finite blocking property. | Finite blocking permits regular blockers; a dark billiard requires those obstructions to become forbidden corners. Surface and room statements must stay separate. |
| [Apisa–Wright, Marked points on translation surfaces](https://public.websites.umich.edu/~alexmw/ApisaWright.pdf) | Non-torus blocking is constrained by periodic points and covering maps. Proposition 3.11 classifies torus-cover rational billiards as Gaussian, Eisenstein, or rectangle-tiled. | This is a structural filter. It does not supply sufficiency for arbitrary periodic pairs, and non-torus hypotheses cannot be imported into our square-tiled controls. |
| [Apisa, IMRN 2025 publication](https://academic.oup.com/imrn/article/2025/16/rnaf254/8237719); [2017 preprint](https://arxiv.org/html/1710.05505v1) | Genus-two point-marking and finite-blocking classifications; primitive nonarithmetic setting includes exceptional golden points. | A recent publication date is not a newly discovered 2025 construction. The theorem does not directly apply to our genus-25 torus cover. Final journal text could not be fetched; theorem details here refer to the accessible preprint. |
| [Freedman, Journal of Modern Dynamics, April 2024](https://www.aimsciences.org/article/doi/10.3934/jmd.2024004) | Periodic-point classification for Prym eigenforms in minimal strata in genera 2–4. | Useful low-genus filters, no direct high-genus extension justified. |
| [Gutiérrez-Romo–Pardo, August 2024 preprint](https://arxiv.org/html/2408.03832v1) | Classifies affine permutations of Prym fixed points in the stated low-genus families. | Reinforces the need to track permutations. A periodic point need not be fixed by every affine map. |
| [Faraco, July 2026 preprint](https://arxiv.org/html/2607.14822v1) | Survey of topology, developing maps, strata, period realization, and deformation of translation surfaces. | Useful toolkit for a future change-of-surface mechanism. Its title “The dark side” is not an illumination improvement. No darkness-preserving surgery follows from the survey alone. |

The 22-wall contact and 20-wall slit diagnoses come from our exact reconstruction, not an explicit topology disclaimer by those authors. No author contact was made.

## A finite classification is available if needed

[Schmithüsen's origami algorithm](https://arxiv.org/abs/math/0401185) computes Veech groups from finite coverings. Current [GAP Origami documentation](https://ag-weitze-schmithusen.github.io/Origami/doc/chap2.html) exposes coset permutations and orbit representatives; [surface-dynamics](https://flatsurf.github.io/surface-dynamics/examples/square_tiled_surfaces.html) accepts right/up permutations and computes Veech groups. These are existing tools, not a reason to write another optical search.

Here is the mathematical reduction. Let Γ be the derivative image of the affine group preserving both finite mark sets, after normalizing its invariant lattice. Rational torus marks have finite orbits, so this stabilizer has finite index in the integral ambient group. Our controls' derivative kernel is trivial. Every integral dihedral group of order eight is conjugate to the standard square group K; this follows from [Jones–Pinto](https://www.mat.uc.pt/preprints/ps/p0924.pdf), Section 3, Remark 3.

Represent a candidate derivative group as A K A⁻¹. It lies in Γ precisely when the finite left coset ΓA is fixed by right multiplication by every element of K:

    Γ A k = Γ A  for every k in K.

Candidates related by the normalizer of K give the same subgroup. Faithful derivatives make lifts unique when they exist. Recover actual maps and retain source/target transitivity, fixed-point counts, mirror stabilizers, disk topology and injective development as separate gates. This is a finite classification framework, with no matrix-entry cutoff; its orbit size may still be expensive. No full marked orbit was computed.

## The new obstruction and the decision it changes

The exact 22-wall gluing has absolute period lattice 2Z². All sixteen source/target lifts share one torus fiber. More decisively, these are exactly its regular square vertices not fixed by rho. A marked integral square-symmetry action therefore appears to force every non-A lattice point to remain a corner in any admissible simple quotient. That returns the quotient to our STRICT canonical triangle family, whose verified minimum is 24, contradicting the forced 22 walls.

A further necessary budget follows: a smaller canonical room needs at least four exceptional B/C positions, which require at least 32 regular lattice lifts outside Fix(rho), including the sixteen marks. The contact control has only sixteen; the 24-wall control has twenty. This is a necessary count, not a sufficient darkness certificate.

This is stronger than the earlier fixed-mass count: that count left open changing the contact topology. The new reduction closes that remaining option conditional on its hypotheses and the prior strict-family result. Opus accepted the supplied-data mathematical argument; the two requested clarifications are incorporated. Independent data/code verification remains pending. The detailed note records the failed anchor assumption and the comparison control where the sixteen-point identity fails.

## Research agenda and stopping rules

1. **[in progress] Complete independent data/code verification of the lattice obstruction.** Opus accepted the mathematical reduction on supplied data. A separate Claude board handoff asks it to check the fixed-scale normalization, induced torus translations, and absence of transparent vertices. Do this before implementing an affine orbit enumeration. The current research decision is to retire the three reconstructed SAME-surface controls under the stated assumptions, reopening only for a specific counterexample or verification failure.
2. **[in progress] Make the next construction mechanism answer a different question.** Can the marked translation surface itself change while preserving a verifiable obstruction for every source/target lift pair? Require an explicit blocking set, the reason it remains unavoidable, and a simple planar quotient with at most 23 walls. Period realization or splitting a cone alone answers none of these. Faraco’s Sections 5.7 and 6.8 explain how surgery can preserve absolute holonomy while changing branch data; preserving holonomy is weaker than preserving the relative marked data and blocking obstruction. A deformation proposal must address that gap explicitly.
3. **[done] Keep current negative results scoped.** The 24-wall minimum covers our canonical family through three exceptions; it does not settle four exceptions, other marked positions, other tilings, or arbitrary polygons. The new obstruction, if correct, closes a specific refolding mechanism only.

I would not call any unconstructed surgery or generic perturbation the most promising breakthrough. The next substantive deliverable should be a precise sufficient lemma with a wall-saving planar model, or a proof that a proposed lemma cannot work. Ray searches remain paused.

**Next move:** complete the independent data check; require the next construction proposal to change the marked surface or the blocking certificate and supply an explicit simple quotient before any ray search.
