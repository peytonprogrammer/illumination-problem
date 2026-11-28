# D240 review: cert-a (A′, FP implies dark and W ≥ 22)

Referee: independent. Date: 2026-11-28. Scope: [cert-a.snapshot.md](cert-a.snapshot.md) only. Checks: [checks_a.py](checks_a.py), output in [checks_a.log](checks_a.log), plus a rerun of `d239-lattice-lines/astra_fp_controls.py`. Three named rooms (the d237 dark row and folds-d237.tsv lines 1 and 2), under 1 CPU-second in total. No search, enumeration or census was run.

**Overall.** I found no wrong step. The refinement argument (claim 2), the alternation argument (claim 3) and the count (claim 4) are correct as written. The A′ theorem holds for **interior** same-class marks, conditional on the d9 census through area 16. The gaps are about scope and provenance, not logic. First, the theorem never says "interior", but FP, fp.py and the census are all interior-only. Second, the note calls the census "reviewed". d9's README says no human reviewed it, and d206 says it didn't re-examine d9's same-parity results. I found no referee review of d9 in the files I read. The base the theorem needs is d9 alone. d205 and d206 cover area 21 and aren't needed.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | Normalization on the coarsest axis-aligned rectangular grid; grid well defined | CORRECT (one scope remark) |
| 2 | Unequal block sets on any FP partition imply disjoint block sets on Π | CORRECT |
| 3 | FP implies dark, by primitive-step alternation | CORRECT (one wording gap) |
| 4 | A′ count: k = 1 gives r ≥ 9; k, m ≥ 2 and r ≤ 8 give km ≤ 16 | CORRECT |
| 5 | Finite base: the cited censuses cover area ≤ 16, W ≤ 20 | CORRECT WITH GAPS |

## 1. Normalization

The definition is well defined. On each axis, the vertex and mark coordinates span at least two values, so the gcd g of their differences is positive. The coset (offset + gZ) on that axis is the unique coarsest 1-D lattice containing them, so the product grid is the unique coarsest rectangular grid. A different offset choice changes the parity labels only by a translation, which permutes the classes, and FP is symmetric in the classes. Axial scaling maps axis-parallel walls to axis-parallel walls and maps the reflection (p, q) → (−p, q) to the reflection of the scaled direction, so lit and dark pairs, W and strict simplicity are preserved. The note is right that an oblique "coarsest lattice" would not give rectangular cells.

Scope remark: the brief's "must be stated on the coarsest grid" applies to Conjecture C (the converse), not to A′. The README's scaled-copy test shows that FP can fail on a finer grid for a dark pair. That is a completeness failure. For A′, claims 3 and 4 never use coarseness, and the d9 census lists every polyomino and every interior lattice point, normalized or not. So the note's statement that A′ holds on any adapted grid is correct.

## 2. Canonical partition Π

Line by line:

- **Coarsening.** Let P be G-invariant with no off-class quotient 2-cycles, and let (u v) be a 2-cycle of g_x upstairs. Then g_x maps block P(u) to P(v), and g_x² fixes P(u). The quotient cycle of P(u) has length 1 or 2. Length 2 is excluded, so P(u) = P(v). P contains every generating pair and is G-invariant, so it coarsens Π. Correct.
- **Π kills off-class 2-cycles.** A quotient cycle length divides the length of each upstairs element of the block. Upstairs lengths are 1, 2, 3, so a quotient 2-cycle needs a block containing a 2-cycle point u. In Π, u ~ g_x u, so that block is fixed. Correct.
- **Edge invariance.** G is the even-word subgroup of the edge group: A_iB_j and B_jA_i are generators or inverses, and A_0A_1 = (A_0B_j)(B_jA_1). Any edge involution E normalizes the even subgroup, and E and G generate the edge group. For an edge factor E of g_x, E g_x E = g_x⁻¹, so E preserves the set of 2-cycle pairs of g_x. E therefore maps the G-closure Π_x of those pairs to itself. Π_x is then invariant under the whole edge group, and so is the join Π. Correct. The order of factors in g_x (A then B or the reverse) changes g_x only up to inverse, which doesn't affect invariant partitions.
- **Orbit argument.** The vertical edge involution A at the mark's x-parity maps NE ↔ NW and SW ↔ SE at the mark, so it maps the cycle (NE SW) to (NW SE). The two upstairs cycles are the front and back lifts. A conjugates g_a to its inverse and preserves Π, so it permutes the quotient points over a. Each mark's quotient points form one A-orbit of size 1 or 2. Orbits of an involution are equal or disjoint. Quotient points over a partition the blocks, so equal block sets ⇔ equal point sets. Correct.
- **Refinement.** If Π gave equal block sets, their images under the coarsening Π → P would be equal. So inequality on P forces inequality on Π, hence disjointness. Correct.
- **Singleton case.** A unit cell has exactly one corner of each class, so distinct same-class interior points share no cell. Correct.

Machine check on the three rooms: monodromy from `foldtest.perms` equals the edge products, Π is invariant under all four edge involutions, and A maps each mark's quotient points to themselves. On the dark row each mark has one quotient point and they are disjoint. On both fold rows each mark has two quotient points and the sets coincide. This matches astra_fp_controls.py, which I reran: blocks {3,4} and {0,2} on the dark row, and four equal blocks at both marks on each fold row.

## 3. FP implies dark

