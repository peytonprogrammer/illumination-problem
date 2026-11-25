Advances: L1 — the horizontal monotone list lights the d233 vertical obstruction with **arbitrary positive integral middle length**, keeping its original end heights. For the full free-gap chart the vertical miss set has an explicit necessary thinness and congruence test. An unbounded region with varying end heights remains undecided by the joint argument. The early-stop clause applies.

### 1. A necessary condition for the vertical miss set V

Use the seven transverse gaps and five axial gaps of the 16-wall chart, with tier intervals (A,G),(A,D),(C,F),(E,H),(E,J), levels y₀,…,y₅ and marks (C,y₁),(G,y₄). In the monotone vertical list write hᵢ for the three axial travels y₂−y₁,y₃−y₂,y₄−y₃, Pᵢ for the doubled tier widths, and T for total travel. The two gate lengths are d₁=D−C and d₂=F−E. A clean superset of V is the miss set of all eight signed monotone cosets. The following computes it from the gaps, including a useful preliminary thinness test.

Form the two rows of the three-column matrix L with entries Pⱼ(Yᵢ/T−1[j<i]), Y₁=h₀,Y₂=h₀+h₁. Let qᵢ be the positive gcd of the entries in row i (clear common denominators and scale back); let Δ be the positive gcd of the three absolute two-column determinants. These are the coordinate projection spacings and the covolume, respectively, by integer column reduction. Necessary for V are **both**

    (d₁≤q₁ or d₂≤Δ/q₁),       (d₂≤q₂ or d₁≤Δ/q₂).

Indeed rows with first-coordinate spacing q₁ have second-coordinate spacing Δ/q₁, and conversely. Strictly wider intervals would hit every translate. For the exact congruence test in this superset, take an integer column combination giving (q₁,t) and use (0,Δ/q₁) for the fiber generator. For every parity take its signed intervals I₁,I₂ and offset v as in d233. For each integer n with v₁+nq₁ in I₁ it is necessary that

    (I₂−v₂−nt) ∩ (Δ/q₁)ℤ = ∅.

Together over the eight parities this characterizes the stated superset, including the case of no candidate row. Both physical gates have corner endpoints in this strict chart. Additional vertical turn words can remove tuples from the superset. Exact V membership, if needed at a tuple, intersects these misses with the bounded signed-word slice tests for ≤2 axial reversals, admitting smooth-wall endpoints with compatible sectors. No flatness converse enters. [Chart, parity offsets and slice tests](l1-two-gate-chart.md)

### 2. A horizontal witness on the N obstruction for every B

Take even N≥40, the d233 transverse supports (0,N−1,N,2N,2N+1,5N/2,3N,4N), and levels −1,0,1,1+B,2+B,3+B with **any integer B≥1**. D233's N/2≤2Aₜ+Aₛ argument is independent of B and puts the entire subfamily in V. For large B with fixed ends the reviewed opposite-end theorem also supplies lighting; that theorem alone imposes no horizontal reversal budget. Here we construct a witness with zero horizontal reversals even for short B. [D233](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d233-review-two-gate-chart/review.md) · [Fixed-end corridor theorem](README.md)

Measure x-travel from S, with total X=3N/2+1. The three column transitions are at travels 1,N+1,N+2. Aim with slope h=K/X, where K≡B mod 2. The first two transmissions must pass (1,B+1), and the third (B+1,B+3). Seek a path going upwards at all three transmissions. Allow j complete transverse periods in the second column, of height B. The actual crossing ordinates are then

    h,       (N+1)h−2Bj,       (N+2)h−2Bj.

If these lie in the three open intervals, a ray exists: it has no turn before the first gate, makes the j complete windings between the first two, and stays in the third column until the third transmission. Beyond that gate the column has height two. At the target abscissa the developed ordinate relative to the chosen middle winding is K−2Bj. It has parity B and therefore folds to the midpoint B+2 of [B+1,B+3]. All intermediate reflections occur on genuine horizontal walls in the corresponding open columns. This last midpoint condition is why a common-period gcd test on all four columns would discard valid witnesses.

For B≥2 set c=(B+2)/2. Choose the nonnegative integer j nearest to ((N+2)c−B−2)/(2B). Set h*=(2Bj+B+2)/(N+2), and choose the integer K of parity B nearest Xh*. Then |h*−c|≤B/(N+2) and |h−h*|≤1/X. The third crossing differs from B+2 by at most (N+2)/X<1. The second differs from c by at most B/(N+2)+(N+3)/X, which is <B/2 for N≥40, B≥2 (use B/42+43/61<B/2). The same bound covers the first crossing. Thus all gates pass strictly.

For B=1 choose K≡5 mod 6 with X<K<2X, so 1<h<2. Since 3(N+1)=2X+1, the second unfolded crossing is (2K+h)/3. Subtracting 2j with j=(K−2)/3 gives (4+h)/3 strictly between 1 and 2. Adding h puts the third crossing strictly between 2 and 4. The same target parity test completes the chord. This proves joint-list coverage on the N subfamily independently of the size or aspect ratio of its middle.

### 3. Unbounded residual and stop

Here is a specific region inside V where this proof stops. For integer m≥2 set N=64m², keep the transverse supports above, and take the five successive axial gap lengths to be

    (m+2, 1, m, 1, m+1).

Normalize y₁=0. The two axial end travels are odd in the d233 comparison, and the end mirrors have the same residues as before. At most two vertical reversals give Aₛ≤3(m+3), Aₜ≤3(m+2), because each monotone piece in its end is at most the full end depth. Thus 2Aₜ+Aₛ≤9m+21<N/2. The entire vertical list is hollow for every m. This is an exact exclusion, valid also for paths meeting admissible smooth-wall gate endpoints.

On the horizontal route the last column now has height m+2 and the target is one unit above its floor. Its two image classes are not the entire parity class used in the proof above. The previous sequential gcd sufficient test gives no replacement here: the three axial prefixes 1,N+1,N+2 are all coprime to X. Indeed 3(N+1)−2X=1 and 3(N+2)−2X=4 with X odd. After the first gate that test has no remaining independent residue and would require the next gate to exceed the whole common period. The exact horizontal cosets retain other windings and both target image classes. Neither their joint hollowness nor a hit in one of the ≤2-reversal lists has been proved on this ray of parameter choices. Fixed-end long-corridor lighting does not resolve it, since the end heights vary as well, and an unrestricted lighting verdict would not decide this list membership.

**Stopping-rule result.** The authorized outcome is the early stop, not (a) or (b). The unbounded residual above is established as a residual of the proof, not as a dark family or a two-list counterexample. There is no explicit H(C) and no seven-reflex follow-on.
