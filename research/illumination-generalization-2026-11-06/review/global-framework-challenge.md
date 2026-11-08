# Global framework challenge: a qualifying diagonal branching disk and the missing optical reduction

The uncapped W<=21 theorem remains OPEN. The existing framework has a complete geometric atlas, but no optical theorem covering every atlas fiber. The explicit room below is a calibration of that missing implication. **It is illuminated**, by a prescribed path proved below. It is neither a dark counterexample nor an unresolved illumination example. Its purpose is to prevent an orthogonal or strict-factor classification from being mistaken for the full canonical45 class.

Recommendation: **pivot to an optical reduction that explicitly handles diagonal mirrors and actual endpoint fibers**. Abandon the specific shortcuts “fill the bevel and keep the witness” and “use arbitrary axial rescaling as an optical conjugacy.” They fail exactly below. A different existence-preserving reduction is not disproved and still needs proof. No further comb case catalogue is proposed.

## 1. Exact qualifying geometry

Take the following counterclockwise cycle, with consecutive vertices joined by straight segments:

```
(-1000,-2), (-2,-2), (-2,-10), (2,-10), (2,-2),
(10,-2), (10,0), (8,2), (2,2), (2,10),
(0,10), (-2,8), (-2,2), (-1000,2).
```

Actual selected marks are S=(-998,0), T=(0,8). The polygon is a four-arm cross with two exterior bevels. All fourteen listed turns are genuine, so W=14, not a raw unit-edge count. The two diagonal supports are x+y=10 and y-x=10. Both have even intercept, so they are actual canonical tiling lines. Horizontal and vertical walls are integer-coordinate lines.

Strict simplicity follows either directly from the displayed arms or from exact nonadjacent-segment intersection tests in global-framework-challenge-check.py. No edges overlap or touch nonadjacent vertices. Its area is4100. This is one Jordan disk, with no slit or hole.

For a fully reproducible canonical triangulation, split every unit square [i,i+1]×[j,j+1] along its positive diagonal when i+j is even, and along its negative diagonal when i+j is odd. These are precisely the parity-compatible diagonals. Each triangle has one even-even A vertex. Retain the triangles with centroid strictly inside the displayed polygon. Because every polygon wall is a union of these tiling edges, no retained triangle is cut by the boundary.

The exact checker obtains8200 triangles,5129 tiling vertices and13328 tiling edges, so V-E+F=1. Every edge has one or two incident triangles, the triangle dual is connected, and the boundary edges form one cycle contained in the fourteen actual walls. Thus this is an actual finite canonical45 triangle disk, not merely a polygon with permitted slopes. Both S,T are strictly interior and each has its full eight-triangle A star. They are distinct. Their midpoint(-499,4) lies outside, so the selected pair is not directly visible.

In this specific canonical presentation there are512 interior A points, J=2561 transparent interior non-A points and s_N=1028 smooth boundary non-A points. Thus k=3589>6. These exact finite counts are reproducible membership calculations, not a room census or a bound on the general class.

## 2. What known hypotheses do and do not establish

|Existing route|Audit on this exact input|What remains|
|--|--|--|
|Historical W<=21,k<=6 theorem|W qualifies, k=3589 fails the exception cap|No uncapped conclusion follows from the historical theorem|
|Orthogonal W<=8, L/U/T/staircase room theorems|Fourteen walls, four distinct unoriented wall directions, four-arm branching; not any literal orthogonal normal form|Replacing/trimming the actual mirrors requires an optical transfer proof|
|Unit-core/height-two comb and A0/A1 extensions|The polygon has diagonal walls and a branching cross; it is not the specified rectangular spine with literal axis-aligned teeth and selected normal marks|No existing comb parameter assignment reproduces this room|
|Orthogonal strip generators|Requires an orthogonal polygon; two genuine diagonal supports violate it|The accepted general octilinear atlas supplies geometry only|
|Strict Euclidean whole-copy parity factor, including arbitrary common similarity scale and diagonal bases|Impossible here by the independently accepted R22 invariant: longest/shortest wall ratio499>33sqrt(2)|This rules out that supplied factor for this room; it does not refute “dark W<=21 implies factor,” because this room is lit|
|One-neck eventual illumination|A family varying only the long left arm DOES meet the opposing-chamber hypotheses with fixed other geometry|It gives an eventual tail depending on those chambers; without its threshold it does not settle every finite prefix or classify all W21 rooms. Do not say its hypotheses fail|
|Fixed-shape finite-dark-pair collars|For the stationary normalized pair in a similarity orbit, neither endpoint approaches boundary nor the pair diagonal|Finiteness alone does not exclude a specified isolated pair. Varying only the long arm changes shape and supplies no fixed-shape conjugacy|
|Global marked geometric atlas/finite monoid generators|DOES apply: the full directions, exact actual marks, simplicity and parity enter its cells|No theorem says each base is illuminated or that its unbounded generators preserve existence of a witness|
|Cone-only/full-physical-fiber and translation-surface reductions|Rational-angle unfolding is available; endpoint-fiber and forbidden-corner requirements remain|There is no proved implication from this geometric membership to the required actual physical connection|

The ratio obstruction is exact: minimum wall length2 and maximum998 give499. Squaring avoids approximation:499²>2·33². R22 applies to EVERY strict factor satisfying its literal inverse-map agreement, transparent-point, base-mark and whole-copy assumptions, including a different diagonal base and arbitrary common Euclidean scale. An affine or nonliteral factor would be a different class whose necessity and wall bound are not supplied by this argument.

