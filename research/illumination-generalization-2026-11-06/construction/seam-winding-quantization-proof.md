# A59: actual seam darkness quantizes independent selected widths

Author theorem pending independent review. Original conservative effort07:47Z--08:01Z includes preliminary phase reasoning. Universal canonical45 W21 remains OPEN.

## 1. Exact quantified result

Use ANY literal A0/A1 room from A58 with integer h>=3 (and integerd>=1 forA1), real positive core widthc, independent selected widths w_s,w_t, and independent positive REAL opposite widths. Marks here are ACTUAL SEAMS ONLY: S=(c,2), T=(c,2h+2). Core height is the actual integer G=2h+4 forA0 and G=2h+d+4 forA1.

If this actual pair is dark, then

0<w_s/c<=1, 0<w_t/c<=1,
2G*w_s/c and 2G*w_t/c are INTEGERS.               (1)

In the six unresolved A58 vertical patterns, the independent selected ratios must moreover lie in the following Cartesian products:

|kind,h,d|possible w_s/c|possible w_t/c|pair count|
|--|--|--|--|
|A0,3|1/4,1|1|2|
|A0,5|5/28,1|1/4,1|4|
|A1,3,2|1/4,1|1/3,1|4|
|A1,3,6|1/4,5/8,1|1/8,3/8,1|9|
|A1,3,7|4/17,1|2/17,6/17,1|6|
|A1,3,10|1/5,1/4,3/5,1|7/20,2/5,1|12|

These are only37 possible selected-ratio pairs, each with opposite widths STILL arbitrary positive reals. They are necessary cells, NOT dark examples and NOT a completed illumination theorem. The independent-depth results of A58 cover other vertical families, but do not convert this SEAM theorem into an all-depth theorem for the six remaining patterns.

## 2. Actual far-only paths and first stationary phase

For q=w/c>0 and integer H>=2, accepted R50 gives

n(q,H)=floor(q*(H-1/2)+1/2),
m(q,H)=(qH-n(q,H))/(1+q), |m|<1/2,
tau=(H+n(q,H))/(c+w).

Its source-far COMPLETE path starts at the actual lower seam, makes a true selected far-wall excursion, exits at a strict portal, reflects on the opposite side at the nominal midpoint PLUSm, and ends at the actual upper seam (normal arm empty). Its target-far COMPLETE path instead turns at nominal midpoint MINUSm and returns to the actual upper seam through its true far-wall excursion. Each uses its OWN consistent tau. They are never concatenated with each other's slopes.

Whenever m!=0, w*tau=n+m is nonintegral, so the far collision is not a corner; |m|<1/2 gives strict portals. All open core segments have0<x<c. This is the full accepted R50 actual-endpoint construction; the first-index formula is used below because it is defined for all real q,H and has strict phases.

More generally ANY integer n>=0 with

qH-(1+q)/2 < n < qH+(1+q)/2                       (2)

gives the same actual far-only construction, with tau=(H+n)/(c+w) and m=(qH-n)/(1+q). Inequalities(2) are exactly |m|<1/2. Every nonzero such m has the same true far-corner exclusion. No convergence to that n is needed: it is an explicit matched finite path. This stronger set of allowed stationary indices is used ONLY for the final finite sign table.

## 3. Two infinite families of actual winding charts

Write s=2,t=2h+2,mu=h+2. Global vertical folding is the actual F_G with period2G, reflecting at ACTUAL floor and roof. All selected copied bands are reflected copies of the original teeth; strict portals avoid every end line. All open core end crossings have0<x<c and are ordinary smooth physical reflections. The actual target is retained by folding the entire completed trajectory. These are the accepted A38/R50 end guards, applied to arbitrary finite winding.

For the SOURCE width, use target center image t+4jG for each integerj>=0. Ordered source/target centers remain s and that image, with half separation H=h+2jG and mean mu+2jG. The fold derivative at this mean is+1. Its physical nominal opposite point is mu=h+2, the UPPER endpoint of the FIRST left mouth. The interval(mu,mu+1) is smooth: A1's next mouth begins atmu+d>=mu+1, A0's atmu+2. Hence if m(q_s,H)>0, the source-far actual path turns in the protected smooth interval and illuminates. Consequently actual darkness forces

m(q_s,h+2jG)<=0 for EVERY integer j>=0.            (3)

