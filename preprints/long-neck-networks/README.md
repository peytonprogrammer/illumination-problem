# Illumination through long rectangular necks

[Read the PDF](manuscript.pdf) · [LaTeX source](manuscript.tex) · [Manuscript catalog](../README.md) · [Explainer video](../../videos/long-neck-illumination/long-neck-illumination.mp4) · [Video source](../../videos/long-neck-illumination/README.md)

Working draft v0.1, November 8, 2026.

Two fixed arbitrary-real orthogonal chambers illuminate each fixed opposing pair for every sufficiently long real neck. A separate conditional theorem propagates one supplied witness on a fixed parallel-neck tree with commensurate widths.

Historical novelty is unconfirmed. These arguments have not been externally refereed or formalized in a proof assistant. The manuscript states its analytic and certificate dependencies explicitly.

## Mathematical sources

- [long-neck-proof.md](../../research/illumination-generalization-2026-11-06/construction/long-neck-proof.md)
- [long-neck-independent.md](../../research/illumination-generalization-2026-11-06/review/long-neck-independent.md)
- [long-neck-independent-acceptance.json](../../research/illumination-generalization-2026-11-06/review/long-neck-independent-acceptance.json)
- [neck-ray-propagation-parallel-tree.md](../../research/illumination-generalization-2026-11-06/construction/neck-ray-propagation-parallel-tree.md)
- [neck-ray-propagation-commensurate.md](../../research/illumination-generalization-2026-11-06/construction/neck-ray-propagation-commensurate.md)
- [parallel-tree-independent.md](../../research/illumination-generalization-2026-11-06/review/parallel-tree-independent.md)
- [parallel-tree-independent-acceptance.json](../../research/illumination-generalization-2026-11-06/review/parallel-tree-independent-acceptance.json)

[Provenance](provenance.json) identifies the exact source versions by SHA-256. Source records can retain older status wording; the cited later reviews determine the accepted scope.

## Build

From this directory, run:

```sh
tectonic manuscript.tex
```

The source is self-contained and includes its figures. It requires no external image files or large-data download to build. A rebuild can differ in PDF timestamps. Mathematical certificate dependencies, where applicable, remain separate from typesetting.
