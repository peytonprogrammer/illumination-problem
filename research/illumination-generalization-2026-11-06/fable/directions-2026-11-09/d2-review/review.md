# Review of the parity-factor audit (d2-factor-audit)

Adversarial second reader, 2026-11-09. Target: `../d2-factor-audit/audit.md`,
`enum_targets.py`, `room_model.py`, `run_room_model.log`.

You get four verdicts, then the evidence. I rederived claims 1 to 3 before
reading the audit's proofs. Nothing here is formally verified or refereed.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. `r = delta * z_N + t`, `s + 2t = 2 delta - 2`, `0 <= t <= delta - 1` | CONFIRMED |
| 2. `Z' = p_a + (3/2) R_a + 2 z_a - 1` under the parity property | CONFIRMED |
| 3. Case list `{(2,2),(2,3),(2,4),(3,2),(4,2)}` plus `delta = 1` for `r <= 8` | CONFIRMED, with a weaker hypothesis than the audit states |
| 4. `k <= 2 delta - 2 <= 6`, so the `k <= 6` theorem covers every case | CONFIRMED WITH CORRECTION, and it has a scope GAP |

I found no mathematical error in sections 1.1 to 1.8 of the audit.

### Corrected statement of claim 4

> Let `P` be a strictly simple orthogonal lattice room with `r <= 8`. Let `N`
> be a parity factor other than the unit pillowcase `PC`. Then
> `delta <= 4` and `k <= k_wall + 2 k_int <= s <= 2 delta - 2 <= 6`.
> If `N` also separates two distinct interior A points, section 1.3 makes the
> pair dark. Theorem 1.1 of `preprints/restricted-minimum-k6/manuscript.tex`
> makes it lit. So no single parity factor separates two interior A points
> when `r <= 8`.

Three corrections to the summary wording:

- "Any parity factor" is false. `PC` is a parity factor of every room, with
  `delta = n`. The bound needs `N != PC`.
- The theorem is not in `twenty-two-wall/manuscript.tex`. That manuscript
  proves existence only and says "We make no claim that 22 sides is minimal".
  The `W <= 21`, `k <= 6` theorem is Theorem 1.1 of
  `preprints/restricted-minimum-k6/manuscript.tex`.
- That theorem is computer-assisted. Its own text says it is not refereed and
  not formalized. `review/baseline-review.md` says the 8.75 GB of
  certificates were not replayed in that review.

## Most serious problem

Claim 4 excludes one darkness mechanism and nothing else. It is not a
statement about dark pairs.

- "Covers every case" means every `(delta, z_N)` case. It does not mean every
  room. A room with `k >= 7` is outside the theorem. Claim 4 shows only that
  such a room has `N_min = PC`.
- The d9 census reports 100,538,916 rooms with `W <= 20` that have a pair
  with `k >= 7`, and 20,332 rooms where every pair has `k <= 6`. So the
  theorem decides illumination for a small fraction of rooms.
- "Parity factor exists" is a sufficient condition for darkness. Nobody has
  proved that it is necessary. The audit says this in sections 3.2 and 3.3.
  The one-line summary of claim 4 drops it.
- Later work in this project lists two more sufficient mechanisms that claim
  4 does not exclude at `r <= 8`. `d10-mechanisms/theory.md`, section 3.8,
  marks both OPEN for rooms: "Par with different factors" and "Rig in
  general". The first one needs only `k >= 7` at `W <= 21`.
- For "Par with different factors", the audit's bookkeeping does not apply.
  The `Z'` formula needs all three non-A classes non-regular in one factor.
  Without it, nothing gives `z_N >= 2`, `delta <= 4`, or the area bound
  `n <= 16`. So "no finite check remains at `r <= 8`" holds for single
  parity factors only.

## What claim 4 implies about the universal target

The target is: no dark pair of interior points in any strictly simple polygon
with fewer than 22 walls.

Claim 4 implies:

- No single parity factor certifies a dark pair of interior lattice A points
  in an orthogonal lattice room with `W <= 20`. This holds in every lattice
  presentation of the room, because a rescaled room is still an orthogonal
  lattice room with the same `r`.

Claim 4 does not imply:

- That an orthogonal room with `W <= 21` has no dark pair. That needs "dark
  implies separating parity factor", which is open and is a lit-side
  statement.
- Anything about rooms with `k >= 7`, beyond `N_min = PC`.
- Anything about the per-class parity mechanism or the rigid-factor
  mechanism.
- Anything about pairs that include a non-lattice point.
- Anything about rooms with diagonal walls, other rational polygons, or
  irrational polygons.
- Anything about pairs that include a boundary point. For those the
  statement is false: see "Hidden assumptions".

## Independent derivation and comparison

I derived claims 1 to 3 from the definitions in `coordinator-log.md` and
`d4-monodromy-blocks/README.md`. My route and the audit's route agree in
every formula.

**Claim 1.** `angle(x) = e(x) * angle(phi(x))` with angles in
`{pi, 2 pi, 3 pi}` leaves five local types `(L, m, e)`: `(1,1,1)`, `(2,2,1)`,
`(3,3,1)`, `(2,1,2)`, `(3,1,3)`. A zero of `N` has `delta` preimages, all
zeros. So `r = delta * z_N + t`. Riemann-Hurwitz for `phi` gives
`s + 2t = 2 delta - 2`. No Galois assumption enters. For `delta = 1` you get
`s = t = 0` and `r = z_N`.

**Claim 2.** `Z'` is the number of zeros of `N` over the three non-A
corners. Fibre sums give `p_X + 3 z_X = d` for non-A classes. Gauss-Bonnet
gives `p_N - z_N = 4`. Eliminating gives the formula. It is an algebraic
identity for a genus-0 target with the parity property.

**Claim 3.** Riemann-Hurwitz for `psi` gives `z_N = d - 1 - R_A / 2`. With
`d >= 2 R_A`, `z_N <= 1` forces `R_A = 0` and `d <= 2`. `d = 2` is impossible
because a zero needs `d >= 3`. So `z_N >= 2` for every parity factor with
`d >= 2`. Then `2 delta <= delta * z_N <= r <= 8` gives the list.

Discrepancies with the audit, all minor:

1. The audit says `z_N >= 2` "needs `phi(S) != phi(T)`". It needs only
   `N != PC`. Separation implies `N != PC`, so the audit's use is valid.
2. Part 2 says the case list needs `t <= delta - 1`. It does not. The list
   follows from `delta * z_N <= r` alone.
3. `0 <= t <= delta - 1` is correct and not sharp. `delta = 2` forces
   `t = 0`, so cases `(2, z)` have `r = 2z` exactly. The audit uses this in
   section 1.7 and omits it from the claim.
4. Section 1.6 says the enumeration finds "exactly types I and II for
   `z_N = 2`, three of each". The script prints nine targets with `z_N = 2`:
   three of type I, three of type II, and three with `(p_A, R_A, z_A) =
   (0,0,1)`. The hand text excludes `(0,0,1)` correctly. The computation
   sentence is imprecise.

**Section 1.3 (darkness).** I checked the fold-back argument line by line.
It is correct. The step `phi(x_{j+1}) = phi(x_{j-1})` holds because `w` is
primitive, so the open segments carry no lattice point and their images
carry no cone point of `N`. The hypothesis "one lift of `S` misses every
lift of `T`" is enough.

**Section 1.8 (the chain).** Each link holds:

- Hypotheses of Theorem 1.1: a finite edge-to-edge union of canonical
  triangles, strictly simple, `W <= 21`, `k <= 6`, two distinct interior A
  points. An orthogonal lattice room is such a union for any choice of
  origin in `Z^2`, because it is a union of unit squares.
- The theorem's `k` is `J + s_N`: interior plus smooth-boundary non-A
  lattice points, each counted once. The audit's weighted count dominates
  it.
