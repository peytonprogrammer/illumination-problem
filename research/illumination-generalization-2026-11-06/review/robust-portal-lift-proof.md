# R52: robust core portals lift to arbitrary independent actual depths

Author theorem pending independent review. Universal canonical45 W<=21 remains OPEN. Original conservative effort start07:39Z/deadline07:53Z includes weighted-phase reasoning. No earlier discovery clock was renewed.

## 1. A reusable sufficient geometric hypothesis

Let a strictly simple orthogonal room have two disjoint selected rectangular teeth on the right of a separator x=0. Their center heights are y_s<y_t, independent half-heights v_s,v_t>0, and actual positive widths w_s,w_t. Both attach through their full open mouths to the room on x<0. Assume the following core-template property has been proved with constants L0>0, K>v_s+v_t and finite R:

For EVERY independent pair

    -v_s<delta_s<v_s,  -v_t<delta_t<v_t,           (H)

there is a corner-free actual specular core path from (0,y_s+delta_s) to (0,y_t-delta_t), contained in x<=0, whose initial velocity is proportional to (-1,tau), final velocity to (1,tau), and whose common absolute slope is

    tau=(K-delta_s-delta_t)/L0.

It has at most R genuine reflections. Its open segments cannot hit the target seam (0,y_t) before the endpoint when delta_t=0. All listed mirrors must be actual finite walls of the room. The property includes the presence of all other teeth; a rectangle with filled-in mouths is NOT an adequate replacement.

The hypothesis can be furnished by a fixed reflection word with developed horizontal length L0 and vertical separation K-delta_s-delta_t; its actual finite-wall guards must hold on the ENTIRE open portal box. There is no assumed witness at an interior tooth mark, no depth bound, no winding/divisibility assumption and no reference to a supplied eventual tail.

Then EVERY independent actual midpoint-row depth pair

    S=(D_s,y_s), T=(D_t,y_t),
    0<=D_s<w_s, 0<=D_t<w_t,                      (2)

illuminates. This holds for arbitrary positive REAL half-heights, including irrational v_s/v_t. The resulting finite path uses at most R+n_s+n_t reflections, with the explicit bounds in section2.

This is a sufficient transfer lemma, not a necessity theorem for all polygons. In particular, (H) is a substantial remaining geometric obligation on any new strip generator. The explicit corollary in section5 verifies it independently in a nonempty family.

## 2. Weighted matching without a commensurability assumption

Set E=D_s+D_t, L=L0+E. For real t>=0 define nearest indices and the weighted map

    n_i(t)=floor(D_i*t/(2v_i)+1/2),
    G(t)=(K+2v_s*n_s(t)+2v_t*n_t(t))/L.           (3)

Start t_0=0 and t_(j+1)=G(t_j). Every n_i(t) is nondecreasing. Since G(0)=K/L>0, the iterates and BOTH integer indices are componentwise nondecreasing.

Take

    Tbar=(K+v_s+v_t)/L0.

The floor bound gives

    G(Tbar)<= (K+E*Tbar+v_s+v_t)/L = Tbar.        (4)

Thus 0<=t_j<=Tbar for all j. Each index is bounded by the finite integer

    B_i=floor(D_i*Tbar/(2v_i)+1/2).               (5)

There are finitely many possible INDEX PAIRS. Whenever the indices change, at least one increases by at least1; at most B_s+B_t such changes occur. After indices cease to change, the next slope is stationary. Denote the eventual value tau>0 and its indices n_s,n_t. This proves termination for every real input. It does NOT assume the weighted scalar values 2v_s*n_s+2v_t*n_t form a discrete lattice: for incommensurable half-heights that assertion would be false.

The stationary slope is the least nonnegative fixed slope reached from zero. More precisely, any supersolution q>=0 with G(q)<=q bounds every t_j above, by monotonicity and t_0=0. This property, rather than arbitrary choice of a fixed point, resolves corner equality below.

Define

    delta_i=D_i*tau-2v_i*n_i.

The rounding convention gives -v_i<=delta_i<v_i. Stationarity is exactly

    L0*tau=K-delta_s-delta_t.                    (6)

The upper bound (5) gives the actual reflection bound

    R+B_s+B_t.                                  (7)

For rational parameters all floors and iterations are exact effective operations. The all-real existence proof uses only real inequalities and finitely bounded integer pairs, not a claim about a numerical algorithm deciding arbitrary real floor equalities from finite precision.

## 3. Every negative rounding equality is excluded

Suppose delta_i=-v_i for one index i. Then D_i>0 and n_i>=1. The corresponding rounding argument at tau is exactly the integer n_i:

    D_i*tau/(2v_i)+1/2=n_i.

Set

    q=tau-2v_i/L
     =(K+2v_i*(n_i-1)+2v_j*n_j)/L>0.             (8)

Since D_i>0, that rounding argument strictly decreases at q, so n_i(q)<=n_i-1. The other index cannot increase. Therefore

    G(q)<= (K+2v_i*(n_i-1)+2v_j*n_j)/L=q.

This is a positive supersolution strictly below tau, contradicting the bound-on-all-iterates property just proved. Hence BOTH residuals satisfy strict (H). The argument also handles simultaneous equalities: select either tied index and the other cannot increase. A zero-depth endpoint has n_i=delta_i=0, so cannot be this excluded equality.

No irrationality, genericity, tie-breaking perturbation or corner continuation is used. An arbitrary stationary solution can have a negative equality; selection by the monotone iteration is essential.

## 4. Actual arms, velocities and original first target

