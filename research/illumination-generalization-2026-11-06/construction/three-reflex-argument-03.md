# TR03: all-pair illumination for a quantified tall-spiral class

Candidate hand proof, pending independent review. All notation, parameter orders and the explicit tall-roof condition are those of three-reflex-candidate-03.md. This proves a geometric subclass of genuine r3 rooms; it does not claim all r3 rooms or the full native objective.

## 1. Reduce only by the accepted original-wall coverage

Use the independently accepted TR01 partial optical theorem. Its proof and five-claim independent review have been read in full. It leaves exactly, after exchanging the actual endpoint labels, a target T=(t,v) with l<t<A,0<v<c, and a source S=(s,u) in either of these classes:

* left lower column: 0<s<a and b<u<h;
* upper cap or its interior arm seam: h<=u<H and 0<s<=w, with S strictly interior to P. At u=h this requires s<a; points on the notch wall are not marks.

We construct an actual optical path for both classes. Reflecting a developed endpoint or using a different original mark is not part of the reduction.

## 2. A uniformly long bottom-portal slope interval

Write z=A-t, d=c-v and e=h-v. Then 0<z<B=A-l, 0<d<c and 0<e<h. A reverse description of the target's bottom segment uses the phase

    z2(tau)=z-tau*d.

Its crossing of y=c is strictly within the actual right-hand portal precisely when |z2(tau)|<R, where R=A-w. The positive slopes satisfying this condition form

    W=(max(0,(z-R)/d), (z+R)/d).

This interval has length strictly greater than R/c=2L. Indeed, if z>=R its length is 2R/d>2R/c; if z<R its length is (z+R)/d>R/c. Put q=max(0,(z-R)/d) and choose

    J=(q+L/2, q+3L/2).

Then J has length L, is strictly positive, and its closure is inside W. Every slope in J already satisfies the target-bottom portal guard. This interval exists for every target, including arbitrarily shallow v or arbitrarily small distances to either bottom side wall.

## 3. Remove only finitely many phase boundaries

In the left-lower case put d0=h-u, so 0<d0<h. Remove the source phase-boundary points

    s+tau*d0=(2n+1)a, n in Z.

They are spaced by 2a/d0>2a/h. Any interval of length L contains at most ceil(L*h/(2a))+1=Ns of them. On each remaining open component the same nearest even period 2na gives

    z0(tau)=s+tau*d0-2na in (-a,a).

Remove also the right-arm phase-boundary points

    z-tau*e=(2j+1)R, j in Z.

They are spaced by 2R/e>2R/h, so at most Nr=ceil(L*h/(2R))+1 lie in J. On each remaining component one integer k is fixed and satisfies

    z1(tau)=z-tau*e+2kR in (-R,R).

The sign convention is intentional: the nearest even multiple to z-tau*e is -2kR. For an upper-cap source only the right-arm boundaries need be removed; we retain the same larger bound Ns+Nr.

Removing at most Ns+Nr distinct points from the interval J leaves at most Ns+Nr+1 open components of total length L. At least one component I=(alpha,beta) therefore has length at least

    delta=L/(Ns+Nr+1)>0.

All applicable indices n,k are fixed on I. No density assertion or endpoint-phase limit is used. The component can be selected by listing the finitely many explicitly prescribed arithmetic boundary points in J and taking a longest gap. The bounds do not involve H, the marks or any denominator.

## 4. Exact actual-target roots must enter that component

Put D=2H-u-v. Since u<H and v<c,

    D>H-c>=2A/delta.

Thus 2A/D<delta. In the left-lower case set

    C=2na+A+2kR+z-s;

in the upper-cap case set

    C=A+2kR+z-s.

The arithmetic progression

    tau_m=(C+2mA)/D, m in Z,

has spacing 2A/D strictly less than the length of I. Therefore a root tau=tau_m lies strictly in I. For an explicit choice take

    m=floor((D*alpha-C)/(2A))+1.

Then alpha<tau<=alpha+2A/D<beta. All parameters and indices are finite, and tau>0 because I is positive. This is the simultaneous selection step: n,k have already been fixed on I, and the chosen m changes only the roof-strip period. The target equation is then exact, not an approximation or a separate ray matching.

## 5. Left-lower source: construct one matched four-band curve

Use increasing developed height eta from u to 2H-v, folding physical height only at H. Put

    eta1=2H-h, eta2=2H-c,
    g0=2(H-h), g1=h-c, d2=c-v.

In the first band, u<=eta<=h, use

    x(eta)=F_a(s+tau*(eta-u)).

At eta=h, its local phase is z0=s+tau*(h-u)-2na in (-a,a). In the unfolded cap h<=eta<=eta1 use

    x(eta)=F_A(z0+tau*(eta-h)).

The exact root equation gives

    z0+tau*g0-(2m+1)A
      =z-tau*(h-v)+2kR=z1 in (-R,R).

Thus in the right arm eta1<=eta<=eta2 use

    x(eta)=A-F_R(z1+tau*(eta-eta1)).

At eta2 its phase after subtraction of 2kR is

    z1+tau*(h-c)-2kR=z-tau*(c-v)=z2 in (-R,R).

