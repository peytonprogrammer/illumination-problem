# Time reversal detects some failed words, but does not characterize R22

For a fixed fully developed target image, write the developed source and target as (0,S) and (D,Y), using absolute longitudinal travel t. Every straight connection satisfies

    y(t) + y(D−t) = S+Y.

The endpoint reflection is (t,y) ↦ (D−t,S+Y−y). Thus if two mandatory windows at complementary times have disjoint images under this reflection, this target image is impossible. A cap insertion changes D and sometimes Y. It may remove one paired obstruction or create a different one; it never removes the displayed identity itself. D158 proves disjointness for the families of words considered there. The converse fails even for a feasible upper-room word in R22.

## A word with a joint slope interval and compatible reversed windows

Use the named R22 pair (0,0)–(2,2). Start leftward; reflect at the vertical cap x=−1 and proceed rightward to the target abscissa. Write t for accumulated absolute horizontal travel. The physical abscissa is −t to t=1, then t−2 to t=4. In the column −1<x<0 the physical height range is (−1,1); in 0<x<1 it is (−2,2); at x=1 take the upper opening (1,2) into the run (1,3). The target is interior to the latter run at x=2. In the normalized 20-wall BBBB edit R22-L1-005, column 0 extends down to −3. The portions visited and all listed windows are identical. [Room cells](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex) · [Edit and four canonical quotients](cap-insertion-law.md)

Develop the initial positive vertical motion, reflecting successively at the physical ceiling y=1 before the left cap, the floor y=−1 after the cap, and the final ceiling y=3 after entering the upper opening. Their developed heights are 1, 3 and 7. On these sheets the longitudinal guards and final section are:

| t | event | open developed height window |
|---|---|---|
| 1 | smooth left cap | (1,3) |
| 2 | entry to the wider column | (3,5) |
| 3 | upper opening | (5,6) |
| 4 | interior of final reflected strip | (7,9), target image 8 |

The reflections at developed heights 1,3,7 must occur respectively inside time intervals (0,1),(1,2),(3,4). The window bounds ensure this order for the positive slopes considered. On the last section the physical height is 10 minus developed height. Substituting y=ts gives the **entire forward slope interval (7/4,2)** for this chart. At s=15/8, for instance, the physical endpoint is (2,5/2). The prefix and all three bounces are legal.

For Y=8 at D=4, the reflected window from t=3 is (2,3), strictly overlapping the cap window (1,3) at t=1. At t=2 the window (3,5) is preserved and contains the forced midpoint 4. There is an even stronger check: the broken line through

    (0,0), (1,9/4), (2,4), (3,23/4), (4,8)

is centrally symmetric about (2,4). It obeys every displayed window and crosses all three developed bounce levels in their prescribed time intervals. So all complementary-time constraints, including the geometry of the intermediate strips, are simultaneously compatible as symmetry constraints. The line bends at times 1 and 3 in the developed chart. A billiard trajectory cannot make those bends.

The only straight slope for that target image is 2. At t=3 it attains 6, an excluded endpoint of (5,6), and hits the physical reflex (1,2). At t=2 it has returned to S. The second half, if legal, would be a shorter shot from S to T whose midpoint is exactly that corner. This describes the obstruction on this particular ray. The d8 exact tracer gives (2,5/2), legal, for initial displacement (−4,15/2), and stops at (1,2) for (−4,8), in both rooms. These replays use prescribed displacements only.

## A two-sided interval criterion that is exact

Fix a single developed chart of convex copies ending on the transverse section t=D, with consistent entry/exit signs. Include the unused-side exclusions specified in the [interval construction](itinerary-slope-interval.md). For clarity assume both endpoints are interior to their initial/final cross-sections; these sections may be cuts through their chambers. Let I_S be the slopes that traverse the whole chart forward from S to the open target section. Let I_T be the slopes that traverse it backward from T to the open source section, expressed as forward-oriented slopes. Assume strict interior gates. When horizontal bounces are encoded by time windows, impose the chart’s transverse sign. Door windows on specified sheets already encode their slope restrictions. Axial chords can be checked separately.

**Lemma.** The chart gives a legal shot from S to this image of T if and only if I_S and I_T overlap. Equivalently the target slope (Y−S)/D belongs to I_S alone, since that chord ends at the prescribed target image. End-section constraints can be retained for the auxiliary slope intervals but are automatic for the target chord.

