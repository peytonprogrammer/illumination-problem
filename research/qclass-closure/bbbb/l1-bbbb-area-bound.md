Advances: L1 — area reduction for a hypothetical dark lattice pair in a BBBB room with at most eight reflex corners.

**Result.** I get no unconditional finite area bound for either parity type. For a normalized same-parity dark pair, a uniform bound of 25 on the number of unrealized off-class coincidence branches would give **area at most 48**. That hypothesis is open. Below is a separate, directly checkable condition giving **area at most 25 for either parity type**, together with its three control tests. No census or illumination search was run.

### The term lost in passing from Q to B

For physical parity y write vᵧ,sᵧ,rᵧ,iᵧ for the numbers of convex, smooth-wall, reflex and interior lattice points. Put mᵧ=sᵧ+2iᵧ and cᵧ=vᵧ+3rᵧ. Counting the unique class-y corner of each unit cell gives

    n = cᵧ + 2mᵧ,      Σ cᵧ = 4r+4,      Σ mᵧ = 2(n−r−1).

On the doubled room mᵧ counts regular degree-two points over y, since an interior point has two lifts and a smooth wall point one. A Q class kills the entire mᵧ term and gives n≤4r+4. BBBB says mᵧ≥1 in every class. Even the *minimum* of the four regular counts can grow without changing r. The exact identities hold for any marks; putting two marks in the same class or in different classes supplies lower bounds on interior counts.

### What the marked-pair budget controls

For a same-class pair of class a let d be the projection degree of its marked union of off-diagonal pair components. The reviewed count is 2d=Rₐ+R_other+J, where Rₐ≤mₐ=(n−cₐ)/2 and J≤2r. For a dark pair every off-class coincidence in that union is unrealized. Write H for their number. Then

    H ≥ 2d−2r−(n−cₐ)/2.

This is a **lower** bound on hidden branches. For normalized rooms at n≥49, d81/d82 supplies d≥⌈2n/3⌉ for a nondirect same-class pair. Hence H≥2⌈2n/3⌉−16−⌊n/2⌋≥26. This proves the conditional bound 48 stated above; it gives no upper bound on H or on mᵧ. Even knowing that some algebraic coincidences are inaccessible in every example would not estimate how many are inaccessible in one dark pair. For different-class marks the unfolded endpoint images retain different parities, so their midpoint has at least one half-integral coordinate. The same-source-fiber midpoint argument and its d81 threshold do not apply.

For the midpoint route alone there is a numerical target at 25: extend condition (i) down to n=26 and prove H≤6 for a dark same-class pair at n≥26. The lower bound is 7 at both 26 and 27 and at least 7 thereafter (six residue classes, increment five every six areas). Six is the largest constant this coarse estimate can use at 26. An estimate that reaches just one candidate wherever the lower bound is positive would also suffice. No reviewed result supplies either extension. [Counting lemma](midpoint-necessity.md) · [d68, d81/d82 and open core](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d70-writeup/RESULTS.md)

### An area-25 condition that also works for different-parity marks

There is no unique weakest extra hypothesis without fixing what data it may use. Here is the least restrictive numerical threshold in a two-class version of d68 that retains the reflex counts outside the two classes but discards their convex counts. Choose two distinct classes I. Let M be their combined mᵧ and t the number of reflex vertices in the complementary classes. Adding the two identities gives

    n = 2r+2+M−(3t+v_out)/2 ≤ 2r+2+M−⌈3t/2⌉.

Indeed 3t+v_out is even. Thus it suffices that **some I satisfies M−⌈3t/2⌉ ≤ 23−2r** (threshold 7 at r=8). This is a condition on regular points and the locations of reflexes, measurable without knowing whether marks connect. The threshold is exact for this upper estimate: raising it by one allows the estimate to return 26. This does not establish geometric sharpness or that darkness implies the condition.

The following is direct cell-incidence arithmetic on the three requested controls only. The m values are in physical 00,01,10,11 order; for R22 the coordinates are those of the archived census control. Each listed I minimizes the displayed upper bound (ties allowed).

| Room | n, r | m values | I | M, t | Area upper estimate | Passes 25? |
|---|---|---|---|---|---:|---|
| R22 | 15, 9 | 0, 2, 2, 6 | 00,01 | 2, 3 | 17 | yes, as a control outside r≤8 |
| cov4181 | 28, 8 | 12, 12, 0, 14 | 00,10 | 12, 1 | 28 | no |
| cov2929 | 22, 8 | 0, 8, 10, 8 | 00,10 | 10, 4 | 22 | yes |

Each cell contributes to four vertex masks. Masks with two adjacent cells add one to m, full masks add two, and three-cell masks count reflexes. **All three controls have a Q class.** R22 is dark; the named cov4181 and cov2929 pairs are lit. In cov4181 seven regular branches over one off-class are inaccessible even though a different class lights the pair. Cov2929's failed path families likewise do not imply darkness. Thus none of the three tests establishes the missing implication inside BBBB. [R22 cells](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d29-rigidity-test/control22.sv) · [cov4181 cells, §7](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md) · [cov2929 cells, §3](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md)

### First shape where the argument loses the bound

Already take two rectangular chambers of widths 5 and 10 with common floor −h and roof h+1, joined by a length-three neck at heights (0,1). The four reflex shoulders are fixed, and the wall-line gaps have gcd one on each axis. As h grows, even the first chamber contains an unbounded number of interior points of *each* parity. Thus every choice of M grows, while t≤4. To use darkness one would need to turn this growth into access for the prescribed pair. The d201 pocket progression requires regular entry and exit, a clear approach and departure, and the correct phase for the *same* slope. The neck map transports the incoming phase. D203 tests whether a specified strip sequence matches both marks. None proves that a growing mᵧ forces one of those tests to succeed, or that it supplies a reachable member of the marked coincidence union. This family witnesses failure of the area estimate from shape alone; no dark pair is asserted.

**First open L1 case.** At exact area 22, a hypothetical BBBB dark pair with r≤8 is outside the completed L2 census. For same-class marks both the degree threshold in the intermediate range and geometric reachability remain open. Above 48 the latter obstruction remains even with the degree threshold. Different-class marks need a separate geometric argument. The one-neck family identifies an obstruction to this counting proof, not a least dark instance. [L2 scope and review record](census-a21-status.md)
