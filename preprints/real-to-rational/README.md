# Rational pairs suffice for orthogonal lattice rooms

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md)

**Working draft v0.1, November 10, 2026.** In a fixed strictly simple orthogonal polygon with integer vertices, if every distinct rational interior pair illuminates, then every distinct real interior pair illuminates.

Primary author: **Peyton Wang**. Coauthor: Daniel Wang.

The proof is elementary: unfold into four copies, construct horizontal and vertical multi-twists, prove density for generic pairs, and analyze the remaining rational relation surfaces. A dark pair with an irrational coordinate slides in a local family containing rational dark pairs arbitrarily nearby. The manuscript includes the finite-power repairs from the source's independent AI review.

The theorem gives no denominator bound, finite direction list, or wall-count minimum. An area-bounded lattice census does not become an all-real theorem, because the required integer dilation can leave the census range. Boundary pairs and self-return trajectories are outside the statement.

The proof needs no program, numerical test, or certificate download. The source argument has independent AI mathematical review; external refereeing and formal verification remain outstanding. [Provenance](provenance.json) records source/review hashes and delivered artifacts.

## Build

With Tectonic installed, from this directory:

```sh
tectonic manuscript.tex
```

All content is included in the LaTeX source; there are no external figures or data files. Rebuilt PDF timestamps can differ.
