# Every spine/middle-row pair illuminates in a rectangular-spine comb

A32 hand proof candidate, pending independent review. This is a complete class statement, not an eventual tail or a finite-search conclusion. No reference billiard path is assumed.

## 1. Geometry and endpoint class

Let P be any finite strictly simple rectangular-spine comb: a spine[0,c]x[y_min,y_max], c>0, and finitely many disjoint right rectangular teeth[c,R_j]x[l_j,u_j], R_j>c. Every tooth has positive height; different tooth bands have positive separating gaps. A tooth may meet the global spine floor or ceiling. Let E consist of all ACTUAL interior points of P which either have x<=c, or lie on the middle horizontal line of one tooth.

Claim: EVERY distinct pair in E illuminates by a finite actual specular trajectory avoiding every actual corner. Dimensions and marks may be arbitrary real numbers, and different tooth heights, depths and far ends are independent. The number of teeth and walls is unrestricted. Extra teeth do not supply auxiliary mirrors or enter the construction.

## 2. Two middle-row points in different teeth

Order the two selected teeth vertically. Translate y so their bands are[0,u] and[H-v,H], with c,u,v>0 and H>u+v. The actual marks are

    S=(c+D_s,u/2), T=(c+D_t,H-v/2),
    D_s,D_t>0,

and each actual right end extends strictly beyond its mark. A mark at x=c belongs to the spine case handled later. Define A=D_s+D_t+2c and, for tau>=0,

    n_s(tau)=floor(D_s*tau/u+1/2),
    n_t(tau)=floor(D_t*tau/v+1/2),
    Phi(tau)=[H-(u+v)/2+u*n_s(tau)+v*n_t(tau)]/A.            (1)

These are exact real floor functions; no numerical approximation is used.

### Finite monotone matching

Start tau_0=0 and iterate tau_{j+1}=Phi(tau_j). The map is nondecreasing and

    Phi(0)=[H-(u+v)/2]/A>0.

Put tau_max=H/(2c). Since floor(x)<=x,

    u*n_s(tau)+v*n_t(tau)
       <=(D_s+D_t)*tau+(u+v)/2,
    Phi(tau)<= [H+(D_s+D_t)*tau]/A.

It follows that Phi(tau_max)<=tau_max. Monotonicity therefore keeps every iterate in[0,tau_max], and the iterates are nondecreasing. On that bounded interval both floor functions take only finitely many integer values. Hence Phi has only finitely many output values there, and the nondecreasing iteration becomes stationary after finitely many steps. Let tau=tau_j be its FIRST stationary value. Then j>=1, tau_j>tau_{j-1}, and tau>0.

This stationary point is NOT a floor jump. If n_s jumps at tau_j, its value there exceeds its value at the smaller tau_{j-1} by at least1; n_t cannot decrease. Thus

    Phi(tau_j)>=Phi(tau_{j-1})+u/A>tau_j,

contradicting stationarity and tau_j=Phi(tau_{j-1}). The same argument applies to a jump of n_t, including simultaneous jumps. Therefore both fractional remainders

    r_s=D_s*tau+u/2-u*n_s,
    r_t=D_t*tau+v/2-v*n_t

are STRICT:0<r_s<u and0<r_t<v. Substituting the fixed equation(1) gives

    r_s+r_t+2c*tau=H.                                      (2)

No equality at either mouth endpoint is accepted.

### Why the half-period is physically valid

The use of periods u and v is special to an EXACT middle-row endpoint. It cannot be used for a general vertical offset. Write n_s=2k_s or2k_s+1. In the even case choose sigma_s=+1; in the odd case choose sigma_s=-1. Then

    r_s=sigma_s*(u/2)+D_s*tau-2u*k_s,
    k_s=floor(n_s/2)>=0.

The same rule gives sigma_t,k_t from n_t and v. Thus the half-period formulas are precisely the union of the TWO legitimate actual source/target images, separated by a half-period. An odd n means a genuine initial downwards leg and an odd count of horizontal-wall reflections; it is not a substituted endpoint.

### Actual source, spine and target path

Launch left from actual S, with initial vertical sign sigma_s and absolute speed ratio tau. Use its tooth unfolding with initial ordinate sigma_s*u/2 and terminal ordinate2u*k_s+r_s. If sigma_s=+1, the horizontal tooth-wall contacts are j=1,...,2k_s; if minus they are j=0,...,2k_s. Each has coordinate

    (c+D_s-(j*u-sigma_s*u/2)/tau, u if j odd else0).

