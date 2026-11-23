# What has to depend on the primitive direction class?

## Two of the four midpoint sites suffice for one class

Let X → Y → ℝ²/Λ be translation coverings, with all maps expressed in the same translation coordinate. Write π for the composite and f for the first map. Fix regular lifts s,t over the same torus site p, with distinct physical endpoints. Fix a nonzero class c in Λ/2Λ, using c/2 to denote its well-defined image in the two-torsion of the torus. Suppose Y admits a −I involution e exchanging f(s) and f(t). For direction class c it suffices that

    f⁻¹(Fix(e)) ∩ π⁻¹({p, p+c/2}) ⊆ F,

where F consists of forbidden physical corner lifts. There is no condition on fixed points over the other two sites.

Indeed a hypothetical legal path with holonomy k v has v primitive in Λ, v mod 2Λ = c and k a positive integer after choosing the sign of v. Its midpoint projects to p for even k and p+c/2 for odd k. Its image path on Y is regular: a zero downstairs has only zero preimages under a translation covering, and a legal path on X avoids zeros. Applying e and reversing time gives the same initial point and velocity as the original image path. Uniqueness of continuation through regular points fixes its midpoint. The displayed inclusion now gives a forbidden point on the original path.

Every e-fixed point projects to one of the four sites p+(½Λ)/Λ: the torus coordinate after e is the negative of the original coordinate plus 2p, by the derivative and the exchanged endpoints. Consequently if the **same f and e for this lift pair** satisfy the displayed test in all three classes, their three inclusions recover the complete fixed-fiber hypothesis. This applies separately to each relative lift choice. Conversely, when full forbidden-fiber transfer fails, record the torus sites of the regular preimages of e-fixed points. A single such preimage over p disqualifies this involution from this test in every class. If the bad sites all differ from p, each disqualifies exactly its own nonzero class. These statements are exact for the inclusion test. A regular fixed preimage alone proves nothing about whether a trajectory reaches it.

This identifies what changing the quotient per direction can buy. If each class uses one common quotient for *all* relative lift pairs and imposes d142's **full** fixed-fiber hypothesis, any one class would already satisfy the d142 hypothesis by itself. Different quotients for the three classes do not evade it. Permitting regular fixed preimages at the two unused sites genuinely weakens the hypothesis. A path-dependent seam reversal need not furnish any involution.

## Exact relay test for the missing geometric implication

On the orthogonal half-translation double Q, take distinct same-class interior marks over a pillowcase pole a. For any other pole x, let c=x−a in physical parity coordinates. Fix a regular lift m over x. For a physical mark S define L_m(S) to be the set of unoriented primitive slopes for which the straight leaf through m, cut at all forbidden corners, contains a lift of S. Every slope in this set has primitive parity c: the displacement in the pillowcase development joins opposite site labels a and x, so the multiple of the primitive vector is odd.

The pair is lit in class c **if and only if** there is a regular m over x with L_m(S) ∩ L_m(T) nonempty. A witness from S to T has a positive even number of primitive steps. Its first step ends over x at a regular interior point of the segment. Conversely, at a regular relay one unoriented line has unique continuation in both senses. The connected corner-free leaf contains both endpoints, so its subarc joins them even if the two legs approach m from the same side. On a closed leaf choose an arc between the endpoints.

There is a finite form retaining the direction data. Use the finite-index affine return subgroup fixing the labeled lattice fibers and preserving the corner set as in [the cusp argument](per-class-converse.md). For the fixed m, each L is a union of cusp orbits. If there are k such orbits in the given parity, the two marks occupying more than k orbits **in sum at the same relay** certify a common slope. Two class failures therefore give two families of disjoint cusp sets, one at every regular relay in each of those classes. BBBB supplies relays in the third class. It gives no lower bound on either mark's cusp occupancy there. The midpoint-site test is sufficient and the relay test is exact, but neither currently proves that a physically dark pair has a fold.

## The two quotient controls from d141

The V-notch B has genus 3. Under the *all-lift, full-fiber* hypothesis the cyclic refinement X → Z in d142 would have genus at least 5. Riemann–Hurwitz immediately excludes it, independently of the degree of the initial quotient X → Y. In particular the actual degree-three quotient by C₃ can block selected lifts without satisfying that hypothesis.

For the four-chamfer octagon, genus(X)=9. The same genus bound gives deg(X → Z) ≤ 2. The higher-genus H branch would require genus(Z) ≥ 11. In the elliptic H branch, one source image has at most three partners by the three nonzero elliptic two-torsion translations, whereas the eight target lifts have at least four distinct images at degree at most two. This applies to the octagon's quarter-turn quotient as well. Both deductions use d142's refinement lemmas, currently in review. Neither transfers the one-in-eight theorem from X to arbitrary quotients. An order-four −I map on X cannot itself reverse a regular segment onto itself: if it did, its square would fix a regular interior point with derivative I, hence be the identity by the local translation coordinate and continuation. Its image in a quotient may have order two.

[Named quotient computations](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d141-review-freeht/review.md) · [Refinement and genus bounds](two-image-midpoints.md)

**Next question.** For a hypothetical dark BBBB pair, can the lifts at even and odd traversal counts in one primitive class be separated by a quotient satisfying the two-site test, or is a developed-path invariant essential as in R22? The torus computation specifies which fibers such a proposed proof actually has to control. No discovery search or new trajectory replay was used.
