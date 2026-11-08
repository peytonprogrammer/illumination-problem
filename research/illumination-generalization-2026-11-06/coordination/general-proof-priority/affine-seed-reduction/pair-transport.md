# Pair transport and a uniform-source L-room criterion

Status: HAND proof completed and four prescribed exact path checks PASS. No universal wall-count claim and no historical novelty claim.

## Exact endpoint transfer without source fixation

Let M be the actual reflection unfolding of a finite room and Sigma every physical corner lift. Let F be a genuine global affine homeomorphism with F(Sigma)=Sigma. Fix actual interior source and target lifts p,q. If F(p) and F(q) are joined by a finite straight regular segment eta in M avoiding Sigma, then F^-1(eta) joins the exact original p and q, avoids all physical corners and refolds to a finite specular path.

F(p)=p is unnecessary. No replacement of either original endpoint is made: the inverse restores both. Unlike a proposed seed physical trajectory, eta may lie on a smooth wall seam. Such a seam segment is an ordinary straight regular segment of M. Its inverse cannot glide along a physical wall on a nonzero interval, because that straight regular path starts at the original interior source. Finiteness follows from compactness away from Sigma and finitely many polygon seams. A segment in one copy's closed rectangle, avoiding all corner lifts, supplies a seed without solving any billiard itinerary.

## Uniform-source theorem for an L room

Let A>a>0 and H>B>0, and let P=([0,A]x[0,B]) union ([0,a]x[B,H]). Let the target satisfy 0<t<a and 0<v<H. Choose a real shear parameter k such that

 k*a/H is an integer,
 k*(A-a)/B is an integer,
 v+k*(t+a) is an integer multiple of 2H.

Then EVERY actual real interior source S in P distinct from T illuminates T=(t,v). More specifically, each pair has a straight seed under one of the two genuine global affine maps V_k or R_y composed with V_k, unless it is already directly visible in the vertical rectangle. Smooth seam-aligned seed segments are allowed.

Proof of global maps: the two vertical cylinders have coordinates

 C_left: x in(-a,a), y in R/(2H)Z,
 C_right: x in(a,2A-a), y in R/(2B)Z.

Define V_k(x,y)=(x,y+k*(x+a)) on C_left and (x,y+k*(x-a)) on C_right. Its derivative is [[1,0],[k,1]]. The shifts on the two vertical boundaries of each cylinder are respectively 0,2ka and 0,2k(A-a), all full circumferences by hypothesis. Hence V_k is pointwise identity on all cylinder boundary subarcs and glues with its common derivative. Its inverse uses -k. Convex corner marks at x0 are preserved since ka is an integer multiple of H; those at xA are preserved since k(A-a) is an integer multiple of B. The reflex and inner roof corner are on vertical cylinder boundaries and fixed. The intrinsic copy involution R_y also preserves Sigma.

Proof of seeds: a source with x<=a is directly visible to T within the vertical rectangle; a source with x>a is in the lower right arm, say S=(s,u), a<s<A and 0<u<B. Write r=u+k*(s-a) modulo2B, with 0<=r<2B. V_k sends T to the smooth bottom point (t,0). If 0<=r<=B, choose F=V_k; otherwise choose F=R_y V_k, so the source image has coordinates (s,2B-r) in the original lower rectangle. R_y fixes the bottom seed point, so in either case F(T)=(t,0).

The segment between F(S) and (t,0) lies in the closed lower rectangle. It avoids ALL genuine corners: t>0 and s<A exclude the two bottom corners; a<s and t<a make any crossing of x=a occur below B unless the entire segment has y0, in which case it stays on a smooth bottom wall away from its corners. If F(S) lies on yB it is strictly between a and A, hence on a smooth ledge rather than at a corner. Thus eta is a straight regular segment on M, and exact pair transfer proves the theorem. Source images at y0 cause no failure.

## Exact arithmetic sufficient condition for native marks

Assume A,a,B,H,t,v are integers. To preserve the finite set of all physical integer-point lifts, restrict to integral k. Define

 K=lcm(H/gcd(a,H), B/gcd(A-a,B)).

