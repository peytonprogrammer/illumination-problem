# First shots and a noncongruence observable on two room doubles

**Result, pending review.** On DB55 and on the seven-unit cross, whether a specified pair is lit along a specified primitive direction does not factor through reduction of that direction modulo *any* integer N. Each counterexample uses one fixed same-parity interior pair, stays in one primitive parity, and allows all physical lift choices and traversal counts. This also rules out a congruence rule for the entire labelled sheet-reachability relation, since taking a finite union over lift labels would preserve such a rule. A class may nevertheless have many successful directions.

## Wall count cannot bound the first shot

**No finite H(W) bounds the height of a first legal shot, even for a pair known to be lit and W=12.** Here primitive height is max(|p|,|q|) in physical grid coordinates. D129's reviewed dumbbell proves this for every B. Put a=10·lcm(1,…,B), take left and right chambers of height five and widths 2a and 2a+1, and join them by a length-two corridor with mouth 2<y<3. The marks are (a,2) and (3a+2,2). In any direction with 1≤|p|≤B, the horizontal travel before the first encounter with the separating wall is a or 3a. Its vertical rise is a multiple of ten, so the shot hits the reflex at the lower lip. Vertical rays stay left. Yet (a+1,1) gives a legal one-reflection shot in the diagonal parity. The room is strictly simple and axis-normalized, r=4, area 20a+7. The previously reviewed Q/proper-factor area bounds imply BBBB at this size. The same construction disproves a W-only bound for the first shot in a *prescribed lit class*, since even its diagonal class needs height >B. [Construction](thin-gap-periods.md) · [d129 review and BBBB dependency](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d129-review-gapper/review.md)

Interchange the axes. Now every legal shot has |q|>B, and an axial horizontal shot cannot reach the other chamber. The total transverse height in d150's **fixed physical horizontal frame** is h=m|q| for a positive integer m. Thus no W-only bound exists for h either. This does not exclude bounds depending on area, the marks, or a different frame chosen for each room.

**Existence verdict.** I have no proof of a first shot in every class for general BBBB rooms. The negative height theorem explains why completing a bounded-height census at fixed W cannot provide such a proof.

## A room hypothesis that does force a first shot

For ordinary illumination it suffices that, for each required pair, two compatible lifts belong to one open, corner-cut cylinder. For a prescribed class c, the weakest condition *within this single-cylinder construction* is the following. In an integral chart that straightens a chosen cylinder, let (u,h) be the displacement and C the circumference. For h=0 require c to be the core class. For h≠0 put b=v₂(|h|). Compute the finite progression u+kC modulo 2^(b+1). Require at least one residue whose vector with h, divided by its common power of two and transformed back to physical coordinates, has primitive parity c. This is determined by the strip and the endpoint positions before any shot has been found. The room-wide hypothesis requires a qualifying cylinder and lift choice for each pair and requested class. Single-cylinder windings realize precisely this progression, so the condition is necessary as well as sufficient for this construction. No globally weakest structural room hypothesis is known. [Proof of the winding criterion](cyclic-separation.md)

There is a constructive height bound under the hypothesis. For any passing longitudinal coordinate one may reduce it, with its sign, to absolute value at most lcm(C,2^(b+1))/2 while preserving the endpoint and primitive class. In cylinder coordinates the primitive height is therefore ≤max(|h|,lcm(C,2^(b+1))/2); multiply by the induced infinity norm of the inverse chart matrix for a bound in physical coordinates. The h=0 case uses the core vector itself. This bound depends on actual geometry.

As a named control, evaluate the hypothesis on both *physical axial* open-cylinder decompositions and all lift choices. Each entry counts pairs for which the axial strips certify exactly that many primitive classes. The two axes are the same test in every room.

| Room | Zero | One | Two | Three |
|---|---:|---:|---:|---:|
| DB55 | 64 | 16 | 32 | 0 |
| Seven-unit cross | 196 | 256 | 114 | 8 |
| cov4181 | 6 | 4 | 0 | 0 |

These counts give first shots for 48, 378 and 4 pairs respectively without assuming a legal seed. All three hard controls, DB55 (2,2)–(10,2), cross (6,0)–(0,6), and cov4181 (2,3)–(4,3), miss the two axial open strips as a common-cylinder certificate. D72 supplies a non-axial or axial common cylinder for **all 112 DB55 pairs** when the target is ordinary illumination. D147 and d148 give every-class physical witnesses on cross7 and DB55 by other means. For cov4181 the last pair has exactly one realized class, so no sound sufficient condition for all three can hold room-wide there. Failure of the two-axis test does not assert failure over all possible cylinders. [Axial arithmetic replay](axis-strip-control.py) · [d72 common-cylinder data](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test/README.md) · [cov4181 all-direction replay](dyadic-classes.md)

## Why a parabolic cannot launch a shot across cylinders

