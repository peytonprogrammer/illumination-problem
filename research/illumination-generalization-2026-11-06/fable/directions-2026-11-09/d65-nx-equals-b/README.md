# d65: the case N_x = B

Date: 2026-11-18. Theory plus exact checks on named rooms and on saved census data
(`d12-lit-side/mine_n*.json`). No room, ray, direction, or reflection-word search.
Tags: **PROVED** (argument here), **COMPUTED** (exact check here), **CITED** (proved or
checked elsewhere), **GUESSED** (judgment).

## Answer

- **The claim is refuted as stated (COMPUTED).** The d63 claim says that, in a
  normalized strictly simple orthogonal room with `N_x = B`, every pair of regular
  class-a points of `DP` is x-lit unless Rig(x) or Cut(x) holds. It fails in a 10-cell,
  12-wall room `S10` with interior lattice marks. The d14 n = 10 obstruction is
  realized by real rooms.
- **No planar hypothesis excludes d14 per lift pair (COMPUTED).** 4 of the 18 d14
  relations are doubles of strictly simple, normalized, orthogonal rooms (`Z12` and
  `S10`). Two of them have interior marks. Planarity, strict simplicity,
  orthogonality, normalization, and interior marks all hold there.
- **The mechanism is a deck involution (PROVED, Lemma M).** Every n = 10 d14 dark
  pair is a pair `{s, delta s}` for the deck involution `delta`. If `delta` has no
  fixed point over `a` or `x`, such a pair is x-lit only by a light loop that
  separates the 2 fixed points of `delta`. No bounce or one-bounce path can join it.
- **What excludes d14: the room-pair form (RL-room).** The target only needs a
  per-class statement about room pairs: all four lift pairs x-dark implies
  certificates. In `S10` the `delta`-pairs are dark. The `iota delta`-pairs are lit,
  so the room pair is x-lit. RL-room has 0 counterexamples on 16 interior room-pair
  rows with `N_x = B` in 11 rooms (weak evidence). It isn't proved.
- **Exact gap.** RL-room for (1) symmetric rooms: the `iota delta`-pair needs a
  transport statement in `N = Q / delta` (section 5); and (2) rooms with trivial deck
  group: there it's still per-class Lemma H on `iota`-classes.
- CPU: under 2 s in total, one process at a time.

## 1. Hypothesis ladder and the d14 relations

Room structure on a tuple `t`, from the d6 model (`d6-hurwitz-census/involution_flag.py`):

| Level | Hypothesis |
| --- | --- |
| H0 | Genus-0 pillowcase cover, cycle lengths 1, 2, 3 |
| H1 (real) | Some state has a seam-reflection lift `iota` with a fixed edge, so `Q / iota` is a disc |
| H2 (flat) | Also every pole and zero of `Q` lies on the fixed circle (no interior cone point) |
| H3 (planar) | Also the development is injective with no slit and no pinch: a strictly simple room |
| H4 | Also normalized (no proper pillowcase factor) |
| H5 | Also both marks are interior lattice points |

`d14_reality.py` reads the saved verdicts and recomputes non-transitivity. It finds
the d14 section 4.3 family: |G| in {1920, 3840}, one block system with blocks of size 2,
and x-lit not transitive. It walks each plain pure-braid orbit (and its b <-> d mirror)
and classifies every seam-reflection lift.

COMPUTED (`d14_reality.log`):

- Exactly 18 relations: 12 with |G| = 1,920 and 6 with |G| = 3,840. 6 have no
  identity corner in `N`. This matches d14.
- All 18: `B_x` is the one-block system, the dark pairs are `delta`-pairs, and no
  dark pair has a Par, Rig, or Cut certificate over any block system.
  - This corrects d63 section 1.2(b). It said only the 6 relations without an
    identity corner are uncertified.
  - Rig needs the two images in different live components. A same-fibre pair never
    has that, so an identity corner doesn't help.
