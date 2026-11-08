# Intrinsic arithmetic bridge for four-direction rooms

Candidate exact hand proof for independent review. This specializes an existing published torus-cover classification; it is not a novelty claim. Its illumination consequence is conditional on the still-open uncapped canonical45 theorem.

## 1. Exact classification

Let P be any finite strictly simple polygon, with redundant straight vertices removed, whose wall directions lie in one rotated copy of the four canonical directions. Use the MINIMAL connected reflection unfolding M, with q=2N copies, where the orientation-preserving rotation subgroup has order N.

- If P has exactly two perpendicular unoriented wall directions, N=2. Its unfolding covers a flat torus if and only if, in the orthonormal wall frame, the horizontal vertex spacing module and the vertical vertex spacing module each have rational rank one. The two units need not be commensurable with each other.
- Otherwise N=4. Its unfolding covers a flat torus if and only if a similarity sends all vertices to rational coordinates in a canonical-direction frame. Consequently a further even-denominator scaling makes it a canonical45 triangle disk.

No wall-count, degree, size, or exception bound is required for this classification. Every genuine polygon corner, including a regular lift of an acute or right-angle corner, is retained in the argument. There are no holes, slits, contacts, or straight-angle corner marks.

## 2. Absolute periods and the rotation action

Suppose M covers a flat torus by a translation map. Its absolute period group Lambda is a discrete rank-two lattice: it is a subgroup of the target torus lattice and contains a finite-index subgroup, since a positive multiple of each base loop lifts to a closed loop on the finite cover. Equivalently integrate the translation form from a fixed basepoint modulo all absolute periods to obtain

    f:M -> R^2/Lambda.

The canonical deck rotation T of order N has derivative R, with R=-I for N=2 and R a quarter-turn for N=4. It preserves the period lattice: R Lambda=Lambda, because it acts bijectively on closed curves and multiplies their holonomies by R.

There is a genuine corner lift p0 fixed by T. For N=2, each corner has interior angle pi/2 or 3pi/2 and each has a unique lift under the rotation action. For N=4, write each corner angle m_i*pi/4. If every m_i were even, every consecutive wall direction would differ by an even number of eighth-turns, so all wall directions would lie in just two perpendicular lines and the minimal N would instead be2. Thus some m_i is odd; this corner has one lift and is fixed by T. Choose this p0 as the integration origin. Then

    f(Tp)=R f(p).

The corner-lift count used here can be seen by gluing the sectors at that vertex: a corner of angle m*pi/N in lowest denominator N/gcd(m,N) has gcd(m,N) distinct lifts in the q-copy unfolding. T cycles those lifts, so its gcd(m,N)-th power fixes each of them. These include the regular lifts when the reduced numerator is one.

## 3. Every actual corner has a half-lattice coordinate

For N=2 every corner lift p satisfies Tp=p, so 2f(p)=0 in the period torus. Thus f(p) belongs to (1/2)Lambda modulo Lambda.

For N=4, a nonstraight genuine corner has m in {1,2,3,5,6,7}. If m is odd, Tp=p and (I-R)f(p)=0 modulo Lambda. Since (I+R)(I-R)=2I, this gives 2f(p)=0 modulo Lambda. If m is even, m is2 or6, and T^2p=p; since R^2=-I this again gives 2f(p)=0. The excluded straight angle m=4 is exactly where this stabilizer argument would fail.

It follows that the holonomy of any path between actual corner lifts belongs to (1/2)Lambda: its value modulo Lambda is the difference of the endpoint torus coordinates. In particular, following boundary edges in a selected polygon copy shows that every original vertex displacement from its chosen base vertex lies in (1/2)Lambda. Integration across a zero at an endpoint is well-defined, so this does not assume that light may pass through a corner.

## 4. Quarter-turn case: the lattice is square

Let w be a shortest nonzero vector of the discrete lattice Lambda. In the N=4 case, Rw is also in Lambda. The inclusion w Z[i] subset Lambda follows by addition and quarter-turn invariance, identifying the plane with C.

