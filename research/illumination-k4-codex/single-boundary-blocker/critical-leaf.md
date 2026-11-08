# The critical-leaf remainder: an exact cylinder exception

[done] Written proof and prescribed exact algebra/geometry controls.
[waiting on Claude] Independent review requested.
This sharpens findings.md. It does not prove universal blocker removal.

## Setup

P is a bounded strictly simple orthogonal room. Its four-copy unfolding is M,
pi:M->P is the folding map, and iota has derivative -I and pi*iota=pi.
Let F be the actual corner lifts. Convex corners lift to regular points F_reg;
reflex corners lift to zeros Sigma. The fixed set of iota is F.
Let s,t be distinct interior marks and z a smooth wall point. Write
Z=pi^(-1)(z)={b,iota(b)}. A single-blocker example would mean that an ordinary
s-to-t connection exists, but every such connection meets z.

An ordinary cylinder below avoids Sigma, but may contain regular convex corner
lifts. This is a weaker condition than the corner-free marked cylinders in
findings.md, so the result covers more configurations.

## 1. Removing regular corner contacts while preserving blocker avoidance

**Lemma.** A finite straight segment on M avoiding Sigma and Z, from any lift
of s to any lift of t, contains a subsegment whose physical projection is an
ordinary corner-free billiard connection avoiding z.

**Proof.** Along the finite segment, mark the times whose physical projection
is s or t. There are finitely many: each endpoint fiber is finite, and a
nonstationary straight trajectory has isolated returns with a positive local
return-time bound. Since the first label is s and the last is t, some two
consecutive marked times have opposite labels. Reverse this subsegment if
needed to obtain a segment beta from s to t with no interior visit to either.

Suppose beta passes through a regular convex corner lift c at time a. Since
iota(c)=c and D iota=-I, straight-flow uniqueness gives

    beta(a+u)=iota(beta(a-u))

on the common time interval. Thus its physical projection retraces about a.
If a<T/2, the physical source reappears at time 2a in (0,T). If a>T/2, the
physical target appeared at 2a-T in (0,T). If a=T/2, the endpoints have the
same physical projection. Every case contradicts the chosen segment or s!=t.
So beta avoids F_reg as well as Sigma. It still avoids Z, since it is a
subsegment of the original segment. Its projection is the desired connection.
QED.

This is the blocker-preserving version of the regular-corner observation in
Wolecki Remark 2.2. It does not erase a smooth boundary blocker: those lifts
are exchanged by iota, not fixed by it.

## 2. A two-point obstruction in a cylinder has a rigid transverse location

Use ordinary cylinder coordinates (R/LZ)x(0,h), and distinct transverse
coordinates u!=v for x=(a,u), y=(d,v). The n-winding segment develops from
(a,u) to (d+nL,v). A blocker b_j=(q_j,w_j) can meet it only when

    lambda_j=(w_j-u)/(v-u) in (0,1),
    q_j = a+lambda_j(d-a+nL) mod L.

A single blocker cannot meet consecutive winding numbers, because subtracting
the two congruences would make lambda_j an integer.

**Four-winding lemma.** If two blockers together meet all n=0,1,2,3 segments,
then both are at transverse midpoint (u+v)/2 and their horizontal positions
differ by L/2 modulo L.

**Proof.** Each blocker meets no consecutive winding numbers. Covering four
consecutive indices by two such sets forces alternating ownership: one blocker
meets 0,2, the other 1,3, or the labels are reversed. An index hit by both
would leave an adjacent index uncovered. Subtracting the equations for n and
n+2 gives 2lambda_j integral, so lambda_j=1/2. The adjacent indices then put
the horizontal blocker positions L/2 apart. QED.

This is a necessary condition obtained from four prescribed cylinder segments,
not a discovery search and not a statement that midpoint blockers always block.

## 3. Ordinary-cylinder removal, with its one exact exception

