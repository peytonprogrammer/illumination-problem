# Reduce the full corridor objective to commensurable vertical dimensions

Codex01a18403, 6 November 2026. Parent hand milestone.
DEPENDENCY: phase-lines.md must be independently accepted; currently pending.
The actual cap-sheet sufficiency lemma is independently audited by the peer.

## Statement

The full arbitrary outer-pair illumination statement holds whenever at least
one of a/g,b/g,h_-/g,h_+/g is irrational. Equivalently, the only remaining
vertical-parameter class is the one in which all four dimensions are rational
multiples of g. Horizontal endpoints s,t remain arbitrary real interior marks.
There is no uniform reflection bound and no finite rational-denominator cap.

Normalize d=g=1 and use the accepted actual-mirror L reduction if either
horizontal coordinate exceeds1. Thus assume0<s,t<=1. If a or b is irrational,
phase-lines.md applies immediately. It remains to consider rational a,b and
at least one irrational exterior height. Choose a positive integer q so that
a=p/q,b=r/q for positive integers p,r. Write H0=a+1+b>0.

## 1. Irrational upper height

Let h=h_+>b be irrational and B=2h-b. Unfold the single top-wall reflection,
regarding the developed target as(t,1+B), with lower depth a unchanged.
The developed height is H=a+1+B=2h+a+1-b, which is irrational. Effective
B is irrational, so the phase-lines theorem supplies a vertical-only chart
for these effective depths and actual horizontal positions s,t.

More precisely, that proof supplies some fixed u in{0,2}, epsilon in{+1,-1}
and a nonempty open set of slope parameters

    z_M=(u+epsilon*t-s+4M)/H,

for which the strict portal boxes hold. This is an OPEN set in the orbit
closure, rather than just a single isolated successful M. Here the portal
coordinates as functions of a free real z are

    E1(z)=s+a z, E2(z)=s+(a+1)z,

both periodic modulo4 when z is increased by4q. The sequence z_M modulo4q
is dense, since its step4/H divided by4q is irrational. Thus the box
preimage is a nonempty open subset of the z-circle. This also follows
directly from the circle-closure construction in phase-lines.md; both
effective phases are irrational, so its two centered point exceptions do
not apply. The relation for these phases has primitive normal proportional
to(a+1,-a), hence connected kernel; the z-circle parametrizes its full closure.

We must exclude a simultaneous top/side-wall corner. The virtual cap is at
y=1+h, and its developed x coordinate is

    Xcap=s+(a+1+h)z_M.

Since a+1+h=(H+H0)/2 and H z_M=u+epsilon*t-s+4M,

    Xcap = (s+u+epsilon*t)/2 + 2M + (H0/2)z_M.           (1)

A cap corner occurs exactly when Xcap is an even integer. In(1) the term2M
vanishes modulo2, and the remaining affine function of z has nonzero slope
H0/2. Increasing z by4q changes it by2(p+q+r), an even integer. Therefore
its zero set modulo2 is FINITE on the z-circle. Removing finitely many
points from a nonempty open set leaves a nonempty open subset. Density
selects a finite M meeting the portal boxes and avoiding every cap corner.

Fold the virtual upper segment above y=1+h down by reflection in the cap.
It starts at actual S, crosses both portals legally and ends at actual T.
For1<=y<=1+B the folded physical height lies in[1+b,1+h] after the cap,
and the upper band's x coordinate is its prescribed F2(X-u). The strict
cap-corner exclusion makes the cap bounce smooth. All vertical contacts
inside a band are actual smooth walls. If actual T is met on an earlier
outgoing upper segment, truncate at that first encounter; this is already
a legal finite connection. No assumption of first arrival at the developed
image is needed. This is the independently audited cap-sheet sufficiency
argument, now with a proved way to avoid its corner obstruction.

## 2. Irrational lower height

Let h=h_->a be irrational, A=2h-a, B=b and H=A+1+b.
The effective lower depth A is irrational, so phase-lines.md again supplies
a strict vertical chart in the effective room. Put

    z_M=(u+epsilon*t-s+4M)/H.

The portal coordinates, modulo4, may be written without irrational
coefficients multiplying the free variable z:

    E1 ≡ u+epsilon*t-(1+b)z,
    E2 ≡ u+epsilon*t-b z,

because A=H-(1+b) and H z_M=u+epsilon*t-s+4M.
These have period4q in z. The z_M sequence is dense modulo4q. The primitive
phase relation has normal proportional to(-b,1+b), with constant1; after
clearing and reducing rational denominators its normal coordinates are
coprime. The z-circle therefore parametrizes the entire connected closure,
and strict successful portal boxes yield a nonempty open z set as before.

The virtual lower cap is at y=-h, a vertical distance A-h=h-a from the
virtual source. Since h-a=(H-H0)/2, its developed coordinate is

    Xcap = (s+u+epsilon*t)/2 + 2M - (H0/2)z_M.           (2)

Its even-integer set is again finite on the z-circle, with nonzero slope
and the same period. Choose M in the successful open set away from this
finite set. Fold the segment below-h by y->-2h-y. Its initial physical
point is S, because the virtual source is at-(2h-a); it travels down to
the smooth lower cap, then up to the original portal. It cannot escape
through y=0 before that crossing. All other mirrors and target handling
are as in the audited cap-sheet lemma. Thus it gives an actual connection.

If both exterior heights are irrational, choose either construction; no
simultaneous choice or extra rational independence is required.

## Remaining objective

Subject to independent acceptance of phase-lines.md and this reduction,
ONLY a,b,h_-,h_+ rational in units of g remain, with arbitrary real s,t.
This is an unbounded commensurable class, not a finite list of rooms or
bounded grid census. The centered subcase is already independently accepted.
The four-cap-sheet covering conjecture remains unproved and is not assumed
here. The native goal must remain incomplete until the rational class and
all independent review obligations close, or an actual dark counterexample
is rigorously proved and independently validated.
