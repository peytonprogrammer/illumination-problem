Advances: T10, pyramid — simultaneous choice of three winding counts gives a sufficient gcd inequality with both aperture widths free. The full word remains open.

**Named tests.** I predicted a vertical miss and a horizontal hit for mask 761 with tier widths (200,V,400,200), levels (0,1,65,67,69), S=(1,68), T=(19200,33), at V=38400 and 57600. Both predictions held. Horizontal scaling by 100 maps the earlier rational obstruction to these integral rooms and preserves axial reflection. In the original units the vertical exclusion uses a=1 or 3 and b=32 or 96. For each sign the only candidate representative E after orienting the second crossing satisfies E=(2−4a/L±1/100)/(1+a/L)>8/b, L=b+2. The preceding representative is below −2; the second gate requires E≤8/b. These comparisons hold in exact rational arithmetic. The old congruence applies since V/100 is a multiple of 192. This excludes even the two specified end-cap options. In the perpendicular sweep the exact d172 wall tracer from T with displacement (−19199,3235) ends at S after 50 horizontal reflections in each room. A preliminary replay mistakenly used 100 times the vertical displacement and missed; the displayed displacement uses the original flight time.

My third prediction was a vertical hit at widths (2,385,4,2), the same levels, S=(1,68), T=(192,33). Both axes hit. From S the displacement (27159,−35) gives 840 vertical reflections; from T, (−191,4259) gives 66 horizontal reflections. The tracer returned the specified mark in each case. Here wb=64>8=ud. Thus the lattice restriction permits arithmetic constructions but cannot discard rational obstructions: horizontal and vertical dilations can clear denominators separately.

**Later-image lemma.** Use the d172 nested three-run sweep, in the residual orientation with shared left side, with integral widths w,u,V and positive integral longitudinal travels a,d,b. Let L=d+b, D=a+L, g=gcd(dV,ub), and η=gcd(wg,auV)/g. For all transverse placements a sufficient condition is

    g/L + bη/D < u.

This controls an unbounded region outside wb≤ud. For example, in the third test allow any odd V>192 with the same endpoint coordinates. Then g=2 and η≤2, so the displayed bound is <4 for all such V.

Proof. For terminal image Z=z+2Vj put M=(Z+2ui)/L and R=dM−2ui. The values of LR form the progression dz+2gℤ. Choose i,j by Bézout to put R within g/L of zero. Holding R fixed, change (j,i) by any multiple of (ub/g,dV/g). This changes M by a multiple of 2uV/g. With the independent source winding k, X=x+aM+2wk can therefore be chosen within η of zero. The slope is M−X/D. The first gate coordinate XL/D has magnitude <w since η≤w. The signed second crossing R+bX/D lies strictly in (−u,u); shared-side folds agree there. The endpoint folds from Z to z. At a shared smooth side a zero crossing is legal. This is the d172 construction with the full integer kernel retained at the first gate.

**Perpendicular variant.** Suppose the chosen transposed chain has its first two intervals [0,w′] and [0,u′], while the third contains [0,u′] and need not share a side. Use the primed travels and widths, with z′ measured from that same origin. Aim R′ at u′/2. The same two progressions work, using the translational target images z′+2V′j. A sufficient condition is

    g′/L′ + b′η′/D′ < u′/2.

The physical second crossing then lies in (0,u′), so the two folds agree without sharing an endpoint. This variant requires an actual three-column passage with uninterrupted side walls.

**Where selection stops.** For mask 761, write the bottom tooth height q, broad row height h and top height f. Write S=(x,h+d+a), T=(z,h−b) relative to the floor of the broad row, with 0<x<w<u<z<V, 0<a<f, 0<b<h. The perpendicular parameters are (w′,u′,V′)=(h,h+d,q+h+d+f) and (a′,d′,b′)=(z−u,u−w,w−x). The explicit unresolved region of the uniform estimates satisfies all three inequalities

    min(ub,dV)+wb > u(d+b),
    g/L+bη/D ≥ u,
    g′/L′+b′η′/D′ ≥ u′/2.

An example is w=4,u=5,V=60, (q,h,d,f)=(8,4,1,2), (x,z,a,b)=(1,15,1,3), area 285. The two bounds evaluate to 15/4+12/5 and 15/4+6/14 respectively, above 5 and 5/2. Multiplying V by any positive integer preserves these failures. This example locates a gap in the uniform inequalities only. Particular offsets can pass. Area 285 is the smallest named example here outside both bounds; I have not established the minimum over pyramid rooms. The census already covers area ≤21.

At this point the choice of terminal image and winding must control the signed first-gate correction as well as its size. The perpendicular estimate can fail on the same parameters. I have no implication that either exact list hits throughout this region, and no simultaneous-miss family. This triggers the method stop, not a counterexample to T10.