All travel times are positive, including the minus j0 time u/(2tau). All contact abscissae are STRICTLY greater than c, since the last unfolded contact2u*k_s precedes the strict terminal height2u*k_s+r_s. They are strictly left of the actual source and far end. Consequently every contact is a smooth actual tooth-wall point; neither actual mouth corner nor an artificial horizontal spine cut is touched. After its n_s ordinary reflections the source reaches the strict portal(c,r_s) with upward vertical velocity.

Use the two spine legs through

    M=(0,r_s+c*tau), then(c,H-r_t).

Equation(2) matches their velocities exactly. M lies strictly between the portal heights, and hence strictly between the global spine floor and ceiling. Its x=0 contact is smooth. Both open legs have x<c, avoiding every other tooth, mouth and actual vertex. No cap or artificial spine end is a reflection. The y-reflected reverse of the corresponding upper-tooth construction ends at the ACTUAL T with the required right/up entry velocity.

The total is n_s+n_t+1 ordinary reflections. It is finite by the matching argument. Lower tooth legs stay in their lower band; the spine legs have x<c; and the final tooth's x coordinate increases to actual T for the first time. The complete path is corner avoiding and cannot substitute a different endpoint or target lift. Reversing it covers either initial ordering of the pair.

## 3. A spine point and one middle-row tooth point

Let the actual spine/seam point be S=(x_s,y_s), with0<x_s<=c and y_min<y_s<y_max. Let T=(c+D,l+u/2), D>0, be the tooth middle-row point. If y_s is in[l,l+u], the direct segment is inside P: before x=c it lies in the spine and afterwards strictly in the selected tooth band. If S is on a tooth-mouth seam, actual interiority excludes a genuine corner. Thus the direct path is legal in this case.

Otherwise put C=c+x_s>0. Reflect S across the ACTUAL left spine wall, using its image(-x_s,y_s). The legitimate vertical images of the MIDDLE target have all ordinates

    l+u/2+u*n, n in Z.

For each integer n the connecting line has slope and portal height

    tau_n=[l+u/2+u*n-y_s]/(C+D),
    z_n=y_s+C*tau_n.

The heights z_n form a two-sided arithmetic progression with positive step C*u/(C+D), which is STRICTLY smaller than u. Hence some n gives l<z_n<l+u. This is an exact finite rounding choice: the interval of admissible n has length(C+D)/C>1. If y_s<l, its tau_n is positive; if y_s>l+u, negative. The line cannot have a corner equality at the mouth because the portal was chosen strict.

Fold once at x=0 and then vertically within the selected actual tooth. The left-wall contact height is y_s+x_s*tau_n, strictly between y_s and z_n because0<x_s<C. It is therefore strictly inside the global spine wall. Both spine legs stay inside the spine. After the strict portal, every tooth-wall contact has x>c and occurs before actual x=c+D; the far end lies beyond T. The target image l+u/2+u*n folds to ACTUAL l+u/2 for either parity of n. Both slope signs and negative n are legitimate finite unfolded tooth itineraries. Thus every such spine/middle-row pair illuminates, with no depth threshold.

This also handles a source on x=c in another mouth: its first leg moves into the spine. No reflection at that mouth is inserted.

## 4. Remaining placements are exhaustive

Two points in the same tooth rectangle are directly visible. Two actual points in the spine with at least one abscissa<c are directly visible through its interior, including a target on x=c. If BOTH are on mouth seams x=c at different heights, direct travel on x=c might run along boundary gaps. Instead use the actual left-wall reflection at(0,(y_s+y_t)/2). Its two open legs have x<c and the reflection is smooth because both heights are strictly between the global ends.

Any distinct pair in E is either a spine/spine pair, a spine/middle-row pair, a same-tooth pair, or a middle-row pair in two different teeth. The preceding cases therefore prove the whole stated theorem.

## 5. A complete uncapped canonical-A subclass

Suppose the comb has integer axial boundary coordinates and EVERY tooth has height2. Every actual interior even-even A point with x>c must have an even integer ordinate strictly between l_j and l_j+2. If l_j is even there is none; if l_j is odd the only one is l_j+1, EXACTLY the tooth's middle row. Actual A points with x<=c are in the spine/seam category. Therefore EVERY distinct actual interior A pair in EVERY such comb illuminates.

This holds for arbitrary finite numbers of teeth and walls, arbitrary integer widths, vertical gaps, endpoint depths, area, k and lattice diameter. It applies in particular to all members of this class having W<=21, without a transparent-exception cap or finite prefix. A tooth of height1 has no integer interior row, so allowing such extra teeth does not alter this conclusion; the stated height2 class already suffices.

The result does not assert illumination for arbitrary off-middle tooth endpoints, every canonical comb, changing diagonal-wall patterns or all canonical45 W<=21 rooms. No general minimum or historical novelty is claimed. Its entire class proof is elementary exact matching plus actual-wall guards, with independent review still required.