The two cylinder and corner conditions hold for precisely k=K*m, m integer. The target condition becomes

 K*(t+a)*m = -v (mod 2H).

It has a solution if and only if gcd(K*(t+a),2H) divides v. This is a complete equivalence for the stated integral vertical-shear subfamily, not for all affine automorphisms or all illuminated targets. A solution can be obtained by Bezout arithmetic with no ray search. It gives a uniform-source conclusion for the target and metric satisfying this explicit sufficient condition.

## Prescribed controls and unresolved scope

For the existing room A28,a16,B4,H16 and target T8,8: K1 and gcd(24,32)=8 divides8; k1 satisfies the target condition. Therefore ALL real interior sources are covered, including the prior S26,2 and S0=24,2. For S22,2 the source image is (22,0), so the seed lies along the smooth bottom wall; inverse pair transport predicts the actual path (22,2)->(20,4)->(16,0)->(8,8), two reflections. This path is declared before computation.

For S26,2, k1 sends source to the smooth ledge point (26,4) and target to (8,0). The inverse derivative sends seed vector(-18,-4) to(-18,14), hence initial direction(-9,7). Before checking, derive all finite-wall contacts exactly from this direction rather than executing a tracer or guessing an itinerary.

For the same room T8,6 fails this restricted criterion: gcd(24,32)=8 does not divide6. That is not darkness or failure of the pair-transport mechanism; it is only failure of this integral vertical-shear subfamily. No complete arithmetic coverage theorem for all L targets, ten-wall rooms or r<=8 is established here.

### Final exact itineraries, declared before checking

- S26,2: direction(-9,7), contacts (164/7,4) then (128/7,0), then T8,8. The portal x16 is crossed at y16/9, strictly between0 and4.
- S24,2: direction(-8,7), contacts (152/7,4) then (120/7,0), then T8,8.
- S22,2: direction(-1,1), contacts (20,4) then (16,0), then T8,8. Its seed is the smooth bottom-wall segment from22,0 to8,0.
- S20,2: use R_y V, direction(-6,7), contacts (128/7,4) then (104/7,0), then T8,8. Its portal is crossed at y4/3.

Each has three legs and exactly two genuine reflections. These four controls distinguish a ledge seed source, an interior seed source, a wall-aligned seed and the required reflected-copy branch. They are prescribed checks of the theorem's formulas, not a source, direction or orbit census.

## Final audit and verification scope

The four predeclared paths passed `python3 -B pair-transport-check.py`: two reflections each, eighteen original finite-wall leg checks each, seventy-two total. Their launch directions agree with the inverse affine derivatives. The exact arithmetic check also confirms T=(6,8) via k4 and failure of T=(8,6) for the full integral vertical-shear subfamily. The latter is a gcd argument, not an enumeration over shear parameters.

The general proof was rechecked separately from the examples: cylinder-boundary values and common derivatives, both convex-corner swaps, fixed reflex and roof corner, exact endpoint and sheet restoration, r=B and r=0 seam cases, the reflected r>B branch, source x=a, and exclusion of all genuine corners on the seed segment. Source equals target is excluded from the quantified statement. No source fixed-point hypothesis is used.

The accepted historical all-real L illumination theorem already covers every source/target pair in every L metric. See ../../../review/all-real-L-dependency-review.md (resolve against the research root if opening manually). Therefore this result is NOT new illumination coverage. It isolates a stronger, reusable property for a specified target: a single global cylinder shear (possibly followed by the physical copy involution) transports every source to an explicit straight seed. No historical novelty determination has been made.

The old source-fixed boundary-inclusive condition remains unresolved for the original S26,2 test. The pair-transport theorem bypasses that unnecessary restriction; it does not silently claim to have settled it. The generic-real trivial-stabilizer obstruction likewise remains true for source-fixed maps and has no implication against pair transport.

The missing general step is to obtain a seed covering theorem for every target/metric of interest, potentially using both cylinder orientations and more general straight seeds. Neither the displayed gcd condition nor the four successful paths supply it. In particular, all ten-wall and full r<=8 assertions remain open. No new discovery run, orbit census, engine, worker, native goal mutation or git operation was used.