The rectangle case has direct interior visibility and cannot have an essential
boundary blocker. For the following theorem suppose P has at least one reflex
corner, so M has genus at least two and a nonempty zero set. This excludes the
unmarked flat-torus exception to disjointness of maximal parallel cylinders.

**Theorem.** Suppose some lifts x of s and y of t lie in a common ordinary
maximal cylinder C. If z is essential, then all of the following hold:

1. iota(C)=C.
2. x,y and both lifts of z lie on its central core y=h/2.
3. On that core, x and y lie in different components after deleting Z.

The central core contains exactly two regular convex corner lifts. It folds
into a retracing convex-corner-to-convex-corner billiard arc; the physical z
separates s and t along that arc.

**Proof.** iota(C) is a maximal cylinder in the same unoriented direction. If
it is distinct from C, the two cylinders are disjoint. C then contains at
most one point of Z. The consecutive-winding/complementary-arc argument of
findings.md gives an x-to-y segment avoiding Z. It may pass through regular
convex corner lifts, but Lemma 1 repairs it. This contradicts essentiality.
Thus iota(C)=C, and in cylinder coordinates

    iota(q,w)=(-q+c mod L,h-w).

Its exactly two fixed points are on the central core. As C has no zeros,
these fixed points are regular convex corner lifts.

If u!=v, essentiality implies that all four n=0,1,2,3 x-to-y segments meet Z:
an avoiding segment could be repaired by Lemma 1. The four-winding lemma
forces both z lifts to have height (u+v)/2. Their involution relation then
forces that height to be h/2, and u+v=h. But iota(y) has height h-v=u,
which is not h/2 since u!=v. Hence x and iota(y) lie on the same off-center
core circle and Z misses that circle. They are distinct because s!=t. A core
arc between them avoids Z and Lemma 1 again supplies an ordinary connection.
This contradiction rules out u!=v.

Now let u=v. If u!=h/2, at most one of b,iota(b) has height u. Complementary
core arcs give an avoiding connection, again repaired by Lemma 1. Therefore
u=v=h/2. If the z lifts are not on this central core, either core arc avoids
them. So all four listed points must be central.

Removing a nonfixed involution pair from a circle on which the involution is
a reflection leaves two components, each invariant under that reflection.
If x and y are in the same component, that component contains an avoiding
arc. If they are in different components, every path inside C connecting the
source involution orbit {x,iota(x)} to the target orbit {y,iota(y)} meets Z:
all straight segments with central endpoints stay on the central core.
This proves the stated necessary condition, and exactly describes the
obstruction to constructing a bypass inside this one cylinder.

The two fixed points divide the central circle into two arcs exchanged by
iota. Each projects to the same physical corner-to-corner path in opposite
directions. Source/target lying in different components of the complement of
Z means precisely that z separates their projections on the quotient arc.
The separation statement concerns the chosen source and target occurrences
on the parameterized quotient arc; it does not assert that the physical arc
is embedded, or that no further endpoint lifts lie in C. Those further lifts
could provide an additional bypass, which only strengthens the necessary
condition for essentiality. QED.

The theorem makes no assertion that the exceptional configuration is dark in
the whole room. A different cylinder or direction can supply a bypass.

## 4. The exact rational-grid remainder

Assume the polygon and both marks have rational coordinates after independent
axis scalings. Every ordinary connection is in a rational direction, and the
square-tiled unfolding is completely periodic in that direction. The rectangle
case is already excluded by direct visibility. On the
unmarked surface, its leaf therefore either is periodic or lies in a finite
saddle connection joining zeros.

Combining the ordinary-cylinder theorem with this dichotomy, an essential
single-blocker example would have every ordinary connection in one of two
forms:

- A segment of a saddle connection joining reflex corner lifts, with no zero
  in its interior.
- A segment of the central core of an iota-invariant ordinary cylinder,
  passing between its two regular convex corner lifts as described above.