- Every one of the 12 orbits satisfies H1 in some state.
- 3 orbits (4 relations) reach H2. All 3 also reach H3 and H4:

| Room | Cells (rows top to bottom) | Walls | d14 relations | Marks |
| --- | --- | --- | --- | --- |
| `Z12` | `#.####` / `####.#` | 12 | x = b, and the transposed copy at x = d | smooth wall points |
| `S10` | `##..` / `###.` / `.###` / `..##` | 12 | x = b and x = d | interior (1,3), (3,1) for class (1,1) |

- The other 9 orbits (14 relations) stop at H1: interior cone points, or `Q / iota`
  is RP^2.

Scope check with `--all` (`d14_reality_all.log`): every non-transitive saved relation
for n = 4 to 10 gives 30 relations. The other 12 have n = 8.

- 6 have |G| = 16. Their `delta`-pairs are dark, and the planar ones are the 2 x 4
  rectangle `R24`.
- 6 have |G| = 48. Their dark pairs aren't `delta`-pairs, and `B_x` has 2 blocks. The
  planar ones are the 8-cell rooms `T8` and `Z8`.
- `R24`, `T8`, and `Z8` aren't normalized (horizontal gcd 2 or 4). Every row with
  `N_x = B` in them is x-lit (`rl_room.log`). So these 12 relations are outside the
  `N_x = B` claim.

## 2. The counterexample room S10 (COMPUTED)

`S10` cells: (0,2), (0,3), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (3,0), (3,1).

- Strictly simple, normalized, r = 4, W = 12.
- It's symmetric under the rotation `sigma` by pi about the interior lattice point
  `C = (2,2)`.
- Take marks of class a = (1,1): the interior points `S = (1,3)` and `T = (3,1) = sigma S`.
  Then `b = (0,1)`, `c = (0,0)` (the class of `C`), and `d = (1,0)`.

