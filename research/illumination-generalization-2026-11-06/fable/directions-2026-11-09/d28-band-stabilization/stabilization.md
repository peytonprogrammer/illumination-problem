# Band stabilization: what holds, what fails

Date: 2026-11-10. Direction d28. Nobody has reviewed this document.

Tags: **PROVED** (proof here), **CITED** (project files, not re-derived),
**CHECKED** (computation, with scope), **OPEN**.

## 1. Answer

- The band lemma is true after three corrections, and it is an "if and only
  if" for each direction (Section 2). **PROVED.**
- The lit set along a one-row line is `Lit = U_p Lit_p`. Each `Lit_p` is a
  union of residue classes modulo `2 L p` for every gap `g >= 1`, with no
  threshold (Section 3). **PROVED.**
- A uniform bound on the witness numerator `p` is false. If the pair is dark
  at one gap `g0`, no witness with `p <= P` exists at any
  `g = g0 (mod 2 L lcm(1..P))` (Section 4). **PROVED.** The 22-wall room is
  such a line. So is, on the evidence, a W = 16 room whose gap-0 degeneration
  blocks the pair.
- A finite "covering certificate" proves a pair lit for every gap when it
  exists (Section 5). It exists for every tested pair of the 20-wall
  neighbour of the dark room. **CHECKED.**
- 20-wall minimality does not reduce to a finite check by this route
  (Section 7). **OPEN.**

## 2. Band lemma, corrected

Setup. `P` is an orthogonal lattice room. A *row* is a strip
`c < y < c + 1` between consecutive lattice lines. It meets `P` in chords of
widths `w_1..w_m`. `P_g` is `P` with that row given height `g > 0` (real `g`
is allowed; `P_1 = P`). `S` and `T` are lattice points outside the open row.
`L = lcm(w_i)`.

Corrections to `idea.md`:

1. The cut need not be a vertex-free lattice line. Every cell row works,
   because a row has no vertex in its interior. This matters: the 22-wall
   room has a vertex on every lattice line.
2. A billiard path in an orthogonal room has one primitive direction
   `(+-q, +-p)`. All band crossings share the same `p`. So
   `M(pi) = 2 L p / gcd(q, 2 L)`, which divides `2 L p`.
3. The statement is two-sided, per direction.

**Lemma B (PROVED).** Fix primitive `(q, p)` with `p >= 1`. If
`(g - g') q / p` is in `2 L Z` and `g, g' > 0`, then `(S, T)` is lit in `P_g`
by a path of direction `(+-q, +-p)` if and only if it is lit in `P_g'` by one.
A horizontal path (`p = 0`) never enters the open row, so its status does not
depend on `g`.

*Proof.* Let `g' < g`, `D = g - g'`. Split the tall row into a lower strip of
height `g'` and an upper strip of height `D`. The open row holds no vertex and
no horizontal wall, so a path with `p != 0` that enters a chord crosses the
whole row; it cannot turn back inside. In the `D`-strip it moves
horizontally by `D q / p`, unfolded over the two vertical chord walls. That is
a multiple of `2 w_i`, so it leaves the strip at the same `x` with the same
direction. Deleting the `D`-strip from every crossing gives a path in `P_g'`;
inserting it gives the converse. Each crossing is treated on its own, so any
number of crossings is fine. Edge cases:

- Wall hits inside the strip are flat points (lattice or not): allowed.
  Lattice points inside the strip are interior or flat: allowed.
- A path that reaches a chord end exactly on the row's top or bottom line
  meets a lattice point of that line. That point and its type (corner or
  flat) are the same in both rooms.
- `S` or `T` on the row's boundary lines is fine: the path starts outside the
  open row. `S` or `T` strictly inside the row is excluded; handle it by
  duplicating the row in the skeleton and stretching one copy (Section 6).
- Vertical paths (`q = 0`) satisfy the condition for every `D`.

Parity: when `S` and `T` lie on opposite sides, keep `D` even to stay in one
class.

## 3. Structure of the lit set on a one-row line

