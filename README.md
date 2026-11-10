# Illumination problem

The polygonal illumination problem asks which pairs of points in a mirrored room can be connected by a reflected light ray that avoids corners. This repository contains our proofs, working manuscripts, verification code, computational evidence, and animated explainers.

The universal minimum-wall problem remains open. The results have internal AI reviews and exact computational checks at the scopes recorded in their sources. External mathematical refereeing remains outstanding.

## Read the results

| To… | Start with… |
|---|---|
| Read a manuscript | [Nine theorem manuscripts, an affine research note and two supporting notes](preprints/README.md) |
| Watch an explainer | [Narrated videos with editable HyperFrames source](videos/README.md) |
| Find a precise statement, hypotheses, and proof | [Results inventory](RESULTS.md) |
| Understand failed approaches and open questions | [Negative findings](docs/NEGATIVE-RESULTS.md) |
| Inspect or download supporting evidence | [Data catalog](docs/DATA.md) |
| Verify files or run prescribed controls | [Reproduction guide](docs/REPRODUCIBILITY.md) |

## Theorems and manuscripts

The [full inventory](RESULTS.md) groups 29 results, including supporting lemmas, conditional mechanisms, and counterexamples to proposed proof methods. The main theorem manuscripts are:

| Result | What it establishes |
|---|---|
| [22-wall room](preprints/twenty-two-wall/README.md) | The specified simple orthogonal room has exactly one dark pair among all distinct real interior pairs: `{(0,0), (2,2)}`. |
| [Eight-wall illumination](preprints/eight-wall/README.md) | Every distinct interior pair illuminates in every simple orthogonal room with at most eight walls, for arbitrary real dimensions. |
| [Rational-to-real reduction](preprints/real-to-rational/README.md) | In a fixed orthogonal lattice room, illumination of every distinct rational interior pair implies illumination of every distinct real interior pair. |
| [Restricted minimum and parity folds](preprints/restricted-minimum-k6/README.md) | A sharp 22-wall minimum for the canonical45 model with at most six transparent non-A lattice points and interior A endpoints; a related minimum in the stated whole-copy fold class. |
| [Three-star illumination](preprints/three-star-surplus-four/README.md) | At the fixed three-star support, the surplus-four class illuminates within 32 reflections under its wall and transparency bounds. |
| [Twelve-wall corridor](preprints/twelve-wall-corridor/README.md) | Every opposing outer-chamber pair illuminates in the specified four-parameter family, with arbitrary positive real dimensions. |
| [Rectangular-spine combs](preprints/middle-row-combs/README.md) | Spine and tooth-middle-row pairs illuminate with arbitrarily many one-sided teeth and arbitrary real dimensions. |
| [Long necks and networks](preprints/long-neck-networks/README.md) | Fixed opposing-chamber pairs illuminate across sufficiently long necks; conditional propagation results extend to specified networks. |
| [Ten-wall spirals](preprints/ten-wall-spirals/README.md) | All-real illumination under tall-or-wide conditions, plus a separate integer coprime-period family. |

The inventory also covers [two-sided comb subclasses](RESULTS.md#r05), [nested staircases](RESULTS.md#r08), and [affine endpoint transport](preprints/affine-endpoint-transport/README.md). Each statement retains its geometric and endpoint hypotheses. The rational-to-real reduction gives no bound on denominators and does not turn a finite-area census into an all-real theorem.

Eight walls means two reflex corners. A bound of eight reflex corners permits twenty walls. A canonical45 room is assembled from 45–45–90 triangular tiles; its outline need not be triangular. In that model, A points have even-even coordinates, and transparent non-A lattice points are non-A points in the interior or on smooth walls.

## Datasets and proof certificates

The archived research snapshot indexes **140,728 source files**: **134,654 files in Git** and **6,074 larger files in 246 downloadable case packages**, totaling **7.17 GB compressed**. These counts describe the archived research, separately from the curated manuscripts and videos. The [data catalog](docs/DATA.md) lists downloads by theorem and case; the [file manifest](manifests/README.md) records locations, sizes, and SHA-256 hashes.

| Evidence | What is available | Start here |
|---|---|---|
| 22-wall cylinder certificates | Explicit finite permutations in directions `(4,7)` and `(7,4)`, their full cycles, and shorter 30-cycle return certificates. A standalone Python checker regenerates them. | [Certificate JSON](preprints/twenty-two-wall/certificate.json), [checker](preprints/twenty-two-wall/verify_cylinders.py) |
| Restricted-minimum proof corpus | SAT formulas and 64 checked DRAT contradiction certificates. A DRAT certificate lets a checker verify that the encoded candidate case has no solution. | [Certificate map](research/illumination-k4-codex/restricted-theorem-note/certificate-appendix.txt), [case downloads](docs/DATA.md) |
| Exact optical guards and clause witnesses | 193,480 saved guard records across 52 files in the restricted-minimum packet, with provenance for 875,332 added optical clauses. Guards specify exact reflected paths and the required/forbidden tiles under which those paths remain legal. Corridor and fixed-support cases have additional exact path evidence. | [Restricted theorem](research/illumination-k4-codex/restricted-theorem-note/theorem.txt), [corridor evidence](research/illumination-k4-codex/symbolic-corridors/) |
| Finite enumerations and controls | Support classifications, room and endpoint fixtures, trajectory witnesses, counterexamples, and verification records. Each run has its own bounds and endpoint conventions. | [Support census](research/illumination-k4-codex/k6-support-census/), [research guide](research/README.md) |
| Integrity and reproduction records | Per-file and per-package hashes, source provenance, review receipts, and supported fixed control suites. Hashes check file integrity; mathematical checkers verify the relevant certificate conditions. | [Manifests](manifests/README.md), [reproduction guide](docs/REPRODUCIBILITY.md) |

A compact certificate can encode a finite step in a proof; a census or successful trajectory sample establishes only its recorded search coverage. The rational-to-real manuscript is an analytic proof and needs no dataset. The default validation command checks file integrity and fixed controls; it does not replay the full SAT/DRAT corpus.

Try the small cylinder certificate, or list the larger proof-audit packages without downloading them:

```sh
python3 preprints/twenty-two-wall/verify_cylinders.py --check
python3 tools/archive.py list-data --prefix illumination-k4-codex/lower-bound-proof-audit/
```

Use the [selective download and restoration commands](docs/REPRODUCIBILITY.md#download-only-the-evidence-you-need) for larger evidence. Each `.tar.zst` package is a complete archive; only packages containing the selected source paths are needed.

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

## Verify a checkout

From the repository root, with the [validation dependencies](docs/REPRODUCIBILITY.md#dependencies):

```sh
python3 tools/validate.py
```

These controls need no large-data download. See the [reproduction guide](docs/REPRODUCIBILITY.md) for dependencies, selective downloads, and restoration. See [contributing](CONTRIBUTING.md) for changes to the research record.

## AI assistance

OpenAI Codex and Anthropic Claude were used to develop, review, and update the research, theorem proofs, and manuscripts in this archive. The authors remain responsible for the content.

## About us

I’m Peyton Wang, a 16-year-old student at Francis Parker School. I work on this project with my dad, [Daniel Wang](https://www.linkedin.com/in/ddwang/), who’s CTO at Citizen Health. It’s a hobby we share, and this is where we keep our proofs, code, and explainers.
