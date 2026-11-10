# Illumination problem

Proofs, working manuscripts, counterexamples to proof mechanisms, and computational evidence for polygonal illumination.

The universal minimum-wall problem remains open. The results have internal AI reviews and exact computational checks at the scopes recorded in their sources. Historical novelty and external mathematical refereeing remain unconfirmed.

## Read the results

| To… | Start with… |
|---|---|
| Read a manuscript | [Eight theorem manuscripts, an affine research note and two supporting notes](preprints/README.md) |
| Watch an explainer | [Three narrated videos with editable HyperFrames source](videos/README.md) |
| Find a precise statement, hypotheses, and proof | [Results inventory](RESULTS.md) |
| Understand failed approaches and open questions | [Negative findings](docs/NEGATIVE-RESULTS.md) |
| Inspect or download supporting evidence | [Data catalog](docs/DATA.md) |
| Verify files or run prescribed controls | [Reproduction guide](docs/REPRODUCIBILITY.md) |

The manuscript catalog distinguishes the explicit 22-wall construction from the restricted minimum theorem. The construction alone does not establish universal minimality.

## Repository layout

```text
preprints/       Readable PDFs, LaTeX sources, figures, and build instructions
videos/          Narrated MP4s, editable HyperFrames projects, and transcripts
research/        Archived proofs, reviews, scripts, and small evidence files
manifests/       Current file locations, hashes, package metadata, and result IDs
docs/            Reading guides, reference catalogs, and dated research notes
tools/           Verification, selective restoration, and catalog maintenance
```

[Documentation](docs/README.md) contains the reading guide, reproduction instructions, data catalog, and dated research notes. [Tools](tools/README.md) verify files, restore selected evidence, and run prescribed controls. [Snapshot scope](docs/SNAPSHOT.md) explains provenance and verification limits.

Research paths retain their original names so source references and restored script dependencies remain usable. Use the curated catalogs to navigate the archive.

## Selected established results

- Every strictly simple orthogonal room with at most eight maximal walls illuminates every pair of distinct real interior points.
- The specified four-parameter twelve-wall corridor family illuminates every lower-to-upper outer-chamber pair.
- The canonical45 lattice model with at most six transparent non-A exceptions has a sharp restricted 22-wall minimum.
- Comb, long-neck, strict-fold, and restricted ten-wall spiral results hold under the hypotheses in the [full inventory](RESULTS.md).

Eight walls means two reflex corners. A bound of eight reflex corners permits twenty walls. A canonical45 room is assembled from triangular tiles and need not have a triangular outline.

## Verify a checkout

From the repository root, with the [validation dependencies](docs/REPRODUCIBILITY.md#dependencies):

```sh
python3 tools/validate.py
```

These controls need no large-data download. See the [reproduction guide](docs/REPRODUCIBILITY.md) for dependencies, selective downloads, and restoration. See [contributing](CONTRIBUTING.md) for changes to the research record.

## AI assistance

OpenAI Codex and Anthropic Claude were used to develop, review, and update the research, theorem proofs, and manuscripts in this archive. The authors remain responsible for the content.
