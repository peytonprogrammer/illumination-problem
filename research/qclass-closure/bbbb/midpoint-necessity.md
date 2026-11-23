# What the ninth reflex corner pays for in R22

**Result.** On the sphere obtained by doubling a strictly simple orthogonal lattice room, algebraic coincidences of two distinct sheets obey an exact budget. For the marked pair in R22 the budget is 24. Six coincidences are regular and the other eighteen require nine reflex corners. This forces nine for that marked-cover configuration. For a hypothetical dark same-parity interior lattice pair in a normalized room with at most eight reflex corners and area at least 49, the budget instead guarantees at least 26 regular candidates outside the source class. Proving that a legal path reaches one of them is the open step.

## The budget

Use the project's degree-n pillowcase map f:Q→B, with n the cell area. Both Q and B are topological spheres with their flat conformal structures, so f is holomorphic between Riemann spheres. Over the four base poles the local degrees in Q are 1 at convex corners, 2 at regular points, and 3 at reflex corners. Away from the four poles f is unramified. For background on the ordered-pair construction see [D23, Lemma 1](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d23-equivariance/README.md).

Take any union of off-diagonal monodromy orbits on ordered pairs of sheets; use the normalization of the corresponding components of f(x)=f(y). If the union has nd ordered states, each of its two projections has total degree d: transitivity gives equal-size fibers of each coordinate projection over a generic sheet. Write R for the number of regular diagonal coincidence branches in this union and J for those at reflex corners. Then

    2d = R + J,       J ≤ 2r.

Indeed, the diagonal of the product of two spheres has bidegree (1,1): in homogeneous coordinates its equation is x₀y₁−x₁y₀=0. Pulling it back by the two projections gives a section of degree d+d whose zeros count intersections including multiplicity. No chosen component is the diagonal. At a ramification point of local degree e choose the same local coordinate for each factor. The non-diagonal germs are y=ζx for ζ^e=1, ζ≠1. Each meets the diagonal with multiplicity one. Thus a regular degree-two point supplies one coincidence, a reflex degree-three point supplies at most two, and a convex corner supplies none. This proof works componentwise without 2-transitivity.

For two distinct interior marks of parity a, take the union containing every pair of incident sheets at the two marked fibers (four choices at each physical mark). A real billiard connection yields a coincidence in this union: lift the path to the room double, and run inward from its ends at equal speed. On the base pillowcase the two developments agree, by the lattice midpoint congruence and the sign quotient. At the midpoint the coordinates in Q agree. At a regular base point the off-diagonal sheets cannot coincide, so this meeting is over a pole. Straight continuation through a regular midpoint there exchanges the local sheets. The coordinate in the normalized pair curve can also be continued across an earlier regular lattice crossing using its local germ. Conversely the mere membership of a coincidence in the algebraic component says nothing about a legal straight route from the two given marks.

Let R_other count the regular coincidences outside the source parity a. At most floor(n/2) degree-two points lie over a. Therefore

    R_other ≥ 2d − 2r − floor(n/2).

Two conditions enter the argument.

- **(ii-geo)** No legal path from S to T has its midpoint at a regular coincidence outside a. Darkness implies this and also rules out realized midpoints in a.
- **(ii-alg)** The marked union contains no regular coincidence outside a, so R_other = 0. The budget needs this stronger hypothesis to deduce a lower bound on r. Darkness alone supplies no such inference.

For r ≤ 8 and d ≥ 2n/3, integrality gives

    R_other ≥ 2 ceil(2n/3) − 16 − floor(n/2).

The right side is 1 at n=19, 2 at n=21 and 26 at n=49. It is positive for every n≥19 and at least 26 for every n≥49 (check six consecutive residues; increasing n by six adds five). Thus d ≥ 2n/3 together with (ii-alg) forces r ≥ 9 already at n≥19. At n=18 the two hypotheses give only r ≥ 8.

In the normalized setting with r ≤ 8, d81 gives direct visibility or d ≥ 2n/3 for n≥49. A hypothetical dark pair in that range therefore has at least 26 off-class candidates, all unrealized. The threshold for d is still open in general at areas 21 through 48. [d81 threshold](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d81-lower-threshold/README.md) · [d82 independent review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d82-review-necessity/review.md)

## Exact controls

The [checker](midpoint-orbits.py) uses the four named-room branch permutations and takes their diagonal action on ordered sheet pairs. It counts degree-two and degree-three local cycles falling in each component and verifies the intersection identity for every component. It does not generate directions, rays or reflection words. [Output](midpoint-orbits.txt)

| Room | n | Marked component degree per projection | Regular coincidences by relative class a,b,c,d | Reflex branches by class |
| --- | ---: | ---: | --- | --- |
| R22 | 15 | 12 | 6,0,0,0 | 0,6,6,6 |
| P6 | 20 | 16 | 8,0,0,0 | 0,8,8,8 |
| DB55 | 53 | 52 | 24,24,24,24 | 2,2,2,2 |
| cov4181 | 28 | 21 | 7,14,0,7 | 0,0,14,0 |
| cov4269 | 28 | 21 | 7,7,0,14 | 0,0,14,0 |

The endpoints S and T account for four of R22’s six regular coincidences, two lifts apiece. The other two are smooth-wall lifts at (2,−2) and (4,0). All six lie in the source class and all six are unrealized. Thus even a smooth-wall candidate distinct from both endpoints can be inaccessible. R22 and P6 both saturate the reflex bound. R22's conditional count is exact: (24−6)/2=9. It is a necessity statement for its coincidence profile and does not assert that deleting a corner would preserve that profile.

## A failure of straightening already below 22

In cov4181 the marked pair (2,3),(4,3) has **seven** regular coincidences over relative class d in the very same component as all sixteen starting sheet pairs. Nonetheless D66's exact per-target verdict excludes lighting at d for every physical lift pair. A straight midpoint in that other parity would yield a path in that directional class: the displacement to the lattice midpoint is an odd multiple of a primitive integer vector of parity d−a. Thus none of those seven can serve as a straight midpoint for this pair. cov4269 gives the transposed failure at b. Both pairs are lit in a different class. [D66 results](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md)

The ninth-corner argument no longer uses cov4181 as a comparison. Its marks are two lattice units apart on a horizontal line, so their incident cells guarantee direct visibility at every wall count. The seven inaccessible candidates still demonstrate failure in a prescribed midpoint class. [Local visibility proof](short-escape.md)

**Open reachability lemma.** For a nondirect same-parity interior lattice pair in a strictly simple normalized orthogonal lattice room with r ≤ 8 and d ≥ 2n/3 in the area range n ≥ 21, prove that at least one regular coincidence outside the source class is the midpoint of a legal path between the marks. Together with d81 this would settle the same-parity case for n ≥ 49. R22 illustrates nonrealization in the source class. cov4181 illustrates it in one off-class of a lit pair. Neither example is a dark pair with off-class candidates.
