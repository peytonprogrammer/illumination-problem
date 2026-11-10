# Adversarial review of the attached 22-wall proof

Verdict: the proof is sound under its stated finite, corner-avoiding billiard convention. I found no counterexample, false geometric assertion, or missing theorem. The seam-endpoint issue is real and essential, but the document handles it correctly. The improvements below make compressed steps explicit; they do not repair a failed argument.

Source: `.context/attachments/qkhk3S/proof-to-send.pdf`, two pages, SHA-256 `b39e4b9e7ae10ea3a0dc7985111843dcad40ab20ef46cf4ce04671811994eb0d`.

This review reconstructs the geometry directly from the attached PDF. Earlier acceptance reports were not used as evidence of correctness. `check.py` imports no existing project geometry, tracer, certificate, or proof code. Its exact integer computation passes; `check.json` records the result. Both PDF pages were rendered and visually inspected.

## 1. Geometry: no hidden contact, slit, or extra straight wall

The five base squares have a single simple boundary with 10 maximal straight walls. Their complete integer-point census is:

| Kind | Points |
|---|---|
| Convex corners | (-1,-1), (-1,0), (0,-2), (1,-3), (1,0), (2,-3), (2,-1) |
| Concave corners | (0,-1), (1,-2), (1,-1) |
| Smooth boundary points | a=(0,0), b=(2,-2) |
| Interior integer points | None |

The three copies have pairwise disjoint interiors. Their closed-set intersections are exactly

- P0 intersect P1 = [-1,1] x {0};
- P1 intersect P2 = {2} x [1,3];
- P0 intersect P2 = empty.

The union contains 15 unit squares. Canceling shared square edges gives one simple boundary of perimeter 28, with 13 convex corners and 9 concave corners. Compressing collinear edges reproduces the PDF's entire 22-vertex cycle, in order. Its only interior integer points are S and T, so both marks are strictly interior.

The six smooth boundary integer points of Q are (-1,0), (1,0), (2,1), (2,3), (2,-2), and (4,0). The first four are the seam endpoints. The last two map to b and a respectively. Thus a direct assertion that every other lattice point of Q is a corner would be false; the supplied proof correctly uses folding instead.

## 2. Parity: the argument quantifies over all connecting paths

A reflection in x=m acts by (x,y) -> (2m-x,y); one in y=n acts by (x,y) -> (x,2n-y). For integer m,n these preserve the integer lattice and each coordinate modulo 2. Their inverses and arbitrary finite compositions have the same property. The walls of unfolded copies also lie on integer coordinate lines.

Given an assumed finite connecting path, its developed endpoint B is even-even. It is nonzero because unfolding preserves length and turns the path into a straight segment of positive length L: B=a+L*u, where u is the initial unit velocity and a=0.

Write B=k(p,q), with k=gcd(|B_x|,|B_y|). Since B is nonzero even-even, k is a positive even integer, at least 2. The primitive point (p,q) is strictly inside the developed segment and at least one of p,q is odd. Fold that point using the copy occupied at its corresponding time along the assumed path. It remains an integer point with an odd coordinate. The census forces it to be a base corner.

Potential objections checked:

- **An irrational direction escapes the lattice argument.** It cannot connect: the assumed unfolded endpoint already forces a lattice direction. No rational-direction hypothesis is imposed in advance.
- **The primitive point lies outside the physical room.** It lies on the developed path, so its time-indexed folded image lies in P.
- **Overlapping developed copies make folding ambiguous.** The assumed reflection history selects the copy; injectivity of the planar unfolding is unnecessary.
- **The primitive point is precisely a reflection time.** The adjacent folding maps agree on the shared wall. Its physical image is still a corner, violating validity.
- **An unfolding word sends b to the origin.** Such an algebraic image cannot be the endpoint of a positive-length developed connecting path.

One detail worth preserving: the primitive point, not an arbitrary midpoint, is needed. The base also has the even-even corner (0,-2). Merely calling a midpoint even-even would not distinguish it from a or b.

## 3. Reversal lemma: correct, with a small ordering clarification

The intended selection should be stated in this order: truncate at the first arrival at b, and then start at the last visit to a before that arrival. The result contains neither mark in its open time interval.

