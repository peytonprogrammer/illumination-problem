# Finite-prefix path certificates using genuine spine ends

R33. Exact finite arithmetic criterion for a specified positive path class, plus actual repairs of two shallow controls. This does not solve the arbitrary finite prefix, prove all combs illuminate or exhibit darkness. All work used the original recorded840-second deadline.

## 1. Actual path class and its two target orientations

Use an actual rational-coordinate comb with spine[0,c]x[0,H_g], selected bands[l_s,l_s+u] and[l_t,l_t+v], l_s+u<l_t, and actual marks

    S=(c+D_s,l_s+b_s), T=(c+D_t,l_t+v-b_t),
    D_s,D_t>0, 0<b_s<u, 0<b_t<v.

Their tooth ends lie strictly beyond the marks. A certificate first travels left through the source tooth, makes ONE horizontal turnaround at the genuine spine wall x0, and then travels right through the target tooth. It may reflect arbitrarily often on the actual spine floor/ceiling and on the selected tooth's horizontal walls. It initially excludes a far right tooth-end reflection. Extra teeth are irrelevant because the middle has x<c, and the two selected prefixes have x>c before their strict mouth crossings.

There are two legitimate target-unfolding orientations. Write e=+ or-, and define

    H_+=l_t+v-l_s, b_+=b_t,
    H_-=-l_t-l_s, b_-=v-b_t.

For signs sigma_s,sigma_t, integers k_s,k_t,j and tau>0 seek

    r_s=sigma_s*b_s+D_s*tau-2u*k_s in(0,u),
    r_t=sigma_t*b_e+D_t*tau-2v*k_t in(0,v),
    r_s+r_t+2c*tau=H_e+2H_g*j.                             (1)

After adding sufficiently many common periods below, require k_s,k_t,j>=0. For e+, the physical target portal is P_t=l_t+v-r_t and its spine image is P_t+2H_g*j. For e-, the physical target portal is P_t=l_t+r_t and its image is -P_t+2H_g*j. The source portal is P_s=l_s+r_s in both cases. Equation(1) gives

    image(P_t)-P_s=2c*tau.

The e- target prefix is the reversed, unreflected local tooth construction with target offset v-b_t; it enters the target tooth with downward velocity. The e+ prefix is vertically reflected and enters upward. Thus e- is a real missing path mode, not merely a different target sheet chosen after constructing a ray.

The lower tooth unfolding and its contact indices are exactly those in accepted R31. Its contacts are strictly at x>c. The central physical curve, parametrized by unfolded horizontal travel d in[0,2c], is

    x(d)=|c-d|, y(d)=F_Hg(P_s+tau*d),

where F_Hg folds with period2H_g onto[0,H_g]. At d=c there is one x0 reflection. All other central reflections are on actual y0/H_g walls with0<x<c. No artificial mouth cap is used.

There is no simultaneous spine corner hit. For e+, the developed height at x0 is(P_s+P_t)/2+jH_g, with its initial average strictly between0 and H_g. For e-, it is(P_s-P_t)/2+jH_g. Since the selected physical portals are in disjoint ordered bands, -H_g<P_s-P_t<0; its half is strictly between-H_g/2 and0. Neither case is a multiple of H_g. Every central contact is therefore smooth.

## 2. An exact FINITE decision of these displayed certificate classes

For positive rational q_i, let gcd_Q and lcm_Q denote their positive rational gcd/lcm: integerize by a common denominator, or use gcd of numerators/lcm of denominators for gcd_Q and the reverse for lcm_Q. Define

    g0=gcd_Q(u,v,H_g), D=D_s+D_t+2c,
    K=lcm_Q(2u/D_s,2v/D_t,H_g/c),
    N=D*K/(2g0), a positive integer.

For each e and each of the four sign choices, ANY solution of(1) has slope

    tau_l=(H_e-sigma_s*b_s-sigma_t*b_e+2g0*l)/D, l in Z.    (2)

Conversely, at any such slope take the residues

    r_s=(sigma_s*b_s+D_s*tau_l) mod2u,
    r_t=(sigma_t*b_e+D_t*tau_l) mod2v.

If BOTH are strict as in(1), their unique winding integers are obtained by division. Check whether

    j=(r_s+r_t+2c*tau_l-H_e)/(2H_g)

is an integer. These conditions are sufficient for the displayed actual path, once the winding indices and slope are made positive.

Only l0,...,N-1 need checking. Increasing tau by K changes the indices by

    Delta k_s=D_s*K/(2u), Delta k_t=D_t*K/(2v),
    Delta j=c*K/H_g,