Write s₀=(Y−S)/D. For a common test slope s, draw the parallel lines y=S+st and y=Y+s(t−D). At their respective crossings of any gate, with times t₁ and t₂ in (0,D), their signed vertical offsets from the chord are (s−s₀)t₁ and (s₀−s)(D−t₂). If s differs from s₀ these have opposite signs. The open gate segment between the crossings therefore meets the chord in its relative interior. If s=s₀ the conclusion is immediate. The chord has the prescribed quadrant, hence crosses the entry and exit sides of each convex copy in the required orientations. Convexity puts the intervening segment inside that copy, which gives the prescribed order and excludes unused-side contacts. Conversely a legal chord itself supplies a common slope. Strict clearance makes this slope interior to both interval tests. Both tests use the same unfolded copies throughout.

In the R22 chart above the complete backward interval is **(2,9/4)**. Indeed the backward heights are 8−(4−t)s; require the three displayed gates and terminal backward height at t=0 in (−1,1). Thus two nonempty open intervals have touching closures and no common slope. This gives the same decision as the one-sided chord test. [D157 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d157-review-doorway/review.md)

## Complete charts including smooth endpoints

Use the actual polygon boundary to decide which cut endpoints can be included. For an exact test, split each gate into its open interior and separate singleton endpoint events. At a tied time group all incident cuts and walls into one event, skipping cells traversed for zero time. Check the incoming and outgoing germs (the short segments immediately before and after the event) in the specified physical cells:

* At an interior point continue straight, including at the intersection of two artificial cuts.
* At a smooth physical wall accept a transversal contact precisely with specular continuation into the room. Count one reflection even if a cut ends there. A cut coinciding with the wall supplies no second event.
* At a physical vertex reject both convex and reflex contacts.

These rules decide inclusion independently for each pair of incoming and outgoing cells. A closed endpoint is an equality constraint on the chord; its slopes can form a singleton. Merely making every gate weak would admit corner shots and incompatible exits. For an axial leg along a cut, suppress that cut and use the interior component of the room on the line of travel, retaining all true boundary contacts, including any physical vertex on the line. An interior-start axial ray can meet a smooth wall only normally; a first tangency along a wall would have to enter at its vertex. At an interior mark on a cut choose the incident germ of the first or last positive-length leg.

**Chart count.** For a prescribed ordered list of e gate encounters with the participating pieces fixed, each encounter has at most three strata (interior, left endpoint, right endpoint), hence at most 3^e refinements. If the incident endpoint is already specified there are at most 2^e. This counts refinements of that event list. A bare physical wall word of R reflections has R+1 legs: in each leg of a fixed rectangular grid with g distinct cut lines a noncoincident line is crossed at most once. Coincident cuts are suppressed as above. Thus there are finitely many cut lists, orders and ties per word. The strict-interval lemma applies only on the open strata; on singleton and tied strata use the direct chord and germ test.

**Coverage.** Develop the candidate physical wall word and subdivide the target chord at successive distinct cut and boundary events. Its positive-length pieces must lie in their named cells, allowing the merged cells along an axial cut. Check relative interiors between successive events and apply the local rule above at every event. Every finite legal shot gives such a subdivision, since a finite number of straight legs meets a finite grid in finitely many isolated crossings after coincident cuts are suppressed. Conversely gluing these pieces by their checked germs gives a corner-free specular shot. This proves coverage in both directions, including tied events, without appealing to openness of a singleton chart.

In R22 the prescribed launch (2,3) from (0,0) hits (2,3) and (4,0), both in the interiors of horizontal physical walls. The grouped events cross the vertical cuts while flipping vertical velocity exactly once each. The next contact is (14/3,1). The earlier target chord stopping at (1,2) still fails: it hits an actual reflex. [D159 replay](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d159-review-timepair/checks.log)

## Scope

The staircase proof selects a dyadic point using the largest power of two dividing an unfolded displacement of a suitably truncated path on the folded base. It does not require disjoint windows at complementary visits of every full physical word. The example disproves that proposed characterization, and its local failure occurs unchanged in a lit W=20 BBBB room. The W≤20 all-itinerary existence question stays open; existence of a chart accepting the target chord restates illumination. No census or direction search was run.
