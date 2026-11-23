# Direction 4: monodromy block systems (computations on rooms in the record)

Opus 5.5 subagent, 2026-11-09. Exact permutation arithmetic only. No room search was run. Every number below comes from a script in this directory. Inputs were copied into `inputs/` unchanged, or read in place with SHA-256 recorded. Not independently reviewed.

## Summary

- The prediction holds for the 22-wall room. In the pillow framework, G has exactly one proper block system. It has block size 3, and its quotient N equals D(staircase) generator by generator. N has the parity property, and phi(S) != phi(T). DP itself fails the parity property at exactly the 4 transparent points.
- G(22-wall) = (S3 wr A5) ∩ A15, of order 233,280. G(staircase) = A5.
- The Direction 4 falsifier, "a dark room whose sheet monodromy is primitive", is met. All 327 census rooms, Tokarsky 26, Castro 24, and the 34-wall orthogonal room (in the pillow framework) are dark and have G = S_n or A_n. They all have k = 0, so the trivial factor N = DP already has the parity property. The conjecture in Direction 2 survives. The dichotomy "G primitive => lit" does not.
- Controls: none of 18,219 lit rooms with W <= 21 has a proper factor with the parity property and phi(S) != phi(T). All 31 orthogonal lit rooms (k = 7) have primitive G in the pillow framework. 11 of the 45-degree lit rooms are imprimitive. In each, the only proper block system comes from a room symmetry that swaps S and T, so phi(S) = phi(T).
- Saved 10,368-state certificate: no state has one horizontal cylinder. The minimum is 2. In the 1,728 states where the source leaf is regular, all 4 source lifts sit on the middle line of height-2 cylinders, and no target lift lies in the closure of those cylinders.

## Setup and choice of base

- **Pillow framework (`square`).** The base B is D([0,1]^2), folded by the triangle wave in each coordinate. This is the project's `E/(-I)` with `E = R^2/(2Z^2)`. Its four corners are the four parity classes: A = (0,0), B = (1,1), C1 = (1,0), and C2 = (0,1), each with angle pi. Sheets are the n unit squares of DP over the top face, so the degree is the area. I chose the unit pillow because its corner fibres are exactly the parity classes. A 2x2 pillow would make odd lattice points regular points of the base.
- **Triangle framework (`tri`).** The base is the double of the canonical45 tile, with A = (even, even) at pi/2, B = (odd, odd) at pi/2, and C = mixed at pi. This framework is needed for the 45-degree rooms. For an orthogonal room it always has an extra block system of size n_squares, which is the pillow D([0,1]^2) as an intermediate cover.
- **Generators.** g_c is the product of the two edge-gluing involutions at corner c, acting on sheets. A cycle of length L is a point with angle L times the base angle at c.
- **Parity property.** No point of N over a B or C corner has angle 2 pi.
- **phi(S) != phi(T).** The images of all DP lifts of S and T in N are disjoint sets of points.
- **Algorithms.** Block systems are computed by Atkinson minimal-block closure over all blocks containing sheet 0. Each one is verified directly. Group orders come from deterministic Schreier–Sims. For degree >= 8, primitive G, and a word of length <= 3 with a power that is a p-cycle (p prime, p <= n-3), Jordan's theorem gives A_n <= G. `check_orders.py` confirms that this shortcut agrees with Schreier–Sims on all 390 rooms in tasks 2 and 3 that are not read in place; it used the shortcut on 352 of them.

## Task 1: the 22-wall room (`task1_room22.py`)

Checked from the manuscript: the union of P0, P1, and P2 equals the interior of the 22-vertex cycle. The room has area 15, 22 walls, 9 reflex and 13 convex corners, and interior lattice points {S = (0,0), T = (2,2)}. The transparent non-A points are (-1,0), (1,0), (2,1), and (2,3), all of class C. Each of S and T has two lifts in DQ, each with angle 2 pi.

Pillow framework: degree 15, |G| = 233,280, transitive and imprimitive. All generators are even. Generator cycle types are A [2^6 1^3], B [3^3 1^6], C1 and C2 [3^3 2^2 1^2].

