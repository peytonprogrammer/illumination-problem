# Independent first audit of folded parity rooms

Status: accept darkness and the wall identity with explicit hypotheses; the finite computational exclusion is independently reproduced below. This remains a computer-assisted theorem for the stated normalized folding class.

Inputs are frozen under `inputs/`; no peer files changed. No new room, fold, ray, direction or word discovery was performed.

## 1. Darkness

Use a coherent fold f:Q->P: restrictions are copy isometries; they agree pointwise on every shared interface, including its endpoints. Fix the parity class A=2Z^2 in the normalized canonical tiling, and require both base marks to lie in A. Every wall reflection preserves A. If instead using a+2Z^2, require each wall reflection to preserve that specific coset; preservation of the integer lattice alone is insufficient. For example, a diagonal reflection swaps the two mixed-parity cosets. This is a definition clarification; the supplied enumerator selects A marks.

The primitive-lattice-step argument excludes ordinary connections between distinct noncorner base marks. Boundary marks cause no difficulty. Base corners have angles r*pi/4, r=1,2,3,5,6,7. If k copies meet coherently over such a corner, transparency in the simple polygon Q means k*theta=pi (smooth boundary) or 2*pi (interior). Divisibility leaves exactly:

| Base angle | Smooth boundary multiplicity | Interior multiplicity |
| --- | ---: | ---: |
| 45 degrees | 4 | 8 |
| 90 degrees | 2 | 4 |

For each of these four cases, the induced velocity change in P is -I. This is stronger and more precise than saying that even multiplicity alone implies reversal. `check.py` constructs the successive sector-reflection matrices and verifies F_out R_physical F_in^(-1)=-I in all 18 possible incoming sectors. At an interior lift R_physical=I; at a smooth lift it is the exterior-wall reflection.

Thus projected paths have ordinary reflections, possible total reversals at convex base corners, and no concave-corner continuations. First-arrival/last-source truncation and deterministic retracing exclude the connection. The projected path has finitely many events because there are finitely many physical legs and interfaces. Motion along interfaces can be treated by one incident fold chart; its projection lies on a base wall and cannot yield a valid new connection between distinct marks. Equivalently, handle such tangential pieces separately from transverse events. A valid physical path cannot run along its own boundary. The definition should preserve the existing prohibition on paths running along base walls; an interface-collinear interior trajectory requires this separate observation rather than an assumption that all paths cross every seam transversely.

For a full-wall seam, a path running along its line must leave the seam at one of its endpoints. That endpoint is a lift of a base corner. If the endpoint is a Q corner the path is invalid; if transparent, the same -I projection applies (including velocity parallel to the seam). If a mark lies within this collinear piece, both marks on that piece would have to be noncorner lattice points on the same base wall. Parity forbids two distinct such A points on one maximal base wall: between them is a non-A lattice point which would have to be a corner. Otherwise the path must encounter an endpoint, giving the same forbidden corner or retracing. This supplies the missing tangent-case justification.

## 2. Wall count, independently derived

Assume the copy decomposition is a finite disk cellulation after splitting interfaces at corner lifts. No overlaps or gaps, and the fold is coherent. Every nontrivial seam vertex is then a lift of a base corner: if it projected to the interior of a base edge, its incident sectors would all have angle pi, so two copies fill an interior neighborhood and their seam continues straight through the point. Suppress these ordinary seam subdivisions.

Write c=W_P. Let b90,b45 count transparent smooth boundary lifts and i90,i45 transparent interior lifts. Let E=sum(k-1) over lift points which remain actual Q corners. Let sigma count seam edges, and I=i90+i45 count interior seam vertices.

Corner incidence counting gives

    m*c = W_Q + E + 2*b90 + 4*b45 + 4*i90 + 8*i45.

Euler for a disk subdivided into m copy faces gives

    sigma = m - 1 + I.

Counting seam endpoints gives

    2*sigma = E + b90 + 3*b45 + 4*i90 + 8*i45.

Hence

    b90 + 3*b45 + 2*i90 + 6*i45 = 2*m - 2 - E.

Eliminating b90,i90 yields precisely

    W_Q = m*(W_P-4) + 4 + E + 2*b45 + 4*i45.

All correction terms are nonnegative. Accept the stated lower bound. Cycles and shared seam endpoints are included by Euler; no tree assumption is used.

## 3. Enumeration implementation: static review and frozen receipts

The source diff from the previously audited enum2.c is exactly a comment and one additional terminal count of smooth boundary A points. Such points appear explicitly in its atomic boundary walk, so this terminal relaxation is the right one. The previously audited pruning does not depend on marks being interior. This does not independently authenticate the new executable or prove which command produced each saved file.

All 412 saved base listings have the claimed wall counts: 8 at9, 52 at10, 128 at11, 224 at12. Independently enumerating lattice points within each *saved* bounding box confirms at least two noncorner A marks, the reported mark count, and no non-A noncorner points. This is a census of supplied fixed bases, not a discovery enumeration.

