# WR01: exact weighted affine transfer, partial descent, and its availability obstruction

Hand proof for arbitrary degree and unbounded integer weights. No engine, discovery search, sample scan or new reflection cutoff. WR01 is a scoped induction-step test; the full r<=8 illumination goal remains open.

## 1. Actual marked object and constructed maps

Let M be the connected orthogonal reflection unfolding of the original integral room. Its ordinary unit-square presentation has right and up permutations h,v. Let Z0 be the ENTIRE finite fiber above the origin of the unit torus. The actual source fiber X, actual target fiber Y and physical corner lifts Sigma are separate subsets of Z0. Sigma includes regular/removable physical corner lifts, following the unpurified direction-skeleton convention. Other regular vertices of Z0 remain transparent.

Set L_h=lcm(lengths of all cycles of h), and L_v=lcm(lengths of all cycles of v). These are positive integers depending on the complete original surface; no bound in W or r is asserted.

Each h cycle of length c is an open horizontal row cylinder R/cZ x (0,1). On its closure define

    F_h(x,y)=(x+L_h*y,y),   x modulo c.

It is the identity on the bottom circle, and on the top circle because c divides L_h. Thus these formulas agree under EVERY top/bottom edge gluing, pointwise on the boundary edges. They also respect each vertical side pairing inside the cycle. Across a regular edge their linear parts agree, so in the translation charts they define one affine surface map with derivative H^{L_h}. The inverse is the same construction with -L_h. At every vertex the continuous cylinder-boundary values fix the vertex, and the map and its inverse extend across the finite cone stars. Therefore this is a genuine affine homeomorphism of M, fixing Z0 pointwise. This construction is valid even when a cylinder boundary was artificially introduced along a regular grid edge. It neither assumes a new physical room nor assumes the affine map descends to the original polygon.

The vertical cylinder construction similarly gives F_v with derivative V^{L_v}, fixing Z0 pointwise. In particular both maps, and all their powers, preserve X, Y and Sigma pointwise. Their inverse forbidden sets satisfy F_h^{-1}(Sigma)=Sigma and F_v^{-1}(Sigma)=Sigma. They also preserve the true cone zeros and distinguish them from transparent and forbidden regular vertices.

## 2. Whole-trajectory transfer and all return weights

Choose primitive w=(p,q). For a complete straight path gamma(t) in direction w, the image F_h^{-k} gamma(t) is a single straight path in direction

    w'=(p-k L_h q,q).

It is NOT a path obtained by concatenating flow in different directions. The map acts on the whole surface and the entire trajectory at once. Since the derivative is in SL2Z, w' remains primitive.

For the marked first-return skeleton with Xi=Sigma union X union Y, each edge of duration ell satisfies gamma(0),gamma(ell) in Xi with no Xi event at intermediate t. Its image has EXACTLY the same first-return duration ell: an intermediate Xi encounter would pull back to an intermediate Xi encounter because F_h^{-k} fixes Xi and is invertible. Incoming/outgoing prongs are transported by the actual local map. All unbounded positive integer durations ell, loops, intermediate transparent fiber vertices and multiplicities are retained. Physical wall reflection counts, seam words and individual physical wall-hit domains need not be preserved and are not used as return weights here. They must not be copied from the preimage itinerary; refolding the mapped straight segment supplies its own physical first-wall sequence.

The event-resolved FIRST-Xi domains transport by this homeomorphism: interiors avoiding Sigma remain so, endpoint labels remain actual X and Y, and no target is replaced by its torus projection. This statement describes mapped ORIGINAL trajectories, not arbitrary invented data with the same graph. Refolding a finite straight X-to-Y segment in M gives a legal original-room billiard path by the accepted unfolding equivalence. A seam-tangent path starting at an actual interior mark cannot appear without a forbidden polygon-corner encounter. Hence an illuminating edge/path in the moved direction pulls back to an illuminating edge/path in the original direction, and conversely.

The same proof gives w'=(p,q-k L_v p) under F_v^{-k}. This is an exact all-word optical equivalence for the specified actual maps. It is separate from (a) inducing a section of the SAME directional flow, and (b) merely changing a direction on a fixed surface without a transport map. No claim about arbitrary H or V generators is made.

## 3. A partial well-founded rank

Use rho(w)=|p|+|q|, a positive integer. A horizontal move decreases rho exactly when

    |p-k L_h q| < |p|.

For nonzero p,q, some nonzero integer k satisfies this iff

    2|p| > L_h |q|.

Necessity: the nearest nonzero lattice multiple has magnitude at least L_h|q|; if this is at least 2|p|, subtraction cannot reduce |p|. Sufficiency: subtract one multiple toward p, or use the nearest integer multiple; the strict inequality supplies a decrease. At equality the best nonzero step ties rather than decreases. The vertical condition is 2|q|>L_v|p|. Every accepted step strictly lowers rho, so any sequence of accepted steps terminates. All integer edge durations ell survive unchanged; they have not been discarded, bounded, or falsely claimed to decrease.

