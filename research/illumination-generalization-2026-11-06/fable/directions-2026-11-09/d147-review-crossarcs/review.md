# d147: referee report on cross-factor-arcs (snapshot 2026-11-22 00:30)

Reviewed file: `../d95-review-queue/snapshots/cross-factor-arcs.2026-11-22-0030.md` and its checker. Context read: `qclass-closure/bbbb/five-sheet-arcs.md` (twist dictionary), `qclass-closure/README.md`, the bbbb README, and the d146 review.

Code: [checks.py](checks.py), log [checks.log](checks.log), 3.3 CPU-seconds. The script uses only the named b = 7 cross, with no room search and no network. It shares no code with `roomtools`, `d4_monodromy` or `hurwitz`. It has two independent models:

- **Monodromy.** Sheets are the 96 cells. Four edge-crossing involutions on (cell, side) pieces give the site permutations. The script finds its own block systems and conjugates D by h^j explicitly for each slice.
- **Physics.** An exact integer billiard tracer runs in the room itself. It reflects at walls, passes interior and smooth points, and stops at reflex and convex corners.

## Verdict

**Sound with gaps.** Every number in the note reproduces exactly. The twist dictionary and the label closure are exact. The identity-cover physical claim is correct: every restricted slice equals straight-line reachability for an explicit slope. The gaps are about reach, not errors. The question the note leaves open is settled by a few lines of computation. The note also understates what the cross computation proves.

## Check 1: the table

The snapshot `.py` and `.md` are byte-identical to the live `qclass-closure/bbbb/` copies. The snapshot can't run in place, because its `parents[2]` import path resolves only from `qclass-closure/bbbb/`. I ran the live copy, which took 0.3 s. It prints the note's table, the 4 + 4 factor residuals and the 16 identity residuals.

My own code finds the same block systems: exactly 24, 48, 48 and 48 blocks, plus the trivial one. It finds 69 interior points and 574 same-parity pairs, so 1,722 rows. Every count matches:

| Factor | Reference | One contact | Closure | Remaining |
|---|---:|---:|---:|---:|
| 24 | 1,014 | 416 | 292 | 0 |
| 48, (6,1) | 998 | 432 | 292 | 0 |
| 48, (−7,1) | 876 | 411 | 431 | 4 |
| 48, (6,−2) | 876 | 411 | 431 | 4 |
| 96 | 722 | 370 | 614 | 16 |

The residual lists match pair for pair. On the (−7,1) factor they're (x,0) in class d. On the (6,−2) factor they're the transposes, (0,y) in class b.

## Check 2: twist dictionary and label closure

- **Dictionary.** My slice uses D_j = h^j D h^−j. The D_j-cycles meeting U are exactly h^j C for the D-cycles C meeting h^−j U. This is the note's statement with j replaced by −j, which is the sign freedom it allows. It held in all 1,440 tests over every factor, origin and pencil.
- **Closure.** I reimplemented the note's residue labels with Python sets. The label is pos(y) − pos(x) mod l, lifted to Z/ord(h). The script runs a Floyd–Warshall closure with union and intersection. For every pair of A-vertices, the result equals the set of powers at which the explicitly conjugated slice graph connects them. All 131,520 comparisons agree, so the claim is exact. Because bitwise AND and OR act on each residue separately, this is a proof, not only a test.
- **Zero slice.** In all 80 cases, the zero slice equals the ordinary ⟨A, D⟩ components.
- **Boundary loops.** Here h is the vertical or horizontal pillowcase loop, which is the boundary of the disk around D and E. On the identity cover ord(h) = 28 for both loops.

## Check 3: the identity-cover physical claim

The argument is correct. A vertex of a 2-cycle is a point of cone angle 2π. Its two arc lifts leave in opposite directions, so passing through it is straight continuation. Removing every edge at a non-2-cycle vertex removes exactly the stops. Either lift of T is the physical point T, so "the right lift" is automatic for marks. Restricted rows are a subset of unrestricted rows, row by row (asserted), so equal counts of 1,706 do mean equal sets.

**Direct test.** For each of the 4 × 574 pencil rows and each of the 28 powers, I compared the restricted slice with physical reachability. The physical side uses an explicit straight slope:

| Class | Pencil | Slope at power j | Result |
|---|---|---|---|
| b | c | (1, 2j) | 574/574 rows match at every j. Each lift matches one sign, and the other lift matches the mirror (1, −2j). |
| d | c | (2j, 1) | 574/574, same pattern |
| c | b, d | (1, 1 + 2(εj + c₀)) and its transpose | Exact for every origin. The fitted offset c₀ is 0 or −1, depending on whether the reference diagonal is (1,1) or (1,−1) at that origin. |

Physical reachability is also periodic in j with period ord(h) = 28: all 72 sampled cases agree. So the twisted arcs are the straight slopes, and the restricted closure is exact billiard illumination within the pencils. These are two independent models agreeing at the level of single slices.