Finally, in the bottom chamber eta2<=eta<=2H-v use

    x(eta)=A-F_B(z2+tau*(eta-eta2)).

Its final argument is EXACTLY z=A-t, strictly between 0 and B, so the final coordinate is the specified actual t. Folding height about H gives actual target height v.

Here F_q(r)=distance(r,2qZ). At the first portal both neighboring folds reduce locally to the same absolute value because |z0|<a<A. At the second they reduce to A minus the same absolute value, since the cap argument differs from z1 by the ODD multiple (2m+1)A and |z1|<R<A. At the third the even period 2kR and |z2|<R<B give the same identity. Positions and SIGNED velocities therefore match at every portal. A zero phase is one smooth outer-wall reflection, not an artificial turn.

Every open-band mirror is a genuine original wall: x=0,a below h on the source arm; x=0,A above h in the cap; x=w,A between c and h on the right arm; x=l,A below c in the bottom chamber. Positive widths and finite phases give finitely many reflections. Height is strictly increasing before H and strictly decreasing afterwards.

The strict portal inequalities exclude (a,h), (w,h), (w,c) and the corresponding ledge endpoints. They also exclude an illegal crossing of a horizontal ledge. The source and target are original interior points, so no endpoint is a true corner.

## 6. Exclude a convex roof corner for the left-lower source

At eta=H the cap argument is z0+tau*(H-h). If it were an integer multiple of A, even triangular-wave symmetry about that point would make the two cap portal x coordinates at eta=h and eta=2H-h identical. But the first lies in [0,a), while the second lies in (w,A], and a<w. This is impossible.

Hence the one top reflection is strictly inside the genuine y=H wall. Every other contact has already been checked on a smooth genuine vertical wall. The constructed curve is therefore a finite ordinary actual S-to-T specular trajectory, with no corner continuation or full-fiber substitution.

## 7. Upper-cap source, including the artificial cut x=w

Now h<=u<H and 0<s<=w, with S actual interior. Start in the cap and define, for u<=eta<=eta1,

    x(eta)=F_A(s+tau*(eta-u)).

The root equation in this case implies

    s+tau*(2H-h-u)-(2m+1)A
      =z-tau*(h-v)+2kR=z1 in (-R,R).

The right-arm and bottom formulas from section 5 apply unchanged. They attain the SAME actual target and satisfy both strict portal guards. These formulas never use a fictitious wall at x=w above h: before eta1 the full cap has width A, and at eta1 the matching is transparent. Thus a source on that artificial cut is an actual interior starting point of this construction.

If the top contact is smooth, all contacts are legal and this is the required path. The only remaining issue is a possible convex roof corner, treated explicitly next.

## 8. At a singular roof, retain only the legal suffix AFTER actual source return

Suppose q=s+tau*(H-u) is an integer multiple of A. The formal folded curve then passes through one convex roof corner. Do NOT use that full curve as an optical witness. At

    eta_return=2H-u,

its cap argument equals s+2tau*(H-u)=2q-s, so F_A(2q-s)=s. Its physical height is u. It therefore returns to the SAME ACTUAL original S after the singular event.

If u>h, eta_return<eta1; and because u>v, eta_return<2H-v. Take only the suffix starting at this interior occurrence of S. Its physical height now decreases strictly from u to v. It never visits the roof again. Every later contact lies in the genuine cap/right/bottom walls already guarded above; the sole bad roof contact lies strictly BEFORE this new launch. At the new start the phase is congruent to -s modulo 2A, with 0<s<A, so the source is not itself a fold cusp. The suffix has nonzero velocity and ends at actual T. This is an explicit original-room legal ray, not permission to reflect at a corner.

If u=h, the same return would occur at eta1 with x=s<=w, contradicting the strict second-portal position x>w. Thus the bad roof case cannot arise there.

The earlier portion of the formal curve is discarded entirely; no legal path is asserted to traverse its corner. No limits, arbitrary-lift replacement or shadowed target are used.

## 9. Every actual endpoint placement in the stated tall class is covered

TR01 covers all pairs except exactly a lowest-chamber mark paired with a left-column or upper-cap mark. Sections 2--6 cover the uncovered left-column sources with u<h. Sections 2--4 and 7--8 cover every remaining upper-cap source, including u=h and x=w above h. Reversing the resulting legal trajectory covers the opposite original label order. Endpoints on y=c on the right were already covered by TR01; y=c on the bottom ledge is actual boundary and never an interior mark.

Consequently every pair in this entire ordered spiral metric class illuminates under H>=c+2A/delta. This is an arbitrary-real theorem if the proof is accepted; there is no rationality requirement or hidden metric/reflection cutoff. The height threshold is deliberately conservative and is SUFFICIENT only. Failure of that inequality is not evidence of darkness.

## 10. Frontier and method boundary

Still open: short-roof metrics in this ordered spiral class; other possible metric orders of (1,1,8); the other seven r3 types; r4..8. No conclusion for mixed-direction rooms or universal wall minimality is made. The full native goal is incomplete.

All construction steps are finite per input: one bounded interval, finite phase-boundary lists, integer rounding and a finite folded curve. No new optical search engine, room census, reflection cutoff or worker is used. The mathematical existence proof is sections 2--4 and is not a claim inferred from later prescribed checks.
