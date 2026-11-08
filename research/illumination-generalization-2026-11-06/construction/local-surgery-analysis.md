# Local single-vertex surgery on the known22-wall room

Candidate complete exclusion for this specified surgery family, Codex01a18403. Independent peer acceptance is required. This is not the uncapped W<=21 theorem.

## Question and fixed scope

Can deleting one vertex from the known22-wall room, then applying a Euclidean similarity, give a canonical45 room with a dark retained S/T pair? The original polygon and marks are the frozen vertex cycle in preprint-review-codex/revised.tex equation(vertices), S=(0,0),T=(2,2). A deletion replaces the two adjacent edges by the segment between the neighboring vertices and leaves every other vertex fixed. No coordinates, vertices or marks were otherwise varied.

We checked exactly those22 operations. This is an exhaustive finite family, not a census of all W<=21 rooms or all local perturbations. An arbitrary similarity of any such shape has the same illumination status for the corresponding marks.

## Geometry classification and normalization trap

All22 deleted cycles are strictly simple and keep both marks interior. Of the22 new chords, twelve have a canonical45-compatible direction (slope+/-1); ten have a direction at an angle other than an integer multiple of45degrees relative to the surviving horizontal and vertical walls. Those ten cannot be canonical45 after any common rotation and scale, because the differences between wall directions do not change.

Of the twelve geometric45 cases, seven chords lie on even-intercept diagonals of the original canonical tiling. The other five have odd intercept. They cannot be discarded: doubling all coordinates makes them canonical45 and keeps the actual marks interior A points. Rejecting them from the unit-scale tiling check would incorrectly omit genuine members of the goal's unbounded-k class.

Exactly seven primitive candidates are canonical45 at the original scale. Their deleted vertices are

    (0,-1), (1,-2), (1,1), (4,1), (3,2), (1,2), (0,1).

Each has W=21 and k=5. The six unit-leg reflex fills add one interior C point, leaving s_N=4 and J=1. The fill at(1,1) has equal legs2: its two previous smooth C points move into the interior together with the removed B corner, so J=3,s_N=2 and again k=5. No other non-A transparency changes. These rooms satisfy the independently accepted W<=21,k<=6 theorem, so the actual retained marks illuminate. All their similarity images consequently illuminate as well, even when their chosen lattice presentations have arbitrarily large k.

The other five primitive deletions remove convex corners at

    (0,-2), (1,-3), (5,1), (4,2), (0,2).

Their factor2 canonical representatives have W=21,k=57. The old k<=6 theorem does not exclude these representatives, and no inference from an invalid unit-scale lattice presentation is used.

## Positive physical certificates for all five remaining shapes

In each of the five doubled polygons, S=(0,0) and T=(4,4). `local-surgery-optics.json` contains the entire exact rational path and actual wall index for each contact. Initial directions and reflection counts are:

| Deleted primitive corner | Initial direction in doubled room | Reflections |
|---|---|---:|
| (0,-2) | (-7,-4) | 20 |
| (1,-3) | (9,-11) | 6 |
| (5,1) | (-9,-11) | 6 |
| (4,2) | (4,7) | 9 |
| (0,2) | (1,3) | 1 |

The last path is simply (0,0)->(1,3)->(4,4). Its middle point is in the relative interior of the new diagonal joining(2,4) and(0,2). Reflection there exchanges the two positive velocity components: incoming(1,3) becomes outgoing(3,1). Its two open legs stay inside the actual modified room.

The discovery search was bounded, exact and positive-only. More importantly, a separate prescribed validator recomputes every contact and complete open-leg guard from the saved paths. It verifies actual S/T endpoints; strict interior of every open leg; intersection against EVERY wall, including nontransverse overlap; no polygon corner anywhere on any leg; each intermediate contact in one actual wall's relative interior; and the specular law via rational normal projections and positive outgoing direction. All five complete paths, totaling42 reflections, pass. A bounded failure to find a path would not establish darkness; no such failure is used.

Reproduce the prescribed validation without any writes or direction search:

    python3 .context/illumination-generalization-2026-11-06/construction/local-surgery-witness-check.py

The discovery scripts retain the original A15 deadline and must not be restarted after it. The prescribed witness validator is a read-only verification of these finite certificates, not a restarted discovery effort.

## Similarity consequence

A Euclidean similarity maps each finite straight leg to a straight leg, preserves equal incidence/reflection angles and wall-relative interiors, maps genuine corners exactly to genuine corners, and maps S/T to their actual images. Thus each of the twelve geometrically admissible deletion shapes and EVERY similarity image of it illuminates its retained marked pair. In particular arbitrarily large lattice diameters and transparent-exception counts cannot rescue this specific21-wall counterexample construction.

This is a finite geometric classification with an unbounded similarity corollary. It does not make k bounded by W in general and does not reduce arbitrary rooms to these twelve shapes. General vertex motions, changes to several vertices, interior marks other than the retained pair, nonlocal modifications, and all other W<=21 rooms remain outside the conclusion.

## Review status and realignment

The geometry audit and all finite physical certificates pass this agent's exact checks. Explicit independent peer acceptance is still pending. Baseline reuse depends on the already reconciled all-support W<=21,k<=6 theorem and its accepted proof chain in baseline-and-gap.md/baseline-receipts.json. The checker source and witness data are frozen for the existing peer; none of the historical proof sources was edited.

This closes a plausible single-corner counterexample route, including the previously unexcluded k57 representatives. It neither proves universal illumination nor supplies a dark counterexample. Next progress toward the goal requires an actual new structural argument, a different proved mechanism, or a materially different counterexample family. Enlarging this already exhausted operation list or replaying more dilation sizes is unnecessary.
