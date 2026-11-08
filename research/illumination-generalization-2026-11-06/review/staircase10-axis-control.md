# Exact oblique illumination of the frozen ten-wall axis-obstruction control

Status: own HAND construction, exact prescribed full-path verification PASS; offered for reciprocal review. This proves illumination of the ONE frozen room/pair. It does not prove all-metric staircase10, all native placements, allr3, or the broad r<=8 objective. No novelty claim.

## Frozen geometry and actual marks

Widths (40,12,8,4), heights (0,12,16,20,40), actual S=(38,2), T=(2,38). Its ten true vertices in boundary order are

    (0,0),(40,0),(40,12),(12,12),(12,16),
    (8,16),(8,20),(4,20),(4,40),(0,40).

The prior axis-only obstruction and its acceptance stay unchanged. They exclude every word using only x=0,y=0 for this pair; they never asserted darkness. The construction below intentionally uses actual non-axis vertical walls.

## Hand construction at one exact direction

Launch S with velocity(-3,+1), retaining |vy|=1 throughout. The first contacts are

    C1=(0,44/3), C2=(8,52/3), C3=(0,20).

Then append thirteen contacts

    C_(3+j)=(4,20+4j/3) for odd j,
    C_(3+j)=(0,20+4j/3) for even j,
    j=1,...,13,

and finish at T=(2,38). There are16 actual reflections and17 free legs. Every leg has positive vertical velocity and horizontal velocity+3 or-3. At every contact the vertical wall reverses the horizontal sign and preserves the vertical component, exactly specularly.

The three narrowing sections occur at

    y=12: x=8<12,
    y=16: x=4<8,
    y=20: x=0.

The first two are strict interior transparent-mouth crossings. The last is an ordinary reflection on the SAME original maximal left wall x=0, whose endpoints are(0,0),(0,40). The point(0,20) is NOT a genuine corner; it is not one of the ten vertices. It is legal to reflect there while crossing the virtual horizontal band seam. No artificial horizontal mirror or corner continuation is inserted.

The non-axis step contact(8,52/3) lies strictly within the actual finite wall x=8,16<y<20. All following x=4 contacts have20<y<40 and are interior to the genuine top-band right wall. None of the left-wall contacts is a true endpoint. Every contact therefore lies on exactly one original maximal wall and avoids all true corners.

Direct hand containment: from S to C1, x=44-3y; at y12 it is8, and the remaining portion up to44/3 lies in the width12 band. From C1 to C2, x=3y-44; at y16 it is4, then it reaches the actual width8 right wall at52/3. From C2 to C3, x=60-3y, strictly between0 and8 until y20. The remaining alternating legs stay in the width4 top band. All y values increase strictly. Actual T is reached first at vertical elapsed time38-2=36; an earlier point cannot have its height38.

## Exact prescribed validation

staircase10-axis-control-check.py extracts ONLY the existing accepted reviewer pure geometry/path_check functions from resumed-exact-check.py; it executes no historical main block, author selector or discovery code. The path above is prescribed explicitly, not found by a direction scan. The checks prove:

- the ten-wall polygon is strictly simple and both actual even-even marks are interior;
- all17 legs stay within the original polygon and meet no intervening finite wall or true vertex (170 wall/leg guards);
- all16 contacts are on a unique actual wall, ordinary and exactly specular;
- the velocity magnitude/direction ratio is common, with y strictly increasing and initial velocity(-3,+1);
- all narrowing coordinates and the smooth-wall seam contact are exact;
- actual T is the endpoint, reached before any later event.

The paired check JSON contains every rational contact, contacted wall and source hash. All referenced source hashes match before and after. This reuses an existing checker, not a second independent numerical engine. Reciprocal hand review is requested; no peer agreement is assumed.

## Independent review lessons for the pending all-metric candidate

A real path can cross a narrowing at x=0 while ordinarily reflecting on the continuous maximal left wall. A proof may choose to avoid such seam contacts, but a claim to exhaust ALL physical paths or ALL corner failures must not classify this point as a vertex merely because it is a band boundary. By contrast x=w_next at that narrowing is a true reflex corner and forbidden.

Actual INTERIOR marks on a band seam have0<x<w_next; a mark at x=0 lies on the room boundary, and x=w_next is the true corner. These endpoint-placement conventions differ from an intermediate ray's legal smooth-wall seam contact. The all-metric proof must preserve that distinction.

The witness supplies a concrete genuinely non-axis control for the author's new mechanism. It gives no uniform bound16 or direction3 for other metrics/marks, and no completeness of monotone-y vertical-wall itineraries. The all-metric/all-placement target remains open. No room/direction search, fitting, engine, worker, discovery-clock renewal, frozen edit or git-state change was used.
