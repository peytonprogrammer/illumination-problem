# Two source phases repair genuine inner-mouth corner equalities

R30 supplement under the SAME original840-second deadline; the frozen main proof remains unchanged. Candidate for independent review.

Let the actual comb have spine [0,c]x[y_min,y_max] and any number of disjoint right teeth. Choose ANY two teeth of the same height u, the lower band [l,l+u] and upper band [l+H-u,l+H], with H>2u. Other teeth may lie below, between or above. Let their actual marks be

    S=(c+D,l+b_s), T=(c+D,l+H-b_t),
    0<b_s,b_t<u, delta=|b_s-b_t|,
    D>=c*(u+delta)/(u-delta).

Each selected tooth end must be strictly beyond c+D. Then the actual marks illuminate. Unlike the first floor construction, neither chosen tooth need be extreme in the entire room. This remains a sufficient class, not arbitrary tooth heights, depths or all marked pairs.

Set p=2uc and

    Z_+=c*min(b_s,b_t)+D*(H-delta)/2,
    Z_-=-c*max(b_s,b_t)+D*(H-delta)/2.

Both are positive. For the minus case, H>2u and the depth bound give

    D*(H-delta)/2 > c*(u+delta)*(u-delta/2)/(u-delta) >= cu > c*max(b_s,b_t).

The middle inequality follows after multiplying by u-delta>0; its excess over u has numerator (3u*delta-delta^2)/2>=0. Moreover

    0<Z_+-Z_-=c*(b_s+b_t)<2uc=p.

Thus Z_+ and Z_- cannot BOTH be integer multiples of p. Choose sigma=+1 if the positive residue Z_+ mod p is nonzero; otherwise choose sigma=-1. For that sign put

    k=floor(Z_sigma/p),
    tau=(H-sigma*(b_s+b_t)+4uk)/(2(c+D)),
    r_s=sigma*b_s+D*tau-2uk,
    r_t=sigma*b_t+D*tau-2uk.

All choices are finite and explicit, with k>=0,tau>0. As in the frozen main proof,

    min(r_s,r_t)=(Z_sigma-pk)/(c+D),
    0<min(r_s,r_t)<p/(c+D)<=u-delta,
    max(r_s,r_t)<u,
    r_s+r_t+2c*tau=H.

Both portals are now STRICT interiors even when the actual mouth ends are genuine reflex corners.

For sigma=+1, use the main proof's lower contacts j=1,...,2k. For sigma=-1 launch initially downward; represent its reflected source at height -b_s in the tooth's vertical unfolding. Use contacts

    (c+D-(ju-sigma*b_s)/tau, l+(u if j odd else0)),
    j=0,...,2k.

The j0 contact has positive travel distance b_s/tau. All contacts lie strictly at x>c because the last unfolded height2uk is strictly below the terminal height2uk+r_s, and all lie left of the actual source/far end. The last outgoing vertical velocity is upward: the minus launch is reversed an odd2k+1 times. With k0 it makes exactly one smooth floor reflection, not a zero-length segment. The plus branch makes2k reflections.

Join through the actual spine at the smooth left-wall point

    (0,l+r_s+c*tau),

then use the y-reflected reversed upper-tooth construction with offset b_t. The spine segment lies strictly between its two strict portal heights and has x<c except at crossings; every intermediate, lower or upper extra tooth is irrelevant. Its left contact is strictly between l and l+H, hence away from the global spine corners even when selected teeth are extreme. No horizontal cut through the spine is treated as a mirror. The final actual T and all velocities match exactly.

The reflection count is4k+1 for sigma+ and4k+3 for sigma-. Earlier target arrival is excluded by the same horizontal/vertical monotonicity split as in the main proof.

For the frozen16-wall countercontrol (spine[0,4]x[0,64], selected bands[10,14] and[50,54],S8,12,T8,52), plus gives the rejected zero portal. Minus gives k2,tau5 and r_s=r_t2, hence an actual eleven-reflection path with strict inner-mouth crossings. This repairs that proposed witness, without retroactively making its original corner path legal.

The independent reviewer script protected-comb-phase-check.py validates five prescribed actual polygon paths, including the repaired16-wall control, unequal offsets at the sufficient-depth equality, rational geometry, a plus branch, and the minus branch with k0. All71 reflections and1216 all-wall/leg guards pass. These controls corroborate the hand proof and are not its arbitrary-parameter justification. No discovery scan or author-file edits were used. Universal W<=21 and the remaining arbitrary marked strip fibers remain OPEN.
