# C2 hand lemma: a globally available geometric reduction system

Author argument for independent challenge, not yet accepted. It proves no
optical transfer. The native illumination goal remains active and unfinished.
No computation, new census or discovery search is used in this argument.

## Statement

Let D be any finite strictly simple orthogonal lattice disk with r>0, and
let S,T be any specified distinct interior even-even points. At least one
of the following geometric operations is available, preserves those ACTUAL
points and the room class, and strictly decreases r:

1. Complete every horizontal section to an interval, if some generic section
   is disconnected.
2. Complete every vertical section to an interval, if some generic section
   is disconnected.
3. Apply the isolated C1 corner completion, if both kinds of section are
   connected.

No bound on area, support, size or exception count is assumed. If correct,
this settles geometric availability for this expanded set of moves. It does
NOT settle existence-level illumination transfer for any of them.

## 1. Horizontal completion remains a strictly simple lattice disk

Use the finitely many vertex heights to split the open vertical support into
open horizontal bands. In each band the old section is a constant finite
union of disjoint positive-length intervals with integer endpoints. Replace
it by the interval from its least left endpoint to its greatest right
endpoint. Take the closure over all bands; this defines H(D).

Every two consecutive nonempty bands have hull intervals overlapping in a
POSITIVE-length interval. Indeed the interior of a polygonal disk is path
connected, so there is an interior path crossing their common height. Its
crossing has an open neighborhood in D, supplying a common open x-interval.
If a horizontal path segment occurs at that height, perturb it inside its
open neighborhood or select a nearby crossing point. Merely touching at
one x coordinate could not provide interior connectivity.

The support in y is an interval by the same connectivity argument. Joining
the band rectangles therefore gives a connected orthogonal interior with
one left and one right boundary chain, a bottom and a top. Positive band
overlap excludes pinches or separated components at a critical level. A
hole is impossible because its generic horizontal section would require
two intervals. Thus the boundary is strictly simple. All critical heights
and extreme abscissae are old integer coordinates. D is contained in H(D),
so original S,T remain strictly interior. The operation introduces no new
marks, endpoint projections or fractional tiling edges.

## 2. Reflex charge from horizontal boundary walls

Classify each original maximal horizontal wall by its two endpoint types:
C for convex-convex, M for mixed, and R for reflex-reflex. Use the same
letters for the counts. Every corner belongs to exactly one horizontal
wall, so

    c(D)=2C+M,   r(D)=2R+M,   C=R+2.

As y passes a horizontal wall, a mixed wall shifts one interval endpoint.
A convex-convex wall starts or terminates an interval. A reflex-reflex
wall splits or merges intervals at an INTERNAL gap. The last type does
not alter the outer envelope by itself. These are local sector statements,
and can be applied to every disjoint wall at the same height; no generic
perturbation of the room or endpoints is required.

Since H(D) has one interval per band, every non-base/top reflex turn of
H(D) is an inward or outward jump of one of its extreme endpoint chains.
Charge that jump to the original horizontal wall at which the old exposed
endpoint disappears or the new exposed endpoint appears. Such an event
has a CONVEX endpoint: an R-R wall only changes an internal gap.

A mixed wall supplies one convex endpoint, so receives at most one charge.
A convex-convex cap supplies at most one INTERNAL envelope charge. For a
cap to affect both extremes, its interval would have to be both the
leftmost and rightmost old interval, hence the only interval. An internal
birth or death of that entire interval with no surviving overlap would
disconnect the original interior across that height. If other intervals
survive, a cap can be extremal on at most one side. If the event is the
global bottom or global top, it instead gives the convex closing edge of
the hull, with no reflex charge. At least one original cap at each of the
global bottom and global top is therefore uncharged.

Consequently

    r(H(D)) <= M+(C-2) = M+R = r(D)-R.            (*)

Coincident heights do not identify separate walls: each chain jump can be
charged to an exposed convex endpoint of an original wall at that height,
and disjoint interval caps cannot each be simultaneously both extremes.
This is the material combinatorial step for the reviewer to challenge.

If R=0, the identity C=R+2 gives exactly two caps, the global bottom and
top. Mixed walls shift endpoints and cannot change interval count. With
no split/merge wall and no internal cap, the generic section has exactly
one interval throughout the support. Therefore H(D)!=D implies R>=1.
Together with (*) this proves strict r decrease whenever H changes D.
If H is unchanged, no reduction is claimed. The vertical result follows
by exchanging x and y, with no change to the actual marked positions.

## 3. Both-axis convexity supplies an isolated C1 rectangle

Suppose both horizontal and vertical sections are intervals and r>0.
There is no horizontal R-R wall, since such a wall creates an internal
gap in sections on one side. There is no vertical R-R wall for the same
reason. Every reflex vertex therefore has TWO CONVEX neighbors.

Choose any reflex vertex and orient/traverse its local boundary as

    A=(0,H), C=(0,0), B=(L,0), H,L>0,

with the preceding wall approaching A from x<0 and the following wall
leaving B toward y<0. This is the C1 local form (boundary traversal can
be reversed). The missing local quadrant is x>0,y>0.

For 0<y<H, the vertical edge AC is the right endpoint of the horizontal
section; horizontal convexity excludes ANY D point to its right. Thus
the open rectangle (0,L)x(0,H) is exterior. For 0<x<L, CB is the upper
endpoint of the vertical section; vertical convexity excludes ANY D point
above it. In particular the open top replacement side has no contact
with D. The horizontal sections likewise exclude contact along the open
right replacement side. A contact at (L,H) with interior on its far side
would require an interior connection to D crossing one of these forbidden
sides, or passing solely through the corner, which would violate interior
connectivity/strict simplicity. Thus it is also excluded. The only
contacts on the replacement sides are A and B, as required by C1.

Section1 of proof-01 then proves that completing this rectangle preserves
strict simplicity, lattice geometry and actual marks and removes one
reflex corner. This proves the final availability alternative.

## 4. What induction would still require

If existential optical transfer were proved for these THREE selected moves
on original rooms with r<=8, (*) and C1 would permit induction on the
nonnegative integer r, ending in the proved convex base. Each simpler room
would still have r<=8 and the literal original S,T. There would be no
size/exception or parameter cutoff in that induction.

But that transfer is UNPROVED. In particular an r-independent C1 transfer
is false by the accepted known22 corner-completion control in proof-01.
Horizontal hulls also add real mirrors and developed target images; no
pointwise selected-path lifting is being asserted. A geometric reduction
system is not an illumination theorem. The exact remaining implication
is the low-reflex EXISTENTIAL optical transfer, or a different actual
path mechanism that can replace it. Independent review of the charge,
coincident-height handling and isolation proof is required before even
the geometric availability lemma is considered accepted.
