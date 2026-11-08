# GT01: actual target access from the cap at every small positive perturbation

Status: HAND proof pending independent review. This is a target-side optical existence lemma, not a source-to-target illumination theorem. It treats all native bottom target placements in every original integral ordered spiral. It uses the new pinned BD01/NG01/BT01–BT03 argument for the long bottom episode and does not assume those new claims have already received independent acceptance.

## Statement

Use 0<a<l<w<A, 0<b<c<h<H integral, with the original ten-wall boundary specified in `three-reflex-two-sided-bottom-depth.md`. Let actual T=(t,v) satisfy l<t<A,0<v<c with integer coordinates (in particular native even-even). Set

    G=h-c, R=A-w, B=A-l,
    P=2*lcm(a,A,R,B), tau=P+epsilon,
    0<epsilon<1/(2H).

For EVERY such epsilon there exists an EXACT regular state on the downward right cap mouth

    Q=(x_h,h; vx=+tau or -tau, vy=-1), w<x_h<A,

whose ordinary finite original-room continuation reaches ACTUAL T before returning to the cap. Every reflection is on an actual finite wall and avoids all true corners. The state, its sign and its whole trajectory use this SAME tau. No pre-existing illuminated source pair is assumed.

The conclusion is solely existence of an admissible target-bound cap state. The actual source must still reach that exact position and signed velocity at the same tau. Nonempty source and target access sets need not intersect.

The geometry/target data are integral. Epsilon itself may be any positive REAL in the stated interval; this is not an arbitrary-real-geometry theorem. In particular all positive rational epsilons in the interval are included. A successful native S-to-T path would have rational direction by integer unfolding, so access at irrational epsilon alone could not solve that goal.

## 1. Transport of a thin negative c-gate back to h

Suppose an exact incoming bottom state at y=c has

    w<x_e<w+2c*epsilon, vx=-tau,vy=-1.

Trace it backward through the ACTUAL right strip [w,A]x[c,h]. With the physical backward velocity (+tau,+1), the endpoint phase at h is

    x_h=x_e+G*epsilon.

Indeed GP is a full 2R period. Moreover

    0<x_h-w<(2c+G)*epsilon=(h+c)*epsilon<1<=R.

Thus the actual h point is strictly inside the right mouth with the correct negative/downward forward germ. At c the point is also strict because 2c*epsilon<c/H<1<=R. The backward right segment has only ordinary reflections on its real vertical walls, with no simultaneous endpoint collision. No horizontal wall inside this strip is invented. Consequently every legal target-reaching c-gate state in the next two cases gives a genuine target-bound R cap state.

## 2. Targets strictly LEFT of w

For l<t<w the hypotheses of BD01/NG01/BT03 hold because epsilon<1/(2H)<1/(2c). Write W=w-l, y=t-l and L_-=w-t>0. For sigma=-1 or +1, put

    z_sigma=(L_-/epsilon-c-sigma*v)/(2c).

If z_sigma is NOT integral, select m=floor(z_sigma)+1 and

    d=epsilon*(2cm+c+sigma*v)-L_-,
    x_e=w+d.

Then 0<d<2c*epsilon, so this is a strict negative bottom gate. Its endpoint phase is -y, BEFORE the slow fold at x=l. Every intermediate upward c contact is on l<x<w, every bottom-floor contact is ordinary, and no corner is met: all corresponding slow phases remain negative and strictly short of x=l before actual T. The large P component supplies real vertical-wall bounces, not a change of direction between independent rays. The elapsed bottom time is 2cm+c+sigma*v, with actual target ordinate and abscissa exact.

The two values z_- and z_+ differ by v/c, strictly between zero and one. They cannot BOTH be integral. Hence at least one exact safe branch exists for EVERY epsilon; when both exist their incoming states are distinct. The integer m is unbounded as epsilon tends to zero. No fixed reflection/return bound is assumed.

