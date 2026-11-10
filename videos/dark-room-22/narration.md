# The 22-sided dark room

## A point that light cannot reach

Imagine standing inside a room whose walls are perfect mirrors. A tiny light source shines in every direction. You might expect reflections to carry light to every other point. This room challenges that intuition. The source is S, and the target is T. No legal finite reflected ray connects them.

## What does “dark” mean?

Here, dark has a precise mathematical meaning. Light travels along straight segments. At a smooth wall, the angle of incidence equals the angle of reflection. A ray that reaches a polygon corner stops. We ask whether even one finite path, with any number of reflections, can connect the two marked points.

## A pair of points, not a region

The statement is about these two exact points. It does not say that the whole room is dark, or that a neighborhood around T receives no light. It also uses ideal mirrors and point sources. We are studying mathematical billiards, rather than the brightness of a real room.

## Start with five unit squares

The construction begins with a five-square staircase, called P. Each square has side length one. Mark a at zero, zero, and b at two, minus two. Both marks lie halfway along smooth boundary segments. For the moment, they are boundary points. Later, assembling copies will make the corresponding points interior.

## Three reflected copies

Keep the original staircase as P zero. Reflect it across the horizontal axis to obtain P one. Then reflect P one across the vertical line x equals two to obtain P two. The interiors of the three pieces do not overlap. Together they form one connected room.

## The seams are open passages

The first seam is the horizontal segment from minus one, zero to one, zero. The second is the vertical segment from two, one to two, three. These dashed lines are open passages, not mirrors. Their midpoints are S and T, so both marked points are genuinely inside the assembled room.

## Exactly 22 exterior walls

Trace only the exterior boundary. It has twenty-two maximal straight sides: thirteen convex corners and nine reflex corners. The room has no holes, interior partitions, crossings, or boundary self-contacts. Its area is fifteen square units. The colors distinguish the three copies; they do not represent separate compartments.

## Fold the room onto one staircase

To prove the result, map all three copies back onto P. Leave P zero unchanged. Flip the sign of y on P one. On P two, send x to four minus x, and y to minus y. The formulas agree on the shared seams, giving a continuous folding map.

## S maps to a; T maps to b

Under this map, S becomes a, and T becomes b. A hypothetical connecting path in the full room would therefore become a path from a to b in the staircase. This reduces the geometry, but we must check how each possible physical event behaves after folding.

## Crossing becomes reflection

Away from a seam, folding is an isometry, so it preserves straight segments and mirror reflections. Crossing the interior of a seam reverses the normal component of the folded velocity. In the staircase, that crossing therefore looks exactly like an ordinary reflection at a smooth wall.

## First, rule out ordinary paths

Set aside the seam endpoints for a moment. We first prove that an ordinary, corner-avoiding billiard path cannot connect a to b in P. The crucial observation is visible on the integer grid: P has no interior lattice points. Its only smooth boundary lattice points are a and b.

## Unfold the reflections

Suppose such an ordinary path exists. Instead of bending the ray at each reflection, reflect the room across the wall. After all its finitely many reflections are unfolded, the path becomes one straight segment. It starts at a, the origin, and ends at some reflected image B of b.

## Every endpoint image stays even

Every wall lies on a line x equals an integer, or y equals an integer. Reflection across x equals c sends x to two c minus x. That preserves whether an integer coordinate is even or odd. Since b has two even coordinates, every unfolded endpoint B also has two even coordinates.

## Find an odd lattice point

The unfolded segment has positive length, so B is not the origin. Divide both coordinates of B by two as many times as possible while they remain integers. Write B as two to the r times z. Here r is at least one, and z has at least one odd coordinate.

## The obstruction lies on the segment

Because z equals B divided by two to the r, it lies strictly between the origin and B. For example, if B were eight, minus four, then z would be two, minus one. This is an arithmetic illustration, not a claimed trajectory. The same division works for every possible nonzero even endpoint.

## Fold z back: it must be a corner

Now fold z back using the hypothetical path’s unfolding itinerary. Every inverse reflection preserves integrality and coordinate parity. Its image is therefore a lattice point of P with at least one odd coordinate. It cannot be a or b. Every other lattice point of P is a vertex. The supposed path hits a corner.

## A contradiction for every finite itinerary

That contradicts the corner-avoiding rule. We have ruled out every ordinary finite billiard path from a to b, regardless of direction, length, or reflection count. This is a proof about all finite itineraries. A computer failing to find a path, even after many trials, would not establish the same statement.

## Four points need special care

There is one remaining issue. Four seam endpoints are smooth points of the exterior wall in the full room, yet fold to convex corners of the staircase. Hitting them is legal in the full room. We cannot simply forbid them because their folded images happen to be staircase vertices.

## Two sign changes make a reversal

Consider the horizontal seam’s right endpoint, at one, zero. A ray arriving from the upper copy with physical velocity u, minus v folds to velocity u, v. The vertical exterior mirror changes the physical velocity to minus u, minus v. The ray enters the lower copy, where folding is the identity.

## The folded ray retraces its route

The outgoing folded velocity is thus the negative of the incoming one. This is an exact reversal, not an ordinary right-angle corner continuation. At the other horizontal endpoint the calculation is analogous. At the two vertical seam endpoints, interchange the horizontal and vertical roles. All four exceptional events produce the same reversal.

## No other corner loopholes

Why are these the only exceptions? The staircase has ten corners, giving thirty corner incidences across three copies. Two incidences meet at each of the four smooth seam endpoints. Removing those eight leaves the twenty-two actual corners of the room. No reflex staircase corner is the image of a smooth point in the assembled room.

## Assume a connecting path exists

Suppose a legal path in the full room still connects S to T. Its folded version goes from a to b by ordinary reflections, perhaps interrupted by these reversals. Stop it at its first arrival at b. Then retain only the part beginning at its last visit to a before that arrival.

## Choose visits in the folded staircase

That last visit must be chosen in the folded staircase. Every visit to a counts, even if the physical path is at a different preimage in the full room. The retained subpath has no interior visit to a or b. There are only finitely many visits because the path has finitely many nonzero straight legs.

## The first reversal forces a return

If this subpath has a reversal, choose its first one. Before it, motion consists entirely of ordinary reflections. Billiard motion at smooth walls is deterministic and reversible. After reversing its velocity, the path must retrace that entire preceding route, in reverse order, until it returns to a.

## Either case gives a contradiction

It cannot encounter b on that return: then it would already have passed through b before the reversal, contradicting the first-arrival choice. So it revisits a before reaching b, contradicting the last-visit choice. There can be no reversal. But an ordinary path from a to b is already impossible by parity.

## Back to the 22-sided room

This completes the proof. An axis-parallel ray cannot connect S and T because both coordinates differ. Every other finite ray crosses the seams transversely only finitely many times. Its folding is therefore a finite path of exactly the type we ruled out. No legal finite trajectory connects these two interior points.

## Geometry turns into parity

The entire mechanism is now visible. Three staircases put the marks inside one room. Folding reduces that room to a lattice problem. Parity forces an ordinary connecting path through a corner, and the only extra events merely reverse the route. Construction and manuscript: Peyton Wang, primary author, and Daniel Wang. Codex and Claude assisted the research and exposition.