| Block size | Blocks | N cone angles (units of pi) | Parity | phi(S) != phi(T) |
| --- | --- | --- | --- | --- |
| 1 (N = DQ) | 15 | A: 1x3, 2x6; B: 1x6, 3x3; C1, C2: 1x2, 2x2, 3x3 | no (4 regular C points) | yes |
| **3** | 5 | A: 1, 2, 2; B, C1, C2: 1, 1, 3 | **yes** | **yes** |
| 15 (N = B) | 1 | all 1 | yes | no |

- **Fibres of the fold.** The fibres of the manuscript fold f form the size-3 system. The induced generators equal the staircase's own generators under f.
- **Ramification.** DQ -> N ramifies only at the 4 transparent points, each with e = 2 over a convex corner of the staircase (angle pi). Riemann–Hurwitz gives 2 = 3·2 - 4.
- **Where the marks sit.** The S lifts lie in blocks {0, 2}, and the T lifts lie in blocks {3, 4}.
- **Group structure.** The block action is A5 (order 60), and the kernel has order 3,888. The stabiliser of a block acts on it as S3. The bound S3 wr A5 has order 466,560 = 2|G|. Since G <= A15, G = (S3 wr A5) ∩ A15 (`task5_structure.py`).
- **Staircase base.** The staircase alone has degree 5, G = A5, and is primitive.

Triangle framework: degree 30, |G| = 466,560. The block sizes are 1, 2, 3, 6, 15, and 30.

| Size | What N is | Parity | phi(S) != phi(T) |
| --- | --- | --- | --- |
| 2 | DQ / tau, where tau is the reflection in x + y = 2, which swaps S and T | no | no |
| 3 | D(staircase) | yes | yes |
| 6 | quotient of D(staircase) by its reflection in x - y = 2, which swaps a and b | yes | no |
| 15 | pillow | yes | no |

**Outcome.** The prediction holds. No other proper block system exists in the pillow framework.

## Task 2: other dark rooms (`task2_dark_rooms.py`)

| Room | W | r | k | Framework | Degree | G | Proper block systems |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tokarsky 26 | 26 | 13 | 0 | tri | 29 | S_29 | none |
| Castro 24 | 24 | 11 | 0 | tri | 27 | S_27 | none |
| O'Rourke 34 (orthogonal) | 34 | 15 | 0 | square | 19 | A_19 | none |
| O'Rourke 34 | 34 | 15 | 0 | tri | 38 | imprimitive | size 19 only (pillow; parity yes, phi(S) = phi(T)) |
| 327 census rooms | 24–26 | | 0 for all | tri | | 197 S_n, 130 A_n | none in any room |

For every room in this table, the discrete factor N = DP has the parity property and phi(S) != phi(T), as expected for k = 0.

Sources:

- Tokarsky 26 and Castro 24: vertex lists in `inputs/peyton-worksheet-build.py.txt`, parsed with `ast`.
- O'Rourke 34: `inputs/historical34-room.json`.
- Census: `inputs/census/`. Each room has `lit: 0` in the record.

## Task 3: lit controls with W <= 21 (`task3_lit_controls.py`)

Lit status comes from the record. The script checks each saved path's endpoints against the marks but doesn't replay the path.

| Group | Rooms | k | Primitive | G | Proper factor with parity and phi(S) != phi(T) |
| --- | --- | --- | --- | --- | --- |
| Orthogonal k7 pilot + W18 control, square | 31 | 7 | 31 | 29 S_n, 2 A_n | 0 |
| Same rooms, tri | 31 | 7 | 0 | pillow block only | 0 |
| Symmetric screen, W = 21 | 13 | 2 | 13 | S_n | 0 |
| two-global records, W <= 21 | 307 | 2 | 306 | 248 S_n, 58 A_n, 1 other | 0 |
| k5 learned rooms | 17,868 | 5 | 17,858 | 13,123 S_n, 4,735 A_n, 10 other | 0 |

