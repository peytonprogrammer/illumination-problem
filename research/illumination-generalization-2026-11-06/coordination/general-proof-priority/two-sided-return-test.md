# Two-sided return test: candidate and prescribed validation

Status: hand derivation, not independently accepted. General existence remains OPEN.

## Predeclared question and control

Can later right/bottom/cap excursions escape LR01's FIRST-right-exit blind stripe? Test the existing K1R01 room ONLY, not a new room:

(a,l,w,A;b,c,h,H)=(12,20,28,32;1,3,4,5), S=(8,4), T=(24,2).

The accepted four-reflection ray has direction (16,3) and unfolded parameter duration 2. Accepted WR01 endpoint-fixing horizontal/vertical cylinder maps will be applied to this whole path, never concatenating different-direction rays.

Horizontal row-cycle lengths are among 2a,2B,2R,2A, so P=2*lcm(a,B,R,A)=192 is an allowed horizontal twist coefficient. Vertical column-cycle lengths are among 2(H-b),2(H-h),2c,2H, so Q=2*lcm(H-b,H-h,c,H)=120 is an allowed vertical coefficient. Apply V_Q once, then H_P:

(16,3) -> (16,1923) -> (369232,1923).

Predicted actual direction tau=369232/1923=192+16/1923, positive source signs, actual target duration D=3846 at |vy|=1. No coefficient/direction choice will be searched if validation fails. Failure means investigate the hand transfer claim, not try another ray.

Prescribed exact check: reuse the existing reviewer replay_actual first-wall routine, removing its SINGLE-roof-only assertion because the present path expressly uses repeated roofs. Extract the pure geometry definitions without running any historical discovery or main blocks. Record whether exact original T is first reached at D, every collision is ordinary, and more than ten bottom-floor reflections occur. No discovery clock or historical search is restarted.

## Proposed arbitrary-metric implications to prove

1. For any already illuminated native terminal pair in an integral ordered spiral, WR01 twists give illuminating directions arbitrarily close to P on its positive side. This is conditional on an existing path and cannot establish illumination of an unknown pair.
2. For each N>=1, 0<epsilon<1/(2beta+2HN) forces the first N complete right-floor-cap circuits after FIRST R exit to remain in the open stripe (w,w+1) whenever they cross a native bottom target's height. The actual intermediate finite-wall guards must be proved; merely extrapolating LR01 is insufficient.
3. Combining these yields already-lit pairs with illuminating directions requiring arbitrarily many right excursions, not an unbounded MINIMUM across all directions. The K1R01 control still has its accepted four-reflection route.

Detailed proof and validation outcome will be appended only after the exact obligations are checked. No independent acceptance, novelty, new room coverage or general nonemptiness is claimed.

## Hand proof A: an already-lit terminal pair has full paths arbitrarily near P

Retain the original integral ordered spiral, actual native source S=(s,u) with 0<s<a and b<u<H, and target T=(t,v) with l<t<A and 0<v<c. They are distinct interior even-even points. Let beta=H-h, G=h-c, R=A-w, B=A-l and

    P=2*lcm(a,A,R,B),
    Q=2*lcm(H-b,beta,c,H).

At a generic horizontal level the physical interval containing the ray has width a, A, R or B. One full horizontal cycle in the four-copy translation unfolding traverses that interval twice and has length twice its width. Thus the order of the unit right-permutation divides P. Similarly, generic vertical intervals have lengths H-b, beta, c or H, so the unit up-permutation order divides Q. These are statements about unit row/column cycles, not an assumption that the entire maximal cylinder has unit height.

The already independently accepted WR01 row construction therefore gives actual global affine automorphisms H_P and V_Q on the SAME unfolding, with derivatives

    H_P(p,q)=(p+Pq,q),
    V_Q(p,q)=(p,q+Qp).

They fix the entire integer-vertex fiber pointwise, including every actual source lift, target lift and forbidden corner lift. Their inverses preserve those same sets. Consequently applying either map to a WHOLE legal finite segment gives another legal segment between the SAME selected lifts, and refolding gives an original-room trajectory. Physical reflection words are reconstructed, not copied. This optical transfer is inherited WR01 content, not newly claimed here.

Assume a legal S-to-T ray exists. Its unfolded displacement has integer coordinates, hence its direction can be written (p,q) with integer components. Here q is nonzero: a horizontal physical ray cannot leave the source's horizontal component and reach this terminal T. If u is not v, it also cannot change height; if u=v, that height lies below c and the left and bottom intervals are separated. Choose an integer k such that p0=p+kPq>0. Apply H_P^k to the existing path, and then apply V_Q^n followed by H_P. The resulting direction is

    (p0+P(q+nQp0), q+nQp0),
    tau_n=P+epsilon_n,
    epsilon_n=p0/(q+nQp0)>0

for all sufficiently large positive n. Moreover epsilon_n tends to zero. Every path remains between the actual original endpoint lifts and avoids every forbidden corner. Thus EVERY already-lit terminal pair has illuminating directions in EVERY sufficiently small right-hand neighborhood of P.

This proves an existence-preserving NORMALIZATION, not existence for a previously unknown pair. It neither supplies a starting ray for the uncovered class nor contradicts LR01, which restricts the physical itinerary. A dark pair stays dark under these maps.

## Hand proof B: any fixed number of right circuits is still blind sufficiently near P

Fix N>=1 and

    tau=P+epsilon,
    0<epsilon<1/(2beta+2HN).