**Proposition 1 (PROVED).** Let `G_{q,p}` be the set of `g >= 1` at which a
direction-`(q, p)` path lights the pair. `G_{q,p}` is periodic with period
`2 L p / gcd(q, 2L)`. `Lit_p = U_q G_{q,p}` is periodic modulo `2 L p`, and
`Lit = Lit_0 U U_{p>=1} Lit_p`, where `Lit_0` is all or nothing. So
`U_{p<=P} Lit_p` is periodic modulo `Q_P = 2 L lcm(1..P)`.

**Proposition 2 (PROVED).** Let `F` be the lcm of all chord widths of all
rows. The horizontal multi-twist by `2 F` is an affine automorphism of the
unfolding of `P_g` for every `g`. It fixes every lattice point and maps
direction `(q, p)` to `(q + 2 F p, p)`. So witnesses can be normalised to
`0 <= q <= F p`. `F` does not depend on `g`. The vertical twist does depend on
`g`, so it gives no bound on `p`.

Consequence: for each `p`, `Lit_p` is computable exactly: `2 L p` residues,
at most `F p + 1` values of `q`, each path followed until it meets a corner or
closes up. `band.c` does this.

## 4. The obstruction: p cannot be bounded

**Proposition 3 (PROVED from Lemma B).** If `(S, T)` is dark in `P_g0`, then
for every `P` and every `g = g0 (mod Q_P)` no witness has `p <= P`. Along
`g_P = g0 + Q_P`, either the pair is dark infinitely often or the least
witness numerator is unbounded.

So stabilization statement (b), "a bound on `p` in terms of the skeleton", is
false on every line through a dark room. Statement (c), "dark at `g` implies
dark at `g - Q`", cannot be proved by transporting witnesses, because the
transport modulus `2 L p` is not bounded.

The same argument applies to `g0 = 0` read as the *slit degeneration* `P_0`:
the two sides glued along the chords, with two-sided walls elsewhere on the
line. `P_0` is not a strictly simple room and can block pairs with few walls.
Then the classes `g = 0 (mod Q_P)` have no small witness. **PROVED** as a
mechanism (the proof of Lemma B allows `g' = 0`); for the instance below,
that `P_0` blocks the pair is **OPEN**.

## 5. Measurements (CHECKED, `band.c`, exact integers)

22-wall room, pair `(1,3)-(3,5)`, each of the 6 rows (the room has a
diagonal symmetry, so vertical rows repeat these), odd `g`:

| Fact | Scope |
| --- | --- |
| Dark only at `g = 1` (N_min separates). Lit at every odd `g` in `3..801`, least `p <= 11` | all 6 rows, `p <= 40` |
| Least `p` histogram is concentrated on 2..5; the maximum grows slowly: 10 at `g = 673`, 13 at `g = 1321`, 17 at `g = 480481` | row 0 |
| Lit at every odd `g` in `3..1,441,445`, least `p <= 17` | row 0, `p <= 20` |
| Uncovered residues modulo `Q_12 = 55440`: 8; modulo `Q_16 = 1,441,440`: 4, one of them `g = 1` | row 0 |
| `g -> min p` is not periodic on `1..801` for 4 rows. Rows 3 and 4 show an apparent period 240 on this range; Proposition 3 shows it cannot persist | `p <= 40` |
| Every pair of every stretched room (band-interior points included) is lit | orbitc, complete decider, both axes, 6 rows, `g = 2..7`, area <= 40: 72 rooms, 0 dark pairs |

So band insertion destroys the dark pair at once, and the control behaves as
Proposition 3 predicts: lit, but with unbounded `p`.

**Covering certificate.** If `U_{p<=P} Lit_p` contains every odd residue
modulo `Q_P`, the pair is lit for every odd `g >= 1`. This is a finite check
and, with Lemma B, a proof.

