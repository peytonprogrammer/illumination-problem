# Short-cap necessity for every one-roof vertical-mirror word

This is a new hand-derived necessary restriction on a physical mechanism. It is not a dark-room claim or a rejection of TR03, whose roof hypothesis is sufficient. It covers arbitrary reflection words within the stated mechanism, rather than only one selected root. No discovery search or additional fixed room is used.

Use the accepted ordered spiral notation `0<a<l<w<A`, `0<b<c<h<H`, `R=A-w`, `B=A-l`. Let actual S lie in the lower left column, `0<s<a`, `b<u<h`, and let actual T lie in the lowest chamber, `l<t<A`, `0<v<c`. Write `epsilon=H-h`, `d=c-v`, `z=A-t`.

Consider ANY legal actual S-to-T trajectory whose only horizontal-wall reflection is one contact with the outer roof y=H. Every other reflection is on an original vertical wall. Let q be its number of contacts with the inner bottom wall x=l **after its descending crossing of y=c**. The trajectory has fixed `tau=|vx/vy|>0`.

Then necessarily

```
tau > (w-a)/(2 epsilon),
tau*d < 2q B+z+R,
q > [d(w-a)/(2 epsilon)-z-R]/(2B).
```

In particular, a trajectory in this mechanism with no inner-bottom-wall contact requires the STRICT inequality

```
2(H-h)(A-t+A-w) > (c-v)(w-a).
```

If the reverse weak inequality holds, no such q=0 trajectory exists, regardless of its source-arm, cap or right-arm period labels, initial horizontal sign, smooth portal-wall contacts, or number of those vertical reflections. This specifically limits the j=0 target-bottom chart used by TR03. It does not refute TR02 with unrestricted bottom periods or any other optical mechanism.

## Physical proof

Normalize |vy|=1. Because only a horizontal mirror reverses vy, the trajectory ascends from S to H and then descends to T. Its ascending first h crossing has x in `[0,a)`; its descending h crossing must have x in `(w,A]`. A descending left-arm exit cannot reach the lowest chamber without a further horizontal reflection: at every height c<y<h the left and right strips are disconnected, and below c the left column is separated from the bottom chamber by the notch. The path thus must use the right strip on its descent.

The elapsed time between those h crossings is exactly `2epsilon`. Reflections at vertical walls leave |vx|=tau unchanged. The total horizontal travel is `2epsilon*tau`, at least the absolute displacement between the two crossings, which is STRICTLY greater than w-a. This proves the first inequality even if either crossing is on its smooth outer vertical wall. No unfolding-label inference is needed.

At the descending c crossing put `Y=A-xportal`, so `0<=Y<R`; the strict upper inequality is exactly the genuine mouth guard xportal>w. The final segment remains in the bottom rectangle because y decreases from c to v. Its only possible mirrors are x=l and x=A. In the distance coordinate `Yphysical=A-x`, these are B and 0; the actual target is z in `(0,B)`.

Any one-dimensional reflected path from Y to z with q contacts at B has length at most `Y+2qB+z`. To see this, if its initial direction is toward 0, it travels Y to 0, then q full trips 0->B->0, and finally z to the target. If it ends before the final return to 0, that path is shorter by 2z. If its initial direction is toward B, append the virtual initial segment 0->Y: the same counting gives length plus Y at most `2qB+z` (or `2qB-z` when it ends on the last return). The q=0 direct possibilities also satisfy the bound. Contacts at 0 exactly at the portal are included as zero initial distance. Therefore its length is strictly less than `R+2qB+z`, since Y<R. Its actual length is `tau*d`. This proves the second inequality. Combining the strict inequalities proves the q bound, including equality in the excluded q=0 regime.

An integer form is `q>=max(0,floor(K)+1)`, where `K=[d(w-a)/(2epsilon)-z-R]/(2B)`. For fixed horizontal widths and target away from y=c, K diverges to infinity as epsilon tends to zero. Thus one-roof trajectories, IF they exist throughout arbitrarily shallow caps, necessarily require unboundedly many inner bottom reflections. This is a lower bound conditional on this entire mechanism, not a claim that arbitrary rays need many reflections or that such rays always exist.

## Consequence for the next construction

Refining source/right nearest-period choices cannot make the no-inner-bottom chart cover all short caps. In the displayed excluded regime, the construction must use inner-bottom reflections, another horizontal mirror pattern, or a genuinely different trajectory. The unrestricted bottom periods in TR02 are therefore material and cannot be removed by a universal j=0 normalization without a new physical argument. The accepted all-pair tall theorem and all earlier positive witnesses remain valid.

The author owns constructive short-roof selection. This reviewer result supplies a disjoint necessary-condition challenge and a quantified guard for that future proof. Full r3 and r<=8 remain open.
