# First witnesses for common horizontal growth of marked combs

R31 candidate for independent review. This proves a first-witness and eventual-tail statement in a specified generator class, without assuming an earlier witness. It does not prove illumination of its finite prefix or the universal W<=21 theorem.

## 1. Exact marked family and conclusion

Let a finite comb consist of the spine [0,c]x[y_min,y_max] and disjoint right-hand rectangular teeth. All dimensions are positive; distinct tooth bands are separated by positive gaps. Keep the spine and all tooth y bands fixed. Add the SAME real length L>=0 to the right ends of all teeth and to the x coordinate of each marked point lying strictly outside the spine. Marks in the spine or its mouth seams remain fixed. The initial marked points are distinct actual interior points.

Assume the tooth heights are commensurate: they are positive integer multiples of one real unit. Then every sufficiently large L illuminates the actual marked pair. With rational data there is an explicit computable cutoff L0, given below for the only nontrivial two-tooth case. No reference path or beam-existence search is required.

The conclusion holds for any number of teeth, in particular the canonical45 combs with W<=20. It concerns the transported fixed marked pair, NOT all newly introduced lattice points uniformly at the same cutoff. Independent changes in spine width, tooth heights or vertical separations are not asserted to share a uniform cutoff.

## 2. Strict portals for two arbitrary selected teeth

Translate y so the lower selected band is [0,u] and the upper band [H-v,H], where H>u+v. Other teeth and global spine boundaries may lie below, between or above these bands. Write the actual marks as

    S_L=(c+d_s+L,b_s), T_L=(c+d_t+L,H-b_t),
    d_s,d_t>0, 0<b_s<u, 0<b_t<v.

The right ends extend strictly beyond the corresponding marks. Define

    Delta=d_s-d_t, z=Delta/(2c),
    g>0 with p=u/g, q=v/g coprime positive integers,
    U=uv/g, P=2g.

For signs sigma_s,sigma_t in{+1,-1}, put delta=sigma_s*b_s-sigma_t*b_t. We seek winding integers k_s,k_t and strict portal offsets r_s in(0,u),r_t in(0,v) such that

    r_s=sigma_s*b_s+(L+d_s)*tau-2u*k_s,
    r_t=sigma_t*b_t+(L+d_t)*tau-2v*k_t,
    r_s+r_t+2c*tau=H.                                      (1)

The last equation is exact physical matching through one reflection on x0. Eliminating tau from the difference gives the congruence

    f(r_s,r_t)=(1+z)r_s+(-1+z)r_t
             =delta+zH-2g*n, n in Z,                       (2)

where n=p*k_s-q*k_t. Importantly (2) is independent of L.

The image of the open portal rectangle under f is the open interval(I_-,I_+), where

    I_-=min(0,(1+z)u)+min(0,(-1+z)v),
    I_+=max(0,(1+z)u)+max(0,(-1+z)v).

Its length is

    W=|1+z|u+|-1+z|v >=2min(u,v)>=2g=P.                    (3)

For |z|<=1 the first quantity is a convex combination of2u and2v. Outside that interval it is at least2u or2v. If W>P every residue class modulo P meets the open interval, so ANY choice of signs supplies an n and a strict portal pair.

If W=P, the only possible obstruction is the single class of its endpoints. Equality in (3) implies one of:

    u=v=g and -1<=z<=1;
    z=1 and u=g;
    z=-1 and v=g.

In the first two cases changing sigma_s shifts delta by2b_s, strictly between0 and2g in absolute value. In the last case changing sigma_t shifts delta by2b_t, likewise. Thus the four sign choices cannot all lie in the excluded class. At least one sign pair and integer n give a value strictly in(I_-,I_+), and hence some strict portal offsets r_s*,r_t*. No equality/corner case is dropped.

This selection is explicitly rational when the dimensions are rational. For example choose n by a floor, and if the remainder equals I_- with W>P use the next representative I_-+P. With W=P change a primitive-width sign if needed. Interpolate between opposite extremal corners of the portal rectangle to obtain strict coordinates. Put

    tau*=(H-r_s*-r_t*)/(2c)>0.

## 3. Bezout supplies nearby exact target slopes for EVERY large L

Choose integers alpha,beta with alpha*p+beta*q=1. Let

    k_s^0=alpha*n, k_t^0=-beta*n,
    k_s=k_s^0+q*h, k_t=k_t^0+p*h, h in Z.

Then p*k_s-q*k_t=n exactly. Define

    C0=H-sigma_s*b_s-sigma_t*b_t+2u*k_s^0+2v*k_t^0,
    D0=d_s+d_t+2c,
    tau_h(L)=(C0+4U*h)/(D0+2L).                             (4)

Equation(4) makes the sum equation in(1) EXACT; it is not a ray arriving only at a reflected/modulo target. Choose h nearest to

    ((D0+2L)*tau*-C0)/(4U).

Then

    |tau_h(L)-tau*| <= 2U/(D0+2L) ->0.                      (5)

This is valid for every sufficiently large REAL L, with no subsequence or congruence restriction on L. Also h->+infinity, so both k_s and k_t eventually become nonnegative.

At these slopes the two actual portal offsets can equally be written

    r_s(tau)=[H+delta-2gn+(Delta-2c)tau]/2,
    r_t(tau)=[H-delta+2gn-(Delta+2c)tau]/2.                  (6)

At tau* these are r_s*,r_t*. They remain strict for all sufficiently close slopes by continuity; (5) therefore gives all of(1) with k_s,k_t>=0 and tau>0 for every large L.