- **Displacement.** Walls lie on integer lines, and reflection x → 2c − x keeps parity, so a developed image of T is in class a. The displacement D ≠ 0 is even-even, so D = g·v with v primitive and g even.
- **Alternation.** The pillowcase group contains the point reflection about every integer point, since 2p ∈ 2Z². So [a+v, a+2v] maps onto [a, a+v] reversed. Every step traverses one arc γ between a and x = a + v mod 2, alternately in the two directions. This uses nothing about the slope, so axis directions are included. An axial path can't graze a wall without first meeting the vertex where that wall starts, so grazing needs no separate case.
- **Intermediate hits.** A legal hit is an interior or smooth wall lattice point, with local degree 2 over B. Its image in N has degree dividing 2. FP excludes degree 2 over x, so the image is unramified. N → B is a local homeomorphism there, so the image path retraces γ to the same point over a. A degree-3 quotient point lifts only to degree-3 points, which are reflex corners, so a legal path can't reach one. Convex and reflex corners end the path, so they're illegal hits.
- **Induction.** At each a-point the outgoing lift in N may change. The next x-hit still returns the path to the same quotient point. Every a-point the path reaches, including an early pass through T, maps to the starting quotient point.
- **Either lift.** The start is one of S's quotient points, and T's arrival lift is one of T's. Disjointness of the full point sets handles all four combinations.

Wording gap: "legal" isn't defined in the note. The argument needs the census convention, which d206 check 1 confirms for `verify_plane.c`: pass through interior lattice points, reflect at smooth wall lattice points, stop at every corner. With that convention, the claim is correct.

## 4. A′ count

- **Case split.** km = n, so the cases m = 1, k = 1 and k, m ≥ 2 are exhaustive. For m = 1 there is one point over a, so there's no separation. Under fp.py's criterion there is one block, so there's no inequality.
- **k = 1.** A singleton FP partition means no off-class 2-cycle upstairs, which means no regular off-class lattice point. That is exactly d217 claim 4's hypothesis, which gives r ≥ 9 for interior marks. Not re-reviewed.
- **Genus zero.** A strictly simple room is a disc, so Q is a sphere. Riemann–Hurwitz for Q → N gives −2 ≥ k(2g_N − 2), so g_N = 0.
- **Local degrees and q.** Quotient cycle lengths divide the upstairs lengths, so they're 1, 2 or 3. Riemann–Hurwitz for N → B gives −2 = −2m + q + 2z, so q = 2m − 2 − 2z.
- **2q ≤ m.** FP puts every degree-2 point over a, and each uses two of the m sheets there. Then 3m ≤ 4z + 4. With m ≥ 2, z ≥ 1.
- **kz ≤ 8.** A degree-3 quotient point has k preimages of local degree 1, each a reflex corner. Corners lie on the boundary and appear once in Q. Distinct quotient points have disjoint fibers, so kz ≤ r ≤ 8 and z ≤ 4.
- **Bounds.** k ≤ ⌊8/z⌋ and m ≤ ⌊4(z+1)/3⌋ give (8,2), (4,4), (2,5) and (2,6). The largest products are 16, 16, 10 and 12. I verified this by hand.
- **What goes beyond d217.** Dropping q ≥ 2 only lowers the minimum m from z+2 to z+1. The upper bounds don't use q ≥ 2. Marked images may be unramified points (degree 1, "endpoints at poles" in the note's sense). Claim 3 and the count never need them to be regular. On the dark row, q = 2, z = 3, k = 3, m = 5 and kz = 9 = r. On both fold rows, q = 2, z = 5, k = 2, m = 7 and kz = 10 = r. Riemann–Hurwitz holds on all three.

W = 2r + 4, so r ≤ 8 ⇔ W ≤ 20. R22 (the d237 dark row, area 15, W = 22) carries FP, so 22 is attained.

## 5. Finite base

What the theorem needs: every strictly simple polyomino room with area ≤ 16 and W ≤ 20, and every unordered pair of distinct same-class interior lattice points in it, shown lit by a legal path.

What the censuses cover:
- **d9** covers every strictly simple polyomino with area ≤ 20 and W ≤ 22, up to the 8 symmetries. It covers every same-class pair of interior lattice points, with all four classes. It found one dark pair, R22's. For area ≤ 16 (721,884 rooms, 792,133 pairs), `crosscheck_full.log` replays every lit certificate with a second tracer. This strictly contains what claim 4 needs.
- **d205/d206** cover exact area 21 and different-parity pairs at areas 17–21. Neither is needed. d206 states that it didn't re-examine d9's same-parity results.

Mismatches and gaps:
1. **Interior marks only.** d9, fp.py's `marks_of` and the note's lift argument all use interior marks. No census covers smooth-wall marks, and FP isn't defined for them. A′ should say "interior same-class pair". The note says so only inside the refinement paragraph.
2. **Provenance.** The note says "reviewed census". d9's README says no human reviewed it. Room-count completeness is independently checked only through area 12 (d9 `check_enum_small`) and area 11 (d206). Areas 13–16 rest on d9's Redelmeier enumerator. d205's copy reproduces d9's area-20 counts, but it's the same code lineage. I found no referee review of d9 in d2, d38, d43, d121 or d206. This search was limited, so the absence of a review is unchecked.
3. **Citation.** The note cites "D9/d205/d206". Only d9 is load-bearing. Citing area 21 suggests a dependency that doesn't exist.
4. **No mismatch on normalization.** The census lists all polyominoes and all interior lattice points, so it covers the normalized grid and any finer adapted grid. Symmetric rooms counted once cause no gap, because illumination is symmetry-invariant.

## Unchecked

- Completeness of d9's room list for areas 13–16. No census was run.
- Whether a referee review of d9 exists outside the directories I read.
- The B′ paragraph and the comparison with the 45° guide. They make no claim that A′ uses.
