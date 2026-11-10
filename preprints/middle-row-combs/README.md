# Illumination in rectangular-spine combs

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md) · [Explainer video](../../videos/comb-illumination/comb-illumination.mp4) · [Video source](../../videos/comb-illumination/README.md)

Working draft v0.1, November 8, 2026.

An elementary finite floor-matching proof for arbitrary real spine and tooth dimensions, with no wall-count bound. Every spine/middle-row pair is covered. The lattice corollary covers all interior even-even pairs when every tooth has integer coordinates and height two.

These arguments have not been externally refereed or formalized in a proof assistant. The manuscript states its analytic and certificate dependencies explicitly.

## Mathematical sources

- [midheight-comb-proof.md](../../research/illumination-generalization-2026-11-06/construction/midheight-comb-proof.md)
- [midheight-comb-independent.md](../../research/illumination-generalization-2026-11-06/review/midheight-comb-independent.md)
- [midheight-comb-independent-acceptance.json](../../research/illumination-generalization-2026-11-06/review/midheight-comb-independent-acceptance.json)

[Provenance](provenance.json) identifies the exact source versions by SHA-256. Source records can retain older status wording; the cited later reviews determine the accepted scope.

## Build

From this directory, run:

```sh
tectonic manuscript.tex
```

The source is self-contained and includes its figures. It requires no external image files or large-data download to build. A rebuild can differ in PDF timestamps. Mathematical certificate dependencies, where applicable, remain separate from typesetting.
