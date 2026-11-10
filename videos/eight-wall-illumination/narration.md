# When darkness is impossible: eight-wall illumination

## When darkness is impossible

The dark-room construction showed that mirrors do not always connect two points. Now turn the question around. How simple must a room be before a connection is guaranteed? This manuscript proves that every strictly simple orthogonal room with at most eight walls illuminates every pair of distinct interior points.

## What exactly is guaranteed?

Orthogonal means every wall is horizontal or vertical. Count maximal straight sides, not grid subdivisions. The boundary cannot cross or touch itself, and the room has no holes. A legal path has finitely many straight legs, reflects at smooth wall points, and never hits a corner. The dimensions need not be rational.

## A proof map, with worked constructions

The full manuscript has a substantial case analysis. This video gives its proof architecture and works through the central constructions. We will prove the turning-count reduction, explain the L-room mechanism in detail, and show how the remaining cases close. The complete corner and equality checks remain in the manuscript.

## Count turns around the boundary

Walk around the boundary counterclockwise. Each convex corner turns you left by ninety degrees; each reflex corner turns you right by ninety degrees. One complete trip turns through three hundred sixty degrees. Therefore the number of convex corners minus reflex corners is four. Combining that with the wall count gives r equals W minus four, divided by two.

## Eight walls means two reflex corners

So four walls force a rectangle. Six walls allow one inward corner, giving an L. Eight walls allow exactly two inward corners. Their shorter cyclic separation along the boundary is one, two, three, or four edges. Up to rotation and reflection, these are the U, staircase, T, and offset corridor.

## The metric freedom stays

These pictures represent families, not a few selected floor plans. Arms can have different widths and heights. In the T, the two wing floors may be at different levels. In the offset corridor, the outer arms may have disjoint horizontal projections. The classification retains every admissible real metric of each type.

## A rectangle needs no reflection

Inside a rectangle, the direct segment between two interior points stays inside. An L is the union of two rectangles, so many endpoint placements are just as easy. The difficult placement puts the source in the lower outer arm and the target above the inward corner. Direct visibility may then fail.

## Control the reflection orientation

The L theorem gives more than a connection. It gives a path using only vertical wall reflections, with monotone height. Exchanging coordinates gives a second path using only horizontal reflections. This choice is essential later: it lets us use an L-shaped subroom without bouncing off an artificial boundary.

## Unfold the narrow upper strip

Let the narrow upper strip have width a. Unfolding its vertical reflections creates target images at plus or minus x sub t, plus two m a. Consecutive image gaps alternate between twice x sub t and twice a minus x sub t. Both gaps are strictly smaller than twice a.

## Choose an image that clears the corner

Write D sub s and D sub t for the vertical distances below and above the seam, and r for their ratio. Put h equal to minus r x sub s. The image spacing lets us choose an image X at a nonzero distance at most a from h. Symmetry lets us choose the source sign consistently.

## The seam crossing is strictly interior

The developed straight segment crosses the seam at q, equal to the chosen distance divided by one plus r. Therefore q lies strictly between zero and a. That is the key guard: the path passes through the open mouth instead of the inward corner. Folding the upper strip brings the endpoint back to the actual target.

## Fold back to an actual ray

Below the seam, the construction has at most one reflection at the left wall. Above it, the narrow-strip folds occur strictly between the seam and the target height. They are smooth contacts, never corners. Height increases throughout. The displayed ray is one prescribed exact example from the manuscript, not a search for a lucky direction.

## A cut inside the room is not a mirror

Now place an L-shaped subroom inside a larger room. Some of its boundary may be an artificial cut. We cannot use that cut as a mirror. Instead choose the L theorem’s reflection orientation so that every wall the ray actually touches is a genuine exterior wall. This is how the T case reduces to the L engine.

## The U needs an opposite-arm connection

In a U, the remaining difficulty is a source in one upper arm and a target in the other. The construction unfolds repeated vertical reflections in each arm and the lower strip. A finite matching procedure chooses compatible portal heights. The resulting ray uses one smooth floor reflection, plus vertical reflections, to join the arms.

## Finite matching, not a limiting argument

Why does that procedure finish? Its selected unfolded arm lengths are nondecreasing step functions of the slope parameter. The induced iteration is nondecreasing and bounded. On the bounded interval, only finitely many step values occur, so the iteration becomes stationary after finitely many updates. A jump at the first stationary value would contradict stationarity.

## Keep the U portals open

The non-jump property gives strict portal inequalities. Both passages are below the notch floor and above the actual floor. A separate bound places the floor contact strictly away from the two bottom corners. Thus neither the portal crossing nor the floor bounce hides a forbidden corner event. Every part uses the same compatible unfolded direction.

## The offset corridor uses slope windows

In the offset corridor, first restrict the slope to an open interval that clears the lower mouth. A nested interval also clears the upper mouth. Over that interval, the developed target coordinate ranges through more than one target-image period. It must contain a target image. Folding then gives a vertical-only connection to the actual target.

## One placement needs new work

The staircase is the most involved case. If the endpoints fit inside a lower or upper L-shaped subroom, the orientation-controlled theorem handles them. The remaining cross placement goes from the lower outer arm to the upper narrow arm. Here the proof needs two portal guards and a choice between floor and roof constructions.

## Strict windows clear both inward corners

The developed coordinates at the two seam heights are called z and w. The inequalities absolute z less than b and absolute w less than a keep the path away from both reflex corners. The folded formulas agree in position and velocity across each seam. A seam is crossed, not used as an added mirror.

## The floor chart

Under condition F, reflect the source across the floor and apply the nested-window construction. The developed target range contains two consecutive target images. Their candidate floor contacts are less than one full room width apart, so both cannot be floor corners. Choose the one with a smooth floor bounce, then fold to the target.

## The roof chart handles another regime

A second construction develops a reflection at the roof. Its sufficient condition is R v, shown here. A partial portal window becomes large enough, after the roof development, to hit a target image. If the candidate roof contact would be a corner, the argument shows that the actual target was already reached earlier. Stop the path there.

## Four conditions cover all metrics

Swapping the axes supplies the transposed floor and roof conditions. The proof must show that at least one of the four always holds; showing several attractive ray examples would not suffice. It normalizes the dimensions using alpha equals a over b, beta equals c over d, and p equals alpha beta.

## The coverage step is algebraic

If neither floor condition holds, the normalized inequalities force at least one roof condition. The remaining calculation splits at p equals one third. In one range the lower bound factors as twice the square of one minus the square root of p, times one plus the square root of p minus p. In the other it exceeds the square of one minus p. Both are positive.

## Six families, every interior pair

We can now assemble the result. Classification leaves a rectangle, an L, a U, a T, an offset corridor, or a staircase. Each family has a connection argument covering every interior pair. The manuscript explicitly handles internal-seam endpoints, rounding ties, equalities in the metric conditions, and potential floor or roof corner contacts.

## What eight walls does not mean

The guarantee is existence of some finite legal path. It is not a uniform bound on reflections across all possible room dimensions. Eight walls also means at most two reflex corners, not eight reflex corners. The theorem does not settle every ten-wall room, allow diagonal walls, or establish the universal twenty-two-wall minimum.

## A small boundary forces a route

The lesson is constructive. Counting inward corners reduces the universe of small orthogonal rooms to six types. Controlled unfolding then gives routes through each type without inventing mirrors at internal cuts. This video presents the proof map and central mechanisms; the manuscript contains the full technical proof. It remains a working draft, not externally refereed.