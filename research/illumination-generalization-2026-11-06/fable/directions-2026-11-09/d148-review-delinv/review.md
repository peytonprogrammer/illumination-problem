# d148: referee report on deletion-invariance (snapshot 2026-11-22 00:40)

Reviewed files: `../d95-review-queue/snapshots/deletion-invariance.2026-11-22-0040.md` and `deletion-check.2026-11-22-0040.py`. Both are byte-identical to the live `qclass-closure/bbbb/` copies. Context read: `cross-factor-arcs.py`, `roomtools.py`, `qclass-closure/README.md`, the d146 and d147 reviews, and `offgrid/cov4181.room`.

Code: [checks.py](checks.py), log [checks.log](checks.log), 4.2 CPU-seconds. The script uses 4 named rooms, with no room search and no network. It has two sides:

- **Physics.** A new exact lattice billiard tracer works on the cell set only. It reflects at walls, passes interior and smooth points, and stops at convex and reflex corners. It follows each line in both orientations until it stops or repeats a state, so there's no length cutoff.
- **Algebra.** The site permutations come from `roomtools.room_tuple`, which is shared infrastructure. Pencil connectivity is recomputed from scratch as orbits of ⟨U, V_j⟩ and ⟨A, D_j⟩, with V_j = h⁻ʲ D³ hʲ. It doesn't call the note's `pencil_components`.

## Verdict

**Sound with gaps.** Every number in the note reproduces. The DB55 pencil counterexample is correct, and the single-arc theorem is correct and matches physics exactly. The gaps concern interpretation. The counterexample only refutes the pencil as a witness family. The pair it uses is physically lit in the same horizontal class by direction (3,2). Across all 4 rooms, every lost or absent row is lit in its own class by some other arc. The note doesn't report this, and one sentence suggests the opposite.

## Check 1: the DB55 counterexample

**Room.** DB55 is strictly simple, with 53 cells, 12 walls and 4 reflexes. It has 32 interior lattice points and 112 same-parity pairs.

**Pencil table, reproduced.** At origin (0,0), h = g_b g_c has ten 5-cycles and three fixed letters, so its order is 5. For S = (2,2) and T = (10,2):

| Residue | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| Relaxed, ⟨A, D_j⟩ | 1 | 1 | 0 | 0 | 1 |
| Legal, ⟨U, V_j⟩ | 0 | 0 | 0 | 0 | 0 |

The legal row is 0 for each of the 4 lift pairs separately, at every residue.

**Residue 0, physically.** The ray in direction (1,0) from S hits (3,2) and (4,2), then stops at (5,2), a reflex. The point (8,2) is also a reflex. The note's description is correct.

**The whole pencil, physically.** The pencil arcs are the lines (±1, 2m). No such line through S reaches T for |m| ≤ 60, which covers 24 full periods.

**The whole horizontal class: not blocked.** Among primitive directions with |p|, |q| ≤ 25, 128 horizontal-class lines through S reach T. The shortest is (3,2). It reaches T after 16 lattice points: (5,4), (2,4), (1,2), (4,0), (3,2), (0,4), (3,4), (6,2), (9,2), (12,0), (11,2), (8,4), (11,4), (12,2), (9,0), (10,2). Each one is interior or smooth. The diagonal and vertical classes also succeed, with shortest witnesses (3,−1) and (4,1). Only the 3 reference arcs fail, which matches the note.

So only the pencil is blocked. Direction (3,2) isn't in the b-pencil (1, 2m). It lies in the orbit of (1,0) under both boundary twists, not just one.

## Check 2: the 272-pair claim

The 4 rooms have 112 + 81 + 27 + 52 = 272 same-parity interior pairs. Note that DB55 alone also has 272 legal *rows*; the two numbers are unrelated.

**Row table, own algebra.** My orbit computation reproduces the note's table exactly:

| Room | Legal | Lost | Absent | Pairs with ≥ 2 pencil-legal classes |
|---|---:|---:|---:|---:|
| DB55 | 272 | 64 | 0 | 112 / 112 |
| DBas | 196 | 38 | 9 | 81 / 81 |
| c4181s | 68 | 11 | 2 | 27 / 27 |
| U2 | 152 | 4 | 0 | 52 / 52 |

**Physical witnesses.** The tracer searched every primitive direction with |p|, |q| ≤ 15 from every source. It found a legal witness in **all three** classes for every one of the 272 pairs, so 816 of 816 rows are lit. The search didn't need the pencil slopes as a fallback. In particular:

- Every note-legal row is confirmed by a physical ray in its class.
- All 128 lost or absent rows (64 + 38 + 9 + 11 + 2 + 4) are lit in their own class by a non-pencil arc.

Check 3 below verifies the note's own pencil witnesses one by one, at every residue.

## Check 3: the single-arc test

**Derivation.** The argument is correct.

- At an orthogonal lattice site, cycles have length 1 (convex), 2 (interior or smooth) or 3 (reflex). All 4 rooms at all 4 origins show only these lengths.
- A sheet is one lift of the arc. A 2-cycle vertex is a point of cone angle 2π. Its two sheets leave in opposite directions, so U = A³ and V = D³ are exactly "continue straight".
- Fixing corner germs makes the orbit of a sheet equal to the set of arc lifts on one maximal corner-free geodesic. That geodesic is closed, or it runs from corner to corner. So orbit membership is equivalent to a legal straight connection.
- I is U-invariant. The group of two involutions is {(UV)ᵏ, (UV)ᵏU}, so the orbit of I is the union of (UV)ᵏ I.
- For a twisted arc, the D-endpoint of sheet i is hʲ i, which gives V_j = h⁻ʲ D³ hʲ.

