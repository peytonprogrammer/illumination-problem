# Zero-charge reduction: exact meaning and a stronger normalization obstruction

[done] 2026-10-31. Established the corner-angle interpretation, the failure of scalar-gcd normalization even for the known dark room, and the exact affine symmetries available in the orthogonal case. No general darkness-preserving local contraction was proved. No new rays, directions, room search or orbit computation.

## 1. Net charge is precisely redistributed corner-angle mass

Fix a simple canonical room. For an occupied A cell a, let T_a be its m triangles. Let C_A(a) indicate that its A center is a genuine corner; let C_B(t) and C_C(t) indicate genuine corners at the B and C vertices of t. Then exactly

    net(a) = (m/4) C_A(a)
           + sum_{t in T_a} [(1/4) C_B(t) + (1/2) C_C(t)].

Proof. Every occupied B/C vertex is either an exception or a genuine corner, so the tile weight equals

    w(t) = 3/4 - (1/4) C_B(t) - (1/2) C_C(t).

For a full A star, cost=6=3m/4; for a smooth A half-star, cost=3=3m/4. For a genuine A corner, cost=m and the difference from 3m/4 is m/4. Substitution proves the formula.

Consequently an occupied cell has zero net **if and only if none of the vertices of its selected triangles is a genuine room corner**. This characterization includes its A center; saying only that its B/C vertices are transparent omits that necessary qualification.

Summing the formula over A cells counts each A or B corner of m*pi/4 angle with mass m/4, and each C corner of m*pi/2 angle with mass m/2. Thus

    sum_a net(a) = sum_{genuine corners v} angle(v)/pi = W-2.

The net identity and nonnegativity are therefore exactly a local allocation of the elementary polygon angle-sum identity. They remain correct, but are not an additional optical obstruction. Bounded positive-charge cells form bounded neighborhoods of the corners already counted by W. Their unbounded separation and the locations of the two marked points still carry metric information.

At W<=21 there are at most 76 positive-net cells, as previously derived. This is a bound on corner neighborhoods, not on the physical room or its optical complexity.

## 2. Neither marked cell must carry charge

Take the already certified 22-wall orthogonal room Q and dilate both coordinates by 2. It remains simple, canonical, dark and 22-walled. All original integer corner coordinates become even-even. The source and target stars meet no room corner, so both have net zero.

Exact geometry receipt:

| Transformation | W | N | k | Positive-net cells | Zero-net occupied cells | Marked-cell nets |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Identity | 22 | 30 | 4 | 7 | 0 | 4, 4 |
| (x,y) -> (2x,2y) | 22 | 120 | 59 | 22 | 8 | 0, 0 |

A proposed lower bound obtained by assigning fixed positive net to each dark marked star is therefore false without an additional normalization and theorem. These transformations do not create new physical darkness mechanisms.

## 3. Orthogonal billiards permit independent axis scalings

Let P have only horizontal and vertical walls. For any a,b>0 the diagonal affine map

    D(x,y) = (a x,b y)

conjugates valid billiard connections in P to valid billiard connections in D(P), in both directions.

Proof. D maps straight segments to straight segments and maps genuine corners bijectively to genuine corners. The linear reflection matrices at vertical and horizontal walls are respectively diag(-1,1) and diag(1,-1). Both commute with D. The translation part of reflection also transforms correctly because each wall coordinate is scaled by its corresponding factor. Thus the incoming/outgoing reflection law is preserved at every wall encounter. The inverse diagonal map gives the converse. Path lengths and Euclidean angles between different directions can change; axis specularity remains exact. Even the outgoing and incoming speeds match under D at each reflection, because the transformed reflection is orthogonal.

This statement concerns the physical room. The original unit-triangle diagonal subdivision need not map to canonical triangles. An integer-axis-scaled orthogonal polyomino admits a new canonical subdivision afterward; this changes the presentation but not its wall geometry or billiards.

## 4. A scalar-primitive dark family with unbounded zero-charge regions

Apply D_M(x,y)=(M x,y) to Q for odd positive integers M. Its corners remain integer points and its marks (0,0),(2M,2) remain A points. It is an orthogonal polyomino with N=30M and exactly 22 maximal walls. Darkness follows from section 3 and the certified original, with no new optical check.

Q has a vertical wall of unit length. Its images retain that unit length, while horizontal coordinate differences are multiples of M. Hence the gcd of all corner-coordinate differences is 1 for every M. No nontrivial uniform integer downscaling preserves integral corner coordinates. The growing family is already primitive under that scalar-gcd convention.

Exact deterministic controls:

