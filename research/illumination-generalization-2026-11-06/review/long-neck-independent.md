# Independent acceptance of eventual illumination through a long neck

Verdict: ACCEPT the entire frozen long-neck-proof.md statement and its locally uniform consequence, for fixed orthogonal end chambers and fixed opposing actual interior marks under its explicit gluing hypotheses. No uniform wall-count bound, general degeneration classification, diagonal-chamber extension or uncapped W<=21 conclusion follows.

## Primary input and its actual use

I independently downloaded and read the original [Zemlyakov–Katok paper](https://akatok.s3.amazonaws.com/pub/AK-Zemlyakov1974.pdf), Proposition3 and Definition2, and [Masur–Tabachnikov's author handbook](https://math.uchicago.edu/~masur/handbook1.pdf), Theorem1.8 and the physical projection discussion. Own source copies and extracted text are preserved and hash-bound in the receipt. The former's quasiminimality definition includes density of each nonsingular forward semitrajectory; the latter supplies the usual minimal-direction statement. Torus chambers are covered by the original paper's preceding torus discussion as well. The import concerns fixed directions in rational-ANGLE polygons; it does not require rational wall coordinates.

For an orthogonal polygon, reflection in its horizontal/vertical sides generates four sign states of a nonaxis direction, with unchanged positive magnitude |vy/vx|. Its standard four-copy translation surface is connected: both kinds of sides exist in a bounded disk, connecting the copies across both sign generators. Removing the finite vertex lifts does not split a two-dimensional surface. Thus the incoming mouth flow box lies in the same connected invariant surface as each chosen interior-mark lift. Excluding the countable exceptional angular classes for BOTH chambers still leaves an available common positive magnitude. Excluding the additionally countable finite-wall-word corner directions for BOTH actual marks prevents genuine and removable corner contacts of the chosen trajectories. Zero-length developed vectors do not represent positive-length trajectories and need not be excluded as directions.

Density enters an OPEN incoming flow box at a strict subinterval of each mouth and then reaches that mouth. This proves a finite first-mouth hit from each actual mark. Taking the FIRST mouth hit prevents an auxiliary cap reflection from appearing earlier in the real chamber path. Neither trajectory is assumed to hit the other actual mark by density.

## Fixed finite entry words and signs

The two finite paths have only transverse contacts because neither velocity component vanishes. Strict contact-interior and aperture guards persist in a common nonempty open interval of angular magnitudes. Finite unfolding in the FINAL mouth charts gives constant virtual mark coordinates S*=(-a,alpha), T*=(b,beta). Their horizontal distances a,b are positive: horizontal speed magnitude is constant and final travel toward the first mouth has positive finite duration.

I independently derive the relative sign: let left outgoing vertical sign be e- and right outgoing-from-T sign be e+. Left slope is tau=e-*m. Reversing the right entry gives slope -e+*m, equal to sigma*tau for sigma=-e-*e+. Therefore z-=alpha+a*tau and z+=beta-b*sigma*tau are the two actual mouth ordinates. Both remain strictly inside (0,w) on a common bounded signed interval I. No reciprocal slope or swapped horizontal/vertical magnitude is imported; this is why orthogonal chambers matter.

## Exact phase and actual velocity match

The developed virtual target (L+b,2nw+sigma*beta) requires

    tau=(sigma*beta-alpha+2nw)/(L+a+b).

The numerator progression has step2w, so slopes have step2w/(L+C), C=a+b. The stated threshold L>max(0,2w/|I|-C) makes the OPEN candidate interval longer than a progression gap; it therefore contains a candidate strictly inside I even at a would-be lattice endpoint tie.

At the left mouth the neck phase is z- in (0,w), where the triangular fold has derivative +1. At the right it is exactly 2nw+sigma*z+; the fold yields z+ with derivative sigma. Thus both coordinates and both velocity components match the left itinerary and the reversed right itinerary. The terminal point is the actual translated T, not an approximate ordinate or another marked lift. All mouth-cap reflections are replaced by straight passages through actual interior interfaces.

Every neck fold is a true horizontal-wall reflection at 0<x<L. Strict mouth ordinates exclude the four joints regardless of whether a joint is genuinely cornered in the union. Finite L,w>0 and finite nonzero tau imply finitely many neck contacts. The chamber guards already exclude all their corners and any premature mouth encounter. This accounts for every actual wall and every source/target arrival.

## Local uniformity

Shrink I so its closure is inside the strict finite-itinerary guard set. Contacts and virtual coordinates depend continuously on the finite orthogonal wall data and interior marks when the wall patterns and gluing persist. In a neighborhood, the same two words and signs and the same smaller interval remain valid; a,b stay positive and mouth width can be bounded above by2w0. Then L>4w0/|I| is sufficient throughout that neighborhood, independently of the changing phase offset. This proves the sequence-level contradiction for dark opposing pairs with L tending to infinity and nondegenerate convergent chamber/mouth/mark data. It does not preclude sequences whose chambers or marks degenerate or lack this decomposition.

## Independent controls and verification level

long-neck-independent-check.py independently constructs four different prescribed paths at L=7,37 and both signs sigma, in the nonconvex-spur chambers. It uses independently written exact geometry validation, explicit boundary cycles, complete all-wall/open-leg guards, strict actual mouth coordinates, physical specular laws and actual marks. It checks 36 genuine reflections and 480 wall/leg comparisons. This checks finite controls, not the universal quantifier by sampling.

I also executed the peer's separately prescribed read-only validator; its result is stored as long-neck-peer-prescribed-replay.json. That replay is reproduction, not a second independent implementation. The independent hand proof and own constructor/checker are distinguished from it.

All peer packet pins match. This is AI mathematical hand review with explicit imported primary theorems and exact controls; it is not formal proof-assistant verification or external expert refereeing. The full uncapped canonical45 objective remains open.
