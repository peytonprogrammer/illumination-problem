# Illumination problem: research archive

A research snapshot containing positive results, failed proof approaches, counterexamples to specific mechanisms, independent review records, exact checkers, and supporting certificate data.

**The universal minimum-wall problem is not solved here. Historical novelty is unconfirmed.** Internal AI acceptance, exact computational checks, and external mathematical refereeing are different verification levels.

## Start here

- [Manuscripts and research notes](preprints/README.md): four theorem manuscripts, historical notes, PDFs and LaTeX sources.
- [Results inventory](RESULTS.md): grouped statements, assumptions, limitations, and priority assessment.
- [Negative findings](docs/NEGATIVE-RESULTS.md): counterexamples and limits of failed proof approaches.
- [Machine-readable result index](manifests/results.json): stable grouped-result IDs.
- [Verification and reproduction](docs/REPRODUCIBILITY.md): what was checked and how to inspect the data.
- [Snapshot and exclusions](docs/SNAPSHOT.md): coverage and archival limitations.
- [Research sources](research/): proofs, failed attempts, scripts, diagrams, review receipts, and smaller evidence files.
- [Case-package manifest](manifests/packages.json): independent large-evidence downloads with sizes and hashes.
- [Current file locations](docs/REPRODUCIBILITY.md): how the historical and dated manifests combine to describe current file locations and hashes.

## Latest reviewed update

[Eight-wall theorem: PDF manuscript](preprints/eight-wall/manuscript.pdf) · [Source and build instructions](preprints/eight-wall/README.md). Full corrected proof, normal forms, example paths and review checklist; working draft for external review.

[Corrected eight-wall proof and affine results](docs/UPDATE-2026-11-08.md): self-contained proof packet, figures, later positive mechanisms, failed reductions and independent reviews. Research is paused; the proposed whole-affine-group bound remains unproved and unrefuted.

[Browse evidence by theorem or case](docs/DATA.md). Small supporting files are now ordinary Git files. Large evidence is split into independent downloads.

## Main established results

| Result | Scope |
|---|---|
| Sharp restricted 22-wall minimum | Canonical45 lattice rooms with at most six transparent non-A exceptions; computer-assisted |
| Complete illumination through eight walls | All strictly simple orthogonal rooms, all real dimensions and distinct interior endpoints |
| Twelve-wall corridor theorem | The specified four-parameter family; every lower-to-upper outer-chamber pair; computer-assisted |
| One-sided comb illumination | Spine/middle-row pairs, arbitrary real teeth and no wall-count cap |
| Complete two-sided comb subclasses | Exact lattice families through 21 walls, without area/support/exception caps |
| Long-neck and network results | Eventual illumination in fixed-chamber families; network propagation has explicit witness/commensurability assumptions |
| Strict-fold class minimum | At least 22 walls for darkness within the precisely defined whole-copy construction class |
| Tall or wide ten-wall spirals | All interior pairs under explicit sufficient thresholds; upper-cap-to-bottom extension at all metrics |

Each statement retains the hypotheses in its source. Eight walls means two reflex corners; the current eight-reflex target allows twenty walls. A canonical45 “triangle room” is built from triangular tiles and need not have a triangular outline.

The 22-wall dark construction is recorded as a likely independent rediscovery. Published work already contains a 22-edge upper bound. No “first”, general minimality, or P-versus-NP/ETH consequence is claimed.

## Supporting data and reproduction

Small proofs, checkers, reviews, diagrams and generated evidence are directly browseable under `research/`. [The data browser](docs/DATA.md) links large theorem/case packages. Each package is independently compressed and has readable historical member paths and SHA-256 checksums. You no longer need the whole historical stream for one result.

```sh
python3 tools/archive.py verify-git
python3 tools/reproduce.py eight-wall
python3 tools/reproduce.py affine
python3 tools/archive.py list-data --prefix illumination-k4-codex/symbolic-corridors/
```

See [verification and reproduction](docs/REPRODUCIBILITY.md) for selective download/restoration, dependencies and verification limits. No archived program runs automatically.
