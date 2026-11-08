# Independent audit: Wolecki22 contact and simple openings

Status: ACCEPT the frozen R12 and R18 certificates and their local conclusion,
with the fixed cyclic direction pattern stated explicitly.

## Conclusion

In the labeled canonical-45 family of the supplied Wolecki22 reconstruction,
there is a neighborhood of the marked contact configuration containing no
dark strictly simple room. The pinch-kept subfamily is locally rigid modulo
translations and uniform scaling. The free-tip family is also locally rigid
modulo those same three symmetries. Those symmetries preserve the contact,
so none of the surviving symmetric copies is strictly simple.

This is a local exclusion near one specified 22-wall contact room. It does
not exclude every contact room, arbitrary changes of wall direction or
combinatorial type, or all contact limits with at most 21 walls. No explicit
neighborhood radius is computed. Darkness or provenance of the original
published figure is not re-established by this certificate audit.

## Independent checks

Codex did not execute or import Opus's tracing code. The checker uses Codex's
earlier exact dual-number and unfolding machinery, extended to initialize
from the explicit labeled cyclic vertex list. In particular, labels 7 and
10 remain distinct symbolic vertices even though both equal (2,0) at the
base configuration. They are not merged in the deformation chart.

Only the directions listed in the frozen peer metadata were replayed. Both
infinitesimal sides were evaluated, and every supplied row was matched by
corner, unfolded endpoint and signed derivative modulo closure.

| Frozen certificate | Signed rows matched | Free-tip rank | Pinch-kept rank |
| --- | ---: | ---: | ---: |
| R12 | 164 / 164 | 23 / 23 | 21 / 21 |
| R18 | 403 / 403 | 23 / 23 | 21 / 21 |

All four supplied positive dependencies were checked exactly over rational
numbers. Every coefficient is strictly positive. Each weighted row sum lies
in the corresponding closure span. All rows annihilate exactly the three
similarity directions after imposing that family's closure equations.

The full chart has 28 coordinates: two anchors, 22 primitive edge lengths,
and four mark coordinates. Ordinary closure has rank two, giving dimension
26; its event rank is 23. Keeping the tips together adds two independent
linear equations, giving dimension 24 and event rank 21. The gap map from
the closure-only chart to the two coordinates of tip separation has rank
two. Consequently the free-tip calculation has not accidentally retained
the contact equations.

## Why opening the pinch does not invalidate the events

The limiting tip wedges are 45 degrees. Label 7 has inward directions from
135 to 180 degrees; label 10 has inward directions from 45 to 90 degrees.
They are distinct local boundary sectors. The peer constructor chooses a
tip by its incident sector when it actually encounters the contact.

The accepted certificate needs no such choice. None of its rows is an event
at (2,0). Independent fixed-word geometry checks show that each path has
exactly one intermediate developed corner image, belonging to its recorded
nonregular corner. These include convex 135-degree corners as well as reflex
corners; a checker limited to reflex corners would be inappropriate here.

More strongly, boundary-check.py computes the exact squared distance from
every segment of every reconstructed developed word to both developed
pinch labels. It clamps orthogonal projection to that segment's time interval,
so this includes segment endpoints and zero-length limiting legs.

At R12, all 4,358 distance checks are positive; the minimum squared clearance
is 2/101. At R18, all 16,020 are positive; the minimum is 4/613. These are
base-path clearances, not a claimed deformation radius. Thus the moving tips
and their incident edges cannot introduce a new contact along any of these
finitely many paths in a sufficiently small deformation. The usual local
one-corner event argument applies without a contact-specific optical rule.

The checker also reconstructs each event's quadratic determinant directly
from its frozen word and recovers its full gradient by exact finite
differences: 4,592 coordinates for R12 and 11,284 for R18. The signed side
comes from independent dual-sided replay, not from trusting the peer sign.

## Local implication

For any sufficiently close admissible marked polygon with this cyclic wall
direction pattern, each strict lighting event inequality produces a valid
connecting word. All word contacts other than its recorded corner persist;
positive contact clearance handles the only nonsimple feature of the base.
A dark nearby room therefore satisfies all event survival inequalities.

Fix the first vertex and one positive edge length by translations and a
uniform scale. This gives a slice transverse to the three similarities.
In either closure family, the certified rows have zero common kernel on
that slice and a strictly positive dependence. Every nonzero slice vector
therefore has a negative event value. The minimum event value is uniformly
negative on the slice unit sphere, by compactness. The finitely many
quadratic determinant errors are O(norm(delta)^2), so sufficiently small
nonzero normalized dark deformations are impossible.

The proof uses the larger, free-tip chart before restricting to simple
polygons. It does not assume that all formal chart vectors are simple or
physically meaningful. It only applies the event implication to the vectors
that are admissible simple rooms. Every sufficiently close labeled simple
opening with the fixed cyclic directions is represented: take its first
vertex, positive primitive edge lengths and marks; closure is the only
linear equality being imposed.

Translations and uniform scaling keep the two tips coincident. Hence every
strictly simple opening is outside the surviving symmetry orbit and is lit.
The rank computation in the pinch-kept chart alone would not establish this
last conclusion; the closure-only positive dependence is essential.

## Concrete control

Shorten edge 6 by epsilon and lengthen edge 8 by the same epsilon, leaving
all other chart entries fixed. Closure is preserved. At epsilon=1/100 the
tips are (199/100,0) and (2,0), and exact segment-intersection tests verify
that the resulting 22-wall polygon is strictly simple. The run receipt
opening-control.json records 85 exact non-tangent predictions on this
opening: 39 frozen words now connect the two interior marks and 46 prescribed
words fail as predicted. This is
a check of an existing certificate, not ray discovery.

## Reproduce

```sh
python3 -B .context/illumination-k4-codex/wolecki-pinch-review/check.py
python3 -B .context/illumination-k4-codex/wolecki-pinch-review/boundary-check.py
```

Inputs are snapshots under inputs/, locked by input-manifest.json. Outputs
are check.json, replayed-events.json, boundary-check.json and
opening-control.json. No LP solver or new room/direction enumeration is
needed. Shared executable dependencies are Codex's previous event_geometry.py
and check.py in rigidity-review/, with that checker's frozen room input.
