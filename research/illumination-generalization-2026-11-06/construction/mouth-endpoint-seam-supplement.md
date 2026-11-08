# A37 supplement: actual middle-row seams, D=0

This extends the frozen A37 mouth-corner theorem to D=0. The original proof is preserved. The same original A37 effort deadline applies. Independent review is required.

Use its selected height2 teeth of equal width w>0 and actual interior mouth marks S=(c,mu-h), T=(c,mu+h), h>1. These points are interior because each is a strict tooth-mouth midpoint. Require the same protected opposite-wall interval mu-1<y<mu. A left opening may start at mu. In the far chart use D_f=2w and normal depth0. The normal floor is identically0 and normal residual r_d=1. The iteration reduces to

    n_f(tau)=floor(w*tau+1/2),
    Phi(tau)=(h+n_f(tau))/(w+c).

Exactly the A32 first-stationary argument yields a finite stationary tau>0 with r_f=2w*tau+1-2n_f strictly in(0,2). Both far-only choices have the same tau. Their central ordinate displacements are

    +/-m, m=(r_f-1)/2=w*tau-n_f in(-1/2,1/2).

Thus m=0 iff w*tau is integral. If m is nonzero, one choice reflects in the required smooth lower interval and supplies an actual connection.

The geometric zero-depth guard is explicit. In the source-only far chart the virtual source at c+2w folds horizontally to the ACTUAL seam source x=c. Its first physical motion is RIGHTWARD into its selected tooth. Since its actual starting y is the midpoint, any finite slope in that direction immediately enters the tooth interior. It reflects once at the actual far wall, then returns to a strict mouth. In the target-only far chart the normal source arm is empty and its initial velocity points LEFTWARD directly into the core; the upper far arm returns to the actual seam T. Empty normal target arms simply end at the strict seam and require no reflection. No point on the seam is being used as a reflecting boundary.

At a far-wall crossing, the middle-row starting phase reaches a horizontal tooth boundary only if w*tau is an odd integer. Nonintegrality excludes every such corner. All other tooth contacts are strict exactly as in A37. Both source and target remain the actual interior points. The choices of positive or negative vertical midpoint image are retained by floor parity, including a downward initial far arm.

There is a stronger arithmetic sufficient condition here. If m=0, the stationary equation and n_f=w*tau imply

    c*tau=h.

For positive integers c,w,h this gives w*tau=hw/c. Hence resonance requires c to divide hw. Therefore

    c does NOT divide hw

is sufficient for an actual finite corner-avoiding path. It is stronger than the old general-D gcd exclusion and is only a sufficient illumination condition: divisibility does not imply darkness.

In particular for EVEN integer c, w=1 and ODD h, c does not divide h. The seam pair illuminates for every such parameter choice and every admissible extra tooth arrangement preserving the protected interval. This is the dependency needed for the peer's even-core/width1/height2 globally separated odd-band whole-class join. That join remains peer-owned and must separately prove its placement and interval hypotheses.

Reflection of y handles an opening ending at mu instead of starting there. No automatic conclusion is asserted for the integer resonant branch c|hw, unequal widths or all canonical45 rooms.
