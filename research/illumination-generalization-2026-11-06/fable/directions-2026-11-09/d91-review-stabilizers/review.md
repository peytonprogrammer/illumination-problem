# D91: review of stabilizer-orbits.md and axial-stabilizers.md

Date: 2026-11-20. Reviewer: independent referee. Both snapshots match their SHA-256 prefixes, and the live originals in `qclass-closure/bbbb/` have the same hashes:

- `stabilizer-orbits.snapshot.md`: `3a744bc6…`
- `axial-stabilizers.snapshot.md`: `cf878129…`

## Verdicts

| Note | Verdict | Reason |
| --- | --- | --- |
| stabilizer-orbits.md | Sound | The kernel description, the dark-to-dark transfer, the D69 staircase bounds, the two-way test and the kernel-escape lemma all check. The note explicitly disclaims a complete list of exceptions, and that disclaimer is needed. |
| axial-stabilizers.md | Sound | The cylinder data, the divisibility λ ∈ 4bZ and A·z = K·z all match an independent permutation computation at b = 7, 9, 11. The bound 4b is sharp. The scope paragraph is accurate. |

The main new finding concerns scope. The full affine group G does give growing orbits for the cross pair. At b = 7 and b = 9 the exact values are |G_s·t| = 36 and 52, which equals n/2 − 12. The negative result kills only the axial-cusp version of route B.

## Method

The scripts build the four-copy unfolding M of each named room as an origami (r, u) on unit squares. Convex-corner lifts are marked, and Q = M/σ, where σ is the deck involution. They track lower-left vertex labels through the elementary shears T and V. An affine map of Q is a square permutation φ intertwining the sheared and original origamis. Its vertex map must be well defined, preserve the marks and commute with σ. All arithmetic is on integers and permutations.

The scripts check their conventions in four ways:

- The vertex labels agree with the commutator cycles of (r, u) on every sheared origami. Reflex lifts have 3 squares and every other vertex has 1.
- Every recovered φ gives a well-defined vertex map. A convention error would break this.
- The horizontal parabolic of the staircase has least shear 6, as the note says.
- The staircase periods equal m/gcd(m,3).

Files:

- [origami.py](origami.py) holds the shared code.
- [check.py](check.py) and [check.log](check.log) cover task 2 and the staircase replay.
- [many.py](many.py) and [many.log](many.log) cover the 40 cusp directions with max(|p|,|q|) ≤ 5. [orbitmap_R5_b9.log](orbitmap_R5_b9.log) holds the matching orbit map at b = 9.
- [veech_index.py](veech_index.py) and its logs give the Veech-group index.
- [fullG.py](fullG.py), [fullG_b7.log](fullG_b7.log) and [fullG_b9.log](fullG_b9.log) cover the full group G.

## 1. stabilizer-orbits.md

**Dark to dark.** An orientation-preserving affine automorphism g of Q maps straight segments to straight segments. It permutes cone points by cone angle, so it preserves the convex corners (angle π) and the reflex corners (angle 3π). The note's "preserving the forbidden corners" condition is therefore automatic on Q. It's a real condition only on M, where convex lifts are regular. If g fixes the lift s, then t is hidden from s exactly when g·t is hidden from s. So G_s·t lies in the hidden set of s. Shadow-budget bounds that set by B(r) at lift level ("distinct regular targets hidden from a single source on Q"), and D86 reviewed the bound. The two-way version uses reversibility of the hidden relation. Both steps hold.

Two optional remarks:

- Orientation-reversing affine maps, such as ι, also preserve hiddenness. Including them would only enlarge the orbits.
- For a physically dark pair the stabilizer of the set {s, ιs} also works. It preserves the set of points hidden from both lifts.

**Kernel K.** Every step checks:

- An element with derivative ±I is holomorphic, so it's a Möbius map of the sphere Q.
- The fixed circle of ι contains every corner, and the Möbius map preserves that circle.
- Reflection in a circle is unique, so the map commutes with ι.
- Descending to the room gives a diagonal ±1 derivative. Copy-swapping elements are exactly the axis reflections.
- The centroid argument allows at most one map per sign choice.
- The descent is injective because ι is antiholomorphic.

So K embeds in (Z/2)². The computation finds |K| = 4 on the cross and |K| = 2 on the staircase at m = 4, 5, 8.

**Fixed-point exceptions.** If |K| = 2, then K is central, so Fix(δ̃) is G-invariant. The bound "at most 6" for a general K holds because K is normal and each involution has 2 fixed points. The identity G_s·(ks) ⊂ Ks also holds.

