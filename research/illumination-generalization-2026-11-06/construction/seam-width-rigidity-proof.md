# A56: darkness forces an exact selected-width ratio, at every core width

Author hand theorem pending independent review. Universal canonical45 W<=21 remains OPEN. Original conservative start07:18/deadline07:32Z includes preliminary arithmetic. No room or ray search establishes this result.

## Statement

Consider any finite strictly simple INTEGER two-sided rectangular-spine comb with core[0,c]x[0,G], integer c>=1, all teeth height2, integer positive tooth widths and vertical band edges, and positive same-side gaps. Opposite-side bands may overlap. Let two selected teeth on the SAME side have EQUAL actual widthw. Their distinct ACTUAL interior seam midpoints have heights0<s<t<G with even t-s (in particular for an actual A pair). Suppose W<=23.

If the ACTUAL selected pair is dark, then necessarily

    w=c, or 2w=c.                                  (1)

There is no bound on c,G, opposite widths, tooth count other than the wall hypothesis, interior A count, diameter or support. This is a necessary condition from darkness, not illumination of the two remaining ratios. It does NOT cover unequal selected widths. In particular it does not establish c/gcd(c,w_s,w_t)<=2 for unequal widths.

## 1. The three physical end charts retain actual endpoints

Reflect the room horizontally if necessary to put the selected teeth on the right. Use the actual source seamS=(c,s) and target images at heights t,-t,2G-t. Their absolute positive half-separations are

    H1=h=(t-s)/2,
    H2=mu=(s+t)/2,
    H3=G-mu.

All are positive integers>=2 because the selected height-two bands have a positive integer gap and even midpoint difference. Folding the three extended-core traces by the ACTUAL floor/roof fold gives physical opposite turn levels mu,h,G-h, respectively. This is exactly the accepted A38 three-chart construction; the lower-target chart is vertically reversed before construction when needed. Original source and target are retained after folding.

By A38, actual darkness requires every integer turn level to be an opposite-mouth ENDPOINT: a smooth mirror or a tooth midpoint already supplies an actual path. Each such endpoint has a protected smooth core-wall interval of length at least1 on one side. Integer band edges and positive same-side gaps ensure this interval; the opposite mouth is on its other side. The turn levels are strictly away from global ends, so the interval does not require an artificial end mirror.

## 2. The equal-width seam response forces divisibility in each chart

Apply the independently accepted A37 D0 seam supplement to each copied pair. Its two selected copied teeth have the SAME actual widthw and height2. Both physical seam marks are interior; in its source-only far chart the initial motion enters its actual selected tooth, while the other arm is empty. The target-only far chart ends at original actualT after its real far reflection. A normal seam is never a mirror.

For the chart half-separationH, the exact first-stationary equations are

    n=floor(w*tau+1/2),
    tau=(H+n)/(w+c),
    m=w*tau-n in(-1/2,1/2).

The two far-only charts provide opposite signed turn displacements. Ifm!=0, select the sign on the protected smooth side of the nominal opposite endpoint. Nonintegral w*tau excludes every actual selected far corner; all other contacts and strict portals have the supplement's guards. After global end folding, open core end crossings are at0<x<c and are ordinary ACTUAL floor/roof reflections. Selected-tooth end contacts stay their original actual mirrors; no extra double reflection or forbidden corner continuation is inserted. Thus m!=0 gives an actual finite S-to-T path in the original room.

Darkness therefore requiresm0 in EACH chart. Then n=w*tau and c*tau=H. Consequently

    c divides w*H1, w*H2, w*H3.                     (2)

This is only necessity. Zero displacement is not accepted as an optical path and may itself be a selected far-corner resonance.

The equal-width hypothesis is essential to this argument: both signed far-only charts use the same w and stationary phase. For unequal selected widths, one cannot substitute the other tooth's far wall or equate its stationary solution. No such inference is made here.

## 3. Wall charge excludes a reduced denominator of three or more

Let r=c/gcd(c,w). The elementary integer equivalence c|wH iff r|H turns (2) into

    r|h, r|mu, r|(G-mu).

Hence r|G and r|s,t because s=mu-h andt=mu+h. In particular r divides all three physical levels h,mu,G-h.

Suppose r>=3. Those three levels are distinct, withh<mu<G-h. Their nonzero separations are multiples ofr and therefore at least3. Each must be an opposite-mouth endpoint by A38. A height-two tooth cannot supply two of these endpoints, since its endpoints differ by2. Thus there are at least THREE distinct opposite teeth.

All three are NONFLUSH: every level is at least3 and at mostG-3, so it is not an endpoint of either possible height-two end-flush band. Both selected teeth are also NONFLUSH: positive s andG-t are multiples ofr and therefore at least3. The exact comb wall charge is W=4+4N_nonflush+2N_flush. These five nonflush teeth alone force W>=24, contradicting W<=23. Additional attachments cannot lower the charge. Therefore

    r<=2.                                          (3)

This is a positive geometric consequence of ACTUAL darkness. It does not use a classification census, a supplied witness, finite diameter or a bound on transparent exceptions.

## 4. Wide selected teeth remove the remaining integer multiples

The independently accepted R44 actual-seam theorem, at D0, already supplies an actual path when one selected widthw exceeds the core widthc. Its proof permits arbitrary real horizontal dimensions and the full height-two comb geometry used here. Hence actual darkness requiresw<=c.

If r1, c dividesw and0<w<=c, so w=c. If r2, c is even, gcd(c,w)=c/2 and0<w<=c. Thenw is a positive odd multiple ofc/2 not exceedingc, so w=c/2. These are exactly(1).

After the explicit horizontal affine map x -> x/c, an orthogonal billiard preserves actual specular reflection and corner avoidance. The core width becomes1, selected widths become either1 or1/2, and opposite widths become positive rationals. This normalizes the exact family but does NOT put opposite widths on an integer grid. The accepted c1 integer-width theorems therefore do not automatically settle it. A compact ratio or finite selected-width list is not a finite room inventory.

The next real optical gap is illumination for those real/rational opposite widths at the two surviving selected ratios, plus all unequal-selected-width and other endpoint classes. No conclusion about arbitrary diagonal canonical45 rooms or universal wall minimality follows from this hand theorem.