**Direct test.** I compared ⟨U, V_j⟩ reachability with the physical ray for every pencil, every residue, every origin and every pair in all 4 rooms. That covers 4,496 residue slices and 79,724 row comparisons, with 0 mismatches. The slope dictionary is as follows. Each entry covers the line and its mirror, which are the 2 lifts.

| Class | Pencil h | Physical direction at power m |
|---|---|---|
| b | g_b g_c | (1, 2m) |
| c | g_b g_c | (1, 1 − 2m) |
| c | g_c g_d | (1 + 2m, 1) |
| d | g_c g_d | (2m, 1) |

The other candidates I tried, (1,4m), (4m,1), (1,1+2m) and (1−2m,1), each mismatch in at least one room and origin. The dictionary agrees with d147's.

**Component bound.** #⟨U,V_j⟩-orbits − #⟨A,D_j⟩-orbits ≤ 2(z_a + z_d) holds in all 4,496 slices. It's attained in 2,212 of them, so it's sharp on these rooms.

**Transitivity.** In DB55 at origin (0,0), BC, BD and CD generate a transitive group on all 53 sheets. That matches the note.

## Check 4: the conditional chain

1. **Accurate.** `qclass-closure/README.md` gives the corner-only 22-wall theorem and the D64/D67 covering-room branch. Its "remaining normalized lattice rooms … all four factors equal to the base" is the BBBB case. The README calls its verification internal, not external review.
2. **Accurate.** It matches d146's corrected statement: BBBB has no proper factor of outer degree 2–4. The endpoint-lifting caveat is correct.
3. **Accurate but stale and incomplete.** "False for the pencils, open across arbitrary arcs" is correct. Since this snapshot, d147's review has finished with *sound with gaps*. Like this review, it found every residual lit in its class by a non-pencil slope. The note should also say that no named row is a counterexample to the arbitrary-arc implication.
4. **Accurate.** The last-class claim is a restatement of same-parity illumination, not a reduction, and the note says so. Calling it "decisive" is fair. Both caveats are correct: transitivity gives no single dihedral orbit, and deletion still needs at least one relaxed connection.

**The precise open statement.** Let X be a normalized, strictly simple orthogonal lattice room below 22 walls in which all four canonical relations B_x are universal (BBBB). Let S ≠ T be interior lattice points of the same parity, with sheet sets I and J. Then some primitive direction (p,q) exists whose billiard ray from S reaches T without meeting a convex or reflex corner.

Equivalently, let α be a simple arc from a to the site of its class, with transport σ_α, a word in the two boundary products. Then J ∩ ⟨A³, σ_α⁻¹ D³ σ_α⟩ I ≠ ∅ for some α.

The deletion route needs two open statements:

- **(i) Existence.** Some class and some arc α give a relaxed connection, J ∩ ⟨A, σ_α⁻¹ D σ_α⟩ I ≠ ∅.
- **(ii) Arbitrary-arc deletion.** A relaxed connection in a class implies a legal connection on some, possibly different, arc in the same class.

DB55 refutes (ii) only for α restricted to one cyclic pencil. Different-parity pairs, nonlattice marks and mixed-wall rooms remain outside the chain.

## Gaps

1. **Medium: the counterexample's physical scope is understated, and one sentence misleads.** The note says S and T "fail … every power of the b-pencil. Other powers in the other classes succeed." In fact other arcs in the **same** class succeed. Direction (3,2) lights the pair in class b, and 128 horizontal lines with |p|, |q| ≤ 25 reach T. The note should say that DB55 refutes only the pencil-restricted implication and satisfies the arbitrary-arc implication.
2. **Medium: the named-room evidence for the open implication is missing.** All 128 lost or absent rows in the 4 rooms are physically lit in their own class. All 272 pairs are lit in all three classes (816/816 rows, |p|, |q| ≤ 15). The note's "≥ 2 classes" column understates this. No named room gives evidence against arbitrary-arc deletion.
3. **Medium: the refuted implication and its repair aren't stated formally.** The note never writes down the "residue-labelled deletion implication". It also gives no V formula for non-pencil arcs. Such arcs need σ_α as a word in both boundary twists; (3,2) is one example. The pencil slope dictionary in Check 3 should be stated, since it makes the physical reading of the table exact.
4. **Low: c4181s is undefined in the note.** It's cov4181 (`offgrid/cov4181.room`, 28 cells) stretched to 41 cells. Column x = 1 is widened by 2 and row y = 4 is raised by 3. The stretch matters, because d146 shows cov4181 itself has a corner-only site, so it isn't BBBB. The checker asserts that the stretched room is BBBB.
5. **Low: the algebra example is misworded.** (12), (23) and (34) aren't "transitive generators". Each one alone is intransitive; together they generate a transitive group. The intended point, that 1 and 4 share no single cyclic orbit, is correct.
6. **Low: the chain status is stale.** Item 3 says the cross equality is "under d147 review". That review is complete and reached the same in-class repair conclusion.
7. **Low: the component bound's sharpness isn't stated.** It's attained in 2,212 of 4,496 slices, so it can't be improved on these rooms without more structure.
8. **Low: reproducibility.** The snapshot checker fails when run from `snapshots/`. It loads `cross-factor-arcs.py` through `with_name`, and the snapshot copy has a dated name. The live copy is identical and runs in 0.4 s.
