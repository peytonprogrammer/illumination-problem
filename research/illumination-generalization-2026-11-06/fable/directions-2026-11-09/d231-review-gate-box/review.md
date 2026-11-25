# D231 review: the gate-box lemmas (d230, Angle 1)

Advances: L1 (area bound). This review checks the proposed effective height bound H(C) through lattice points in a gate box.

Referee review of `../d230-fresh-angles/README.md`, Angle 1 only. All arithmetic is exact (`fractions`). Rooms are limited to the named ones: the seven-cell room, the parabola family at (m,u) = (3,5), (3,12), (4,7), (6,20), (10,30), and the six-reflex locked-gate family at (a,t,B) = (1,1,1), (1,1,18), (1,2,3). The scripts enumerate only itineraries, parity patterns and winding vectors inside these named rooms; there are no room, direction or size searches.

**CPU budget overrun.** Total CPU was about 12 minutes, against a 10-minute limit. Two early runs hit their wall-clock timeouts (300 s and 200 s) before writing logs, mostly in a brute-force winding search that I later replaced. The last pass (`light2.py`) also timed out on the six-reflex point B=18 roof itinerary and never reached (1,2,3). I stopped computing at that point.

## Verdicts

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Affine map k ↦ u, derivative 2w_j(Y_i/H − [j<i]), legal chords = coset points in the open box | CORRECT WITH GAPS (minor) |
| 2 | Lemma 1: Λ_τ* = {n : Σ n_j μ_j = 0}, ℓ_i = n_{i−1}/(2w_{i−1}) − n_i/(2w_i) | CORRECT |
| 3 | Lemma 2: flatness criterion, constants Flt(1)=1, Flt(2)=1+2/√3 | CORRECT WITH GAPS ("explicit in general" overstated; real rooms need a closure argument) |
| 4 | g=1: \|J\|(h_A+h_B) ≤ 2 gcd(w_A h_B, w_B h_A); "recovers nearest winding" | CORRECT WITH GAPS (formula right; d229's parabola witness is not a g=1 itinerary) |
| 5 | Universal relations encode the midpoint constraint; rational independence forces lighting | Midpoint: CORRECT. Independence: CORRECT but vacuous for lattice rooms. Implied use ("universal relations need thin boxes"): WRONG |
| 6 | Parabola hand check: for large m,u the monotone itinerary has no short relation | WRONG |

## Claim 1: the coset parametrization

**Re-derivation.** In visit j the slab interval is (a_j, a_j+w_j). Let p be the signed horizontal travel per unit of absolute vertical travel, σ_j the cumulative sign from odd visits, and u_i = σ_i x_i. Folding one visit gives

    u_{j+1} = u_j + p h_j − c_j − 2 w_j k_j,   c_j = 0 (even visit) or 2σ_j a_j (odd visit).

The endpoint equation σ_{g+1} T_x = x_0 + pH − Σ_{j≤g}(c_j + 2w_j k_j) fixes p. Substituting it gives the note's derivative, 2w_j(Y_i/H − [j<i]). Horizontal-wall turns don't change v_x, and Y counts absolute vertical travel, so turns need no special case. The parity pattern (2^{g+1} choices) changes only c_j and the signs σ_i. A box interval maps to σ_i J_i, which has the same length. The script's finite differences matched Φ exactly in every itinerary of the seven-cell and parabola (3,5) runs (`deriv_bad=0`).

**Open box ⇒ legal chord.** Every polygon vertex lies on a level, so an open slab has only smooth vertical sides. Open J_i excludes every corner. The fold is self-consistent because x_i ∈ J_i lies inside both adjacent slab intervals. Non-corner lattice points don't matter. Passing through T early still lights the pair. Exact traces confirmed this. In the seven-cell room every box hit for every itinerary with g ≤ 4 traced to a legal ray that follows the itinerary and ends at T. In parabola (3,5) and (3,12) every box hit that could be traced also passed.

The first full run reported four "soundness failures" for g=4. These came from a tracer bug that recorded level crossings within one segment in level order, not time order. A debug trace showed the correct events, and after the fix all those hits traced correctly.

**Gap 1 (legal chord ⇏ open-box point).** A ray can hit a smooth vertical wall exactly on a level, where the wall continues across that level. Examples are x=3 at y=1 and x=0 at y=2 in the seven-cell room, x=0 at y=u−1 and y=u in the parabola family, and x=16t at y=D in the six-reflex family. That ray is legal, but its event abscissa is an endpoint of J_i, which the open box excludes. The fix is to close each endpoint of J_i that is a smooth wall point. Lemma 2 is unaffected because it only uses open box ⇒ chord. The tracer flags such chords, but none appeared in the enumerated seven-cell windings.

**Gap 2 (bookkeeping).** A mark on a level, such as pinned S=(0,0), starts with a full-height visit h_0. A mark strictly inside a slab gives a partial h_0 or h_g. In that case a later full visit to the same slab has a different μ and creates no universal relation. The note doesn't say this, and it matters for Claim 5. Non-primitive chords need no special case.

## Claim 2: Lemma 1

Independent derivation. ℓ ∈ Λ* iff ℓ·Φe_j = 2w_j(L − t_j) ∈ ℤ for all j, with L = Σℓ_iY_i/H and t_j = Σ_{i>j}ℓ_i. Put n_j = 2w_j(t_j − L). Abel summation gives Σ t_j h_j = Σ ℓ_i Y_i = LH, so Σ n_j μ_j = 0. Conversely, take n with n·μ = 0. Then t_j = L + n_j/(2w_j), t_g = 0 forces L = −n_g/(2w_g), and the relation makes this L consistent with Σℓ_iY_i/H. The map n ↦ ℓ is injective: ℓ = 0 forces n_j = 2w_j c, and then n·μ = cH = 0. So it is an isomorphism, and the sign convention matches the note.

**Rank.** In a lattice room μ is rational, so the integer kernel of Φ has rank 1 (k ∝ μ) and Λ_τ is a full lattice of rank g in ℝ^g. In a real room with μ not proportional to an integer vector, Λ_τ has rank g+1 and isn't discrete.

**Numerical check.** For every itinerary analysed, the ℓ(n) built from a ℤ-basis of {n·μ=0} lie in the directly computed Λ* and have the same covolume (`lemma1=True` everywhere; 9 seven-cell itineraries, 5 parabola points, 2 six-reflex points).

## Claim 3: Lemma 2 (flatness)

**What is proved.** Suppose an open box misses a coset v+Λ of a full-rank lattice in ℝ^g. Then some nonzero ℓ ∈ Λ* has Σ|J_i||ℓ_i| ≤ Flt(g). To get this, apply flatness to a slightly smaller closed box (its interior is lattice-free) and pass to the limit; Λ* is discrete. The inequality is non-strict, and it is only a necessary condition for darkness.

**Constants.**
- Flt(1) = 1. This is elementary: an open interval of length greater than 1 contains an integer.
- Flt(2) = 1+2/√3 ≈ 2.1547. Confirmed: C.A.J. Hurkens, "Blowing up convex sets in the plane", *Linear Algebra Appl.* 134 (1990), attained by a triangle.
- g ≥ 3: "explicit in general" is overstated. Exact values aren't known for g ≥ 3. Polynomial upper bounds exist: Kannan–Lovász O(g²); Banaszczyk–Litvak–Pajor–Szarek O(g^{3/2}); Rudelson; Reis–Rothvoss polylog·g. I didn't confirm explicit numerical constants for these bounds.
- The lower bound Flt(g) ≥ g is elementary: the open simplex {x>0, Σx<g} is hollow with width g.

**Real rooms.** Flatness needs a discrete lattice. The fix: the closure of Λ_τ is V ⊕ L. Because the box is open, it misses v+Λ iff it misses v+closure. Projecting along V and applying flatness gives the same conclusion with Flt(g − dim V) ≤ Flt(g), and Flt is nondecreasing.

**Consistency check.** The script never found a hollow coset for g ≤ 2 whose minimum width exceeded Flt(2) (`flat_bad=0`).

## Claim 4: g = 1

Λ is generated by −2w_Ah_B/H and 2w_Bh_A/H, so its spacing is d = 2gcd(w_Ah_B, w_Bh_A)/H. A hollow open interval needs |J| ≤ d, and in one dimension this is the exact criterion for each parity coset. Lemma 1 gives the same result: the minimal n_B = w_Bh_A/gcd yields |ℓ| = H/(2gcd).

**Gap.** "Recovers nearest winding" is loose. In the parabola family, d229's itinerary has g = 2: gates at y=m (0,1) and y=u−1 (0,m), with slab widths 2, m, m+2. The roof variant has g = 4. d229's nearest winding is a one-coordinate rounding with the upper windings held fixed, taking both parity patterns together; that is why its spacing is 2U/u. It is the projection of the g=2 coset onto u_1, not a g=1 instance. The two methods agree only as heuristics.

## Claim 5: universal relations and independence

**Midpoint constraint: correct.** For a turn in slab j, take n = e_j − e_{j+1}. Then ℓ = (−1/(2w), 1/w, −1/(2w)) on the entry, turn and exit events, and ℓ·u ∈ ℤ + c is the folded midpoint relation X_a − 2X_b + X_c ≡ const.

**Main finding: universal relations are always short.** Take two full-height visits to one slab. Their relation has width at most (sum of at most four gate lengths)/(2w), and each gate is at most w, so the width is ≤ 2. With a turn the bound is (|J_a| + 2|J_b| + |J_c|)/(2w) ≤ 2. Any itinerary with a repeated full-height visit has g ≥ 2, and Flt(g) ≥ min(Flt(2), g) > 2. So **Lemma 2 can never certify lighting along an itinerary with a repeated full-height slab visit**, whatever the box thickness. The check agrees: 33 universal relations in the seven-cell room and 1 in parabola (3,5), none of width above 2 (`univ_long=0`).

Two statements in d230 are therefore wrong:
- "Universal relations need thin boxes, which cost exposed walls" (open step 2). They need no thinness at all.
- "Each relation bounds a modulus ratio." A universal relation has ratio 1 and bounds nothing.

A thin-box statement does hold for the sharper one-direction test, where the projection of the box onto ℓ misses ℓ·v + ℤ. That test needs width < 1, and it isn't Lemma 2.

**Rational independence.** Λ_τ is dense iff μ has no nonzero integer relation (Kronecker), and then the open box is hit. This is correct. But in a lattice room every μ_j is rational, so the hypothesis never holds for g ≥ 1. Any repeated slab also breaks it. It applies only to real rooms (L3).

**Six-reflex lock.** For the monotone itinerary at (a,t,B) = (1,1,1) and (1,1,18), all 8 parity cosets are hollow. The minimal relation is ℓ = (−1/16, −1/16) with width 1/8, from n = (1,0,−1): the two end slabs have equal moduli μ_0 = μ_2 = a/(16t). This is d230's "end-phase" lock. Its width 1/8 < 1 means the obstruction is a projection miss in one direction, which is exact. So the criterion is consistent with the lock but only as a necessary condition. The roof itinerary at (1,1,1) has 2 of 32 cosets lit, but its minimal width is 5/8, so the criterion gives no certificate. I didn't trace those hits. Budget ran out before the B=18 roof itinerary and the point (1,2,3).

## Claim 6: parabola hand check

For the monotone itinerary (gates (0,1) at y=m and (0,m) at y=u−1):

| (m,u) | covol Λ | min width | minimizing ℓ | lit cosets | certified (> 2.1547)? |
|---|---|---|---|---|---|
| (3,5) | 4/5 | 5/2 | (5/2, 0) | 8/8 | yes |
| (3,12) | 1/3 | 2 | (−2, 0) | 8/8 | no |
| (4,7) | 32/7 | 9/8 | (−5/8, 1/8) | 6/8 | no |
| (6,20) | 4/5 | 5/2 | (−5/2, 0) | 8/8 | yes |
| (10,30) | 8/15 | 3/4 | (3/4, 0) | 8/8 | no |

The pair is lit at all five points, so there is no contradiction with d229, but the criterion certifies only 2 of them.

**Minimal counterexample family.** Take ℓ_2 = 0, so n_1/(2m) = n_2/(2(m+2)) = s and n_0 = −4sU/m. This relation has width s·u/m. For even m with m | U, s = 1/4 is admissible, giving width (1 + U/m)/4. That is ≤ Flt(2) whenever U ≤ 7m. So for every even m and U ∈ {m, 2m, …, 7m}, the monotone itinerary has a short relation. Example: (10,30) gives width 3/4.

The roof itinerary always has a universal relation (Claim 5); at (3,5) its minimum is 13/12. Therefore "for large m,u the monotone itinerary has no short relation" is false along an infinite family. The criterion does **not** reproduce d229's "lit for all m ≥ 3, u ≥ m+2". The pairs are lit, but Lemma 2 is silent on them.

## Scripts and output

- `gatebox.py`: polygon builder, exact polygon billiard tracer, itinerary enumerator, coset map (my derivation), lattice/HNF, Lemma 1 check, LLL and min width, exact coset hollowness, and the A-versus-B comparison driver. The event-order bug is fixed in this version. `run.out` is a partial log from **before** that fix, so its four g=4 "SOUNDNESS FAIL" lines are tracer artifacts. Its other totals stand: seven-cell g ≤ 4 and parabola (3,5) have `BnotA_bad=0`, `BnotA_boundary=0`, `deriv_bad=0`, `lemma1_bad=0`, `flat_bad=0` and `univ_long=0`.
- `light.py`: lattice pass plus exact traces of every box hit. Seven-cell, all 9 itineraries with g ∈ {2,4}: every hit traced OK. Parabola (3,5) and (3,12): traced hits OK; some hits needed |k| > 6 and weren't traced. The run timed out after (3,12), so no `light.log` was written. Results are copied above.
- `light2.py`: lattice-only pass, the source of the Claim 6 table and the six-reflex figures. It timed out before writing `light2.log`; results are copied above.

## Which lemma does this advance, and what is the first case still open?

It advances **L1**, but only through itineraries with no repeated full-height slab visit. For every other itinerary, Lemma 2 is automatically satisfied, so darkness carries no information through it.

A valid restatement: a dark pair forces a short relation on every itinerary τ whose full-height visits use distinct slabs. In a room with N slabs there are finitely many such itineraries, at most about N!·(branching), with g < N. That finite family is the natural object for d230's persistence step. Turns and excursions have to be handled by a sharper projection test, not by Lemma 2.

**First open case.** The parabola family with m even and m | U ≤ 7m, for example (m,u) = (10,30). The pair is lit by d229. The monotone itinerary has a short relation (width 3/4), and the roof itinerary has a universal relation, so Lemma 2 certifies nothing. A working version of the route must certify this pair some other way. Flatness can't do it here. A one-direction projection test can only prove hollowness, never lighting. What works at a fixed point is the exact finite coset enumeration, which finds 8/8 cosets lit; the open step is a family-wide version of it. Until a certificate like that is proved for a whole family, the persistence step cannot start from Lemma 2 as stated.