This proves TRANSFER and PARTIAL DESCENT only. It does not prove that a decreasing step exists outside axes, that a terminal direction is illuminating, or that r<=8 forces either fact. It also does not change the physical room or its reflex count.

## 4. Exact unbounded obstruction, allowing every fiber-preserving pure shear

Use the mandated P_n square calibration, n>=2. Write B=8n^2. The usual four-copy reflection unfolding is the flat torus R^2/(2B Z)^2. The actual lift sets are

    X={ (+/-B/2,+/-B/2) },
    Y={ (+/-(B/2+2n),+/-(B/2+2)) },
    Sigma={0,B} x {0,B},

all coordinates modulo 2B. Both signs vary independently. The direct segment from actual S to actual T is interior and has primitive direction (n,1). Thus this direction illuminates. The square has r=0, W=4.

We now permit MORE freedom than the constructed cycle-lcm twists: ANY affine torus homeomorphism with horizontal unipotent derivative H^lambda and ANY translation that preserves X,Y,Sigma SETWISE. Because the torus period lattice is (2B Z)^2, lambda is an integer. Write

    F(x,y)=(x+lambda*y+c_x, y+c_y).

A translation preserving a two-point subset of a circle is either zero, or the half-period translation when those two points are antipodal. The two y coordinates of Y, +/-Y0 with Y0=B/2+2, are not antipodal: their difference is B+4, neither B nor0 modulo2B. Thus c_y=0. Likewise the two x coordinates +/-X0, X0=B/2+2n, are not antipodal. In each fixed Y row the horizontal shift must therefore be zero modulo2B:

    lambda*Y0+c_x = 0 mod 2B,
    -lambda*Y0+c_x = 0 mod 2B.

Subtracting gives lambda*(B+4)=0 mod2B. Since

    gcd(B+4,2B)=4,

lambda must be a multiple of 4n^2. These necessary conditions do not rely on Sigma or on source invariance, so adding those restrictions cannot lower this bound. It is attained: for lambda any multiple of4n^2 choose c_x=-lambda*Y0. Then c_x is0modB, the X rows are shifted by -2lambda modulo2B, a multiple of B, and Sigma is preserved. Thus these are exactly the possible derivative coefficients for the full setwise requirement.

By the coordinate-swapped calculation, a vertical shear with derivative V^mu preserving these actual fibers setwise must have

    mu*(B+4n)=0 mod2B,
    gcd(B+4n,2B)=4n,

so mu is a multiple of4n. The bound is again attained by c_y=-mu*X0. Here X and Y exchange coordinate ROLES in the calculation, not the actual endpoints or their labels.

Consequently at the illuminated direction (n,1), every nonidentity permitted horizontal shear has

    |n+lambda| >= 4n^2-n > n,

and every nonidentity permitted vertical shear has

    |1+mu*n| >= 4n^2-1 > 1.

Translations have no effect on direction or rho. Thus NO nonzero integer power of ANY fiber-preserving pure horizontal or vertical shear decreases rho at this direction. In particular no cycle-lcm step decreases it. This is a symbolic all-n/all-powers obstruction, not a finite search failure.

The tentative universal availability premise in candidate-01 is REFUTED already at r0. It cannot be rescued by asserting r<=8 alone or by ignoring large return periods. An induction that recognizes convex rooms as a different terminal base is NOT refuted by this example; neither are non-parabolic affine moves, uphill intermediate steps, induced-section ranks, or room-changing reductions with a separately proved transfer. Those require new proofs and are not supplied by WR01.

## 5. Why an axis terminal cannot be assumed

No horizontal trajectory on this torus connects X to Y, since their y-coordinate sets are disjoint. No vertical trajectory connects them, since their x-coordinate sets are disjoint. Therefore any genuine whole-surface affine map preserving X,Y,Sigma setwise cannot send the LIT direction (n,1) to an axis: applying it to the lit path would contradict those coordinate separations. This is true even for affine derivatives other than the two parabolic types above.

Thus an exact fiber-preserving reduction of directions on a fixed surface cannot universally end at an axis illuminated base. A room-dependent terminal collection could contain illuminated non-axis directions, as the already accepted per-input finite-orbit decider does. Proving that one of those terminal classes is illuminated from r<=8 is still the original missing force; running its existing orbit calculation again would not prove it.

## 6. Decision and remaining scope

ACCEPT as proved here, pending peer review: constructed full-fiber affine maps; exact complete weighted first-return/optical transfer; strict partial rho descent. REJECT as a universal claim: every non-axis direction has a rho-decreasing such move, or axis termination supplies illumination. The P_n obstruction uses the actual physical square and actual four-point endpoint fibers, not a nonphysical cover or a selected synthetic target.

The method never composes different-direction returns at an interior point. It retains all original weights and all forbidden regular physical corners. It proves no new r<=8 illumination theorem, no qualifying dark example and no nine-corner bound. This result pinpoints a new weighted-descent availability failure; it does not rule out every possible weighted induction. Full theorem remains open.
