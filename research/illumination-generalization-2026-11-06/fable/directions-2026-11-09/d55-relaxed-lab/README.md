# d55: relaxed orthogonal rooms as a laboratory for "dark implies fold"

Opus 5.5 subagent, 2026-11-15. Capped experiment. No human or second agent has
reviewed it. Tags: **PROVED** (argument written here, unreviewed),
**CITED**, **COMPUTED**, **GUESSED**.

## Verdict

- Every dark pair found is certified by Theorem U. No new darkness mechanism
  appears. (COMPUTED)
- The corpus is small. In 8,303,245 relaxed rooms with 12,694,162 interior
  pairs, only 5 pairs are dark: the known 22-wall room's pair and 4 slit-room
  pairs. (COMPUTED)
- All 4 slit-room dark pairs are Tokarsky-type. Par holds with `N = DP` at
  b, c and d, because the room has no regular lattice point outside the
  marks' class. No pair needs Cut, Rig or a relative base. (COMPUTED;
  darkness PROVED by hand, section 5)
- No pinched room in range has a dark pair. No different-class pair is dark.
  (COMPUTED)
- The relaxed lab isn't a large corpus. In this range it adds one new
  mechanism instance: the orthogonal analogue of Monteil's slit room.

## 1. Room class (task 1)

### 1.1 Definition

A relaxed orthogonal room is a pair `(C, S)`.

- `C` is a finite set of closed unit lattice cells. Cells are edge-connected,
  and pinch points are allowed.
- `S` is a set of interior unit edges, meaning both side cells are in `C`.
  These edges are walls (slits).
- The room's interior is connected and simply connected. The interior is
  the open cells, the open non-wall edges between two cells, and the lattice
  points whose 4 cells are present with no wall at the point. For this open
  surface, `chi = F - E + V`. So the test is: connected and `F - E + V = 1`
  (`lab.is_valid`).

A **pinch** is a lattice point with exactly two diagonally opposite cells. A
slit's **foot** is its end on the boundary; its **tip** is the end inside the
room.

### 1.2 Sectors and cone points

At each lattice point, the present cells split into sectors. Two cells around
the point are joined when they share an edge that isn't a wall. Each sector is
one point of the room's abstract closure (`lab.sectors`).

| Sector | Angle in room | Point of `DP` | `g`-cycle | Paths |
| --- | --- | --- | --- | --- |
| interior (4 cells, cyclic) | 2 pi | two regular points | `[2, 2]` | pass |
| 1 cell | pi/2 | pole | `[1]` | stop |
| 2 cells in a row | pi | regular point | `[2]` | reflect |
| 3 cells | 3 pi/2 | zero | `[3]` | stop |
| 4 cells in a path (slit tip) | 2 pi | one point, cone angle 4 pi | `[4]` | stop |

So these cases follow:

- A **pinch** gives two separate poles of `DP`, and paths stop there.
- A **slit tip** gives one 4-cycle, and paths stop there.
- A **slit foot on a flat wall** (T-junction) gives two poles.
- A **slit foot at a reflex corner** continues one wall straight into the
  room. It gives one pole and one regular point. On the flat side, the
  boundary walk doesn't turn, so a path reflects there.
- An inner point of a slit gives two regular points, one on each face.

The double `DP` is the double of the room's abstract closure, which is a
disc. So `DP` is still a sphere and a cover of the unit pillowcase `B`
branched only over the four corners. Its sheets are cells, and slit edges
are fixed points of the edge-crossing involutions. `d4_monodromy.Room` builds
it with the `slits=` argument (PROVED).

### 1.3 Wall-count conventions (`lab.wall_counts`)

- `W_walk`: sides of the boundary walk. That is the number of sectors of
  types 1, 3 and 4. A slit counts as 2 sides plus its foot turns, and a pinch
  counts 2 corners. This is Monteil's convention: 20 for his slit room and 22
  for his pinched room.
- `W_slit1 = W_walk - #slits`: a slit counts as 1 side.
- `W_seg`: maximal straight runs of wall edges as point sets. A slit merges
  with collinear walls, and walls through a pinch or a T-foot aren't split.

For strictly simple rooms, all three equal `W = 2r + 4`. Hand check: a 4 x 3
box with a unit slit from the bottom wall gives `(7, 6, 5)` (`validate.py`).

### 1.4 What survives of the theory (PROVED here, unreviewed)

The changes come only from slit tips. A pinch adds no new cycle type, so
everything in d10 holds for pinched rooms verbatim. That excludes
propositions that use embeddedness (R4, R5, Lemma F); this lab doesn't use
them.