**Witnesses, unfolded in the room, with no forbidden corner on any path:**

- (−6,0) → (0,−6), class b, j = 2, direction (−1,−4), 8 arcs. Lattice points: (−6,0), (−7,0), (−6,0), …, (−2,0), (−1,−4), (0,−6). The path passes back through the source, which is legal.
- (−6,0) → (0,0), class c, direction (1,7), 6 arcs.
- (−6,0) → (−4,0), class d, j = 3, direction (6,1), 4 arcs.

## Check 4: the Riemann–Hurwitz component bound

The bound is correct. Site i has (m + f_i − z_i)/2 cycles, so V − E = (f_i + f_j − z_i − z_j)/2. The counts don't depend on the arc. Quotient cycle lengths divide upstairs lengths, so they're at most 3. Strictly, this is Euler's inequality for the preimage graph and uses no Riemann–Hurwitz.

On the degree-24 factor, sites (0,1) and (1,0) each have type 1² 2¹¹, so the bound is 2. The reference arc attains it with 2 components. All four factors are spheres: total ramification is 46 = 2·24 − 2 and 94 = 2·48 − 2. In every pencil slice the component count respects the bound. The note's reading is accurate: the bound forces a split but not a separation of the marks. Origin (0,1), class c, uses exactly this split, and all its rows reconnect.

## Check 5: the residuals

Each of the 8 factor residuals, and each of the 16 identity residuals, is joined by a straight interior lattice chord in the other axial class. The (x,0) pairs use direction (1,0), class b. The (0,y) pairs use (0,1), class d. The 8 extra identity residuals, (±x,±1) and (±1,±y) at origin (1,1), use the same chords.

**Stronger:** every residual is physically lit *in its specified class* by a slope outside the pencils:

- (−5,0) → (1,0), class d, direction (−2,5). Lattice points: (−5,0), (−7,−1), (−5,2), (−3,−1), (−1,4), (1,5), (1,0). Only smooth and interior points occur.
- The other residuals use directions (−5,−2), (−3,4), (−4,−3), (−3,−2) and (−2,3), all in the specified class.

## Check 6: scope

- **Link 1** matches `qclass-closure/README.md`, which cites the corner-only all-area proof and the D64/D67 covering-room replay.
- **Link 2** matches d146's corrected statement.
- **Links 3 and 4** are correctly marked open. The 668 identity rows where the unrestricted power set is strictly larger than the restricted one show corner blocking inside single slices. That is a concrete instance of link 4's worry, and the note could cite it.
- **What the note proves.** "Every pair covered in some class" proves illumination for this one 12-wall room. It proves nothing about other BBBB rooms and gives no degree bound. The note says this.
- **What the cross gets.** The cross is fully lit at interior lattice pairs. With slopes |p|, |q| ≤ 12, all 574 same-parity pairs are lit physically in **each** of the three classes, for 1,722/1,722 rows. All 1,772 mixed-parity pairs are lit as well, so all 2,346 = C(69,2) interior pairs are lit. The note doesn't test the mixed-parity pairs. Reachability is symmetric with 0 violations, as reversibility requires.

## Gaps

1. **Medium: the "open" question is closed for this room, and the factor table follows from it.** Every one of the 16 identity residuals has a legal straight witness in its specified class. A legal path on the identity cover projects to a connected walk in any quotient's arc graph. So all four factors connect 1,722/1,722 rows, and the 0/0/4/4 split is an artifact of the pencils. The sentence "whether some other arc reconnects each in the specified class remains open" should be replaced. On this room, the projected factor table adds nothing beyond the identity computation.
2. **Medium: the note doesn't state the slope at each twist power.** "A simple path develops to a legal straight segment" relies on each twisted arc being a straight saddle connection of a known slope. The map is b: (1, 2j), d: (2j, 1), and c: (1, 2j ± 1) or (2j ± 1, 1). For class c the reference diagonal depends on the origin. I verified this numerically on the identity cover at every slice, but the note should state it and cite it.
3. **Low: scope of "physical illumination" is understated.** The cross is lit for all 2,346 interior lattice pairs, including the mixed-parity pairs, and in every class for the same-parity pairs. Nonlattice and boundary endpoints are untested.
4. **Low: slice-level corner blocking deserves a line.** The 1,706 = 1,706 equality holds at row level only. Within slices, 668 rows lose powers when the stops are removed. This is the concrete identity-cover form of link 4.
5. **Low: "Riemann–Hurwitz" is a misnomer.** The bound is Euler's V − E for the preimage graph. Riemann–Hurwitz enters only through the sphere remark.
6. **Low: reproducibility.** The snapshot checker can't run from `snapshots/`, because its relative import resolves only from `qclass-closure/bbbb/`. The live copy is identical and runs in 0.3 s.
