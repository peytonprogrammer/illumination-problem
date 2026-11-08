# Candidate arithmetic bridge: dark endpoints are rational

Codex01a1a00f, 6 November 2026. NEW hand derivation within the persisted bounded effort. **CONDITIONAL pending peer review** of the derived argument. Published theorems are explicit dependencies, not re-proved here. No uncapped illumination theorem is assumed proved.

## Claim and consequence

Let P be a finite strictly simple polygon with rational vertex coordinates and walls in the four canonical directions. If distinct interior points S,T do not illuminate each other under ordinary corner-stopping billiards, then BOTH S,T have rational coordinates in that frame.

Consequently, proving illumination of every rational pair in each such polygon would imply illumination of every real interior pair in the SAME rational-coordinate polygon. Together with the accepted exact scaling equivalence, the uncapped canonical45 W<=21 target would then imply illumination of all real interior pairs in rational-coordinate octilinear rooms with W<=21. This does not change irrational wall coordinates or arbitrary wall directions. This is arithmetic locus rigidity, not approximation or closedness of illumination.

## External premises actually read

1. Lelièvre–Monteil–Weiss, *Everything is illuminated*, Theorem2 and Theorem11: on a translation surface the nonillumination locus is a finite union of isolated points and affine translation-surface correspondences. Each nonconstant correspondence projects with finite degree to either factor and has local scalar real slope lambda. Horizontal/vertical product components do not occur for zero blocking. The authors allow marked regular points among the forbidden singular set. We import this theorem and its deep prerequisites.
2. Wolecki, *Illumination in Rational Billiards*, arXiv1905.09358v3, Definition1.1, Lemma2.1 and Theorem1.2(i): actual physical nonilluminating pairs are finite in a rational-angle polygon; corner-stopping illumination equals existence of a geodesic between some allowed lifts. These are used exactly with distinct interior endpoints. We import finiteness; we do not infer rationality from finiteness alone.

