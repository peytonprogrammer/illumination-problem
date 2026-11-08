# A horizontal witness cutoff uniform over vertical separation

R32 candidate for independent review. This strengthens the independently accepted R31 first-witness theorem by removing its fixed-H restriction on the horizontal cutoff. The literal vertical-neck decomposition and joint finite-prefix join are owned by the existing peer; they are not assumed proved here.

## 1. Exact quantified statement

Keep fixed c,u,v,d_s,d_t,b_s,b_t with c,d_s,d_t>0, 0<b_s<u,0<b_t<v and commensurate u,v. Let M_min>0. The selected lower/upper teeth have bands[l,l+u] and[l+H-v,l+H] in an actual rectangular-spine comb, where

    H>=u+v+M_min.

The spine contains both bands. Other teeth may lie anywhere outside those selected open bands, below/between/above, with any right-end lengths and any changing vertical positions consistent with a strictly simple comb. The actual marks are

    S=(c+d_s+L,l+b_s), T=(c+d_t+L,l+H-b_t),
    L>=0.

Their actual tooth ends remain strictly beyond them. Then an EXPLICIT cutoff L_bar, depending only on the fixed listed data and M_min, ensures actual illumination for EVERY L>=L_bar and EVERY such H and intervening tooth configuration. The cutoff is independent of H. Rational data give a rational computable cutoff.

This is not uniformity over changing c,u,v,offsets or depth difference, all newly created marks, arbitrary chamber shapes, or all W<=21 rooms. No finite prefix is declared illuminated.

## 2. Uniform strict portal margin, including equality phases

Use R31 notation

    Delta=d_s-d_t, z=Delta/(2c),
    u=p*g, v=q*g with coprime positive integers p,q,
    U=uv/g, P=2g,
    f(r_s,r_t)=(1+z)r_s+(-1+z)r_t,
    f((0,u)x(0,v))=(I_-,I_+), W=I_+-I_->=P.

Its phase equation is f=delta+zH-P*n with delta=sigma_s*b_s-sigma_t*b_t. R31 establishes the equality classification and actual meaning of every term.

If W>P, set

    mu=(W-P)/4>0.

The trimmed interval(I_-+mu,I_+-mu) has length(W+P)/2>P. Every residue modulo P therefore has a representative in that interval, for any H, using sigma_s=sigma_t=+1 if desired. Its distance from either endpoint of the untrimmed interval exceeds mu.

If W=P, R31's equality cases supply a primitive-height tooth: u=g when u=v=g or z1, or v=g when z-1. Let b_* be that tooth's actual interior mark offset. Flipping just its sign shifts the phase by d=2b_* in absolute value, with0<d<P. Put

    mu=min(d,P-d)/4>0.

On the phase circle of circumference P the excluded endpoint classes for the two sign choices have circular separation min(d,P-d). Their mu-neighborhoods cannot intersect, because2mu is half that separation. Consequently for EVERY H at least one of these two phases has a representative at distance >=mu from BOTH endpoints of(I_-,I_+). The argument includes exact resonances and does not assume generic H or continuity of the chosen word/signs.

In either case choose such a representative and interpolate the opposite extremal corners of the portal rectangle, as in R31. The interpolation parameter lies between mu/W and1-mu/W. Therefore all four portal margins are at least the SAME positive constant

    rho=min(u,v)*mu/W:
    r_s*,u-r_s*,r_t*,v-r_t* >= rho.                         (7)

This constant is independent of H, although the chosen signs, representative n and portal point may change with H.

## 3. Uniform slope matching and actual winding positivity

Write

    t_min=M_min/(2c)>0,
    a_s=(Delta-2c)/2, a_t=-(Delta+2c)/2,
    A=max(|a_s|,|a_t|),
    eta=min(t_min/2,rho/[2(A+1)]),
    L_bar=max(U/eta+1,4max(u,v)/t_min+1).                    (8)

For each H select the strict portal pair above, and put tau*=(H-r_s*-r_t*)/(2c). Since H>=u+v+M_min, tau*>t_min (the weak >= would also suffice).