The rows (`notch12.py`, exact orbit walk from the room's own tuple; d63 `test_level`):

| Lift pair | x = b | x = d |
| --- | --- | --- |
| `S_f`, `T_f` (`delta`-pair) | dark | dark |
| `S_b`, `T_b` (`delta`-pair) | dark | dark |
| `S_f`, `T_b` (`iota delta`-pair) | lit, depth 2 | lit, depth 2 |
| `S_b`, `T_f` | lit, depth 2 | lit, depth 2 |

- `N_x = B` at b and d: `B_x` is one block.
- No dark row has Par, Rig, or Cut over any block system, `DP` included.
- At c, `N_c` has degree 5 and every row is lit.
- At room level every pair is lit (d9 `orbit.decide`, complete). This agrees with the
  d15 theorem and the d9 census.
- The verdict agrees with the census verdict saved by d12 `mine.py`, which is
  independent code.

`Z12` (2 x 6 rectangle minus cells (2,1) and (5,0)) gives three wall-mark room pairs
that are x-dark and uncertified with `N_x = B`. It also gives the pair `C_f, C_b` over
its centre `C = (4,1)`.

## 3. Lemma M: the d14 mechanism (PROVED)

**Lemma M.** Let `Q -> B` be a genus-0 pillowcase cover with cycle lengths 1, 2, 3.
Let `delta != 1` be a deck involution, `N = Q / delta`, and `s` a regular a-point with
`delta s != s`. Fix `x != a`.

1. `delta` has exactly 2 fixed points. Both are regular points of `Q` over corners,
   and each lies over a pole of `N`.
2. The live poles of `N` over `a` and `x` are the images of the fixed points over `a`
   and `x`.
3. Suppose no fixed point lies over `a` or `x`. Then `s` and `delta s` are x-lit
   exactly when some state has a live component `K` of `u = [s]` that's a cycle
   separating the 2 branch values of `Q -> N`.

Proof.

1. `Q -> N` has degree 2 between spheres. Riemann-Hurwitz gives `-2 = 2(-2) + R`, so
   `R = 2`. A deck transformation that fixes a point over a non-corner is the
   identity. At a fixed point the local degree over `N` is 2. Over `B` it is at most 3,
   so it's 2: the point is regular, and its image is an `N`-pole.
2. A live pole is an `N`-pole `{s', delta s'}` with a regular `Q`-point above it. That
   point is the 2-cycle `(s', delta s')`, which `delta` fixes.
3. `u` is `N`-regular: otherwise the `Q`-point of `s` would be the 2-cycle
   `(s, delta s)`, a single point. By part 2, `K` has no live pole. d14 Lemma D2
   (CITED, PROVED there) then says the pair is joined exactly when `K` is a cycle
   whose lift isn't closed. A degree-2 cover of the sphere, branched at 2 points, has
   non-trivial monodromy around a simple closed curve exactly when the curve separates
   them.

COMPUTED (`rl_room.py`): every deck involution in the 11 rooms has exactly 2 fixed
points, both regular (28 checks). Every uncertified x-dark lift pair of distinct
points is a `delta`-pair with no `delta`-fixed point over `a` or `x`. That's 15 of 15
rows in `Z12` and `S10`.

Consequences:

- **One-bounce and channel paths can't join a `delta`-pair (PROVED).** The image in
  `N` of such a path would reverse at a live pole (FC part 4), and part 2 rules that
  out. This kills idea (ii) for these pairs.
- **In a room, the fixed points are geometric (GUESSED in general; COMPUTED here).**
  d10 R6 (CITED) says size-2 systems come from symmetries of `P`. For a rotation by
  pi about a lattice point `C`, the fixed points are `C_f` and `C_b`, both over the
  class of `C`. So for x not equal to that class, the pair `S`, `sigma S` (same
  copy) is x-lit only by a light loop that, with its rotated copy, separates
  `C_f` from `C_b`.
- **The d14 obstruction lives in centrally symmetric rooms.** Its centre is a lattice
  point of the fourth class. That's the geometric invariant behind it. It isn't
  non-planarity.

## 4. The corrected claim

**RL-room.** Let `P` be a normalized strictly simple orthogonal lattice room, `a` a
corner class, and `x != a` with `N_x = B`. Let `S != T` be interior lattice points of
class `a`. If all four lift pairs of `(S, T)` are x-dark, each has a Rig(x) or Cut(x)
certificate.

- **It suffices for the target (PROVED).** A dark room pair has all four lift pairs
  x-dark for every `x`. So RL-room can replace RL in d63 section 1.3 step 2, and the
  rest of the chain is unchanged. The `N_x != B` part (RL-fin) and the gaps G1 and G2
  from d63 are as before.
- **Two lift pairs are enough (PROVED).** `iota` maps a light path in direction
  `(p, q)` to one in direction `(p, -q)`. It fixes the corners, so it keeps the class
  `x`. Hence `(S_f, T_f)` is x-lit iff `(S_b, T_b)` is, and `(S_f, T_b)` iff
  `(S_b, T_f)`.
- **Each hypothesis is needed (COMPUTED or CITED):**

| Dropped hypothesis | Witness |
| --- | --- |
| Room pair (state it per lift pair) | `S10`, x = b and x = d |
| Interior marks | `Z12` (3 room pairs), `S10` (4), wall marks |
| Normalized | cross scaled by 3 (d39, d43; CITED) |
| Room (H3) | Without `iota` the room-pair form isn't defined. 14 d14 relations are non-planar. |

- **Tests (COMPUTED, `rl_room.log`).** The rooms: cross12, dumb12, R22, P6, P6found,
  the L-room, `Z12`, `S10`, `T8`, `Z8`, and `R24`. That's the d63 list plus the five
  census rooms. The d38 and d43 named rooms are the 22-wall room, P6, the L-room, and
  cross scaled by `k`. All are here except cross x 3 (n = 108, not normalized).

| Rows with `N_x = B` | Count | x-dark | x-dark, uncertified |
| --- | --- | --- | --- |
| Interior room pairs | 16 (cross12 2, dumb12 12, `S10` 2) | 2 (cross12, Cut) | 0 |
| Interior lift pairs of distinct points | 64 | 12 (cross12 8, Cut; `S10` 4) | 4 (`S10`), all `delta`-pairs |
| Wall room pairs | 222 | 7 | 7 (`Z12` 3, `S10` 4) |

The evidence is weak. Only 16 interior room-pair rows have `N_x = B`. R22 and P6
contribute none, because their interior marks have `N_x != B`.

## 5. What is proved toward RL-room, and the exact gap

**Symmetric rooms (deck involution `delta`, `T = sigma S`).**

- `(S_f, T_f)` is governed by Lemma M.
- The remaining pair `(S_f, T_b)`, with `T_b = iota delta S_f`, has distinct images
  `u` and `iota u` in `N`. There's no live pole over `a` or `x` (Lemma M part 2). So
  by d14 I1 and I2 (CITED), the following holds. A state lights some lift pair over
  `{u, iota u}` exactly when `u` and `iota u` share a live component. The lift from
  `S_f` then ends at `S_b` (the `iota`-bijection) or at `T_b` (the
  `iota delta`-bijection).
- **Gap S.** Suppose no state has a separating `K` at `u`. Show that some state
  transports by the `iota delta`-bijection, unless a certificate holds. In `S10` both
  bijections occur: depth 0 and depth 2 states. No argument is known. It's a parity
  statement about how `delta`'s branch points sit relative to the live loops through
  `u` and `iota u`.

**Trivial deck group.**

- No saved census relation with n <= 10 shows non-transitivity at `N_x = B` without a
  deck involution (section 1).
- RL-room there is per-class Lemma H plus E on the `iota`-orbits. That's the d14 dead
  end, now on room pairs.
- **Gap A.** Nothing in this directory reaches it. The only room input known to
  matter is `iota`. Group-only arguments stay excluded.

**Hypothesis that excludes d14 and is consistent with all data (GUESSED as the right
form).** RL-room, H3 + H4 + H5 + room pairs. The strongest hypothesis that excludes
the d14 mechanism outright is a trivial deck group of `DP -> B` (no lattice symmetry
of `P`). Lemma M plus the census shows every n = 10 d14 dark pair needs `delta`. No
proof follows under either hypothesis.

## 6. Consequences for STATE.md

- "x-dark implies a certificate per lift pair" (d61 and d63 RL) is false for rooms.
  Replace it with RL-room.
- d63 section 1.2(b) should say all 18 d14 relations are uncertified. 4 of them are
  rooms (`Z12`, `S10`).
- Every symmetric-room proof route must handle Lemma M. Light between `S` and
  `sigma S` on the same copy needs a loop around the symmetry centre.

## Files and CPU

| File | Content |
| --- | --- |
| `d14_reality.py`, `.log`, `.json` | d14 family: reality ladder, deck involutions, `B_x`, certificates. `--all 4 ... 10` writes `d14_reality_all_*`. |
| `develop_planar.py`, `.log`, `develop_planar_all.log` | Planar developments of those orbits |
| `notch12.py`, `.log`, `.json` | `Z12` and `S10` from cells: rows, positions, certificates over all factors, room-level verdicts |
| `rl_room.py`, `.log`, `.json` | Lift-pair versus room-pair test on 11 rooms, deck-involution checks |

Run each with `python3 -B <file>` from this directory. Reused, read-only:

- d6 `hurwitz.py`, `involution_flag.py`, `d4_monodromy.py`
- d10 `unified_test.py`, `roomtools.py`
- d9 `orbit.py`
- d60 `fh_star.py`, d61 `fold_converse.py`, d63 `realize.py`

CPU (measured with `time`): `d14_reality.py` 0.1 s (three runs), `--all` 0.4 s,
`notch12.py` 0.12 s (two runs), `rl_room.py` 0.3 s (four runs), `develop_planar.py`
0.1 s (two runs). Total under 3 s, one process at a time.
