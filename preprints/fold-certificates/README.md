# No fold certificate of darkness below 21 walls in orthogonal lattice rooms

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md)

**Working draft v0.1, November 23, 2026.** No strictly simple orthogonal lattice room with at most 20 walls has a rational interior pair certified dark by a Par, Cut, or Rig certificate over any pillowcase base.

Primary author: **Peyton Wang**. Coauthor: Daniel Wang.

The result is computer-assisted. Lemmas on pillowcase bases reduce every base to the unit pillowcase or to two finite residues. A filter on area and reflex classes then leaves a finite room enumeration. The checks cover about 14.4 billion rooms and at least 59.4 billion pairs, with 0 certified pairs. A second proof of the core case enumerates fold quotients and their covers instead of rooms. The known 22-wall dark room is the positive control: the pipeline certifies its dark pair. The manuscript also states the fold-converse lemma and a separate result that an R22-type parity fold needs at least 9 reflex corners.

The theorem covers certificates only. It doesn't show that every pair is lit: a pair with no certificate can still be dark, and the realization lemma that would close this gap is open. Irrational pairs, boundary marks, other darkness mechanisms, and rooms with 45-degree walls are outside the statement.

Each theory input has one independent AI referee and no human referee, and the referees' repairs are not reviewed again. The programs are not formally verified, and the full 20-wall room check has one implementation. Section 9 of the manuscript lists the limitations and the discrepancies between sources. [Provenance](provenance.json) records source hashes, reruns, and delivered artifacts.

## Build

With Tectonic installed, from this directory:

```sh
tectonic manuscript.tex
```

All content is included in the LaTeX source; there are no external figures or data files. The cited research files live under `research/` in this repository, and Section 10 of the manuscript gives the commands that reproduce the computations. Rebuilt PDF timestamps can differ.
