# First actual paths on every positive horizontal growth-rate ray for equal-height comb teeth

A30. Candidate for independent review. This is distinct from a common-extension theorem: the two selected depths may grow at ANY fixed independent positive real rates. It supplies first witnesses without assuming a seed trajectory. It does not assert uniformity as those rates vary or resolve finite prefixes.

## Geometry and claim

Take a finite comb with actual rectangular spine[0,c]x[y_min,y_max], c>0, and separated right-hand rectangular teeth. Select any two teeth of the SAME height u>0; translate y so their bands are[0,u] and[H-u,H], H>2u. They may be inner teeth, with arbitrary other teeth below/between/above. All this vertical geometry is fixed. Let the actual marks be

    S_L=(c+D_s(L),b_s), T_L=(c+D_t(L),H-b_t),
    D_s(L)=a*L+d_s, D_t(L)=b*L+d_t,
    a,b,d_s,d_t>0, 0<b_s,b_t<u, L>=0.

The corresponding actual tooth ends extend strictly beyond the marks for all L; for example transport each end by its mark's rate and retain a fixed positive right margin. Other teeth may have arbitrary valid right ends. Every sufficiently large REAL L has a finite actual S_L-to-T_L specular path avoiding all corners. There is no reference-witness premise. For rational input data a finite computable cutoff is available by the rational branch below.

A sufficient exact optical certificate is signs sigma_s,sigma_t in{+1,-1}, integers k_s,k_t>=0 and tau>0 satisfying

    r_s=sigma_s*b_s+D_s*tau-2u*k_s in(0,u),
    r_t=sigma_t*b_t+D_t*tau-2u*k_t in(0,u),
    r_s+r_t+2c*tau=H.                                      (1)

The direct actual realization is proved in section4, not inferred from parameter arithmetic alone.

## 1. Rational rate ratio: eliminate the growing part exactly

Suppose a/b is rational. Choose coprime positive integers m,n with m*a=n*b. Set

    E=m*d_s-n*d_t,
    delta=m*sigma_s*b_s-n*sigma_t*b_t,
    j=m*k_s-n*k_t.

The weighted difference and sum in(1) give

    m*r_s-n*r_t=delta+E*tau-2u*j,
    (m+z)*r_s+(-n+z)*r_t=delta+z*H-2u*j, z=E/(2c).          (2)

On the open portal square(0,u)^2 the latter functional has open image of length

    u*(|m+z|+|-n+z|) >= u*(m+n) >= 2u.

If this length exceeds2u, every residue class modulo2u has a strict representative. Equality2u forces m=n=1 and -1<=z<=1. In that critical case changing sigma_s shifts delta by2b_s, strictly between0 and2u, so the four signs cannot all give the excluded endpoint residue. Thus signs, j and strict r_s*,r_t* exist. Choose them, and put tau*=(H-r_s*-r_t*)/(2c)>0. With rational input these choices are rational, using a floor, a possible critical sign change, and interpolation between extremal opposite square corners.

Choose integers alpha,beta with alpha*m+beta*n=1. All integer solutions of the weighted index equation include

    k_s=alpha*j+n*h, k_t=-beta*j+m*h, h in Z.

Define A(L)=(a+b)*L+d_s+d_t+2c and

    C0=H-sigma_s*b_s-sigma_t*b_t+2u*(alpha*j-beta*j),
    tau_h(L)=[C0+2u*(m+n)*h]/A(L).

This imposes the exact sum/target equation. Choose h nearest to

    [A(L)*tau*-C0]/[2u*(m+n)].

Then |tau_h-tau*|<=u*(m+n)/A(L), for EVERY L. Since a+b>0, h tends to+infinity and both winding indices become nonnegative. The actual portal offsets at these indices are also

    r_s(tau)=[n*H+delta-2u*j+(E-2n*c)*tau]/(m+n),
    r_t(tau)=[m*H-delta+2u*j-(E+2m*c)*tau]/(m+n).             (3)

These formulas follow by solving the weighted difference and sum; their derivatives are INDEPENDENT of L. At tau* they are precisely the selected strict offsets. Hence the rounding bound preserves their strictness and tau>0 for all large L.

For explicit rational data, let v_s=(E-2n*c)/(m+n),v_t=-(E+2m*c)/(m+n), and choose

    eta=min(tau*/2, r_s*/[2(|v_s|+1)],
            (u-r_s*)/[2(|v_s|+1)], r_t*/[2(|v_t|+1)],
            (u-r_t*)/[2(|v_t|+1)]),
    h_min=max(0,ceil(-alpha*j/n),ceil(beta*j/m)),
    A_bound=max(u*(m+n)/eta+1,
                (|C0|+2u*(m+n)*(h_min+1))/tau*+1),
    L0=max(0,[A_bound-d_s-d_t-2c]/(a+b)).

For L>=L0 the error is strictly below eta and the rounding center exceeds h_min+1. Thus all the stated winding and portal guards hold. The cutoff need not be small. No smaller L is declared dark or illuminated by this calculation.

