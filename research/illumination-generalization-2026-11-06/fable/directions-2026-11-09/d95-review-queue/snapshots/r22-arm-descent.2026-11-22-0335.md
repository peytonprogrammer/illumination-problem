# What changes at the old R22 cap

R22 gives an exact threshold for **loss of a hypothesis of its known certificate** on each of three arm slices. The first added layer destroys that hypothesis, and every further extension leaves it false. D152 proves actual lattice illumination at the first edit and all-real illumination sufficiently far out. These statements leave room for other obstructions at intermediate lengths.

## The local check

Keep the junction fixed and extend one rectangular end straight outward. In base R22 the odd–odd fiber consists entirely of corners, with degree count 15 = 6 + 3·3. The certificate uses this physical corner test for four lift/displacement cases. The staircase fold and its seam rule handle the remaining cases. An upper bound on physical support is the full 15-cell complex with its boundary, marked incidences and four seam endpoints. In particular its outside boundary is part of the input. [Fiber and case accounting](clean-site-cost.md)

| Slice, length 1 → 2 | Old odd–odd cap vertex | Its status afterward | D152 length-two result |
|---|---|---|---|
| Bottom, R22-L1-007 | (1,−3) | smooth side wall | All 10 regular lattice points pairwise lit |
| Right, R22-L1-025 | (5,1) | smooth side wall | All 10 pairwise lit |
| Top, R22-L1-012 | (1,3) | smooth side wall | All 11 pairwise lit |

I checked these three corner incidences against the saved d8 cell sets. At length one each selected vertex has one incident room square. The extension puts a second, edge-adjacent square there. Every further layer is farther along the arm and leaves those two squares in place. Thus the old fiber loses cleanliness at **every integral length ≥2**, even when the new cap returns to the old parity. This is a pointwise test requiring no trajectory enumeration. The original three-copy tiling by a five-cell staircase also has total area exactly 15, whereas the edited area is 15+w(L−1). A different fold would need a fresh proof. [D152 geometry and orbit evidence](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d152-review-uniformtail/review.md)

Both original marks remain interior. At length two the saved positive witnesses cover every distinct regular lattice pair. On the top-arm slice the reviewed all-real sufficient tail is L≥72(1+2F₁₅₆)² (w=2 and sealed area 13). The reflected junction copies in the proof are distinct abstract pieces even if their planar drawings overlap. Between 2 and the tail the cited evidence gives no all-length illumination result. Dilation therefore rules out a uniform real-mark equality tail already for arm-inclusive W=22 types; its two-genuine-chamber version and W≤20 version are separate questions. The direction of the observed change is dark **short** to lit **long**. [Capped-arm theorem](effective-chamber.md) · [Dilation argument](uniform-tail.md)

This is a positive control for **detecting dependence on a cap**. Even though all original closed cells are retained on lengthening, the boundary incidence at the old cap changes. A sound verifier cannot ignore that change and still certify this pair. Moving the cap also changes its round-trip signed phase by 2ΔL·s modulo 2w at transverse slope s. R22 supplies no positive example of transferring darkness along an uninspected arm. [Interface locality lemma](support-locality.md)

## A precise descent conjecture for the lattice core

Fix the orthogonal, strictly simple integral rooms with W≤20 and wall-length gcd one on each axis. Let D(P) mean there exist two distinct same-parity interior lattice points in P with no legal billiard path between them. All vertices stop a path. The marks are existential anew in each room. Restricting the starting room to BBBB is appropriate when using the separate closure results.

Here is one version with explicit coverage. Sort the distinct supporting-line coordinates in each axis. Let G be the largest consecutive gap over both axes. Conjecture that there is an integer C≥2, depending only on the wall cap, such that whenever G>C and D(P) holds, there is an admissible two-unit deletion with D(P′). Allow either of the following moves.

* Compress any consecutive supporting-line gap of length at least max(3, G/2) by two. Translate everything beyond it by two toward the near side and linearly compress the intervening slab. This includes gaps through a chamber, indentation, cap or several disjoint runs at once.
* Within one separating rectangular corridor or straight terminal arm of length at least max(3, G/2), remove two full transverse unit layers. Reattach the far subroom translated by two, or translate the cap inward for an arm. The side identifications must reproduce the same ordered wall directions and turns.

