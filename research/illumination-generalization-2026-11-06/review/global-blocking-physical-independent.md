# Independent physical-quotient check for the Heisenberg control

This independently verifies the author's proposed B04 exclusion by a shorter period-map argument. Full frozen author application read and reconciled against hash e56eda41f70f9353c8835b4eb279741f2bd9c52dfb75bd6a3cadcb6ce0f1786e. ACCEPT this exact application; no new general rigidity is claimed. The abstract R60 positive-slope dark graph remains unchanged; it is not a qualifying physical counterexample.

## Explicit period map

For the R60 square labeled(a,b,c), define

```
F(a,b,c;xi,eta)=(a+xi,b+eta) mod3Z².
```

Right gluing sends a to a+1 and top gluing b to b+1, so this expression agrees pointwise on every glued edge. It is a translation map to the3-by3 torus. Above any open unit square of that torus there are the three c sheets, hence degree3. Its nine branch values are exactly the nine integer points mod3; each has ONE true cone point above it, of local degree3. The other cover to the unit torus has degree27; these degrees must be distinguished.

Every absolute period belongs to3Z² because F is globally well defined. Conversely a horizontal loop with right monodromy r³ and a vertical loop with up monodromy u³ close and avoid branch points at a suitable noninteger basepoint. Their periods are(3,0),(0,3). Thus the absolute-period lattice is exactly3Z², so F is the primitive period quotient. This also follows from the abelianization obstruction for closed lifts, with loops perturbed off the finite zero set if necessary.

## Any derivative-minus-identity map fixes exactly one zero

Let f be ANY global affine automorphism of this surface with derivative-I. The map F∘f+F to the3-by3 torus has derivative0 on the connected regular surface, hence is a constant c. Continuity extends the identity to the zeros. Since f permutes zeros and F maps them bijectively to F3², c belongs to that nine-point set. Its action on zero images is

```
w -> -w+c  in F3².
```

Multiplication by2 is invertible mod3, so this action has EXACTLY ONE fixed point. Therefore f fixes exactly one of the nine genuine zeros. No assertion that f exists is needed for the obstruction; if one exists, it has this fixed-zero count. No proof of the full translation automorphism group, prong saturation or normalization is necessary.

Every canonical45 physical unfolding has its intrinsic physical half-turn rho with derivative-I fixing EVERY genuine corner lift, hence EVERY true zero, as independently accepted in half-turn-quotient.md. Such a rho would fix all nine zeros here, contradicting the count. Thus the Heisenberg surface cannot be the minimal canonical45 disk unfolding, at ANY wall count. The argument is unchanged under a simultaneous affine deformation of the surface: -I is central and the zero-fixed-point count is invariant under conjugacy.

## Prior-work and scope

This is an explicit application of already accepted torus-cover-bridge.md section3: corner images lie in a single half-lattice coset on the period torus, hence have at most four values. The nine branch values here violate that criterion. It is NOT a new general physical rigidity theorem or a W21 lower bound.

An alternate check uses tau's order-three quotient. A putative rho fixes zeros and locally commutes with tau at a6pi cone, hence globally. The quotient by tau is the degree-three torus with nine distinct branch images; descended rho has derivative-I and would fix all nine images, whereas such a torus affine map has exactly four fixed points. The explicit F argument is simpler and avoids invoking this alternate route.

The lesson is precise: generic translation-surface counterexamples must pass the planar physical-quotient constraints. Excluding this control does not classify the possible zero-blocking components of actual canonical45 unfoldings, nor supply the full q-by-q endpoint constraint needed for the universal theorem. No new room, ray search or state engine was run.

Own exact primitive-map checks use the frozen R60 right/up permutations to verify162 seam coordinate controls, the three sheets over each regular primitive-torus unit cell, nine distinct zero images, and all nine affine-negation actions. Each fixes exactly one zero. No author checker or new discovery was executed.