**D69 staircase.** By hand:

- The bands, the half-turn about (m+1, m+1) and the area 2m² + 6 all check.
- The overlaps are 1, 2 and 1. The right shifts are strict for m ≥ 2. The direct chord meets the reflex corner (m, m).

Computed at m = 4, 5 and 8:

- |K| = 2, and K fixes both lifts of T.
- The M horizontal cylinders are (6,1)×4 and (2m, m)×4, and the least shear in the stabilizer is 6.
- An element with derivative T^6 that fixes both lifts of T moves s with period 4, 5 and 8. These equal m/gcd(m,3).

The gcd step is gcd(2m, 6(m−1)) = 2·gcd(m, 3).

**Two-way test.** F^u ∈ G_s acts on t with period v/gcd(u,v), and the claim follows. The multitwist period formula is correct, and boundary circles are fixed pointwise.

**Kernel-escape lemma.** Suppose t = k₁s and ιt = k₂s. Then k₁⁻¹k₂ sends s to ιs, so it swaps the copies and acts physically as an axis reflection fixing S. The sign symmetries commute, so T lies on the same axis. That axis meets the interior of a simply connected symmetric domain in one interval, so the pair is direct. This argument holds. The statement that only the rotation center can be an interior fixed point also holds, because copy-swapping elements fix no interior lift.

**Are the exceptions complete?** No, and the note correctly doesn't claim they are. Three points:

- **A slightly more general exception.** If t ∈ N_G(G_s)·s, then G_s fixes t, because h⁻¹G_s h = G_s fixes s. The central-kernel case t = ks is the special case h = k. The normalizer is finite modulo G_s, but the note doesn't analyze it.
- **Lattice points.** On these square-tiled doubles, every lattice-point stabilizer G_s has finite index in G. So orbits are always finite and at most the number of lattice lifts. Bounded orbits are therefore a quantitative matter, not a structural one. A finite list of exceptions can't be complete in a meaningful sense without a lower-bound theorem.
- **A proper subgroup.** The axial computation below gives bounded orbits for the subgroup A outside every listed exception. The same happens for the subgroup H generated by 40 cusp stabilizers. Neither is a counterexample for the full G.

## 2. axial-stabilizers.md

**Cylinder data and stabilizers (check.log).** The table uses M units. Each Q cylinder lifts to the M cylinders listed with the same circumference and height.

| b | Horizontal M cylinders | Multitwist λ | Least λ in the full stabilizer | Maps at that λ |
| --- | --- | --- | --- | --- |
| 7 | (28,4)×2, (8,5)×4 | 56 | 28 = 4b | 4 |
| 9 | (36,4)×2, (8,7)×4 | 72 | 36 = 4b | 4 |
| 11 | (44,4)×2, (8,9)×4 | 88 | 44 = 4b | 4 |

The vertical data are identical. So the middle cylinder has circumference 4b and height 4, and the outer cylinders have circumference 8 and height b − 2, as the note states. The full horizontal stabilizer has least shear exactly 4b, half the multitwist 8b. That confirms the note's divisibility λ ∈ 4bZ and shows it is sharp. The 4 maps at λ = 4b are one element composed with K.

The scripts search every λ that divides the multitwist. Upper-triangular elements of the Veech group are ±T^λ, because the relative period lattice is Z². That lattice contains (4,0) and (b−2,0), and similarly on the vertical axis. So the search finds the whole direction stabilizer, not only the multitwist.

**A·z = K·z (check.log).** At b = 7, 9 and 11:

- The orbits of A = ⟨horizontal stabilizer, vertical stabilizer, K⟩ on all Q lattice lifts equal the K-orbits. There are 194, 258 and 322 lifts.
- The maximum orbit size is 4.
- For each lift s of (6,0), |A_s·t| = 1 for both lifts t of (0,6).
- K sends (6,0) to (±6,0) only.

**Hand check of the argument.** Each step holds:

- The circumference argument forces the horizontal scale to be 1.
- The attachment intervals force the rim rotations to be 0 or 2b.
- The vertical-axis kernel lift is the rim rotation by 2b, and on a width-4 doubled row it is the rotation by 4.
- The cap's fold θ ~ c − θ commutes with rotation by 4.
- The step λ = bj/2 to 8 | j uses the fact that b(b − 2) is odd.
- A pointwise kernel match on lattice lifts suffices, because K lies in both stabilizers.

