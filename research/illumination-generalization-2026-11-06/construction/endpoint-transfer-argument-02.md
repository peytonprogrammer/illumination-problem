# ET02: one-wall endpoint repair fails with five physical reflex corners

## Precise negative result

The conjectural broadened premise in candidate-02 is false. A strictly simple orthogonal lattice room with r=5 and W=14 has distinct actual interior even-even marks whose direct chord meets exactly one true reflex corner, but no legal path between them with zero or one reflection. They have the two-reflection path below. This refutes universal ONE-wall repair, even with arbitrary choice of physical wall and no rectangular-collar requirement. It does not refute unrestricted endpoint repair or the full r<=8 illumination objective.

## Actual geometry

Use this counterclockwise boundary, with its last vertex joined to its first:

    (0,0), (49,0), (49,19), (51,19), (51,0), (80,0),
    (80,40), (40,40), (40,80), (0,80), (0,51), (19,51),
    (19,49), (0,49).

It is the L-shaped union [0,80]x[0,40] union [0,40]x[0,80], with two open-to-exterior rectangular notches: the floor indentation (49,51)x[0,19], and its coordinate-swapped left indentation [0,19]x(49,51). The boundary coordinates above specify the retained walls precisely. The disjoint notch boundaries have no contacts with the outer arm boundary or one another. All successive edges are nonzero and perpendicular; nonadjacent edges are disjoint. Thus this is a finite strictly simple disk, without holes, slits or self-contacts. Its integral orthogonal boundary admits the canonical45 unit-square triangulation.

The five reflex vertices are (49,19),(51,19),(40,40),(19,51),(19,49). The other nine vertices are convex. Consequently W=14=2r+4.

Set S=(60,20), T=(20,60), C=(40,40). Both marks are strictly interior, distinct and even-even. The direct chord x+y=80 runs in the lower-right arm before C and the upper-left arm after C; both notches are disjoint from it. It meets the true corner C and no other boundary point. This is exactly a straight one-reflex-degenerate actual match.

## Exhaustive one-reflection exclusion

For a single specular reflection on a horizontal wall y=h, reflect the ACTUAL target to T_h=(20,2h-60). A legal path requires the segment from S to T_h to meet that finite wall at a parameter strictly between zero and one. It must also reach the contact without another boundary hit. This is a necessary condition for every one-reflection path, with no bound on directions and no sampled search.

There are seven horizontal segments, on six distinct supports. The two floor pieces share y=0 and the same reflected target. The complete table is:

| Support | Physical wall x range | Candidate | Exact exclusion |
| --- | --- | --- | --- |
| y=0 | [0,49] or [51,80] | (50,0) | Contact lies in removed notch mouth, on neither actual wall. |
| y=19 | [49,51] | (1240/21,19) | Abscissa exceeds 51. |
| y=40 | [40,80] | No contact | Developed segment has constant y=20. |
| y=49 | [0,19] | Parameter 29/18 | Contact would occur after the developed target. |
| y=51 | [0,19] | Parameter 31/22 | Contact would occur after the developed target. |
| y=80 | [0,40] | (30,80) | Source leg hits physical wall first at (50,40). |

For example, the y=19 image is (20,-22), so its contact parameter is 1/42 and its abscissa is 60-40/42=1240/21. For y=49 and 51 the image heights are respectively 38 and 42, giving the stated parameters. For the roof contact, the initial leg rises from (60,20) to (30,80), meeting y=40 at x=50, strictly on the actual inner ceiling. Even earlier obstruction would also invalidate this proposed one-reflection path.

Coordinate swap (x,y)->(y,x) preserves this entire room and swaps S,T. Applying it to a putative vertical one-reflection S-to-T path and then reversing time gives a horizontal one-reflection S-to-T path. Reversibility preserves reflection legality and all corner/first-hit conditions. Therefore the table also excludes every vertical wall. All fourteen actual segments are accounted for. Tangent contact cannot change an interior straight ray's direction or bypass C; wall endpoints are forbidden true corners. No legal zero- or one-reflection connection exists.

## Exact legal two-reflection connection

Let F=(160/3,40) and G=(40,0). The actual path is

    (60,20) -> (160/3,40) -> (40,0) -> (20,60).

The three displacement vectors are respectively

    20*(-1/3,1), 40*(-1/3,-1), 60*(-1/3,1).

All scalar travel times are positive. At F and G only the vertical velocity changes sign; the horizontal velocity remains -1/3. These are exact specular reflections at horizontal actual walls. F lies strictly inside the inner ceiling x in (40,80), and G lies strictly inside the floor x in (0,49).

Whole-leg physical guards:

1. S-to-F lies in the lower-right arm, with y in [20,40] and x in [160/3,60]. It stays above the floor notch and right of its x range; it first reaches boundary at F.
2. F-to-G has x=40+y/3 for 0<=y<=40. Except for F and G it lies strictly inside the lower arm. At floor-notch abscissae 49<=x<=51 its height is 27<=y<=33, strictly above 19. It never approaches the left notch. It reaches G before any other boundary.
3. G-to-T has x=40-y/3 for 0<=y<=60. For 0<y<40 it lies in the lower arm; at y=40 it crosses strictly into the upper arm at x=80/3<40. For 40<=y<=60 it lies strictly in the upper arm. At left-notch heights 49<=y<=51 its x coordinate is between 23 and 71/3, strictly greater than 19. At floor-notch heights y<=19 its x coordinate is at most40<49. It meets no corner or other wall before actual T.

The x coordinate strictly decreases along the full path, so neither earlier leg reaches actual T at x=20. This proves actual target attainment, signed velocity matching, first-hit legality and true-corner avoidance without changing endpoint lifts or introducing abstract sectors. The minimum number of reflections for this actual pair is exactly two.

## Implication and limitation

ET01 remains a correct conditional remote-floor repair. Its universal full-collar availability fails at r2. ET02 removes that full-collar restriction and allows EVERY actual single wall, yet availability still fails at r5. The failure is therefore not just an overly strong rectangular containment test. A general physical transfer theorem must accommodate multiple remote contacts and their complete joint guards.

This room is lit. It gives neither a trapped transfer cycle nor a bound requiring nine DISTINCT physical reflex corners. No completeness or finiteness of an unrestricted transition graph follows. Isolated singular-match repairs also do not cover root-free intervals. The global r<=8 theorem remains open.

Method: one predeclared hand-designed polygon; finite exhaustive actual-wall reflection argument and one prescribed exact witness. No computational discovery, room census, coefficient fitting, new engine or search clock.
