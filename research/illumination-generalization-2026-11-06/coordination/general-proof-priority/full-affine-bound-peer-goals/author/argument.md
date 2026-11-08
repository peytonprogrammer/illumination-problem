# Absolute homology alone cannot prove the affine norm bound

## Scope and verdict

The proposed realized-affine minimum remains OPEN. This note proves an obstruction to one proof route: the full integral symplectic absolute-homology/period constraints admit EVERY determinant-one torus matrix. In particular they admit an abstract shortening action that is known NOT to be a genuine affine map.

This is not a shortening affine automorphism, nor a refutation of the proposed norm bound. It does not assume a generating set for the actual affine group. No directions, matrices, rooms or orbits are enumerated.

## Quantified homological lifting lemma

Let M be a closed genus-two oriented surface with a translation covering pi:M->R²/(2Z²) of degree N. Suppose pi_*:H_1(M,Z)->H_1(T²,Z) is onto. Then for EVERY C in SL(2,Z) there is an integral symplectic automorphism Q of H_1(M,Z) such that

    pi_* Q = C pi_*.

Q is a lattice automorphism only. No affine, marked, or even covering-equivariant surface homeomorphism is asserted.

Proof. Work first on the unimodular rank-four cohomology lattice H with its cup-product pairing. E=pi^*H^1(T²,Z) is primitive: pi_* is onto, so its dual inclusion has torsion-free cokernel. In a positively oriented torus basis the restriction to E has matrix N J, where J=[[0,1],[-1,0]], by degree.

Let K=E-perpendicular in H. It is primitive, rank two and nondegenerate. Unimodularity and primitivity identify the discriminant groups D(E)=E*/E and D(K)=K*/K by an anti-isometry phi of their induced alternating pairings. Both have order N² and are isomorphic to (Z/N)². Consequently, after choosing an orientation, K has pairing N J as well.

Here is the gluing assertion used explicitly. The integral lattice H lies between E direct-sum K and E* direct-sum K*. Its image in D(E) direct-sum D(K) is the graph of phi. Projection of that subgroup to either discriminant group is injective by primitivity of the complementary lattice; unimodularity makes its order N², so both projections are onto. Pairing integrality makes phi an anti-isometry. Thus preserving that graph is sufficient and necessary to preserve H.

The desired action on E is the pullback C^*. It is a determinant-one automorphism, hence preserves N J and induces alpha on D(E). Choose a determinant-one integral automorphism B of K inducing phi alpha phi^-1 on D(K). Such B exists because reduction SL(2,Z)->SL(2,Z/N) is onto. The block action (C^*,B) preserves the graph and the alternating pairing. It therefore extends to an integral symplectic automorphism of H. Dualizing yields Q with the displayed period covariance.

For completeness, reduction surjectivity does not require a numerical group computation. For a unimodular first column (a0,c0) modulo N, choose a nonzero lift c of c0. Choose a=a0+kN coprime to c: primes dividing both c and N already cannot divide a0, and the finitely many remaining primes dividing c can be avoided by Chinese remainder choices of k. Extend (a,c) to an integral determinant-one matrix by Bezout. Modulo N its desired second column differs from the obtained one by a multiple of the first, since both have determinant one. Add that multiple of the first column to the second. This lifts the prescribed matrix. N=1 is immediate.

This proves the lemma for every C, with no enumeration.

## Application to the assigned L family

The accepted period lattice is exactly 2Z², so pi_* is onto. There is one order-two cone, hence genus two. The four-copy area divided by the torus area 4 gives

    N=area(P)=d(3d+2).

For the already prescribed ambient matrix

    C=[[0,-1],[1,2]],

the lifting lemma therefore supplies an integral symplectic period-compatible action for every assigned d. Its effect on v=(-d,d-1) is

    C v=(1-d,d-2),
    |Cv|_1=2d-3 < 2d-1.

But the accepted complete antidiagonal-stabilizer theorem rules out ANY genuine affine realization of this exact C: its unit unipotent coefficient is not a multiple of (4d+1)(3d+1)/2.

Thus the homological constraints pass a lowering action which actual gluing forbids. They cannot, by themselves, imply the desired minimum. This is a universal algebraic limitation, rather than another selected-direction exclusion or candidate affine construction.

## Limits and the still missing implication

The lemma does NOT preserve the marked corner set, the complete covering monodromy, cylinder phases, a relative-homology representative of gamma, or its exact endpoint action. It is therefore not a counterexample to any claim using those additional physical data.

In particular: an abstract symplectic lift cannot be promoted to a genuine affine map. Even a topological realization would not supply that promotion. The actual full-group minimum still needs a geometric or marked-cover restriction that excludes ALL shortening derivatives, or a genuine shortening map. This note supplies neither.

The original gamma, exact F(ORIGINAL Rxq), smooth-wall seed allowance, all frozen sources, accounting and clocks remain unchanged. No numerical check, search, engine, worker or git mutation was used.
