# d98: independent check of d64 `enum_K.c` at z = 4

Date: 2026-11-20. Review queue item Q04. Brief: cross-check d64's quotient list at `z = 4`,
`delta = 2`, with a different algorithm. No scope extension and no room search.

## Verdict: MATCH (d = 1 to 18)

My enumerator and `enum_K.c` produce the **same set of shapes**, not only the same counts. I
compared canonical forms one by one. At `z = 4`, both lists have 3,743 genus-0 shapes
and 3,663 admissible `(K, delta = 2)` cases. Neither list has an object the other lacks.
The match also covers `d = 18`, the step 5 bound. That degree has 6 genus-0 shapes and no
admissible shape.

| d | Genus 0 (d98) | Genus 0 (enum_K) | Admissible (d98) | Admissible (enum_K) |
| --- | --- | --- | --- | --- |
| 5 | 1 | 1 | 1 | 1 |
| 6 | 42 | 42 | 42 | 42 |
| 7 | 191 | 191 | 191 | 191 |
| 8 | 423 | 423 | 423 | 423 |
| 9 | 600 | 600 | 600 | 600 |
| 10 | 716 | 716 | 714 | 714 |
| 11 | 633 | 633 | 633 | 633 |
| 12 | 493 | 493 | 483 | 483 |
| 13 | 321 | 321 | 321 | 321 |
| 14 | 187 | 187 | 149 | 149 |
| 15 | 78 | 78 | 78 | 78 |
| 16 | 46 | 46 | 22 | 22 |
| 17 | 6 | 6 | 6 | 6 |
| 18 | 6 | 6 | 0 | 0 |
| **Total** | **3,743** | **3,743** | **3,663** | **3,663** |

The admissible column equals d64 `logs/shapes.log` at `z = 4`, row by row. Degrees 1 to 4
have no `z = 4` shape in either list. As a control, `z = 0, 1, 2` with `d <= 12` match set
for set: 6, 15, and 106 shapes. `z = 3` with `d <= 14` matched in a slower first version of
this code, with 549 shapes.

## 1. What's enumerated at z = 4 (from d64 README section 2, with d52 for the types)

A case is a transitive W-set `K` on `d` cells. Here `W` is the free product of four
involutions `V0, V1, H0, H1`, and a fixed point is a wall. Two W-sets are the same case when
a relabelling of cells maps one to the other. Each case must meet these conditions:

- For each class `(i, j)`, every `<V_i, H_j>`-orbit is cvx (path of 1), smooth (path of 2),
  rfx (path of 3), cone (2-cycle), or int (4-cycle). The README cites d52 C9 for these
  types. The definitions come from the d52 `fold.py` docstring.
- Class `x = (0, 0)` has only cvx, rfx, and cone orbits.
- `z`, the number of rfx orbits over all four classes, is 4. There's at most one cone, also
  over all classes. Genus 0 means `cvx + 2 cone - z = 4`, so `cvx + 2 cone = 8`.
- Admissible means at least 3 singular classes and some `delta >= 2` with `delta z <= 8`,
  where `delta` is even if a cone exists. At `z = 4` the only value is `delta = 2`, so the
  cases are the admissible shapes.
- `d <= 18` comes from step 5.

**Ambiguities and observations.**

1. **"Singular class."** `shapes.py` counts a class as singular when it has a cvx, rfx, or
   cone orbit. Step 4's argument uses corners only. Corners map to wall fixed points, so
   they map to cvx or rfx and never to a cone. Under the corner-only reading, 68 of the
   3,663 `z = 4` cases drop out: 12 at `d = 10`, 24 at `d = 12`, 24 at `d = 14`, and 8 at
   `d = 16`. d64's list is therefore a superset of the strict reading. This is harmless for
   completeness (`logs/strict_sing.log`).
2. **Equivalence.** Cases are counted up to relabelling only, not up to the symmetries of the
   square that fix class `(0, 0)`, such as swapping `V` and `H`. Mirror images count twice.
   This is also a harmless superset.
3. **"At most one cone"** applies to all classes, not only to class `x`. The README cites C4
   without saying so. Both codes read it this way.

## 2. Method (different from enum_K.c)

`enum_K.c` grows a W-set from one cell. It adds cells in first-encounter order and
dedupes with a BFS canonical form. `skel.c` works differently:

- **Fixed d and skeleton first.** Class `(0, 0)` has only cvx, rfx, and cone orbits. So `V0`
  and `H0` are fixed up to relabelling by the counts `(a, b, c)` with `a + 3b + 2c = d`,
  `b <= 4`, `c <= 1`, and `a + 2c <= 8`. Each skeleton is laid out explicitly.
- **Fill V1, then H1.** The code backtracks over `V1` and `H1` on the fixed `d` cells. It
  checks classes `(1, 0)`, `(0, 1)`, and `(1, 1)` on partial orbits, keeps rfx, cone, and
  cvx counts incrementally, and prunes a closed component that misses some cell.
- **Symmetry breaking.** Untouched cvx cells and untouched rfx triples are interchangeable.
  The code links only to the first untouched one of each kind.
- **Dedupe with a different canonical form.** The form is the minimum over start cells of a
  recursive DFS labelling, with generator order `V1, H1, V0, H0`.
- **Object-level comparison.** `./skel canon` reads `enum_K.c`'s output and recomputes `z`,
  the cone count, and the singular classes with this code. It writes each W-set in the DFS
  canonical form. `cmp.py` then compares the two sets.

I shared no code with d52 or d64. I read `enum_K.c` only for its output row order
(`V0, V1, H0, H1`).

## 3. Re-run

```
cd d98-check-enumK
cc -O2 -o skel skel.c
./skel enum 4 1 18 > data/skel_z4_all.txt          # about 440 CPU-s; d = 18 alone is 390 s
./skel canon < ../d64-finite-case/data/K_z4_d18.txt > data/enumK_recanon.txt
python3 -B cmp.py data/skel_z4_all.txt data/enumK_recanon.txt 4 18
python3 -B strict_sing.py data/skel_z4_all.txt
```

## Files

| File | Role |
| --- | --- |
| `skel.c` | Independent enumerator (`enum`) and re-canonicalizer (`canon`) |
| `cmp.py` | Set comparison and per-`d` table |
| `strict_sing.py` | Count of cases that depend on the cone being counted as singular |
| `data/skel_z4_*.txt` | d98 shapes in the format `d z cone sing \| DFS form` |
| `data/skel_z{0,1,2}_d1_12.txt` | Control runs |
| `data/enumK_recanon.txt` | d64's 4,420 shapes in d98 canonical form |
| `logs/` | Run logs (node counts and times), comparisons |

## CPU

About 9.5 CPU-minutes in total:

- Final runs: 0.7 s for `d <= 12`, 47 s for `d = 13..16`, and 391 s for `d = 17..18`.
- A first version without symmetry breaking: about 2 to 3 minutes, stopped during `z = 3`.
- Controls: a few seconds.

Nothing was written outside this directory.
