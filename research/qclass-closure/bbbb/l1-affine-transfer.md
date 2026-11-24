Advances: L1 — affine transport of a legal chord is valid, but an integral band twist fixing its source cannot turn a unit lattice chord into a chord to a same-parity target. The obstruction holds on the primitive area-22 branch as well. Even with a longer seed of the right parity, a pinned target is a singleton orbit for these two band twists.

### Transfer and its invariant

Work on Q, the two-copy room double. Keep every convex and reflex lift forbidden. If an affine automorphism F fixes these corners, it maps a straight segment with regular interior to another such segment. Thus a legal chord s→u gives a legal chord s→F(u) whenever F fixes s. Fixing both physical source lifts suffices, though fixing the chosen lift alone is enough. To light the physical target, F(u) must be one of its compatible lifts. This proves the proposed transfer implication for seeds of any length. [Band construction](l1-seam-parity.md)

Take the integral horizontal and vertical multi-twists from that construction and let A be the group they generate. In a horizontal band of height h and physical width W the least positive integral shear parameter, common to the room, is Lₕ=lcm(2W/gcd(2W,h)), taken over all bands and intervals. On lattice level d above its floor the generator rotates the 2W unit positions by Lₕd modulo 2W; band boundary levels are fixed pointwise. Exchange the axes for Lᵥ. These two permutations, with the actual wall identifications, generate the exact image on regular lattice sites of Q. They are permutations of **points over the pillowcase poles**. The room monodromy G acts on a generic fiber of 22 sheets instead. Computing G=A₂₂ or S₂₂ does not identify these two actions. [Primitive-branch theorem](l1-large-monodromy.md)

**Unit-seed obstruction.** Develop a seed in the integer grid and write its displacement as v. Its endpoint difference modulo two is the physical target parity minus the physical source parity: every reflection in an integral wall preserves coordinate parities. An affine word with derivative M sends its developed displacement to ±Mv. The overall sign disappears modulo two. Here M∈SL₂(ℤ), so Mv≡0 mod 2 iff v≡0 mod 2. Consequently a seed from S to another parity cannot enter the source parity under A_S. In particular *none* of the axial unit neighbors, or diagonal neighbors displaced by (±1,±1), can seed the requested orbit. A unit segment ending at a forbidden corner would also fail the legality premise. More generally gcd of the two components of the developed displacement is unchanged by any such word. The argument uses no monodromy hypothesis.

In a normalized room these particular twists give a stronger invariant. There is a horizontal band of odd height, since otherwise all vertical wall lengths would be even. The condition 2W | Lₕh on that band forces Lₕ even. Likewise Lᵥ is even. Every generator displaces integer positions in its cylinder by an even number of steps, and folding back preserves parity. Thus each of the four physical parity fibers is itself invariant, and the primitive direction class is also unchanged. Relative to any fixed S, membership in its own parity fiber already obstructs the unit-seed proposal without normalization.

### What a same-parity replacement seed would require

Start instead with the set of directly visible regular lifts u of the **same** parity as S. The repaired test is T-lifts intersecting the union of their A_S-orbits. This is sufficient for lighting and never changes the gcd of any chosen seed displacement. For the band subdivision in the proposal it has an additional obstruction independent of parity. Any interior mark at the intersection of a horizontal wall level and a vertical wall level is fixed on both copies by both generators: it is on a band boundary in each construction. If T is such a pinned target, only that very lift can be sent to it. Consequently these two band twists cannot turn any direct chord from S into a first witness for a nondirect pinned T. This last statement is conditional on such a target occurring; it does not assert a dark pair or classify all area-22 charts.

These partitions do not give a separating factor. A factor Q→N→B requires an equivalence relation on the *generic sheet fiber* invariant under continuation around all four poles. The parity partition above is the division into four different base fibers to start with. A singleton orbit on a band boundary is a statement about the affine generators fixing a particular regular point. Neither yields the required equivalence or separation of marked images. No lattice property of the derivative group would undo the integral displacement obstruction. [Factor hypotheses](l1-dark-implies-fold.md)

### Hand check on cov4181

Use the d66 cells, S=(2,3), T=(4,3). In the table a horizontal entry lists physical interval widths in a band; a vertical entry lists physical interval heights. Repetitions denote separate intervals. [Cell rows and class verdicts](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md)

| Horizontal range in y | Widths | Vertical range in x | Heights |
|---|---|---|---|
| (0,2) | 1,2,1 | (0,1) | 6 |
| (2,3) | 8 | (1,3) | 2 |
| (3,4) | 6 | (3,5) | 6 |
| (4,6) | 1,2 | (5,6) | 2 |
| | | (6,7) | 1 |
| | | (7,8) | 3 |

The horizontal lcm is 48: the unit-height bands require divisibility by 16 and 12, and the others require at most 2. The vertical lcm is 12: the first band alone requires 12, and the others require 2, 6, 4, 2 and 6 respectively. Every horizontal circumference (2,4,12,16) divides 48, and every vertical circumference (2,4,6,12) divides 12. On **every integer level** the corresponding rotation is therefore zero modulo the circumference. The image of A on all regular lattice sites of Q is trivial, so its orbit partition there is the singleton partition. This computation uses maximal constant-slice bands cut at the physical wall levels.

In particular the unit step from S through (3,3) cannot be transported to T. The direct *two*-step horizontal chord already reaches T in class b. Its primitive direction has parity (1,0), whereas class d requires (0,1). Every derivative in this group fixes directions modulo two, so no word changes that witness into a class-d witness. The singleton site orbits and direction invariant explain the transfer failure; d66's complete verdict separately rules out **all** class-d rays. cov4181 is physically lit, has area 28, and belongs to the imprimitive control rather than the primitive area-22 target. [Marked class-b witness](l1-cylinder-levels.md)

**First open case.** For a nondirect same-parity interior pair in a positive normalized eight-reflex BBBB chart of area 22 with primitive G, find one legal connection. The unit-seed orbit assertion fails at its starting parity. For a nondirect pinned target, even switching to a directly visible same-parity seed cannot repair it using these two band generators. Neither failure excludes a straight witness in a different geometric state.
