# Simultaneous short relations already occur in fully lit ten-wall rooms

The d173 necessary relations, even for both axes and all four independent choices of endpoint return, do not force a 22-wall lower bound. This persists with a unit gate clearance and the least common middle winding period. This result concerns the homogeneous relations. The translated gate tests carry additional information.

## Cap arithmetic for any band chain

Write A=Pa/(2w), B=Pb/(2V), C=Pc/w and E=Ph/V, where c,h are the endpoint band depths. Up to coordinate signs, the four rotations are (A,B), (C−A,B), (A,E−B), (C−A,E−B). If A,C are integers then (1,0) annihilates all four, regardless of B,E or the intermediate gates. More generally the reduced denominators of A and C−A bound the two pure source characters separately. This applies to every chain admitting the d173 charts, including every such chain at W≤20. Physical caps with openings still require an independent mirror-window check. Even granting the entire caps does not remove these characters.

## Both axes, simultaneously

Take the symmetric Ferrers staircase on the grid (0,1,2,3,N) in both coordinates, N any integer ≥5. Its widths are 1,2,3,N and its heights N−3,1,1,1. It is strictly simple and axis-normalized. Take S=(1/2,4), T=(4,1/2). They are distinct interior marks. Viewed from the narrow end on either axis the source depth is a=1, the narrow width is 1, and the top band depth is c=N−3. The least positive middle period is lcm(4,6)=12. Hence A=6 and C=12(N−3). In the opposite orientation exchange the endpoint labels. A signed common-side beam has δ=1. Thus a unit character survives for every choice, on both axes, at unbounded area. The same computation allows any two narrow-end depths in (0,N−3) that are multiples of 1/6, independently. Yet d170 proves the entire room lit: its two comparisons read 2≤2 and 6≤9. The mechanism is arithmetic locking of an endpoint under a shear that independently preserves the middle bands. It requires neither darkness nor an exceptional room size.

The outer lengths also vary independently. Replace the grid endpoint N by Nₓ on the horizontal axis and Nᵧ on the vertical axis, both arbitrary integers ≥5. Both sweeps still have the same two middle bands and A=6. Their cap constants are now 12(Nᵧ−3) and 12(Nₓ−3). The d170 comparisons are unchanged. Thus even physical diagonal symmetry is unnecessary.

## Named controls

The following exhibit simultaneous short characters for the named Ferrers rooms. Read each orientation from its narrow end. The two narrow-end depths can be chosen independently, since one specifies the top mark's ordinate and the other the far mark's abscissa. The remaining two mark coordinates are free inside the opposite terminal cells. Choose a=2w/P in each orientation so A=1. The two columns display (P,C) in the original and transposed orientations, using positive integer common periods. Each choice of a is strictly interior.

| Room | Original (P,C) | Transpose (P,C) |
|---|---|---|
| U1 | (30,105) | (20,20/3) |
| U2 | (6,78) | (70,35/2) |
| U2b | (6,6) | (70,35) |
| T1 | (24,8) | (6,6) |

The cap source character therefore has magnitude at most 3, strictly below d173's bound 4 with δ=w. All four rooms have whole-room lighting proofs. [Controls and transpose](deep-terminal-band.md)

In pyramid mask 761 at V=384 the forward source has A=1 and C=4 (c=2); the terminal rotations have denominators 6 and 2. All four forward charts really do fail for the saved pair, even allowing arbitrary windings. The perpendicular shot reaches it. This demonstrates the difference between eliminating a sweep and eliminating the physical pair. For R22 a legal positive-clearance chart for its dark pair necessarily misses the translated phase rectangle; d173 implies a short relation separately for each such chart. No relation is inferred for a chain with no crossing beam. [Pyramid proof](pyramid-sweep-obstruction.md)

## Room-dependent clearance without guessing a shot

For a monotone chain in an integral room, fix the middle itinerary's signed unfolded gate intervals (lᵢ,rᵢ), with integer endpoints, and measure integer longitudinal distances tᵢ from its first gate. This calculation concerns the unmarked reference beam, before extension to the marks. Put H=max(1,max |tᵢ|). If a strictly clearing line exists, one exists with δ≥1/(6H). Indeed maximize δ subject to lᵢ+δ≤x+tᵢs≤rᵢ−δ and δ≥0. A strictly feasible beam gives positive optimum. One can bound x and s by sufficiently large integers containing a strictly feasible beam, making the polytope bounded since the first gate bounds δ. At an optimal vertex three independent active equations have integer right sides. Every determinant term contains at most one slope coefficient of magnitude H, with the other factors at most one. Cramer's rule gives the bound. Touching the eroded interval boundary allows every subsequent perturbation of size strictly less than δ. This argument includes extra unfolded solid cap windows at integer longitudinal times, provided their winding shifts are separately respected. It does not manufacture a beam through a chain with incompatible windows. For a monotone unreversed chain H is bounded by the room's longitudinal span. In particular the coefficient cutoffs 24wH and 24VH suffice for d173 in these charts.

## Scope at W≤20

No new ledger word moves. The outstanding whole-word list is exactly all 4,568 entries at W=10,12,14,16,18,20 in the [ledger](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d163-pattern-ledger/ledger.json). This statement of coverage does not classify which individual placements fail. The W=10 residuals remain open. The missing assertion is that at least one physically available chart has a translated window intersecting its rotation subgroup; the small integer relations alone discard the translation that decides this intersection.

**What is the smallest W ≤ 20 room this result doesn't cover?** A smallest OPEN word is LLLRLLLRLR, with vertices (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
