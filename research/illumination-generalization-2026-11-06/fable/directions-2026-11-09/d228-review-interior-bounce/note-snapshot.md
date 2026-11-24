Advances: L1 — two interior reflections realize the ordered (−,+) demands of the pinned six-reflex family for every parameter. The ray enters the middle tier, reflects from its ceiling and floor, then leaves through the opposite gate. For a prescribed sequence of tiers and wall copies, the following interval test characterizes all permitted sign vectors, including constraints at gates visited more than once.

### Displacement per visit

Use physical height y with source height 0 and target height D>0. Fix a developed transverse coordinate with source X₀ and target X₀+K, oriented so K>0. Horizontal reflections change the sign of the vertical velocity. Vertical-wall reflections, if prescribed, are unfolded in X. Let s be accumulated **absolute vertical travel** and H its terminal value. The developed line is X=X₀+Ks/H. Relative to the unbounced line with these same transverse endpoint images, the displacement at a visit to height y=Dα, in units of the new slope K/H, is exactly

    q = s − Hα.

The line is straight in the development. At a reversal physical height changes direction, so a single height can carry several q values. At an exact graze q is the unfolded offset μ of the previous note. At any other gate add (K/H)q to the original crossing. All signs below refer to the oriented unfolded coordinate and the selected approach. [End-bounce convention and gate test](l1-pinned-pairs.md) · [D226, claim 4](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d226-review-pinned-staircase/review.md)

**One reflection.** If the ray starts upward and turns at U, then U>D, H=2U−D, and the two legs have s=y and s=2U−y respectively. For a downward start turning at V, one has V<0, H=D−2V, and s=−y and s=y−2V. These formulas give q on either leg by subtraction of Hα. In the open range 0<y<D the first itinerary gives q=−2(U−D)α throughout, the second gives q=(−2V)(1−α) throughout. A single horizontal reflection at a level strictly between the marks cannot be the only vertical reversal on a connecting ray.

**Two interior reflections.** For an up–down–up excursion, turn first at U and then at V<U, with U>0 and V<D. Write L=U−V. Then H=D+2L and the complete sign rule is

| Visit | Physical traversal | s | q |
|---|---|---|---|
| First ascent | 0 to U | y | −2Lα |
| Descent | U to V | 2U−y | 2[U−(D+L)α] |
| Final ascent | V to D | y+2L | 2L(1−α) |

For 0<y<D the signs in travel order are minus on the first leg, increasing through at most one zero on the descent (at α=U/(D+L)), and plus on the final leg. Thus a lower pin on the first leg and a higher pin on the final leg receive (−,+). This is a demand on specified *visits*. Every intervening gate must still admit each additional visit or provide a wall face for the turn. For two reversals starting downward, the first height V is below 0 and the second U is above D. Here H=2(U−V)−D and the successive s values are −y, y−2V and 2(U−V)−y. In the open range between the marks only the middle leg occurs. Its q=−2V−(H−D)α is decreasing. Together the tables and the one-turn formulas specify the signs at arbitrary selected visits, including equality. They follow by adding the vertical distances to the preceding turn. Zero at an exact corner is forbidden.

### When a sign vector is realizable

Fix an ordered chain of slab components and developed copies, with its turn walls. Split it at every crossed horizontal interface and turn. In a tier with side reflections one can use its reflected strip of rectangular copies: prescribe the copies of the entry and exit, with the intervening side faces genuine reflecting walls. In a single rectangular tier their order is then fixed by monotonicity of developed X. At an interface select a connected open interval Iⱼ in the developed coordinate. For a crossing it must belong to the overlap with the next component on the selected copies. For a turn it must lie in the relative interior of the *exposed horizontal face on the incoming component*, returning to that component. In particular an overlap cannot serve as a mirror. Artificial cuts through smooth interiors can be joined across a subdivision point when the local passage is open. Split intervals further wherever the permitted continuation changes. At a signed pin intersect Iⱼ with the demanded open side of its unfolded corner image cⱼ. Keep distinct visits even when they have the same physical level.

Write the resulting interval as (lⱼ,uⱼ) and let sⱼ be the visit's accumulated travel. A nonempty choice of intervals realizes this chain, winding and sign vector **if and only if**

    maxⱼ (lⱼ−X₀)/sⱼ  <  K/H  <  minⱼ (uⱼ−X₀)/sⱼ .

