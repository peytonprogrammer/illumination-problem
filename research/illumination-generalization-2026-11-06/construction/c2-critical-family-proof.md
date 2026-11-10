# All even members of the c2 four-corner family illuminate

A41 candidate complete family theorem, pending independent review. This uses six prescribed exact base certificates and a guarded actual two-gap insertion proof. It covers all allowed parameters in this family, not all c2 combs.

## The family and endpoints

For every EVEN integer h>=6, let P_h be the union of

    core [0,2] x [0,2h+4],
    right teeth [2,3] x [1,3] and [2,3] x [2h+1,2h+3],
    left teeth [-1,0] x [h,h+2] and [-1,0] x [h+4,h+6].

Use actual S_h=(2,2), T_h=(2,2h+2). Claim: EVERY such pair illuminates by a finite actual corner-avoiding specular trajectory.

All four teeth are nonflush, same-side gaps are positive and the core connects their mouths. The two left teeth also lie strictly between the selected right bands for h>=6. The boundary is one strictly simple orthogonal disk with exactly20 maximal straight walls, area4h+16 and no slits or self-contact. All coordinates are integral, so these are canonical45 rooms. Both marks are actual interior seam midpoints, with all four incident square sectors present. Indeed they are the ONLY actual interior even-even A points: the strict core has no even abscissa, left seam tooth midpoints have odd ordinates because h is even, unit-width teeth have no other interior integer x coordinate, and the right seam contributes precisely S_h,T_h.

The four simple turning levels are h,h+2,h+2,h+4, all opposite mouth endpoints. The simple D0 far twists are resonant. Neither failure establishes darkness; the paths below use genuine repeated core/tooth excursions and end-wall reflections.

## Six exact base paths

The exact unit-cell geometry and independent physical Fraction tracer in c2-critical-family-check.py construct the first successful path in a prescribed finite q1/3 direction pack for each of the SIX residues. The search stops on each first verified path and has no replacement inputs. Every base path is stored with its exact rational contacts and wall indices in c2-critical-family-check.json.

| Base h | Actual initial velocity | Smooth reflections | All physical wall/leg guards |
| --- | --- | ---: | ---: |
| 6 | (-7,-3) | 26 | 540 |
| 8 | (-7,-3) | 25 | 520 |
| 10 | (-1,3) | 4 | 100 |
| 12 | (-1,3) | 3 | 80 |
| 14 | (7,-3) | 40 | 820 |
| 16 | (-2,-3) | 12 | 260 |

All six have primitive absolute vertical component q=3. They total110 actual smooth reflections and2320 all-wall/leg guards. Each finite leg excludes every earlier boundary event, every wall contact has exactly one relative-interior wall parameter, the axial component flip is the exact specular law, and the actual target is reached before any later wall. Geometry and source/target unit-star checks are exact. The h6 path was separately obtained by the completed A40 single-room search; its inclusion here is a base dependency, not a second assertion of independent discovery.

These finite certificates establish ONLY their base rooms until the next transfer argument is proved. The general theorem is not inferred by sampling.

## Two actual bare-core insertions

Fix one base h0 in {6,8,10,12,14,16} and its already verified velocity with absolute components (p,3), p in {1,2,7}. Two open vertical gaps have the actual constant cross-section0<x<2:

    gap1: 3<y<h0,
    gap2: h0+6<y<2h0+1.

Both have positive length, including the minimal second gap at h0=6. Choose a rational horizontal cut in each gap, away from the finitely many reflection heights of the base path. Every reference crossing of these cuts is therefore transverse and strictly between the two actual sidewalls. The cuts are auxiliary interfaces, never reflecting mirrors.

Increase BOTH gap lengths by12n, n any nonnegative integer. Equivalently insert a rectangle of width2 and height12n at each cut, translating the middle cap by12n and the upper cap by24n. The resulting polygon is EXACTLY P_(h0+12n): the left-tooth bands shift by12n, the upper right tooth, actual target and global ceiling by24n, and the lower right tooth and source remain fixed. Cut locations do not affect this rank-coordinate result because neither gap contains any actual vertex or endpoint. No new corner is created at a cut; its sidewalls extend collinearly.

Consider any crossing of an inserted rectangle by the reference path, upward OR downward. In that actual width2 rectangle, with the same velocity magnitudes, the developed horizontal displacement through the added height is

    p*(12n)/3 = 4pn.

The horizontal rectangular billiard has full position-and-velocity period4. Thus after the added transit it has EXACTLY its original transverse x coordinate AND horizontal velocity sign. The vertical velocity sign is unchanged. All added sidewall reflections are at genuine actual vertical walls, strictly between the two ports. None can hit a corner because the entrance point is strict and the developed displacement is an exact full period, giving a strict exit as well.

Continue the original chamber trace, translated into its new cap. Perform this substitution at EVERY crossing, including returns and multiple visits to either gap. The matching does not assume that a gap is crossed once or that the vertical motion is monotone. No reflection word is guessed for the newly inserted transit; ordinary rectangular folding explicitly supplies it.

One may insert the lower gap first and then the upper gap. All contacts newly created in the first inserted rectangle lie below the translated second cut. Hence no new coincident event is forced at that cut, and its strict original transverse phases are retained. The second insertion satisfies the same exact period condition. The two existing cuts can therefore be chosen once for the finite base path and used for all n.

All other walls and contacts belong to unchanged, translated cap pieces. Both left far-end contacts and any repeated upper-tooth visits remain ordinary actual mirrors. The global floor and ceiling are actual cap walls, translated only where appropriate; none is replaced by an artificial cap. The original actual S and T lie outside the inserted open rectangles. Therefore no earlier actual target is created within a strip, while the old first-target ordering in the cap pieces is preserved. The resulting finite trace reaches ACTUAL T_(h0+12n), with all original and new contacts corner avoiding.

Each fixed n adds finitely many reflections at each of finitely many crossings. The construction is therefore finite for every parameter, though its reflection count need not be uniformly bounded.

## Exhaustion of every allowed h

Every even integer h>=6 has a UNIQUE representation

    h=h0+12n,
    h0 in {6,8,10,12,14,16}, n>=0 integer.

Use its corresponding base certificate and the preceding exact actual insertion. This proves illumination for the ENTIRE family, including every small member. No finite-prefix, residue or large-gap exception remains within this one-parameter class.

The larger c2 thin-comb class still permits arbitrary placements and many independent gaps not constrained to this displayed family. It is not covered by these six residues. Wider teeth, c1 rooms and arbitrary canonical45 disks are also outside this theorem. There is no dark counterexample, universal22-wall lower bound. Full family acceptance requires independent validation of the exact bases AND the all-n actual transfer, not just receipt of six positive search results.
