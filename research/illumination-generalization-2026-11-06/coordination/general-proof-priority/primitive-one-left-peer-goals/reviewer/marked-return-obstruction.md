# Marked-flow obstruction to every axis or diagonal realization

HAND theorem for EVERY assigned d>=3,d=3 modulo4. It strengthens exclusion of one selected Bezout matrix to exclusion of ALL genuine affine maps carrying the prescribed one-left direction to ANY coordinate or diagonal direction. No direction survey, numerical orbit, new ray discovery or checker is used.

Let A=2d+1, P=[0,A]x[0,d] union [0,d]x[d,A], M its actual four-copy unfolding, c the sole cone, and v=(-d,d-1). Gamma is the fixed p->ORIGINAL Rxq segment of holonomy2v. This theorem concerns genuine full-group direction realization; it does not refute compression into other image directions.

## 1. A regular marked point that every candidate must track

The exact period lattice is2Z². With cone torus image (d,d) as origin, the five regular physical corner marks have classes modulo2:

O=(0,0): (1,1),
X=(A,0): (0,1),
Y=(0,A): (1,0),
E=(A,d): (0,0),
K=(d,A): (0,0).

There is exactly ONE regular marked point over each nonzero class. A genuine Sigma-preserving affine F fixes the unique cone and induces its integral unimodular derivative L on this intrinsic torus. Since v=(1,0) modulo2, the relative torus class of F(Y) is L v modulo2.

If L sends the PROJECTIVE direction of v to an axis, primitivity forces Lv to be a signed unit axis vector. If it sends it to a diagonal/antidiagonal, primitivity forces Lv=(+/-1,+/-1). Consequently:

- Lv=(+/-1,0) forces the exact actual corner F(Y)=Y.
- Lv=(0,+/-1) forces F(Y)=X.
- Lv=(+/-1,+/-1) forces F(Y)=O.

This identifies actual marked points, not arbitrary points in their torus fibers: uniqueness among regular Sigma is essential. No independent sheet or translation adjustment remains available.

## 2. Exact initial v-flow from Y

We use the UNDERLYING translation flow, not an optical ray through physical corners. Regular convex corner marks are ordinary flat points and may be traversed when comparing an affine map's flow conjugacy. A true cone is never continued through. Starting at the regular corner Y is legitimate for this invariant, not an illumination witness.

In the signed cross, the initial upward motion from (0,A) is represented immediately after the roof seam as (0,-A). At time1 it reaches (-d,-d-2), strictly inside the lower-arm left wall, and translates to (d,-d-2). No cone has occurred. Until the first outer-x wrap its x coordinate is therefore

x(t)=2d-dt after time1.

At time2 the representative is (0,-3); at time3 it is (-d,d-4), on an internal arm entry with -d<d-4<d. The nominal outer-x contact time is

t0=4+1/d,

when x=-A.

For d=3 the left-arm top contact would occur at time5>t0=13/3. The actual first outer-x contact is consequently

(-A,5/3),

strictly inside that outer wall. No earlier cone occurs along these legs; the lower and central entries and the outer wall contact all have strict noncorner coordinates.

For d>=7 the left-arm TOP wall occurs first at

t1=(3d+1)/(d-1)=3+4/(d-1),
x(t1)=-d-4d/(d-1).

Here 3<t1<4<t0 and -A<x(t1)<-d. It is a strictly smooth horizontal-arm wall, so y translates from d to -d while x is unchanged. At t0 the next outer-x contact is

(-A,-4-1/d),

with -d<-4-1/d<d. Between t1 and t0 the point remains strictly in the left horizontal arm; no cone or other vertical-wall jump intervenes. Earlier lower-arm and central crossings are internal or strictly smooth as already listed.

Thus for EVERY assigned d, the forward flow from Y is defined without a true cone through t0 and makes at least ONE actual outer-x wrap by t0. Also t0<2d; for d>=7, t0<d. The d=3 computation will not require t0<d.

## 3. Horizontal crossing counts give a marked-flow gap

Along any continuation before a true cone, x velocity is constantly -d. Every x-boundary jump is positive and has length2d (inner arm side) or2A (outer arm side). Let Ni(t),No(t) be their nonnegative integer counts. Regular convex corner simultaneities do not invalidate this formula: the two relevant translations commute, and the x jump is still one of the same positive lengths. A true-cone continuation is not used.

Starting at x=0,

x(t)=-dt+2d Ni(t)+2A No(t).

After t0, No(t)>=1.

If this trajectory first reaches the true cone at time tau, then tau is an integer: its developed displacement is tau v, all seam translations and the starting/ending corner coordinates are integral, and v is primitive integral. At the cone x=+/-d. The displayed identity modulo d gives

2A No(tau)=0 modulo d.

Because d is odd and gcd(A,d)=1, No(tau) is a multiple of d. There was no cone up through t0, so No(tau)>=1 and hence No(tau)>=d. With Ni>=0 and x<=d, the identity then forces

d tau >=2A d-d,
so tau>=2A-1=4d+1.

In particular the v-flow from Y cannot reach the cone at time d. At d=3 this conclusion also follows directly from the no-cone initial segment through t0>d; the count argument covers every later first cone.

Nor can this flow return to Y at time2d. If a true cone interrupts it, there is no such regular return. Otherwise Y has representative x=0, so at that integer time

d^2=d Ni(2d)+A No(2d).

Modulo d this gives No(2d)=0 modulo d. Nonnegativity gives No(2d)<=d^2/A<d, hence No(2d)=0. But t0<2d already forced No(2d)>=1. Contradiction.

These are statements about this actual marked trajectory, with all returns allowed and no cutoff. They do not infer a billiard path from a singular continuation.

## 4. Exhaustion of axis and diagonal images under the ENTIRE affine group

For Lv=(+/-1,0), section1 forces FY=Y. The horizontal translation flow through Y is a regular closed underlying orbit of period2d, wrapping across the upper-arm side and passing the regular K mark halfway. It never meets the true cone. Affine flow conjugacy would force the actual v-flow from Y to return at time2d, contradicting section3.

For Lv=(0,+/-1), FY=X. The vertical flow through X similarly has period2d in the right-arm cylinder and never meets the true cone. It produces the SAME impossible return of Y under inverse affine transport.

For any of the four signed diagonal unit vectors Lv=(+/-1,+/-1), FY=O. Its flow from O reaches a true cone at time d, along the central-square diagonal, without an earlier true cone. Affine conjugacy fixes the unique cone and would force the v-flow from Y to meet it at exactly time d. Section3 excludes that.

All affine orientation signs and all translation phases are included. Therefore NO genuine global Sigma-preserving affine homeomorphism sends v to any axis, diagonal or antidiagonal projective direction.

## 5. What this excludes, and what it leaves open

In particular EVERY ambient Bezout matrix sending v to an axis is unrealizable, not only the author's chosen B. This conclusion does not enumerate those matrices: it is a full-group marked-flow obstruction independent of their free parameter. It also excludes every realization sending v to a diagonal, not merely the original-direction stabilizer or a controlled-subgroup word.

A hypothetical compressor of the actual gamma must consequently have primitive image vector w outside the axes and both diagonals, as well as satisfying the independently accepted sharp one-copy chord geometry and the exact named endpoint/holonomy equality. No genuine map into the other feasible directions has been constructed or excluded here.

This is NOT a full-group negative for gamma, an existential all-path/all-four-L result, darkness, or broad r<=8 completion. The physical native dilation2 conjugates the maps, paths and time-normalized invariant exactly. No worker, room/ray/direction search, census, engine, frozen edit, git mutation or old effort-clock reset was used.
