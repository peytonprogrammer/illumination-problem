# Opus coordination: structural illumination question

[in progress] Opus consultation running. This section records Codex's independent deduction before reading its response. No trajectory or orbit computation performed.

## Covering transfer has a wall cost

Assume f:X→X0 is a degree-d translation covering of compact translation surfaces, each admitting the faithful order-eight quotient and wall identity in refolding-bound.md. Let rho and rho0 be the quotient half-turns. Suppose f^-1(Fix(rho0)) is contained in Fix(rho). This is stronger than equivariance; equivariance alone does not fix individual points in the fibers.

At a point p of cone multiplicity m0, a preimage q of local degree e_q has cone multiplicity e_q*m0. Summing local degrees over the fiber gives d. Therefore

    sum_{q over p} m(q) = d*m0.

This also applies to a regular absorbing corner, m0=1: ramification simply multiplies the angle. Positivity and the assumed fixed-fiber inclusion give

    W(X/D4) >= 2 + d*(W0-2).

Thus full-corner-preserving covers of a 24-wall simple control have at least 24 walls for d=1 and at least 46 for d=2. Even a degree-two cover of the 22-wall contact control has bound 42, if the old wall identity and fixed-corner correspondence apply. This does not rule out arbitrary surface surgery, covers preserving only a sufficient subset of blockers, or non-equivariant quotient transfers.

## The sharper question is weighted blocking

Let C0 be a D4-invariant subset of old corner preimages that already intercepts every straight segment from the old source-lift set to the target-lift set. Preserving only its full fiber as new corners would suffice for darkness transfer. Set M(C0)=sum_{p in C0}m0(p). The same proof gives

    W >= 2 + d*M(C0)/4.

For W<=23, necessarily d*M(C0)<=84. A degree-two construction needs M(C0)<=42, compared with total fixed mass 88 on simple24 and 80 on contact22. Merely opening one or two corners cannot satisfy this route; a sufficiently small surviving blocking set must be proved first. The mass bound is necessary only. A cover still needs a compatible faithful D4 action, every required fixed fiber, and a simple injective planar development.

This changes the useful research target from vague surgery to a precise question: is there a proper invariant subset of corner lifts that still blocks all marked connections, with small enough mass to beat the wall budget? No such subset is established here.

## Awaiting Opus

The prompt asks Opus to challenge both the finite-orbit-invariant proposal and this covering inequality, then select one theory-first mechanism or state that none is ready. Its raw response and actual model identity will be inspected before reporting conclusions.

## Stronger independent cone-only obstruction (before Opus response)

A translation covering cannot erase a genuine cone: a point of multiplicity m0>=2 lifts to multiplicity e*m0>=2. Any simple faithful D4 quotient in our framework puts every genuine cone in Fix(rho). Thus all preimages of genuine base cones contribute to the new fixed mass automatically, without assuming full preservation of regular absorbing corners and even without equivariance of the cover with the quotient actions.

Let M_sing(X0)=sum of m0 over genuine cones. Then

    W >= ceil(2 + d*M_sing(X0)/4).

The audited simple24 cone list is 23 times m3 plus 2 times m5, so M_sing=79. For d>=2 this gives W>=42. Contact22 has 21 times m3 plus one m7, so M_sing=70, giving W>=37 at d=2. Slit20 has 4 times m2, 17 times m3, one m5, so M_sing=64, giving W>=34 at d=2, before its additional even-cone local gate is considered. New branching at regular points can only increase the cone contribution.

Consequently a genuine degree>=2 translation cover of any known control cannot produce a sub24 simple faithful D4 quotient, regardless of whether it preserves all regular blockers. The weighted-subset question alone cannot rescue this particular cover route. It may still inform surgeries that are not translation coverings, but those require a new darkness theorem. Degree-one maps reduce to isomorphisms and return to the existing refolding analysis when the mark-transfer hypotheses hold.

This argument assumes the same D4 quotient and cone/corner correspondence as the previous work. It is not an obstruction to all rational polygons, different derivative groups, maps to a different simpler base, or non-cover surgery.

## Why a quotient invariant needs a genuinely different base

A natural small certificate maps square indices by pi to a smaller pair of permutations, with pi r=r0 pi and pi u=u0 pi. This relation survives every Nielsen shear because it survives composition and inverse. If source/target and blockers project with the appropriate safety conditions, darkness downstairs certifies darkness upstairs for the entire shear orbit.

For connected origamis, such an equivariant square map is a square-tiled translation covering. Therefore a quotient certificate using one of the known control surfaces as its base inherits the cone-only wall obstruction above. Packaging that cover as an invariant does not evade its geometric cost. This observation narrows the next question: either find an auxiliary base with lower cone mass and a sufficient blocker pattern that lifts to real corners, or find a certificate that does not factor through a translation cover. Neither is supplied here. An abstract auxiliary base need not itself have a simple room quotient, so this is distinct from trying to improve an existing polygon by covering it.

## A separate scope gap in the peer research brief

The peer brief infers that n>=8 triangles cannot yield planar finite rooms because they do not tile the entire plane by reflections. That inference needs an additional theorem. A finite injective assembly does not require a global reflection tiling. For example, the right triangle (pi/8,3pi/8,pi/2) has a planar full A-star: sixteen reflected sectors form a regular octagon with C at side midpoints. This example fails the no-transparent-C condition, so it is not a dark-room construction. It does demonstrate why absence of an infinite tiling alone does not exclude finite assemblies satisfying additional constraints after modification.

The worthwhile question is whether the requirement that every B/C image remain a genuine corner prevents joining two full A-stars in *every finite injective patch* for these noncrystallographic triangles, or forces at least 24 walls. Neither the n=4 lattice model nor the n=6 enumeration proves that statement. Thus the claimed optimality across the entire generalized Tokarsky–Wolecki lemma framework should be restricted to the global reflection-tiling cases actually analyzed, unless this gap is closed.

This is a scope correction and a theory question, not evidence that a sub24 room exists for n=8.
