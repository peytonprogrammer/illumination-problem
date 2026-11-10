# A 22-wall room with exactly one dark pair

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Illustrated companion](explainer.html) · [Manuscript catalog](../README.md) · [Construction video](../../videos/dark-room-22/dark-room-22.mp4)

**Working draft v0.5, November 10, 2026.** Among all unordered pairs of distinct real interior points in this strictly simple orthogonal room, the only dark pair is `{(0,0), (2,2)}`.

Primary author: **Peyton Wang**. Coauthor: Daniel Wang.

The manuscript contains the staircase construction and folded-parity darkness proof, followed by the full cylinder argument for every other pair. A strip diagram explains why an interior source lift can reach any regular target in a cylinder's closure. Two finite permutations, in directions `(4,7)` and `(7,4)`, certify the cylinder decompositions. The four integrality conditions leave only interior lattice points as possible dark-pair endpoints.

The [illustrated companion](explainer.html) lets you move the source and target, inspect the integrality conditions, and move a target onto the boundary of a covering strip. Open the HTML file locally in any modern browser; it needs no server or network connection. The existing construction video explains the construction and darkness proof; the cylinder classification is covered by the manuscript and companion.

The argument has independent AI review and fixed-certificate checks. It has not been formally verified or externally refereed. Its scope is distinct interior pairs in this polygon; boundary endpoints and self-return trajectories are excluded.

## Reproduce the finite inputs

From this directory, with standard-library Python 3:

```sh
python3 verify_cylinders.py --check
```

The checker rebuilds the room and the right/up neighbour permutations, lists every strip-permutation cycle, and compares the result with [certificate.json](certificate.json). The cycle lengths are `210 + 210` for `(4,7)` and `120 + 120` for `(7,4)`. The manuscript also prints the equivalent first-return certificates on 60 squares: two 30-cycles in each direction. The checker regenerates these reduced permutations too. It also checks that the only interior lattice points are `(0,0)` and `(2,2)`.

To print a regenerated certificate:

```sh
python3 verify_cylinders.py
```

These finite checks supply the cylinder inputs to the analytic proof; they do not approximate its real-coordinate quantifiers by a sampled grid.

## Build

With Tectonic installed:

```sh
tectonic manuscript.tex
```

All figures are included as TikZ source. [Provenance](provenance.json) records the source versions and delivered artifact hashes. Rebuilt PDF timestamps can differ.