If it has a corner reversal, take the first one. Everything before that event consists of ordinary reflections. Specular reflection is reversible, so negating the velocity retraces this entire prefix. It cannot reach b while retracing: b was absent from the prefix. It must return to a before any possible arrival at b, contradicting the selected last visit.

This is valid even when the original projected path revisits a, self-intersects, or has many later reversals. A geometric self-intersection is not a collision or a choice of direction. The first reversal cannot encounter a new corner while retracing a prefix that had no corner events.

The PDF's phrase “after its last visit to a and before its first arrival at b” is mildly ambiguous in isolation if a longer path visits b, then a, then b again. Step 3 already instructs first-arrival truncation before applying the lemma, so the main proof is not invalidated. An explicit order would make the lemma independently precise.

## 4. Folding: the strongest apparent counterexample is neutralized

The linear parts of the folding maps are

F0=I, F1=diag(1,-1), F2=diag(-1,-1).

They agree pointwise along their respective shared seams. Along an open seam, the physical ray is straight and changes copy. The folded velocity changes by diag(1,-1) on the horizontal seam and diag(-1,1) on the vertical seam: exactly an ordinary reflection at the corresponding base wall.

At a seam endpoint, the physical exterior-wall reflection and the copy change occur together. The exterior wall is perpendicular to the seam. For a nonaxis ray, its component across the seam is nonzero and is not changed by the exterior reflection, so the ray necessarily changes copy.

For example, at either endpoint of the horizontal seam, the exterior wall is vertical. For a P0-to-P1 event, a physical incoming velocity (u,v) becomes (-u,v) after wall reflection. Applying F1 gives (-u,-v), the negative of the folded incoming velocity. The reverse crossing gives the same result. At the vertical seam, the roles of the two coordinate directions swap.

Equivalently, for both directions across each seam,

F_out R_exterior F_in^(-1) = -I.

This is a symbolic identity for every velocity; it is not inferred from numerical ray samples.

The complete exceptional-preimage table is:

| Smooth point of Q | Base corner | Incident copies |
|---|---|---|
| (-1,0) | (-1,0) | P0, P1 |
| (1,0) | (1,0) | P0, P1 |
| (2,1) | (2,-1) | P1, P2 |
| (2,3) | (2,-3) | P1, P2 |

All four base corners are convex right angles. Enumerating all 10 corners in all three copies produces exactly 22 single incidences at actual Q corners and eight incidences at these four smooth points. Every concave base-corner preimage is an actual Q corner, hence forbidden to a valid Q path.

Thus no unexamined smooth point can fold to a concave corner, and no valid Q event induces a continuation other than ordinary reflection or total velocity reversal in P.

## 5. Finiteness and degeneracies

An axis-parallel ray cannot connect S=(0,0) to T=(2,2): orthogonal reflections preserve the zero component of velocity, so one coordinate stays fixed. Every remaining candidate has both velocity components nonzero throughout.

A physical path with N reflections has N+1 straight legs. Each leg intersects each of the two seams at most once because it is transverse to both seam lines. Consequently subdivision at seams introduces only finitely many events, at most two seam intersections per leg. Endpoint coincidences are handled by the -I rule above. The projected path is a finite generalized billiard path, so the reversal lemma applies without a hidden limiting argument.

Ordinary wall tangencies and motion along a seam would require an axis direction, already excluded. Earlier encounters with the physical points mapping to a or b are handled by first-b/last-a truncation.

## Suggested small additions before sending

1. Step 1: “The unfolded endpoint is nonzero because the developed segment has the same positive length as the path.”
2. Step 2: “Truncate at the first arrival at b, then restrict to the portion beginning at the last visit to a before that arrival.”
3. Step 3: show one velocity calculation, such as (u,v) -> (-u,v) -> (-u,-v), and say that the perpendicular seam is identical with coordinates interchanged.
4. Step 3: “Each of the finitely many straight legs crosses each seam at most once, so the projected generalized path has finitely many events.”

These are explanatory additions. The original document already contains the essential proof. Its conclusion is the stated exact dark pair under the stated corner convention;, global minimality, and tolerance to perturbing the room are separate questions and are not claimed.