all positive integers. Portal residues and the integrality of j do not change. Also D*K/(2g0) is an integer: D_s*K/(2g0),D_t*K/(2g0),c*K/g0 are integers because u/g0,v/g0,H_g/g0 and the displayed increments are integers. Thus(2) modulo K has exactly N representatives. Every integer solution reduces to one representative, and any successful representative can be shifted by enough positive K to make tau positive and all three indices nonnegative.

This is a complete finite equivalence for equations(1) and their actual positive realization. It is NOT a darkness decision: genuine paths may make a far-tooth-end reflection, return across x=c more often, or use other branches. The algorithm returns actual certificates when positive and only a restricted mechanism rejection when negative.

## 3. The A29 shallow control is genuinely repaired

For the author's A29 example c=u=v1,D_s=D_t1/2, bands[2,3],[8,9], actualS=(3/2,7/3),T=(3/2,25/3), global spine height11, choose

    e+, sigma_s=sigma_t+, tau36,
    k_s=k_t9, j3, r_s1/3,r_t2/3.

The equations hold exactly. The spine-end path has43 ordinary reflections. Own all-wall checking validates every contact and actual target. Scaling by12 gives the actual canonical16-wall A-pair control(18,28),(18,100), still illuminated. Its previous no-spine-end candidate remains invalid; the positive new path uses actual spine-end mirrors.

The e+ branch alone is insufficient in general. With spine height8, same c,u,v,depths/source offset, selected bands[2,3],[4,5] and actual target(3/2,13/3), the e+ criterion has no certificate. The e- branch gives

    sigma_s=sigma_t+, tau40/9,
    k_s=k_t1,j1,r_s=r_t5/9.

Its6-reflection actual path is checked independently, including the true spine ceiling hit and downward final tooth entry. Omitting the e- orientation would falsely reject this positive mode.

## 4. Both spine orientations still do not close arbitrary prefixes

A stronger exact restricted countercontrol has

    c2,u1,v4,D_s1/2,D_t1,
    b_s4/5,b_t16/5, selected bands[2,3],[7,11], H_g16.

Take the full actual comb with four tooth bands[0,1],[2,3],[7,11],[15,16], all right ends5. Its actual marks are(5/2,14/5),(3,39/5), strictly in their selected teeth. For this input g0=1,D=11/2,K8,N22. Every e/sign class has22 slope representatives. Exact independent literal enumeration of all176 possibilities rejects them: at least one strict portal or the integer spine-image equation fails. Thus this displayed certificate program cannot prove every arbitrary rational/canonical prefix.

All coordinates and marks become canonical/A after scaling by20: the actual marks are(50,56),(60,156), with a strict sixteen-wall integer axial boundary. This is NOT a dark pair. Indeed a13-reflection actual path exists after using the two actual far tooth ends.

For this positive repair each actual tooth width is w3. Reflect its actual mark across the far support once before unfolding toward the spine. This changes its effective horizontal depth to

    D_s^*=2w-D_s=11/2, D_t^*=2w-D_t=5,

while preserving the ACTUAL source and target by folding horizontally in the physical tooth. Use

    e+, sigma_s=sigma_t+, tau42/29,
    k_s4,k_t1,j0,r_s111/145,r_t354/145.

The matching equations are exact with those effective depths. At each far wall the corresponding unfolded vertical height is not a multiple of its tooth height, so no far corner is contacted. Every other tooth contact has x>c and every central open leg has x<c. The actual source and target after both horizontal folds are the original marks. All13 reflections and every actual-wall incidence are checked; after scaling by20 the same path reaches the actual A target.

This repair does not prove that adding these extra choices always works. It identifies the next positive completeness obligation: arbitrary finite-prefix witnesses may need genuine tooth-end reflections as well as spine-end reflections. No failure of a prescribed path program is darkness.

## 5. Evidence and disciplined scope

Own scripts contain no imported author optical code. The first positive control is checked at its rational and scaled canonical geometry (43 reflections each). The e- and far-end controls are checked in comb-spine-end-actual-controls.py, including source/target folds and the far-corner guards; the far-end path is also checked after20 scaling. The no-far-end countercontrol is exhausted exactly in176 slope residue checks, independently of the discovery loop.

Bounded proof-question discriminators, all under the ORIGINAL R33 deadline, tested696 integer-A patterns for e+ only (positive controls, no theorem), found an e+-only rational failure after7 patterns, tested972 rational patterns with both orientations (positive controls, no theorem), then found the two-orientation restricted failure at pattern112 of the recorded seed3301 challenge. Each scan stopped at its stated bound or first counterexample; no restart extended the840-second effort. No unsuccessful scan was classified dark.

Independent review of the finite criterion, all mirror/endpoint guards, exact residue rejection and positive repairs remains required. Universal W<=21, all-comb illumination, full finite-prefix coverage and arbitrary strip-family completeness remain OPEN.
