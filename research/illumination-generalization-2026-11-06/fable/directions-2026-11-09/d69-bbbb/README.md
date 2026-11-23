# d69: a geometric decomposition attempt at the BBBB case of OL

Date: 2026-11-18. Theory plus exact checks on named rooms, eight hand-built rooms, and the
saved d64 room list. No room, ray, direction, or reflection-word discovery search. Tags:
**PROVED** (argument here), **COMPUTED** (script and log here), **CITED** (file),
**GUESSED** (judgment).

## Verdict

**No proof of BBBB. Partial foothold: a lattice lemma, and the exact first step that fails.**

- The rectangle step holds (PROVED). The door step is decidable per pair, but nothing proves
  it in general. The chain step is where the decomposition fails.
- The counting identity forces nothing geometric beyond "no Q class". BBBB rooms with
  area > 36 can contain unit corridors of any length (section 1).
- **Midpoint lemma (PROVED, new).** Every lighting path of a same-class lattice pair passes
  through a lattice point at its midpoint. For lattice rooms, this explains why they sit on
  resonance sets. It makes lattice arithmetic an obstruction for monotone path families,
  not a tool (section 2).
- **One-axis families cover every tested BBBB pair (COMPUTED).** The families are visible,
  x-monotone, y-monotone, and one bounce off an extreme wall line (V, X, Y, B). They cover
  all 726 same-class pairs in 7 hand-built BBBB rooms with area 41 to 63. The exact orbit
  verdict lights every pair in those rooms, and no lift pair is x-dark at any target.
- **First failing step (COMPUTED).** In OL's own range, `cov2929` has two asymmetric pairs that
  no V, X, Y, or B path lights. No room symmetry swaps either pair. The room is R\*, BBBQ,
  W = 20, area 22. d66 lights both pairs.
  - Every path that lights them reflects off walls of both orientations, away from the
    extreme lines.
  - No explicit family with a proved success condition covers such turning routes.
  - The transfer lemma (section 4) shows that lattice arithmetic can't rescue a family that
    fails on an open set of real lengths. d58 found such open failures at cut hubs.
- CPU: about 25 s in total, one process at a time.

## 1. What BBBB plus area > 36 forces

**Types (CITED).** Area > 4r + 4 rules out a Q class (d68). Area > 8r rules out a proper
factor (d63, d66). So at `r <= 8`, every normalized room with area > 64 is BBBB. Rooms
with area 37 to 64 are BBBB or have a proper factor. d64 closes the rooms with a proper
factor.

**Thin parts are not controlled (PROVED by example, types COMPUTED).**

- `DB55` consists of two 5 x 5 squares joined by a unit corridor of length 3. It has
  `r = 4`, `W = 12`, area 53, and type BBBB.
- Lengthening the corridor or the squares keeps `r = 4`, so unit corridors of any length
  occur in BBBB rooms.
- Pick's theorem gives `int = n - Lambda/2 + 1`, where `Lambda` is the perimeter. So a
  room with area > 36 can have a single interior lattice point, for example a 3 x 3 square
  with a long unit arm.
- The counting identity bounds no single class from below.

**Where lattice points sit (PROVED).**

- An interior lattice point needs all four cells around it. So a width-1 corridor holds no
  interior lattice point; all its lattice points are wall points.
