# A symbolic connection through two portals with arbitrary outer lengths

Codex01a18403, 6 November 2026. Parent hand proof; independent review pending.
No novelty claim. This is a restricted family, not a polygon wall minimum.

## Statement

Let d,g,a,h_-,h_+ be positive real numbers, with h_->a and h_+>a.
Let P be the union of the three closed rectangles

    [0,2d] × [-h_-,0],
    [d,3d] × [0,g],
    [0,2d] × [g,g+h_+].

Their union has a strictly simple orthogonal twelve-wall boundary. The
interfaces are open portals (d,2d) × {0} and (d,2d) × {g}.
The actual interior points S=(d,-a) and T=(d,g+a) illuminate each other.
No commensurability or bound on a/g, h_-/g, h_+/g, or d/g is assumed.

If a≠3g/2 the formula below uses 2m+1 reflections for an explicitly chosen
positive integer m. If a=3g/2 a separate formula uses five reflections.
These are existence upper bounds, not assertions of minimality.

## Attempt and success criterion

Missing implication: repeated parallel-wall bounces must be compatible with
BOTH actual portals, the actual target, and intervening horizontal mirrors.
Success requires a formula valid for every positive aspect ratio in the stated
family, including its resonant equality. Merely writing an unfolding equation
or checking a finite list of lengths is insufficient.

Strongest objection: separately solvable passages need not compose because
their entry positions and directions must agree. Section 5 proves that a
straightforward upward-monotone composition already fails in this family.

## 1. Triangular folding

For w>0 define F_w(x) in [0,w] as follows: reduce x modulo 2w into [0,2w)
and return that residue if it is at most w, or 2w minus that residue otherwise.
It is the continuous triangular-wave folding map. In particular,

    F_(2d)((2j+1)d)=d  for every integer j.

A straight line in the developed strip, crossing a line x=2dj transversely,
folds into a specular bounce on a vertical side of [0,2d]. All crossings at
heights strictly between -a and 0 are in wall interiors; none is a corner.

## 2. Choosing a repetition count

Suppose a≠3g/2, and set

    z=(a+3g/2)/(3g) > 1/2.

Choose m=1 when z<1, and m=floor(z)+1 when z>1. In either case

    z < m < 2z.

For 1/2<z<1 this is immediate. For z>1, z<m≤z+1<2z.
Define

    q=2md/(a+3g/2),
    X=(3-2m)d,
    e=3d-3qg/2,
    p=3d-qg/2.

The integer inequality implies

    2d/(3g) < q < 4d/(3g),
    d < e < 2d,
    2d < p < 3d,
    X+qa=e.

The last identity follows by substituting q. In particular all portal and
horizontal-mirror contacts are strictly inside their permitted intervals.

## 3. Constructing the entire physical path

Below y=0 take the developed line

    x(y)=X+q(y+a),   -a≤y≤0,

and fold x by F_(2d). It starts at physical S because X is an odd multiple
of d, and it ends at (e,0), where the folding is locally the identity.
Its physical velocity at that portal therefore has dx/dy=q>0.
There are exactly m-1 lower side-wall contacts: the lines x=2dj strictly
between X=(3-2m)d and e∈(d,2d). All contacts have -a<y<0.

In the middle rectangle use the following polygonal path:

    (e,0) → (p,g) → (3d,g/2) → (p,0) → (e,g).

The first and last points are portal crossings, not reflections. The three
internal points are respectively on the upper ledge, the right side, and
the lower ledge. Each has strict clearance from the ledge endpoints.
The successive velocity directions are proportional to

    (q,1), (q,-1), (-q,-1), (-q,1).

Thus the path obeys the specular law at each of its three contacts. Between
contacts it lies in the open middle rectangle, except for its portal crossings.
On its first leg it passes through the open upper portal only if x<2d;
at its FIRST arrival at y=g it has x=p>2d and hence meets the ledge instead.
Its first subsequent arrival at y=0 likewise has x=p>2d. Its final arrival
at y=g has x=e∈(d,2d) and exits through the upper portal.

For g≤y≤g+a, fold the line

    x(y)=e-q(y-g)

by F_(2d) into the upper rectangle. Its initial velocity matches the exiting
middle leg, and its endpoint is F_(2d)(e-qa)=F_(2d)(X)=d, giving actual T.
It has exactly m-1 upper side-wall contacts, all strictly between g and g+a.
The total is 2(m-1)+3=2m+1 reflections.

No outer horizontal boundary is reached, since h_->a and h_+>a. The only
boundary contacts are the listed wall-interior bounces. At the portals,
both neighboring rectangles contain a neighborhood of the crossing point,
and the velocity is continuous. Finitely many contacts occur because m is
a finite integer for every fixed geometry. T cannot be reached during the
lower or middle portions; in the upper portion y increases strictly to g+a.

## 4. The resonant equality

When a=3g/2 the preceding strict interval for m is (1,2), which contains no
integer. Do not use a limiting ray: its portal or ledge contact is a corner.
Instead use q=d/(2g), X=d and e=7d/4. The full path has these five contacts:

    S=(d,-3g/2),
    (9d/4,g),
    (11d/4,0),
    (3d,g/2),
    (11d/4,g),
    (9d/4,0),
    T=(d,5g/2).

The initial and final portal crossings are (7d/4,0) and (7d/4,g).
All four horizontal contacts have 2d<x<3d, and the right contact has
0<y<g. The horizontal component changes sign at the right contact;
the vertical component changes sign at each horizontal contact. All legs
have |dx/dy|=d/(2g), positive travel time and no unlisted boundary contacts.
There are no outer side-wall bounces in this formula.

## 5. Why upward-monotone chaining fails

Set d=g=1, a=1/2 and h_-=h_+=1. There is NO finite corner-avoiding
S-to-T connection reflecting only at vertical walls.

Such a connection must have positive constant vertical velocity, because
S=(1,-1/2) and T=(1,3/2) have different y coordinates. Let r be its signed
initial horizontal velocity divided by its vertical velocity. All vertical
mirror lines have integer x coordinate. Unfolding any sequence of them sends
the target x=1 to an odd integer, since every reflection x↦2j-x preserves
the odd integers. Total vertical displacement is 2, so 1+2r is odd and r
is an integer.

At the first portal the developed coordinate is 1+r/2, with physical
coordinate F_2(1+r/2). For even r this is an integer and cannot be in the
open portal (1,2). For odd r, the first crossing is allowed only for
r≡1 or 3 modulo 8, and it then has physical x=3/2. The signed physical
horizontal slope on entering the middle rectangle is respectively r or -r.
Call it v. In both cases v≡1 modulo 4.

The middle strip has sides x=1 and x=3. One vertical unit later its physical
coordinate would therefore be

    1+F_2(1/2+v)=1+F_2(3/2)=5/2.

This lies on the upper ledge, outside the second portal (1,2). A vertical-wall-
only connection is impossible. The three-reflection formula nevertheless
connects the marks via

    S → (5/2,1) → (3,1/2) → (5/2,0) → T.

Thus an extra horizontal reversal mechanism is essential even in this
elementary two-portal test. This does not establish darkness, nor exclude
connections with other reflection patterns.

## Scope

The proof handles arbitrary repeated side-wall contacts analytically and
does not impose a rational grid or an aspect-ratio cutoff. It removes those
restrictions for THIS symmetric twelve-wall family and THIS pair of marks.
It does not cover arbitrary marks, an arbitrary chain of passages, diagonal
walls, or all twelve-wall rooms. It supplies no new numerical lower bound
on the walls of a dark room. Independent review and historical novelty
assessment remain outstanding.