- **The 11 imprimitive 45-degree rooms.** Each has exactly one proper system, with block size 2. Each room has a lattice isometry that swaps S and T (`task5_structure.py`). The factor has phi(S) = phi(T) and no parity property. G is the full S2 wr G^Sigma in 4 rooms and has index 2 in it in 7 rooms.
- **No lit orthogonal room with k <= 6.** The record has no lit orthogonal room with saved coordinates and 1 <= k <= 6. The k <= 6 theorem's rooms are 45-degree rooms.

## Task 4: the saved 10,368-state certificate (`task4_cylinders.py`)

The certificate is the 60-square translation surface M (the four-copy unfolding). Its SHA-256 matches the one in `negative-control-audit.py`.

Horizontal cylinders, counting true zeros only:

| Cylinders | States |
| --- | --- |
| 2 | 2,160 |
| 6 | 4,968 |
| 7 | 1,728 |
| 9 | 576 |
| 10 | 432 |
| 12 | 504 |

- **Marked count.** With S and T lifts also treated as marked points, the counts are 2: 2,160; 6: 4,104; 8: 2,592; 10: 432; 11: 192; 12: 600; 14: 288.
- **One-cylinder states.** There are none. If the saved set is the full SL2(Z) orbit, as the record states, M has no one-cylinder rational direction.
- **Source on a regular leaf.** This happens in exactly 1,728 states, all with square 0. In each of them, all 4 source lifts lie on zero-free horizontal lines. These lines are the middle line of height-2 cylinders: 1,920 with circumference 4 and 864 with circumference 12.
- **Targets in those 1,728 states.**
  - No target lift lies on a source line, on the line between the two strips, or on either boundary line.
  - No target lift lies on any zero-free line in the same state. Every target lift lies on a line that carries a zero.
  - The 6,912 target lifts that do lie on regular lines occur only in other states.
- **Boundary lines.** Each source cylinder's boundary lines carry 1 or 3 zeros. Some also carry convex-corner lifts or other regular vertices. The per-cylinder line labels are in the JSON.

## Task 5: structural observations

These are interpretations, not proofs.

1. **Darkness has two observed forms.**
   - k = 0: G is S_n or A_n, so it's primitive, and N = DP is the parity factor.
   - k = 4 (the 22-wall room): G is imprimitive, and the parity factor is proper.
   
   A usable dichotomy is "lit unless DP or a proper factor has the parity property with phi(S) != phi(T)". Primitivity alone isn't enough.
2. **A transparent point must ramify.** Suppose N has the parity property. A transparent point of DP has angle 2 pi, and its image must be a non-regular B or C point of N. In the pillow framework, that forces ramification e = 2 over an angle-pi point. So k <= R = 2·delta - 2 for a sphere-to-sphere factor of degree delta. The 22-wall room meets this with equality: k = 4 = R, and all ramification sits at the transparent points.
3. **Symmetric rooms are imprimitive without separating the marks.** Room symmetries that swap S and T give proper block systems with phi(S) = phi(T). These are the only proper systems seen in lit 45-degree controls. A theorem must exclude such factors through the phi(S) != phi(T) condition.
4. **G is close to the largest group the blocks allow.** Where G is imprimitive, it is the full wreath product, or has index 2 or 4 in it. For the 22-wall room, the index-2 cut is the sign condition G <= A15.

## Reproduce

Run from this directory:

```
python3 -B task1_room22.py        # under 1 s
python3 -B task2_dark_rooms.py    # about 2 min
python3 -B task3_lit_controls.py  # about 15 min; reads 3 inputs in place
python3 -B task4_cylinders.py     # about 1 s
python3 -B task5_structure.py     # needs task3_lit_controls.json
python3 -B check_orders.py        # Jordan shortcut vs Schreier–Sims, about 5 min
```

## Files

- `monodromy.py`: the library.
- `task1_room22.py` through `task5_structure.py`, each with its `.json` output. Tasks 1–3 also have `.log` files.
- `check_orders.py` and `check_orders.log`.
- `inputs/`: copied record data.
