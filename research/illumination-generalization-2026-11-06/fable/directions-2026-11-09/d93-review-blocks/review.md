# D93: review of small-orbit-blocks.md (snapshot)

Date: 2026-11-20. Reviewer: independent referee. Reviewed file: `small-orbit-blocks.snapshot.md`, SHA-256 prefix `4357f45a` (checked before and after review).

## Verdicts

| Claim | Verdict | Reason |
| --- | --- | --- |
| 1. Darkness bounds mirror suborbits at both endpoints | Sound, weak | Darkness is symmetric, so T has the dark partner S and d92's bound 2e ≤ B(B−1) applies at both ends. B(r) is non-effective (d86), so "bounded" only means bounded along fixed-r families. |
| 2. Iff test for an intermediate cover from two point blocks; R22 gives 15, 3, 15, 15 | Sound; R22 numbers reproduced exactly | Both directions check. The "A joins one pair" check is automatic once the part size is k; only the B check carries content. |
| 3. Cubic graph lemma: K₃,₃ or cube, hence blocks of size 3 or 4 | Sound | Every step checks (details below). Its hypothesis is a case assumption, not a consequence of darkness. The lemma never uses darkness. |
| Recovered system = staircase fold fibres | Confirmed | G has exactly one nontrivial block system. It is W-invariant and develops onto a 5-cell staircase. |

## Claim 2: the test

Necessity: if A is the full unramified fibre over a regular point y of N = Q/Σ, then g_a swaps two Σ-blocks β₁, β₂, and each A-cycle has one sheet in each. Choosing the β₁ sheets gives a closure finer than Σ whose part containing β₁ has size ≥ k, so it equals Σ. Sufficiency: parts of size k form a G-block system. g_a maps the chosen block to the block of the other ends, which is different because it holds k other sheets. So y is a 2-cycle on blocks, and its fibre has exactly k 2-cycles of g_a, all from A. Fixing the first choice is justified because g_a ∈ G maps one choice to its complement. The test is a check on given point sets. It does not turn affine point blocks into sheet blocks, as the note says.

## Claim 3: the graph lemma

- An edge orbit is edge-transitive, so each stabilizer is transitive on 3 neighbours and so contains a 3-cycle, which is transitive on pairs.
- Each 4-cycle count per edge is 2c_L = 2c_R. The seed square gives c ≥ 1.
- c = 2 saturates to K₃,₃.
- c = 1: twin classes divide 3. A class of size 3 forces K₃,₃, a contradiction. So the u's are distinct. The common neighbour of u_ab, u_ac′ besides a can't be b or c′, because either would make u_ac′ = u_bc′ or u_ab = u_bc′. The same argument at b closes the cube.

The lemma holds for any edge-transitive orbital, lit or dark. "Physical darkness forces blocks" in the Decision overstates this. Darkness enters only through the cubic, single-orbital hypothesis, which is verified for R22 and nowhere else.

## R22 recomputation ([blocks.py](blocks.py), [blocks.log](blocks.log), [systems.py](systems.py), [systems.log](systems.log))

My own code builds the corner monodromies g_(p,q) = σ_x,p σ_y,q on the 15 cells (rooms.json order), with 13 poles, 9 zeros, and 22 walls.

- A-cycles: (0,4), (1,3), (12,14). B-cycles: (8,11), (9,10), (6,7). These match the note.
- Choices (0,1,12), (0,1,14), (0,3,12), (0,3,14) give sizes 15, 3, 15, 15. Only (0,1,14) is accepted. It has 5 blocks, A joins {0,2}, and B joins {3,4}. This matches the note.
- |G| = 233,280 and |W| = 466,560. G's only block systems are trivial and Σ = {0,1,14}, {2,5,13}, {3,4,12}, {6,9,11}, {7,8,10}. So any degree-3 factor is Σ.
- Σ is W-invariant. Developing it gives a fold onto the 5-cell staircase (−1,0), (0,0), (0,1), (1,1), (1,2), with 3 cells per fibre. These are the staircase fold's fibres.
- B_x on R22: class (0,0) = a is one block, (0,1) and (1,0) equal Σ, and (1,1) is discrete. So Q/Σ = N_b = N_c, but it is not N_a, since it has regular points over a by construction.
- R34-base: G is primitive and has no proper factor.

The affine group action itself was not recomputed; the triples come from d92's archived orbit data.

## The d64 bridge question

The two notions are the same kind of object, but they are selected differently. Both are G-block systems on sheets, that is, intermediate pillowcase covers. Two differences matter:

- N_x = Q/B_x is the *finest* system merging all 2-cycles of g_x. It is W-invariant (a fold), and it has no regular point over x.
- The note's factor is any system for which the A and B triples are regular fibres. It need only be G-invariant (a translation cover, not necessarily a fold), and over a it has regular points by design.

d64 covers only rooms where some class has 1 < deg N_x < n. A room whose proper factors all have regular points over every pole (for example, quotients shaped like the 1×3 tromino, where every class has type (1,2)) is outside d64's scope. So "darkness ⇒ fold" plus d64 does **not** close W ≤ 20.

**Bridge lemma needed (BL).** For a strictly simple orthogonal lattice room with r ≤ 8 and a dark same-class interior pair, some corner class x has B_x neither discrete nor one block. A sufficient form: the forced proper system Σ merges every 2-cycle of g_x for some x where g_x has a 2-cycle, so that B_x ≤ Σ and deg N_x ≥ deg N > 1.

R22 satisfies BL at x = b, c, and it is excluded from d64 only by r = 9. BL also needs:

- the note's open step, which promotes affine point blocks to sheet blocks;
- a proof that darkness yields the cubic or otherwise imprimitive case at all.

Even with BL, d64 covers only same-class interior lattice pairs. Different-class pairs (G1) and non-lattice marks (G2, via d16) stay open.

Re-run: `python3 -B blocks.py; python3 -B systems.py R22-base; python3 -B systems.py R34-base`. Each takes under 5 CPU-seconds, uses exact permutations, and covers named rooms only.