In a horizontal cylinder with coordinates (x mod C,y), a horizontal ray keeps y constant. It stays on its own closed leaf. A horizontal multitwist also keeps y constant; it fixes the horizontal direction. For a core-parallel shot in an open cylinder, it is necessary and sufficient that compatible lifts of both marks lie on the *same leaf*. On a boundary one can instead use the same corner-free interval of a saddle connection. A regular lattice mark can lie on such an interval. Knowing only that the marks avoid boundary leaves is insufficient.

For example in DB55, at (1,1) and (3,1), both vertical billiard lines bounce between the bottom and top of the left chamber and never hit a tip. No vertical shot joins the marks: the abscissa stays fixed. This failure needs no boundary tip aligned with either mark. A transverse segment can cross several cylinders; its multitwist images remain legal if it is already legal, and its endpoints generally move unless the twist power fixes them. This gives no first shot. It leaves open whether *some* direction in each parity lights every BBBB pair. [DB55 geometry and exact arc test](deletion-invariance.md)

## A congruence obstruction for a fixed marked pair

Let F(p) be the bit that some physical launch in the unoriented primitive direction p reaches the target. Use the complete sets of source and target lifts. Suppose the marked affine stabilizer contains the horizontal and vertical integer shears E(a) and L(b) (off-diagonal entries a and b). If F factors modulo N, it also factors modulo the part N₀ of N supported on the primes dividing ab.

Indeed, write N=N₀N₁ with coprime factors. Powers of E(a) that are identity modulo N₀ generate every upper elementary shear modulo N₁, since aN₀ is invertible there. Likewise powers of L(b) give every lower shear modulo N₁ while fixing N₀. These generate SL₂ modulo N₁, by elementary row reduction over each prime power and CRT. They act transitively on primitive residue columns there: at each prime power a primitive column has a unit coordinate and can be reduced to (1,0). Thus a function of primitive residues modulo N invariant under the two shears can only depend on the N₀ component. The same proof works on a prescribed parity if the shears preserve parity and 2 is included among the retained primes.

For square coordinates, a valid a is the order of the right-edge permutation. Shear each horizontal unit-height row by a: at its upper and lower seams the map is the identity modulo the row circumference, so the affine maps glue with the same derivative and fix every grid vertex, including the marks and stops. The vertical construction gives b. After an integral unimodular change of basis the surface is square-tiled again. If the horizontal row order in this chart is P, the same argument makes F of the vector (m,1) periodic in m with period P. These are periods, not necessarily least periods. For DB55 the original vertical unit columns have periods 10 and 2 (chamber height five and corridor height one). A change by 10 in vertical slope per horizontal unit therefore preserves the lattice marks; in the d148 parameter (1,2j) this gives the period five. [Order-five pencil](local-global.md)

The following table uses that periodicity in a *tilted* chart. Orders come from the unit-square permutations. The four bits in the last two columns were checked by physical reflection, stopping at the first corner or repeated state. All launch signs are included. [Fixed-slice checker](parabolic-first-shot.py)

| Room, S → T | a,b | Chart horizontal axis | Original vector for chart (m,1) | P | Failed slice | Successful slice |
|---|---|---|---|---:|---:|---:|
| DB55, (2,2) → (10,2) | 130,10 | (3,2) | (3m+1,2m+1) | 110 | m=0 | m=10 |
| Cross b=7, (6,0) → (−6,0) | 56,56 | (1,1) | (m,m+1) | 572 | m=0 | m=4 |

In DB55 any N₀ uses only 2,5,13. Thus gcd(N₀,110) divides 10. Choose m≡0 mod N₀ and m≡10 mod 110 by CRT. Its vector agrees with the failed slice modulo N₀ and is lit by tilted periodicity. On the cross N₀ uses only 2,7, and 572=4·11·13. Here gcd(N₀,572) divides 4, so use m≡0 mod N₀ and m≡4 mod 572. The identical contradiction proves the result. One may adjoin a factor of two to the purported level before starting. In either case every successful slice so constructed has the same parity as its failed comparison.

The argument uses neither a Veech-index computation nor a search for a congruence level. It concerns line-by-line reachability. The much coarser existential question “is some direction in this parity lit?” has a positive answer for both named pairs in every parity by existing witnesses. [d147 cross review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d147-review-crossarcs/review.md) · [d148 DB55 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d148-review-delinv/review.md)

## Conditional chain

Internal reviews close the orthogonal corner-only branch below 22 walls and the proper canonical branch for interior lattice pairs. An all-class first-shot theorem in normalized BBBB rooms would therefore close the remaining *same-parity orthogonal interior lattice-pair* branch. Even one successful class would suffice there. The proposed core-to-core argument supplies neither theorem. Different-parity BBBB pairs, arbitrary nonlattice marks, and mixed-wall rooms require their own links before claiming the full W ≤ 20 goal. [Closure scope](../README.md)

The next mathematical target is the union of **individual** straight-leaf relations in the finite marked cusp action. The noncongruence result shows why replacing it by direction residues loses the necessary information already on these two rooms.