- **Fact L** still holds: `len(q) = e * len(phi(q))`. Its corollary
  "`phi` is branched only over poles of `N`" fails. A tip (`len 4`) can lie
  with `e = 2` over a regular point of `N`.
- **Par, Rig** (Theorem U over `B`): the soundness proofs in d10 section 2.2
  never use that corollary. A live vertex over `x` in a Par factor is still a
  pole, because `2 = e * len` forces `len` in {1, 2}. Rig needs only the
  isotopy in the base. **Both stay sound unchanged.**
- **Cut** uses the corollary in the cycle case: "the disc bounded by `C`
  contains no pole, so `phi` is unbranched over it". **Adapted rule Cut+**:
  d10 Cut plus "every point of `Q` over a non-pole of `N` has `e = 1`". With
  that hypothesis, the d10 proof goes through word for word. The unadapted
  rule is computed separately and never counted (`certs.cut_d10`).
- **Relative bases `P'`** (d10 ParRel and RigRel, Lemma 0): Lemma 0 uses the
  corollary. A tip over a non-corner of `P'` would stop paths that the `P'`
  rule ignores. **Adapted:** a relative base is used only when H0 holds,
  meaning every `Q`-point over a regular point of `P'` is regular
  (`certs.h0`).
- **R3(1) fails as stated** when class `x` contains a tip. Take a 4-cycle
  `(c, gc, g^2 c, g^3 c)` of `g_x`. Its image cycle has length 1, 2 or 4, and
  length 2 is a regular point. **Corrected:** "no regular point over `x`"
  means each 2-cycle is merged, and each 4-cycle is either fully merged or
  has 4 distinct blocks. The finest such systems are among the `C_M`. `C_M`
  is the closure of the 2-cycles plus the full 4-cycles in `M`, for each
  subset `M` of tips of class `x`. Par(x) holds for some factor iff a valid
  `C_M` separates. R3(2) (`R_y`) and R3(3) (iota-invariance) hold unchanged.
- **R1** (normalized rooms have no proper pillowcase factor) may fail: a tip
  need not map to a pole of `P'`. This lab doesn't test R1. It needs no R1
  because it searches all block systems.

## 2. Tools (task 2)

| File | Role |
| --- | --- |
| `lab.py` | Room model, sectors, validity, wall counts, canonical form under 8 symmetries, slit enumeration, 4-fold unfolding for `orbitr` |
| `orbitr.c` | d9 `orbitc.c` with the unfolding built by the caller. Slit edges are walls, and decoration is per sector (tip, pinch and convex foot are -1). A cap reports `CAP` instead of exiting. |
| `enum_relaxed.c` | d9 `enum_rooms.c` with pinches allowed and counted. The hole test is on the interior Euler characteristic. Writes polyominoes with at least 2 interior points. |
| `certs.py` | Theorem U over every block system of the monodromy group: Par, Rig, Cut+, d10 Cut, ParRel and RigRel under H0, canonical `C_M`/`R_y` cross-check, and `hurwitz_dark` (independent decider) |
| `run.py`, `cert_run.py` | Drivers |
| `validate.py`, `check45.py` | Validation and the 45-degree examples |
| `lib/` | Unchanged copies of d6 `hurwitz.py` and `d4_monodromy.py`, d11 `rooms45.py` (path constants patched only), d51 `check51.py`, d10 `unified_test.py`, d9 `orbitc.c` |

Validation (`python3 -B validate.py 60`, all passed):

- **22-wall room.** `orbitr` and the untouched `orbitc` agree. Both reach
  2,592 states with one DARK pair. Certificate class: full (Par at b, c, d).
  d6 `marked_orbit` says DARK (3,456 states).
- **Hand cases:**
  - sector types at a tip (`[4]`), T-foot (`[1, 1]`), reflex foot
    (`[1, 2]`) and pinch (`[1, 1]`);
  - a floating slit and a cutting slit rejected, a hole rejected, the pinched
    ring accepted;
  - **tip blocks:** in the 5 x 2 box with a slit, the horizontal-only scan
    (cap 1) leaves `(1,1)-(3,1)` and `(1,1)-(4,1)` unjoined and joins
    `(3,1)-(4,1)`. Without the slit, it joins all three.
- **Random rooms.** On 60 random relaxed rooms (area 6 to 9, up to 2 slits),
  `orbitr` agrees with d6 `marked_orbit` on every same-class pair and on a
  30% sample of different-class pairs. Different-class pairs are checked in
  the room scaled by 2. There were 0 mismatches, but no dark pair was among
  them.
