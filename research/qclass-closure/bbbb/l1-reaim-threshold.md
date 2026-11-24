Advances: L1 — every sufficiently long insertion preserves illumination of retained lattice pairs with known seeds. For the rank-11 and rank-18 terminal caps the resulting **all-pair** thresholds are respectively **E ≥ 7** and **E ≥ 151** added rows. These are sufficient thresholds.

## Keeping the target and all intermediate entrances

This is a one-row specialization of the reviewed d182/d184 re-aiming argument. The useful refinement here is to measure clearance only at integer row interfaces and keep the signed error at each visit. A separate slope window for each of two end legs would overlook paths with intermediate visits. [d184 review, Claim 1](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d184-review-gaphyper/review.md)

Replace one entire unit row whose section is a single interval of width w by an identical row of height 1+E. This gives the same room as inserting at its half-integral cut. Retain old marks in their respective end pieces, including marks on the original row interfaces. A horizontal seed carries over on its side. A vertical seed already preserves its phase. For a remaining seed use transverse-to-axial slope magnitude s₀=u/v in lowest terms. Record axial travel in the development, so it increases even when physical motion is downward. Let D be its total vertical travel and k the number of full traversals of the selected row, including repeated traversals in opposite directions. Lattice endpoints and horizontal walls are at integral levels. Every vertical step from one integer level to the next therefore stays in one row component. If k=0 the seed carries over unchanged.

At integer time t in [0,D] let b(t) count the selected steps completed by t. Choose the **same integer N** on every traversal, and take

    s = (D s₀ + 2wkN)/(D+kE),       δ = s−s₀.
    E s − 2wN = −(D/k)δ.

In the developed transverse coordinate oriented along the base ray, subtract b(t) complete translations of 2wN. The error at the t-th old level is then

    e(t) = [t − D b(t)/k] δ.

In particular the target error vanishes. The signed state on a row interval lives on its doubled-width circle. Adding 2wN there changes neither position nor horizontal velocity sign. Axial travel is positive on downward as well as upward traversals, which is why the same correction works on every visit.

**Gate justification.** For an ordinary unit step the change in unfolded transverse increment is δ. For a selected step, after subtracting whole periods, it is (1−D/k)δ. Interpolate these increments from their base values to the proposed values. Within each row component the transfer is a translation on its doubled interval; a physical ray can bounce only on its straight vertical sides before the next level. A switch at an integer level requires meeting an endpoint of an opening or a corner. In the unfolding these have integer transverse coordinate. At a base level with nonintegral coordinate the distance to the nearest integer is at least 1/v. At an integral base coordinate the seed is regular: an interior neighborhood continues across the interface, or a single straight wall continues in its reflected chart. Perturbing to either side there is legal up to the next distinct integer. In particular a vertical-side bounce may move from one row to the next without losing the branch. This gives continuation through all levels if |e(t)| < 1/v throughout; more sharply the perturbed coordinate may stay anywhere between the nearest *strictly* lower and higher integers around its base value. This argument tracks circle states, so interpolated increments may be signed. At the chosen s the true elongated row has exactly the prescribed circle transfer. The last level reaches the original marked lift in its end chart, on a regular approach.

Put M=max |t−Db(t)/k|. Rounding Es₀/(2w) to the nearest integer makes s positive and gives |δ| ≤ w/(E+D/k). Thus every integer

    E > wvM − D/k

works, including all residues. This uses controlled changes of the intermediate phases. D197's divisibility obstruction concerns exact replay at a fixed slope. D198 permits arbitrarily many visits at one slope; here the entire finite seed supplies b(t), without a cutoff on other paths. [d197 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d197-review-shrinkprimitive/review.md) · [d198 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d198-review-exterior/review.md)

## All-pair thresholds for the two terminal caps

Use the same cut y=3/2 and width w=2 as in the wide-insertion note. The cap height becomes H=2+E. Its center column contains every cap mark, old and new. There are no interior lattice marks on its unit-width entrance. Cap-to-cap pairs have a straight segment. For cap-to-upper pairs one can sharpen the collar estimate by allowing either the direct cap leg or one floor reflection. [Base geometry, seed records and floor-corner proof](l1-wide-insertion.md)