Primary sources: [journal LMW](https://msp.org/gt/2016/20-3/gt-v20-n3-p11-s.pdf), [author LMW manuscript](https://www.math.tau.ac.il/~barakw/papers/illumination.pdf), [Wolecki v3](https://arxiv.org/html/1905.09358v3). The rational-coordinate consequences below are our derivation, not attributed to either source as a quoted theorem.

## 1. Arithmetic unfolding and two lifted shears

Scale the rational data once so every polygon vertex is even-even. Let M be the usual finite reflection unfolding, with every lift of a polygon corner in the forbidden set Sigma, including removable/regular corner lifts. The linear reflection group Gamma is a subgroup of signed permutation matrices. Use coordinates z=gamma*p on a disjoint copy of gamma*P; copies need not be embedded disjointly in one common plane to define charts. Along a wall, the two edge charts differ by an INTEGER translation: (2c,0) or (0,2c) for an integer axis line, and (c,c) or (c,-c) for an even-intercept diagonal line. Hence z mod Z^2 gives a finite translation cover

    pi:M -> T^2=R^2/Z^2

branched only over0, with every forbidden corner lift projecting to0. Area degree is finite. Deleting the entire finite fiber pi^{-1}(0) gives an ordinary finite covering of the punctured torus; this deletion is ONLY for constructing automorphisms, not an additional forbidden set in the billiard problem.

The base shears H(x,y)=(x+y,y) and V(x,y)=(x,y+x) fix0. A degree-D cover of a finitely generated fundamental group has only finitely many isomorphism classes: label its sheets and encode the two generators by permutations in S_D. Therefore a positive power of H stabilizes this cover's isomorphism class and lifts to a homeomorphism h with pi*h=H^r*pi. It extends over the finitely many missing points. A further positive power fixes each member of pi^{-1}(0). Locally it is affine with derivative H^L for some positive integer L. The analogous construction gives v with derivative V^K, K>0. They preserve Sigma pointwise, even if some corner lifts are regular. No change of physical mirrors or descent of these maps to P is claimed.

Equivalently, these maps can be built as full twists in the finite horizontal/vertical cylinder decompositions. The covering argument avoids assuming the physical source and target fibers coalesce under a shear.

## 2. Arithmetic of every surface correspondence

Let N_M be the nonillumination locus on M, with precisely Sigma forbidden. The maps h*h and v*v preserve N_M, since invertible affine maps preserve straight geodesics and the forbidden set. The imported finite decomposition has finitely many maximal connected2D affine components and isolated0D points. Affine maps permute these components. A connected analytic component cannot switch between finitely many other components across their discrete intersections; apply the inverse map to get equality. Isolated points are permuted as well.

First consider an isolated pair(x,y). Some positive power of h*h fixes it. Since pi*h=H^L*pi, each torus coordinate z=(z1,z2) of x and y satisfies an equation a*z2=0 modulo1 for a nonzero integer a. A suitable power of v*v similarly gives b*z1=0 modulo1. All coordinates of both torus points are rational. In the chosen integer-transition charts this means rational coordinates on M.

Now take a connected correspondence F, locally y=lambda*x+c, with lambda a nonzero real scalar. We must prove lambda rational rather than merely using the published weaker lambda^2 rational assertion. The first projection F->M has finite degree. Choose a closed curve in M with nonzero integral holonomy u; such a curve exists because pi is a finite torus cover. After a positive iterate it lifts to a closed curve in F. Its first-coordinate holonomy is a nonzero integer vector U and its second-coordinate holonomy is lambda*U, also an integer vector. A nonzero coordinate of U gives lambda as a ratio of integers. This reasoning works on the punctured covers and their finite completions, so loops can avoid every branch/marked point.

Write lambda=m/n with integers n>0,m!=0. On connected F,

    C = n*pi(y)-m*pi(x) in T^2

has derivative zero and hence is constant. A positive power of h*h preserves F, so H^a*C=C for a nonzero integer a. Thus C2 is rational modulo1. Similarly a power of v*v gives C1 rational modulo1. Every local branch of F therefore has rational affine equations

    n*y-m*x=C+z,   z in Z^2.

Only finitely many local branches occur around a nonsingular pair, because both projections have finite degree. This proves that N_M is LOCALLY a finite union of rational affine subspaces and rational isolated points. The maps h,v need not preserve a physical mark fiber: only their action on the surface-locus components is used here.

## 3. Return to all physical lifts

Take a distinct interior dark pair(S,T) and small interior coordinate neighborhoods avoiding the diagonal. There are finitely many polygon lifts, each with local coordinates gamma*S and eta*T plus INTEGER chart translations, gamma,eta in Gamma. The unfolding equivalence says a pair is physically dark exactly when EVERY pair of its lifts belongs to N_M.

By step2 each such local condition is a finite union of rational affine equations in the four real coordinates(S1,S2,T1,T2). There are finitely many lift pairs, so distribute these finite unions through their intersection. Locally the physical dark set is a finite union of rational affine solution spaces intersected with the open neighborhoods. This step uses all copies; no selected-target-fiber assumption is hidden.

The imported physical-pair finiteness theorem makes this local set finite. Any positive-dimensional affine solution space through(S,T) would have infinitely many points in its open neighborhood. Thus every solution space containing the pair is zero-dimensional. A consistent zero-dimensional rational linear system has a rational unique solution. Both endpoints are rational, as claimed.

## Hostile cases and exact boundaries

- A square torus may have no dark pairs. Then the claim is vacuous, and no positive-dimensional component needs to exist.
- Marked regular corner lifts are kept forbidden and fixed by the chosen powers; transparent interior lattice vertices are not added to Sigma.
- Nontrivial torus-cover degree, rational slope denominators, multiple correspondence branches, component intersections and negative lambda are all retained.
- The image surface maps are NOT claimed to be physical affine symmetries of the polygon. Such a claim would fail the independently proved mirror-rigidity test.
- Finiteness alone does not force rationality. Rational local equations were proved first using arithmetic cover automorphisms and finite correspondence decomposition.
- The resulting rationality theorem says nothing about W<=21 illumination until the uncapped canonical target is proved; it only removes the endpoint-arithmetic gap conditional on that target.
- Arbitrary irrational wall coordinates lack the integer torus cover and are outside this argument. Arbitrary slopes lack the signed-permutation arithmetic unfolding in this proof.

## Review obligations

CONDITIONAL: independently check finite-cover shear lifting with regular corner marks, permutation of maximal correspondence components, finite-degree period lifting, conversion from global torus constants to local rational equations, and exact ALL-fiber intersection before invoking physical finiteness. The external LMW/Wolecki theorems remain cited imported dependencies. No finite computation can replace them or the arbitrary-degree hand argument. No final acceptance is asserted before the peer challenge is reconciled.