The one-half is a chosen comparability constant, not an estimate. There is no requirement that two eligible necks exist. For either move the output must remain integral, strictly simple, normalized per axis and of the same cyclic wall pattern. A gcd-changing move is ineligible; there is no implicit renormalization of the marks. A legal geometric move need not preserve the original pair. If there is no admissible move carrying any dark pair, the conjecture fails at that input. A room with no neck still has a largest coordinate gap; global gap compression is geometrically well-defined by a strictly increasing coordinate map when the gap exceeds two. Normalization and survival of darkness remain proof obligations.

Each admissible move lowers the integer area, so iteration terminates. A dark exit from BBBB at W≤20 would already contradict the corresponding reviewed lattice closure; alternatively state the same conjecture on the full normalized domain. At termination G≤C. For r≤8 each axis has at most r+2 wall lines, so the terminal box has sides at most 9C and area at most 81C². This is a conditional finite family up to lattice translation. There is no value of C from R22. This formulation makes no descent claim for mixed-wall rooms, arbitrary real marks or different-parity pairs. [Lattice closure scope](../README.md)

**Next proof obligation.** For a putative dark BBBB room with a large gap, exhibit one admissible deletion and an obstruction whose door or cap transition relation still certifies exclusion afterward. The R22 check gives a quick rejection criterion for proposed certificates which require a disappearing boundary incidence. It supplies neither existence of an alternative cut nor completeness of such certificates.

## A bound on a gap read by a clean-fiber certificate

Let G be any consecutive supporting-line gap of a connected orthogonal lattice room. Suppose the lines are vertical. Some horizontal row of unit cells runs across the entire gap. Indeed the interior meets the open slab, and the vertical cross-section is constant throughout that slab because there is no vertical wall in it. Choose one occupied row. At each of the G−1 intermediate integral abscissas, both ends of that row's vertical unit edge are regular physical points. Each has two adjacent squares on the row side and cannot be a corner, since there is no vertical wall at that abscissa. Their ordinates have opposite parity. The identical argument with the axes exchanged covers horizontal gaps.

Consequently **each of the four parity fibers has at least floor((G−1)/2) regular points on the double**. This estimate uses just one row. In particular a physical corner-only fiber forces G≤2 on both axes. In the normalized proper fold setting of the [ramification count](clean-site-cost.md), let k be the inner degree and J a nonempty set of distinct sites clean on the same sphere quotient. The degree-two points over downstairs poles each consume one ramification unit, giving

    |J| floor((G−1)/2) ≤ Σ_{x∈J} q_x ≤ 2k−2,
    G ≤ 2 floor((2k−2)/|J|) + 2.

For normalized proper clean factors with a downstairs zero, k≤r, hence G≤4r−2. This is a necessary bound for that certificate type. At R22 the physical odd–odd fiber already gives G≤2 and all actual coordinate gaps equal one. The cap-incidence test above detects its length-two edits more sharply. In BBBB a proper clean factor is already excluded. The bound identifies why this known type never needs a long-gap deletion and leaves other certificate types open.

## Route assessment after d153

* **First-shot existence** remains the direct route for primitive BBBB or a large imprimitive factor. D153 illustrates the freedom a proof needs: a length-dependent slope lights the pair even while the prescribed direction loses it. The open requirement is one legal shot, with no uniform direction-height bound available.
* **Uniform tails** settle fixed junctions and sufficiently long arms. R22 rules out a wall-count-only equality tail on the dilation-closed arm class at W=22; two comparable necks already defeat the available sufficient thresholds at W=20. Neither result proves the one-way existential descent conjecture.
* **Certificate descent** gives explicit bounds for known clean fibers. A proof for BBBB needs a certificate for a different mechanism, with verified behavior under an admissible deletion. Counting its cells alone supplies neither fact.

**Decisive lemma for the support route.** Total darkness forces a clean physical fiber or a proper clean quotient for some parity site in a normalized W≤20 orthogonal room with same-parity interior lattice marks. If true, the existing closures finish this branch directly. If false, there is a dark BBBB pair and any complete certificate theory must handle it. This is the core expressed as a structural implication. Of the three routes I would pursue first-shot existence unless an independent reason for that implication emerges.