- `W = 2r + 4 <= 20`.
- The optical model matches: corners stop rays, and smooth lattice points
  on walls reflect.

**Section 1.7 (hand case analysis).** This is outside the four claims. I
reworked every case: `delta = 1`, the three `delta = 2` cases, `(3,2)` types
I and II, and `(4,2)` types I and II with `X = B` and `X = C1`. I found no
error. Lemma 3 matches the output of `enum_targets.py 4 -v`. The d9 census
gives separate support: within area 20 it reports that `N_min` separates
only the known 22-wall pair, and section 1.6 bounds the area by 16.

## Exact tests on explicit rooms

Script: `check_rooms.py`. Log: `check_rooms.log`. Run time: 10 seconds, one
process.

The script shares no code with the audit. It builds the four corner
permutations by rotating about lattice points. It checks that the cycles
equal the points of `DP` computed from cell counts. It lists all block
systems three ways: every equal-size set partition (area at most 8), orbits
of every candidate block through cell 0, and joins of single-pair closures.
The three lists agree in every case.

Rooms:

- All 3,747 strictly simple fixed polyominoes of area at most 8, in all four
  choices of the A class.
- 19 rooms written by hand, area 5 to 20. They include the staircase, the
  22-wall room, and unions of two, three, and four staircases.

Checks on each of 30,868 factors, with none imposed as a filter:

| Check | Result |
| --- | --- |
| Cone angles of `N` are in `{pi, 2 pi, 3 pi}` and `p_N - z_N = 4` | 0 failures |
| `r = delta * z_N + t` and `s + 2t = 2 delta - 2` | 0 failures |
| Sum of `e` over each fibre of `phi` equals `delta` | 0 failures |
| `Z'` formula and `z_N = d - 1 - R_A/2` on 15,102 parity factors | 0 failures |
| Corrected formula with `- R'/2` on 15,766 non-parity factors | 0 failures |
| Parity property if and only if the partition contains `B_min` | 0 failures |
| `k_wall + 2 k_int <= s` on parity factors | 0 failures |
| `z_N >= 2` on parity factors other than `PC` | 0 failures |

How strong the test is:

- 744 factors are proper (`1 < delta < n`). 200 of them have `t > 0`.
- Only 38 parity factors differ from `PC`, and 19 of those are proper. So
  claims 2 and 3 are tested on few non-trivial instances.
- Cases `(2,2)` and `(2,3)` occur in real rooms: 7 and 9 instances. Example:
  the 8-cell pinwheel with the A class at `(1,1)` has a type II target with
  `delta = 2` and `r = 4`. So the case list is not empty at room level. Two
  interior A points are what the exclusion needs.
- One parity factor has `t > 0`: three staircases around `(-1,0)`, with
  `(delta, z_N, t) = (3, 3, 1)` and `r = 10`.
- The only separating parity factor found is the known one in the 22-wall
  room. No room with `r <= 8` has one. This covers 44 pair-factor
  combinations, so it is a spot check and not a confirmation of section 1.7.

`enum_check.py` enumerates abstract parity targets for `d <= 6` with a
different parametrisation and canonical form. Its counts match the audit's:
1, 0, 6, 7, 21, 57.

## Script findings

- **`room_model.py` reproduces its log.** A rerun gives the same output,
  byte for byte (`rerun_room_model.log`).
- **The corner permutations are right.** `cross_check_audit_scripts.py`
  compares `pillow_model` with my construction on 15,064 room and origin
  cases. Cycle sets, `B_min`, and generated block systems all agree.
- **`all_block_systems` is incomplete.** It returns closures of single pairs
  `(0, b)` only. It misses 76 block systems in 44 of the 15,064 cases. No
  claim in the audit depends on it. The log line labels the output "from
  pairs (0,b)", which is accurate. The function name is not.
