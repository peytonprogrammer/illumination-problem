# Full-row lighting under two height conditions without a spanning hall

**Result for review.** A smallest dented target-1 word whose ledger realization lacks a spanning hall is LLLRLLLRLLRR, W=12. In that realization every pair of abscissas on two prescribed rows, one in the bottom tip and one in the top tip, is lit under either of the height conditions below. The half-lattice rows a=b=1/2 are excluded. The denominator cutoff 101 comes from the chosen 1/100 patch. The construction uses attachment sides and crosses all four intermediate mouths. The lengths of this realization are fixed; the proof also gives a sufficient condition on other realizations.

Use the live ledger split of 6 COVERED, 270 PARTIAL, 4,298 OPEN. Nine two-bank words are provisional and cov279's PARTIAL result is for same-parity lattice pairs. [Live status](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d163-pattern-ledger/STATUS.md)

## A crossing that survives winding

The unit-height runs, bottom to top, are (0,1), (0,5), (3,5), (2,5), (4,5). The extreme runs are disjoint. Take the first mouth crossing at e=1/2 and launch upward with horizontal travel s=16/5 per unit rise, initially to the right there. On the next three levels the crossings are 37/10, 31/10 and 41/10. There is a reflection at x=5 in the middle run (3,5), then a reflection at x=2 in the run (2,5). The outgoing horizontal sign at the last mouth is positive. The two reflections are essential to this particular crossing sequence. D164's B example motivated allowing the ray to use attachment sides. [Attacker report](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d164-attack-combs/attack.md)

In the rectangle |Δe|,|Δs|<1/100, the three crossing coordinates are e+s, 10−e−2s and e+3s−6, evaluated at the perturbed e,s. Each remains strictly inside its mouth: the smallest baseline margin is 1/10 and the largest possible change is 4/100. All internal side contacts in these open bands are smooth. Adding 60k to s, k a nonnegative integer, preserves every signed mouth crossing. Indeed each of 10, 4 and 6 (the three doubled widths) divides 60. Crossing a band in unit height adds or subtracts 60k in its reflected coordinate while preserving the folded exit and its outgoing sign. This argument works on the whole perturbation rectangle.

For a short exact replay take S=(3/10,3/4), T=(43/10,9/2). Folding the bottom tip makes the initial direction (−16,5). The four physical reflections are at (0,27/32), (5,77/32), (2,107/32), (5,137/32). The d164 rational tracer returned T exactly.

## Full-row theorem

Let the source row be y=1−a and the target row y=4+b, with 0<a,b<1. Every pair of interior abscissas on those rows is lit if either condition holds.

1. The real numbers 1, 30a and 30b are rationally independent.
2. The reduced denominators q and q' of 30a and 30b are coprime and both at least 101.

To see this, use unfolded endpoint abscissas, modulo 2 in each unit-width tip. At the base crossing they are x₀=e−as and z₀=e+3s−6+bs. The shifts indexed by k translate this pair by (−60ka,60kb) modulo 2. In case 1 the translates are dense on the two-dimensional torus by Kronecker's theorem. In case 2 they form the full rectangular grid of spacings 2/q and 2/q' by the Chinese remainder theorem. For any desired pair of physical abscissas choose their positive-sheet representatives. Some translate lies within 1/100 of each, using the nearest grid points in case 2. Write dx,dz for the signed remaining errors in these representatives.

Correct the errors exactly by taking

    Δs=(dz−dx)/(3+a+b),     Δe=dx+aΔs.

Then |Δs|<1/100, and Δe is a convex combination of dx and dz, so |Δe|<1/100. The new crossing remains in the verified rectangle. The two corrections change the developed endpoint coordinates by exactly dx and dz, even after the large winding. Folding the bottom and top legs into their respective tips gives the requested physical endpoints. Their intermediate side reflections are legal. Case 1 covers almost every pair of row heights but does not cover rational heights. Case 2 supplies rational rows with **every** pair of abscissas lit there, including rational abscissas.

**Exact CRT replay.** For a=1/101, b=1/103, x=3/4 and z=17/4, rounding each displacement to its nearest grid point and solving the two congruences gives k=2740. The corrections are Δe=559/125652 and Δs=−211/314130. With slope 10328795401/62826, exact folding gives successive mouth abscissas 63385/125652, 155129/41884, 389131/125652 and 515479/125652, and final positive horizontal sign. Folding the two end legs gives exactly 3/4 and 17/4. This computes the windings from the specified endpoints without a direction search.

**What generalizes.** For consecutive rational rectangular bands of heights dᵢ and widths uᵢ, choose an integer P with Pdᵢ in 2uᵢℤ for every intermediate band. A single strictly interior through-crossing and its nearby launches survive all shifts s↦s+kP by the same signed folding argument. For end widths u,v the normalized rotations are −Pa/(2u) and ±Pb/(2v). Density gives all abscissas for independent rotations, and coprime denominators give all abscissas as soon as the endpoint grid fits inside the local image of the crossing patch. That image has interior: after correcting for the outgoing sheet sign the two endpoint derivatives in (e,s) are (1,−a) and (1,D+b), with D the total intermediate height. Their determinant is D+a+b>0. No common intersection of all the horizontal runs is required.

**Explicit patch for a supplied crossing.** Let m be the minimum transverse distance of its first crossing and each subsequent crossing from both physical mouth ends and the sheet ends there. Require m>0. For endpoint errors dx,dz on the chosen signed sheets, the change at every joint is a convex interpolation of dx and the sign-corrected dz along the developed segment. Thus max(|dx|,|dz|)<m preserves all the joints and their sheets, including under an exact period shift. Coprime rotation denominators q,q′ suffice if u/q<m and v/q′<m. This is conditional on an exhibited crossing. A nested staircase supplies its own crossing and explicit clearance at all lengths by [the terminal-strip construction](ferrers-terminal-strip.md).

**Remaining obstruction.** For example at a=b=1/2 both rotations vanish. Winding translates this patch to itself on the endpoint torus. The proof then certifies only its local image and reflected copies. It gives no claim of darkness on those rows. An all-length theorem needs control of these resonant rows and existence of a crossing patch across the required mouths in each geometry. This result does not change a ledger status.

## What is the smallest W ≤ 20 room this result doesn't cover?

Globally a smallest OPEN word is LLLRLLLRLR, W=10, with ledger vertices (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2). Within the 296 requested realizations the present word LLLRLLLRLLRR still lacks an all-length, all-pair proof. Its ledger vertices are (0,2), (0,0), (1,0), (1,1), (5,1), (5,5), (4,5), (4,4), (2,4), (2,3), (3,3), (3,2).
