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

**The d213 stress test at t=15.** The gains 15 and 21 send the area-18 marked template to area 18+3(15+21)=126. In the lower-first order the only first-stage slope is 15/19; in the upper-first order they are 3/5 and 21/25. The three strict last windows reported by d213 contain no integer congruent to 3 modulo 6. On the simultaneous lift the marked chord has displacement (3,40) and crosses the three interfaces at **83/40, 131/40, 197/40**, respectively. Their minimum distance to an overlap endpoint is 11/40. It follows that the two gains may be restored together with strict clearance. This room requires no new base check. D213 found 135 misses of the strict family in the first 200 lengths; the simultaneous proof above covers all 200 and all later lengths. [d213 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d213-review-marked-selection/review.md)

**An exact ratio region for convex tiers.** Keep the transverse tier intervals and the marked abscissae fixed. For a monotone direct chord let hⱼ>0 be the axial lengths between successive interfaces and endpoints, H their sum, and Hᵢ their partial sums. At interface i with open overlap (aᵢ,bᵢ) impose

    (aᵢ−x_S)H < (x_T−x_S)Hᵢ < (bᵢ−x_S)H.

These strict linear inequalities give the exact region for crossings inside the open overlaps. Their intersection is a convex cone in the hⱼ, with rational coefficients for lattice rooms. Necessity comes from the chord equation; sufficiency follows tier by tier from convexity. Thus if two realizations satisfy the tests, interpolating their axial lengths also preserves the itinerary. For t=15 this certifies the entire straight deformation in gain space from (0,0) to (15,21), even though the two one-at-a-time gate tests miss. On a face where one hⱼ goes to zero, strict inequalities at both of its interfaces certify passage through their common open overlap for nearby positive lengths. Equality on the face requires a separate argument.

**Multi-band lemma.** In a fixed marked orthogonal chart, normalize the two axes independently by positive scale factors after translation to their minima. Suppose the gap ratios converge to a positive vector on each axis and the proposed template wall itinerary, developed in the **limit** room, joins the limit marks regularly. Then every sufficiently near ratio vector admits that itinerary. Unfold the indicated copies. The endpoint images and edge endpoints depend continuously on the gap vectors. Each prescribed transverse edge hit persists in its open edge and in strict order; each leg keeps positive clearance from the nonincident edges. Folding the segment gives the seed. This argument requires regularity at the limiting ratios; a seed checked at unit ratios alone certifies only its own open neighborhood. Irrational gap ratios cause no change in the proof. [Perturbation and marked templates](l1-descent-skeleton.md)

Compressing **both axes** to unit marked gaps gives template area ≤11²=121. The finite marked-template target below plus a proof that seed itineraries cover all target ratio regimes would suffice. The census is reviewed only through 21. The number 121 bounds the template, not the area of a general ratio representative or the threshold of an arbitrary itinerary. Uncertified positive ratios can remain open even before reaching a degenerate ratio. In the named staircase the fixed-height end tiers themselves vanish under axial normalization; the explicit interface calculation above checks their gates separately.

## Follow-on: one vanishing scale

**Transparent collapsing band.** Suppose one normalized horizontal band thickness tends to zero and the other normalized gaps stay positive. Keep a regular limit itinerary away from the collapsed level. At each encounter with that level require a transverse crossing, with abscissa strictly inside a common open interval of the two adjacent pieces and a component of the missing band. Assume the endpoints lie away from that level. The crossing persists after reinsertion of any sufficiently small positive normalized thickness. Indeed take a small open rectangle about each crossing abscissa contained in that common column on both sides and throughout the inserted component. The unfolded perturbed chord crosses both interfaces there in order, and its transverse drift between them tends to zero by transversality. Outside these finitely many neighborhoods use ordinary itinerary stability. This proves a one-vanishing-ratio lift even for an irregular band, conditional on the common-overlap crossing. Repeating it requires compatible crossings at each successive scale. A corner hit, a missing overlap, a reflection in the disappearing layer, or a mark carried by it is not covered.

**A two-scale theorem when the direct limiting chord fails.** In the staircase let x now denote the *smaller* of its two gains, y the larger, and restore x first. Either order has the first-lift slope window (1/2,1). For x≥9, D=4+x>12, so (D/2,D) has length greater than six and contains an integer 3+6n. Use its quotient by D as the passing parent slope. Its reduced denominator is ≤D. The remaining unit band is crossed once, its width is three, and M≤D in the reviewed level-error bound. Consequently

    x≥9 and y>3(4+x)²−(4+x)

guarantee a passing last lift in the actual one-band parent. This proves strict selection eventually when x→∞ and y/x²→∞. Only the explicit area-18 template chord is needed for this family. The comparison uses the denominator of the seed actually inherited by the second parent; a separation merely by y/x→∞ gives no such inequality.

**First open cases.** For strict marked selection the comparable √2 family outside the certified arithmetic classes remains open, despite its all-t direct chord. For a scales-only selection argument, a concrete gap between the proofs is x→∞, y=⌊x^(3/2)⌋: the middle direct gate eventually fails and the quadratic domination estimate does not apply. Individual congruence classes may still pass. Neither positive-density all-itinerary failure nor a universal induction on the number of scales follows.

## Exact finite base for marked descent (supersedes the area-census proposal)

**Base theorem target.** Every member of the following finite class F is lit. One member is a room **with one unordered marked pair**; a room with several qualifying pairs has several obligations. Use translation and the eight square symmetries to take one representative per orbit.