For any z in Lambda, write z/w=x+iy. Choose integers a,b nearest to x,y. The residue z-(a+ib)w belongs to Lambda and has norm at most |w|/sqrt(2), strictly less than |w|. Minimality forces this residue to be zero. Hence

    Lambda = w Z[i].

The similarity z->z/w makes every vertex displacement a half-Gaussian integer. A chosen nonzero wall edge e in these coordinates is a nonzero element of Q(i). Multiplying once more by 1/e is a similarity with rational real and imaginary parts. It keeps all vertex coordinates rational and makes this wall horizontal. Every other wall direction remains an integer multiple of pi/4 from it. This proves the necessary similarity-rational form in section1.

Conversely, rational vertices in a canonical-direction frame can be scaled to even-even vertices. The reflected edge gluing translations are integral, so developing modulo Z^2 gives a finite translation torus cover. This is the already accepted arithmetic-unfolding construction, and a similarity preserves the torus-cover property.

## 5. Half-turn case: independent axis units suffice

Choose a nonzero horizontal edge u and a nonzero vertical edge v of the polygon. Both exist for a bounded orthogonal polygon of positive area. Section3 gives 2u,2v in Lambda. These are independent lattice vectors, so they generate a finite-index sublattice. Therefore every vector in Lambda is a rational linear combination of u and v. Every vertex displacement, belonging to (1/2)Lambda, has rational coefficients in this perpendicular basis.

Scaling the horizontal and vertical axes independently by the lengths of u and v makes all vertices rational. The spacing-rank-one criterion in orthogonal-affine-bridge.md follows, including necessity in this intrinsic torus-cover formulation. The chosen axis normalization preserves ordinary specular reflections and all actual marked paths in both directions.

Conversely that criterion gives a rational-coordinate orthogonal room after a reflection-preserving diagonal map. Its unfolding is a torus cover; applying the inverse diagonal linear map takes the torus lattice to another flat torus lattice and preserves the covering property. This is a geometric property of the translation surface, independent of whether the period torus is square in the original Euclidean metric.

## 6. Conditional all-real endpoint coverage

Assume the uncapped W<=21 canonical45 all-interior-A illumination theorem. Every four-direction W<=21 room whose unfolding is a torus cover can be transformed to rational walls by section4 or5, by a similarity or a reflection-preserving independent-axis map respectively.

If there were an actual distinct real interior dark pair, its image would remain dark. The accepted arithmetic endpoint theorem, with its bibliographic supplement, makes both normalized endpoints rational. A common even-denominator similarity of that same room and pair would give a canonical45 W<=21 disk with a dark interior A pair, a contradiction. Thus the hypothesized uncapped theorem would cover EVERY real interior pair in EVERY torus-covered four-direction W<=21 room.

This identifies the broad real-wall bridge that is already available conditional on the main theorem. The additional four-direction wall class still requiring a new optical argument consists precisely of the NON-torus-covered unfoldings. The classification does not show that this class has a dark pair or that it fully illuminates. It does not transfer to other wall directions, and the k<=6 baseline cannot replace the uncapped premise.

## 7. Published comparison and review targets

Apisa-Wright, Marked points on translation surfaces, arXiv1708.03411v3, Proposition3.11 proves the general rational-polygon torus-cover classification into Gaussian, Eisenstein, and rectangle-tiled cases. The proof explicitly includes removable corner lifts when comparing relative and absolute periods. The argument here independently specializes the four-direction cases using fixed corner stabilizers and a shortest-vector lattice proof. [Primary text](https://arxiv.org/html/1708.03411v3#S3.Thmthm11).

Review all of: minimal connected unfolding, existence of a T-fixed corner, every other corner's stabilizer, rank-two discreteness of the absolute periods, origin choice and descended rotation, relative corner periods, square-lattice proof and final wall-frame adjustment, independent-axis case, actual marks and endpoint transfer. Neither the deep arithmetic endpoint theorem nor the uncapped illumination theorem is re-proved by this classification.
