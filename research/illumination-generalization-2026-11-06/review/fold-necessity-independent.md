# Independent review of the beveled43-wall control

Verdict: ACCEPT the complete original hand construction ONLY WITH the frozen axis-case supplement. The original universal projection sentence was incomplete; the supplement resolves that finding for every initial direction. This is a43-wall dark example outside the narrow orthogonal whole-copy class, not a counterexample to W<=21 or to broader octilinear folding necessity.

## Sources and review method

Read the full frozen fold-necessity-beveled-candidate.md, fold-necessity-assessment.md, final review request and fold-necessity-axis-supplement.md. Independently reconstructed the listed square chain, boundary turns, removed triangle, exact seam contacts and optical proof by hand. No peer program, room reconstruction script, ray search, direction sample or numerical geometry check was run. Source hashes are retained in the receipt. This is independent AI mathematical hand review, not formal verification or human refereeing.

## Geometry and base parity

The nine cells form a staircase: two top cells, seven alternating descending steps, with a final vertical pair. Tracing their exterior gives precisely the18 listed vertices. The only maximal length2 walls are the top [-1,1]y0 and right x4,y[-5,-3]; all other axial walls have unit length. No interior integer point occurs, since the cell chain never surrounds four quadrants at a lattice vertex. The only smooth integer points are their midpoints a0,0 and b4,-4. Every other occupied integer point is a listed genuine corner.

At c2,-1 the incoming east edge turns south, a convex90degree corner of this clockwise cycle. Replacing its two unit incident edges by the southeast primitive diagonal removes exactly that corner. Its neighbors1,-1 and2,-2 were reflex270degree vertices and become225degree vertices, still genuine. The replacement lies in the attached triangle of the relevant single square and removes area1/2. It creates no crossing/contact or extra integer point. The new diagonal x+y0 is canonical; its reflection(x,y)->(-y,-x) preserves both the integer grid and the even-even residue. Integer axial wall reflections do so as well. Thus the17-wall base remains a strict parity base with exactly the two smooth marks and area17/2.

The prescribed three copies lie respectively in y<=0, in y>=0,x<=4, and in y>=0,x>=4. The first two share exactly their top segment [-1,1]y0, and the upper copies share exactly x4,y[3,5]. The bottom/right copies are disjoint even at y0: their x intervals there are[-1,1] and[7,9]. The bevels are away from these seams. Each successive gluing is along one full boundary interval with distinct endpoints, so the union remains a disk with Jordan boundary. S0,0 and T4,4 are actual interior seam midpoints with open neighborhoods supplied by the two adjacent half-planes. The inverse maps agree pointwise on each seam and send the actual marks to a,b.

All four seam endpoints join right-angle corner pairs and are smooth physical boundary points. Every other copy corner remains a genuine boundary corner, including all six225degree bevel neighbors. Hence51 corner incidences lose8 at the four smooth seam endpoints, leaving43 maximal walls. Axial and diagonal exterior edges both survive, so there is no single perpendicular direction pair for all walls.

## Optical audit and resolved finding

The base parity proof has no finite reflection/direction bound. Unfolding any ordinary candidate from a to b ends at an even-even integer image. A nonconstant straight segment cannot end at its start. For a nonzero image the gcd is at least2, and the first primitive integer point is earlier and outside even-even. The inverse reflection chart retains that residue distinction and maps it to an actual base corner. A legal ordinary base path is impossible.

The original section5 asserted a projection for every physical path. A ray can instead lie ON an interior seam and fold to a boundary glide. This was a substantive missing direction case, independently reported before acceptance. The axis supplement repairs it:

- A horizontal launch from S stays on y0 between x=-1 and1. Those two endpoints are in actual smooth VERTICAL walls; normal reflections reverse horizontal velocity and keep it trapped. T has y4.
- A vertical launch reaches(0,-1) or(0,1) first. Each is an actual270degree room corner, inherited from its staircase copy. The open segment from S is interior and has no earlier wall contact.
- Every other launch has two nonzero components. Axial and45degree diagonal reflections are signed permutations, preserving that property. Hence every axial seam crossing is transverse. A grazing encounter with an exterior wall cannot arise from an interior segment without an earlier corner; genuine corners stop paths.

For the remaining directions, an exterior smooth reflection and every transverse seam crossing project to the appropriate ordinary reflection at the same base point, except at the four smooth seam endpoints. There the physical wall reflection composed with the perpendicular seam chart change is-I, exactly projected velocity reversal. All other base-corner preimages are actual forbidden corners; in particular none of the225degree corners receives an unauthorized continuation.

Take the first projected b visit of a hypothetical actual S-to-T path and the last preceding projected a visit. Finitely many nonconstant line pieces ensure these times exist. If no exceptional reversal occurs, the subpath is an ordinary base a-to-b path and is excluded by parity. Otherwise the first reversal retraces the previously nonsingular subpath back to a. No earlier b or new exceptional encounter is possible on that reverse trace. This contradicts the selected last a. The argument uses actual endpoint images and excludes premature projected b arrival as well; it does not substitute one selected unfolded target for the actual target.

## Narrow converse consequence

For whole congruent copies of an ORTHOGONAL base, pointwise inverse-map agreement forces every seam neighbor to be its wall reflection. That reflection preserves the copy's one perpendicular direction pair. The positive-seam adjacency graph is connected because a Jordan disk's interior cannot be connected by point contacts alone. Induction therefore gives one common perpendicular frame for every copy and every exterior wall. The verified mixed axial/diagonal Q cannot belong to that precise class, even after a global rigid rotation.

This refutes only the UNRESTRICTED all-wall-count orthogonal-base converse. It does not refute a W<=21-only orthogonal converse, and it does not refute octilinear parity-fold necessity: Q visibly has its17-wall octilinear base. The separate new R21 counting results may extend the numerical construction-class exclusion, but are not prerequisites for this candidate's acceptance.

## Remaining obligations

No finding remains in this repaired packet. The main uncapped W<=21 theorem, local-to-global fold necessity and arbitrary-polygon bridge remain OPEN. No novelty or global minimum claim is accepted.
