# Exact physical constraints for the complete monotone-height vertical-wall class

Status: HAND reviewer prerequisite pending reciprocal review. This is a necessity/sufficiency description and finite native arithmetic reduction for ONE RESTRICTED optical class. It is NOT an all-metric existence theorem and is not a new search engine. Author's possible floor/roof/step-horizontal itineraries remain outside this class and must not be discarded.

## Scope and endpoint conventions

Let integral widths w0>w1>w2>w3>0 and0=y0<y1<y2<y3<y4=H define the phase's actual ten-wall nested room. Reverse S,T if needed so u=S_y<=v=T_y. If u=v, the direct horizontal segment lies inside the room's horizontal interior section. If both endpoints lie in the same band, their direct segment lies in its convex rectangle; no reflection on an internal horizontal cut is needed.

For u<v assign every mark on an internal seam to the narrower UPPER band. Thus S=(s,u) in band i and T=(t,v) in band j satisfy0<s<wi,0<t<wj, i<=j. Native even-even marks have integer heights, and all travel-height differences below are integers. A physical interior mark at seam y_l has0<x<w_l. The points x=0 and x=w_l at that seam are not interior marks. This differs from a ray's permissible ordinary wall contact at x=0.

Consider only rays with vy=+1, initial horizontal sign sigma in{-1,+1} and horizontal speed tau>0, having no horizontal-wall reflection before actual T. Then y increases strictly; every visited band is crossed once, in order. Include the vertical direct path tau=0 separately when it is legal.

## MC01: signed portal recursion is necessary and sufficient

Write F_w(z)=min(z mod2w,2w-(z mod2w)), the triangular fold. Define C_i=0. In source band i the actual x coordinate is

    x(y)=F_wi(s+sigma*tau*(y-u)).

For each crossed seam y_l, l=i+1,...,j, define the old developed phase

    Z_l=s+sigma*tau*(y_l-u)-C_(l-1).

A legal upward passage is possible exactly when some integer k_l satisfies

    r_l=Z_l-2k_l*w_(l-1), |r_l|<w_l.

Equivalently F_w(l-1)(Z_l)<w_l. The center k_l is UNIQUE when the strict guard holds, because w_l<w_(l-1). Set

    C_l=C_(l-1)+2k_l*w_(l-1).

In the next band use x(y)=F_wl(s+sigma*tau*(y-u)-C_l). The SAME sigma and tau are retained everywhere, not independently reselected at a seam. At that seam both folds reduce locally to |r_l|, so actual position and incoming/outgoing velocity match. If r_l!=0 it is a transparent interior passage with0<x<w_l. If r_l=0 it is the single ordinary reflection on the continuous original maximal left wall. Both neighboring formulas implement its same outgoing germ. It is not an artificial seam reflection.

Why the guard is exact: x>w_l hits the actual horizontal step and reverses vy, so leaves the admitted monotone class. Equality x=w_l is a forbidden true reflex corner; old x=w_(l-1) is the other true ledge endpoint. The strict bound also excludes that old endpoint. x=0 is a smooth left-wall point because all seams lie strictly between the actual left-wall endpoints0,H. These exhaust the seam possibilities for this class.

After the last seam require

    F_wj(s+sigma*tau*(v-u)-C_j)=t.

It is actual T, including a target exactly on y_j. Because height increases strictly, this is its first hit. Between seams the folds reflect only on original finite vertical walls, and their only endpoint heights are the guarded seams or room floor/roof outside the interior endpoint height range. No other genuine corner can occur. A finite tau, finite heights and positive widths imply finitely many contacts. Thus the recurrence and target equation suffice for one actual finite corner-free ray; conversely every ray in this class has precisely these folds and guards. This does not assert that every illuminating ray belongs to the class.

## MC02: necessary native target-image resonance

Put D=v-u>0 and g=gcd(w_i,...,w_j). Every C_j is in2gZ. Therefore a necessary actual-target condition is

    s+sigma*tau*D in {+t,-t}+2gZ,
    tau=(eta*t-s+2g*n)/(sigma*D), eta in{-1,+1}, n integer.

Both target images AND both initial horizontal signs must be retained. One cannot substitute arbitrary independent per-band target residues. This condition is not sufficient without every MC01 guard. Native even-even s,t and integer walls imply rational tau; in particular tau*D is an even integer. The gcd condition may be sharper than parity alone.

## MC03: a complete slope period for this restricted native class

Let P=2lcm(w_i,...,w_j). For the SAME initial sigma, adding P to nonnegative tau preserves every crossed-seam position and horizontal sign, all strict seam/corner conditions, and actual target attainment. It can change the number of ordinary vertical-wall bounces, which must be reconstructed rather than copied from an old word.

Proof. Every cumulative seam travel height T_l=y_l-u is an integer. Set C_l'=C_l+sigma*P*T_l. The new seam residual is exactly r_l. Its recursion is legitimate since

    C_l'-C_(l-1)'=(C_l-C_(l-1))
        +sigma*P*(y_l-y_(l-1))

is again an even multiple of the preceding width. For the first seam, use T_i=0 in this formula, representing the ACTUAL source height u rather than y_i. At actual target the extra phase is sigma*P*(v-y_j), also a full2w_j period (for i=j the direct whole-source-band cancellation uses D instead). All those heights are integral. Between seams extra bounces remain ordinary for the reason given in MC01. This proves period preservation for the entire restricted class, not a finite empirical reflection cutoff or an affine transport assertion for arbitrary physical words.

At tau=0, treat physical direction as vertical; if the recurrence succeeds it is the ordinary direct vertical segment. The sign sigma is then redundant. No invented zero-speed wall germ is used.

Consequently, for any fixed native input, COMPLETE monotone-class feasibility reduces to checking the candidate slopes from MC02 in0<=tau<P, with both sigma and eta, and then the deterministic MC01 guards. Each(sigma,eta) has D*P/(2g) residues moduloP, so there are at most2D*P/g candidates before duplicates. This finite number depends on the unbounded metric data. It is not a wall-only cutoff, a universal direction bound, a claim that some candidate passes, or permission to run a census. No such enumeration is implemented or run here.

## Frozen control calibration, by hand

For widths40,12,8,4 and S38,2/T2,38, the explicit verified initial sigma=-1,tau=3 ray has C1=0,C2=0,C3=-16. Seam residuals are8,-4,0, satisfying |r1|<12,|r2|<8,|r3|<4. At T the final phase is38-3*36-(-16)=-54, with F4(-54)=2. The overall unfolded x is-70=2+8*(-9), consistent with g4 and D36; P=240. The zero third residual is the legal smooth left-wall contact(0,20), as the exact170guard/16reflection prescribed path already verifies. No new direction was replayed in deriving MC01-MC03.

## What this permits an independent reviewer to conclude

A proposed monotone vertical-wall construction must satisfy this signed recurrence, the actual target equation and the exact seam convention. A claim to refute the COMPLETE monotone class must cover all candidate residues at the justified input-dependent period, both initial/target signs, and possible smooth-wall seam bounces. Failure of nearest-window selection or one sign is insufficient. Failure of the entire restricted class still would not imply darkness, since horizontal step/floor/roof reflections are outside it.

This packet deliberately does not duplicate the author's all-metric window/floor/roof construction or claim a new universal positive result. It supplies a physical completeness/quantifier audit prerequisite while that candidate is pending. All metric and endpoint cases outside the accepted prior sufficient classes remain unresolved at their recorded scopes. No search, fitting, new engine, worker, clock reset, frozen edit or git mutation.
