# Twenty-two walls is exact for rooms with a corner-only parity class

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md)

**Working draft v0.1, November 23, 2026.** In a strictly simple orthogonal lattice room where one parity class contains only corners, a dark pair of distinct interior lattice points needs at least 22 walls. The known 22-wall room attains the bound. At 15 cells the same bound holds for every pair of distinct real interior points.

Primary author: **Peyton Wang**. Coauthor: Daniel Wang.

A counting identity bounds the area of every such room below 22 walls by 36. That reduces the lattice statement to a finite computation: 780,565 rooms and 3,933,192 pairs, same-class and different-class, all lit. Two exact tracers that share no code with the search replay every witness. The area-15 result uses exact cylinder certificates over 77,725 rooms. An independent reimplementation confirms the six hardest rooms.

Both results are computer-assisted. Enumeration completeness is checked by reading the code. Each step has independent AI review; no human referee has read it, and nothing is formally verified. The results don't cover rooms in which every parity class has an interior or smooth wall point, non-lattice marks above 15 cells, real side lengths, or 45-degree walls.

The repository's research mirror holds the programs, logs and room files this manuscript cites. It lacks the three compressed witness files (15.9 MB), so the d102 full replay needs the full research tree. [Provenance](provenance.json) records their SHA-256 digests.

## Build

With Tectonic installed, from this directory:

```sh
tectonic manuscript.tex
```

All content is included in the LaTeX source; there are no external figures or data files. Rebuilt PDF timestamps can differ.
