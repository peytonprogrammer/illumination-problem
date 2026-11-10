# Illumination in tall and coprime-period ten-wall spirals

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md) · [Explainer video](../../videos/ten-wall-spirals/ten-wall-spirals.mp4) · [Video source](../../videos/ten-wall-spirals/README.md)

Working draft v0.1, November 8, 2026.

Sufficient tall-or-wide conditions cover all real interior pairs in a stated spiral normal form. A separate arithmetic construction covers all native even-even pairs in an infinite thin-cap family, including metrics outside those thresholds. Neither result covers every ten-wall polygon.

These arguments have not been externally refereed or formalized in a proof assistant. The manuscript states its analytic and certificate dependencies explicitly.

## Mathematical sources

- [three-reflex-argument-01.md](../../research/illumination-generalization-2026-11-06/construction/three-reflex-argument-01.md)
- [three-reflex-argument-03.md](../../research/illumination-generalization-2026-11-06/construction/three-reflex-argument-03.md)
- [three-reflex-argument-04.md](../../research/illumination-generalization-2026-11-06/construction/three-reflex-argument-04.md)
- [three-reflex-tr04-independent.md](../../research/illumination-generalization-2026-11-06/review/three-reflex-tr04-independent.md)
- [three-reflex-tr04-independent.json](../../research/illumination-generalization-2026-11-06/review/three-reflex-tr04-independent.json)
- [coprime-candidate.md](../../research/codex-proof-verification/specialist-ideas/terminal-resumption-2026-11-07/coprime-candidate.md)
- [coprime-proof.md](../../research/codex-proof-verification/specialist-ideas/terminal-resumption-2026-11-07/coprime-proof.md)
- [three-reflex-coprime-independent.md](../../research/illumination-generalization-2026-11-06/review/three-reflex-coprime-independent.md)
- [three-reflex-coprime-independent.json](../../research/illumination-generalization-2026-11-06/review/three-reflex-coprime-independent.json)

[Provenance](provenance.json) identifies the exact source versions by SHA-256. Source records can retain older status wording; the cited later reviews determine the accepted scope.

## Build

From this directory, run:

```sh
tectonic manuscript.tex
```

The source is self-contained and includes its figures. It requires no external image files or large-data download to build. A rebuild can differ in PDF timestamps. Mathematical certificate dependencies, where applicable, remain separate from typesetting.