Here is one explicit conservative cutoff. Let a_s=(Delta-2c)/2,a_t=-(Delta+2c)/2 and

    eta=min(tau*/2,
            r_s*/[2(|a_s|+1)], (u-r_s*)/[2(|a_s|+1)],
            r_t*/[2(|a_t|+1)], (v-r_t*)/[2(|a_t|+1)]),
    h_min=max(0,ceil(-k_s^0/q),ceil(-k_t^0/p)),
    D_bound=max(2U/eta+1,
                (|C0|+4U(h_min+1))/tau*+1),
    L0=max(0,(D_bound-D0)/2).

For L>=L0 the strict error bound is <eta. The nearest integer h is >=h_min, since its real center exceeds h_min+1. Both winding indices are nonnegative. All quantities are rational and computable for rational input data. For an even strip parameter L=2N, only finitely many N lie below L0. None of them is silently declared illuminated.

## 4. Full actual billiard realization and corner guards

The lower tooth has unfolding source image sigma_s*b_s and final height2u*k_s+r_s. Start at actual S with horizontal velocity left and vertical sign sigma_s, with speed ratio tau. If sigma_s=+1 its contacts are j1,...,2k_s; if sigma_s=-1 they are j0,...,2k_s:

    (c+d_s+L-(ju-sigma_s*b_s)/tau,
     u if j odd else0).

All travel times are positive. In the minus case the first time is b_s/tau>0, including k_s0. Every contact lies STRICTLY at x>c, because the last contact precedes the strict portal by the positive unfolded height r_s. They also lie left of S and of the far tooth end. No source-side corner or other mouth is encountered, and the outgoing vertical velocity at the mouth is upward in both sign cases. The upper backward construction uses v,k_t,sigma_t,b_t and has the same properties.

Join the portals (c,r_s) and(c,H-r_t) through

    M=(0,r_s+c*tau).

Equation(1) gives exactly matched slopes tau and one ordinary vertical-wall reflection at M. Its height lies strictly between the two portal heights because tau>0; both portals lie inside the selected bands. The entire middle stays within the spine, with x<c except at its two strict mouth crossings. M cannot be a global spine corner. Every extra tooth/mouth/corner is avoided, and no artificial horizontal cut or cap is used. Reverse the upper backward leg to reach the ACTUAL T with matching velocity. There are

    2k_s+2k_t+1+[sigma_s=-1]+[sigma_t=-1]

ordinary reflections. Lower legs remain in their lower band, middle legs have x<c, and the upper final leg increases x monotonically to T. Thus no earlier spurious target or chosen lift substitutes for actual arrival.

## 5. Other mark placements, including seams

If both marks lie strictly inside the spine rectangle, or in one tooth rectangle, direct visibility applies. If one lies on x=c and the other strictly in the spine, the open direct segment has x<c. If BOTH lie on the mouth seam x=c at distinct heights y_s,y_t, use the one-left-wall reflection through(0,(y_s+y_t)/2). Its open legs lie strictly in the spine and its left contact is smooth. This handles a seam segment which would otherwise run along actual boundary gaps.

For one mark S=(x_s,y_s) in the spine or a mouth seam, 0<x_s<=c, and T=(c+D,l+b) in a selected tooth [l,l+w],0<b<w,D=d_t+L, an elementary construction supplies a finite path whenever D>c+x_s. Put

    C=c+x_s, y0=l+w/2, tau0=(y0-y_s)/C.

Use the image of S across x0, so the developed horizontal distance to T is D+C. Choose k nearest to

    ((D+C)*tau0+y_s-l-b)/(2w),
    tau=(l+b+2wk-y_s)/(D+C).

The actual portal height is r=y_s+C*tau and

    |r-y0|<=C*w/(D+C)<w/2.

Thus it is strictly inside the mouth. Fold once at x0, with contact(0,y_s+x_s*tau), and then vertically within the actual tooth to T. The spine part has heights between the interior source and strict portal, so its left contact avoids both spine corners; every tooth reflection is at x>c, and the far end lies beyond T. The unfolded target height differs by2wk and therefore folds to the ACTUAL l+b. A zero slope is a direct horizontal reflected connection with no tooth reflections. Negative slopes and negative k use the same finite ordered tooth crossings. The case x_s=c begins by moving into the spine, so the source mouth seam remains legal. D>2c suffices uniformly over the spine source's x coordinate.

These cases exhaust transported distinct marks of the fixed comb family. They do not give a cutoff uniform over all newly created A marks or over all other generator parameters. Actual spine width/height, each selected mouth, and the marks in their fixed chambers remain part of the data.

## 6. Evidence and exact remaining gap

comb-unequal-depth-first-witness-check.py independently builds all actual paths and all actual polygons, using reviewer geometry predicates. Six prescribed Bezout controls include unequal depths and heights, rational dimensions and noninteger L, and all three equality mechanisms in(3) requiring a sign change. Three more controls cover positive/negative spine-to-tooth slopes and two genuine source/target mouth seams. All1404 reflections and22608 all-wall/leg guards pass. These finite controls corroborate the universal hand argument; they do not establish its quantifiers by enumeration.

The theorem supplies FIRST witnesses and a computable full one-parameter tail for arbitrary transported marks in commensurate rectangular-spine combs, including arbitrary chosen inner teeth. It does not assume a previously discovered witness. Together with exact checks of a given finite prefix it would settle that one marked family. Prefix coverage itself, general nonrectangular chamber trees, independently varying perpendicular generators and the diagonal-wall subclass remain OPEN. No W<=21 universal conclusion or darkness inference follows from this milestone.
