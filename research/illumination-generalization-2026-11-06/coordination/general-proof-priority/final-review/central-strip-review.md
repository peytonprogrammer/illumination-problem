# Independent review of ST10-E central-strip reduction

Decision: ACCEPT the stated endpoint normalization, guarded local propagation and specified one-sided discontinuity. This closes the pending six-source review at these exact scopes. It does not prove any new all-pair illumination theorem or failure of the full one-left class. No external review or formal verification is claimed.

## Actual endpoint normalization

The accepted four L placements leave S=(s,u), T=(t,v), s>=w2, 0<u<y2, y2<=v<H, 0<t<actual_width(v)<=w2, with (u<y1 OR v>y3) AND (t<w3 OR s>w1).

If t<w3 nothing changes. Otherwise t>=w3 and actual interior membership imply v<y3, including at v=y3 where the narrower width is w3. The second disjunction then forces s>w1; interior membership implies u<y1. Transpose the complete room and reverse endpoint order. Its widths are (H,y3,y2,y1), seams (w3,w2,w1), height w0; its source is (v,t) and target (u,s). All parameters remain strictly ordered. The source satisfies v>=y2 and 0<t<w2; the target satisfies 0<u<y1 and w1<s<w0. These are precisely the new central-strip cross-placement bounds, with the target strictly left of the new narrowest width y1.

Old t=w3 is included by the second case, old v=y2 by its allowed equality, and s=w2 remains allowed in the first case. The map is an isometry of the entire original room, not a covering or surgery. Specular laws, original corners, actual interior endpoints, and native parity are preserved; time reversal restores source order. Thus proving the enlarged normalized domain would suffice for the residual, but that optical premise remains unproved.

## Guarded widening propagation

Use horizontal traveled distance as time. Before the one left reflection, vx=-1; afterwards vx=+1, while the developed vertical derivative remains lambda. At a widening the old strip phase is reduced to W_h(z) in (-h,h). Because the new ceiling hnew>h, both old and new folds equal the absolute value locally at that residual, hence preserve actual height and signed vertical velocity. At residual zero the cusp is a single physical smooth-floor reflection; the original bottom wall does not end at this vertical section. Residual +/-h is a true reflex hit and excluded. At a source exactly on an internal section, initialize in the strip to its left with the actual height and signed velocity, with no preceding artificial contact.

Once x=0 has been reached, 0<t<w3 ensures the returning portion lies wholly inside the full-height central strip. A left contact at height 0 or H is forbidden. If the nominated later target occurs after such a contact, F_H(B-lambda*t)=F_H(B+lambda*t), B in HZ, gives the same actual target on the preceding outward crossing x=t. Truncate before the corner, provided earlier guards hold. At a later target in (0,H), the truncation endpoint is interior. This does not admit a path through a corner.

## Independently derived jump

On the frozen widths (40,12,8,4), heights (0,12,16,20,40), S=(38,2), lambda0=5/13, the first section x=12 has raw phase 2+26lambda0=12. From below, no initial ceiling reflection occurs and the limiting signed phase is +12. From above, one genuine y=12 reflection occurs at x>12 and the residual tends to -12. Add 4lambda0 successively to x=8,4,0 and then 2lambda0 on returning to x=2. This independently gives:

    below: 12, 176/13, 196/13, 216/13, 226/13;
    above: -12, -136/13, -116/13, -96/13, -86/13.

The actual endpoint heights are 226/13 and 86/13, a jump of 140/13. No later critical event coincides: all phase magnitudes at x=8 and x=4 are strictly below the old ceilings 16 and 20; x=0 is strictly between 0 and 40. The prescribed exact check bounds both entire one-sided neighborhoods lambda=lambda0 +/- epsilon, 0<epsilon<1/100. Its affine phase coefficients are 26,30,34,38,40; every stated intermediate guard remains strict. No other room, direction scan, or candidate target was evaluated.

## Limits

The discontinuity defeats an intermediate-value proof across this reflex. It says nothing about attainment on another branch. The frozen target (2,38) is already known illuminated. Central-strip normalization changes the form of the remaining question but supplies no legal ray for an arbitrary remaining pair. All ten-wall staircase, all r3 and all r<=8 illumination remain open. The blocked native goals were not resumed or changed.
