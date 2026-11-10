# Eight-wall illumination manuscript

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md) · [Explainer video](../../videos/eight-wall-illumination/eight-wall-illumination.mp4) · [Video source](../../videos/eight-wall-illumination/README.md)

**Working draft v0.1, November 8, 2026.** Every finite strictly simple orthogonal polygon with at most eight maximal walls illuminates every pair of distinct interior points by a finite specular path avoiding all corners. Dimensions and endpoints are arbitrary real numbers. Eight walls means at most two reflex corners.

The manuscript contains the full corrected proof, the six normal forms, four prescribed path illustrations, a referee checklist and reproduction instructions. It has no lattice or rationality assumption. It makes no claim about the universal 22-wall minimum or historical novelty.

The proof was developed and cross-reviewed with AI agents. It has not been externally refereed or checked in a proof assistant. This is a manuscript for mathematical review, not a journal or arXiv submission.

## Proof source and figures

Sections 0–8 typeset the complete [corrected proof packet](../../research/illumination-generalization-2026-11-06/fable/eight-wall-review-packet/theorem-and-proof.md), retaining its proof and theorem numbering. `build.py` checks that packet's SHA-256 before generating the LaTeX. Mathematical variables in ASCII notation are translated into print notation; in particular, the packet's `Beta` is printed as capital B in its local roof argument. The original mathematical source remains unchanged.

The normal-form figure uses the original coordinates and marks reflex corners with black dots. Four example illustrations preserve the original geometry and paths, replacing embedded headings and overlapping legends with captions. Exact fixtures remain in the packet's `figures/paths.json`.

[Provenance](provenance.json) records the source path and pinned SHA-256. [Verification](verification.json) records the manuscript delivery checks. The [coordinator review](../../research/illumination-generalization-2026-11-06/coordination/general-proof-priority/final-review/eight-wall-review.md) describes the corrections and mathematical review limits.

## Build

The generated `manuscript.tex` and the four figure PDFs are included. With Tectonic installed, build directly:

```sh
cd preprints/eight-wall
tectonic manuscript.tex
```

Alternatively, use a current LaTeX installation with XeLaTeX and the packages listed in the source. To regenerate the TeX and figure PDFs from the pinned research packet, install PyMuPDF and run from the repository root:

```sh
python3 preprints/eight-wall/build.py
```

PyMuPDF is needed only for regeneration; the included TeX and figure PDFs build without Python. The recorded build used Tectonic 0.17.0. LaTeX engines can embed different creation timestamps, so a rebuilt PDF need not have the same file hash.

## Check the prescribed controls

From the repository root:

```sh
python3 tools/reproduce.py eight-wall
```

This executes twelve prescribed checks in a disposable workspace and needs no large-data download. These fixed controls support inspection of the constructions; they do not replace the analytic proof or establish its arbitrary-real quantifiers.
