# Mirror room illumination analysis

**Current result (2026-10-30): 24 walls is the attained minimum for simple canonical 45-degree rooms with distinct interior A marks and at most three transparent B/C vertices, over arbitrary finite assemblies.** All ten two-star placements are now excluded; the final 190/657 symmetry groups cover 699/2530 complete outside-cell cases. This composes with the earlier higher-star and zero/one/two-exception results. It is a computer-assisted family result, not a general-polygon bound or formal UNSAT proof. Final report: `three-triples/three-exception-complete.md`; composition: `three-triples/three-exception-complete.json`.

**Completed follow-up:** classifying the two exceptional points closes the final three placements.477 new room-and-mark configurations supply1650 independently checked exact ray cuts; combined with the preceding phase,1454 distinct configurations and3660 ray cuts support the two-exception exclusion. A smaller simple room in this tiling with interior A marks must have at least three transparent B/C points.

[done] Original grid search and two transparency follow-ups completed on 2026-10-28. No improved dark room found. The simple-room search is exhausted through two transparent B/C vertices in the fixed 64-triangle patch; its minimum remains 24 walls. Across the transparency experiments, 1,274 distinct candidate geometries have explicit connecting rays.

## Judgment

The simple canonical45-degree construction is now excluded below24 walls with zero, one, or two transparent B/C vertices, without any patch-size restriction. Within this tiling and with interior A marks, a smaller simple room needs at least three such exceptions. The earlier 20-wall slit and 22-wall contact optima remain bounded-patch results; the complete-family conclusions apply only to simple polygons.

The transparency follow-ups now rule out the entire simple canonical family through two exceptional vertices. Coordinate remainders alone lose too much information for all 939 tested candidates. A useful stronger search must retain reflection itineraries, or use a different mirror symmetry group. A path-based exclusion mechanism is now implemented and independently audited.

## Verified baselines and room definitions

| Construction | Wall count ↓ | Geometry | Exact local certificate |
| --- | ---: | --- | --- |
| Idealized reconstruction of the 20-side image | **20** | 18 outer walls plus the two faces of one slit | Pass; 22 triangles |
| Wolecki Figure 1 | 22 | Boundary branches touch at one point | Pass; 24 triangles |
| Search output with a simple boundary | 24 | One simple closed polygon; no slits, contacts, or holes | Pass; 27 triangles |

A wall is a maximal straight segment along a boundary traversal. A slit has two faces and contributes two walls. At a point contact, separate boundary sectors are counted separately. Consequently, these counts must be compared within the same room definition.

