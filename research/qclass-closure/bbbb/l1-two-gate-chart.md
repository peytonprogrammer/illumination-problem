Advances: L1 — outcome (b). In this six-reflex chart there is an explicit unbounded family of lit pinned pairs for which **every witness needs unboundedly many axial reversals**. This excludes the proposed monotone, single-excursion and end-bounce tests together, with unrestricted side windings. The obstruction comes from a half-period mismatch between the first and last visits. A long sequence of regular roof and floor reflections gives an exact witness outside the family.

### Open rectangles: the exact two-dimensional test

Let Λ be a full lattice, v its translate, and J an open rectangle. Choose a primitive shortest-width dual direction ℓ and complete it to an integer basis ℓ,m of Λ*. Use coordinates u=ℓ(x−v), z=m(x−v). The transformed rectangle is an open parallelogram and the coset is ℤ². Its width W in u is the sum of the two side lengths times the absolute corresponding coefficients of ℓ. With the d230 lattice those coefficients are consecutive differences of nⱼ/Pⱼ for an integer modulus relation. For a discrete full dual, positive side lengths ensure the minimum is attained.

If W>1+2/√3 the rectangle contains a coset point by planar flatness. Otherwise take **all integers i strictly between the lower and upper u supports**. The complete list of cases is zero, one, two or three rows. Zero rows is a split certificate. For each remaining row intersect u=i with the four open half-planes of the parallelogram; denote the resulting open z interval by (lᵢ,rᵢ). The rectangle is hollow iff for every such row

    floor(lᵢ)+1 ≥ rᵢ.

This is necessary and sufficient by the dual change of basis. Other primitive directions can also give split certificates; the row test need not recognize them as splits to give the correct answer. It includes equality at an excluded endpoint. For legal smooth-wall endpoint events use the appropriate closed-side convention and sector checks separately. [D231, box and width conventions](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d231-review-gate-box/review.md)

**The proposed lower width bound for non-split configurations is false.** In ℤ² take the open rectangle with bottom vertex (1/2,−1/100) and perpendicular edges (6,3/5), (−1/50,1/5). Its vertical span is (−1/100,79/100); its only integer row is 0, whose open slice lies between x=499/1000 and x=3/5. Thus it is hollow. Its width in an integer covector (p,q) is

    (3/5)|10p+q| + (1/50)|−p+10q|.

For p≠0 this exceeds 1: if |10p+q|≥2 the first term suffices, otherwise |−p+10q|≥91. The primitive vertical covector has width 4/5 and its projection contains 0. No primitive direction has a projection miss. Changing coordinates to the rectangle's edge axes gives an axis-aligned rectangle with a full-rank lattice. Thus a list restricted to non-split widths above 1 omits even a rational one-row example. The row list above has no such restriction.

### Conditions for all free gaps

Write the ordered transverse supports as A<C<D<E<F<G<H<J. From bottom to top the tiers are (A,G), (A,D), (C,F), (E,H), (E,J). Let the successive axial levels be y₀<⋯<y₅. The pins are S=(C,y₁), T=(G,y₄). All consecutive gaps on both axes are free positive lattice lengths. Take all vertical itineraries with at most two changes of axial sign, including initial or final end bounces and a roof–floor excursion in any slab; this contains the requested single moves. The obstruction below also works for any fixed larger reversal budget.

At the four internal levels the transmission intervals are respectively (A,D), (C,D), (E,F), (E,H). For a turn, take the open part of the incoming tier face outside the neighboring tier, splitting into incident wall intervals; at y₀,y₅ take the whole outer face. For each fixed level word and side parity let wⱼ be the width from the tier list, hⱼ the absolute difference of consecutive event heights (including the marks), Pⱼ=2wⱼ, and σ₀=1, σⱼ₊₁=(−1)^εⱼ σⱼ. Put cⱼ=0 for even parity and cⱼ=2σⱼ times the tier's left support for odd parity. Define

    Htot=Σhⱼ,  Yᵢ=Σ_{j<i}hⱼ,
    vᵢ=C+(Yᵢ/Htot)(σ_final G−C+Σcⱼ)−Σ_{j<i}cⱼ,
    Λᵢⱼ=Pⱼ(Yᵢ/Htot−1[j<i]).

