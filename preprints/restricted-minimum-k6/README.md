# A restricted 22-wall minimum and a parity-fold corollary

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md)

Working draft v0.1, November 8, 2026.

A computer-assisted lower bound for canonical45 triangle disks with at most six transparent non-A lattice points, followed by a strict whole-copy fold corollary. The finite support and optical certificate dependencies are explicit. This does not prove a minimum for arbitrary polygons.

Historical novelty is unconfirmed. These arguments have not been externally refereed or formalized in a proof assistant. The manuscript states its analytic and certificate dependencies explicitly.

## Mathematical sources

- [theorem.txt](../../research/illumination-k4-codex/restricted-theorem-note/theorem.txt)
- [certificate-appendix.txt](../../research/illumination-k4-codex/restricted-theorem-note/certificate-appendix.txt)
- [baseline-and-gap.md](../../research/illumination-generalization-2026-11-06/construction/baseline-and-gap.md)
- [fold-wall-bound-scope.md](../../research/illumination-generalization-2026-11-06/review/fold-wall-bound-scope.md)
- [fold-exception-bound-supplement.md](../../research/illumination-generalization-2026-11-06/review/fold-exception-bound-supplement.md)
- [fold-base-incidence-supplement.md](../../research/illumination-generalization-2026-11-06/review/fold-base-incidence-supplement.md)
- [fold-normalization-supplement.md](../../research/illumination-generalization-2026-11-06/review/fold-normalization-supplement.md)
- [fold-normalization-acceptance.json](../../research/illumination-generalization-2026-11-06/review/fold-normalization-acceptance.json)
- [findings.md](../../research/claude-illumination-check/attainment-review/findings.md)

[Provenance](provenance.json) identifies the exact source versions by SHA-256. Source records can retain older status wording; the cited later reviews determine the accepted scope.

## Build

From this directory, run:

```sh
tectonic manuscript.tex
```

The source is self-contained and includes its figures. It requires no external image files or large-data download to build. A rebuild can differ in PDF timestamps. Mathematical certificate dependencies, where applicable, remain separate from typesetting.
