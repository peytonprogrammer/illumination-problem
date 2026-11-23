# Shortest routes to regular coincidences in cov4181

**Finding.** The globally nearest non-source candidate is reachable in this control. But distinct non-source classes can share a physical first obstruction, even when *all* shortest routes and *all* starting lifts are allowed. This defeats assigning a fresh physical reflex corner solely from the class of the candidate. The universal high-valency lighting question remains open.

## The nearest candidates

Use S=(2,3), T=(4,3) in the 28-square room. Take the intrinsic flat path metric on the normalized marked ordered-pair component, allowing paths through its vertices when measuring distance. Its two room projections have the same length as the path itself. Minimize from the set of lifts of the ordered marks. A route is clean when both projections avoid room vertices before arrival at the regular coincidence. A clean minimizing route locally develops as a straight line; at a regular coincidence the local exchange reverses the line, giving a legal path from S to T.

* Class b has 14 candidates. Its minimum length is 1, to either double lift of (3,3). No route to any forbidden point can be this short: the physical distance from either mark to the nearest room corner is √2. This recovers the direct segment.
* Class d has seven candidates, and the minimum is 1+√2. For either lift over (4,2), every minimizer first projects to the ordered corner pair ((3,2),(5,2)). For either lift over (4,4) the pair is ((3,4),(5,4)). In both cases the first leg has length √2 and the last has length 1. All seven candidates have blocked minimizers. The stronger assertion that *every legal straight shot* in class d fails comes separately from the exhaustive D66 verdict.
* A general sufficient test follows from the same distance comparison. Let ρ be the least planar distance from either mark to any polygon vertex. A regular coincidence at intrinsic distance strictly less than ρ is lit via a minimizing route: an intermediate forbidden event would project to a physical corner after traveling less than its planar distance from the corresponding mark. This test needs a metric upper bound to a specific candidate. The algebraic count alone gives none.

## A physical corner shared across classes

| Candidate | Class | Exact shortest distance | Possible physical ordered pairs at first obstruction |
| --- | --- | --- | --- |
| (7,1) | b | 1+2√2+√10 | ((5,2),(7,2)) or ((5,4),(7,2)) |
| (8,2) | d | 1+√26 | ((7,2),(7,2)) |

In both rows the projection launched from T hits the **same reflex corner (7,2)** at the first obstruction, for every shortest route. The source projection also hits a corner there in time, at the positions listed. The normalized product vertices differ between the rows. Thus counting distinct product vertices as distinct physical corners would overcharge the room. This does not rule out a more selective assignment or a theorem about the nearest candidate across all classes. Nor does a blocked minimizer exclude a longer clean route to the same candidate.

## Why the distance check is exhaustive

The checker constructs square faces as ordered face pairs having the same base face and glues across matching edge colors. At each base corner it takes connected components under the two incident edge gluings, thereby keeping distinct local branches separate. Starting from the marked component yields 1,176 faces, eight starting vertices and the previously recorded 7,14,0,7 regular swap-fixed vertices by relative parity. A vertex is forbidden if either of its physical projections is a convex or reflex corner.

A metric minimizer between lattice vertices splits at every lattice hit. Between consecutive hits it is straight in the developed grid, hence has a primitive integer displacement and length √(p²+q²). Its initial square and corner determine its ordered edge crossings by exact integer comparisons; for an axial edge either incident face represents the same edge path. Conversely each graph edge so constructed is a genuine surface path. Arbitrary concatenations give admissible metric paths, including paths through singular points. Thus the shortest graph distance equals intrinsic distance within the chosen radius. A cut at radius 12 is sufficient because every candidate reported has a path shorter than 12; no shorter competing path can have an edge longer than this. Only the previously named room is used.

Multi-source Dijkstra retains the union of all tied predecessors' first forbidden vertices (or a clean flag). Positive edge lengths ensure these flags are final before a vertex is expanded. Sums of square roots are reduced to squarefree radicals and compared by refining rational enclosures, treating identical coefficient vectors as equal. A forbidden event between graph vertices is impossible because a polygon vertex develops to an integer grid point. The output includes every individual b and d candidate and the actual first forbidden lift IDs. This calculation has not received independent review.

[Checker](shortest.py) · [Exact output](shortest.txt) · [D66 per-class verdict](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md)
