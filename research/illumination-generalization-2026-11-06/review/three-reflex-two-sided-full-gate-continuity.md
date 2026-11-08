# FG01: all four final-bottom gates still have a finite continuous-selection horizon

Status: new HAND result offered for independent review, conditional on the frozen BD01/BT01-BT02 complete final-bottom description. This sharpens MS01 from the two safe preturn gates to ALL FOUR literal corner-free final-bottom branches. It is a countercontrol to a continuity premise, not source-to-target existence or darkness.

## Quantified claim

Use integral ordered spiral dimensions and actual integer/native T=(t,v) with l<t<w and 0<v<c. Set W=w-l, y=t-l, L_min=W-y=w-t>0, G=h-c, epsilon in (0,1/(2H)). A legal final downward right-cap state that reaches T before another cap return has negative/downward velocity by NG01 and x_h in (w+G*epsilon,w+(G+2c)*epsilon).

Let I be ANY interval in z=1/epsilon>2H. Suppose x_h(1/z) continuously selects one such state for every z in I. Then for ANY z1<z2 in I,

    (w-t)*(z2-z1) < 2c.

Consequently the diameter of I is at most 2c/(w-t). In particular no continuous selector exists on the whole half-line z>2H, or equivalently on every sufficiently small positive epsilon. The diameter bound is NONSTRICT for an open interval; only the inequality between two included parameter points is strict. No direction, metric, return count or reflection cutoff is imposed.

## Proof using all target images and both arrival signs

For kappa=-1 (before slow left turn) or +1 (after slow left turn), sigma=-1 or +1 (target vertical arrival), the frozen complete relation gives

    d = epsilon*(2cm+c+sigma*v) - (W+kappa*y),
    0<d<2c*epsilon,
    x_h=w+d+G*epsilon.

The unique m for each branch is retained without bounding it. Postturn branches also retain the literal true-corner guard from BD; removing those illegal branches can only restrict selections, so no sufficiency assertion is needed for the monotonicity proof.

Define the normalized gate coordinate

    q(z)=z*(x_h(1/z)-w)-G.

A continuous physical selector produces a continuous q with 0<q<2c. Every allowed branch is one of the lines

    q_(m,kappa,sigma)(z)=2cm+c+sigma*v-(W+kappa*y)*z.

Their slopes are -(W-y) or -(W+y), both at most -L_min<0. On every compact z interval only finitely many lines can meet 0<q<2c: the displayed equality bounds m there. Duplicate lines, if any, may be identified. The finite set of pairwise intersections partitions that compact interval into finitely many pieces. On each open piece a continuous selector must stay on a single line, since distinct lines do not meet there. Thus for any included z1<z2, summing the affine increments over this finite partition yields

    q(z2)-q(z1) <= -L_min*(z2-z1).

But q(z1),q(z2) in (0,2c) imply q(z2)-q(z1)>-2c. Combining gives L_min*(z2-z1)<2c. Taking supremal distances gives the stated diameter bound. The argument includes every m and every legal switch; it does not assume a fixed branch index or a finite global number of branches.

## Actual junction and corner check

A junction between a preturn branch (m_-,sigma_-) and a postturn branch (m_+,sigma_+) obeys

    2y*z=2c*(m_+-m_-)+(sigma_+-sigma_-)*v.

At their common incoming state, with r=x_e-l=W+q/z,

    r*z/c = m_++m_-+1+(sigma_++sigma_-)*v/(2c).

If the arrival signs are opposite, the right side is an integer. The postturn continuation therefore meets a genuine l-floor or l-underside corner BEFORE its postturn target, so it is excluded by the literal BD guard. This is not a legal splice through a corner. If the signs agree, the fractional term is sigma*v/c, which is nonintegral; subject to strict entry and the other stated guards this is a permissible shared state, representing target visits on one actual trajectory. FG01 already allows these junctions, so legal postturn switching cannot evade its bound.

The check does NOT authorize continuation through any corner, count developed images as physical corners, or replace a chosen target lift. Every state here is on the actual h section, transported from the actual c gate with its negative/downward germ and the SAME epsilon.

## Optical meaning and exact limits

GT01 supplies at least one literal target-bound state at every small epsilon. FG01 shows that even its COMPLETE four-branch last-bottom extension does not thereby supply a globally continuous target curve. On every long enough reciprocal-parameter interval a selection must jump, cease to exist as a continuous selection, or leave this final-cap class. Such a jump is not a legal fixed-parameter ray.

This does not refute existence at an isolated rational epsilon, the full source-return/target relation, or a cycle construction proved on a different legitimate space. Every successful full trajectory to t<w has a final cap state in this class, but the source may select disconnected branches as epsilon varies; illumination needs only ONE exact match. No positive degree, essential curve, all-slope obstruction, nine-corner charge or full theorem follows.

The argument uses strict t<w. At t=w, L_min=0 and this proof gives no finite horizon; GT01 treats that actual interior equality separately. Targets t>w likewise remain outside FG01. General equality seams and other r3 shapes are not covered by this continuity claim.

The next positive obligation remains an actual same-parameter source match inside a common regular branch domain. FG01 prevents substituting pointwise target access plus assumed global continuity for that obligation. Independent BD/GT/FG review remains pending. No new search, numerical case, engine, worker, clock renewal, frozen edit or git change.
