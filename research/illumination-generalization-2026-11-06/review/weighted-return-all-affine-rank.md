# A marked all-affine obstruction to the same rho descent

Independent hand corollary extending WR01's pure-shear availability obstruction. No new room, discovery, direction list or engine. This is a constraint on a proposed repair with the SAME rank and SAME actual marked surface, not a rejection of all non-parabolic or weighted methods.

## Statement

For every n>=2, use the accepted square P_n=[0,B]^2, B=8n^2, actual S=(B/2,B/2), T=(B/2+2n,B/2+2). Let M=R^2/(2B Z^2), with complete physical endpoint fibers X,Y and forbidden corner marks Sigma as in WR01. Put w=(n,1) and rho(p,q)=|p|+|q|.

For ANY actual invertible affine automorphism F of M preserving X,Y,Sigma separately setwise, with derivative A, one has

    rho(Aw)>=n+1=rho(w).

This includes arbitrary parabolic/non-parabolic maps, orientation-reversing affine automorphisms and every finite composite with that complete marked-set preservation. There is no strictly decreasing move of this class at w. If equality holds, |(Aw)_1|=n and |(Aw)_2|=1. This states necessity of equality, not existence of every signed equality case.

## Independent all-direction arithmetic bound

Take any actual illuminating trajectory in the square, with primitive physical launch direction (p,q). Its developed actual target has coordinates

    (epsilon*(B/2+2n)+2B*i, delta*(B/2+2)+2B*j),

where epsilon,delta are independent signs and i,j arbitrary integers. Subtract S and divide by2 to get an integer displacement (U,V):

    U=epsilon*(2n^2+n)-2n^2+8n^2*i,
    V=delta*(2n^2+1)-2n^2+8n^2*j.

For EVERY such image, U=0 mod n and V=delta mod n. Parallelism gives qU=pV; reducing modulo n and using that delta is a unit modulo n gives p=0 mod n. A vertical ray p=0 cannot change the physical x coordinate to T_x; a horizontal ray q=0 cannot change y to T_y. Hence every illuminating primitive direction has

    |p|>=n, |q|>=1, rho(p,q)>=n+1.

This is an all-image necessary bound, not an assertion that all images define legal rays. The actual direct interior segment has displacement (2n,2), primitive direction w=(n,1) and rho=n+1, so the lower bound is attained. The argument proves the relevant rho minimum directly, rather than deriving an L1 minimum from a Euclidean-norm lower bound (which alone would be insufficient).

For an unfolded connection starting at ANY other member of X, refold in its physical copy. The derivative of that copy's projection is a diagonal sign matrix in the four-copy orthogonal unfolding. It preserves |p| and |q|. Thus the same lower bound applies to the primitive DEVELOPPED direction of every X-to-Y connection in M. No coordinate exchange, torus projection replacement or change of actual endpoints is assumed.

## Transfer to every marked affine automorphism

An affine automorphism of M has linear part A preserving its period lattice 2B Z^2, and its inverse preserves that lattice. Therefore A is in GL(2,Z), with determinant +1 or -1; in particular Aw is a nonzero primitive integer vector. The translation part has no effect on the direction.

The direct connection from a member of X to a member of Y avoids Sigma. Its image under F is one straight connection from X to Y and avoids Sigma because F is invertible and F(Sigma)=Sigma. This checks the entire original forbidden set, including the four regular physical corner lifts. Its developed primitive direction is Aw. Applying the established all-direction bound gives rho(Aw)>=n+1. If equality holds, the two individual absolute-value lower bounds force |(Aw)_1|=n and |(Aw)_2|=1.

The argument uses actual optical transport, not merely a generated transitive group or abstract direction reachability. It applies to composites only when their TOTAL map satisfies the stated actual endpoint and forbidden-set preservation. Intermediate states with differently transported markings require a different induction formulation; this lemma does not silently identify them with the original marked problem.

## Exact implication and boundary

WR01 established no decreasing pure horizontal/vertical shear. This corollary shows that replacing those moves by a more general affine automorphism of the SAME marked square cannot supply a strictly decreasing move for the SAME rho at this lit state. Even a proposed composite that is allowed to go uphill along the way cannot have a net rho decrease below n+1 when its final map preserves the original marked fibers and corners.

This does not reject non-parabolic maps in a different rank or terminal scheme. A convex-room terminal detects this already-lit square and needs no decreasing step. A rank on transported surfaces/markings, a room-changing reduction, a multi-part invariant or an induced tower may also evade this exact premise, but each needs its own transfer/availability/base proof. If only one direction orbit is reduced, a terminal may be dark even when some other orbit is lit; a classification still must force an illuminating orbit using the original r<=8 hypothesis.

No claim is made that all weighted ranks fail, that the full theorem is false, or that a dark counterexample has been found. This is a modest new rank-availability restriction derived from the accepted unbounded calibration, with all integer images, affine maps and n retained.