Write F_h(u)=min(r,2h-r), r=u mod2h, for folding into[0,h]. The source's actual normal arm, with 0<=r<=D_s, is

    x=D_s-r,
    y=y_s-v_s+F_(2v_s)(v_s-2v_s*n_s+tau*r).      (9)

At r0 the odd midpoint phase folds to v_s, so the arm starts at ORIGINAL S. At rD_s its phase is v_s+delta_s, strictly in(0,2v_s); the arm ends at the required source portal with upward vertical velocity. Every internal horizontal contact is at phase2v_s*k, strictly between r0 andrD_s. There are exactly n_s such contacts, all at 0<x<D_s<w_s. Each is therefore inside an actual horizontal tooth wall, avoiding both mouth corners and the unused far end. Initial vertical sign may be either sign; illumination permits that. The terminal vector is proportional to(-1,tau), matching (H).

For the target arm, with 0<=r<=D_t, use

    x=r,
    y=y_t-v_t+F_(2v_t)(v_t-delta_t+tau*r).        (10)

It starts at the strict target portal with vector proportional to(1,tau), and ends at ORIGINAL T because its final phase is v_t+2v_t*n_t. Exactly n_t horizontal reflections occur strictly at0<x<D_t<w_t. A zero-depth arm is empty. Neither portal is a mirror. The source and target velocities are matched through the SAME stationary tau; independently chosen incompatible slopes are never concatenated.

Apply (H) at these strict residuals and splice the actual arms. The source arm lies in its lower selected band, disjoint from the upper band. The core lies in x<=0; it cannot meet T if D_t>0, while the first-seam condition handles D_t0. Along the target arm x strictly increases until its original marked abscissa, so that arm reaches actual T first. This proves the assertion and count without changing any physical endpoint fiber.

## 5. Concrete positive family with independently unequal tooth heights

Let c,v>0, and independent half-heights

    0<h_s<=v, 0<h_t<=v.

Take core[0,c]x[0,11v], left teeth of arbitrary independent positive real widths a,b in bands[3v,5v],[6v,8v], and right teeth of arbitrary independent positive real widths w_s,w_t centered at2v,8v with half-heights h_s,h_t. Let actual

    S=(c+D_s,2v), T=(c+D_t,8v),
    0<=D_s<w_s, 0<=D_t<w_t.

This is a strictly simple20-wall room, including h_s=v or h_t=v; same-side mouth gaps stay positive. EVERY such actual pair illuminates, for all listed positive REAL parameters. In particular h_s/h_t need not be rational.

Here is a complete check of the core hypothesis, without assuming it from a strip-growth heuristic. Put L0=4c, K=28v and choose arbitrary delta_s in(-h_s,h_s), delta_t in(-h_t,h_t). Their normalized values lie in(-1,1). Start the developed core at height2v+delta_s and slope

    tau=(28v-delta_s-delta_t)/(4c),

fold x by the actual two core sides and y between actual floor0 androof11v. At the four side events, developed heights are

    9v+(3delta_s-delta_t)/4 in(8v,10v),
    16v+(delta_s-delta_t)/2 in(15v,17v),
    23v+(delta_s-3delta_t)/4 in(22v,24v),
    30v-delta_t in(29v,31v).

They fold to left gap(8v,10v), right gap(5v,7v), left gap(0,2v), and the ORIGINAL target portal8v-delta_t. The actual right gap is(2v+h_s,8v-h_t), which contains(5v,7v), including h_t=v because both intervals are open. Both left turns lie outside the unchanged actual left mouths. End-line crossings11v,22v have0<x<c and are the only horizontal core events; none coincides with a side event. Thus exactlyfive actual reflections occur. The open core segments stay in0<x<c; initial and final signs match sections1/4. No earlier target seam is encountered. This independently verifies (H) with R5 for the WHOLE portal box.

Sections2--4 now give every independent actual normal-depth pair with at most

    5 + floor[D_s*(28v+h_s+h_t)/(8c*h_s)+1/2]
      + floor[D_t*(28v+h_s+h_t)/(8c*h_t)+1/2]      (11)

reflections. All horizontal widths, the vertical scale, selected half-heights and endpoint depths vary independently within the stated inequalities; no joint finite prefix remains inside this family.

For integer c,v,h_s,h_t,a,b,w_s,w_t and integer depths with c+D_s,c+D_t even, these are actual interior even-even A points in a canonical45 disk with20 maximal walls. Independent selected heights h_s,h_t can be arbitrarily large as v grows. The integer theorem has no size, diameter, k or other-A-count bound. This supplies a positive family beyond the earlier height2 integer comb closure. It does not classify all pairs or all 20/21-wall rooms.

## 6. Evidence and precise unresolved bridge

robust-portal-lift-check.py contains own exact weighted matching, an independently written actual FIRST-HIT ray tracer, and actual simple20-wall contours for the corollary. All30 prescribed rational controls pass798 reflections and16560 full wall/leg guards, including unequal selected heights, independently real depths, tiny far-end margins and large opposite widths. Four additional weighted-matching controls use EXACT Q(sqrt2) arithmetic with selected half-heights sqrt2/2 and1. Rational squares determine every comparison and floor. They check the material incommensurable case; they are explicitly ARITHMETIC controls, not actual irrational ray replays. No floating approximation is used in those field comparisons.

The finite controls support the hand proof but do not replace its arbitrary-real quantifiers. No author optical code executed. No literature or external theorem is imported. Independent peer acceptance remains required.

The missing universal obligation is to construct a robust core template or another actual witness for every residual marked W<=21 generator fiber. This lemma does not prove such a template exists, does not show arbitrary perpendicular strip growth preserves one, and does not replace that geometric gap by a supplied-witness hypothesis. All canonical45 geometries outside the explicit family remain open under the original goal and accounting.
