# R34: geometric input and complete negative-closure audit

This is a verifier milestone, pending independent review. The universal W<=21 theorem remains OPEN. The finite marked-origami orbit theorem is existing accepted work, not a new result here. Its frozen review is `../../illumination-k4-codex/origami-decider-review/findings.md`.

## Domain and claim

Inputs are finite strictly simple canonical45 triangle disks with integer coordinates and distinct actual interior integer marks. Boundary vertices must be actual maximal-wall corners, with no redundant collinear marks. The executed fixtures meet this domain. Arbitrary boundary endpoints, corner endpoints and noninteger coordinates without a specified scaling are outside this certificate. No W-uniform orbit bound is claimed.

The independent builder supplies a finite geometric certificate for each input it accepts. On four prescribed fixtures it certifies all triangle pairings and all oriented square side gluings, and its complete rooted, source-colored components equal those returned by the frozen historical builder. This is per-input exact verification, not a machine-checked proof that the historical program is correct on every input.

## Why the geometric certificate suffices

The canonical grid divides each unit cell along its even-even/odd-odd diagonal. Every permitted boundary support is a grid edge. Each open elementary triangle is wholly inside or outside the polygon. Exact centroid membership therefore determines its inclusion. All selected triangles are distinct with disjoint interiors. The checker verifies their total area and that their edges of incidence one are precisely the subdivided polygon boundary; every other edge has incidence two. These conditions certify the exact triangle disk, not a visually similar polyomino.

For each triangle and each g in D4, take a copy with developed coordinates g p. Interior sides glue to the neighboring triangle in the same frame. Across a physical wall through p with linear reflection A, the adjacent frame is g A with affine shift g(p-Ap). These coordinates agree pointwise on the wall, and the triangles occupy opposite sides. This is exactly physical reflection unfolding, including nonzero translations.

Pair each developed triangle with its neighbor across its diagonal. The checker verifies opposite half-planes, exactly four union vertices and a unit axis-aligned square. Each triangle occurs in precisely one pair. It then checks BOTH oriented outgoing square sides: the adjacent square's affine-translated box differs by (1,0) or (0,1), and its edge endpoints coincide. The resulting right and up maps must each be permutations. These are local geometric identification certificates; no assumption that a combinatorial permutation automatically describes the intended room is used.

The physical projection of each square's southwest corner is computed from both triangles. It must be unique. Labels mark every actual room corner as forbidden and every actual S or T preimage with its corresponding mark. The cycle permutation u r u^-1 r^-1 must preserve labels. Source and target vertices must be regular (fixed cycles). Thus the surface retains all actual forbidden corners, including regular convex ones. No cone-only substitution or purification theorem is needed.

All physical source lifts are related by D4. A selected regular source lift has one northeast sector, so a rooted square specifies it without a hidden choice of sector. Varying all lattice directions from that lift covers every physical path after applying the copy symmetry. An orthogonal unfolding may have several connected components; a physical path starting at this lift cannot leave its component. The checker compares the set of all rooted source components, without silently equating differently colored targets.

## Complete closure certificate

Import the previously accepted finite-orbit reasoning under these endpoint conventions: lattice holonomy makes every candidate direction an integer primitive direction followed by possibly several periods; SL2Z sends that primitive direction to horizontal. The anchored shears (r,u r^-1) and (r u^-1,u) preserve the southwest vertex cycle permutation and its labels. On the finite rooted state space each shear is a bijection, so a finite set closed under both forward generators is also closed under their inverses. Horizontal checks stop at the first forbidden actual corner, and inspect every later regular vertex along the horizontal cycle until source return. Returning to the same rooted regular vertex repeats the entire future, hence no missed longer path occurs. Target labels represent the actual target fiber, not a chosen different physical point. Interior endpoints exclude wall gliding.

For the prescribed known22 polygon and actual S=(0,0), T=(2,2), the independent builder gives a 60-square source component. Own traversal produced a complete 10,368-state set. A separately read-back gzip certificate contains those states. Every state has valid permutations and vertex labels, contains no unblocked horizontal target, and both generator images belong to the saved set. All 20,736 closure checks and 10,368 horizontal checks passed. This gives a negative certificate for that known22 input only. It is a calibration of the negative verifier branch, not a new counterexample or a W21 result. A capped traversal must return UNDECIDED.

The saved binary layout is sorted triples (r,u,labels), each permutation and label list 60 bytes, with no header. Label codes are empty0/source1/target2/forbidden3. Concatenate triples, then gzip with mtime0. Raw and compressed hashes are in marked-origami-orbit-check.json. The separate readback checks closure independently of traversal order and queue state; it still shares the explicitly inspected transform formulas and must not be described as an independent implementation of the group action.

A prescribed L-room positive control yields word T,U, matrix [[1,1],[1,2]], chart direction (2,-1), physical direction (-2,1), horizontal length4. Direct exact physical tracing confirms arrival at the actual target after four smooth reflections, with all30 wall-leg guards. This tests the direction convention as well as existence.

## Coverage and limits

Four input certificates: square32triangles/128squares; diagonal16/64; L24/96; known22 30/120. Total816 oriented outgoing side certificates. Rooted source component sizes are64,64,48,60 respectively. Counts of rooted colored component types need not equal counts of connected components.

These exact fixtures and stored closure do not bound primitive degree, area, state count, reflection count or strip parameters uniformly. They can decide a specified finite prefix when exhaustion is feasible; they do not prove that its verdict is positive, nor that finitely many prefixes cover arbitrary joint strip growth. The missing universal positive step remains.

Primary geometric checks used Matheus, Three lectures on square-tiled surfaces §§1.2,2.3; Jeffreys–Matheus §2.2; and GAP Origami documentation. No claim depends on an unverified literature theorem beyond the already accepted finite-orbit foundation. All authoring, computation and setup remain in the ORIGINAL R34 effort interval; no renewed search deadline.
