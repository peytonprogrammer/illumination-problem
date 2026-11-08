# TR04: non-overlapping spiral arms and the transposed wide-room theorem

Predeclared positive extension. Parameters now satisfy

    0<a<w<A, 0<l<w,
    0<b<h<H, 0<c<h,
    a<l OR c<b.

P has the same ten-vertex cycle as TR01. The last disjunction is required for strict simplicity; it permits the bottom arm to extend left of the source column only when their height ranges are disjoint. This is an explicitly quantified normal-form class, not a claim that every (1,1,8) polygon has already been normalized to it.

Define the vertical threshold delta_v exactly as TR03:

    R_v=A-w, L_v=R_v/(2c),
    Ns_v=ceil(L_v*h/(2a))+1,
    Nr_v=ceil(L_v*h/(2R_v))+1,
    delta_v=L_v/(Ns_v+Nr_v+1).

Claim: every distinct actual interior pair in P illuminates if either

    H >= c+2A/delta_v,

or the transposed condition holds:

    R_h=H-h, L_h=R_h/(2a),
    Ns_h=ceil(L_h*w/(2c))+1,
    Nr_h=ceil(L_h*w/(2R_h))+1,
    delta_h=L_h/(Ns_h+Nr_h+1),
    A >= a+2H/delta_h.

The statement is arbitrary-real; integral canonical45 rooms with actual even-even endpoints are included. There is no reflection-count bound or source/target restriction.

Proof obligations before acceptance: re-prove the genuine-wall coverage after replacing raw x<a membership by the actual left column x<a,y>b; verify all additional original corners when b,c or a,l change order; retain actual first T in the new overlap-in-x case via vertical separation c<b; check transposed parameters and actual endpoint mapping. The old frozen TR01/TR03 statements are not silently widened.

Expected discriminator: sufficiently wide ordered rooms can satisfy the second condition while failing the old tall-roof criterion. This is an additional entire metric class, not merely renaming accepted tall rooms in their original coordinates.

This does not close all metrics of (1,1,8), all r3 or r<=8. Hand proof and prescribed checks only; no discovery clock or process started, and no old clock renewed.