| Horizontal factor M | W | N | I | k | Positive-net cells | Zero-net cells | Scalar coordinate gcd |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 22 | 30 | 2 | 4 | 7 | 0 | 1 |
| 3 | 22 | 90 | 7 | 38 | 16 | 1 | 1 |
| 5 | 22 | 150 | 12 | 72 | 16 | 11 | 1 |
| 11 | 22 | 330 | 27 | 174 | 16 | 41 | 1 |
| 21 | 22 | 630 | 52 | 344 | 16 | 91 | 1 |

This explicitly refutes a bounded-size or bounded-exception theorem for scalar-primitive dark rooms at W<=22. It does not refute the target W>=22 theorem. At W<=21, the analogous conditional observation is that any orthogonal counterexample with unit-height coordinate gcd would have scalar-primitive stretched copies of arbitrarily large complexity. A separate normalization or direct optical argument is needed there too.

Independent axis normalization does collapse this particular stretched family. It is therefore a valid exact reduction for orthogonal rooms, stronger than quotienting by similarities. It does not show that every orthogonal room normalizes to bounded complexity: independent ratios among multiple horizontal lengths and among multiple vertical lengths remain.

## 5. Why this affine freedom does not extend to mixed wall angles

Let A be an invertible linear map. To conjugate reflection R to a Euclidean reflection, the pulled-back metric G=A^T A must satisfy

    R^T G R = G.

For horizontal/vertical reflections, this requires G to be diagonal, allowing independent axis factors. If a diagonal wall reflection is also present, its matrix exchanges the two coordinates (up to signs), requiring the two diagonal entries of G equal. Thus G is a scalar multiple of identity: A is a similarity, possibly reversing orientation.

More generally, in the canonical direction set, a perpendicular pair of wall directions admits independent scalings in that rotated basis. Any two nonperpendicular available directions differ by 45 degrees and force the similarity restriction. This is a necessary-and-sufficient metric classification for global affine conjugacies of all wall reflections. Additional integrality/mark conditions still govern whether a transformed room stays in the canonical presentation class.

This separates the orthogonal construction's useful affine normalization from the broader canonical-45-degree problem. A global anisotropic rescaling must not be applied to a room containing both axis and diagonal mirror directions.

## 6. Local strip deletion does not give a path-transfer proof

A naive local reduction deletes a vertical strip of width h and joins the left/right pieces. Consider a straight segment crossing it obliquely. If it enters at (0,0) and exits at (2,1), deleting width 2 sends these contacts to (0,0) and (0,1). They do not coincide. Keeping the collapsed strip gives a vertical segment between them, with direction changes at its ends; deleting it leaves a gap. Both violate the proposed direct straight-path transfer.

More generally, the two exterior pieces retain their original direction but have a perpendicular offset h*d_y/d_x. Only horizontal crossings have zero offset. Local absence of corners in the strip does not remove this obstruction.

This breaks the naive map-based proof, not the assertion that some different connecting path might exist. No counterexample to all possible darkness-preserving reductions is claimed. Proving a replacement would require a global compatibility argument, an exact covering relation, or a finite optical state carried across the removed region.

## 7. Research decision

Do not use net charge alone to justify deleting zero-charge cells or bounding primitive size. It supplies corner localization but no new darkness constraint. Do not assign positive charge to the marked stars without proving the required normalization first.

For the orthogonal branch, the exact next reduction is to identify rooms under positive independent axis scalings. Afterward, investigate the remaining relative wall-coordinate parameters or a global folding/cover relation. For the mixed-angle branch, the available global affine freedom is only similarity, so a different argument is required.

A promising stronger invariant would record transport between the finite corner neighborhoods: not just their total angle mass, but the exact reflection/translation identifications that determine which marked lifts can connect. A finite number of corners alone does not bound those lengths or periods. No finite-state bound for this transport has yet been established.

## Validation and handoff

`zero-charge-check.py` independently reconstructs corner sectors, verifies the per-cell angle formula and its exact zero criterion on all six deterministic transformations, checks strict simplicity and all reported counts, and verifies the strip-offset control. It uses only Codex geometry helpers and the already frozen room. The reflection-conjugacy and metric classification are written proofs, not numerical optical assertions.

    python3 -B .context/illumination-k4-codex/proofs/zero-charge-check.py

Receipt: `zero-charge-check.json`, status PASS. Frozen room SHA-256: c7838dfe640932458e6853af7171396af05df71067658ee8f78f9ca3d91cab20.

[waiting on Claude] Independently verify the corner-angle formula, axis-affine conjugacy, scalar-primitive stretched family and the limits of the strip argument. Review the L5/L6 draft separately.

Next move: replace the raw net-charge size argument with a global optical transport/normal-form theorem, starting with the orthogonal affine quotient. No new ray search is justified by charge alone.