1. Take a strictly simple orthogonal lattice polygon with 10, 12, 14, 16, 18 or 20 maximal walls, and two distinct interior lattice marks S,T. Translate the minima on both axes to zero. Let X be the set of vertical-wall abscissae and Y the set of horizontal-wall ordinates. Write Bₓ,Bᵧ for the box spans.
2. Require both exact equalities

       X ∪ {Sₓ,Tₓ} = {0,…,Bₓ},       Y ∪ {Sᵧ,Tᵧ} = {0,…,Bᵧ}.

   Thus a missing interior wall level must be supplied by one of these very marks. Using different pairs to fill the two coordinate lists is invalid.
3. Keep only area >21 and pairs whose open straight segment is not contained in the room interior. The reviewed through-21 result, Theorem S for at most eight walls, and direct visibility supply the other leaves. The projection of F onto canonical rooms is the requested room list; within each such room only the retained pair orbits need a verdict. [Reviewed reductions](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d70-writeup/RESULTS.md)

**Why this particular base.** Sort the wall and mark levels independently on each axis and replace the distinct values by their ranks starting at zero. Extend this map monotonically and piecewise linearly between levels. It preserves simplicity, incidence, turns, interior marks and their distinctness. It produces the unique all-unit realization of that marked order type. Conversely both equalities in item 2 say exactly that no refined band on either axis can be shortened while preserving those strict level orders. Every such leaf is its own rank template. This is the exact irreducible base for this move, after the three specified discharges. Minimality here is structural: another lighting theorem may discharge more leaves. It is not a claim about a minimum number of machine checks among all possible proofs.

**The quantifier that must change.** Base theorem F plus the existing through-21 result implies orthogonal lattice L1 **if** every reducible marked room of area >21 with lit smaller parents admits a passing lift from one such parent (or an independently proved lighting construction). At a least dark pair, either its template is already itself, in which case the base discharges it, or there is a strictly smaller eligible parent and the lift hypothesis applies. In particular selection is needed also at reducible areas **22 through 121**. The former conditional statement with selection only above 121 would leave those rooms unaccounted for. An ordered lift from every all-unit chart to every realization is an alternative sufficient hypothesis. Lighting F alone proves neither selection nor ratio coverage.

**Size bound without enumerating rooms.** There are at most eleven gaps on either axis, so Bₓ,Bᵧ≤11. The following purely combinatorial bound is **867,415,174,096,573,784 marked pair orbits** (rounded up), hence also bounds the number of rooms. It is an upper bound, not a workload forecast. For a reproducible calculation set

    f(z) = Σ_{j=1}^{10} zʲ/(2j)!,
    P(k) = (k−2)(2k−3) + (k−1)(2k−1).
    Bound = ceil(½ Σ_{m=5}^{10} (2m)! · (Σ_{k=2}^m P(k)[zᵐ]f(z)^k)²).

For W=2m, put one vertex at each occupied entry of a zero-one matrix indexed by the ranked wall levels. Every used row and column has positive even degree (wall endpoints), and there are 2m entries equal to one. For ordered row degrees dᵢ and column degrees eⱼ the matrix count is at most (2m)!/(∏dᵢ!∏eⱼ!): match individually labeled stubs at the two sets of levels and discard parallel edges. The vertex set determines the walls, since consecutive endpoints on each support line must pair in order to form disjoint wall interiors. Invalid or disconnected polygons only increase the bound. The coefficient above sums the reciprocal factorials for one axis. On k wall levels the first mark coordinate either selects one of k−2 interior levels or inserts a new level in one of k−1 gaps. The second then has respectively 2k−3 or 2k−1 choices. This gives P(k). Squaring combines the axes. After excluding coincident marks, swapping the labels acts freely before quotienting spatial symmetries, which justifies the factor ½ as an upper bound.

The definition gives an exact generator if the finite target is ever checked: generate ranked vertex matrices and mark orders, pair wall endpoints, discard invalid polygons and marks, apply items 1–3, and deduplicate by symmetry. There is no enumeration over arbitrary room areas. No such run was performed. Ratio-limit rooms are not an alternative finite base at present: the normalized ratios form a continuum, and no finite itinerary cover including the degenerate strata has been proved. The proposed computation is confined to F; proving the lift or finding its obstruction remains the theorem-level frontier.


### An exact room-first count for the proposed finite class

For each unmarked room P up to translation and square symmetry within the specified box, wall and area limits, form a set M of **tagged** missing wall levels (vertical or horizontal). Reject P if either axis is missing more than two levels. Let G be the subgroup of square symmetries restoring this normalized room. For J⊆M discard each interior lattice mark on any level in J. Let C(g,J) count the unordered nondirect pairs of the remaining marks fixed *as an unordered pair* by g. This includes two individually fixed marks and a pair interchanged by g. Then the exact contribution of P to the finite target is

    (1/|G|) Σ_{g∈G} Σ_{J⊆M} (−1)^|J| C(g,J).

Inclusion–exclusion removes exactly the pairs that leave some required level unfilled. Averaging counts one representative per surviving symmetry orbit. The inner sum has at most 16 terms. In the most constrained case (two missing levels on each axis), the only possible pairs are the two diagonals of the rectangle of missing-level intersections. Either diagonal is retained only if both endpoints are interior and its open segment fails direct visibility. A room contributes if and only if its integer contribution above is positive. This gives an exact count specification, rather than treating all marks in a qualifying room as obligations. The earlier numerical bound remains an upper bound; no template enumeration was run.

The theorem still needed after the redirect is **coverage by simultaneous lifts or other proved lighting constructions for every nonterminal marked realization above area 21**. The strict single-band parent at t=15 is unnecessary for that theorem. A concrete open regime for the current staircase constructions remains x→∞, y=⌊x^(3/2)⌋ outside their certified subfamilies: the direct-chord cone is left, and the quadratic scale-separation estimate does not yet apply.