Use the column span over ℤ of this matrix as lattice and multiply each physical interval by its event sign σᵢ. For the monotone case h=(y₂−y₁,y₃−y₂,y₄−y₃) with box (C,D)×(E,F) before signs; the row test is the explicit hollowness condition. For each excursion with a repeated full visit, take the primitive dual of the +1,−1 equal-modulus relation. Slice the box on every integer level of that character after subtracting v. On each nonempty slice complete the character to a lattice dual basis and test the residual integer coordinates in the resulting bounded polytope (recursively intersect open intervals with integer rows). The excursion is hollow exactly when every slice misses. This retains the affine levels; discarding the universal direction without slicing loses the condition. For other words use the same slice recursion in any dual basis. The input lengths are rational, so the lattice is discrete and its connected part is zero. Include smooth endpoints by testing the permitted faces with their incident sectors. These formulas specify membership or hollowness for every free-gap choice without a direction cutoff. [Exact projected coset criterion](l1-dark-flat-exactness.md)

### An unbounded obstruction, with a legal ray beyond the reversal budget

Let N be an even integer, N≥40. Use axial levels −1,0,1,1+B,2+B,3+B, with B=2N+2. Take transverse tiers

    (0,5N/2), (0,N), (N−1,2N+1), (2N,3N), (2N,4N).

The pins are S=(N−1,0), T=(5N/2,2+B). The two transmission gates have width one. All supports have exactly the required strict order, the chart has six reflexes, and unit gaps keep both axes primitive. In particular this is unbounded in ratios as well as in area.

For any putative ray let Aₛ be its absolute axial travel from S to the **first** passage into the middle, and Aₜ the absolute axial travel backwards from T to the **last** passage out of the middle. Both are odd integers: the net axial displacement has magnitude one and each reversal occurs at an integer level. Write p for the absolute transverse slope. All side mirrors in either end have abscissas in (N/2)ℤ, so developing or folding changes a transverse coordinate only by sign modulo N. The first mouth lies between N−1 and N; both signed images of S are within 1 of 0 modulo N. The second mouth lies between 2N and 2N+1; both signed images of T have residue N/2. Consequently

    dist(Aₛ p, Nℤ) ≤ 2,      dist(Aₜ p, N/2+Nℤ) ≤ 1.

These weak inequalities even grant the gate endpoints. Multiply the first by Aₜ and the second by Aₛ. Since Aₛ is odd the two progressions remain separated by N/2. Eliminating the common quantity AₛAₜp gives the necessary condition

    N/2 ≤ 2Aₜ + Aₛ.

If the ray has at most r₀ axial reversals, each of its end legs consists of at most r₀+1 monotone pieces of length at most 2, the full axial depth of that end. Thus N≤12(r₀+1). For N≥40 every itinerary with at most two reversals is hollow in every parity. In particular the obstruction holds regardless of what side windings are allowed. Axial rays cannot join these marks since both coordinates differ. Increasing N defeats **any fixed** reversal budget at the same wall count.

**The pairs are lit.** Launch with transverse/axial velocity (1,2), initially upward. The first crossing is at N−1/2. After middle travel B=2N+2 the crossing is at 2N+1/2, strictly inside the second gate. Keep moving transversely right in the upper end. Measured from that crossing, after one unit of axial travel the ray reaches the target's height, after two it reflects off the outer roof, and after four it returns to the floor at 2N+5/2, on the exposed wall beyond the gate. Each further four-unit period increases the abscissa by 2. Until the target is reached all return hits lie strictly between 2N+1 and 3N, and all passages through the target level are inside its open overlap. After N−1 units of absolute axial travel the abscissa is 5N/2. Since N−1 is odd the height is exactly 2+B. The path reaches T and has no corner contact. This is a symbolic family proof; no ray or room search is involved.

### Three gates and stopping rule

In dimension three slice in a primitive dual direction, then apply integer-row tests to each planar polygonal section (which need not be a rectangle). Alternatively a full dual basis gives a bounded three-level enumeration for rational input. Use integer equality tests for allowed boundary faces. This gives exact membership for a supplied seven-reflex itinerary. There is no resulting completeness guarantee for a list of bounded-length words at fixed r: the six-reflex bound above already forces arbitrarily many axial reversals. The exhibited long word is itself a repeated excursion, so a bounded list of templates **with unbounded repeat counters** is a separate possibility. The seven-reflex window control previously studied needs only one side reflection for its specified family. [Seven-reflex witness](l1-excursion-normal-form.md)

**Stopping-rule result.** Outcome (b) holds. The finite list of individual vertical itineraries cannot yield H(C), even on the six-reflex chart with its prescribed pinned pair. The first open case for a chart-wide lighting theorem is to choose a repeat count, or a different template, for every remaining free-gap tuple. This result closes the test of the proposed finite list, not the whole chart's illumination problem.