| Room | W | Lines tested | Result |
| --- | --- | --- | --- |
| `r20a` (22-wall room minus cell (5,3)), 1 pair | 20 | 11 rows, both axes | certificate at `P <= 9` on every line |
| `r20a`, row duplicated once or twice (even gaps; points in the band at offset 1 or 2) | 20 | 24 lines, 52 pairs | certificate at `P <= 10` for all |
| `chain16` (three chambers, width-1 corridors), area 34 | 20 | 17 rows, 306 pair-lines | certificate at `P <= 6` for all |
| `dumb12` (two 3x3 chambers, corridor) | 12 | 11 rows, 44 pair-lines | certificate at `P <= 3` for all |
| `x1` (d26 room, area 27) | 14 | 17 rows, 102 pair-lines | certificate at `P = 1` for all |
| `x0` (d26 room, area 24) | 16 | 12 rows, 120 pair-lines | 116 certified at `P <= 2`; 4 not certified at `P = 8` |
| 22-wall room, row duplicated once | 22 | 6 lines | certificate at `P <= 10` for all pairs |
| 22-wall room, row duplicated twice (total gap odd) | 22 | 6 lines | fails on the classes of total gap 1, as Proposition 3 requires |

The 4 failures in `x0` (axis 1, rows 1 and 2, the same two-row gap): the
single uncovered residue is `g = 10079 = -1 (mod Q_8)`, that is total gap
`0 (mod Q_8)`. The pair is lit there with `8 < p <= 12`. This matches the
slit-degeneration mechanism of Section 4. No pair in any W <= 20 test was
unlit at any tested gap (largest 20163).

Lit or dark status was periodic in `g` in every run, trivially: lit
everywhere except the one dark gap of the control.

## 6. Several gaps

- **Several horizontal rows (PROVED).** Lemma B applies to each row. For
  direction `(q, p)` the status depends on each `g_i` modulo `2 L_i p`. A
  covering certificate exists in principle, over `prod_i Q_P(L_i)` residue
  vectors.
- **A point inside a tall gap.** Its row splits the gap into two rows. This
  is the two-row case. Only offsets 1 and 2 were tested.
- **Horizontal and vertical together (obstruction).** A vertical stretch
  changes chord widths `w_i`, so it changes the modulus `2 L p` of every
  horizontal row, and the converse. For a fixed direction the lit set in
  `(g, v)` is not periodic in any fixed lattice. Lemma B gives no joint
  statement.

## 7. Does 20-wall minimality reduce to a finite check?

No, not by this route. Exact obstructions:

1. Covering certificates do not exist on lines whose gap-0 slit degeneration
   (or any other gap value) blocks the pair. There the needed `p` grows
   without bound, on the evidence like the least integer not dividing
   `g - g0` (control: `p = 13` at `g = 1321`, `p = 17` at `g = 480481`). A proof for
   those classes needs a witness family with growing `p`. **OPEN.**
2. For `k` horizontal rows the certificate has about `Q_P^k` residue vectors.
   With `Q_10 = 5040 L` and `k` up to `r + 2 = 10`, that is beyond 10^37.
3. Mixed horizontal and vertical stretching has no periodic structure at all.

What a finite computation could prove: for one skeleton, one row, one pair,
"lit for every gap", at a cost of seconds, when no degeneration blocks the
pair. The number of (skeleton, row, pair) lines with all other gaps equal to
1 and W <= 20 is finite, but those lines do not cover rooms with two or more
long gaps.

## 8. Weakest steps

- `band.c` is new. Checks: it leaves the 22-wall pair unlit at `g = 1` over
  all normalised directions with `p <= 40`; its verdicts agree with orbitc on
  18 stretched 22-wall rooms (`g = 1, 3, 5`). No second tracer replayed the
  individual witnesses.
- Proposition 2 (twist normalisation) is used to truncate `q`. It can only
  lose witnesses if wrong, so "lit" claims do not depend on it; "no witness
  with `p <= P`" claims do.
- The slit-degeneration reading of the `x0` failures is a hypothesis.
- Test rooms are few (6 rooms with W <= 20). No census-scale run.

## 9. Files

- `band.c`: tracer, `Lit_p` tables, N_min check, covering certificates.
  `band AXIS ROW PMAX GMAX [dup] [quiet]`.
- `cover.sh`, `summ.py`, `stretch.py`, `allpairs.py`: drivers and orbitc
  cross-checks.
- `rooms/`: test rooms. `runs/`: outputs.
- Compute used: about 12 minutes wall-clock, at most 3 workers, under 1 MB.