For the coherent reflected-copy class, copy adjacency has a connected dual graph. If two adjacent congruent copies reflect across an open shared segment, the reflection fixes the supporting line and matches the complete corresponding maximal wall pointwise. Therefore reflecting across whole base walls covers every needed adjacent placement. Growth from an identity copy along a spanning tree covers every finite connected assembly; the implementation also checks every later shared edge for mirror consistency. No-overlap pruning is monotone and safe. Evaluating a partial assembly before growth stops is appropriate: boundary simplicity must not be used to prune growth, and here it is only an evaluation filter.

The quarter-triangle raster is exact for the allowed lines. Polygon reconstruction rejects pinches and additional boundary cycles. The `around` check correctly requires the full integer-vertex star for an interior lifted mark. `mmax_rule` is unused, harmless for this caller because the copy cap comes directly from the wall inequality and LIM. The m=1 case is separate and covered by the earlier parity-room exclusion at W<=21.

There are 12 saved W22 positive listings. Independent D4/translation canonicalization finds **one unmarked polygon shape**. It is important not to call these 12 different rooms. This census does not independently reconstruct the copy maps of every positive listing.

## 4. What remains before accepting the computed minimum

Need frozen base-run commands, terminal receipts and source/executable provenance; exact fold-run input hash and LIM setting; and either a complete independent replay of the finite fold enumeration or an independently checked coverage certificate. `hits.txt` being empty is not itself that proof. The lower-threshold log and W22 controls are evidence but not a replacement for run provenance and completeness.

The result is therefore: the broader theorem is mathematically plausible and its principal theoretical reductions are accepted with the explicit coherent-fold/parity/tangent hypotheses above. The full computational W<=21 exclusion remains conditional on the outstanding audit. No global orthogonal or arbitrary-polygon minimum follows.

## 5. Computational gap closed: fresh source run plus independent fold exhaustion

Rebuilt the frozen `inputs/enum_base.c` with clang -O2 and executed the new binary with argument12. The completed receipt is391,531 nodes,1,930 closed boundaries and412 output bases. The output-line multiset matches the peer’s frozen base file exactly. Source, executable, raw output, compiler and exact argv are recorded in `base-provenance.json`. The terminal change remains covered by the source/pruning review above and the prior enum2 audit.

Independently implemented full-wall fold exhaustion in `replay.py`, using integer vertices scaled by2, explicit transformed triangle-vertex sets, base-wall precomposition, undirected boundary reconstruction, complete shared-edge mirror checks and interior mark incidence. It imports no peer fold code. The wall formula permits at most3 copies. Running the finite class through W22 also supplies the known positive control; m=1 below22 uses the previously independently audited parity exclusion.

Completed:2,508 states including412 identity roots;2,096 assemblies evaluated;1,648 coherent simple assemblies. No assembly with two eligible interiorized distinct base marks has W<22. There are12 qualifying W22 listings, and every one is the known polygon under D4 and translation. Full per-base receipts and positive copy-map witnesses are in `replay.json`. This is a complete verification replay of the theory-bounded class, not an optical discovery run.

Reproduce the base artifact with the recorded compile/run argv, then run `python3 -B .context/illumination-k4-codex/folded-review/replay.py`. Keep independent replay outputs in a separate copy. No global minimum or arbitrary room classification follows.

## 6. Short proof delivered and independently reviewed

`short-proof.md` now replaces the full fold-exhaustion exclusion by four geometric lemmas and only the W<=9 base classification plus the previous m=1 exclusion. The15-triangle fan budget forces14 base walls if one mark is interior. A supporting-wall necessity and Euler inclusion-exclusion exclude two-copy low-wall constructions. The only9-wall base has a non-supporting marked wall and cannot interiorize both marks for any copy count.

A separate tools-disabled Claude Opus review accepted Lemmas1–4 and the minimum reduction conditional on the earlier audited inputs (`peer-short-review.txt`, exit0). All recommended clarity changes are incorporated. Its preliminary assertion that each parity coset is preserved was too broad; diagonal reflections can exchange mixed-parity cosets. The final proof correctly only needs preservation of A.

`short-proof-check.json` checks80 prescribed local half-stars, records12 impossible local masks, verifies minimum15 required triangles among the remaining cases, and checks explicit A-preserving isometries for all8 frozen9-wall bases. The supporting-line overlap figure was visually inspected.

Added afterward, awaiting live peer review: equality at22 forces3 copies of a10-wall base, a tree of2 seams and4 distinct right-angle endpoints; and any2-copy coherent reflected double that interiorizes two smooth boundary base marks makes them directly visible along the shared seam. These are written consequences, not new discovered rooms or optical searches. The full independent replay remains a separate cross-check; global polygon minimality remains open.