- **Enumerator.** `enum_relaxed` and an independent Python generator
  (`lab.free_polyominoes` with `lab.is_valid`) give the same 2,662
  polyominoes at area 11 or less.

## 3. Pilot and bounds (task 3)

The pilot used about 2 CPU minutes. Areas 10 to 13 showed that Python slit
enumeration dominates, and `orbitr` costs about 0.1 ms per room. The area 15
slice (1/40 of area 15) took 50 s. That gave the bound below.

**Bounds:**

- area at most 15 cells;
- at least 2 interior lattice points;
- 0 to 3 straight slits, any length;
- any number of pinches;
- symmetry classes under the 8 lattice symmetries.

Slits are pairwise disjoint closed segments. A foot is a non-interior
lattice point of the slit-free room. Every other slit point is interior to
the slit-free room.

**Excluded:**

- area 16 or more;
- 4 or more slits;
- bent, branched or touching slits, and slits sharing a foot;
- slits whose inner points touch the boundary (these disconnect the room);
- holes;
- all 45-degree rooms.

## 4. Full run (task 4)

All counts are COMPUTED. Each room is decided exactly by `orbitr` with a cap
of 1,000,000 states.

| Class | Rooms | Pairs | Dark pairs (exact) | Undecided at cap |
| --- | ---: | ---: | ---: | ---: |
| strict (no slit, no pinch) | 908,220 | 1,634,938 | 1 | 0 |
| slit only | 7,136,786 | 10,736,911 | 1 | 3 |
| pinch only | 70,312 | 99,534 | 0 | 0 |
| slit and pinch | 187,927 | 222,779 | 0 | 0 |
| **Total** | **8,303,245** | **12,694,162** | **2** | **3** |

- Pairs are all unordered pairs of interior lattice points, same-class and
  different-class.
- `orbitr` visited 306.8 million states in total.
- The 3 undecided pairs also exhausted d6 `marked_orbit` at 2,000,000 states.
  They're dark by proof (section 5).

**Certificates, all 5 dark pairs** (`dark_pairs.tsv`, one row per pair):

| Pair | Class | Certificate | Kinds needed | `N` degrees | R3 canonical agrees | Recheck |
| --- | --- | --- | --- | --- | --- | --- |
| 22-wall room, area 15, `(1,3)-(3,5)` | full | Par at b, c, d, all 4 lift pairs | Par | 5 (parity factor), also 15 | yes | `marked_orbit` DARK, 3,456 states |
| slit room A14, `(2,2)-(2,4)` | full | Par at b, c, d | Par | 14 (`N = DP`), one target also 7 | yes | `marked_orbit` DARK, 1,128 states |
| 3 slit rooms, area 15, `(2,2)-(2,4)` | full | Par at b, c, d | Par | 15 (`N = DP`) | yes | both deciders hit their caps |

- Uncertified: 0. Partly certified: 0. Fully certified: 5, all by Par over
  `B`.
- No pair needs Cut, Rig or a relative base.
- In no case does the unadapted d10 Cut hold where Cut+ fails.

**Minimum wall counts of a dark room:**

| Class | Smallest dark room | W_walk | W_slit1 | W_seg |
| --- | --- | ---: | ---: | ---: |
| slit only | A14 (exact decider) | 26 | 24 | 22 |
| slit only | area-15 variants (dark by proof) | 27 | 24 | 21 |
| pinch only | none in range | - | - | - |
| slit and pinch | none in range | - | - | - |
| strict | 22-wall room | 22 | 22 | 22 |

## 5. The slit rooms

Room A14: `C=0,1;0,4;1,0;1,1;1,2;1,3;1,4;1,5;2,1;2,2;2,3;2,4;3,2;3,3`, slits
`(1,3)-(2,3)` and `(3,3)-(4,3)`, marks `*` = `(2,2)`, `(2,4)`. `=` is a slit.

```
  +-+
  |#|
+-+ +-+
|# # #|
+-+ * +-+
  |# # #|
  +=+ +=+
  |# # #|
+-+ * +-+
|# # #|
+-+ +-+
  |#|
  +-+
```

The line `y = 3` is a wall with a one-unit doorway between the two tips
`(2,3)` and `(3,3)`.

The three area-15 rooms add one cell and one more slit to the same core, so
again no flat point occurs (`logs/tokarsky_check.log`):

- `S=1,3-2,3;2,5-2,6`
- `S=1,3-2,3;2,5-3,5;3,3-4,3`
- `S=1,3-2,3;3,3-4,3;3,4-3,5`