Use exactly R31's Bezout base and nearest-integer winding parameter, which may depend on H:

    k_s=k_s^0+q*h, k_t=k_t^0+p*h,
    tau=(C0+4U*h)/(D0+2L), D0=d_s+d_t+2c.

Nearest rounding always gives |tau-tau*|<=2U/(D0+2L). For L>=L_bar this is strictly less than eta. R31's affine portal identities have derivatives a_s,a_t independent of H. By(7),(8), the new offsets remain strict, in fact with margins >rho/2. Also tau>=t_min/2>0.

The H-dependent Bezout base does NOT force an H-dependent positivity threshold. Use the exact physical portal equations instead:

    2u*k_s=sigma_s*b_s+(L+d_s)*tau-r_s
           > -2u+L*t_min/2 >0,
    2v*k_t=sigma_t*b_t+(L+d_t)*tau-r_t
           > -2v+L*t_min/2 >0.

The last inequalities follow directly from(8). Thus both indices are positive integers for every allowed H. No bound on the Bezout representative n, its signs, the number of reflections or H is required. This is the key uniformity step; a bound on h_min from R31 would have introduced spurious dependence on H.

R31's actual construction now applies: every tooth contact is at x>c, portals are strict, the central two legs stay in x<c and use one smooth actual x0 reflection between the two portal heights, and the reversed final tooth leg reaches the ACTUAL target. Extra teeth and their changed corners remain untouched. There are no reflections on artificial horizontal cuts, no ghost mirrors and no modulo-endpoint substitution.

## 4. Remaining placements and what a joint-prefix application still needs

R31's source-in-spine/target-in-tooth formula requires only D=d_t+L>c+x_s. Therefore L>2c is a uniform sufficient threshold over all allowed vertical separations, source heights, tooth heights and vertical offsets in that mixed case. The source and chosen portal heights remain inside the actual spine, so their left-wall contact is smooth even when they move vertically. Both-spine, same-tooth and two-mouth-seam cases already illuminate without a large-L hypothesis. These observations do not add a uniform bound over arbitrary new marked points in the two-tooth case; its fixed offsets/heights/depth difference remain premises.

For a rational actual two-parameter comb family L=2n and H=H0+2m, a useful CONSEQUENCE is conditional on the following separately checked geometry: each fixed n gives a literal admissible one-vertical-neck family, whose cut lies between the actual marked chambers and crosses only the spine. The accepted one-neck theorem would then give a vertical tail at each of the finitely many n with2n<L_bar. Its accepted rational open-beam algorithm would compute those tail thresholds. Together with the H-uniform horizontal tail, this would leave a computable finite possible-dark rectangle.

The uniform theorem proved here does not rely on that application. The peer owns verification of the literal neck decomposition, all fixed-coordinate hypotheses and the joint finite-prefix join. The rectangle's entries would still need actual illumination certificates. If the vertical gap does not separate the marked chambers, or cuts a tooth rather than the bare spine, that application cannot be silently substituted.

## 5. Reproducible evidence and limits

comb-uniform-joint-growth-check.py loads only definitions from the frozen reviewer R31 checker, not its top-level writer or any peer program. Twelve prescribed actual path controls test four fixed parameter sets at minimum, rationally perturbed and larger H, with the SAME L_bar for each set. They include both primitive-width equality mechanisms and unequal heights/depths. All2982 actual reflections and47904 wall/leg guards pass. Eight additional exact algebra controls at H increments10^6 and10^12+1/11 verify strict portal equations and integer positivity, but deliberately do not materialize or replay the huge finite trajectories. These are labeled arithmetic controls, not actual path audits.

The all-H and all-large-real-L quantifiers come from the uniform hand argument. This is a first-witness theorem and a genuine independently moving-separation extension in the stated comb class, not a supplied-witness propagation result. It leaves the finite prefix, general intersecting strips, changing mouth heights, nonrectangular chamber trees and full uncapped canonical45 W<=21 illumination OPEN.
