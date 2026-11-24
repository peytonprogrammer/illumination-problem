Advances: L1 — marked band selection at the prescribed height. Ordered parallel lifts work for a certified class of comparable gaps, including bounded offsets from exact replay. An arbitrary successful first lift need not preserve a passing seed for the second.

## Template size and the conditional theorem

Fix both marks as supporting levels in each coordinate. There are at most 11 refined gaps on each axis. Replacing **all** gaps on both axes by one gives a strictly simple lattice room of area at most **121**, with both marks still distinct and interior. Compressing only the selected axial gaps to one gives no such absolute bound. If all compressed-parent axial gaps are ≤b and the transverse span is B, its area is at most 11bB. For example, if the transverse refined gaps are ≤c, the census needed for these parents is at most **121bc**. An arbitrarily long untouched transverse span already precludes a fixed area estimate for a rectangle of fixed positive compressed height.

**Conditional selection theorem.** A census through 121 suffices if every marked room above that area admits an ordering of its nonunit refined gaps and a seed in its all-unit template which passes at every restoration. At the last restoration all the other gaps have their original lengths, so this gives the single-band parent and passing seed asked for. More generally, by strong induction one may start from *any* smaller parent obtained by compressing a nonempty subset, provided an ordered passing chain from that parent is proved. Only the census through 21 is currently available. The assertions below prove sufficient conditions for a chain; they do not assume that an arbitrary seed has the required property. [Band selection and the area induction](l1-descent-skeleton.md)

## The compatibility invariant for a parallel stage

Use the axial coordinate as time in a developed seed. Let U,D be the positive integer transverse and axial travels of its **whole** path. At a still-unit band j write m for the number of visits and Q for the lcm of the visited widths. A missing band needs no test. For an insertion E and integer winding choice N the updated travels are

    U′ = U+2QmN,       D′ = D+mE,       s′=U′/D′ > 0.
    R = 2QN D − E U.

At old integer time t let b(t) be the number of completed j-visits. The signed change in the developed coordinate, after subtracting the whole periods, is

    e(t) = [mt−Db(t)] R/(D D′).

Use the strict gate test of the skeleton. In particular a sufficient test is

    m D |R| < D′ gcd(U,D).                                      (1)

Indeed |mt−Db(t)|≤mD, and every nonintegral base coordinate has clearance at least gcd(U,D)/D from an integer. At integral coordinates strict simplicity and regularity supply the usual two-sided continuation. This proves (1) also at levels *inside every previously enlarged band*. If it passes, the same components and axial visits of every not-yet-enlarged parallel band persist by level induction. Thus the next m and Q come from the original itinerary, whereas **U,D and the gate clearances must be updated**. Axis-parallel seeds carry over separately. For stages on the other axis the roles must be exchanged and its visit data taken from the current seed.

Two unrestricted-height cases follow immediately. If the current slope satisfies E U/D ∈ 2Qℤ, take the exact winding; R=0. A chain of such stages, checking the actual widths at each change of axis, passes from the area-121 template. Also, if the template has U=1, use N=0 on every parallel lift, in any order. Every internal integer level before and after each lift lies strictly in the same open unit transverse interval between the endpoint coordinates; the endpoints agree. Thus arbitrary parallel height ratios pass for this seed, even if (1) is inconclusive.

## Comparable gaps beyond exact replay

Here is a class where choosing the first seed to serve the **next** parent gives an all-large-length theorem. Start with a fixed marked template and fixed seed of travels U,D. Choose a first visited band of multiplicity m₀. Assume its signed gate interval for the *new slope* has zero in its closure. This is a finite check: intersect the strict affine level inequalities with s>0. The interval contains s₀=U/D, hence all 0<s≤s₀. Insert E₀ using N₀=0. This passes for every E₀ and produces slope U/T where T=D+m₀E₀. Maintaining a bounded transverse travel here matters more than minimizing the parent's slope change.

For the remaining parallel bands in a specified order, suppose their actual insertions are

    Eⱼ=cⱼT+bⱼ,     cⱼ>0 rational,   cⱼU = 2QⱼNⱼ,  Nⱼ integral.

Take only T giving integral nonnegative insertions. The offsets bⱼ are fixed integers. Before each stage put A=1+Σ mᵢcᵢ and B=Σ mᵢbᵢ over stages since the first lift and strictly before j. Set A′=A+mⱼcⱼ, B′=B+mⱼbⱼ. The current travels are UA and AT+B, and the next travels are UA′ and A′T+B′. In (1) the large terms cancel *exactly*:

    Rⱼ = U(cⱼB−bⱼA).
    mⱼ(AT+B)|Rⱼ| < A′T+B′                                    (2)

is sufficient. If mⱼA|Rⱼ|<A′ at every stage, the entire chain passes for all admissible T larger than

    max over j of (mⱼB|Rⱼ|−B′)/(A′−mⱼA|Rⱼ|),

