# Independent audit of the absolute-homology route obstruction

Decision: ACCEPT all five requested claims, at their stated algebraic scope. The entire genuine affine-group norm bound is UNRESOLVED. The packet constructs symplectic lattice actions, not affine maps or a marked-cover realization.

Source read in full: author/argument.md, SHA256 03ac5e76d92e8d61a470c647ae45a2d455058e6b632c6470a959a033cf1602ac. The request, attempt ledger and route assessment were also read in full. No author checker or numerical run was used. The source pin is checked before and after this hand audit.

## 1. Primitive period sublattice and degree pairing — ACCEPT

Write f=pi_*:H_1(M,Z)->Z^2. Surjectivity splits this map as a map of free abelian groups. Its dual inclusion pi^*:Z^2->H^1(M,Z) therefore has a free cokernel. Thus E=pi^*H^1(T,Z) is a primitive rank-two sublattice, not merely a rational subspace or a finite-index image in a larger primitive lattice.

For a positive integral torus basis a,b with pairing1, naturality gives

    <pi^*a,pi^*b>_M = degree(pi)*<a,b>_T = N.

Hence E has alternating form NJ. The branching does not alter the topological degree identity. The integral cup pairing on the closed genus-two surface is unimodular of rank4, so the rank-two orthogonal complement K is nondegenerate. It is primitive: an integral vector whose nonzero integer multiple pairs trivially with E also pairs trivially with E.

## 2. Complement scale and full graph gluing — ACCEPT

I independently recover the complement scale without assuming the desired discriminant identification. Choose an oriented basis of K in which its form is kJ with k>0, and set I=[H:E direct-sum K]. The determinant formula for full-rank integral sublattices in the unimodular H gives

    I^2=N^2*k^2, hence I=Nk.

Every x in H splits rationally as e+kappa with e in E^*, kappa in K^*, because its integral pairings with E and K put the components in those dual lattices. Thus H/(E direct-sum K) embeds into D(E) direct-sum D(K).

Projection to D(E) is injective: if e is integral, subtract it from x; the remainder is in H intersect K_R=K. The analogous argument uses H intersect E_R=E, which is exactly primitivity of E. Therefore

    Nk=I<=|D(E)|=N^2,
    Nk=I<=|D(K)|=k^2.

These inequalities force k=N and I=N^2. Both projections are bijections, so the gluing subgroup is the FULL graph of an isomorphism phi:D(E)->D(K). Integrality of the pairing of any two elements of H gives opposite pairings on the two components modulo Z: phi is an anti-isometry. Conversely the graph recovers H as its full inverse image in E^* direct-sum K^*, by the index calculation. Consequently a compatible symplectic block action preserves the actual integral H, not just its rationalization.

This verifies the author's graph assertion including the crucial onto projections and sufficiency of graph preservation.

## 3. Every determinant-one torus action lifts algebraically — ACCEPT

Let C^* be the torus cohomology action. It has determinant1 and preserves NJ on E. Its induced alpha on D(E) is symplectic. Conjugating by an anti-isometry on both sides makes beta=phi alpha phi^{-1} symplectic on D(K). In a basis of K with form NJ, its discriminant module is (Z/N)^2 with the alternating form scaled by1/N. A rank-two matrix preserves this form exactly when its determinant is1 modulo N. Thus beta belongs to SL(2,Z/N), including composite N.

The proposed lifting of SL(2,Z/N) is valid. Choose a nonzero integer lift c of the desired first-column lower entry. For every prime dividing c and N, the desired unimodular column guarantees that the upper residue a0 is nonzero modulo that prime. For the finitely many prime divisors of c not dividing N, choose the parameter in a=a0+kN to avoid divisibility; Chinese remainders do this simultaneously. Then gcd(a,c)=1. Bezout extends this column to an integral determinant-one matrix.

After reduction, its second column and the desired one differ by a multiple of the first: express their difference in the obtained invertible basis over Z/N, and the determinant equality forces its second coefficient to vanish. Adding the required integer multiple of column1 to column2 therefore gives the requested lift. N=1 is immediate. No assumption about a prime modulus or integer invertibility of one nominated entry is needed.

Choose the resulting B on K lifting beta. The block action (C^*,B) preserves both alternating forms and their gluing graph, hence defines an integral symplectic automorphism A of H^1(M,Z). Its dual Q on H_1(M,Z) satisfies Q^*=A. For every torus cohomology class ell and homology cycle z,

    ell(pi_*Qz) = (pi^*ell)(Qz)
                 = (A pi^*ell)(z)
                 = (pi^* C^*ell)(z)
                 = ell(C pi_*z).

Thus pi_*Q=C pi_* with the correct covariance; there is no inverse or transpose error hidden by dualization.

## 4. Application and exact shortening control — ACCEPT

The normalized L area is

    (2d+1)d + d((2d+1)-d) = 3d^2+2d.

The four-copy area is four times this value and the period torus has area4, so N=d(3d+2). The accepted exact period lattice2Z^2 makes pi_* onto. The sole order-two zero/cone has genus2 by the translation-surface Euler relation.

For the already prescribed C=[[0,-1],[1,2]], direct multiplication gives Cv=(1-d,d-2), determinant C=1, and norm2d-3 for d>=3. The new algebraic lemma supplies a symplectic period-compatible lift of this C for EVERY assigned d. Its actual affine realization remains excluded by the accepted COMPLETE antidiagonal stabilizer, whose admissible coefficient is a multiple of (4d+1)(3d+1)/2, not the unit coefficient of C.

This is an exact countercontrol to absolute-homology/period sufficiency. It is not a new matrix search or an admissible norm-reducing affine F.

## 5. Quantifiers and unresolved global bound — ACCEPT

The lemma is quantified over every C in SL(2,Z), so its scope is a complete algebraic obstruction to the proposed weaker proof route. It does not classify or enlarge the realized affine derivative group. Marked covering monodromy, pointwise flat-coordinate compatibility, corner/separatrix action, actual endpoint fibers and the relative path gamma are absent from its hypotheses.

Therefore neither an abstract lift nor its possible topological realization can be promoted to an affine realization. The packet supplies neither the lower bound for all genuine F nor a genuine shortening F. The fixed-gamma and broader illumination questions remain open, and no darkness follows. No material correction is required.