Suppose a legal ray from the native terminal source reaches its FIRST downward right mouth at y=h. LR01's source-injection/last-left-entry argument applies: before first R the path has only left/cap episodes, and its first right state is

    x=w+rho, vx=+tau, vy=-1,
    0<rho<2beta*epsilon.

The bound above is at least as restrictive as the LR01 first-tail bound for a native bottom target, since h+v<2H. Upper sources' initial descending contact is in L under the same smallness estimate; S at y=h is a regular left-mouth source. Any corner encountered earlier would already disqualify the ray.

Define d_j=rho+2Hj*epsilon. Inductively, from the j-th downward right state x=w+d_j, the exact physical positions at successive horizontal section/floor/roof events are:

| Event | Physical x |
| --- | --- |
| y=c downward | w+d_j+G*epsilon |
| y=0, actual bottom reflection | w+d_j+h*epsilon |
| y=c upward | w+d_j+(h+c)*epsilon |
| y=h upward | w+d_j+2h*epsilon |
| y=H, actual roof reflection | w+d_j+(h+H)*epsilon |
| y=h downward | w+d_j+2H*epsilon = w+d_(j+1) |

For j=0,...,N-1 all displayed displacements from w are strictly between zero and one, because

    rho+2HN*epsilon < (2beta+2HN)*epsilon < 1.

Since R is a positive integer, all section and floor/roof positions lie strictly in (w,A). In particular each upward y=c crossing is a genuine right-mouth passage, each downward y=h crossing is immediately back into R, and none is a notch reflection or a reflex hit.

To justify the formulas and ALL intervening original walls, use the actual rectangle folds: first the right strip [w,A]x[c,h], then the bottom strip [l,A]x[0,c], then the right strip upward, then the cap [0,A]x[h,H]. Every relevant section height is an integer, and P is a full 2R, 2B and 2A phase period. Removing the P part at EACH integer-height section leaves precisely the small epsilon offsets in the table. These offsets remain on the same strict fold branches there, with physical vx=+tau. Between sections, each path is the standard unique rectangular billiard with its actual vertical mirrors; its vertical reflections may be numerous but are ordinary. Possible vertical-wall corner collisions occur only at a strip's endpoint height, where the table gives strict mouth/floor/roof interior positions. At intermediate integer b on the bottom right outer wall there is no actual corner. Thus no unguarded seam or artificial horizontal reflection is introduced. The only horizontal reflections during these N circuits are at the genuine bottom y=0 and roof y=H. In particular this is an actual physical induction, not just a formal return equation.

At the actual target's integer height v, the two bottom visits in circuit j occur at

    x_down=w+rho+(2Hj+h-v)*epsilon,
    x_up  =w+rho+(2Hj+h+v)*epsilon.

Both belong to (w,w+1) for every j<N. No integer target abscissa lies there. Before first R the path cannot reach the bottom target at all. The first N complete floor/cap circuits are therefore legal but miss actual T. This is a finite-circuit extension of the LR01 blind stripe; it does NOT exclude all later circuits or all slopes.

## Consequence: unbounded right-return depth in these normalized directions

Combine A and B. For EVERY already illuminated native terminal pair and EVERY prescribed N, choose n so epsilon_n<1/(2beta+2HN). The transferred ray is legal and does eventually hit actual T, while B forces at least N completed right-floor-cap circuits beforehand. Hence full trajectories arbitrarily near P can succeed, but their required right-return depth in that direction becomes unbounded as epsilon tends to zero.

This does not assert an unbounded minimum over ALL directions. In particular the existing K1R01 pair still has its original four-reflection illuminating ray. It also supplies no argument that an arbitrary unknown pair is illuminated. The substantive mechanism conclusion is: LR01's first-R obstruction is not an obstruction to full near-period illumination, and adding any fixed number of right circuits does not uniformly resolve its small-epsilon failure.

## Prescribed exact replay result

`two-sided-return-check.py` passed for the SINGLE predeclared K1R01 input and affine-image direction 369232/1923. The reused exact first-wall routine and full original-wall `path_check` verify:

- actual FIRST target arrival at normalized vertical time 3846;
- 47,748 ordinary physical reflections, with no corner encounter;
- 97 downward right-mouth entries and 96 upward right-mouth entries;
- 176 actual bottom-floor reflections (later bottom-only excursions can occur);
- first downward right-mouth position 53848/1923 = 28+4/1923;
- the first eleven downward right positions agree with w+rho+10j*epsilon, j=0,...,10;
- both target-height visits in each of the first ten circuits are in (28,29).

The input room/pair was previously illuminated. The direction was derived before the run, not selected by trial. The generic first-hit function was extracted from the existing review checker; only its one-roof-special-case assertion was removed in the extracted function. Its earliest-wall, corner, exact-first-target-time and whole-path guards remained. No frozen file, historical main/discovery code, search limit or clock was changed. Source hashes remained current before/after.

## Review status and remaining proof gap

The new deductions A/B and their combination are coordinator HAND arguments pending independent mathematical review. The exact replay corroborates one instance; it is not an independent review or a universal proof certificate. WR01 transfer and LR01 overshoot are accepted shared dependencies. Historical novelty is not assessed.

The original general existence gap is unchanged: produce a legal path for an unknown residual pair without first assuming it is lit. The normalization alone does not force a source orbit to meet the actual target. A two-sided approach must accommodate unbounded right-return depth or derive a different sufficient direction family with its own existence proof; another fixed-depth patch cannot justify the near-period strategy.
