# A finite construction connecting arbitrary upper-arm marks in a U room

[in progress] 2026-11-01. The new opposite-arm proposition (§1–4) is accepted by a separate tools-disabled Opus symbolic audit (`all-heights-peer-review.txt`). The all-interior-pair corollary additionally uses the previously accepted L-room theorem; the separate reviewer treated that unreproduced dependency as conditional. Live coordinating-peer review of this new proof is pending. This is an illumination theorem, not yet universal singleton-blocker removal or a novelty claim. No optical/direction discovery search.

## Geometry and statement

Let a,b,M,c>0, H_L,H_R>c, and A=a+M+b. The room is the simple polygon with vertices

    (0,0),(A,0),(A,H_R),(a+M,H_R),
    (a+M,c),(a,c),(a,H_L),(0,H_L).

Take s=(x_s,y_s) with0<x_s<a and c<=y_s<H_L, and t=(a+M+x_t,y_t) with0<x_t<b and c<=y_t<H_R. The arms may have different widths/heights, and the marks may have different horizontal offsets and heights.

There is a finite corner-free connecting billiard path reflecting exactly once at the bottom wall and otherwise only at vertical walls. It crosses the lower passage2k+1 times for an explicitly chosen finite integer k. The bottom reflection stays strictly within(M/2,A-M/2), so it cannot hit an outer corner. All roofs and the notch wall are avoided.

## 1. First admissible arm lengths

Use horizontal unfoldings initially directed toward the passage on each side. The available left and right-backward lengths are

    L_n=a-x_s+2na,   R_m=x_t+2mb,  n,m>=0.

For tau>0 let L(tau) be the first L_n strictly above(y_s-c)tau, and R(tau) the first R_m strictly above(y_t-c)tau. Both are nondecreasing right-continuous step functions. Set S=y_s+y_t and

    ell_s=L(tau)-(y_s-c)tau in(0,2a],
    ell_t=R(tau)-(y_t-c)tau in(0,2b].

A remainder equals its upper bound only at a jump. Explicitly choose index max(0,floor((threshold-base)/period)+1).

## 2. Finite monotone matching construction

Choose tau0>2max(a,b)/c and choose k>=0 such that

    B=M+2kA > 2c*tau0.

Define H(tau)=[L(tau)+R(tau)+B]/S and iterate tau_{n+1}=H(tau_n).

Initially H(tau0)>tau0, because

    S*tau-L(tau)-R(tau)=2c*tau-ell_s-ell_t <=2c*tau.

H is nondecreasing, so the iterates remain nondecreasing. They are bounded by

    tau_max=(B+2a+2b)/(2c),

because H(tau_max)<=tau_max. On this bounded interval, only finitely many arm-length pairs occur. Hence only finitely many H values occur; the nondecreasing iteration reaches a fixed value tau_* after finitely many steps.

The fixed value is strictly between jumps. Let tau_n be the first stationary iterate. Its index satisfies n>=1, and tau_n>tau_{n-1}. If L jumps at tau_n, then L(tau_{n-1})<=L(tau_n)-2a, while R(tau_{n-1})<=R(tau_n). Thus H(tau_{n-1})<H(tau_n)=tau_n, contradicting tau_n=H(tau_{n-1}). The same argument applies to a jump in R. The initial iterate cannot be stationary by strictness above.

Consequently0<ell_s<2a and0<ell_t<2b at tau_*. Write tau=tau_*, L=L(tau), R=R(tau), beta=1/tau. The fixed equation gives

    S*tau=L+R+B.

## 3. Strict portals and legitimate arm reflections

The portal heights are

    u=y_s-beta L=c-ell_s/tau,
    v=y_t-beta R=c-ell_t/tau.

They lie in(0,c), because tau>tau0>2max(a,b)/c. Also

    u+v=B/tau.

Every earlier left inner-wall encounter is at least2a units before the portal and has height at least

    u+2a/tau=c+(2a-ell_s)/tau>c.

The right-backward test is identical with b,ell_t. Therefore no earlier encounter is an accidental passage exit or a reflex-corner hit. All arm heights are positive and no larger than the corresponding mark height, so roofs and bottom corners are avoided. Outer-wall encounters in each arm are smooth.

At the left portal the horizontal velocity points right and the vertical velocity down. At the right portal the reverse target path points left/down, so the forward continuation must point right/up. These are the velocities provided by the lower-strip construction below.

## 4. Lower-strip continuation and the missing corner check

For horizontal developed distance0<=d<=B from the left portal, use

    X(d)=a+d,
    Y(d)=u-d/tau,
    physical coordinates=(F_A(X(d)), |Y(d)|),

where F_A folds a coordinate into[0,A] with period2A. The start is(a,u). Since a+B=a+M+2kA, the endpoint is(a+M,v) with positive horizontal velocity. Its developed vertical coordinate is-v. The physical vertical coordinate stays strictly below c and vanishes exactly once, at d0=u*tau in(0,B).

The developed bottom coordinate is

    X0=a+u*tau
      =a+M/2+kA+(ell_t-ell_s)/2.

Since0<ell_s<2a and0<ell_t<2b,

    kA+M/2 < X0 < kA+A-M/2.

Thus X0 is not a multiple of A. The interval(M/2,A-M/2) is invariant under reflection x->A-x, so either parity of k yields physical x in this interval. The bottom hit is strictly away from both outer corners. Every outer-wall reflection in the lower strip has nonzero height and lies below c. There are finitely many, and all are smooth. At the two portals the strip and arm velocities match. At the unique bottom hit vertical velocity reverses, and at every vertical wall horizontal velocity reverses. This completes the proof.

## 5. Consequences and limitations

Every pair of interior points in a U room is illuminated. Opposite high-arm points use this construction. Two points in one arm, or with at least one strictly below c and both at height at most c, have direct visibility. Opposite-arm points on the level y=c are included in the construction. A high-arm point and a lower-rectangle point lie in the corresponding L subroom and use the previously proved vertical-only monotone [L construction](../single-boundary-blocker/l-monotone-proof.md), already accepted by both coordinating agents and by a separate symbolic reviewer. That construction touches no artificial horizontal wall of the subroom, so remains valid in the U room.

For the opposite-arm case, every horizontal boundary blocker except the constructed bottom hit is avoided. A prescribed blocker at that hit, or a vertical-wall blocker, still needs a second suitable connection. Changing phases/k supplies more candidates, but no empty-common-contact theorem is asserted here for arbitrary asymmetric U rooms.

This proves the all-height matching and corner-avoidance step. It does not establish the global22wall minimum, resolve arbitrary single blockers, or establish priority in the literature.