The maximum and minimum use the internal visits, where sⱼ>0; the source and the selected target image must belong to the prescribed endpoint components. With multiple possible gate components take the union over *incident chains*, retaining the same K/H for every test along a chain. If target images vary, the open interval must contain an actual compatible target slope. Necessity follows by evaluating X at each visit. For sufficiency join the evaluated endpoints in each developed rectangular tier strip. Convexity keeps that leg inside the strip, all intermediate side hits are transverse and away from horizontal levels, and the open face tests glue the legs with the required transmission or reflection. This also protects ordinary gates that the excursion moves. Signs alone omit interval widths, wall exposure, and endpoint aim. The exact residual for this move is that every eligible chain with at most two reversals misses its compatible target slope or has an empty required interval.

### Six-reflex family. Two middle-tier reflections suffice

Use the previous note's coordinates, t=10m+1, m≥1, S=(0,0), T=(4t,4t). Set U=3t, V=t. Then H=8t, K=4t, so the initial velocity is proportional to (1,2). The entire itinerary is given by the following strict face tests. [Tier coordinates](l1-pinned-pairs.md)

| Height | s | x | Required interval and event |
|---|---|---|---|
| t | t | t/2 | (0,t), enter middle tier |
| 3t | 3t | 3t/2 | (0,3t), reflect from middle ceiling |
| t | 5t | 5t/2 | (t,4t), reflect from middle floor |
| 3t | 7t | 7t/2 | (3t,4t), enter upper tier |
| 4t | 8t | 4t | reach T inside the overlap (3t,6t) |

The entry and exit shifts from x=y are −t/2 and +t/2. The lower and upper rectangles contain the initial and final legs, and the middle rectangle contains all three intervening legs. No vertical wall is touched. The strict inequalities hold for all t>0, so neither integrality of the bounce points nor a lower size threshold is needed. This closes the specified pair throughout the family.

### R22 and the first open case

The R22 fold rules out every legal itinerary for its dark pair. After first-arrival/last-visit truncation, a folded path would be an ordinary staircase path between the two even sites. Its development has an intermediate lattice point with an odd coordinate, which folds to a forbidden staircase vertex. Thus every candidate here fails some full-chain requirement. The fold need not fail the same sign or gate for different windings. [R22 parity and reversal argument](l1-periodic-obstruction.md)

“No permitted pattern for any winding” is equivalent to darkness **if** the patterns test exact endpoint aim and every legal itinerary is included (with axial passages treated separately). For the family tested here, winding varies the transverse target image, while at most two horizontal turns are allowed. The fold implies failure of that restricted test in R22. The converse would require a completeness theorem for the restricted class.

**First general case still open.** For a nondirect pinned pair with at most eight reflexes, an ordered (−,+) demand can now be served by a ceiling–floor excursion. The unresolved case is when every such choice, in each winding tested, lacks an exposed turn face at the required abscissa or fails another visit or the endpoint-slope test, and no other legal itinerary has been established. A ceiling and a floor in the tier diagram alone do not settle this. The six-reflex family above is discharged. No bound on the number of axial reversals needed for the general pinned pair follows.

### Combined excursions. A strict sign theorem for any number of slabs

Fix the winding, the successive slab components of the upward passage, and its ordered exact pin visits at 0<α₁<⋯<αₚ<1. Here a pin visit is the **transmission** between successive slabs. A ceiling–floor excursion in one slab precedes its transmission through the upper interface and follows its transmission through the lower one. Count it at the cut between those two visits. Additional contacts with either interface are turns and must be checked separately. We allow repeated excursions in the selected slab before continuing upward. This move set also allows longitudinal end delays when their physical itineraries exist. D227 independently gives the (1,2) witness above and the repeated-end switch. [D227, claims 5 and 7](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d227-review-pinned-pairs/review.md)

Index each available delay j by its cut cⱼ, the number of pin transmissions already completed. Thus 0≤cⱼ≤p. A slab of axial width Lⱼ has delay quantum λⱼ=2Lⱼ. An end delay lies at cut 0 or p, with its actual delay quantum (2d₀ or 2d₃ in d227). For now “available” means there are wall faces for the proposed turns; their lengths and the locations of hits enter below. For integer multiplicities mⱼ≥0 put hⱼ=mⱼλⱼ, E=Σhⱼ and H=D+E. At transmission i the exact shift is

    X′ᵢ−Xᵢ = (K/H) qᵢ,     qᵢ = Σ_{cⱼ<i} hⱼ − αᵢ E.

Indeed travel to that transmission is Dαᵢ plus exactly the completed delays. The numerator profiles therefore add. All physical shifts have the same new denominator H. The two end terms alone give the switch h₀/(h₀+hₚ) when their sum is positive. Each interior term adds a jump of hⱼ between transmissions. This formula concerns a fixed transverse development with rectangles unfolded consistently across the selected transmission chain.

**Which strict sign orthants does the cone meet?** For p≥1 let J be the available cuts. A demand εᵢ∈{−,+} is realized at the level of displacements by some integer multiplicities if and only if all three rules hold:

1. If the first demand is plus, cut 0 is available.
2. If the last demand is minus, cut p is available.
3. At every adjacent change εᵢ=−, εᵢ₊₁=+, cut i is available.

A cut between pins means any eligible slab delay between their transmissions, including when other ordinary interfaces intervene. Thus (−,+,−) needs a cut between the first two and a delay after the last; the change from plus to minus needs no intervening wall. P0 can use either strict sign, so take the union over its two choices.

**Proof.** For E>0 let Fᵢ=Σ_{cⱼ<i}hⱼ/E. The demand is the strict comparison of Fᵢ with αᵢ. F is nondecreasing, is constant across missing cuts, begins at zero if cut 0 is missing and ends at one if cut p is missing. This proves necessity. For sufficiency break the pins into runs at every available internal cut. Within a run the demands consist of a plus prefix followed by a minus suffix, either possibly empty. Choose a constant F for that run strictly between the last plus fraction and the first minus fraction. For a pure-minus run choose just below its first fraction, and for pure plus just above its last. Since successive runs have disjoint ordered fraction ranges, the constants can be chosen strictly increasing in (0,1). If cut 0 is absent fix the initial run at 0 (it must be pure minus); if cut p is absent fix the final run at 1 (it must be pure plus). If both are absent and there is only one run, the rules already exclude every demand. The jumps, including the initial jump from 0 and the terminal jump to 1 when needed, give nonnegative unit-total masses on available cuts. Choose one generator per positive mass w. Counts floor(Mw/λⱼ) have normalized masses tending to w as M increases. All strict comparisons therefore hold simultaneously at some finite M. This last argument proves integer **sign** feasibility only.

**Simultaneous clearance and the exact geometric residual.** For fixed counts use the departure time s₀ at entry to a slab of length L. With m repetitions, its roof turns occur at s₀+(2h−1)L and its floor turns at s₀+2hL, 1≤h≤m; it transmits at s₀+(2m+1)L. Charge every end visit by its actual accumulated travel as well. For *every* visit v, including ordinary transmissions, choose its incident interval (lᵥ,uᵥ) in that unfolded copy: an open overlap to transmit and an exposed wall to turn. With X₀ the developed source coordinate the exact simultaneous clearance condition is

    minᵥ { K sᵥ − H(lᵥ−X₀), H(uᵥ−X₀) − K sᵥ } > 0.

The minimum is over internal visits. Endpoints and copy compatibility are as in the interval-chain theorem above. This is a strict threshold for the entire vector of counts; division by H gives the smallest transverse clearance. If several roof hits use the very same developed interval, monotonicity in s lets one check its first and last hit, likewise for the floor. Different copies or disconnected faces require their own tests. Necessity and sufficiency follow by evaluating the one straight line and joining consecutive visits inside each developed slab. Scaling counts to obtain strict signs can send a return into a gate or a corner. For this move set the residual is exactly failure of a cut rule, or failure of the displayed clearance inequality for every sign-compatible count and incident chain at the chosen winding. The six-reflex room meets both tests with one interior generator.

**R22 distinguishes the cone from legal paths.** Take the *direct* transverse development of (0,0) to (2,2), so D=K=2. The sole internal transmission at y=1 needs a minus shift into (0,1). In the slab 1<y<2 the component is (0,4); its floor is exposed over (1,3), and its roof over (0,1) and (3,4). This gives an available cut after the pin. A single double excursion there has H=4. The first crossing is x=1/2, strictly inside the required gate: the demand **is in the sign cone**. At the supposed roof turn, s=2 gives x=1, exactly the corner (1,2). The strict clearance is zero there. These coordinates follow from the three five-square copies. [R22 room definition](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex)

Consequently R22 refutes “outside the sign cone for every winding” as a characterization of darkness. Its fold proves the stronger geometric fact that every attempted itinerary fails, including every count and chain above. An equivalence using the clearance test for slab excursions alone would additionally require proof that whenever a pair is lit it has such an itinerary. A downward leg that exits its slab before turning again is outside this move set. [Fold and reversal proof](l1-periodic-obstruction.md)

**First open case for L1.** For the displacement problem the three cut rules settle every strict demand. For lighting, already a single minus demand can pass these rules and have a proposed turn hit a corner, as R22 demonstrates at nine reflexes. In scope, the unresolved implication is that for a specified nondirect pinned pair with at most eight reflexes, some winding and counts have positive simultaneous clearance, or a legal itinerary exists outside the slab excursions. Even the ordered (−,+) repair needs an intervening slab with two usable wall hits. No eight-reflex darkness or closure follows from the cone alone.