For the TARGET width, use the reflected copy of T at center -t-4jG, ordered BELOW the actual S center s. This time the half separation is H=mu+2jG and the mean is -h-2jG. Its fold derivative is-1 and physical nominal mean is h, the LOWER endpoint of the first left mouth. The copied LOWER source-far excursion uses the original TARGET width w_t; its turn shift+m folds to physical shift-m. Thus a positive m puts it in(h-1,h), a smooth actual left wall, and yields a complete actual T-to-S connection. Reverse that ordinary trajectory to obtain an S-to-T connection. Therefore darkness also forces

m(q_t,mu+2jG)<=0 for EVERY integer j>=0.           (4)

All nominal levels are strictly away from global ends; shifts have magnitude<1/2. Other teeth cannot interfere with the open core legs. Every j supplies a finite actual path if its sign succeeds. There is no uniform reflection-count or winding cap, and no formal image-target substitution. A prior actual endpoint encounter can be truncated.

## 4. A short-arc orbit cannot hide a nonzero rotation

If q>1, n(q,H)<=qH-(q-1)/2<qH, so m(q,H)>0 for EVERY H. Thus (3)/(4) exclude either selected q>1. If q=1 and H is integral, n=H,m=0; equation(1) already holds.

Suppose0<q<1. Put x_H=q*(H-1/2)+1/2. Then

m(q,H)=({x_H}-(1-q)/2)/(1+q).

Accordingly m<=0 iff the fractional part {x_H} belongs to the CLOSED arc[0,(1-q)/2], of length strictly less than1/2. Applying(3) or(4) gives the circle orbit

{x_0+2Gq*j}, j>=0,

entirely in this short arc. This forces2Gq to be an integer. Here is an elementary proof covering rational and irrational q alike. If theta=2Gq is NOT integral, the Cesaro average of exp(2pi*i*(x_0+j*theta)) tends to zero by the finite geometric-series formula. But rotating this arc to be centered at angle zero makes every term's real part at least cos(pi*(1-q)/2)>0. Their average therefore cannot tend to zero, a contradiction. No density, ergodic, arithmetic-lattice or genericity theorem is imported.

This proves(1) for both independent selected widths, without assuming their equality or rationality beforehand. If the rotation is nonzero, the contradiction guarantees some FINITE j with an actual legal illuminating path; an effective uniform j bound is unnecessary for this existence implication.

## 5. Finite strict-phase sign table after quantization

Set q=n/(2G),1<=n<=2G. Use the following four ACTUAL ordered end charts; this finite subset suffices for the table:

A0 source darkness requires
m(q,h)<=0, m(q,h+G)>=0, m(q,mu)>=0, m(q,mu+G)<=0;
A1 source darkness requires
m(q,h)<=0, m(q,h+G)<=0, m(q,mu)>=0, m(q,mu+G)>=0.

For the target width reverse ALL four inequalities. Here each inequality is required for EVERY strict index satisfying(2), because ANY nonzero phase pointing onto its protected actual wall gives a complete legal connection. Zero phases neither prove illumination nor darkness.

These signs follow directly from physical folds. For target image t+2kG,k0/1, ordered S is the lower endpoint, the mean is mu+kG and fold derivative is(-1)^k. The protected physical level is mu for evenk; for oddk it is G-mu, an opening END inA0 but an opening START inA1. Source-far has shift+m, target-far-m. For target image -t-2kG,k0/1, ordered Tcopy is lower and S is upper; mean -h-kG has derivative-(-1)^k. Its physical level is h for evenk, an opening START, and G-h for oddk, an opening START inA0 but an opening END inA1. Reversing which physical endpoint supplies the source/target far arm gives exactly the signs displayed above.

The prescribed exact rational checker evaluates these finite inequalities on ALL integers n1..2G for each of the six literal vertical rows, retaining EVERY index in the strict open interval(2). Its output is the explicit table in Section1:2+4+4+9+6+12=37 Cartesian ratio cells. No floating equality decision or sampled-width interpolation is used. An additional audit of both image orientations and winding representatives -3..3 returns the same table; this extra check is not needed as an arbitrary-word completeness claim.

## 6. Limits and next obligation

This derives a positive necessary geometric constraint FROM ACTUAL darkness. It does not infer darkness from a failed construction. Neither opposite tooth width has been discretized; no finite room census has been established. Arbitrary independent positive endpoint depths in these six patterns remain open, as do other comb forms, taller general teeth, diagonal geometries and universal W21. Rescaling an axial optical example does not justify importing an integer-core theorem when the opposite normalized widths become nonintegral. Independent peer acceptance of the full winding/actual-endpoint argument and finite table is required.