An invertible affine map cannot turn this room into an orthogonal one: its linear part maps distinct direction lines injectively, so four direction lines cannot become two. More strongly, an affine map conjugating all its actual mirror reflections is necessarily a similarity. Reflection conjugacy forces its positive metric M=AᵀA to commute with the horizontal and vertical reflection matrices, hence M is diagonal. Commutation with either45-degree diagonal reflection then forces its two entries equal. General anisotropic axial normalization therefore cannot repair the missing optical reduction.

The table separates FALSE hypotheses, genuinely applicable but limited theorems, and MISSING implications. It does not claim that every possible future reduction fails. In particular the general atlas is valid and includes this room; optical coverage is the obligation.

## 3. The main actual pair is lit: no darkness inference

Launch from S=(-998,0) with velocity(1,4). Until x=-2 the room section is the full strip -2<y<2. The actual horizontal collision points are

```
x_j = -998 + (4j-2)/4,
y_j = 2 if j is odd, and -2 if j is even,
1<=j<=996.
```

They all have -998<x_j<-2. The last point is(-5/2,-2). After its ordinary floor reflection the velocity points up-right; the ray enters the central core at(-2,0). Its final straight segment runs from(-5/2,-2) to T=(0,8), passing through the central square and then the top arm. It stays strictly to the right of the beveled top-left support y-x=10, and hits no intermediate genuine corner or other mirror. The source arm has y in[-2,2], while T has y8, so there is no earlier T visit. Thus there is a finite actual corner-avoiding path with996 reflections. Exact finite-wall guards validate the whole prescribed path.

This explicit witness is a calibration, not an additional family search and not universal progress by itself. The room's failure of the restricted theorem hypotheses is compatible with actual illumination.

## 4. Proved failure of bevel filling to preserve a supplied actual path

Use a SECOND actual A pair U=(0,0), Z=(6,0) in the SAME room. This distinction from S,T is intentional. The prescribed path is

```
U -> (90/11,20/11) -> (22/3,-2) -> (58/9,2) -> Z.
```

The first contact lies strictly inside the diagonal wall x+y=10. Incoming velocity(9,2) reflects to(-2,-9), and the next two contacts are ordinary bottom/top horizontal reflections. All four open legs stay inside the original room, all contacts are strict, and the original Z is reached first. The checker independently validates all finite-wall intersections and the three reflections.

Now fill the exterior bevels to recover the twelve-wall orthogonal cross. The former diagonal contact(90/11,20/11) is a strict INTERIOR point. The displayed kink cannot be a billiard reflection there. The same initial velocity instead continues to a different actual wall. Therefore the identity inclusion does NOT send this actual connecting path to a legal path in the filled room. The reverse restriction also cannot retain this supplied kink: the mirror has been deleted.

This disproves the claimed pointwise path-preservation property, if used in a reduction. It does NOT disprove equivalence of mere existence for these two rooms. Indeed U,Z are directly visible in both rooms. Any existential surgery lemma needs a separate rerouting argument. No counterexample to illumination follows.

For an equally explicit scaling check, use A=diag(2,1). The image of the true reflected velocity is(-4,-9). Euclidean reflection of incoming A(9,2)=(18,2) across the image diagonal tangent(-4,2) is instead(46/5,-78/5). These vectors are not parallel. Hence this axial scaling fails the ordinary specular law already at one actual smooth contact. Coordinate homeomorphism and canonical shape reconstruction are insufficient optical substitutes.

## 5. Actionable challenge to the global reduction

The author owns the global reduction. This report does not assert that the author claimed the failed shortcuts. Any proposed reduction should state its quantifiers and specify which of these obligations it proves:

1. A source/target-preserving construction of an actual finite path in the ORIGINAL room, including how every removed/added diagonal mirror contact is rerouted.
2. If using a factor, a necessity theorem providing the exact factor assumptions; this room shows those assumptions cannot merely be inferred from W<=21 and canonical geometry.
3. If using compactified wall-count induction, a mechanism lifting a boundary-limit path through degenerating mirror events. Strict word persistence away from degeneration does not handle a newly created corner.
4. If using finite atlas generators, a genuine optical transfer or jointly uniform witness bound for every relevant unbounded fiber, not only a geometric decomposition or isolated one-parameter tail.

Proving one of those for arbitrary inputs would advance the universal goal. This report only supplies an exact qualifying test and two rigorously failed preservation premises. It does not complete any universal bridge. Pending author assessment and independent review are recorded separately.

## Provenance and verification limits

Sources: accepted review/fold-area-invariant-acceptance.json and fold-area-invariant.md; polyhedral-atlas.md/acceptance.json; strip-generators.md/acceptance.json; fixed-shape-boundary-independent.md/acceptance.json; baseline-review.md. Their mathematical conclusions are inherited within their exact scopes. No new external theorem, literature search, worker or optical discovery scan was used.

Own exact checker: global-framework-challenge-check.py/json. Prescribed geometry and paths only. It reuses the disclosed independent finite-wall validator resumed-exact-check.py. This is mathematical reasoning and exact reproducible checking, not formal verification or external expert refereeing. Original R58 aggregate deadline is recorded in global-framework-challenge-effort.json and is not renewed.
