# Orthogonal translations descend faithfully to polygon symmetries

R23 candidate theorem for independent hand review. This strengthens the conditional A23 group bound and obstruction; it does not prove the W<=21 illumination target. No discovery scans or fixed-room calculations are used.

## Statement and assumptions

Let P be any bounded finite strictly simple orthogonal polygonal disk, with arbitrary real side lengths. Merge all straight-angle vertices. Let M be its connected minimal four-copy reflection unfolding, Gamma the physical Klein four reflection group, and Sigma the full set of actual corner lifts, including regular lifts. Let G be ALL globally single-valued affine automorphisms of M with derivative I which preserve Sigma setwise. Then:

1. Every element of G commutes with EVERY element of Gamma.
2. G descends faithfully to Euclidean self-isometries of P whose linear parts belong to Gamma.
3. Consequently G is isomorphic to a subgroup of Gamma. In particular |G| divides4; combining with the regular-corner count gives |G| divides gcd(4,r+4), where r is the reflex-corner count.
4. If S,T are distinct physical interior points and A,B their disjoint four-point lift fibers, there do NOT exist globally single-valued Sigma-preserving derivative -I affine automorphisms connecting EVERY a in A to EVERY b in B. Neither cleanliness nor involutivity is needed for this exclusion.

No arithmetic hypothesis, area/diameter bound, exception count, darkness classification or wall-count restriction is needed.

## 1. Fixed corners anchor the full centralizer

Every orthogonal genuine corner has angle pi/2 or3pi/2. Its two incident wall reflections generate all of Gamma. Therefore it has ONE lift in M, fixed individually by EVERY gamma in Gamma. This applies to both regular convex marks and singular reflex marks. It is stronger than just Fix(rho)=Sigma.

There is a regular convex mark p: the signed turning identity gives c=r+4>=4. For alpha in G, alpha(p) is also a regular corner mark, since affine automorphisms preserve local cone angle and preserve Sigma. Thus gamma fixes both p and alpha(p), for every gamma in Gamma.

The conjugate gamma*alpha*gamma^-1 is another derivative-I affine automorphism: conjugation by an orientation-reversing reflection still has derivative R*I*R^-1=I. Its value at p is alpha(p). Hence

    alpha^-1 * gamma * alpha * gamma^-1

has derivative I and fixes p. A derivative-I map fixing a regular point is identity on a regular chart and then globally, by continuation on the connected surface minus its finite singularities. This proves gamma*alpha=alpha*gamma. Only setwise Sigma preservation is assumed; individual corner labels need not be preserved by alpha.

## 2. Physical quotient and local Euclidean maps

Let pi:M->P be the physical projection. Its fibers are exactly Gamma orbits, including all boundary stabilizers, by the construction of the minimal reflection unfolding. Commutation makes

    f_alpha(pi(x)) = pi(alpha(x))

well defined. The inverse is induced by alpha^-1, so f_alpha is a homeomorphism of P. Commutation also preserves every point stabilizer: Gamma_alpha(x)=Gamma_x. A physical interior point has trivial stabilizer; each smooth-wall lift has a nontrivial wall-reflection stabilizer; each corner lift has all of Gamma as its stabilizer. It follows that f_alpha maps the interior of P onto itself.

On an interior neighborhood, choose an unfolding sheet for x and one for alpha(x). The corresponding developing charts differ from physical coordinates by linear parts A,B in Gamma and constant translations. Since alpha has derivative I, the derivative of f_alpha in physical coordinates is

    B^-1 * I * A in Gamma.

Thus f_alpha is a local Euclidean isometry of the open polygon interior. The derivative is locally constant and takes values in the finite group Gamma. The interior is connected, so it has ONE constant derivative R_alpha. The local translation terms then join to a single v_alpha. Therefore

    f_alpha(z)=R_alpha*z+v_alpha

on the whole interior, and by continuity on P. No convexity or extension across a corner is needed: connected overlapping interior neighborhoods suffice.

## 3. Faithfulness and order bound

If f_alpha is identity, then over any small interior neighborhood alpha sends each lift to a Gamma-related lift of the same point. The physical fiber is free, so on a still smaller connected neighborhood there is one constant gamma with alpha=gamma. Comparing derivatives gives gamma=identity, since the representation of Gamma is faithful and alpha has derivative I. Equality on an open regular chart implies alpha=identity globally. Hence alpha->f_alpha is injective.

The map alpha->R_alpha is a group homomorphism. Its kernel is trivial: R_alpha=I would make f_alpha a translation z->z+v preserving the bounded nonempty polygon P. Iterating such a translation preserves P; boundedness forces v=0, and faithfulness then gives alpha=identity. Thus G embeds in Gamma, proving |G| divides4. The separately accepted free action on c=r+4 regular corner marks implies |G| divides gcd(4,r+4).

This proves an UPPER bound and faithful descent; it does not require that every polygon symmetry lifts to an element of G.

## 4. Consequence for complete -I explanations

Here is a self-contained orbit proof, avoiding any symmetry-to-darkness implication. Let rho in Gamma be the physical half-turn. All marked derivative -I affine automorphisms are exactly G*rho: multiplying one by rho has derivative I and preserves Sigma. By section1, rho commutes with G.

Assume the complete cross-fiber premise in the statement. Fix a in A. Every b in B lies in G*rho(a). Applying rho and using rho(B)=B gives B subset G*a. These two G orbits meet, so they coincide. Fix b in B. Inverses of the original maps supply derivative -I maps from b to EVERY a' in A. Thus A subset G*rho(b). But rho(b) lies in B subset G*a. Therefore A union B lies in one G orbit.

A,B are disjoint, each has4points, so this orbit contains8points and |G|>=8. Section3 gives |G|<=4, a contradiction. This excludes the full global-automorphism explanation even if the maps vary with the selected lift pair and even if they are not involutions or clean. It does not exclude one isolated cross-fiber global map, a union of higher-degree correspondences, or other reasons for darkness.

## Dependencies, independence and scope

Dependencies are the elementary reflection-unfolding conventions and accepted corner-lift/physical-fiber facts in review/half-turn-quotient.md, plus the finite symmetry/prong definitions in construction/reverser-prong-lemma.md. The full proof of the strengthened bound and orbit obstruction appears here. The A23 exact-four-fixed-points theorem is not used. No Riemann-Hurwitz, classification or new literature theorem is imported in this proof.

The accepted orthogonal22 dark control shows that physical darkness cannot generally imply the excluded complete global-automorphism premise. For W<=21 the physical illumination question remains OPEN. This theorem rules out that proposed explanation on all orthogonal rooms; it supplies neither a new dark room nor the required strict whole-copy parity fold. Diagonal walls have corner stabilizers of different sizes, so the pointwise full-Gamma corner argument must NOT be transferred to the eight-copy model without a separate proof.

Review targets: all-corner stabilizers, preservation of regular corner marks, antiholomorphic conjugation, connected punctured-surface identity, exact physical quotient fibers, interior preservation, local-to-global Euclidean descent on a nonconvex disk, both faithfulness kernels, full8-point orbit argument and all scope exclusions.