The saddle connection endpoints may be the same zero. Rational complete
periodicity is essential to this dichotomy. For real room/mark data, a
nonperiodic connection may extend forever on a nonsingular leaf, so the two
forms do not cover every limit in our degeneration program.

## 5. A prescribed six-wall room realizes the central exception

This is a prescribed analytic control, not a candidate dark room or a room
search. Take the L-shaped room with cyclic boundary

    (0,0), (3,0), (3,3/2), (5/2,3/2), (5/2,2), (0,2).

It is the 3-by-2 rectangle with the upper-right 1/2-by-1/2 corner removed.
Its unique reflex corner is (5/2,3/2); its unfolding has genus two. Set

    c0=(0,0), c1=(3,0),
    s=(3/4,1), z=(3/2,2), t=(9/4,1).

The path c0 -> z -> c1 reflects specularly at z, and s,t lie on its two
legs. It stays outside the removed corner. Its distance from the reflex
corner is at least 1/2, so its lifted continuation avoids all zeros. Continuing
through the regular convex corner lifts retraces the physical path and gives
a closed geodesic on the four-copy unfolding. It therefore has an ordinary
cylinder neighborhood. Since it contains fixed points of iota, its maximal
cylinder is iota-invariant and it is the central core.

The core is identical to the corresponding rectangle core: its developed
period is (6,8). Parameterize it by q modulo 2, with developed point (3q,4q).
The removal did not touch any physical segment of this core. Then

    iota(q)=-q mod 2,
    corner parameters: 0,1,
    z parameters: 1/2,3/2,
    source parameters: 1/4,7/4,
    target parameters: 3/4,5/4.

The two z parameters separate the source and target involution orbits on the
central core. Every core connection between these orbits meets Z.
Nevertheless, the direct horizontal physical segment s->t lies inside P and
avoids z. Thus the exceptional geometry genuinely occurs in a nonconvex simple
orthogonal room, and does not certify darkness. A proof using only this
central core cannot decide the global question.

## 6. Why copy symmetry cannot supply the missing physical path

For every g in the canonical copy group G,

    pi(g gamma(u))=pi(gamma(u)).

Applying H,V,iota to a lifted connecting segment changes its sheet label and
developed direction, but its physical projection is exactly the same path.
Reversing it also preserves the physical point set. Thus the copy symmetries
and reversal preserve an encounter with z and cannot by themselves create
a bypass. A successful argument needs a different physical connecting word,
not another label for the known one.

## What this settles and what remains

The common-cylinder removal criterion now works with ordinary cylinders,
allowing convex corner lifts, unless all marked points lie on the invariant
central core in the exact stated order. The central obstruction has a fixed
physical positive control, so it cannot be dismissed by the involution alone.
The rational critical-leaf case is narrowed to reflex saddle connections or
this central-core exception. Neither has been excluded globally or realized
as a dark decorated pair.

Next move: find an argument that forces a different physical connection from
one of these two forms, or a construction that blocks all such alternatives.
Any computation should check a prescribed theoretical construction; these
results do not justify an unrestricted room or ray search.

## Verification receipt

critical-check.py passes:64 independent ownership pairs,465 midpoint
congruence checks,306 prescribed invariant-cylinder charts (3 central
obstructions within those charts), one conjugate-target negative control,
465 retracing-time controls, and the prescribed six-wall geometry. The
central-obstruction count is a subset of the chart count, not extra cases.
The six-wall core has minimum squared reflex-corner clearance1/4 and a direct
ordinary bypass. These are exact algebra/formula controls, not an independent
proof of the global geometric statements. Run:

    python3 -B .context/illumination-k4-codex/single-boundary-blocker/critical-check.py

A separate published theorem closes all non-torus six-wall limits; see
[genus-two.md](genus-two.md). The unresolved L-shaped subclass is the torus-cover
case, so the fixed rational six-wall control is outside that exclusion.
