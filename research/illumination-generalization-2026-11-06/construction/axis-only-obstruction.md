# Exact limitation of the two-axis mechanism

Candidate hand lemma, Codex01a18403. Independent peer review pending. This rules out a proposed universal path construction; it does not give a dark pair.

## Missing implication and bounded criterion

Question: can the outer-left/bottom-axis construction alone cover arbitrary nested staircases after dropping the bounding-triangle inequalities? Success means either a proof of that extension or an exact structural obstruction. The strongest objection is that another axis-reflection word, possibly with repeated reflections, might have been omitted.

## Characterization for the restricted optical mechanism

Let P be a strictly decreasing nested staircase as in nested-window-proof.md, outer width A and height H. Every real interior pair connects using only reflections on x=0 and y=0 if and only if P contains the bounding triangle Delta with vertices (0,0),(A,0),(0,H).

Sufficiency is the elementary folded-segment construction in staircase-axis-triangle-proof.md: use the line from (s,u) to (-t,-v), fold by absolute values, and use the direct segment in the collinear case. Its middle leg stays in Delta; its two outer legs stay componentwise below S and T. The original source remains frozen and unreviewed; this supplement does not promote it to accepted status.

For necessity, suppose a bounding-triangle inequality fails at the j-th narrowing: w_j < A(1-y_j/H). Choose a height y* strictly inside band j, slightly above y_j, still satisfying w_j < A(1-y*/H). Then p*=(A(1-y*/H),y*) is strictly outside P, with positive distance from P.

For sufficiently small epsilon>0 take actual interior marks

    S_epsilon=(A-epsilon,epsilon),
    T_epsilon=(epsilon,H-epsilon).

They lie in the bottom and top bands. Any legal path reflecting only on the two axes hits each axis at most once: after an x=0 hit, horizontal velocity points right and cannot reverse again without some other vertical wall; likewise for y=0. Thus unfolding any such path yields one of exactly four straight segments to (sigma*epsilon,tau*(H-epsilon)), sigma,tau in {+1,-1}. Its physical fold is

    gamma_(sigma,tau,epsilon)(q)
      = (abs((1-q)(A-epsilon)+q*sigma*epsilon),
         abs((1-q)*epsilon+q*tau*(H-epsilon))).

All four converge uniformly as epsilon tends to0 to

    gamma_0(q)=(A(1-q),Hq).

For q*=y*/H this limit equals p*. The positive exterior distance implies all four folded paths leave P for all sufficiently small epsilon. This excludes EVERY possible axis-only word, including paths with zero or one reflection. It says nothing against a connection using a step, right, or top wall.

## Prescribed canonical45 ten-wall obstruction to this mechanism

Use the four nested rectangles with widths (40,12,8,4) and band heights (0,12,16,20,40). Take S=(38,2), T=(2,38). They are distinct actual interior A points. The room is a finite strictly simple orthogonal canonical45 disk with ten maximal walls. No size, k, or endpoint approximation is used.

For each of the four developed images (+/-2,+/-38), the midpoint of the folded segment has x in {18,20} and y in {18,20}. At either such height the actual room has x<=8. Every one of these four paths therefore exits P. Repeated-axis words are already excluded by the velocity argument, so this is an exact failure of the entire axis-only construction in the active lattice model.

The example is NOT dark: it has not been subjected to an all-path exclusion. The structural lesson is precise: on metrics failing triangle inclusion, any universal argument must sometimes use a non-axis wall. Combining axis-only paths with the tall-band sufficient conditions still leaves the earlier four-band complement open.

## Realignment

Proved by this hand argument, pending independent review: triangle inclusion is necessary for universal axis-only connectivity. Still open: arbitrary-metric four-band illumination, nonnested and diagonal-wall rooms, and the uncapped W<=21 theorem. No new discovery search, room enumeration, direction search, or implementation was required. Do not count this mechanism obstruction as an illumination exclusion or a lower-bound theorem.