Both rooms have a lower cap mark and every upper mark has the regular nonvertical entrance required by the collar lemma, as the six positive ratios below document. For each upper mark reverse its archived seed from the lower mark and stop at its first downward cap entry, y=2 in base coordinates. Write D₁ for vertical travel to this entry. The same entrance itinerary persists between the nearest distinct ratios i/t on either side of u/v with 1 ≤ t ≤ D₁. This follows from the integral corner and endpoint argument; s₀ itself is a regular entry. Write Δ for this open interval's width. For a center target of height y above the floor, the direct image interval has length (D₁+H−y)Δ. Length greater than 2 includes a center image. The floor-return interval has length (D₁+H+y)Δ. Length greater than 4 includes two consecutive center images; their floor contacts differ by strictly between one and two units, so at least one misses the floor corners. If (D₁+H)Δ > 3, these two tests cannot both fail. This also covers the original lower mark.

| Rank | Upper mark | s₀ | D₁ | Persistent interval | Sufficient E for every cap target |
|---|---|---:|---:|---|---:|
| 11 | (4,3) | 7/4 | 3 | (5/3, 2) | 5 |
| 11 | (3,6) | 24/5 | 4 | (19/4, 5) | 7 |
| 18 | (3,3) | 1/2 | 1 | (0, 1) | 1 |
| 18 | (1,5) | 3/8 | 15 | (4/11, 5/13) | 127 |
| 18 | (4,6) | 14/9 | 8 | (3/2, 11/7) | 33 |
| 18 | (5,6) | 23/5 | 12 | (55/12, 37/8) | 59 |

The remaining pairs are upper-to-upper. Rank 11's only such seed avoids the cut. In rank 18 four of the six avoid it. For the two others the stored seed starts at (3,3), has s₀=3/5, and traverses the selected row on unit steps ending at t=10,13,14,17. Thus k=4 and b(t) is the count of those four numbers ≤t. These data and D₁ above come from the original paths; no extended rooms were run. [Archived pair records](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/records.md)

| Target | D | M | Sufficient signed interval for δ | Last E missed by this interval |
|---|---:|---:|---|---:|
| (1,5) | 20 | 9 | (−1/35, 1/40) | 57 |
| (4,6) | 35 | 18 | (−1/85, 1/90) | 150 |

To reproduce the last two columns, set z=3t/5, B=t−Db(t)/4. Intersect the inequalities ⌈z⌉−1 < z+Bδ < ⌊z⌋+1 for t=1,…,D−1, and require positive slope. If the resulting interval is (−1/A,1/C), let R=(3E/5 mod 4) in [0,4). The two nearest choices of 4N give a legal δ as soon as

    E+D/4 > min(A R, C(4−R)).

For residue e=0,…,19 put R=(3e/5 mod 4) and U=min(A R,C(4−R))−D/4. The last missed nonnegative E in that class is e+20⌊(U−e)/20⌋ if U≥e. Taking the maximum gives 57 (residue 17) and 150 (residue 10). This finite arithmetic evaluates a sufficient window; a missed window does not imply darkness.

## What remains below and beyond the thresholds

| Family | All-pair K, added rows | First area in the proven tail | Positive extensions below K outside the census | Largest such area |
|---|---:|---:|---|---:|
| Rank 11 | 7 | 35 | E=1,…,6 | 33 |
| Rank 18 | 151 | 323 | E=1,…,150 | 321 |

Area is 21+2E. Only E=0 is in the through-21 census. The first untested extension by that census has area 23 in both families. Some lengths below K satisfy the individual tests; the table gives the census gap, without asserting failure at every shorter length.

D110's reviewed sufficient lengths for its rectangular examples were 595,360 to 1,127,680; the later first-hit bound cited in the length note gives 21 for opposite-end pairs in those three examples. Here K counts added rows in different rooms and covers every lattice pair. The smaller numbers come from using known marked entrances and their actual clearance. [d110 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d110-review-length/review.md) · [Period-one tail and comparison](length-periodicity.md)

**First open general step.** The retained-pair bound is polynomial in the *seed data*, since M ≤ D. A first hit in a fixed primitive direction on the four-sheet unfolding has at most 4·area primitive steps before repeating its starting-square state or another state, so D ≤ 4·area·v. Consequently a polynomial bound on the axial denominator v of one selected seed per pair would give a polynomial box bound here. The empirical box conjecture would suffice, but has no proof. For new collar marks, one stepped or L-shaped terminal foot already leaves the regular-return step open, even with a known lit base and a regular first entry. The two-image proof uses a single flat floor across the cap. Neither the all-residue result for retained marks nor these two cap tails establishes a uniform L1 area bound.