## 2. Irrational rate ratio: fast phase density without a seed witness

Suppose a/b is irrational. Choose signs+,+, r_s*=r_t*=u/2 and tau*=(H-u)/(2c)>0. Put gamma=u/2, choose epsilon=gamma/8 and

    d=min(tau*/4,gamma/(16c)), J=[tau*-d,tau*+d].

For tau in J consider the two phases modulo1

    theta_s=[b_s+D_s(L)*tau-r_s*]/(2u),
    theta_t=[b_t+D_t(L)*tau-r_t*]/(2u).

For each nonzero integer character(h,k), the phase derivative is

    [L*(h*a+k*b)+h*d_s+k*d_t]/(2u).

Irrational a/b implies h*a+k*b!=0, so the average of that character on the fixed nonzero interval J tends to0 as L tends to infinity. This conclusion holds for all sufficiently large real L, not just a subsequence. Approximate any continuous nonnegative periodic bump supported in the small product phase box by trigonometric polynomials, uniformly. Its average tends to its positive torus integral. Therefore, for every large L there is tau_L in J and integers k_s,k_t for which

    e_s=b_s+D_s*tau_L-2u*k_s-r_s*,
    e_t=b_t+D_t*tau_L-2u*k_t-r_t*,
    |e_s|,|e_t|<epsilon.

This is phase selection, not an illuminating path yet. Because tau_L>=3tau*/4 and BOTH rates are positive, the chosen indices are nonnegative for all sufficiently large L.

## 3. Correct the ACTUAL target equation at fixed indices

At the selected integers, set

    F(tau)=[b_s+D_s*tau-2u*k_s]
           +[b_t+D_t*tau-2u*k_t]+2c*tau-H.

Its derivative is the positive A(L). At tau_L,

    |F(tau_L)| <= 2c*d+2epsilon <= 3gamma/8.

Set tau'=tau_L-F(tau_L)/A(L). This gives EXACTLY F(tau')=0. Since 0<D_s/A(L)<1 and 0<D_t/A(L)<1, each corrected portal differs from its selected u/2 by at most

    epsilon+|F(tau_L)| < gamma/2.

Thus both portals remain strictly in(0,u). Also |tau'-tau_L|<=3gamma/[8A(L)] tends to0, so tau'>0 for all sufficiently large L. The indices remain the same; no endpoint sheet or winding word is changed during this correction. Equation(1) is now satisfied, including actual target matching.

The irrational proof supplies qualitative eventuality. Its convergence rate depends on the fixed irrational ratio and is not asserted computable for arbitrary encoded reals. No uniform bound over all rate ratios follows from character-by-character convergence.

## 4. Full actual geometric realization

For either branch, launch from actual S horizontally left with vertical sign sigma_s and absolute speed ratio tau. In its tooth unfolding, use source ordinate sigma_s*b_s and final unfolded height2u*k_s+r_s. If sigma_s=+1 the horizontal tooth-wall contacts are j=1,...,2k_s; if minus they are j=0,...,2k_s. Their physical coordinates are

    (c+D_s-(j*u-sigma_s*b_s)/tau, u if j odd else0).

Every time is strictly positive, including the first j0 minus contact b_s/tau. Every contact has x>c, because its unfolded ordinate is strictly less than the terminal2u*k_s+r_s. It lies left of the actual S and the far tooth end. The physical outgoing vertical velocity at the strict mouth(c,r_s) is upward for both signs.

Join this mouth to(c,H-r_t) through the single smooth left-wall point

    (0,r_s+c*tau).

Equation(1) makes the two slopes match exactly. The left contact lies strictly between the portal heights, since tau>0; both portal heights are strictly in their selected bands. Both open central legs have x<c, and therefore avoid EVERY extra tooth mouth, newly created reflex corner and removed side mirror. No artificial horizontal spine cut is a reflection. The y-reflected reverse of the analogous upper tooth path reaches the actual T with the required right/up velocity. All tooth contacts are strictly at x>c, so neither a true mouth corner nor the artificial-cut flaw of A29 can occur.

The total reflection count is2k_s+2k_t+1+[sigma_s=-1]+[sigma_t=-1], finite for each L. Lower arm legs stay in the lower selected band; middle legs have x<c; the final arm x coordinate increases monotonically to T. Thus there is no earlier target substitution or reflected-sheet-only arrival. Each claimed path is actual and corner avoiding.

## 5. Exact contribution and limits

This supplies a first actual path and an eventual tail on EVERY fixed positive real horizontal-rate ray for two equal-height selected comb teeth, including rationally resonant, irrational and extremely unequal fixed rates. The depth offsets, vertical mark offsets and other teeth are arbitrary as stated. It extends the equal-growth premise of the prior first-witness result; it is not a provided-witness propagation lemma.

Finite prefixes, varying tooth heights, a cutoff uniform over ALL growth-rate ratios, and the full two-independent-depth orthant are NOT proved. Pointwise eventuality on all rays does not imply a compact or finite exceptional parameter set. The universal canonical45 W<=21 theorem remains open. There is no novelty claim.