with positive path lengths as above. This proves preservation of a passing seed through the later multi-band parents in this regime. For bⱼ=0 throughout, all subsequent stages replay exactly. Nonzero offsets also pass: for U=1, one subsequent once-crossed band, c=2Q and b=1, (2) reads T<(1+2Q)T+1. More generally (2) is a usable check for seeds with U>1, without replacing the determinant by its worst possible rounding error. These are same-axis conclusions with template-area bound 11bBₓ when compressing y (b bounds the template's vertical gaps). They give a last-band selection in the final room when the transverse coordinates were already final; a two-axis application requires a successful transition between the stages on the two axes.

For a nonunit transverse example, use left-aligned tiers of widths 4,5,6 on y-intervals [0,2], [2,3], [3,5], with S=(1,1), T=(3,4). The direct template seed has U=2,D=3. Restore [2,3] first with N₀=0: at the two internal base times the old transverse offsets 2/3 and 4/3 become 2/T and 2−2/T, strictly within the same unit gates for every T=3+E₀. Restore [3,4] next with E₂=6T+1 and N₂=1 (Q₂=6, m₂=1). The determinant is −2, so (2) is 2T<7T+1. The inherited seed passes at the actual second height despite its phase increment 12+2/T being outside 12ℤ. This proves marked selection for this entire comparable-growth progression using just its explicit template chord.

## An exact first lift can be the wrong choice

Take a two-tier room, left aligned, with two rows of width 4 and above them two rows of width 5. Mark S=(1,1) and T=(2,3). The two refined horizontal bands between their levels each have height one. The template area is 18. Grow the lower band by 80n and the upper by 80n+10, n≥1. This is symbolic and uses no new census.

The template direct seed has s₀=1/2. Exact replay through the lower band works since its added transverse travel is 40n, divisible by 8. In this parent the seed has D=2+80n and meets the interface at t=1+80n at a half-integral developed coordinate. For the upper lift, m=1,Q=5, and (80n+10)s₀ is 5 modulo 10. Every winding gives |δ|≥5/(12+160n). At the interface, before any upper traversal, the error is tδ. Its magnitude exceeds 1/2 for every n≥1. **No winding passes the upper gate for this replayed seed.** Yet choosing N=0 in the first lift and again in the second works by U=1. The ratio of the two gains tends to one. This rules out the inference that one may choose any successful lift and then appeal again to the template clearance.

## Where the ratio restriction comes from

There is also a necessary condition on an extensive earlier traversal for the strict test. Suppose in a previously restored band the current increasing developed x crosses two consecutive transverse integers at times at least one full axial unit from either end of the traversal, with 0<s<1. At the next parallel lift this earlier traversal is retained. The correction from the newly chosen band is constant there. For a nonintegral crossing time τ, the two neighboring integer levels bracket that same transverse integer strictly for the perturbed ray if it passes. For integral τ use τ−1,τ+1. Thus each matched crossing time shifts by at most one old unit in local axial time. Subtracting the two crossing times gives

    |1/s′ − 1/s| ≤ 2.                                            (3)

The period offset is constant between the two crossings, so it has no effect on their spacing. This test concerns the integer gates of a *particular parent seed*. A regular geometric path can violate this certificate.

For example, with just two growing parallel bands take E₁=t, E₂=⌊√2 t⌋. After a bounded winding in the first stage the transverse travel U₁ is a fixed positive integer along a subsequence; D₁=D+m₁t. With another bounded winding, U₂=U₁+2Q₂m₂N₂, D₂=D₁+m₂⌊√2 t⌋. If the earlier traversal has the two crossings above, (3) forces equality of the leading coefficients of D₁/U₁ and D₂/U₂, namely

    √2 U₁ = 2Q₂ m₁ N₂,

which is impossible. This is an obstruction for that ordering and seed class, conditional on the two crossings. A single-crossing or unused-band seed, a different ordering, or windings that grow with t are still possible. No lighting counterexample follows.

**Named open selection test: the offset four-tier staircase.** From bottom to top take the horizontal intervals [0,3], [1,4], [3,6], [4,7] of heights 2, 1+t, 1+⌊√2 t⌋, 2. Put S=(2,1) and T=(5,one unit below the roof). The room has six reflex corners, and the marked x-levels are exactly 0 through 7. The marks split both end heights into unit gaps. Thus the two middle heights are the **only** eligible bands. Compressing both gives area 18. Every path crosses both bands and has transverse travel at least three.

In fact bounded first winding cannot start the ordered construction from **any fixed template seed** here. If the lower band is lifted first, the exit of its last traversal has x≤4 and T has x=5. The suffix has at most D axial travel, unchanged by this lift, so its slope must satisfy s′≥1/D. If the upper band is lifted first, the prefix from S at x=2 to its first entry at x≥3 gives the same bound. For fixed seed and bounded winding the first updated slope tends to zero in either order, a contradiction. A finite menu of template seeds with bounded winding fails for the same reason. A winding growing with the first gap, or a seed selected in the one-band parent without this fixed-template restriction, is still available in principle.

The named question concerns **selection**, not the existence of a chord in the final room. Indeed the direct chord at the three successive interfaces tends in abscissa to 2, 2+3/(1+√2), and 5, strictly inside the respective overlaps (1,3), (3,4), and (4,6). So it is legal for all sufficiently large t by convexity within each tier. This isolates exactly what the passing-parent proof must still supply. For rational ratios the determinant test covers the synchronized ratios and offsets satisfying (2); outside that test a different seed or winding may pass. Perturbation likewise proves lighting inside certified neighborhoods of smaller lit templates, possibly at irrational ratios, without necessarily producing a passing single-band parent. The general marked selection theorem above area 121 remains conditional.