- **The formula check in `enum_targets.py` is vacuous.** The audit says
  "Both displayed formulas hold on all of them". The script has no
  assertion. It also keeps a target only if `poles - zeros == 4`. Given
  that filter and the cycle types, the `Z'` formula is forced by algebra.
  The filter is active: it removes 7, 19, and 176 transitive parity tuples
  at `d = 3, 4, 6`. The formula is still true, because it is a proved
  identity. The script adds no evidence for it.
- **The illumination decider was not re-implemented here.** Section 3.4
  rests on it for four boundary pairs. The interior pair of the 22-wall
  room has separate certificates in `d3-review/`.

## Hidden assumptions

- **Normalization.** Claims 1 to 3 need none. `k` depends on the lattice
  presentation, as the theorem's own text says. Claim 4 holds in each
  presentation separately.
- **Strict simplicity.** It gives cone angles of at most `3 pi`,
  `W = 2r + 4`, and the pinch exclusions in section 1.7. A slit gives a
  `4 pi` point and breaks section 1.1.
- **Interior marks.** Claim 4 is false for smooth boundary A points. The
  staircase has `r = 3`, `k = 0`, and `N = DP` separates `a` from `b`. That
  pair is dark at `W = 10`, by Lemma 1 of the 22-wall manuscript. So the
  universal target must say "interior".
- **Points on flat walls.** A smooth point has one lift and costs 1. An
  interior point has two lifts and costs 2. A regular A point over an A pole
  also spends budget. The audit handles all three.
- **Factors that are not Galois.** No step assumes a Galois factor. The
  22-wall factor is not Galois: over one pole it has an `e = 2` point and an
  `e = 1` point.
- **Degree 1.** `N = DP` is a parity factor exactly when `k = 0`. Section
  1.7 then gives `r >= 11`, so an orthogonal room with `k = 0` and two
  interior A points has `W >= 26`.
- **Degree `n`.** `N = PC` is always a parity factor and never separates.
  Every bound in claim 4 excludes it silently.
- **One factor for all three classes.** Sections 1.3 and 1.4 need it. The
  per-class variant is a different mechanism with no bound here.
- **Unit pillowcase only.** A factor is an intermediate cover of the fold to
  `PC`. Section 3.1 argues that triangle-sphere factors add nothing for
  orthogonal rooms. The argument reads correctly. I did not test it.

## What is established

For a strictly simple orthogonal lattice polygon, the Riemann-Hurwitz
bookkeeping in claims 1 and 2 is correct, and it passes exact tests on 30,868
factors of 3,766 rooms. A parity factor other than the pillowcase has
`z_N >= 2`, so `r <= 8` leaves the five listed cases plus `delta = 1`, each
with `k <= 6`. A separating parity factor makes a pair dark. No single
parity factor separates two interior A points when `r <= 8`. Three sources
support that: the computer-assisted `k <= 6` theorem, the hand proof in
section 1.7 that I reworked, and the d9 census within area 20. This removes
the finite check that direction 2 proposed. It does not show that rooms with
`W <= 21` have no dark pair. That still needs the open lit-side statement
"dark implies separating parity factor", and it needs the two open
mechanisms in `d10-mechanisms/theory.md` to be excluded.

## Not checked

- The baseline theorem's certificates and finite reduction.
- The exact illumination results in section 3.4.
- The d9 census. I cite its reported totals only.
- Section 3.1 beyond a read of the argument.
- Rooms with diagonal walls.

## Files

- `review.md`: this file.
- `check_rooms.py`, `check_rooms.log`: factor tests on explicit rooms.
- `enum_check.py`, `enum_check.log`: independent target enumeration.
- `cross_check_audit_scripts.py`, `cross_check_audit_scripts.log`:
  comparison with `room_model.py`.
- `rerun_room_model.log`: rerun of the audit's script.

Reproduce from this directory:

```
python3 -B check_rooms.py 8
python3 -B enum_check.py 6
python3 -B cross_check_audit_scripts.py
```