The [20-side image](https://commons.wikimedia.org/wiki/File:Unilluminable_room_with_20_sides_purple.png), uploaded by Bhavya1805 on August 30, 2024, describes work under George Tokarsky's guidance. Its central descending segment is a slit. The integer reconstruction below verifies the intended geometric pattern, rather than the imperfect pixel coordinates of the raster. It does not establish a historical priority or global record.

The [published Wolecki construction](https://arxiv.org/html/1905.09358v3#S3) uses reflected right-isosceles triangles. Parsing its [actual SVG](https://arxiv.org/html/1905.09358v3/22gon_vert.svg) gives a boundary contact at (2,0), boundary degree four there, and Euler characteristic zero for the tile complex. This figure is therefore not a simple Jordan polygon. The 24-wall search output is consistent with the previously reported 24-side benchmark; no novelty is claimed for it.

## Exact coordinates for the 20-wall room

Source S=(0,0), target T=(2,0). Traverse the outer polygon in this order:

```text
(-2,0), (-1,1), (0,1), (0,2), (1,1), (2,1),
(2,2), (3,1), (3,0), (4,0), (3,-1), (2,-1),
(2,-2), (1,-1), (0,-1), (0,-2), (-1,-1), (-1,0)
```

Add the mirror slit from (1,1) to (1,0). Both faces reflect. All wall corners, including the slit tip, terminate a ray. Removing this slit makes (1,0) an ordinary interior point and invalidates the certificate. Indeed, the horizontal segment from S to T would then illuminate T directly.

The full triangle list and slit are in `illumination-20.json`; `illumination-20-certified.png` shows the reconstruction. The source image is saved as `illumination-20.png`.

## Why the certificate proves darkness

The grid has three vertex labels: A for even-even coordinates, B for odd-odd coordinates, and C for mixed parity. Each unit square is split along its A-to-B diagonal. Every resulting tile is a 45–45–90 triangle, with its right angle at C.

The checker verifies disjoint canonical tiles, exact reflections across shared open edges, connected room interior, two distinct interior A points, and an absorbing corner in every occupied boundary sector at B and C. A B/C point cannot be interior or a smooth point on a straight wall. A slit tip with a full 360-degree sector remains an absorbing corner.

Here is a direct parity proof for this particular grid, independent of numerical ray sampling:

1. Unfold a hypothetical finite billiard path by reflecting whole room copies at each bounce. The path becomes a nonconstant straight segment.
2. Every room wall lies on a horizontal or vertical integer line, or on a diagonal x+y=2k or x−y=2k. Reflections in these lines preserve the integer lattice, the A lattice, and the other two parity classes as a union.
3. Thus the unfolded segment connects distinct even-even lattice points. Write its displacement as (2a,2b). If g=gcd(|2a|,|2b|), the first intermediate lattice point is S+(2a/g,2b/g). Since g≥2 and this step is primitive, at least one step coordinate is odd. This point is a B/C point and lies strictly between the endpoints.
4. At that time the hypothetical path lies in some unfolded room copy, possibly at a bounce between copies. Its B/C lattice point is an absorbing room corner by the certificate. The path must terminate there, contradicting arrival at T.

This proves darkness for every finite legal reflection sequence under the stated corner convention. It uses no finite-ray miss criterion. Wolecki's triangle-folding argument supplies a broader framework, but the integer-grid argument above is enough for these checked examples.

## Search scope and results

The final searches use every one of the 288 unit triangles in the closed coordinate box [-4,8]×[-4,8]. The source is fixed at (0,0); the target may be any other fully interior A grid vertex. Tile choices are arbitrary subsets, with no imposed symmetry and no tile-count restriction beyond the patch itself.

| Room class | Final solver result | Supporting file |
| --- | --- | --- |
| Slits, contacts, and holes allowed | At most 19 walls: INFEASIBLE | `illumination-search-under20-unrestricted-result.json` |
| No slits; contacts and holes allowed | At most 21 walls: INFEASIBLE | `illumination-search-under22-unrestricted-result.json` |
| Simple polygon | Minimum 24 walls: OPTIMAL, bound 24 | `illumination-search-simple-unrestricted-result.json` |

The first run permits 500 atomic slit edges; the patch contains only 408 shared edges, so this does not constrain slit placement. All three runs finished before their 55-second limits. The first two combine with the checked 20- and 22-wall examples, which lie within the patch, to give patch optima of 20 and 22 respectively.

The model chooses tiles and which shared edges are open. Local tables enforce absorbing B/C corners and count boundary turns. A parent forest with strictly increasing integer ranks enforces connected interior through open edges. Simple polygons additionally require one occupied boundary sector per vertex, no slits, and Euler characteristic one, excluding holes and contacts.

The exact scope excludes larger or differently positioned assemblies outside this box, other triangle angles, non-grid walls, and valid dark rooms that fail the sufficient B/C-corner certificate. Infeasibility is the integer solver's result, not an independently checked formal unsatisfiability proof.

## Validation and reproduction

The solver uses angular slots around vertices; the certificate checker independently traverses fans of adjacent tiles and sums their exact 45- or 90-degree angles. Exhaustive comparison agrees on all 4,461 local tile/open-edge configurations for representative A, B, and C vertices. All seven saved room certificates pass. Four deliberately invalid changes are rejected: removing the slit, moving the target to the boundary, duplicating a tile, and calling the slit room simple.

Dependencies are pinned in `illumination-requirements.txt`. The geometry checker itself uses only the Python standard library; Pillow is needed for drawings and OR-Tools for search.

```sh
uv venv .context/illumination-venv
uv pip install --python .context/illumination-venv/bin/python -r .context/illumination-requirements.txt
.context/illumination-venv/bin/python .context/illumination-baselines.py
.context/illumination-venv/bin/python .context/audit_illumination.py
.context/illumination-venv/bin/python .context/search_illumination.py --bounds -4 8 -4 8 --any-target --seconds 55 --slits 500 --max-tiles 288 --max-walls 19 --out illumination-search-under20-unrestricted
.context/illumination-venv/bin/python .context/search_illumination.py --bounds -4 8 -4 8 --any-target --seconds 55 --slits 0 --max-tiles 288 --max-walls 21 --out illumination-search-under22-unrestricted
.context/illumination-venv/bin/python .context/search_illumination.py --bounds -4 8 -4 8 --any-target --seconds 55 --slits 0 --simple --max-tiles 288 --out illumination-search-simple-unrestricted
```

## Transparent secondary vertex experiments

The original certificate requires every B/C vertex to absorb a ray. The relaxed search permits one or two such vertices to become interior points or smooth points on a straight wall. Each admitted exception is counted once, even if it has multiple occupied sectors. Source and target remain distinct interior A points.

The first transparency follow-up used five screening runs to generate 1,090 room records, representing **939 distinct geometries** after deduplication. Every distinct geometry has an exact rational connecting path, independently verified using segment intersections, triangle coverage, corner avoidance, and the reflection law. The candidates comprise 229 rooms with two exceptions and 710 with one. Wall counts range from 16–19 in the slit family and 22–23 in the simple family. The longest saved witness uses 22 reflections.

Two apparent successes demonstrate why direction sampling cannot establish darkness. An 18-wall room passed every primitive integer direction with coordinate magnitudes at most eight, but direction (-4,-11) reaches its target after 13 reflections. A 22-wall simple room similarly fails in direction (-2,-9), after nine reflections. Both witnesses pass the independent validator. The first is drawn in `transparent-path-example.png`; its room and complete path are saved in `transparent-path-example.json`.

### A bounded result with one exception

For simple rooms in [-2,6]×[-2,2], built from any subset of the patch's 64 triangles, fix S=(0,0) and T=(4,0). There is no dark room with at most 23 walls and exactly one transparent B/C vertex in the tested model. The original strict-certificate search already excludes zero exceptions within these bounds.

The solver exhausted this relaxed case after 165 ray-based cuts. Each cut records local geometric facts sufficient to preserve an independently verified connecting path: traversed tiles remain present, crossed edges remain open, reflecting walls remain closed, and visited lattice vertices retain their incident geometry. Any room satisfying those facts has the same connecting ray, so the solver can exclude the whole class. The final status is INFEASIBLE. This is a bounded computer-assisted exclusion, not a global lower bound or a formally checked unsatisfiability proof.

The slit experiments use [-2,4]×[-2,2], its 48 triangles, S=(0,0), T=(2,0), at most 19 walls, and one or two transparent vertices. They reached time limits before exhausting the geometry space. All sampled candidates were illuminated; this does not exclude unexamined candidates.

### Extension to two transparent vertices

For the same 64-triangle patch [-2,6]×[-2,2], S=(0,0), and T=(4,0), **24 walls remain optimal within the tested simple-room model when up to two B/C vertices may be transparent**. The search with one or two exceptions and at most 23 walls is exhausted; a separate zero-exception control is also infeasible. The known 24-wall room lies entirely in this patch and passes its exact darkness certificate.

The completed exclusion uses 500 recorded room/path pairs: the previous 165 one-exception cases and 335 new two-exception cases. The sampled geometries have 21–23 walls. Reflecting a room across y=0 or x=2 preserves the patch; the second reflection exchanges S and T, so reversing the ray restores the original source-target order. All four symmetry-derived paths are independently verified before their cuts are added. The final model contains 2,000 path cuts and returns INFEASIBLE. Rebuilding a fresh model from the 500 saved records reproduces INFEASIBLE without needing another candidate.

The independent audit rebuilds every cut, validates all 2,000 exact paths, and checks 2,932 unrelated tile mutations preserving the path facts. The recorded rays use at most 31 reflections and primitive direction coordinates of magnitude at most 17. The search's direction bound of 32 supplies witnesses; it is not used as a negative illumination test. Every excluded class has a validated connecting path, and no unexamined class remains in the final model.

The 500 records represent 500 distinct geometries. Their 165 one-exception cases overlap the first follow-up, so the combined number of distinct tested candidate rooms is 1,274. All 500 also have the same full affine reflection group identified in the earlier arithmetic analysis.

Artifacts: `transparent-simple-two-symmetric-screen.json` contains all saved room/path pairs; `transparent-simple-two-symmetric-result.json` records exhaustion. `transparent-two-final-audit.json` records the independent checks, controls, and exact scope. The scripts can resume from validated records, so the initial run's atomic checkpoint was reused after adding symmetry-derived cuts.

Replay the completed exclusion in a fresh model, then rerun the independent audit:

```sh
.context/illumination-venv/bin/python .context/search_illumination.py --bounds -2 6 -2 2 --target 4 0 --seconds 300 --slits 0 --simple --max-tiles 64 --transparent-budget 2 --require-transparent --max-walls 23 --screen-candidates 1 --direction-bound 32 --path-cuts --symmetry-cuts --seed-screen .context/transparent-simple-two-symmetric-screen.json --out transparent-two-replay
.context/illumination-venv/bin/python .context/audit_illumination_two.py
```

This remains a bounded computer-assisted result, relying on the integer model and path-cut implementation. It does not cover other source-target arrangements, larger patches, three or more transparent vertices, slits, or other triangle geometries. It is not a global 24-wall lower bound.

### Why refining parity alone fails here

A valid sufficient test was implemented that tracks finite reflection orbits modulo 4, 8, or 16. It collects the coordinate remainders of all nonabsorbing lattice points in all reflected copies. For every primitive direction remainder, it checks whether a sequence of lattice steps could reach an image of T without first leaving that nonabsorbing set. If none can, the room is certified dark. A surviving sequence is only an arithmetic possibility, not a billiard trajectory.

The test certifies the original rooms and fails on the relaxed example. The reason extends beyond these three moduli. Exact affine-group calculations show that all 939 candidates in the first follow-up generate the full group of square symmetries and translations by (2i,2j). The calculation uses representatives of the eight linear symmetries and an integer translation lattice of index four; it does not infer the infinite group from a finite modulus.

Under this group, T's orbit contains every even-even point. One transparent B point fills the odd-odd orbit; one transparent C point fills the mixed-parity orbit. Thus the arithmetic test always permits a two-step sequence 0 → v → 2v: choose v=(1,1) for B, or an axis unit vector for C. The endpoint 2v lies in T's orbit. The test cannot tell that the necessary reflected copies may require incompatible wall sequences.

Consequently, this specific reflection-orbit test cannot certify the tested candidates after any refinement of coordinate remainders. This does not rule out every arithmetic argument, other mirror groups, or an itinerary-sensitive certificate.

### Validation and reproduction of the follow-up

`transparent-final-audit.json` records 939 independently validated paths and their deduplicated counts. Twenty local path-cut patterns were additionally checked under 836 unrelated tile or edge mutations that preserve the recorded facts; every connecting path remains valid. The original strict certificate audit still passes, and a regression search still recovers the 20-wall optimum in the original small patch.

```sh
.context/illumination-venv/bin/python .context/illumination_paths.py .context/transparent-one-exhaust-survivor.json 32
.context/illumination-venv/bin/python .context/illumination_residues.py .context/illumination-20.json 8
.context/illumination-venv/bin/python .context/illumination_group.py .context/illumination-20.json
.context/illumination-venv/bin/python .context/search_illumination.py --bounds -2 6 -2 2 --target 4 0 --seconds 55 --slits 0 --simple --max-tiles 64 --transparent-budget 1 --require-transparent --max-walls 23 --screen-candidates 1000 --direction-bound 32 --path-cuts --out transparent-simple-pathcuts
.context/illumination-venv/bin/python .context/audit_transparent_illumination.py
```

The direction bound is a falsification resource, not an assumption behind the exhausted simple-room result: every excluded class has a saved exact witness, and the remaining model is infeasible. The exclusion still depends on the model and correctness of its path cuts. The cuts require a fixed target; the script rejects their use with an automatically chosen target.

## Where a further improvement could come from

One testable conjecture is that 20, 22, and 24 are global minima for these three room classes within this exact certificate family. The finite searches do not prove that conjecture. A next theoretical step would seek a local counting inequality whose sum bounds walls using the number of interior A vertices, eliminating dependence on patch size.

For a construction beating those counts, change the proof family. Wolecki's generalized no-return lemma allows triangle angles π/n, mπ/n, and (n−m−1)π/n with even n. The 30–60–90 pilot is now completed below; its 30-degree source needs twelve incident tiles, compared with eight here, and the tested patches did not improve the wall counts. More promising but harder is a blocking argument permitting some B/C images to be transparent: the current certificate forbids these automatically and may exclude better rooms.

For the broader question, Wolecki's theorem gives finitely many nonilluminating pairs in each rational polygon with connected interior. A room defeating every possible source would therefore have to leave that rational class. Approximating a curved dark room with rational polygon walls cannot preserve an open dark region.

The next two experiments test different source-target arrangements and the 30–60–90 geometry. Their outcomes follow.


## Placement sweep and 30–60–90 pilot

[done] The authorized follow-up found no smaller dark room. It tested three additional non-axis placements and built an exact model for a second triangle family. All counts below use maximal straight boundary segments and count slit faces separately.

### Source-target placement sweep

The source is (0,0), targets and patches are listed below, and at most two B/C vertices may be transparent. Every sampled candidate has an independently checked exact connecting path. The square-grid symmetry implementation now selects only square-lattice isometries preserving both the rectangular patch and the unordered marked pair, reversing paths when the marks exchange.

| Target | Patch; tiles | Class and wall limit | Recorded rooms | Result |
| --- | --- | --- | ---: | --- |
| (2,2) | [-2,4]×[-2,4]; 72 | Simple; ≤23 walls | 263 | Exhausted: INFEASIBLE after 1,052 ray cuts |
| (4,2) | [-2,6]×[-2,4]; 96 | Simple; ≤23 walls | 163 | Time cap; 326 ray cuts, not exhausted |
| (4,4) | [-2,6]×[-2,6]; 128 | Simple; ≤23 walls | 42 | Exhausted: INFEASIBLE after 168 ray cuts |
| (2,2) | [-2,4]×[-2,4]; 72 | Up to two atomic slit edges; ≤19 walls | 35 | Time cap; 140 ray cuts, not exhausted |

The resumed runs reuse 249, 98, 39, and 18 previously saved records respectively. The table counts each saved geometry only once per final run. Across these four final datasets there are 503 distinct room-and-mark configurations, all illuminated. Two complete exclusions rule out improvements below 24 in their stated models; they do not establish a matching 24-wall construction for those marks. The remaining two models have unexamined geometries. A solver status of OPTIMAL for the last examined candidate does not override `exhausted:false` or `stop_reason:time_limit`.

For the no-slit class only, the nearest axis placement T=(2,0) does not need a solver search: the two required full A stars force the direct horizontal connecting segment. Its zero-reflection witness is checked independently in `placement-adjacent-axis.json`. A slit can end at the intervening lattice point without touching either mark; the existing 20-wall example does exactly this. Thus this exclusion must not be applied to slit rooms.

`placement-final-audit.json` records independent geometry/path checks, reconstructed cuts, and mutations outside cut facts. The earlier horizontal-pair audit was rerun after generalizing symmetries: its 2,000 paths and 2,932 mutation checks still pass. Raw room/path records, result summaries, and logs use the `placement-*` prefix.

### An exact 30–60–90 tiling

The model subdivides each equilateral triangle into six triangles using its centroid and edge midpoints. A is an original equilateral vertex (30° in each tile), B a centroid (60°), and C a midpoint (90°). Twelve tiles surround an interior A. Coordinates `(x,y)` mean physical coordinates `(x,√3 y)`, so all coordinates and reflection calculations remain rational when using the metric `dx²+3dy²`.

The same folding argument applies: all occupied B/C sectors must be actual absorbing corners, while source and target are distinct full A stars. A connecting path would fold to a nontrivial return from A to A in the triangle, excluded by [Wolecki, Lemma 3.1](https://arxiv.org/html/1905.09358v3). This certificate uses the paper's n=6, m=2 case; it is not a ray-sampling conclusion.

Define lattice vertices P(i,j)=(12i+6j,6j). A radius-r patch contains the two equilateral triangles in each lattice parallelogram for -r≤i,j<r, each subdivided into six tiles. The source is P(0,0); the target may be any other full A star. There is no tile-count cap below the patch size.

| Patch | Room class | Result |
| --- | --- | --- |
| Radius 2; 192 tiles | ≤1 atomic slit edge; contacts and holes allowed | Optimum 30 walls; certified example has 34 tiles, one slit, one contact |
| Radius 3; 432 tiles | Same class, ≤19 walls | INFEASIBLE |
| Radius 3; 432 tiles | No slits; contacts/holes allowed, ≤21 walls | INFEASIBLE |
| Radius 2 and radius 3 | Simple polygon; no wall limit | INFEASIBLE in both patches |

All listed runs terminate with a conclusive solver status. In particular, the simple-polygon result excludes every wall count within each patch and strict certificate, not merely counts under 24. It is not a theorem about all 30–60–90 assemblies or all rational polygons. The one-slit constraint does not cover longer or multiple slits.

`illumination_306090.py` implements the model, exact checker, and renderer. `audit_illumination_306090.py` compares fan connectivity with an independent twelve-direction angular-slot algorithm on all 16,576 representative local configurations with zero or one closed edge. All 272 shared-edge reflections in the 192-tile patch are checked exactly, including vertex labels; the saved 30-wall room passes the independent angle/wall audit. Results: `306090-audit.json`; diagram: `306090-slit.png`.

```sh
.context/illumination-venv/bin/python .context/illumination_306090.py --radius 2 --slits 1 --seconds 120 --out 306090-slit
.context/illumination-venv/bin/python .context/illumination_306090.py --radius 3 --slits 1 --max-walls 19 --seconds 120 --out 306090-large-under20
.context/illumination-venv/bin/python .context/illumination_306090.py --radius 3 --slits 0 --max-walls 21 --seconds 60 --out 306090-large-noslit-under22
.context/illumination-venv/bin/python .context/illumination_306090.py --radius 3 --slits 0 --simple --seconds 120 --out 306090-large-simple
.context/illumination-venv/bin/python .context/audit_illumination_306090.py
```

### The next useful change: retain the reflected copy

The placement and angle pilots reinforce the limitation of the current sufficient certificate. A more useful next investment is an exact illumination decision procedure for square-grid rooms with transparent B/C vertices, retaining the identity of the reflected copy rather than just its coordinates.

Proposed approach, not implemented or verified here:

1. Construct the room's actual unfolded translation surface from its oriented triangles and glue them into unit squares. Preserve every lift of S and T and every absorbing corner, including removable surface vertices that remain absorbing under the billiard convention.
2. Encode neighboring squares by permutations. Enumerate the finite SL₂(Z) orbit while carrying these vertex labels and their incident sectors. [Tan's square-tiled-surface methods](https://arxiv.org/abs/1207.3493) supply a relevant orbit-enumeration framework; the billiard blocker decoration is an additional requirement, not a result claimed from that paper.
3. Reduce a primitive integer direction to horizontal using an integer area-preserving matrix. In every resulting decorated surface, follow every source sector horizontally until it reaches any target lift, an absorbing vertex, or a repeated state. The method must establish that the enumeration represents all directions and all target lifts before a negative result is called a darkness certificate.
4. Validate against known dark 20/24-wall controls and the false 18-wall survivor with its independently checked 13-reflection path. Only then use it to search more permissive candidates or design an unfolded structure before seeking a planar room.

This addresses the specific information loss proved in the earlier arithmetic analysis: the same coordinate may lie in incompatible reflected copies. A finite orbit could still be too large to enumerate; building the square decomposition, carrying blocker labels correctly, and proving coverage are unresolved engineering/mathematical tasks. No new all-direction certificate is claimed.

The prototype below implements and tests this idea. No improved dark room or global wall-count lower bound has been established.


## Reflected-copy certificate prototype

[done] Implemented an exact unfolded-sheet model, a finite sufficient darkness certificate, and a bounded exact direction-code search. It proves the three known dark controls dark and supplies independently verified paths for both earlier false survivors. It has not produced a smaller room or proved a new transparent dark example.

### Unfolding and blocker labels

`illumination_cover.py` constructs eight oriented copies of every canonical 45–45–90 tile. Open edges join the adjacent physical triangle in the same orientation; a mirror edge joins the same triangle in the reflected orientation. Pairing the triangles across their hypotenuses gives 4N unit squares for N physical triangles. Two permutations H and V record crossing a square's right and top edge. Every square corner keeps its physical location and source/target/blocker decoration. Edge identifications are checked in both decorations and physical locations; every nonabsorbing vertex must be regular in the cover.

The implementation treats absorption by **occupied boundary sector**. A π-angle sector is smooth even when a different sector at the same physical coordinate is a corner. A slit tip with a 2π occupied sector remains absorbing. This is the more permissive convention at a boundary point contact, so it cannot manufacture a dark room by adding absorbers. All three original dark controls work under this convention, and all previous explicit illumination paths remain valid.

The audit caught this distinction on two local mutations of the 20-wall room: treating every occurrence of a corner coordinate as absorbing appeared to certify them. With the smooth sector allowed to reflect, both have an exact direction (5,3) connecting the marks after eight reflections. They are saved as `cover-mixed-sector-1.json` and `cover-mixed-sector-2.json`. The obsolete proofs are explicitly marked REJECTED in `cover-rejected-global-corner-*-certificate.json`; they are regression fixtures, not dark examples.

`illumination_sector_paths.py` constructs the actual physical witness by exact tile crossings and sector-aware reflections. Its separate segment/wall validator checks containment, absence of forbidden boundary crossings, approach to the correct boundary sector, and the reflection law. For the two original false survivors, it reproduces directions (-4,-11) with 13 reflections and (-2,-9) with nine reflections.

### A finite sufficient certificate for all directions

Any connecting ray in these rooms unfolds to a straight segment between integer lattice points. Its direction is therefore proportional to a primitive integer vector. The eight orientation copies cover every physical sign and coordinate order, so it suffices to handle positive primitive directions plus the two axes.

For a positive primitive vector (p,q), record the internal vertical/horizontal grid crossings as a word in H and V. There is no internal lattice vertex. Crossings at times t and 1−t have the same edge type in reverse order, so the word is a palindrome. After its last square, crossing V and then H identifies the endpoint's northeast corner with a southwest corner at the same surface vertex. At a nonabsorbing regular vertex this is the next departure sector.

`illumination_cover_certificate.py` computes the least endpoint relation R containing the identity and the actions H and V, and closed under wrapping a word with H on both ends or V on both ends. In pair form, (a,b) in R implies (H⁻¹(a),H(b)) and (V⁻¹(a),V(b)) are in R. There are at most n² pairs, so this computation terminates.

The relation contains every palindrome, including words that are not primitive lattice cutting words. A graph then allows any such word at each nonabsorbing vertex, potentially changing words between steps. This only enlarges actual visibility. If no target sector is reachable from any source sector, and both exact axis checks also fail, the room is dark in every direction. A graph path is only a possibility and returns INCONCLUSIVE. It never proves illumination.

The serialized finite certificate contains H, V, vertex colors, the relation rows, and a closed reachable set excluding targets. `verify_certificate` in `audit_illumination_cover.py` independently checks its base pairs, wrapping closure, reachable-set closure, and both axes. Six deliberately corrupted certificates are rejected. This is an independently replayable mathematical/computational certificate, not a proof formalized in a proof assistant.

### Exact direction codes, with an honest resource limit

The second branch preserves a single direction code through every lattice step. It uses the crossing-code/Farey framework in [Tan, Codes for Square-Tiled Surfaces, Sections 3–4](https://arxiv.org/html/1207.3493v1). Write composition in traversal order. If W is the internal crossing code, its left code is C=W V H. Codes of neighboring primitive directions compose under Farey addition: C(u+v)=C(u)C(v). The formal seeds are C(1,0)=H and C(0,1)=H⁻¹ V H; the actual axes are checked separately as H and V.

The code traverses the Stern–Brocot tree of positive primitive directions and deduplicates entire pairs of neighbor permutations. Equal pairs have identical descendant codes and visibility behavior on the fixed decorated cover. Finite closure would cover every direction. A positive result is converted to an exact physical ray and independently verified. A state/time cap returns UNKNOWN, never DARK.

On the 20-wall dark control this branch reached its 20,000 processed-pair limit, with 40,001 discovered pairs and 20,000 distinct direction codes, without closing. The sufficient certificate handles that control, but full exact enumeration is not yet practical as a general negative test. Simple color-preserving automaton minimization gave no reduction for any of the five main controls: their 88,96,108,84,104 square states all remain distinguishable by arbitrary crossing words.

### Validation and what improved

| Control | Finite sufficient certificate | Exact positive branch |
| --- | --- | --- |
| Known 20-wall slit room; 88 cover squares | DARK | Full-code negative diagnostic capped; not needed for the proof |
| Known 22-wall contact room; 96 squares | DARK | Not needed |
| Known 24-wall simple room; 108 squares | DARK | Not needed |
| Earlier 18-wall false survivor; 84 squares | INCONCLUSIVE | Illuminated, direction (-4,-11), 13 reflections |
| Earlier 22-wall false survivor; 104 squares | INCONCLUSIVE | Illuminated, direction (-2,-9), 9 reflections |
| Two mixed-sector contact mutations | INCONCLUSIVE | Both illuminated, direction (5,3), eight reflections |

The independent audit compares all 63 primitive positive directions with coordinates ≤10, plus axes, in every source sector for each of these seven controls: 3,640 cover-versus-physical-ray comparisons. It also checks Farey-generated codes against direct chronological grid-crossing codes, verifies every encountered positive physical path, checks a small noncommuting permutation relation independently by inward palindrome peeling, and rejects six corrupt certificates. The two mixed-sector controls each exhibit six positive-direction differences from the old globally absorbing-coordinate tracer, confirming that the regression is exercised. Two additional controls—a rectangle and the 20-wall room with its slit removed—correctly yield direct, zero-reflection illumination.

A complete local mutation pilot examines every one/two tile flip among each baseline and its immediate edge neighbors: 2,244 attempted mutations, 611 valid configurations with nominal transparent B/C vertices. None receives a new darkness certificate. More decisively, on every one of these 611 configurations, the entire palindromic endpoint relation is exactly the parity-permitted relation: all square pairs except those differing in both coordinate parities. Thus merely keeping sheet identities in this conservative relation does not improve its discriminatory power for the tested rooms. Noncertification is not a proof that those 611 rooms are illuminated.

The reusable result is a checked unfolding/compiler and a three-outcome tool, `illumination_decide.py`: DARK with a finite sufficient certificate, ILLUMINATED with a checked physical witness, or UNKNOWN after a cap. `cover-run-summary.json` collects the audit, mutation results, minimization probe, and capped diagnostic. No improvement in wall count is claimed.

```sh
.context/illumination-venv/bin/python .context/illumination_decide.py .context/illumination-20.json --out .context/cover-dark20-combined.json
.context/illumination-venv/bin/python .context/illumination_decide.py .context/transparent-one-exhaust-survivor.json --out .context/cover-light18-combined.json
.context/illumination-venv/bin/python .context/audit_illumination_cover.py
.context/illumination-venv/bin/python .context/probe_illumination_cover.py
```

The follow-up below tests a state reduction that preserves one coherent direction code and all its future compositions.


## Coherent direction-code state reduction

[done] Implemented and validated an exact state quotient that retains the full action of both neighboring direction codes. It provides almost no reduction on the dark controls and does not remove the enumeration bottleneck.

Two neighbor pairs (U,V) and (U′,V′) can be merged when a single relabeling of reflected sheets simultaneously conjugates both permutations and preserves every source, target, ordinary, and blocker label. Conjugacy respects products and powers. Thus it preserves the mediant code UV, both child pairs (U,UV) and (UV,V), and every descendant's visibility under repeated use of a single direction code. This avoids the earlier relaxation that could change direction words between lattice steps.

`illumination_code_quotient.py` computes an exact canonical form for the colored pair graph. It handles each orbit component separately, tries every root of its rarest vertex color, uses deterministic U-then-V traversal to label that component, and selects the lexicographically least encoding. Sorted component encodings handle disconnected covers. Equality of encodings gives an explicit colored graph isomorphism; no probabilistic hash or approximate graph match is used for merging. The solver retains actual permutation pairs and actual Farey-neighbor vectors as representatives, so a positive result still reconstructs a physical ray in the original room.

| Dark control | Processed pair limit | Merged duplicate children | Discovered pair classes | Exact branch result |
| --- | ---: | ---: | ---: | --- |
| 20-wall slit room | 20,000 | 5 | 39,996 | UNKNOWN: state cap |
| 22-wall contact room | 20,000 | 11 | 39,990 | UNKNOWN: state cap |
| 24-wall simple room | 20,000 | 0 | 40,001 | UNKNOWN: state cap |

The earlier sufficient certificates still prove these rooms dark. UNKNOWN here describes only this attempt to close the more detailed exact direction-code enumeration. Counts from the capped search do not establish an orbit size or an impossibility theorem for other reductions.

The independent quotient audit compares canonical equivalence against exhaustive relabeling on all 972 colored three-sheet permutation systems. Three small complete orbit tests compare the entire quotient closure with canonicalized raw closure; one reduces six raw pairs to three classes, so the test exercises real merging. All merged representatives agree on mediant visibility and both canonical successor keys. Another 140 arbitrary relabelings of real-room direction-code states leave their canonical keys and visibility invariant. All four positive controls still yield independently verified physical paths: 13,9,8,8 reflections, respectively.

Artifacts: `cover-code-quotient-audit.json`, `cover-code-quotient-summary.json`, and `cover-quotient-dark{20,22,24}-result.json`. The option is explicit and disabled by default; its negligible observed compression does not justify making it the default search path.

```sh
.context/illumination-venv/bin/python .context/illumination_cover.py .context/illumination-20.json --quotient --max-states 20000 --seconds 45 --out .context/cover-quotient-dark20-result.json
.context/illumination-venv/bin/python .context/audit_illumination_code_quotient.py
```

**Next move:** shift effort toward a structural wall-count inequality or a genuinely different construction mechanism. The conservative endpoint relation and this exact relabeling quotient have both been tested; increasing their search caps alone has no demonstrated route to fewer walls.


## Research judgment: construct a midpoint obstruction first

[done] Reassessed the next direction on 2026-10-29. No new room, search run, or improved wall count is claimed.

The highest-upside construction proposal is to search for unfolded surfaces equipped with affine involutions of derivative -I, then ask whether they admit a planar mirror-room quotient with few walls. This is an inverse construction proposal, not a novel theorem. The midpoint argument appears explicitly in Lelièvre–Monteil–Weiss, Everything is illuminated, §6.3: https://arxiv.org/html/1407.2975v1#S6.SS3 . Their §6.1, Proposition 16, also constructs nonilluminating pairs by making every preimage of a common torus blocking set ramified.

Precise sufficient mechanism: let tau be an affine involution with derivative -I, sending regular point x to distinct regular point y. For a hypothetical unit-speed straight segment gamma:[0,L]→M from x to y avoiding blockers, tau(gamma(L-t)) starts at x with the same velocity as gamma. Uniqueness of straight continuation outside singularities makes the paths equal. Thus gamma(L/2) is fixed by tau. If every fixed point belongs to the absorbing set, no such segment exists. The affine map must respect the actual surface identifications; a coordinate half-turn alone is insufficient. The obstruction itself does not need a direction cutoff or direction-code orbit closure.

The essential gate is billiard realization. Fix one source lift x in the unfolded room. Every target lift y must be blocked; a separate admissible involution tau_y may be required for each y. A dark pair on an arbitrary translation surface does not imply a dark pair in a room. The quotient must be a bounded planar region with connected interior, the intended boundary class, and the actual absorbing corner sectors. These compatibility conditions should be imposed before optimizing walls. One useful bounded pilot would seek such certificates on known controls and positive regression fixtures, then search small compatible gluings. Failure to certify a known dark control would limit the certificate rather than refute the control.

The Veech-group alternative has sound prior art: square-tiled surfaces have finite-index modular stabilizers, and surface-dynamics computes their groups/cusps (https://flatsurf.github.io/surface-dynamics/examples/square_tiled_surfaces.html). Source/target/blocker markings must be preserved, including removable absorbing vertices. This does not yet justify another implementation: modular-orbit enumeration can reproduce the large permutation-pair orbit already encountered. No practical compression is established.

### A separate finite-size observation for the strict simple family

There is a useful elementary bound that improves the theoretical framing of the old searches. In the canonical unit 45-degree tiling, a strict certified simple polygon cannot have a B/C lattice vertex in the interior of a straight wall. Along any available axis or diagonal wall, no two consecutive lattice vertices are A. Consequently a maximal wall contains at most two atomic tile edges; its coordinate changes satisfy |dx|≤2 and |dy|≤2.

For a simple polygon with W walls, total horizontal boundary variation is at most 2W and at least twice the bounding-box width. Therefore width≤W; similarly height≤W. Translate its interior source A to (0,0), preserving the lattice labels. The entire room then lies in [-W,W]². Thus, for W≤23, the strict simple-family problem has a complete finite search domain of at most 4,232 available triangles, rather than an unbounded geometric search. This is an analytic size bound, not an executed search or a 24-wall lower bound. It does not cover transparent B/C vertices or general polygons. Contacts and slits require a separate boundary-occurrence argument before extending the statement to those classes.

Recommendation: prioritize the midpoint-involution realization gate for a smaller construction. If the goal changes to the most reliable theorem within the existing family, use the finite-size bound to develop a complete boundary-based exclusion. Do not increase the existing direction-code cap merely because more resources are available.


## Midpoint-involution pilot: complete lift coverage fails

[done] Executed the approved midpoint-symmetry gate on 2026-10-29. No new dark room or smaller wall count was found. The idea does not provide a shortcut for the current controls, and a small pilot on a different planar geometry also fails complete coverage.

### Exact maps and fixed-point accounting

`illumination_midpoint.py` compiles the existing room unfolding, identifies its actual surface vertices, and enumerates affine involutions with derivative -I separately on every connected component. Any such map that sends a lattice-vertex source to a lattice-vertex target preserves the integer grid. On unit squares it has the form (i,x,y)→(f(i),1−x,1−y). Edge compatibility requires fH=H⁻¹f and fV=V⁻¹f, and involutivity requires f²=id. A chosen image of one square determines the entire map on a connected component, so enumerating all its root images is complete for these maps; this is not a direction-bounded search.

The fixed-point test covers all three possibilities: square centers, edge midpoints, and vertices. A map is admissible only if every fixed point is an absorbing vertex. Removable absorbing corners are retained; any fixed regular point that is not an actual blocker disqualifies the map. Source and target need not be preserved as color sets by the symmetry itself. The certificate instead records exactly which source lifts it sends to which target lifts. DARK requires every source/target lift pair within each connected component to be covered by at least one admissible map. A missing certificate remains INCONCLUSIVE.

`translations` separately enumerates all grid-preserving derivative-I automorphisms. Two derivative-minus-I maps differ by a translation automorphism. In a connected eight-copy room unfolding, covering all eight distinct target lifts from a fixed source therefore requires at least eight distinct admissible half-turns, and hence at least eight translation automorphisms. This is a necessary filter for this certificate, not a necessary condition for darkness in general.

### Existing controls

| Room | Cover squares | Translation automorphisms | Half-turn involutions | Covered lift pairs / required |
| --- | ---: | ---: | ---: | ---: |
| 20-wall slit control | 88 | 1 | 1 | 0 / 64 |
| 22-wall contact control | 96 | 1 | 1 | 0 / 64 |
| 24-wall simple control | 108 | 1 | 1 | 0 / 64 |
| 18-wall illuminated survivor | 84 | 1 | 1 | 0 / 64 |
| 22-wall illuminated survivor | 104 | 1 | 1 | 0 / 64 |
| Mixed-sector regression 1 | 92 | 1 | 1 | 0 / 64 |
| Mixed-sector regression 2 | 96 | 1 | 1 | 0 / 64 |

Each unique involution is admissible, but maps source copies to copies of the same physical source rather than the distinct target. The three known dark controls retain their earlier parity proofs. Failure of this stronger sufficient certificate does not challenge those proofs.

### A different actual-room family

`probe_illumination_midpoint.py` constructs rectangular outer rooms with separated rectangular interior holes. For an nx-by-ny array, the outer rectangle is [0,4nx]×[0,4ny], and hole (i,j) is [4i+1,4i+3]×[4j+1,4j+3]. The interiors are connected; holes do not touch each other or the outer boundary. Walls count all maximal segments of the outer and hole boundaries.

| Hole array | Walls | Interior lattice points | Distinct physical point pairs checked | Admissible half-turns per component | Fully covered pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| 3×1 | 16 | 6 | 15 | 2 | 0 |
| 4×1 | 20 | 9 | 36 | 1 | 0 |
| 2×2 | 20 | 13 | 78 | 1 | 0 |

These orthogonal-room unfoldings have two connected components; each contains four lifts of each interior point and four translation automorphisms. All 129 distinct interior integer-grid point pairs were checked. The scope excludes non-lattice marks, other obstacle placements, and other surface gluings.

The 16-wall room has three partially covered physical point pairs. In particular S=(4,2), T=(8,2) has 8 covered lift pairs out of 32 required across the two components. Nevertheless direction (2,1) illuminates T after exactly 12 reflections. The existing exact physical tracer constructs this ray and the independent segment/wall verifier validates it. `midpoint-holes-partial-room.json` and `midpoint-holes-partial-witness.json` preserve the example. This is a concrete counterexample to accepting partial reflected-target coverage, not a dark-room discovery.

### Audit and outcome

`audit_illumination_midpoint.py` compares complete half-turn and translation enumeration with brute-force permutations for all 617 H,V systems on one through four squares, checking 1,161 half-turns. An independent corner-equivalence graph and direct gluing/fixed-point checks validate every admissible map on the real controls and the obstacle pilot. A 4×4 torus with four explicitly absorbing regular points certifies one dark pair; removing those blockers makes the certificate fail. This positive fixture is an abstract surface, not a polygonal room. Three corrupt certificates—an invalid square map, removed blockers, and an omitted connected component—are rejected. Four earlier illuminated physical controls and the new 12-reflection partial-coverage example have independently validated rays.

The audit output is `midpoint-final-audit.json`; the inverse pilot summary is `midpoint-inverse-pilot.json`. Reproduce with:

```sh
.context/illumination-venv/bin/python .context/probe_illumination_midpoint.py
.context/illumination-venv/bin/python .context/audit_illumination_midpoint.py
```

The physical partial-coverage witness is already saved; generating it used `illumination_cover.solve` with a 2,000-state/5-second cap and terminated positively after two processed states. No negative conclusion depends on that cap.

Judgment after this pilot: the midpoint method works mathematically but requires substantially more suitable surface symmetry than any tested room supplies. A general inverse-gluing search is not implemented and is not ruled out. I would now prioritize the strict-simple-family finite-size bound and a boundary-based exclusion, rather than expanding this symmetry pilot or returning to larger direction-code caps. That is a recommendation, not a claim that 24 is globally minimal.


## Complete exclusion below 24 in the strict simple 45-degree family

[done] Completed 2026-10-29. **The minimum wall count in this entire family is 24**, conditional on the mathematical model and solver correctness. The finite reduction is analytic; the seven finite exclusions are independently reproduced by two different integer solvers and formulations. No formal proof-assistant theorem or independently checked UNSAT proof file is provided. No novelty or literature-priority claim is made.

### Precisely which family is covered

The room is a finite union of the canonical unit 45–45–90 triangles used throughout this report. Its interior is connected and its boundary is a simple Jordan polygon: no holes, slits, or point contacts. It has at least two distinct interior A vertices. Every used B/C vertex is an actual absorbing boundary corner; none is interior or a smooth boundary point. Smooth A boundary points are permitted. Walls are maximal straight boundary segments. Uniform scaling and Euclidean reorientation of such a room do not affect the result.

This excludes arbitrarily large assemblies in this family, all placements of the two marked interior A points, and additional interior A points. It does not exclude a 23-wall polygon with transparent B/C vertices, other angle/length structures, non-grid walls, different source/target conventions, or other room classes.

### Counting identity

Let N be the number of triangles, I the number of interior A vertices, s the number of smooth boundary A vertices, and W the wall count. For a nonsmooth boundary A vertex, let k be its number of incident triangles, equivalently its interior angle in units of 45 degrees. Let K be the sum of these k values. Since each triangle has exactly one A vertex,

    N = 8I + 4s + K.

Every nonsmooth boundary vertex is one wall endpoint along the simple boundary; all B/C vertices are nonsmooth. Thus the number of boundary lattice vertices is W+s. Euler's formula for a triangulated disk gives

    N = 2I + W + s - 2.

Combining the equations gives

    W = 2 + 6I + Q,       Q = 3s + K.

Call Q the boundary A charge. An empty A-centered cell contributes zero. Every nonempty nonfull A cell contributes at least one: k for a nonsmooth A boundary vertex, or three when k=4 is smooth. Interior A cells contribute zero charge.

Each full A cell is the square [-1,1]² about its A center, subdivided into eight triangles. At the C midpoint of each of its four sides, two incident triangles are already occupied. A strict simple C vertex may have one or three incident 90-degree triangles; it cannot be smooth or interior. Therefore exactly one triangle on the other side is required. All four neighboring A cells are nonempty and nonfull. In particular, adjacent full A cells are impossible and Q>=4 whenever I>=1.

Consequently W>=6I+6. If W<=23 and I>=2, then **I=2 and Q<=9**. The two original identities also give

    N <= floor(4(W-2)/3) <= 28.

The bound counts every interior A, including unmarked ones; an overlooked third interior source-type vertex cannot evade it.

### Seven possible separations

Divide A coordinates by two so their centers form the square lattice Z². Adjacent cells share two possible B–C boundary edges. Open-tile connectivity implies connectivity of the graph of used A cells, with ordinary horizontal/vertical grid adjacency.

Normalize one interior A center to (0,0), and write D for its Manhattan distance to the other full A cell. D=1 is forbidden by the C argument. If D>=3, the four mandatory partial neighbors of each full cell are all distinct, using at least eight of the nine available units of charge. The two five-cell crosses (a full cell plus its four neighbors) are at graph distance D-2. Connecting them requires at least D-3 additional partial cells, each of charge at least one. Hence

    Q >= 8 + (D-3) = D+5,       D <= 4.

For D=2 the crosses can overlap; that case is retained explicitly. Rotations and reflections preserve the canonical tiling and all its labels. They reduce every possible separation to the following seven A-cell targets:

    (1,1), (2,0), (2,1), (3,0), (2,2), (3,1), (4,0).

In physical coordinates these are (2,2), (4,0), (4,2), (6,0), (4,4), (6,2), and (8,0).

### Finite support with no arbitrary cutoff

Let R consist of the two full cells and their mandatory neighbors. Let b be the number of distinct mandatory partial cells in R. At most r=9-b other partial cells can occur anywhere. For any used cell outside R, follow a shortest path in the connected used-cell graph until it first meets R. The path has at most r outside vertices. Therefore every used cell lies within Manhattan distance r of R.

This proves that the supports constructed by `illumination_family_bound.support` contain every possible <=23-wall candidate. No large-distance placement or long corridor is silently excluded.

| Second A, physical coordinates | Mandatory partial cells b | Extra cells r | Available triangles in complete support | CP-SAT <=23 |
| --- | ---: | ---: | ---: | --- |
| (2,2) | 6 | 3 | 400 | INFEASIBLE |
| (4,0) | 7 | 2 | 296 | INFEASIBLE |
| (4,2) | 8 | 1 | 176 | INFEASIBLE |
| (6,0) | 8 | 1 | 192 | INFEASIBLE |
| (4,4) | 8 | 1 | 184 | INFEASIBLE |
| (6,2) | 8 | 1 | 192 | INFEASIBLE |
| (8,0) | 8 | 1 | 200 | INFEASIBLE |

### Two independent formulations

`search_illumination_family.py` uses CP-SAT with binary tile choices, local angular-sector tables, exact wall costs, a connected parent forest, and Euler characteristic one. It fixes exactly the two full A stars, bounds N by 28, and imposes W=14+Q with W<=23. All seven cases return INFEASIBLE.

`verify_illumination_family.py` builds a separate one-hot fan formulation using the independent fan-angle traversal from `illumination_geometry.check_fan_angles`. Fan rows are linked through shared binary triangle variables. This model keeps the necessary identity W-Q=14 but relaxes explicit connectivity and the tile-count bound. SCIP 10.0.0 proves that every integer solution in each finite support has W>=24. Since this is a relaxation containing every candidate, it independently excludes W<=23. Higher minima returned by SCIP in particular bounded supports must not be interpreted as family-wide optima at those placements: the supports were derived only under the assumption W<=23.

The continuous GLOP relaxations have bounds 131/6 or 22, insufficient to exclude 23 walls. These are not used as proof of the integer result. No exact rational dual certificate above 23 was obtained; the exclusion relies on the integer solvers.

The known 24-wall simple room is accepted by the CP-SAT model at wall cap 24, both with a solution hint and with its exact triangle choices fixed. Its one-hot fan assignment satisfies every independent equation with integer arithmetic and has objective 24. Thus the lower bound is attained in the family.

### Independent checks and reproducibility

`audit_illumination_family.py` checks:

- All 528 local tile masks around representative A, B, and C vertices: angular slots and independent fan traversal agree exactly.
- All 617 connected A-cell supports obtained by attaching the remaining <=3 cells to the mandatory crosses for symmetry representatives through Manhattan separation eight. They match the seven allowed targets and fit the proven supports. The analytic D+5 inequality, not this finite audit, excludes larger separations.
- Sixteen rotations/reflections/source exchanges and even translations of the known 24-wall room. The counting identity, charge ten, and tile count 27 remain correct.
- The exact 24-wall control in both formulations.
- All seven CP-SAT infeasibilities and all seven independently formulated SCIP exclusions.

The audit passes. `family-under24-summary.json`, `family-independent-summary.json`, and `family-final-audit.json` retain the results. Dependencies are the existing pinned OR-Tools environment; SCIP and GLOP are bundled solver backends. No new package installation was needed.

```sh
.context/illumination-venv/bin/python .context/search_illumination_family.py --seconds 60
.context/illumination-venv/bin/python .context/search_illumination_family.py --control --seconds 30
.context/illumination-venv/bin/python .context/verify_illumination_family.py
.context/illumination-venv/bin/python .context/audit_illumination_family.py
```

**Consequence for further construction work:** enlarging the patch or relocating the source and target cannot improve the strict simple 45-degree construction below 24. A smaller simple room must leave at least one of this family's defining assumptions. Transparent B/C points remain a possible escape; the earlier one/two-transparent-point exclusions were bounded-patch results and are not upgraded by this theorem.


## Complete one-exception exclusion

[done] Completed 2026-10-29. **A single transparent B/C vertex cannot reduce the simple canonical 45-degree family below24 walls.** Combined with the strict-family result and its attained24-wall control,24 remains the minimum when at most one exception is allowed. This is a computer-assisted result conditional on the geometric model, finite reductions, path-cut implementation, and CP-SAT correctness. It is not a general polygon theorem or a formally checked UNSAT proof.

### Extended counting identity

Retain I_A, s_A, and K from the strict proof. Let J be the number of interior non-A vertices and s_N the number of smooth non-A boundary vertices. These are precisely the two kinds of transparency in a simple room. A boundary contact cannot combine both kinds at one coordinate because the boundary is simple. Define

    Q = 3s_A + K,       E = 2J + s_N.

Euler's formula counts I_A+J interior lattice vertices and W+s_A+s_N boundary lattice vertices. Counting A incidences still gives N=8I_A+4s_A+K. Hence

    W = 2 + 6I_A + Q - E,
    N <= floor(4(W-2+E)/3).

For exactly one exception, J+s_N=1, so E is one for a smooth boundary exception and two for an interior exception. Below24 walls this bounds N by29 and30 respectively. Every nonempty nonfull A cell still contributes at least one unit of Q.

### There are exactly two full A cells

The identity first gives I_A<=3 below24, since I_A>=4 would imply W>=26-2=24. For three full A cells, their external grid-neighbor set has at least seven cells. Each such neighbor must be nonempty unless a smooth C exception removes that obligation; at most s_N neighbors can be missing. Therefore

    Q >= 7-s_N,
    W >= 20 + 7-s_N - (2J+s_N)
      = 27 - 2(J+s_N) = 25.

Thus I_A=3 is also impossible below24, leaving **I_A=2 and Q<=9+E**. In particular there are at most13 used A cells.

The grid-neighbor lemma is elementary. If the three cells have two internal grid edges, they form a straight or bent path with eight or seven external neighbors. With one internal edge, the isolated cell overlaps the adjacent pair's external neighborhood in at most two places, leaving at least eight. With no internal edges and mixed checkerboard parities, only one pair can share neighbors. With all three on one parity, any pair shares at most two neighbors; all three pairs cannot simultaneously have two shared neighbors because the diagonal-neighbor grid has no triangles. Inclusion-exclusion then gives at least seven. `three_vertex_boundary_check` independently enumerates all138 connected distance-two-overlap patterns, attaining seven. Disconnected overlap patterns have at least4+6=10 external neighbors, so arbitrarily separated triples are covered too.

### Fourteen complete placement supports

As before normalize the source A cell to (0,0) and divide physical A coordinates by two. Adjacent full A cells illuminate one another by the direct segment through their shared, necessarily ordinary C midpoint. They therefore cannot be a counterexample, irrespective of the search.

Let R be the two full cells and all their grid neighbors, and b the number of distinct nonfull cells in R. At most one mandatory neighbor can be absent, and absence requires the single exception to be a smooth C point. If m is the number absent, then

    E+m <= 2,       Q+m <= 11.

The number of used partial cells outside R is at most

    Q - (b-m) <= 11-b.

Every used outside cell has a path to R through the connected A-cell graph, so the complete support is the Manhattan neighborhood of R of radius r=11-b. This proof allows R to include the possibly absent neighbor; it does not assume every mandatory cell is used.

If the full-cell separation D>=3, b=8. Connecting the two crosses requires at least D-3 outside cells, while at most three are available. Thus D<=6. After square symmetries the fourteen nonadjacent A-cell target placements are

    (1,1), (2,0), (2,1), (3,0), (2,2), (3,1), (4,0),
    (3,2), (4,1), (5,0), (3,3), (4,2), (5,1), (6,0).

All candidate triangles lie in the corresponding analytically derived finite support. No arbitrary spatial cutoff is used.

### Complete search outcome

`search_illumination_family.build_model(..., transparent_budget=1)` allows exactly one B/C vertex to be interior or smooth, fixes the two full A stars, and imposes the extended identity, the30-triangle bound, the support bounds, connected interior, and Euler characteristic one. It enforces a single occupied boundary sector per vertex and forbids slits, contacts, and holes. Both exception types pass fixed-geometry positive checks against saved illuminated examples.

Eleven placement models are geometrically INFEASIBLE below24 walls without any ray cuts. The three remaining cases are exhausted by exact connecting-ray cuts:

| A-cell target | Physical target | Saved room-and-mark configurations | Distinct symmetry-derived ray cuts | Final result |
| --- | --- | ---: | ---: | --- |
| (1,1) | (2,2) | 79 | 273 | INFEASIBLE after cuts |
| (2,0) | (4,0) | 404 | 204 | INFEASIBLE after cuts |
| (2,1) | (4,2) | 29 | 58 | INFEASIBLE after cuts |
| Other eleven placements | Twice the listed A-cell coordinates | 0 | 0 | Geometrically INFEASIBLE |

The512 configurations are distinct when both geometry and marks are included. Comparing canonical triangle/mark keys against every historical transparency/placement screen mechanically identifies423 reused configurations and89 new configurations. Saved witnesses have at most31 reflections. These ray counts are positive witnesses, not negative direction bounds.

A ray is found using the existing exact rational tracer and then checked by the independent sector-aware segment/wall verifier. Each cut preserves enough tile choices to retain that exact path. Smooth contact ambiguities do not occur in this simple-room family. Symmetry operations preserve the unordered marks; swapping the marks also reverses the path. Every derived path is independently checked before use.

For cut compilation, only tiles whose closure meets the ray's closed coordinate bounding box need inspection. This includes every tile incident at a visited vertex and both sides of every crossed/reflected edge, including absent tiles. `tile_facts` translates the previous open-edge guards into tile choices, since no slits are allowed and an edge is open exactly when both incident triangles are selected. Three full-support-versus-clipped guard comparisons agree exactly, and64 unconstrained tile flips preserve the independently verified paths.

The first diagonal attempts hit solver caps and were explicitly left unresolved; an initial axis attempt spent its allotted time on seeding and did not solve. Validated cuts were retained across resumptions. The final diagonal model closes after79 saved configurations, and the final axis and offset models also close. No capped run or finite ray miss is used as an exclusion. `one-global-summary.json` now records EXCLUDED for all14 cases.

### Audit and limits

`audit_illumination_one_exception.py` rebuilds every complete support and all535 recorded cuts from the saved evidence, checks all535 symmetry-derived paths against the independent segment/wall verifier, and obtains INFEASIBLE in **fresh CP-SAT models for all14 placements**. It also checks the extended count and support identities on165 prior one-exception geometries, accepts exact fixed-geometry controls for both interior and boundary exceptions, verifies the138-pattern grid lemma, and performs the guard comparisons and mutations described above. The audit passes; see `one-global-final-audit.json`.

The strict-family audit was also rerun successfully after extending the shared model builder:528 local tile masks,617 connected-cell support checks,16 transformed controls, and the exact24-wall control still pass. The independent fan formulation was extended to allow one exception. An auxiliary SCIP feasibility run independently reproduces four geometric exclusions, while another case hits its60-second limit; the remaining auxiliary work was stopped. `one-global-independent-geometric.json` preserves these partial secondary checks. **This is not a full second-solver replication of the one-exception result.** The complete result uses fresh-model CP-SAT replay and independently verified ray cuts; it still lacks a formal UNSAT certificate.

Additional geometric checks on the final diagonal placement show that an interior non-A exception must be the midpoint B=(1,1), which yields a direct illuminating segment. The only other possible exception locations are the four neighboring C points (1,0), (0,1), (2,1), and (1,2). These checks are saved in `one-diagonal-interior-midpoint-check.json` and `one-diagonal-exception-location-check.json`; the complete ray-cut exclusion does not depend on them.

Reproduce the full negative replay without relying on search caps:

```sh
.context/illumination-venv/bin/python .context/audit_illumination_one_exception.py
```

Search/resume uses the saved positive evidence and skips already exhausted cases:

```sh
.context/illumination-venv/bin/python .context/search_illumination_one_exception.py --seconds 90
```

The result covers simple canonical45-degree rooms of any assembly size with distinct interior A marks and at most one nonabsorbing B/C point. It does not cover two or more exceptions, non-A marks, different tilings, non-grid mirrors, holes, slits, or contacts. No smaller room was found and no historical priority claim is made.

**Next construction threshold:** within this family, a simple room below24 walls now needs at least two transparent B/C vertices. The same general identity gives N<=33 for at most two exceptions and W<=23, providing a finite starting point for that next investigation. This33-triangle bound is derived; the complete two-exception family has not been searched. The older two-exception result remains confined to its original small patch.


## Two transparent vertices: complete reduction and search (2026-10-29)

[done] Two-exception structural reduction and bounded experiment completed. The extension has a complete finite reduction. The three-interior-A case is impossible. A connected-cell degree argument reduces the two-interior-A branch to seven nonadjacent marked placements, at most nine partial A cells, and at most33 triangles. Four of seven finite cases are excluded; three remain open at search caps. No two-exception family exclusion is claimed.

### Interior A count and the three-star equality case

Write k=J+s_N<=2 and E=2J+s_N. Every absent external neighbor of a full A cell requires a smooth C exception; at most s_N external cells can therefore be absent. Any finite nonempty set of full grid cells has at least four external neighbors (take extremal cells in the four coordinate directions). Thus Q>=4-s_N, and

W=2+6I+Q-E>=6+6I-2k>=2+6I.

For I>=4 this is at least26. For I=3 the earlier seven-external-neighbor lemma gives W>=27-2k>=23. Equality at W<=23 forces k=2, exactly seven external cells, no charge beyond the required partial cells, and every occupied partial cell has charge1. Enumeration of all138 connected distance-two overlap triples shows that the unique seven-neighbor pattern, up to grid isometry, is an L. Disconnected overlap components have at least ten external neighbors, so they cannot attain equality.

The two internal full-cell adjacencies in the L force two interior C exceptions. Consequently J=2, s_N=0, Q=7, and each of the seven external A cells contains exactly one triangle. The complete80-triangle CP-SAT model is INFEASIBLE (`two-three-star-check.json`). An independent fan-based constraint enumeration, with no CP-SAT, wall equation, connectivity requirement, or Euler constraint, finds zero assignments after257 search nodes over the seven eight-choice partial cells (`two-three-star-independent.json`). It allows transparency at the two forced interior C coordinates and forbids any other transparent B/C point. Therefore this necessary local relaxation already excludes the three-star equality case, regardless of which two full stars are marked.

### Charge pays for connections

Form a graph with one vertex per occupied A cell and an edge when two cells share a selected triangle edge. Triangle edge-connectivity implies graph connectivity. A full cell has graph degree at most4. A partial cell has one contiguous A fan of k triangles; its charge is k, except k=4 has charge3. The fan touches at most its charge many distinct cell sides. This is verified independently on all56 nonempty, nonfull contiguous masks in `degree_lemma`.

If P is the number of partial cells and I the number of full cells, the connected graph has at least I+P-1 edges. Summing degrees at partial cells and bounding total full-cell degrees by4I gives

Q >= sum(partial degrees) >= 2P-2I-2.

For I=2, Q>=2P-6. Since W<=23 gives Q<=9+E<=13, P<=9. Let R contain the two full cells and their grid neighbors, b=|R|-2, and m count absent required partial cells. As in the one-exception proof, m<=s_N and E+m<=4. Each absent required cell removes at least one possible full-cell graph edge, so total full-cell degree is at most8-m. Therefore the stronger inequality is

Q >= 2P-6+m.

Combining with Q<=9+E gives

2(P+m) <= Q+6+m <=15+E+m<=19,

so P+m<=9. There are at most9-b occupied cells outside R. Connectedness places every occupied cell within Manhattan radius9-b of R. For full-cell separation D>=3, b=8, and a connecting path requires at least D-3 outside cells; hence D<=4. D=1 illuminates directly. The seven remaining normalized A-cell targets are

(1,1), (2,0), (2,1), (3,0), (2,2), (3,1), (4,0).

These are the same support sets used for the strict zero-exception family. Their sizes are50,37,22,24,23,24,25 A cells, respectively; each A cell contributes eight available triangles. This is a complete reduction for W<=23, not a restriction to an arbitrarily selected patch. The intermediate looser reductions to23 and then10 placements were superseded before any final exclusion claim.

`illumination_two_exception_bound.py` constructs these complete supports. `search_illumination_two_exception.py` searches them with exact positive ray cuts. A capped solver or missed finite ray search remains incomplete. Historical rays are recompiled against the new triangle indexing before reuse. `audit_illumination_two_exception.py` reconstructs guards, verifies rays, checks fixed positive models and mutations, and replays exhausted cases. The earlier full14-case one-exception audit also passes after generalizing the shared model builder.


### Finite search outcome

The final bounded run covers all seven complete supports. Four placements are exhausted: (3,0), (3,1), and (4,0) are geometrically INFEASIBLE; (2,2) is INFEASIBLE after42 saved exact-ray configurations supply76 cuts. The remaining A-cell placements (1,1), (2,0), and (2,1) remain open at60-second search caps per case (seed validation/build time is additional). The final run finds39,49,90 additional illuminated configurations in those cases, respectively. Earlier same-turn pilots also contribute newly found records; the independent audit measures novelty against historical transparency and placement files rather than adding overlapping run counts.

Source normalized to physical (0,0), any sub24 counterexample with at most two B/C exceptions therefore has target (2,2), (4,0), or (4,2), subject to grid symmetries and mark exchange. It has exactly two full A stars and exactly two exceptions. This conclusion uses the completed zero/one-exception results, the three-star exclusion, the connected-cell reduction, and the four completed finite cases. It does not claim the three capped cases are excluded.

Reproduce with `.context/illumination-venv/bin/python`:

```sh
python .context/audit_illumination_three_star.py
python .context/search_illumination_two_exception.py --seconds 60
python .context/audit_illumination_two_exception.py
python .context/audit_illumination_one_exception.py
```

The search resumes saved positive rays, recompiles their guards for the current support, and skips saved exhausted cases. At that capped stage the complete two-exception family remained INCOMPLETE; the typed-pair follow-up below supersedes that status. No smaller dark construction, general polygon lower bound, or formal UNSAT proof was established by the capped experiment. The next useful target is the geometry of the two exceptional vertices within these three nearby mark placements; larger patches add no cases under the proved support bounds.


### Final audit

`two-global-final-audit.json` passes: all977 distinct configurations and2010 symmetry-derived exact rays/cuts are rechecked, all335 historical two-exception geometries satisfy the connected-cell inequalities, all three exception combinations pass fixed positive model controls, three clipped/full-region guard comparisons agree, and64 guard-preserving tile mutations preserve their witnesses. Fresh CP-SAT models replay all four exhausted placements as INFEASIBLE. Against all preexisting transparency/placement screen records,193 configurations are new in this turn and784 are reused; the maximum saved path has34 reflections. The independent three-star fan audit passes separately, as does the full prior14-case one-exception audit after the shared model changes. The known24-wall strict control remains feasible with its fixed geometry (`two-control24.json`).

All searches and audits have stopped. Artifacts stay local and gitignored. The tracked checkout is unchanged. No external publication or communication was made.


## Typed exception-pair classification (2026-10-29 follow-up)

[done] Classified the exception geometry of the three remaining placements and exhausted their fixed-pair models with exact illuminating rays. The original seven placement files and their final audit remain immutable; the new files retain their SHA-256 provenance and triangle-index digest.

A typed pair records the physical coordinates of both exceptional B/C points and whether each is ordinary interior (value2) or smooth boundary (value1). Mark-preserving square symmetries and mark exchange give four isometries for the diagonal and axis placements, and two for the skew placement. After the previously audited exact-ray exclusions, complete projection enumeration gives45,38,49 classes for A-cell targets(1,1),(2,0),(2,1), respectively. A fresh infeasible model after blocking these pairs establishes complete class coverage; it does not by itself exclude the classes. Counts of26,65,68 in `two-pair-observed.json` instead describe classes represented in the earlier saved illuminated configurations, so these are different populations.

`classify_illumination_two_exception.py` saves one geometrically checked feasible room per projected pair and blocks its full typed symmetry orbit. A projection time cap remains incomplete; the diagonal projection was resumed and then exhausted, without adding another class. Every mark-preserving isometry is checked to preserve the complete triangle support.

`search_illumination_exception_pairs.py` fixes each pair's coordinates and types. Existing exact-two-exception constraints force every other B/C point to be absorbing. New ray guards are added to both the fixed-pair branch and the shared parent model, allowing one class's rays to eliminate other classes. Closed branches remain closed as positive cuts accumulate. Geometry, exception types, connecting paths, and each symmetry-derived path are checked before excluding a room. A finite ray miss is saved as an unresolved candidate and never cut.

The first bounded pass and resumed searches close all38 axis classes and all49 skew classes; each combined parent model is INFEASIBLE. The diagonal has four classes left after the8-second-per-class resumed pass; these receive30-second caps. The subsequent30-second-per-open-class diagonal pass closes all four remaining classes after21 additional rays. All three combined models are INFEASIBLE. Independent audits now pass for all three placements.

`audit_illumination_exception_pairs.py` independently extracts exceptions by angle sums, uses explicit isometries rather than the classifier's group routine, fixes every projected witness in a fresh positive model, replays class coverage, reconstructs every new ray guard, compares clipped/full guards, mutates unconstrained tiles, and replays every claimed class and complete parent exclusion.


### Completed exclusion and audit

The classification has132 classes in total. Every class has a fixed, geometrically verified positive witness in the parent model, and independently rebuilding the model after blocking all typed pair orbits gives INFEASIBLE for each placement. The independent orbit check uses explicit coordinate maps; the independent exception extractor sums incident triangle angles instead of calling the classifier's fan routine.

| A-cell target | Typed classes | New illuminated configurations | New exact ray cuts | Fresh combined-model replay |
| --- | ---: | ---: | ---: | --- |
| (1,1) |45|269|1076|INFEASIBLE|
| (2,0) |38|79|316|INFEASIBLE|
| (2,1) |49|129|258|INFEASIBLE|
| Total |132|477|1650|All three excluded|

All132 fixed-pair exclusions also replay INFEASIBLE individually. Each of1650 new symmetry-derived rays is checked by the independent physical segment/reflection verifier and its tile guard is recompiled. Six full-region/clipped guard comparisons agree, and48 unconstrained tile mutations retain their witnesses. The longest saved new path has48 reflections. Room-and-mark keys confirm that all477 new configurations are distinct and disjoint from the previous977; the two-exception phases therefore total1454 configurations and3660 exact derived ray cuts. `two-pair-final-audit.json` reports PASS/EXCLUDED, with per-case source hashes.

Crucially, the final combined models use the original complete geometric supports plus positive-ray cuts only. The pair-fixing and projection-blocking constraints are confined to discovery/coverage branches. The final global infeasibility replays therefore do not depend on the pair-classification strategy for their negative conclusion.

Compose those three exclusions with the four completed earlier placements, the independent three-full-star exclusion, and the analytic exclusion of four or more full A stars. This rules out every simple canonical room below24 walls with exactly two B/C exceptions and distinct interior A marks, across arbitrary assembly sizes. The preceding zero/one-exception results cover smaller exception counts. The known strict24-wall room is an attained control. Hence24 is the minimum for this family with at most two exceptions.

This is a computer-assisted result conditional on the finite reductions, geometric model, exact ray verifier/guards, and CP-SAT correctness. It is not a general-polygon lower bound, formal UNSAT certificate, or claimed literature record. No smaller dark construction was found. All jobs have stopped; this task made no publication, external communication, or tracked-file edits. A separate AGENTS.md modification appeared during the work and was preserved.

Reproduce with `.context/illumination-venv/bin/python`:

```sh
python .context/classify_illumination_two_exception.py --seconds 60
python .context/search_illumination_exception_pairs.py --seconds-per-class 3
python .context/search_illumination_exception_pairs.py --seconds-per-class 10
python .context/search_illumination_exception_pairs.py --target 1 1 --seconds-per-class 30
python .context/audit_illumination_exception_pairs.py
```

Search commands resume saved positive rays and previously closed classes. The standalone summary `two-complete-summary.json` composes the earlier and final audit receipts; historical `two-global-summary.json` preserves the previous capped phase and is not the current final status.

**Next construction threshold:** a sub24 simple room in this tiling now needs at least three transparent B/C points. The most structurally different next branch allows an additional unmarked full A star: unlike the two-exception case, three exceptions no longer make that branch impossible by the same wall-count bound. This is a proposed next direction, not a searched or proved three-exception result.


## Three exceptions and the cost of connecting marked neighborhoods

[done] The three-full-A-star branch is excluded below 24 walls: all five complete arrangements and ten raw nonadjacent marked-pair cases pass CP-SAT and separate fan/SCIP exclusions. Its 23 configurations have exact rays. Claude independently rederived the finite reduction and confirmed every guard and exclusion in his own model (`claude-illumination-check/report.md`). The prior proposal to investigate this branch is therefore resolved.

The remaining two-full-star branch has P+m≤10, at most 36 triangles, mark distance at most five, and exactly ten complete normalized nonadjacent placements. A new connecting-path bound charges partial cells at least two for a turn and three for a straight passage. Exhaustive local-fan and path checks agree with an independent directed-edge shortest-path calculation. Restricting the outside cells to the complete connected sets strengthens the geometric models.

The bounded pass excludes six placements in the current necessary models. Targets (4,1) and (5,0) have wall lower bounds 24 and 26; targets (4,0) and (3,2) are geometrically infeasible after the connectivity restrictions. Targets (3,0) and (3,1) are excluded by 26 and 84 exact positive-ray guards. The former needs a 48.4-second direct replay; its frozen case and short audit replay retain UNKNOWN. The latter also excludes in a separate one-hot fan/SCIP relaxation. Physical marked coordinates are twice these A-cell coordinates.

All 318 new configurations have exact connecting rays, with up to 45 reflections. The full audit passes all 4,944 guards (3,908 recompiled seeds plus 1,036 new guards), 72 guard-preserving mutations, 72 corrupt-guard checks, and all eight applicable path and outside-set checks. Final parents contain necessary geometry and positive-ray cuts only. A supplementary typed-triple partition closes ten explicit branches for (3,0), but its complement caps; the direct parent replay supplies that exclusion.

[waiting on Claude] Independent verification of this phase's new connectivity bounds, no-cut geometry, and ray inputs. The 54-path input manifest is frozen; his files and AGENTS.md are untouched. Four placements, (1,1), (2,0), (2,1), and (2,2), remain open at solver limits. No smaller dark construction or full three-exception minimum is established. The 24-wall minimum still applies to at most two exceptions. All Codex jobs have stopped.

Detailed derivation and reproduction: `three-two-star/findings.md`. Composed status: `three-two-star/summary.json`; guard receipt: `three-two-star/audit.json`; frozen inputs: `three-two-star/proof-inputs.json`.

**Next move:** combine Claude's independent geometry projection with typed-exception searches on the four remaining nearby placements. Larger patches add no cases under the complete reduction.


## Complete cell partition closes the seventh three exception placement

[done] Target A-cell (2,2), physical displacement (4,4), is excluded below 24 walls for simple canonical 45-degree rooms with distinct interior A marks and exactly three B/C exceptions. The typed-triple searches add 558 illuminated configurations and 1,988 exact guards across four placements; 150 fixed positive representative models and 128 class exclusions pass audit. Their projections remain incomplete, so closing all 63 listed diagonal classes does not itself prove that placement impossible.

A complete occupied-cell partition supplies the missing coverage. P+m=b+o≤10 bounds the outside-cell count. Adding absent mandatory neighbors preserves connectivity through the full roots. Frontier growth and independent exhaustive subset enumeration agree on 2,530/699/105/40 connected outside sets for targets (1,1)/(2,0)/(2,1)/(2,2), respectively, over 698,437 checked subsets. All 40 diagonal branches are excluded after 51 additional illuminated configurations and 202 exact new guards. A fresh audit replays every branch and the unrestricted positive-ray parent INFEASIBLE.

This phase therefore checks 609 new configurations and 2,190 guards, plus 40 tile mutations and 40 corrupt-guard checks; all pass. Seven of ten placements are now excluded in the current models. Three remain open: (1,1), (2,0), (2,1). No smaller dark room or complete three-exception minimum is claimed. The previous 24-wall minimum with at most two exceptions is unchanged. Claude's independent verification of this phase is pending; frozen inputs and neutral reproduction commands are on the board. All Codex jobs stopped.

Detailed derivation and receipts: `three-triples/findings.md`, `summary.json`, `audit.json`, `connectivity-audit.json`, `cell-audit-2-2.json`, `proof-inputs.json`, and `cell-proof-inputs.json`.

**Next move:** use the complete 105-cell-set partition for target (2,1), then the two shorter mark separations. The complete partition avoids treating an unfinished triple projection as exhaustive.


## Complete cell partitions explained and the 105 set follow up

[done] The breakthrough is complete coverage: the wall budget gives P+m≤10, and P+m=b+o with b=8 leaves at most two outside cells. Missing mandatory neighbors still consume the budget. Adding them to a real occupied-cell graph preserves connectivity, so the connected outside-set enumeration covers arbitrarily large assemblies in this canonical family. Each coarse set represents many possible rooms; exact illuminating-ray guards eliminate families within it. This closes the 40-set diagonal case despite an unfinished exception-triple projection. An explanatory diagram and derivation are in `three-triples/cell-2-1-findings.md` and `cell-partition-explanation.png`.

The next target, A-cell(2,1), has a complete105-set partition. Bounded 4/20/60-second passes exclude87/97/99 sets, respectively. Fresh replay of every branch raises the exclusion count to100, leaving five feasible-after-cuts sets. The new516 configurations and1032 exact ray guards,8 mutations and8 corrupt-guard checks all pass audit. All two-outside-cell cases are excluded. The residual sets are empty, {(-1,-1)}, {(3,2)}, {(1,-1)}, {(1,2)}, forming three types under mark exchange c→(2,1)−c. The whole placement remains open; seven of ten placements remain excluded overall.

Claude independently checked the path-charge and cell-set lemmas. His earlier weaker-model caps omit these constraints and do not refute the exclusions; independent model replays with those lemmas and newer guard checks remain pending. Frozen current inputs: `three-triples/cell-proof-inputs-2-1.json`; fresh receipt: `cell-audit-2-1.json`. All Codex jobs stopped. No smaller dark construction or full three-exception minimum.

**Next move:** split the three residual symmetry types by local cell fan patterns, including absence where allowed.


## Central-cell fan refinement narrows the skew placement

[done] A complete 57-mask split at A-cell(1,0), including absence, refines all five residual target(2,1) outside sets into285 branches. The discovery passes exclude264; fresh audit excludes267 and leaves18 feasible-after-cuts branches. All57 fan masks are excluded for each of {(-1,-1)} and {(3,2)}, closing two more outside sets. Combined with the previous100 audited exclusions,102/105 sets are excluded. The remaining sets are empty, {(1,-1)}, {(1,2)}, forming two mark-exchange types.

The audit checks393 new illuminated configurations,786 exact guards,8 mutations and8 corrupt guards; longest path39 reflections. Independent triangle adjacency verifies the56 nonempty partial fans plus the empty mask. The separate three-second replay directly excludes98/105 original cell branches; four previously proved two-cell branches cap at this shorter limit. Their earlier exclusions persist under the added valid constraints, so the cumulative102 count uses the union of prior proofs and two complete new fan proofs. The unrestricted parent remains feasible. Overall seven of ten placements remain excluded; no smaller room/full three-exception minimum.

Detailed report: `three-triples/fan-findings-2-1.md`. Frozen94-input manifest: `fan-proof-inputs-2-1.json`. Fresh receipt: `fan-audit-2-1.json`. All Codex jobs stopped; independent peer check pending.

**Next move:** split the18 residual branches at central cell(1,1), including absence.


## Double central-fan refinement and common-ray diagnostic

[done] The18 prior residual families refine into1,026 complete second-cell masks. Fresh audit excludes1,002, closes four first-fan families, and leaves24 feasible-after-cuts patterns across14 families. The physical half-turn exchanges them in12 pairs, verified from the triangle permutation. No additional outside set or whole placement closes: cumulative102/105 outside sets and seven of ten placements excluded remain unchanged. The unrestricted parent remains feasible.

The mechanism probe samples18 distinct rooms and tests61 directions/1,098 exact traces. Within this catalogue, an exact set-cover solve requires15 directions; no universal few-ray lemma follows. Five selected directions supply9 of129 new search witnesses, with120 using fallback. Audit verifies147 total new illuminated configurations and292 unique new guards,8 mutations/8 corrupt checks; longest new path28 reflections. An internal CP-SAT duplicate-column presolve assertion occurred at a saved discovery checkpoint; resume and fresh audit disable presolve without changing constraints. All checks pass and all jobs stop.

Claude now independently confirms the earlier(3,1),(3,2),(4,0) exclusions, plus(4,1),(5,0) by his checked path bound; his report notes no placement-specific positive control for(4,0). Newer(3,0)/(2,2)/(2,1) inputs are sent for independent replay. No smaller room or full three-exception minimum.

Report/figure: `three-triples/double-fan-findings-2-1.md`, `neck-patterns-2-1.png`; fresh receipt `double-fan-audit-2-1.json`; frozen102-input manifest `double-fan-proof-inputs-2-1.json` and supplementary symmetry manifest `neck-pattern-proof-inputs-2-1.json`.

**Next move:** seek a geometric illumination argument for the12 necessary neck types using the remaining wall/exception budget. The hoped-for common-ray shortcut remains unproved.


## Exceptional-state bound and a common midpoint-path candidate

[done] A local budget/connectivity propagator preserves422 valid saved/half-turned room controls across all12 neck types.17,440 local fan masks,200 exhaustive budget fixtures and200 exhaustive connectivity fixtures pass audit. Types8–10 force one additional detour triangle, but no universal illumination conclusion follows from the local propagation.

A derived elementary lemma bounds exceptional-vertex visits of a first-arrival ray by K=rJ+(r/2)S, where J counts interior B/C exceptions, S smooth-boundary B/C exceptions, and r=|D4*d|. Hence K<=24 with three exceptions. Primitive unfolding time is twice the encounter count. Canonical grid-line crossings then give a reflection bound2K*(|p|+|q|+max(|p|,|q|)) for each fixed primitive direction. The implementation decides that direction without an arbitrary bounce cutoff. Primitive directions remain infinite; this is not an all-direction darkness decision or a new room exclusion. Independent peer verification of the derivation is pending.

All147 saved rooms now have exact paths with one exceptional encounter at their optical midpoint, including104 samples spanning all12 current neck types.122 original rays already had this property. A128-direction probe finds21 alternatives; a targeted component-bound16 pass finds the last four. Fresh independent triangle tracing replays all1,940 direction tests and25 alternative witnesses. The gate audit also checks490 affine edges/four parity classes,64 point-group products,147 original positives,192 low-direction negatives,32 strict-dark directional controls and three rejected inputs. All pass. This is evidence from a selected positive population, not a universal single-pass theorem.

No new room geometry or exclusion guard is added. Twelve neck types remain; cumulative102/105 outside sets and7/10 placements excluded are unchanged. All jobs stopped. Proof/findings: `three-triples/neck-budget-findings-2-1.md`; frozen123-input manifest: `neck-budget-proof-inputs-2-1.json`; receipts `neck-budget-audit-2-1.json` and `gate-bound-audit-2-1.json`.

**Next move:** prove or disprove single-pass midpoint-gate sufficiency for every completion of the12 neck types under the wall/exception budget.


## First universal conditional midpoint cover

[done] The geometry-only parent now proves every completion of neck type 7 is illuminated by an exact one-exception midpoint ray. Its fixed signature is no outside cells, central masks 40 and 83. A finite catalogue of 1,066 sufficient triangle patterns covers this family; a fresh replay needs only a sufficient 37-pattern assumption core. All paths, independent closed-triangle coverage, twelve fixed positive controls, eight mutations and eight corrupt guards pass. The longest path has33 reflections. This is a computer-assisted conditional theorem; independent peer review and a formal UNSAT certificate remain unavailable/pending respectively.

The central-gate-only and forced-pair finite catalogues remain inconclusive. The successful core uses variable third-exception locations. One canonical family and its mark-exchange partner close:24 raw/12 canonical patterns become22/11. The whole target(2,1) placement remains open, with102/105 outside sets and7/10 whole placements excluded.

Of390 processed geometries,380 are genuinely new and10 revisited. The midpoint phase adds586 genuinely new guards (542 learned and44 alternative seed paths), bringing the composed parent to3,793 guards. Cumulative three-triples totals are2,045 new geometries and4,886 new guards. Counts and old input hashes are checked by `finalize_illumination_midpoint.py`; receipt `three-triples/midpoint-cover-dedup-2-1.json`.

[done] Claude independently confirms all seven earlier whole-placement exclusions. His23-wall survivor also has a verified12-reflection one-pass midpoint ray via(4,3), outside the previous sufficient catalogue. This separate peer check is not included in phase search totals.

[waiting on Claude] New conditional theorem/core review, plus prior fan/neck/gate derivations. Frozen137-input manifest: `three-triples/midpoint-cover-proof-inputs-2-1.json`. Full report: `three-triples/midpoint-cover-findings-2-1.md`.

**Next move:** a bounded sufficient-cover extension over the eleven remaining neck types, seeded by the peer survivor, with separate outputs and fresh audits.


## Midpoint extension closes seven of twelve residual neck types

[done] The fresh geometry-only audit proves universal one-pass midpoint illumination for types5,7,9,10,12. New sufficient cores have147,91,91,105 guards for types5,9,10,12, respectively; the original type7 core has37. Fresh core-only replays and positive controls pass; none of these subsets is claimed minimum. The2,598-pattern catalogue includes1,066 inherited conditions, two peer seeds, and1,530 learned conditions. All765 recorded positive geometries and1,530 learned paths/guards pass exact checks and independent closed-triangle coverage; twelve fixed positive controls and8 mutation/8 corrupt-guard checks pass. New rays use at most24 reflections; inherited rays reach33. Both peer guards pass independent coverage checks.

Composition with historical cuts gives5,063 unique half-turn-closed guards and additionally excludes types4 and11. Thus7/12 canonical neck types (14 raw patterns) are excluded;5 types (10 raw patterns) remain:1,2,3,6,8. The standalone midpoint theorem still has seven open types; the smaller-dark-room search only needs the five that survive composition. All three remaining outside sets and the unrestricted parent remain feasible. Counts102/105 outside sets and7/10 whole placements excluded stay unchanged; no smaller dark room or full three-exception minimum.

Cross-phase reconciliation finds746 genuinely new geometries among765 (19 revisits),1,268 new learned guards, and2 new peer guards. Cumulative three-triples totals become2,791 new geometries and6,156 new guards. The separate peer geometry is not added to search-geometry totals. All Codex jobs finished.

[waiting on Claude] New neck implications/composition review. The151-input `three-triples/midpoint-extension-proof-inputs-2-1.json` freezes the new scripts, results, findings and original137-input dependencies. Earlier frozen inputs remain unchanged. Full report: `three-triples/midpoint-extension-findings-2-1.md`.

**Next move:** focus the midpoint argument on the five live types, especially type8, the only surviving canonical outside-cell case. Avoid further universal-only work on already excluded types4 and11.


## Type 8 and type 6 reduce the remaining placement to three neck types

[done] Both new searches exhausted and fresh audits passed. Type8 adds70 new geometries/140 guards; type6 adds26 new geometries/52 guards. All96 are new against frozen earlier inputs. Exact paths, independent triangle coverage, positive geometry controls and mutation/corrupt-guard checks pass. The composed parent has5,255 unique guards and remains feasible.

Type8 closes both remaining nonempty outside-cell sets;104/105 complete outside sets are excluded. Type6 leaves three canonical necks1,2,3, all with empty outside set and first central mask12 (second masks82,83,210). Nine of12 canonical necks are excluded. Their geometry-only midpoint parents remain feasible, so these two exclusions require historical positive-ray cuts. Whole-placement count stays7/10; no smaller dark room or full three-exception minimum.

Cumulative three-triples totals:2,887 new geometries/6,348 new guards. Frozen inputs: `three-triples/type8-proof-inputs-2-1.json` (159 paths), `three-triples/type6-proof-inputs-2-1.json` (168 paths). Reports: `type8-findings-2-1.md` and `type6-findings-2-1.md` in that directory.

[waiting on Claude] Neutral reproduction commands for both phases posted on the board. Claude has independently confirmed the original type7 core and seven prior whole-placement exclusions; the new phase checks remain pending.

**Next move:** search the shared empty-outside / first-mask12 parent, then require a fresh unrestricted-parent replay before claiming closure of placement(2,1).


## Eighth placement excluded by complete partition composition

[done] Placement(2,1), physical displacement(4,2), is excluded below24 walls for the canonical simple two-A-star / exactly-three-B/C-exception family. The shared first-mask12 search exhausts after180 new geometries/360 new sufficient ray guards. Fresh exact paths, independent triangle coverage, three positive controls,8 mutations and8 corrupt-guard checks pass; all12 canonical necks replay INFEASIBLE. The composed parent has5,615 unique half-turn-closed guards.

The unsplit parent solve returns UNKNOWN at60 seconds. Exclusion instead follows from the checked exhaustive certificate hierarchy:105 cell sets (100 already excluded),285 first-fan branches (267 excluded),1,026 second-fan branches (1,002 excluded), then24 raw patterns paired into the12 freshly excluded neck types. `audit_illumination_partition_closure.py` checks all branch keys, independent57-mask lists, source hashes/provenance, symmetry and guard inclusion. All earlier branch conditions remain valid with the new positive-ray cuts. Every leaf is excluded; no UNKNOWN is treated as proof. The geometry-only midpoint parent remains feasible.

Whole-placement count is now8/10. Only(1,1),(2,0) remain; the full three-exception minimum remains open. All180 phase geometries are new against frozen inputs, bringing cumulative three-triples totals to3,067 new geometries/6,708 new guards. This does not establish a general-polygon bound or export a formal UNSAT proof.

[waiting on Claude] New179-input manifest `three-triples/mask12-proof-inputs-2-1.json` freezes paths, audits and the complete composition checker. Neutral independent-review instructions are on the board. Earlier manifests and peer files are untouched. Report: `three-triples/mask12-findings-2-1.md`.

[done] Next-case saved-path comparison verifies37 paths for(1,1) and39 for(2,0). Single-event midpoint witnesses account for34/37 and29/39, respectively. This is sample evidence only; multi-event witnesses do not preclude alternative single-event paths. Receipt: `three-triples/remaining-gates.json`. All Codex jobs finished.

**Next move:** target(1,1). Try exact alternative single-event paths for its three saved multi-event rooms, then formulate a bounded midpoint-cover parent.


## Placement(1,1): one-pass samples and a complete two-family hub reduction

[done] All three saved multi-event samples have alternative single-event midpoint rays; all37 original samples now have one-pass witnesses. A bounded complete-parent run adds110 illuminated configurations; fresh exact rays, independent triangle coverage, three positive controls,8 mutations and8 corrupt-guard checks pass.96 geometries are genuinely new,14 revisited. The588-pattern midpoint catalogue remains feasible as a geometry-only parent.

[done] Historical reconciliation corrected the initial parent: it had2,001 original cuts but omitted a626-cut later extension.112 of448 phase guards were already in that extension, so only336 are globally new. All514 restored missing guards received fresh exact and coverage checks. The merged2,963-guard parent, with the previously audited2,530-set connected-cell table, remains feasible. Cumulative three-triples totals now3,163 new geometries/7,044 new guards. The eight-placement exclusion count is unchanged.

[done] The two full marked stars meet at physical(1,1), forcing four of eight hub triangles. Independent adjacency and sector enumeration agree on seven possible masks. Full hub255 is always illuminated by the direct zero-reflection ray; a positive full-hub control and sufficient-condition implication pass. The other six masks form exactly two symmetry families: two six-triangle masks175/243, and four seven-triangle masks191/239/247/251. All six fixed-mask models replay feasible. These are local necessary shapes, not six room outlines or dark examples.

[waiting on Claude] New193-input manifest `three-triples/midpoint-proof-inputs-1-1.json`; neutral check commands posted, with required `<root>/.context/` copy layout. Peer now independently confirms the earlier(2,1) midpoint extension, including all2,598 paths and four new standalone cores; newer eighth-placement phases remain pending. Peer files and all earlier frozen inputs untouched. All Codex jobs finished.

**Next move:** target the denser seven-triangle hub family, canonical mask191. Reconstruct the merged parent from original2,001 + current448 + restored514 guards (2,963 total), apply the audited connected-cell table, then attempt a bounded exact one-pass cover. Do not restart from the incomplete2,001-cut base alone. No smaller dark construction or full three-exception minimum established.


## Seven-hub refinement excludes five of seven tip fans

[done] Canonical hub191 raw search adds50 genuinely new geometries/200 sufficient guards, freshly audited with independent triangle coverage and mutation/corrupt controls. Family remains feasible. The absent hub triangle has A tip physical(2,0); hub191 fixes one present and one adjacent absent star bit. Independent cycle/sector enumeration gives exactly seven compatible tip masks4,5,7,23,87,215,247, containing1–7 triangles.

[done] Bounded complete seven-fan synthesis adds24 new geometries/96 guards. Fresh exact paths, coverage, three fixed controls,8 mutations/8 corrupt checks and all seven replays pass. Five tip branches close:7,23,87,215,247. The last two are geometrically impossible without rays; the first three need historical cuts and remain feasible with the midpoint-only catalogue. All four mark stabilizers preserve the3,259-guard parent. Only tip masks4,5 remain, differing by one bit; whole hub191 and placement(1,1) remain feasible. Global counts8/10 placements,3,237 new geometries/7,340 guards.

[done] Claude independently confirms the complete(2,1) exclusion:6,125 exact witnesses,5,615 independently rebuilt cuts, all105 outside sets excluded and monolithic INFEASIBLE in his own stronger model. All eight whole-placement exclusions now independently confirmed. New(1,1) phases await his review.

[waiting on Claude] Frozen204-input raw-hub certificate `three-triples/hub7-proof-inputs-1-1.json` and212-input fan certificate `hub7-fan-proof-inputs-1-1.json`; neutral nested-layout commands on the board. Older inputs and peer files untouched.

**Next move:** the union of tip masks4,5 fixes every tip bit except bit0. Test this residual parent under all3,259 guards and audit the full seven-fan composition.


## Two residual tip patterns differ by one fixed C exception

[done] The residual union of masks4,5 adds30 genuinely new geometries/120 sufficient one-pass guards; fresh exact paths, independent coverage, three fixed positive controls,8 mutations/8 corrupt checks pass. Maximum new reflections22. The3,379-guard parent is closed under all four mark stabilizers. Both residuals remain feasible; the prior five fan exclusions replay intact. Whole seven-hub and whole(1,1) remain open; counts stay8/10 independently confirmed whole placements. Cumulative three-triples totals3,267 new geometries/7,460 new guards.

[done] Exact incident-triangle geometry shows why the two residuals differ: at C(1,0), mask4 fixes3 of4 right triangles, an ordinary270-degree concave boundary corner. Mask5 adds the fourth, forcing an interior C exceptional vertex and leaving only two of the three B/C exceptions unfixed. Independent sector and right-angle assertions pass without a solver. This does not force rays to use that C point or prove illumination.

[waiting on Claude] Frozen223-input certificate `three-triples/hub7-residual-proof-inputs-1-1.json` includes the current fresh audit and `tip-gate-1-1.json`; neutral nested-layout commands are on the board. Earlier inputs and peer files unchanged. All Codex jobs finished. Across this continuation104 new geometries and416 new guards; five of seven tip branches excluded, not an entire placement.

**Next move:** target tip5 with fixed interior C(1,0); project the two remaining typed exceptional vertices under the3,379-guard parent. Keep tip4 and the six-hub family as separate open branches. Full three-exception minimum remains unproved.


## Forced-C case closes: six of seven tip fans excluded

[done] Local geometry fixes both interior C(1,0) and smooth C(2,1) under hub191/tip5. The third exception has exactly six typed possibilities after3,379 historical-ray guards. Projection exhausts, with144 logical partition checks, positive rooms/controls and a fresh complementary-parent exclusion. This is complete, not a capped sample.

[done] All six cases exhaust after8 illuminated configurations/32 sufficient one-pass guards. Fresh audit: all six cases, the complementary parent and the unsplit tip5 parent INFEASIBLE;6 fixed positives and8 mutation/8 corrupt checks pass, new rays at most21 reflections.3 geometries genuinely new,5 revisit projection controls. The3,411-guard parent retains all four mark symmetries. Geometry-only midpoint parent remains feasible, so historical cuts are essential to this exclusion.

Six of seven hub191 tip fans are now closed:5,7,23,87,215,247. Only one-triangle tip4 remains open within this hub family; the six-triangle hub family remains open separately. Whole count8/10 independently confirmed; cumulative3,270 new geometries/7,492 new guards. No smaller dark room or full three-exception minimum.

[waiting on Claude] Frozen231-input pair-partition and239-input case-cover manifests; neutral nested-layout commands posted. Earlier certificates/peer files untouched.

**Next move:** project the two free typed exceptions in tip4 with smooth C(2,1) fixed, ordinary concave C(1,0), and all3,411 guards.


## Last thin-tip projection retains an open remainder

[done] After the verified tip5 exclusion, tip4 is the sole remaining fan within hub191. A finite local check confirms smooth C(2,1) is fixed and C(1,0) is ordinary concave. Two free exceptional vertices remain. Bounded projection lists25 typed pairs; fresh audit accepts physical/model controls and1,012 logical disjointness/complement assignments. The unlisted remainder is feasible (witness smooth(3,1),smooth(5,1)), so projection is incomplete. The25 listed branches plus their explicit complement form the complete partition.

No new illumination cuts or placement exclusion. Whole count8/10 independently confirmed;3,411 current guards, cumulative3,270 new geometries/7,492 new guards. The six-hub family stays separately open. New247-input certificate `three-triples/thin-tip-pairs-proof-inputs-1-1.json` and prior239-input six-case exclusion frozen; neutral peer commands posted. All Codex jobs finished.

**Next move:** targeted ray covers of25 known pair branches AND the explicit remainder, without treating capped enumeration as complete.


## Thin-tip ray phases:24 of25 listed pairs excluded

[done] Fresh replay excludes24 of25 listed typed pairs under hub191/tip4. The sole listed survivor fixes interior C(1,2) and interior C(2,3), in addition to the forced smooth C(2,1). The unlisted-pair complement also remains feasible. Both are retained explicitly. Tip4, the seven-hub family, and placement(1,1) remain open; the six-hub family is separate. Whole-placement count stays8/10 independently confirmed.

[done] This extension adds27 verified one-pass witnesses/108 sufficient guards:26 geometries new relative to the256-input lineage, one revisit. Fresh audit accepts three pre-extension positive controls, eight mutations, eight corrupt-guard checks, and all four mark stabilizers. Maximum new reflections20. Parent now3867 unique guards.

Across both thin-tip ray phases:114 verified configurations,100 genuinely new geometries,14 revisits,456 new sufficient guards. Cumulative three-triples totals3370 new geometries/7948 new guards. These are computer-assisted exclusions under the historical ray cuts, not geometry-only universal midpoint lemmas or formal UNSAT certificates.

[done] Claude independently confirmed the preceding247-input thin-tip projection and3411 guards. The256-input first ray cover and newest continuation have been handed off neutrally; their independent review remains pending. Claude has been offered disjoint discovery at placement(2,0), while Codex retains(1,1). No Claude-owned files changed.

[waiting on Claude] Verify thin-tip-extension-proof-inputs-1-1.json, preserving the nested root/.context layout, with audit_illumination_thin_tip_extension.py. This manifest freezes all inputs and receipts.

**Next move:** analyze the interior-C survivor pair geometrically, and refine or search the explicit unlisted complement. Any complete tip4 exclusion must close both. No smaller dark room or full three-exception minimum is established. All Codex jobs finished.


# All originally listed pairs closed; complete remainder classification

[done] All25 originally listed typed pairs under hub191/tip4 now replay INFEASIBLE with3987 guards. The final interior-C pair was refined into five complete local fans; one new11-reflection ray at direction(4,11), together with historical conditions, closes the last fan. Independent local angular-slot/triangle-adjacency checks agree on34600 masks. The pair forces22 present/8 absent triangles; local and solver positive controls pass.

[done] The unlisted complement is now split completely by the number of free interior exceptional vertices:0,1,2. Each exceptional vertex has type1(smooth boundary) or type2(interior), and the fixed gate C(2,1) has type1. The four assignments(1,1),(1,2),(2,1),(2,2) have unique counts0,1,1,2 and total defect credits3,4,4,5. This gives an exact exhaustive logical partition. The solver-only complementary query remains UNKNOWN; it is not used as an infeasibility proof. The initial audit stopped on that query; its traceback is retained in the log, followed by the corrected audit and PASS receipt.

[done] Remainder phase:26 genuinely new geometries/104 sufficient one-pass guards; fresh counts0/1/2 all feasible. Six positives include a fixed room in each count group;8 mutations/8 corrupt checks and all four mark stabilizers pass. Maximum17 new reflections. All25 earlier pairs freshly replay INFEASIBLE; unsplit tip4 remains feasible.

Across this continuation:30 verified configurations,29 genuinely new geometries,1 revisit,120 new sufficient guards. Cumulative three-triples totals3399 new geometries/8068 guards; current parent3987 unique guards. Interior-pair/fan certificate276 inputs is frozen separately. Latest remainder certificate includes all dependencies and receipts. New phase independent review pending.

[waiting on Claude] Verify remainder-types-proof-inputs-1-1.json in a nested root/.context copy with audit_illumination_remainder_types.py; independently derive the count partition and check sufficient tile conditions. Claude is actively running the disjoint(2,0) cut loop in his own directory. His files remain untouched.

Whole placements remain8/10 independently excluded. Tip4 and the six-hub family at(1,1) remain open; placement(2,0) remains open pending Claude's ongoing search. No smaller dark room or full three-exception minimum. All Codex jobs finished.

**Next move:** inspect the surviving zero-interior group, where all three exceptional vertices lie on smooth boundary segments, and choose a complete geometric split of their boundary arrangement. Retain the one- and two-interior groups explicitly.


## Three-exception family completed (2026-10-30)

[done] All ten two-full-A-star placements are excluded below24 walls. Final audits check7725 exact paths, rebuilding5710 and4671 sufficient conditions at(2,0)/(1,1). All190/657 symmetry groups are INFEASIBLE, with explicit maps covering699/2530 outside-cell cases. The earlier I=3 exclusion and W>=6+6I-2k bound for I>=4 complete the exactly-three-exception branch. Prior results cover k<=2; the strict24-wall control attains the bound. A smaller simple room in this tiling with interior A marks needs at least four B/C exceptions. No smaller dark construction or general-polygon result was obtained.

[done] Allowing multi-event paths improved the finite cover:457 of2299 new(2,0) witnesses use more than one exceptional event. The saved single-event-only cover remains feasible in both difficult subcases. This limits that finite certificate; it does not prove another single-event path impossible.

[done] Final proof uses complete partition/symmetry composition, passing independent physical/condition checks and positive controls. UNKNOWNs and interrupted experimental runners are not proofs. Scope, frozen manifests and reproduction: `three-triples/three-exception-complete.md`.
