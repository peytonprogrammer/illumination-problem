# R34 independent geometric and stored-closure review

ACCEPT the stated per-input verifier milestone. The mathematical finite marked-origami orbit argument is imported from the previously accepted frozen review. This does not prove a new universal algorithm implementation theorem, a W<=21 state bound, or a new dark example.

## Hand review of exact geometric certification

I read the full independent builder and orbit checker. In the canonical tiling every polygon boundary side is a union of elementary triangle sides. An open triangle cannot straddle the boundary; exact centroid membership consequently selects precisely the triangles in the input disk. Incidence-one sides must equal the complete subdivided physical boundary, incidence-two sides are interior, and the total triangle area equals polygon area. Strict simplicity and actual interior marks are checked on the four supplied inputs. Redundant collinear vertices are excluded by the stated input domain, not proved to be rejected by the certificate program for every other input.

Across a physical side with reflection A and point p, the copied triangle gA has shift g(p-Ap), since gAq+g(p-Ap)=gq for every point q on that supporting side. Neighboring developed triangle interiors lie on opposite sides. Across an interior triangulation side the frame remains g and shift zero. Pairing across each diagonal is involutive; the explicit half-plane, unit-box and four-vertex checks certify each actual square. The relative affine shifts in each square are then propagated across right and top edges, and the target boxes and side endpoints are checked in the same developed coordinates. With right/up permutations, the negative edge identifications are their inverses. This is a geometric certificate of the intended unfolding on these inputs.

The physical southwest vertex labels agree between the two half-triangles. All actual room corners remain forbidden, including regular convex lifts. Labels are constant on commutator cycles; S and T cycles are regular. Rooting at one regular source northeast sector retains a physical source lift. D4 symmetry recovers every physical path from another source lift in the chosen component; it does not identify S with a different physical point or discard any target lift reachable from that source. Comparing every source-rooted colored component is stronger than comparing an uncolored graph. Multiple orthogonal components are explicitly retained until rooting.

The peer's816 geometric side checks are its own executed result. I inspected their derivation but did not rerun that geometric builder, which would write peer-owned output files. No claim of an independently executed second816-check run is made.

## Independent stored certificate and actual-path execution

The new construction/marked-origami-builder-independent-check.py imports only the frozen historical builder for the prescribed initial known22 state. It does not import the peer orbit or physical-path checker. It reads the peer's saved gzip as certificate data, validates its frozen compressed/raw hashes, independently canonicalizes the initial state, and verifies membership.

It then independently checks ALL10,368 stored states: right/up permutations, canonical source rooting, all622,080 vertex-label guards, regular source/target cycles and no horizontal target before a forbidden actual corner. It independently derives each anchored generator composition and rooted relabeling, and checks ALL20,736 forward transitions remain within the saved set. No traversal queue, author visited set, new orbit generation or discovery direction is used. Because both generators act bijectively on the finite rooted marked state space, closure under the forward generators also covers inverse generators. By the accepted finite-orbit theorem this is a complete negative certificate for the prescribed known22 pair, rather than a capped unsuccessful search.

The checker also verifies the supplied L-room trajectory independently with exact Fraction arithmetic: four smooth specular contacts, all30 wall-leg intersection guards, and the actual source/target. Every leg avoids earlier boundary events and all contacts avoid vertices. The direction convention matches the supplied matrix. These checks passed in under one second; timing is descriptive, not a performance result.

## Scope limits

The initial triangle builder is reused from the frozen source, with its new affine certificate separately hand-reviewed. The shear theorem is an accepted dependency. This is independent stored-certificate and physical-path checking plus hand geometric review, not formal verification of every program branch or an independent implementation of the whole billiard decision algorithm. A finite cap must still return UNDECIDED. The known22 negative calibration does not address the uncapped W<=21 lower bound or decide unchecked comb prefixes.
