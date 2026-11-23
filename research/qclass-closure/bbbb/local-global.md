# Density of legal vectors and the limits of a congruence sieve

**Result.** For exact corner-free legality, one legal vector already implies positive lower planar density of legal vectors in its marked affine orbit. Density does not produce the first legal vector. For one DB55 pair in a lit class, the per-line bit on its prescribed pencil cannot be a function of direction residues modulo a power of two. General finite-index affine invariance does not imply invariance under a principal congruence subgroup.

## The exact vector test

Use an oriented developed displacement w=m p with p primitive and m positive. For same-parity lattice marks m is even. In the marking adapted to p, each sheet labels one edge of the lifted pillowcase arc; mark the two physical lifts at each end. Launch along each allowed incident edge at a source lift, stop at any physical corner, and after m edges test membership in the target lifts. This defines legal w with the appropriate frame/sign choice. If length and launch sense are free, regular continuation is given by the two swaps A³,D³; the orbit test in d148 is exactly existence of *some* traversal count, not a verdict at a prescribed m. A relaxed candidate may instead allow all corner continuations. A formal target image imposes only the reflection-group displacement condition. These definitions give different sets. A corner image lying on the developed line blocks that launch only if the lifted segment hits that corner on its actual sheet. [d148 single-arc test](deletion-invariance.md)

## Density theorem without a sieve

Let H be the finite-index subgroup of SL₂(ℤ) admitting affine lifts fixing all corner stops and endpoint lifts pointwise, intersected with Γ(2) to preserve primitive parity. The stabilizer of the finite permutation-cover data has finite index; among its affine lifts the kernel of the finite permutation action on marked grid fibers has finite index too. Projecting that kernel gives a finite-index derivative subgroup. Existence of one mark-preserving lift of a given derivative suffices. The proof concerns exact shots only. Each H-orbit of oriented developed vectors, with the corresponding lifted endpoints, has constant legality: an affine lift and its inverse carry a corner-free straight segment to a corner-free straight segment. In particular the fraction of legal vectors on such an orbit is one or zero. [Marked subgroup construction](per-class-converse.md)

For completeness each nonzero H-orbit has positive lower density in the full lattice for fixed content m. Let K be the normal core of H. Finitely many linear translates of Kp cover all primitive vectors, because SL₂(ℤ) acts transitively on primitive vectors. If there are d translates and all inverse representatives have operator norm ≤C, the number of primitive vectors in a ball of radius R is ≤d times the number of Kp points in the ball of radius CR. The former grows proportionally to R² by ordinary Möbius inversion. Scaling by m costs a factor m². Since Kp⊂Hp, this proves the claim. No uniform density constant in the room or m is asserted. Conditional on a legal seed this works even for noncongruence groups.

Schmithüsen constructs square-tiled surfaces in genus two with noncongruence Veech groups. Marking more points cannot make their subgroup contain Γ(N). This refutes the proposed general level premise. It does not rule out a particular observable factoring through a congruence quotient, or prove a noncongruence example among the restricted BBBB room doubles. [Schmithüsen, noncongruence examples](https://arxiv.org/abs/0704.0416)

## A dyadic countercheck on DB55

Take S=(2,2), T=(4,4), and the horizontal primitive pencil p_j=(1,2j). The order-five d148 pencil gives the following physical row, allowing all lift choices and traversal counts:

| j modulo 5 | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| reaches T | 0 | 1 | 1 | 1 | 1 |

Replay the existing d147 label closure on the d148 DB55 tuple at origin (2,2): for h=BC take the bitwise union of pencil_components(A,B,h,regular=True) over one incident sheet from each endpoint lift. The mask is 30. Equivalently, residue zero is the horizontal line at y=2; the four nonzero powers give legal hits. This is one algebraic row of the previously reviewed pencil, with no direction discovery. [Pencil implementation](cross-factor-arcs.py) · [Physical dictionary](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d148-review-delinv/review.md)

For every k≥1, p₀ and p_(2^k) agree even modulo 2^(k+1), yet only the latter line reaches T. This even puts successful directions arbitrarily close 2-adically to the unsuccessful p₀. Thus the direction observable “some legal length on this line” does not factor through any fixed dyadic modulus. Every crossing of x=5 by a (1,2j) ray has integer height, so the ray cannot enter the open unit mouth. Inside the left 5×5 box the unfolded vertical period is ten, giving period five in j. At multiples of five only lattice heights folding to y=2 are visited. The example does not refute an odd-prime certificate for a whole dark class; the class tested here is lit. An iff for class darkness needs a specified family of local tests defined independently of the unknown legal set.

## Dark controls

In R22 all three classes are dark. Its proof uses divisibility of a developed displacement *after folding*, the position of the resulting lattice hit, and reversal at smooth seam endpoints. The dyadic calculation and the fold geometry work together. In cov4181 the clean fiber excludes the diagonal class. The vertical class has ten regular sites and nevertheless the marked lifts are separated even in the corner-continued arc graph on the four-sheet quotient. Its proof uses the action on sheets and the distinct singleton images; a planar sieve for interior corner hits would start too late for that class. These examples establish darkness, without establishing a prime-power characterization of all dark classes. [R22 parity and seam mechanism](dyadic-classes.md) · [cov4181 quotient](exclusion-descent.md)

## Fixed-chain follow-on

In a developed corridor with fixed endpoint images S,T′, the only straight candidate is [S,T′]. At an ordered seam on a supporting line, its crossing must lie strictly inside the selected open interval and in the prescribed order. A segment through a reflex tip has zero clearance there. Keeping S and T′ fixed allows no transverse push of a straight segment, even to one side. A taut shortest path bending at the tip is forbidden. If several lifts develop to the same point, changing the lift or seam choice is additional itinerary data.

DB55 gives an exact witness. For this separate example switch the target to (10,2). The segment from (2,2) to (10,2) along the lower lip meets (5,2) and (8,2). A downward push enters the exterior of the corridor; an upward detour with the endpoints fixed must bend. D148's legal direction (3,2) uses another development. More generally a genuine change of developed endpoint by a lattice vector Δ changes primitive parity to (w+Δ)/2^v mod 2, where v is the smaller of the two coordinate valuations (w+Δ nonzero). A continuous push of a taut string supplies no such Δ. The outstanding geometric step is to realize an alternative endpoint image with the required primitive parity and strictly interior seam crossings. [Fixed-chain residue test](class-repair.md)

D151 confirmed the DB55 row by direct billiards for |j|≤60; its review did not independently recompute the bit mask. [Review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d151-review-localglobal/review.md)
