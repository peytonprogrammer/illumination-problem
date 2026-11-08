# Candidate uniform support of every vertical-only failure

Codex01a18403. Parent theorem combining new hand reductions and exact finite certificates. Independent review of the new reductions and full positive certificates remains required. This is not a theorem that every room illuminates.

## Statement

Normalize d=g=1. Fix positive depths a,b and arbitrary 0<s,t<=1. If no compatible vertical-only chart connects the actual marks (s,-a),(t,1+b), then the depth pair lies on one of these10 lines:

    a=1, b=1,
    b=a+1, a=b+1,
    b=2a+1, a=2b+1,
    b=2a+2, a=2b+2,
    b=3a+1, a=3b+1,

or belongs to the following11-point set:

    (1/2,1/2),
    (1/5,3/5), (3/5,1/5),
    (3,5), (5,3),
    (1/3,7/3), (7/3,1/3),
    (1/7,3/7), (3/7,1/7),
    (5,8), (8,5).

This is a NECESSARY support condition for vertical-only failure, independent of endpoint rationality or any denominator bound. It does not say every endpoint placement fails at a listed depth, nor that these are dark pairs. The original room can still use endpoint-cap and middle-reflection mechanisms. Existing accepted reductions cover many listed placements.

## Uniform reductions before computation

If either a or b is irrational, the previously independently accepted phase-lines theorem gives a connection for every actual horizontal endpoint pair. Thus a vertical-only failure has rational phases alpha=a/(a+b+1), beta=(a+1)/(a+b+1). Write (alpha,beta)=(A/q,C/q) with primitive joint denominator q.

If no relation of l1 norm<=4 holds and q>100, lattice-sampling.md guarantees even the common chart for every endpoint offset. Therefore no such failure occurs. All remaining phases without a short relation have q<=100.

If a short relation holds, normalize to one of the30primitive triples listed in short-line-margin.json. Twenty of these have a closed-endpoint-square eta=1/8 circle margin. Their finite rational orbits therefore hit a compatible box whenever q exceeds the row's safe cutoff16(|m|+|n|)<=64. The other10 correspond precisely to the10critical lines in the statement. Membership in several relation lines causes no gap: a point on any critical line is already in the support, and a point outside them satisfies the finite cutoff of any good relation it has.

Thus the remaining positive verification problem is FINITE: (i) all primitive phases with q<=100 having no short relation; (ii) all primitive phases on a good short line and outside every critical line, with q no greater than the smallest available certified line cutoff.

## Exact continuous finite certificates

The frozen helper finite-short-cover.py generates every compatible chart at each M=0,...,q-1, u=0or2, epsilon=+/-1. It enumerates the integer portal residue translates that can meet [0,1]^2. Each clause is the intersection of four strict affine guards in s,t.

For each phase, begin with the closed unit endpoint square. Remove the OPEN region of each successful chart, preserving the exact complement as closed convex polygons, segments and points. Guard-boundary points remain in the complement unless a different strictly successful chart covers them. Pieces confined to s=0 or t=0 are discarded, because actual marks have s,t>0; every other retained convex piece has an admissible barycenter. Arithmetic uses Fraction, with no numeric tolerances or endpoint grid. Clipping and source generation must be independently audited, not trusted from counts alone.

exceptional-phase-support.py/json exhausts115408primitive phase pairs in group(i), through q=100. Exactly two phase pairs retain a nonempty admissible endpoint complement. Their depths are (5,8),(8,5).

short-line-finite.py/json exhausts4332primitive phase pairs in group(ii), through the applicable cutoff no greater than64. Exactly nine retain an admissible endpoint complement: the first nine points in the statement. The classifier excludes phases on ANY critical line, not merely a selected good line.

Both receipts retain every final closed failure piece and an exact admissible representative, rechecked over the entire q target-image period. Their positive coverage claims rely on the exhaustive strict-complement algorithm and the analytic cutoffs; no sampling inference is used. Every original effort completed before its persisted840-second aggregate deadline.

The counts are reproducibility metadata. They do not themselves prove the exclusions. Required independent review includes source generation, primitive phase enumeration, strict boundaries, degenerate pieces, mathematical denominator cutoffs and exact replay or a distinct complete verification.

## How this connects to the four endpoint-cap sheets

For an actual room the four effective depth pairs are

    (a,b), (A,b), (a,B), (A,B),
    A=2h_--a>a, B=2h_+-b>b.

The accepted cap-corner-removal lemma shows that any strictly successful portal chart on any of these sheets yields an actual legal connection. Consequently a room not covered by those four charts would determine a strict NE rectangle whose four vertices lie in the support just listed, with endpoint placement simultaneously in their genuine failure complements.

The support condition greatly reduces the geometry but does not close that rectangle problem. Also, the accepted outer-leg-transfer lemma closes a room whenever ANY one of its four effective pairs is equal-depth, even when that sheet needs the three-middle-reflection equal-depth construction rather than a vertical-only chart.

critical-rectangles.py/json classifies only the rectangle-support assignments on the10lines; finite-point mixed assignments and optical closure remain separate. Its rank3families are potential supports, not proven failed rooms. The full room goal remains incomplete until every such possibility is optically closed or a rigorously dark counterexample is independently established.
