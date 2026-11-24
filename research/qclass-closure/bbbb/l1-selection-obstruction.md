Advances: L1 — simultaneous marked lifts and a two-scale single-band selection theorem for the offset staircase. The all-itinerary obstruction in (a) remains undecided.

## What density says about the strict test

In the four-tier staircase write x=t, y=⌊√2 t⌋ for the gains, D=4+x, H=x+2. For the increasing-axial template branch, a candidate parent slope is s=(3+6n)/D in (1/2,1). Its strict last window uses the nearest rationals l<s<u with denominator at most H. If s=a/b in lowest terms, each distinct i/j has |a/b−i/j|≥1/(bj). Hence the numerator window has width **at least 2(D+y)/(bH)**. The proposed order (D+y)/H² is not uniform over the candidate slopes. Even for large b there are order D candidates; the width of one window is not a bound on the density of their union. [Signed test and construction](l1-marked-selection.md)

In fact the passing set for this very branch has **positive lower natural density**. The following disjoint subfamilies already suffice.

- For t≡y≡0 mod 8 the template slope 3/4 replays exactly in both width-three bands, since either added phase is divisible by 6. Density 1/64.
- For t≡17 mod 42 and y≡±17 mod 42, use 5/7. The parent numerator (4+t)5/7 is 3 mod 6 and the last phase is within 1/7 of a multiple of 6. The resulting level error is at most H/[7(D+y)]<1/7, strictly inside every gate. Density 2/42². Both gains are odd here, so no crossing seed can replay exactly.

For the density computation, on t=mk+r the fractional parts of k√2+r√2/m are equidistributed. The event ⌊√2 t⌋≡j mod m is an interval of length 1/m. Equidistribution follows from the geometric-series bound on every nonconstant integer Fourier mode and the equidistribution criterion. Thus the lower bound is 1/64+1/882. This rules out zero-density **success** even in the proposed family. It leaves open positive-density **failure**, which is a different claim. To prove (a) negatively one must also exclude both restoration orders and trajectories that reverse axial velocity. The Farey test characterizes just one itinerary family. I have neither that exclusion nor a construction passing for every t.

## Simultaneous lift: an exact answer for the marked pair

The two end interfaces of the specified staircase are at transverse coordinates 2+3/D* and 5−3/D* on the direct chord, where D*=4+x+y. The middle interface is at 2+3(2+x)/D*. The end crossings are inside (1,3) and (4,6) for all nonnegative gains. The middle crossing lies strictly inside (3,4) exactly when

    y < 2x+2    and    x < 2y+2.

Each chord segment then stays inside its convex tier until the next crossing. For x=t, y=⌊√2 t⌋ both inequalities hold for **every integer t≥0**. The all-unit-height area-18 template and the final room have the same regular three-interface chord itinerary. This proves the simultaneous lift directly, regardless of the answer to (a). The limiting middle abscissa is 2+3/(1+√2), strictly between 3 and 4.

**Multi-band lemma.** In a fixed marked orthogonal chart, normalize the two axes independently by positive scale factors after translation to their minima. Suppose the gap ratios converge to a positive vector on each axis and the proposed template wall itinerary, developed in the **limit** room, joins the limit marks regularly. Then every sufficiently near ratio vector admits that itinerary. Unfold the indicated copies. The endpoint images and edge endpoints depend continuously on the gap vectors. Each prescribed transverse edge hit persists in its open edge and in strict order; each leg keeps positive clearance from the nonincident edges. Folding the segment gives the seed. This argument requires regularity at the limiting ratios; a seed checked at unit ratios alone certifies only its own open neighborhood. Irrational gap ratios cause no change in the proof. [Perturbation and marked templates](l1-descent-skeleton.md)

Compressing **both axes** to unit marked gaps gives template area ≤11²=121. A census through 121 plus a proof that the seed itineraries cover all target ratio regimes would suffice. The census is reviewed only through 21. The number 121 bounds the template, not the area of a general ratio representative or the threshold of an arbitrary itinerary. Uncertified positive ratios can remain open even before reaching a degenerate ratio. In the named staircase the fixed-height end tiers themselves vanish under axial normalization; the explicit interface calculation above checks their gates separately.

## Follow-on: one vanishing scale

**Transparent collapsing band.** Suppose one normalized horizontal band thickness tends to zero and the other normalized gaps stay positive. Keep a regular limit itinerary away from the collapsed level. At each encounter with that level require a transverse crossing, with abscissa strictly inside a common open interval of the two adjacent pieces and a component of the missing band. Assume the endpoints lie away from that level. The crossing persists after reinsertion of any sufficiently small positive normalized thickness. Indeed take a small open rectangle about each crossing abscissa contained in that common column on both sides and throughout the inserted component. The unfolded perturbed chord crosses both interfaces there in order, and its transverse drift between them tends to zero by transversality. Outside these finitely many neighborhoods use ordinary itinerary stability. This proves a one-vanishing-ratio lift even for an irregular band, conditional on the common-overlap crossing. Repeating it requires compatible crossings at each successive scale. A corner hit, a missing overlap, a reflection in the disappearing layer, or a mark carried by it is not covered.

**A two-scale theorem when the direct limiting chord fails.** In the staircase let x now denote the *smaller* of its two gains, y the larger, and restore x first. Either order has the first-lift slope window (1/2,1). For x≥9, D=4+x>12, so (D/2,D) has length greater than six and contains an integer 3+6n. Use its quotient by D as the passing parent slope. Its reduced denominator is ≤D. The remaining unit band is crossed once, its width is three, and M≤D in the reviewed level-error bound. Consequently

    x≥9 and y>3(4+x)²−(4+x)

guarantee a passing last lift in the actual one-band parent. This proves strict selection eventually when x→∞ and y/x²→∞. Only the explicit area-18 template chord is needed for this family. The comparison uses the denominator of the seed actually inherited by the second parent; a separation merely by y/x→∞ gives no such inequality.

**First open cases.** For strict marked selection the comparable √2 family outside the certified arithmetic classes remains open, despite its all-t direct chord. For a scales-only selection argument, a concrete gap between the proofs is x→∞, y=⌊x^(3/2)⌋: the middle direct gate eventually fails and the quadratic domination estimate does not apply. Individual congruence classes may still pass. Neither positive-density all-itinerary failure nor a universal induction on the number of scales follows.
