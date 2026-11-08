# Independent hand review: arithmetic rationality of dark endpoints

Reviewer Codex01a18403, 2026-11-06. Reviewed frozen peer `review/dark-endpoint-rationality.md`, SHA256 defb97e3eb4414ae61f855ffca08087a6b1c340f9e58bf6a0a02db22926f150b. Source unchanged.

Verdict: ACCEPT the mathematical argument, with the citation/version precision below. No uncapped W<=21 illumination theorem is inferred. This is an independent hand challenge of the arbitrary-degree proof, not finite computation, formal verification or external refereeing. Novelty is not assessed.

## Imported theorem scope personally checked

LMW, Everything is illuminated, journal Theorem2 and Theorem10 (arXiv v1 calls the latter Theorem11) supply a finite nonillumination decomposition into isolated points and connected affine correspondences, with finite-degree projection covers away from a finite set and nonzero real scalar derivative ratio. Journal Section2 explicitly allows labeled angle2pi marked singularities. They may be included in the forbidden set. Wolecki v3 Theorem1.2(i) supplies physical dark-pair finiteness for rational-angle polygons; Definition1.1, Lemma2.1 and Remark2.2 match corner-stopping billiards and the all-lifts connection criterion. These deep results are imported, not re-proved.

Bibliographic precision: the frozen peer text cites LMW Theorem11 while giving the JOURNAL PDF. The relevant journal statement is Theorem10, p1753 (PDF p17); arXiv1407.2975v1 uses Theorem11. The journal's projections cover the complement of a FINITE set, not necessarily every point. The peer argument already chooses loops away from finite exceptional points, so this does not change the mathematics. Preserve the freeze and record a supplement.

## 1. Integer torus cover and liftable shears

Independently derive the unfolding charts on each gamma*P copy. Every wall reflection is an integer affine signed permutation after common even scaling of polygon vertices. Across a glued mirror edge the linear part is removed by the gamma-copy chart, leaving an integer translation. Thus chart coordinates modulo Z^2 glue to a translation map pi:M->T^2. All physical corner lifts map to0. After removing the ENTIRE finite fiber over0, this is a finite ordinary covering of a once-punctured torus. Removing extra regular points here only constructs the maps; they are not newly forbidden in billiards.

A degree-D ordinary covering of the punctured torus is classified by a conjugacy class of a transitive permutation representation of its two-generator fundamental group in S_D. There are finitely many such classes. Each torus shear acts bijectively on this finite set, even if one works with outer automorphisms and changes basepoints. Some positive power stabilizes the class and therefore has a lift to the covering. Its local expression is the base shear plus integer chart translations, so it is affine of that exact derivative. The lift extends over every puncture: it sends a finite cyclic local cover of a punctured disk to another of the same degree. A further positive power fixes the finite completed fiber pointwise. This includes every regular/removable physical corner lift, so the PRECISE original forbidden set Sigma is fixed. Vertical shear follows separately. Neither lifted map has to descend to the polygon.

## 2. Permuting nonillumination components

The diagonal action h x h preserves the surface nonillumination locus because it maps straight segments and Sigma in both directions. Use maximal connected analytic two-dimensional components of the finite decomposition, not connected components of their entire topological union. Components of different scalar tangent slopes can only intersect discretely away from the finite exceptional fibers; two branches of the same slope that agree locally belong to the same maximal continuation. An affine image cannot switch between distinct analytic branches at an isolated intersection. Equivalently remove the finite exceptional/intersection points from a connected surface component, continue the same affine branch, and use the inverse map to get equality. Thus the finitely many maximal components are permuted. Truly isolated points are permuted too. Positive powers preserve any specified component or isolated pair.

For an isolated pair, powers of the horizontal and vertical lifts fix BOTH entries. Their torus images satisfy H^a z=z and V^b z=z with nonzero integers a,b. These imply az2 and bz1 integral, respectively. Every torus coordinate of both entries is rational. Integer-transition local charts then give rational developed coordinates.

## 3. Finite-degree holonomy forces lambda rational

Take a component F and remove the finite exceptional values of both projections. Choose a closed curve gamma in the first M coordinate with nonzero integer holonomy and missing those values. Such a curve exists: the punctured torus cover has finite index image in the base fundamental group, so positive powers of horizontal/vertical torus loops lift to closed M curves. Extra finitely many removed points can be avoided by local detours without changing holonomy.

Lift gamma to F. Since the first projection is a finite cover on that domain, some positive iterate gamma^q lifts to a CLOSED curve. Its two projected holonomies U,V are integral vectors, U!=0. The global scalar local derivative ratio implies V=lambda U. Any nonzero coordinate of U proves lambda rational. Neither primitive cover degree nor a bounded denominator was used. Negative lambda is harmless.

## 4. Rational torus constants and full local graphs

Write lambda=m/n, n>0,m!=0. The continuous torus-valued map n*pi(y)-m*pi(x) has zero derivative on F and is constant C. A positive power of the horizontal lift preserves F and gives H^a C=C, so C2 is rational mod1. The vertical lift gives C1 rational mod1. Integer-transition charts yield n*y-m*x=C+z for an integer vector z, hence rational affine equations.

A mere containment in those equations would be insufficient for the final rank argument. Here the finite-degree projection and local affine embedding make each regular branch an OPEN subset of its two-dimensional affine graph. At the particular nonsingular pair choose chart neighborhoods small enough to exclude exceptional endpoints and use the finite sheets. The locus is therefore locally a finite UNION OF FULL AFFINE GRAPH PATCHES, plus rational isolated points. This exact local equality closes the potential containment-versus-equality gap.

## 5. Actual endpoint sheets and rank argument

Choose disjoint small INTERIOR neighborhoods of distinct physical S,T. All their finitely many lift charts have expressions gamma*S+c and eta*T+d with signed permutation gamma,eta and integer c,d. A physical connection exists iff at least one lifted pair connects, so physical darkness is the INTERSECTION of every lifted-pair nonillumination condition. Each condition is locally the finite union of rational graph patches just proved (or rational isolated pairs). Distributing intersections over these finitely many unions produces rational affine solution patches in four real variables. All patch neighborhoods are open around the pair; there are no added portal, inequality or corner boundary constraints through these interior endpoints.

By Wolecki physical-pair finiteness, every nonempty patch through the dark pair must be zero-dimensional. Otherwise its open neighborhood contains infinitely many physical dark pairs. A zero-dimensional consistent rational linear system has a rational solution. Thus BOTH actual physical endpoints have rational coordinates. The inference uses ALL allowed lift pairs, not a chosen image of T or an affine symmetry of the physical room.

## Accepted consequence and exact remaining gaps

For a fixed rational-coordinate octilinear room, it suffices to illuminate all rational distinct interior pairs in order to illuminate all real distinct interior pairs. Combined with the separately accepted common-denominator scaling equivalence, a proof of the uncapped canonical45 W<=21 target WOULD prove all-real-endpoint illumination in all rational-coordinate octilinear <=21-wall rooms. The word WOULD matters: the uncapped target remains open, and this bridge does not lower k in any hypothetical dark room.

Irrational wall coordinates and other wall directions remain outside this proof. No rational density/closedness shortcut is used. No uniform reflection bound or effective bound on dark-point denominators is provided. This acceptance imports published deep dynamics theorems and remains an AI hand review, not a proof-assistant certificate or independent human referee verdict.
