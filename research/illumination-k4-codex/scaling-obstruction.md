# The exception count needs a scale normalization

[done] Theory correction for joint part A, 2026-10-31. No rays were traced. The numerical controls are exact geometric subdivisions of the already established 24-wall control; their darkness follows by similarity, not a new optical test.

## Proposition

Let P be a canonical simple room with distinct interior A marks and W maximal walls. For every positive integer M, its dilation M P is again a finite union of the fixed unit canonical triangles, has the same W, and has the corresponding pair dark if and only if the original pair is dark. The number k of transparent B/C points in the fixed unit-grid presentation is unbounded as M grows.

Proof: canonical wall lines have equations x integer, y integer, x-y even integer, or x+y even integer. Integer dilation preserves that arrangement's line types, and maps even-even marks to even-even marks. Thus each dilated polygon can be subdivided into whole unit canonical triangles. Similarities preserve reflected paths and genuine corners in both directions. Every polygon of positive area contains an open disk, whose dilations contain quadratically many interior B/C lattice points. Every such point is a transparent interior vertex in the fine presentation. Hence k tends to infinity along an integer-dilation sequence while W and darkness stay fixed.

## Exact control

The existing simple 24-wall room gives these unit-grid presentations:

| Dilation M | W | N | I | J | s_N | k |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 24 | 27 | 2 | 0 | 0 | 0 |
| 2 | 24 | 108 | 2 | 28 | 25 | 53 |
| 3 | 24 | 243 | 21 | 64 | 34 | 98 |
| 4 | 24 | 432 | 30 | 137 | 50 | 187 |

scaling-check.py constructs subdivisions using exact integer centroid-side tests, independently checks the resulting simple geometry and count identities, and verifies N(M)=M²N(1) and fixed wall count. It invokes no ray tracer or orbit decider.

## Consequence for part A

There is no finite k bound for dark canonical presentations at W<=24. For W<=23, a finite k bound without a normalization would be logically as strong as nonexistence: if one counterexample existed, dilations would violate every finite k bound. Thus the intended finite-search reduction cannot first assume an absolute presentation-level bound and later discover whether counterexamples exist.

A useful weaker theorem would bound k for a selected primitive presentation, or show that every sub24 dark room is similar to a presentation with bounded k. The admissible normalization must preserve the canonical triangle arrangement, the distinct interior A marks, and the wall count. A gcd/coarsest-grid convention is a candidate definition, not a proved finiteness theorem. A bound on primitive complexity remains open.

## Consequence for the R budget

The identities R=4(N-W+2), R>=16+8J+4s_N, and N>=W+6 remain valid necessary conditions for each presentation. However R counts regular vertices of a chosen square subdivision; it is not invariant under similarity plus finer subdivision. Dilation changes the period lattice from 2Z² to 2MZ² in unit coordinates and introduces more regular grid vertices on a homothetic copy of the same surface. Therefore a larger R alone is not evidence of a new darkness mechanism or a new marked surface up to similarity.

This does not invalidate the earlier refolding obstruction: that proof fixes the intrinsic period normalization, the marked orbits, the affine action, and its corner mass. The wall obstruction comes from that argument, not from the unit-grid R threshold by itself.

## Reproduce and independent check

Run `.context/illumination-venv/bin/python -B .context/illumination-k4-codex/scaling-check.py` in a separate copy. Independently review the arrangement/similarity argument and the need for primitive normalization. No ray work is needed.

**Next move:** specify the primitive presentation used by part A before trying to bound k; keep the completed k=4,...,12 tables as presentation-specific eligibility results.
