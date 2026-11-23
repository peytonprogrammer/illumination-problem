# Eight stops and a single shared width

**Decision.** A single average of corner visibility from the two endpoints cannot force nine indispensable corners. This obstruction applies to every strictly simple orthogonal lattice room, including every BBBB room with at most eight reflexes. For a single proportional width shared across a pinch, exact synchronization of two prescribed histories has one scalar congruence. The stop argument does not decide it. A deformation of the named cov279 staircase shows that the congruence can miss the entire opening, for all monotone histories, even at parameters where a path is proved to exist.

## A universal limit on counting stops

Fix distinct same-parity interior lattice marks S,T. Use the pointwise marked affine stabilizer of the four-copy unfolding as in [the consultation](eight-stop-consult.md). Its cusps are orbits of unoriented rational directions. For a physical reflex C, let E_C(P) be the cusps for which a straight leg from some lift of P to C has no earlier physical corner. If a cusp contains one such leg, every representative direction has one: use a label-preserving affine map. The use of all physical lifts of P is important.

For any one representative direction there are at most four signed physical launches at P. Each meets at most one *first* corner, regardless of the number of smooth reflections before it. Consequently for **any** probability measure μ on the cusps,

    Σ_C μ(E_C(S)) ≤ 4,       Σ_C μ(E_C(T)) ≤ 4.

For a dark pair, a corner whose two sets intersect is indispensable by the consultation's cone argument. Attempt to prove intersection from the two marginal masses by requiring μ(E_C(S))+μ(E_C(T))>1. Summing shows that **at most seven** corners can pass this test. The strict inequality matters: equality allows the endpoint sets to be complements. This ceiling holds even when μ is chosen separately for each room and marked pair, as long as the same μ is used for all corners of that pair. It bounds what this proof can certify; it does not bound the actual number of common corners. Different weights for different corners, actual correlations between the endpoint sight lines, and paths through multiple corners are outside the argument.

In particular a single directional average cannot explain the ninth reflex in R22, even though all nine are known independently to be indispensable. The BBBB condition guarantees regular sites in each parity, but that count gives no correlation between these two endpoint sets. We have no stop-avoidance theorem for r≤8. A putative counting proof must exhibit where it uses joint trajectory data; replacing one probability distribution by a more favorable common distribution cannot fix this approach.

## One shared proportional width

Use the first-arrival setup of [component-ends.md](component-ends.md): fixed rational ordinates, widths rational affine in the parameter t, and two finite histories arriving transversely at a common mouth abscissa c with compatible directions. Fix their combinatorial chart. At a transcendental t, distinct proportionality classes of positive doubled widths separate by the reciprocal-function argument in that note. Suppose exactly one class occurs on both legs, with representative P(t). Write each shared traversal frequency as v_j=b_j/P(t), b_j a positive rational. Let α,β be the positive generators of the integer spans of the b_j on A and B respectively. Set λ to the positive generator of αℤ ∩ βℤ.

**Exact obstruction for these two reference phase vectors.** They belong jointly to the closure of one common slope flow if and only if

    λ (s_A(t,c) − s_B(t,c)) / P(t) ∈ ℤ.

Indeed an integral relation among frequencies splits by width class. On the shared class its weighted sum on A is the negative of its weighted sum on B and ranges over exactly λℤ before division by P. Every multiple occurs by the definitions of the two integer spans. All other classes already cancel on their own side. The torus character test gives the formula. It controls the reference phase vectors; an actual shot need only preserve the applicable inequalities and match at the opening. Other phase vectors and other histories remain possible. At a particular algebraic parameter other relations must be checked unless the actual frequencies are known to separate.

**What the pinch itself decides.** Let the shared period have positive limiting value at t₀, and let c tend to the common lip p. In the chosen fixed reflection words each reference slope has the form (ε_i c−u_i(t))/D_i, where D_i>0 is the fixed total vertical travel, u_i is affine, and ε_A=−ε_B are the terminal horizontal signs. Thus the mismatch varies with c at rate of magnitude 1/D_A+1/D_B. For each integer in the congruence there is one candidate c_k(t), affine in t. At the end the limiting residue must be integral, since it is finite and any sequence of integers converging to it is eventually constant. If it is nonintegral the reference phases fail throughout a one-sided neighborhood. If it equals k, only c_k survives, and comparing its affine slope with those of the opening lips decides whether it lies strictly between them. Any other chart restrictions must still hold. A candidate staying on a lip gives no open-mouth match. This statement needs no estimate for word length.

## The obstruction on a named room

Use exactly the cov279 rows recorded in [d69](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/decomp.py). Keep the bottom run fixed and translate the whole upper staircase horizontally by 1−t. The runs are

| Height | Horizontal run |
| --- | --- |
| (0,2) | (0,2) |
| (2,3) | (2−t,5−t) |
| (3,4) | (3−t,6−t) |
| (4,6) | (5−t,7−t) |

At t=1 this is the named room. For 0<t≤1 its boundary is strictly simple with six reflex corners. The overlap at y=2 is (2−t,2). Put S=(1/2,1), T=(4−t,3); the latter is interior on an artificial cut. This pencil is different from the earlier cov279 control, which moved only one run wall. Moving the upper chamber rigidly keeps the two run widths 2 and 3 constant, so they belong to the same proportionality class.

Consider **all** paths from S to T that never reverse vertical motion. Their two vertical travels must both equal 1. Unfold in the lower and upper vertical walls, using the physical orientation at the seam. Every possible crossing abscissa is the mean of a lower image from ±1/2+4ℤ and an upper image from 2−t±2+6ℤ. Conversely each such mean strictly in the overlap gives a legal shot: only open vertical walls can be reflected in the two intervening bands. Thus the attainable seam positions are

    c ∈ −t/2 + ({−1/4,+1/4}+ℤ).

The overlap has center 2−t/2 and radius t/2. Its center is always exactly 1/4 from the nearest attainable point. For 0<t≤1/2 **no monotone shot exists**, including every sign choice and winding number. At t=1 the direct chord crosses at 7/4 inside (1,2); equivalently the direct chord works for any t>1/2 in this interval. Hence the [reviewed marked-line theorem](generic-line.md) proves the pair lit for every irrational 0<t<1/2. Every such shot must reverse its vertical motion at least once. This establishes existence without selecting any reflection word.

The obstruction also occurs in the arithmetic core. For t=p/q with p odd, q twice an odd prime, 0<p/q<1/2 and gcd(p,q)=1, stretch the horizontal axis by q. The horizontal wall lengths include q and 2q−p, so the gcd is one. The vertical gcd is also one. The two marks have odd abscissas q/2 and 4q−p, and odd ordinates 1 and 3. The primitive area is 14q, and for large q the d69 criterion gives BBBB. Fractions of this form with arbitrarily large q are dense in (0,1/2): choose a large odd prime and an odd numerator in the rescaled interval avoiding its one possible interior multiple of the prime. Since lighting is open around each lit irrational parameter, there are lit primitive same-parity BBBB examples arbitrarily near the pinch for which every path must turn. This does not assert illumination at every rational specialization. [Area criterion](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md)

**Implication for the goal.** The arithmetic miss in this example is a quarter-unit placement error at an open seam, established before any stop is chosen. The very same line has a lit parameter elsewhere. Counting reflexes alone cannot force this one-class synchronization even for a lit pair with r=6. A universal eight-stop theorem, if proved, would of course imply ordinary illumination at r≤8; it would not require the path to synchronize these histories. Neither the seven-corner ceiling nor the scalar calculation settles the universal theorem.