No gap found.

## 3. Scope: what the full affine group does

The axial note's scope sentence is correct: elements outside A can matter. The computation confirms that they do.

**Cusp stabilizers alone stay small for this pair (many.log).** H is generated by the full stabilizers of all 40 primitive directions with max(|p|,|q|) ≤ 5, together with K. At b = 7, 9 and 11, |H·s| = 4 for both lifts of (6,0), and |H_s·t| ≤ 2. Lattice lifts in the odd parity classes already form one orbit of size 96 at b = 9 and 136 at b = 11. The even classes, including the reviewed pair's class (0,0), stay in orbits of size at most 16. In every one of these directions, every cylinder has gcd(C, H) ≤ 4. That bounds each single-cusp lattice orbit, and it is the arithmetic reason that each cusp separately is weak here.

**The full group G (fullG_b7.log, fullG_b9.log).** The script enumerates the SL(2,Z)-orbit of the marked, σ-equipped origami of Q. That gives the Veech-group index. It then lifts every Schreier generator to an affine map of Q; each lift passes the mark and σ checks. Adding K gives a generating set of G.

| b | Area n | Veech index | Lattice lifts | \|G·s\|, s over (6,0) | \|G_s·t\|, t over (0,6) | Max \|G_s·t\| over same-parity interior targets |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 96 | 12672 | 194 | 40 | 36, 36 (both s lifts) | 36 |
| 9 | 128 | 34560 | 258 | 56 | 52, 52 (both s lifts) | 52 |
| 11 | 160 | 65664 | 322 | not run | not run | not run |

At b = 7 the pairs (5,1)–(1,5) and (4,0)–(0,4) give 44 and 36. The two data points fit |G_s·t| = 8b − 20 = n/2 − 12. With two points this is a fit, not a theorem. For the reviewed pair, the full stabilizer of either source lift has an orbit on either target lift that grows with area. The orbit is about one fifth of all lattice lifts (36 of 194, 52 of 258). The growth comes from elements outside every cusp stabilizer with max(|p|,|q|) ≤ 5.

## 4. What survives of route B

The bookkeeping survives intact:

- G_s preserves hidden lifts.
- Both orbits of a dark lift pair are at most B(r).
- The kernel exceptions are exactly as stated.
- The two-way period test is valid for any certified parabolic.

Axial-axial words are dead for the cross. The low-height cusp stabilizers tested here are also too weak for this pair. The full source stabilizer is not dead: at b = 7 and 9 it gives orbits n/2 − 12 on the reviewed pair. So the cross is not a counterexample to route B. It shows that any orbit lower bound must use deep elements of the Veech group, whose index grows from 12672 to 65664 between b = 7 and b = 11. Cylinder bookkeeping in a few directions won't supply them. Three obstacles remain.

1. **A universal growth theorem.** Route B needs a theorem that every nondirect same-parity pair has a large orbit in one orientation and for one lift. Nothing proves it. The staircase shows the one-way version fails. The two-way version has the central-kernel blind spot the note names, and possibly normalizer cases.
2. **A non-effective constant.** B(r) is non-effective. Even linear growth would light every pair above an unknown area N(r). That gives no explicit census cutoff.
3. **The test case is already lit.** The cross pair is lit, so it can't test whether dark pairs evade growth.

## Limits and budget

- The Veech-group enumeration assumes that the Q-Veech group lies in SL(2,Z), which holds because the relative period lattice is Z². Even without that assumption, the computed orbits are lower bounds for G.
- Without a web connection, I relied on memory for the standard facts: Veech groups of square-tiled surfaces are finite-index subgroups of SL(2,Z), and every rational direction is parabolic.
- **The 10-CPU-minute budget was exceeded.** The total was about 15 CPU-minutes. A first stabilizer pass in fullG.py used a quadratic Schreier-generator loop and ran to a 500 s timeout without output. I replaced it with the pair-orbit union-find in the current script. I didn't run the full-G pass at b = 11 because of the budget.

## Re-run

```
cd d91-review-stabilizers
python3 -B check.py   > check.log          # ~2 s
python3 -B many.py 5  > many.log           # ~1 s
python3 -B orbitmap.py 5 9 > orbitmap_R5_b9.log
python3 -B veech_index.py 7 300000         # 13 s; b=9 47 s; b=11 111 s
python3 -B fullG.py 7                      # ~75 s, three pairs
python3 -B fullG.py 9 one                  # ~165 s, the reviewed pair
```
