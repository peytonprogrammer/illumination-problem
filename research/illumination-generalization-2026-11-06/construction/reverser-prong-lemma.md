# Global reversal does not supply the missing physical factor

A23 hand result, pending independent review. No illumination minimum or historical novelty is claimed. Original effort deadline remains in reverser-prong-effort.json.

## Definitions and accepted dependencies

Let P be a finite strictly simple polygonal disk with four-direction rational angles, q in {4,8} its minimal reflection-group order, M its connected reflection unfolding, Gamma its physical reflection group, and Sigma ALL actual corner lifts, including regular ones. For the orthogonal theorem below, every angle is 90 or 270 degrees and q=4; side lengths may be arbitrary real positive data.

An automorphism is globally single-valued on M, affine in translation charts and preserves Sigma as a set. Let G be the group of these automorphisms with derivative I. Let rho be the intrinsic central physical half-turn. A clean reversing involution means an automorphism tau with derivative -I, tau^2=id, and Fix(tau) contained in Sigma. These explicit hypotheses justify the ordinary time-reversal midpoint obstruction. A multivalued correspondence is NOT such an automorphism.

Dependencies: the independently accepted angle/prong counts in construction/genus-and-degree-review.md and construction/direction-skeleton.md; peer review/half-turn-quotient.md proves Fix(rho)=Sigma and, for orthogonal P, M/<rho> is a topological sphere. The latter uses the standard double-cover Euler/Riemann-Hurwitz count already in that accepted packet. No new external classification theorem is imported here.

## 1. A finite symmetry bound without a degree bound

At a marked cone point of total angle 2*pi*n, fix one oriented flat direction and its n outgoing germs (prongs). G permutes the finite set of all these germs. If an element fixes a germ, its local translation along that germ fixes its points and hence is the identity on an open regular chart; continuation through the connected regular surface makes it globally the identity. The same conclusion holds at a regular fixed point, without choosing a germ.

Thus G acts FREELY on the set of marked directional prongs, whose total is

    L = q*(W-2)/2.

In particular G is finite, |G| divides L, and |G|<=L<=76 at W<=21. This does NOT bound the primitive torus-cover degree, area, side lengths or k.

More sharply, for an orthogonal disk with r reflex corners and c=r+4 convex corners, Sigma has c regular points and r points of cone angle 6*pi. G preserves each stratum. Its actions on the c regular marks and the 3*r singular prongs are both free. Hence

    |G| divides gcd(r+4,3*r) = gcd(r+4,12).

When r=0 the second stratum is empty; the convention gcd(4,0)=4 gives the same statement.

## 2. Complete global-reverser explanations require a large translation orbit

Suppose two DISTINCT physical interior marks give disjoint free Gamma orbits A,B, each of size q. Assume the MUCH STRONGER premise that, for every a in A and b in B, a Sigma-preserving global derivative--I automorphism sends a to b. They need not yet be clean or involutive.

All derivative--I automorphisms form G*rho: tau*rho has derivative I, and conversely. G is normalized by Gamma because conjugation preserves derivative I and Sigma. For a fixed a0 in A we obtain B contained in G*rho(a0). Applying rho and using rho(B)=B gives B contained also in G*a0. The two G orbits intersect, so G*a0=G*rho(a0). For fixed b0 in B, the full cross-orbit premise gives A contained in G*rho(b0)=G*a0. Therefore A union B lies in ONE free G orbit of regular points. Its 2*q distinct points imply

    |G| >= 2*q.

This hypothesis is not inferred from darkness. Its orbit consequence is stronger than pairing one selected lift and retains all physical endpoints. It makes no factor-existence claim.

## 3. Exact orthogonal obstruction: only rho is clean

**Theorem.** For EVERY orthogonal P above, a Sigma-preserving global derivative--I involution tau distinct from rho has EXACTLY FOUR fixed points, all regular and outside Sigma. Consequently rho is the ONLY clean reversing involution.

Proof. First, every Sigma-preserving affine automorphism alpha commutes with rho. The conjugate u=alpha*rho*alpha^{-1} has derivative -I and fixes every point of Sigma, since Fix(rho)=Sigma. The map u*rho has derivative I and fixes any chosen regular convex-corner mark. A derivative-I automorphism fixing a regular point is the identity. Thus u=rho. Such a regular corner exists because c=r+4>=4. This argument needs no uniqueness theorem for hyperelliptic involutions.

Now t=tau*rho is a nonidentity derivative-I INVOLUTION, because tau and rho commute. It fixes no regular point. It fixes no singular corner either: at such a corner it would permute the THREE positive-direction prongs with order at most two. Any such permutation of three objects fixes a prong, which would make t the identity by Section 1. Hence t has NO fixed point in Sigma.

Let X=M/<rho>, the accepted sphere quotient. Since t commutes with rho, it descends to a nontrivial orientation-preserving involution tbar of X. It cannot descend to the identity: the two deck transformations of the connected double cover are id and rho, whereas t is neither (their derivatives distinguish rho).

An orientation-preserving conformal involution of a sphere has exactly two fixed points. Explicitly, the branched-cover Euler formula is -2=2*(2*g_Y-2)+F, where F is its number of fixed points and g_Y>=0. This forces g_Y=0 and F=2. A finite-order holomorphic fixed point is simple for this double quotient; the same local branch calculation was used in the accepted rho quotient.

Neither fixed point of tbar is a branch value of M->X: a branch fiber is a SINGLE point of Sigma, and t would fix it. Thus each fixed fiber contains two regular points outside Sigma. On each, rho swaps the two points; t also swaps them, because t has no regular fixed point. Their product tau=t*rho fixes BOTH points. Conversely every tau-fixed point maps to a tbar-fixed point. There are exactly four, and all lie outside Sigma. This proves the theorem.

## 4. What this changes, and what stays open

A clean global reversal can pair only x with rho(x). Those project to the SAME physical point. Therefore a distinct physical dark pair in an orthogonal room cannot be explained even one lift-pair at a time by clean globally defined reversing involutions on its original unfolding. In particular the already accepted orthogonal 22-wall control refutes an unrestricted proposal that every physical dark pair must have that explanation. This is a mechanism obstruction, not a W<=21 dark counterexample.

The theorem does NOT say that a non-clean tau graph illuminates, that all surface dark correspondences are graphs, or that nonillumination is exhausted by involutions. A particular pair related by a non-clean involution may still be dark for another reason. Higher-degree correspondences, quotients with additional lifting data, and the original parity folds remain possible. The known 22-wall control remains entirely consistent with the result.

Assessment: RETIRE global clean reversing automorphisms as a positive replacement for the missing factor theorem. The prong bound is an exact conditional constraint, not an uncapped proof strategy. To progress centrally, one must justify a multivalued/quotient mechanism from actual off-orbit darkness, or supply a different direct illumination argument. No such implication is proved here, and no new metric class or scan is proposed.
