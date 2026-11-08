# Reproduce the checks and figures

All commands run in a few seconds on a machine with Python 3 (tested with
3.15) and no third-party packages. The proof-check runner copies its inputs into a scratch directory first.
The figure and manifest commands execute the packet scripts and rewrite their
respective outputs inside the packet, as described below.

## 1. Prescribed exact checks of the proof chain

```
sh <SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/fable/eight-wall-review-packet/reproduce.sh
```

The script copies 12 check scripts and the source files they hash into a
fresh `mktemp` directory, then runs each with `python3 -I`. Expected: every
script prints a JSON summary with a `PASS`-type status and the last line is
`ALL CHECKS EXITED 0`. The runner checks each Python exit code directly and
stops on failure; output truncation occurs only after a successful check. Run time on 2026-11-08 was 2.3 seconds. The checks and
what they verify:

| Script | Proof part | What it computes |
| --- | --- | --- |
| `review/eight-wall-turn-check.py` | Prop 1.2 | 28 labeled reflex positions fall into the four k classes; one simple representative per class |
| `single-boundary-blocker/arithmetic-check.py` | Thm 2.1 | Vertical-only and horizontal-only L formula on 486 fixed pairs in 6 rooms; 7,132 wall contacts checked |
| `two-reflex-blocker/all-heights-check.py` | Thm 3.1 | Fixed-point construction on 6 fixed U inputs; every wall contact checked |
| `construction/T-whole-check.py`, `review/uneven-T-check.py` | Thm 4.1 | Fixed opposite-wing witness with 17 reflections in a u < v room |
| `review/wide-middle-constructor-check.py`, `review/wide-middle-boundary-controls.py` | Thm 5.1, 5.2 | Three-piece constructor on 4 fixtures; rotation and seam-endpoint controls |
| `review/staircase-window-check.py` | Lemma 6.2 | Nested-window constructor on 4 fixtures |
| `review/staircase-roof-check.py` | Lemma 6.3, Thm 6.8 Steps 2 to 3 | Partial-window roof constructor on 4 fixtures |
| `review/staircase-floor-check.py` | Thm 6.5 | Reflected-source constructor on 6 fixtures, including one where the first image hits a floor corner |
| `review/staircase-overlap-check.py` | not needed by the final chain | One fixed witness |
| `review/whole-staircase-check.py` | Prop 6.10, Thm 6.8 Step 4 | Symbolic polynomial identities (6.4) and both factorizations; 625 metric controls of "F or Ft or Rv or Rh"; three roof-corner earlier-arrival controls |

Two older scripts, `construction/staircase-window-check.py` and
`construction/staircase-roof-check.py`, exit immediately because their
original effort clocks have expired. The `review/` scripts in the table cover
the same constructions and are the ones used here.

All of these evaluate fixed inputs. They do not search for directions and do
not prove the arbitrary-real statements.

## 2. Figures and independently verified example paths

```
python3 -I <SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/fable/eight-wall-review-packet/figures/make_figures.py
```

This rewrites the seven SVG files in `figures/` and `figures/paths.json`.
The script implements the constructions of Theorems 2.1, 3.1, 4.1, 5.1, 6.5,
and 6.8 in exact rational arithmetic and then checks each resulting path with
its own verifier: endpoints strictly interior, every contact on exactly one
wall and not at a corner, the reflection law at every contact, and every
open segment disjoint from the boundary. It prints a summary with the
reflection count and number of checks per path. The roof figure contains two
paths from the same pair: the lowest admissible image (one roof contact) and
the image whose roof coordinate is a multiple of a, which exercises the
earlier-arrival truncation of Theorem 6.8 Step 4. Open the SVG files in any
browser.

## 3. Dependency manifest

```
python3 -I <SOURCE_WORKSPACE>/.context/illumination-generalization-2026-11-06/fable/eight-wall-review-packet/make_manifest.py
```

Recomputes SHA-256 for the 34 source files of the chain, compares each with
the hash pinned in its acceptance file, and rewrites
`dependency-manifest.json`. Expected output includes `"mismatched_pins": 0`.