- Same-class pairs therefore always cross unit corridors, and never start inside one.
- A width-2 corridor holds interior points only on its midline, at any depth (`DBw2`).
- Lemma U's deep-point danger (d57) can arise in lattice rooms only at width 2 or more
  (GUESSED that d57's bound applies there unchanged).

## 2. Midpoint lemma

**Lemma MP (PROVED).** Let `S` and `T` be lattice points of one class in a lattice room. Let
`gamma` be a billiard path from `S` to `T` that avoids vertices. Then `gamma` passes through
a lattice point at half its length. That point is interior or a smooth wall point.

Proof:

1. Unfold `gamma` to a segment from `S` to an image `T*`. The unfolding uses reflections in
   integer lines.
2. A reflection in an integer line preserves coordinates mod 2. So `T* = T = S (mod 2)`.
3. Hence the midpoint `(S + T*)/2` is a lattice point of the plane. It folds to a lattice
   point of the room on `gamma`.
4. `gamma` avoids vertices, so that point is interior or smooth. ∎

Equivalently, in the development `T*` is the half-turn image of `S` about a lattice point.
The direction `(p, q)` is primitive, and `T* - S = g (p, q)` with `g` even.

**Corollary MO, midline obstruction (PROVED).** An x-monotone path reflects only off
horizontal walls. It crosses the line `x = (s1 + t1)/2` once, at that midpoint. The crossing
point must be interior, or a smooth point of a horizontal wall. If the line has no such
lattice point, family X is empty. Family Y is the transpose.

**Data (COMPUTED, `midline.py`).** The data covers all non-visible pairs in all 4,581 d64
rooms, the named rooms, and the hand-built rooms.

- MO fires on 254 of 1,067 X failures and 160 of 727 Y failures.
- It never fires on a pair that the family lights: 0 soundness failures.

**Reading (GUESSED).** d58 states that lattice rooms sit on resonance sets. That's MP at
work.

- For a unit door, Lemma P's `n = L h / (w D)` is always an integer, so the phases decide.
- MO is the special case in which the midpoint lands on a door line, at a vertex.
- In `DB55`, 8 of the 12 pairs that need family B are pairs where X is midline-blocked
  (`s1 + t1 = 2 * 5` or `2 * 8`, the two door lines).

## 3. The decomposition, step by step

| Step | Statement | Status |
| --- | --- | --- |
| 1. Rectangle | If the closed bounding box of `S` and `T` lies in the open room, or the segment `ST` lies in it, the pair is lit. | PROVED (trivial) |
| 2. Door | One-axis families X, Y, and B decide exactly per pair. Validity is periodic in the slope with period `2 L`, where `L` is the lcm of the run lengths, so one period is checked. | Decision PROVED. No general success theorem. |
| 2'. Lattice dumbbell lemma DL | In every unit-corridor dumbbell, every same-class pair is lit by V, X, or B. | OPEN. COMPUTED on `dumb12`, `DB55`, `DBas`. `DB55` needs B for 12 pairs. |
| 3. Chain | Induct over rectangles. | **FAILS: no inductive invariant, residual pairs exist (below)** |

**Door step in a unit-corridor dumbbell (PROVED, reduction only).**

- Take the left rectangle `[0, A] x [0, H]`, a corridor `[A, A + l] x [c, c + 1]`, and the
  right rectangle at height `[b, b + H']`.
- Every reflection group met along an x-monotone path is generated by reflections in integer
  lines. So the composite map from the corridor to the exit door image `(j, j + 1)` is
  determined by `j` alone:
  - the translation by `j - c` when `j = c (mod 2)`;
  - the reflection `y -> c + j + 1 - y` otherwise.
- With `delta = (t1 - s1)/2` and slope `j'/delta` (by MP), family X lights the pair exactly
  when some integer `j'` meets three conditions:
  1. The entry height `s2 + (A - s1) j'/delta` folds into `(c, c + 1)`.
  2. The exit height `s2 + (A + l - s1) j'/delta` isn't an integer.
  3. `s2 + 2 j'` is an image of `t2` under that composite.
- This is a finite congruence problem. I didn't find a proof that X or B always succeeds.

**Residual pairs (COMPUTED, `decomp.py`, `symcheck.py`).** A residual pair is lit by none of
V, X, Y, and B.

| Set | Pairs | V | X | Y | B | Residual |
| --- | --- | --- | --- | --- | --- | --- |
| d64 rooms (4,581, area <= 40) | 11,437 | 5,997 | 2,248 | 2,808 | 316 | 68 |
| Hand-built (8 rooms) | 743 | 429 | 225 | 16 | 73 | 0 |
| Named rooms | 13 | 5 | 5 | 0 | 0 | 3 (R22, P6, P6found: the dark controls) |

- Of the 71 residual pairs, 56 are swapped by a room symmetry (mirror or half-turn). For
  those, d66's relay reduces the pair to "S sees a fixed point on the axis". That's a
  different-class or wall-target lit statement, which is open (G1).
- 15 residual pairs are asymmetric. 3 are the dark controls. In OL's range (R\*, area >=
  21), the asymmetric residual pairs are `cov2929` `(3,1)-(5,3)` and `(3,3)-(5,5)`. The
  other asymmetric ones lie in rooms with a proper factor, which d64 closes.

```
cov2929, n = 22, r = 8, W = 20, types 00 Q, 01 B, 10 B, 11 B (pair_level.json: 7 pairs, all lit, 0 x-dark rows)
y=5  ....##.#
y=4  ....####
y=3  ..####..
y=2  ..####..
y=1  ####....
y=0  #.##....
```

The three blobs meet only at reflex corners along a staircase. The segment `ST` hits the
reflex corner `(4,2)`.

**Hand-built BBBB rooms (COMPUTED, `verdicts.py` with the d66 orbit model).** All are
normalized, with types BBBB, every pair lit, and 0 x-dark rows at any target:

