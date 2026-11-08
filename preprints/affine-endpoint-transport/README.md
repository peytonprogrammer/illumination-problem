# Affine transport of endpoints in L-shaped billiards

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md)

Working draft v0.1, November 8, 2026.

A research note on exact transport of both endpoints, an explicit uniform-source shear criterion, and its arithmetic limits. It proves a useful mechanism, not new L-room illumination coverage or a general affine compression theorem.

Historical novelty is unconfirmed. These arguments have not been externally refereed or formalized in a proof assistant. The manuscript states its analytic and certificate dependencies explicitly.

## Mathematical sources

- [pair-transport.md](../../research/illumination-generalization-2026-11-06/coordination/general-proof-priority/affine-seed-reduction/pair-transport.md)
- [noncompressible-connection.md](../../research/illumination-generalization-2026-11-06/coordination/general-proof-priority/target-fiber-peer-goals/reviewer/noncompressible-connection.md)
- [noncompression-reconciliation.json](../../research/illumination-generalization-2026-11-06/coordination/general-proof-priority/target-fiber-peer-goals/reviewer/noncompression-reconciliation.json)
- [manuscript.tex](../../preprints/eight-wall/manuscript.tex)

[Provenance](provenance.json) identifies the exact source versions by SHA-256. Source records can retain older status wording; the cited later reviews determine the accepted scope.

## Build

From this directory, run:

```sh
tectonic manuscript.tex
```

The source is self-contained and includes its figures. It requires no external image files or large-data download to build. A rebuild can differ in PDF timestamps. Mathematical certificate dependencies, where applicable, remain separate from typesetting.