**Darkness, PROVED by hand (Tokarsky's argument).** In all four rooms, the
only regular lattice points are the two marks. `logs/tokarsky_check.log`
lists no flat or interior point outside class a. A billiard path from `S` in
a primitive direction `(p, q)` first meets a lattice point of class
`(p, q) mod 2`, which isn't a. Reflections in lattice lines keep the class.
That point is a corner, tip or foot, so the path stops. This argument uses
no software beyond the sector list. It settles the 3 cap-undecided pairs.

**Pattern (GUESSED, from 4 rooms).** These are the orthogonal analogue of
Monteil's slit room. They aren't degenerations of the 22-wall room, whose
certificate is a degree-5 parity factor, not `N = DP`. Every relaxed dark
pair in range has `k = 0` transparent points. Pinches produced nothing up to
area 15.

## 6. Controls (task 5)

- **(a) Strict rooms.** 908,220 strict rooms at area 15 or less. The only
  dark pair is the 22-wall room's pair (the area-15 room above,
  `W = 22`), certified by Par at b, c, d. No dark pair at `W <= 21`. This
  agrees with d9 (CITED).
- **(b) Soundness on lit pairs** (`lit_control.tsv`). The sample is 1,000
  random pairs that `orbitr` calls LIT:
  - areas 10 to 14, pinched polyominoes oversampled, 75% bias toward rooms
    with slits;
  - by class: 617 strict, 243 slit, 124 pinch, 16 both;
  - 109 same-class and 891 different-class pairs.

  Results:
  - full certificates: 0;
  - partial (some target certified): 14;
  - lift pairs a certificate would complete if the unadapted d10 Cut were
    allowed: 0.

  An earlier 400-pair sample with fewer slit rooms also gave 0 full and 2
  partial (overwritten; `logs/cert_lit.log` keeps the 1,000-pair result).

## 7. 45-degree rooms (task 6, minimum only)

There was no compute left for an enumeration. `check45.py` runs d51's
`analyse()` on the two known examples. **Every verdict below rests on the
unreviewed d51 definitions (Theorem U45).**

| Room | Tiles | Canonical factors | Verdict |
| --- | ---: | --- | --- |
| Monteil slit room (d42 coordinates) | 22 | `B_B = B_C = Q` (`d = 22`) | Par(B) and Par(C), all 4 lift pairs separated: certified, Tokarsky-type |
| Monteil pinched 22-gon (d53 coordinates) | 24 | `B_B = B_C = Q` (`d = 24`) | Par(B) and Par(C), all 4 lift pairs separated: certified, Tokarsky-type |

These match d51's own log for the slit room and for `WOLECKI22`.

## 8. What is verified and what isn't

- **Independent of `orbitr`:**
  - the 2 decided dark pairs: d6 `marked_orbit` on `d4.Room`, different
    code;
  - the 4 slit-room pairs: the hand argument in section 5.
- **Single tool:**
  - every LIT verdict in the full run rests on `orbitr` alone, plus the 60-room
    agreement test;
  - certificates rest on `certs.py`, which ports d10 code. The R3 canonical
    path agrees on all 5 pairs, but it's the same author.
- **Not verified:**
  - the adapted Cut+ and H0 proofs (section 1.4) have no referee;
  - R1 for slit rooms is untested;
  - rooms beyond the bounds;
  - the 45-degree enumeration.
- **Convention dependence:** paths reflect at the flat sector of a
  reflex-corner slit foot. If that foot were a stopping vertex instead, some
  verdicts could change. No dark pair here has such a foot.

## 9. Caps and deviations

- **CPU.** About 2,810 s (46.8 min) in total:
  - pilot and validation: about 126 s;
  - areas 1 to 14: 435 s;
  - area 15: 50 s + 2,133 s, plus about 7 s of enumeration;
  - an accidental duplicate area-14 job: at most about 20 s, then killed;
  - certificates and the `marked_orbit` rechecks: 90 s;
  - lit control and 45-degree checks: about 2 s.
- **Processes.** At most 3 at once: `enum_relaxed | run.py | orbitr` during
  the area-15 run.
- **RAM.** Under 50 MB resident per process.
- **Disk.** The directory is 540 KB.
- **Deviations:**
  1. A missing upper-area check made the first job cover areas 1 to 14,
     although its arguments and output name said 1 to 13. The files are
     renamed to `a01-14`; the summary's `args` field still shows `1 13`.
     The duplicate area-14 job was killed and its output discarded.
  2. Temporary polyomino lists of 14 MB and 65 MB existed for about 15
     minutes, above the 5 MB output cap. They were deleted, and area 15 then
     streamed through a pipe.
  3. The 400-pair lit sample was replaced by the 1,000-pair sample.