| Room | Area | r | W | Pairs |
| --- | --- | --- | --- | --- |
| `DB55` | 53 | 4 | 12 | 112 |
| `DBas` | 48 | 4 | 12 | 81 |
| `DBw2` | 63 | 4 | 12 | 190 |
| `CR34` | 57 | 4 | 12 | 144 |
| `c4181s` | 41 | 8 | 20 | 27 |
| `U2` | 46 | 3 | 10 | 52 |
| `st279` | 56 | 6 | 16 | 120 |

`c4181s` is the d66 failure room `cov4181` stretched to area 41. In it the per-target failure
disappears. `st279` is the residual room `cov279` with its end blobs stretched. Stretching
gives the blobs full back walls, and family B then lights the former residual pair. This
fits d66's guess that per-target forms may hold in BBBB rooms. It's weak evidence: these 8
rooms are hand-picked, not a sample.

## 4. Transfer lemma

**Lemma TR (PROVED, sketch).** Fix a combinatorial type with `r <= 8` and a path family `F`
defined combinatorially, such as a reflection-word set or "x-monotone". Suppose `F` fails
for every configuration in a non-empty open set `U` of real (lengths, S, T). Then `F` fails
for some same-class interior lattice pair in infinitely many normalized lattice rooms. Each
of those rooms is BBBB, with area > 64.

Proof:

1. Billiards and `F` are scale-invariant, so `U` is a cone.
2. For large `lambda`, the ball `B(lambda u, lambda eps)` inside `U` has radius > 3. So it
   contains integer points with prescribed parities: `S = T (mod 2)`. Its horizontal lengths
   can have gcd 1, and so can its vertical lengths.
3. Interior lattice points of a lattice room have four cells. Strict simplicity is open.
4. Area grows like `lambda^2`, and section 1 gives BBBB. ∎

**Consequence (PROVED from CITED).**

- d58 found failure sets with non-empty interior at cut hubs, for the Lemma C+ K-condition
  family (r3.md's type 4991). By TR, those failures recur in BBBB lattice rooms. So a
  decomposition proof needs turning families whose failure sets have empty interior.
- MP adds the other direction: lattice rooms sit on special closed sets where monotone
  families fail even though they succeed for generic real lengths.
- Lattice arithmetic helps in neither case. GUESSED: this is why "decomposition plus
  lattice arithmetic" doesn't close BBBB without a new turning lemma.

## 5. The exact remaining step

**Lemma T (turning, OPEN).** In a normalized room with `r <= 8`, let a same-class pair
lie in no common one-axis unfolding. That covers V, X, Y, and B, including through extreme
back walls. Then the pair is lit by a path family whose success condition is proved.

- The first instance in OL's range is `cov2929` (BBBQ).
- No BBBB instance is known. Finding one needs a room search, which needs approval.
- Proving DL (section 3) would close the dumbbell class only. It doesn't induct, because
  `cov2929`-type staircases have no door at which a monotone family applies.

Estimate (GUESSED): the BBBB claim can't be proved by this decomposition with current
tools, about 3%. Proving DL by itself, as an elementary number-theory exercise, is about
40%.

## Tests and files (all COMPUTED, exact integer arithmetic)

| File | Content | CPU |
| --- | --- | --- |
| `decomp.py`, `decomp.log`, `decomp.json` | Families V, X, Y, B on named, hand-built, and all 4,581 d64 rooms. The period cap of 3,000 was never hit (0 skipped). | 0.7 s |
| `crosscheck.py`, `crosscheck.log` | `decomp.trace` against d66 `g1_check.shoot` on fixed direction lists: 16,632 agree, 0 disagree | 1.8 s |
| `verify_b.py`, `verify_b.log` | Every B witness (389) folded back and traced in the room: 389 verified, 0 failed | 0.7 s |
| `midline.py`, `midline.log` | Corollary MO: soundness and coverage | 0.6 s |
| `symcheck.py`, `symcheck.log` | Symmetry type of residual pairs | 0.1 s |
| `verdicts.py`, `verdicts.log` | d66 orbit verdicts and types on the hand-built rooms | 8.7 s |

The first `verify_b` run reported 25 failures. They came from a verification bug: the
reversed direction was taken at the wrong end of the path. The fix uses the initial
direction mirrored in the glued line. After the fix, 0 failures.

Total about 25 CPU-s, including reruns and one debug check, one process at a time. Run with
`python3 -B <file>` from this directory. Reused read-only: d10 `roomtools`, d63 `realize.rooms`,
d65 `notch12`, d66 `pair_level.test_room` and `g1_check.shoot`, and d64 `covers.json`.
Nothing was written outside this directory, and nothing in git changed.
