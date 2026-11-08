# Independent acceptance: all real equal- and unequal-floor T rooms

Verdict: ACCEPT both T-room-theorem.md and uneven-T-theorem.md in their FULL all-interior-pair scopes, without a k, size, aspect-ratio or arithmetic restriction. The second contains the first. This adds a genuine cap-free class to the main objective; it does not close that objective.

## Accepted dependency and logic

I reread the actual arbitrary-real L construction and its two-orientation assertion. A horizontal-only L path has no vertical-wall contact; the transposed vertical-only path has no horizontal-wall contact. These properties include contacts at smooth wall points, not merely reflections in a bounded itinerary. Endpoints in these applications are strictly interior to the chosen L. No local trajectories are concatenated.

I independently checked the equal-floor placement split and each artificial cut. Shared bar or stem-column pairs have direct visibility. In the remaining case, the stem mark is strictly below the bar and the wing mark is strictly outside the stem, so the appropriate Q_left or Q_right really contains both in its interior. Every allowed horizontal reflection wall is a genuine original T wall. The sole artificial cut is vertical, and its lower endpoint is a genuine T reflex corner that may be smooth on the L boundary. Horizontal-only reflection paths avoid the entire vertical wall, including that point. Restoring the omitted wing therefore changes neither the chosen path nor its reflection law.

## Unequal-floor case: independent endpoint/corner audit

The assignment of marks with x<=a to the left, a<x<b to the stem, and x>=b to the right is exhaustive and disjoint. Interior points on x=a satisfy y>u; those on x=b satisfy y>v. Thus same-region segments and same-seam segments stay in the actual polygon interior.

For a stem/left pair Q_L contains the entire stem and left wing needed by the marks. Its horizontal walls at0,u,C are genuine P walls. The potentially artificial boundary is on x=b and is never touched. This removes the actual corner (b,v) even if it is a smooth point of the chosen L boundary. Reflection and the analogous Q_R handle the right case.

For an opposite-wing pair assume u<=v by reflecting the WHOLE room and marked pair if necessary. When the left mark has y_s>=v, direct visibility in the upper common rectangle is valid. At equality y_s=v the target has y_t>v, so every open point of the segment has height>v; the equality is not an artificial-wall trajectory.

Otherwise u<y_s<v and Q=([0,A]x[v,C]) union([0,b]x[u,v]) contains BOTH actual marks strictly in its interior, including x_s=a or x_t=b. Its vertical walls are the genuine x=0 aboveu, x=A abovev, and x=b fromu tov. Its artificial horizontal floor at y=u over(a,b) is avoided by the vertical-only L path. The extra actual P corner (a,u), smooth on this L floor, is avoided by the same orientation restriction. The actual corner (b,v) is an L corner and already excluded. The stem bottom is outside Q. This checks every actual corner and every candidate artificial reflection, not just generic placements.

Thus one complete ordinary billiard connection in the chosen L is already an ordinary finite corner-free connection of the original polygon, at the actual S,T. All real parameter values in the stated inequalities are covered.

## Exact independent controls

T-whole-check.py independently checks the prescribed9-contact equal-floor witness and17-contact unequal-floor witness using Fraction arithmetic and the complete finite physical wall segments. All28 open segments stay strictly inside, all26 contact points lie on exactly one genuine smooth wall, and all26 reflected velocities satisfy the ordinary specular law. This did not run a peer checker or discover another ray. It supplements the arbitrary-real hand argument; two fixtures alone would not prove it.

My overlapping long-stem T construction also passed8640 prescribed exact paths, but was developed after the peer's stronger proof was already frozen. It is superseded and is not an additional theorem or justification for this acceptance.

## Scope

ALL equal/unequal-floor T8 rooms in the stated normal form illuminate every distinct real interior pair at arbitrary k. All-real L6 and U8 retain their earlier independent acceptances. Eight-wall staircase and offset-corridor types, diagonal-wall polygons, and the full uncapped W<=21 target remain open. No novelty or universal-minimum claim is made.