Section 1 now gives a regular downward R cap state reaching actual T. Its horizontal sign is NEGATIVE. This target-side nonemptiness holds even if the original unknown S-to-T pair is dark; it says nothing yet about whether S attains that cap state.

The complete last-bottom-episode characterization in the pinned BD packet allows up to two additional post-left-turn branches, with explicit corner exclusions. They are unnecessary for GT01's existence proof; they are not silently treated as accepted or needed for the safe branches here.

## 3. Target exactly ON x=w

The line x=w is transparent inside the bottom chamber at 0<v<c; T is interior, not the reflex corner (w,c). Treat this placement directly rather than taking a limiting argument from t<w.

For either d=c-v or d=c+v, set

    x_e=w+d*epsilon, vx=-tau,vy=-1 at y=c.

Since 0<d<2c, this is a strict negative gate. Direct descent, or the one ordinary bottom-floor reflection for d=c+v, gives actual T at duration d. No underside contact occurs before T. At every relevant floor/target section the slow x coordinate lies between w and x_e, so it stays away from the actual vertical corner at l. Floor x is w+v*epsilon in the floor branch and is strictly between l and A. The right transport gives

    x_h=w+(h-v)*epsilon or w+(h+v)*epsilon,

with the negative/downward germ. Both are strict R cap states because (h+v)*epsilon<1<=R. Thus GT01 includes t=w with its actual interior-point convention. No unbounded-bottom-depth lower bound is claimed for this equality case; these particular tails have m=0.

## 4. Targets strictly RIGHT of w

Now t-w and A-t are positive integers, so each is at least one. For each sigma in {-1,+1} and d in {c-v,c+v}, set

    F=G+d=h-v or h+v,
    x_h=t-sigma*F*epsilon,
    vx=sigma*tau, vy=-1.

All four x_h are strict R-mouth points because 0<F*epsilon<1. At c the actual state has

    x_e=t-sigma*d*epsilon,

again strictly in (w,A), and the SAME physical horizontal sign. The period identities GP in 2R*Z and dP in 2B*Z justify each fold separately; no source/target chart is independently reselected.

For d=c-v, the genuine right/bottom descent reaches T before hitting the bottom. For d=c+v, the actual bottom-floor contact is at x=t-sigma*v*epsilon, still strictly in (w,A), and the subsequent ascent reaches T. All section, floor and endpoint positions are strict, so no true corner occurs. Between sections the mirrors are the original vertical walls w,A or l,A, and every intermediate reflection is ordinary. Thus four explicit legal cap states are available in this placement. They are sufficient states; no claim of a complete four-state classification for this placement is required here.

## 5. The precise positive step and its remaining coupling

GT01 proves actual target-bound cap access for ALL native bottom targets at EVERY small positive epsilon, rather than only moving a previously illuminating path. The difficult unbounded bottom episode for t<w is chosen exactly through the floor expression, with no scan and no prior illumination assumption. The equality placement is handled directly, and right-side targets use fully guarded original right/floor tails.

This is not yet illumination of an arbitrary actual S,T pair. The source must generate one of these states at that same epsilon with the required horizontal and vertical signs. In particular LR01's FIRST R exit near P has POSITIVE horizontal sign, whereas the left/equality target states constructed here have NEGATIVE sign. Ignoring this mismatch would produce a false connection. The full two-sided return programme must actually create the required directed state after later scattering. No transitivity, recurrence, degree or independent-subroom composition supplies that match automatically.

Next independent challenge: compare the actual source-induced later cap exits to this exact target-bound set while retaining the shared epsilon and every first-hit domain. A proof of that intersection, or a complete obstruction to it, is still needed. All ordered/r3/r<=8 goals remain OPEN.

No numerical example, new room, ray search, engine, census, worker, clock renewal, frozen-source edit or git change was used. The new BD and GT hand arguments are pinned separately for review by the EXISTING author/coordinator; no review agreement is assumed.
