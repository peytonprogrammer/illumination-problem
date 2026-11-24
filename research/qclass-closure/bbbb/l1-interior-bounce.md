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
