# Chamber pockets and an infinite lit family of 20-wall rooms

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md)

**Working draft v0.1, November 23, 2026.** Three aligned 3×3 chambers joined by unit corridors of equal length, with chamber spacing D = 3k + 4, form a strictly simple orthogonal lattice room with 20 walls and area 29 + 6k. For every k ≥ 1, every pair of distinct interior lattice points is lit.

Primary author: **Peyton Wang**. Coauthor: Daniel Wang.

The equal-offset pair in the two outer chambers needs at least two horizontal reversals; the manuscript proves that zero or one is impossible. An explicit path climbs into the middle chamber's upper pocket, crosses 2k + 2 side-wall images, reflects once at the roof, and returns one unit to the right on the rightward sheet. The manuscript also proves the pocket lemma (the return map is a phase shift of 2hc modulo 2w) with an exact matching criterion, which lights every aligned 3×3 room with independent corridor lengths. It adds neck phase maps with a lit 3×4 middle-chamber family, and a group-ring coefficient J that is positive exactly when a prescribed sequence of strip transits exists.

The theorems concern lattice endpoints in the stated families. They give no general wall-count bound. The 22-wall dark room R22 lacks the three-chamber decomposition, so its dark pair doesn't conflict with these results. Non-coprime aligned rooms, other chamber shapes, the adjacent-side and same-side two-neck words, and the one-neck word LLLLRRLLLLRR remain open.

Each main result has one independent AI review, and the manuscript includes each review's corrections and stated gaps. External refereeing and formal verification remain outstanding. The review check scripts trace only prescribed rays; their rerun results are in the manuscript's reproduction section. [Provenance](provenance.json) records source and review hashes and delivered artifacts.

## Build

With Tectonic installed, from this directory:

```sh
tectonic manuscript.tex
```

All content, including the TikZ figures, is in the LaTeX source; there are no external figures or data files. Rebuilt PDF timestamps can differ.
