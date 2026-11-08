# Manuscripts and research notes

Start here for readable PDFs and their sources. Each manuscript has its own folder with `manuscript.pdf`, `manuscript.tex`, a README, and any required figures. These are working drafts for review; historical novelty is unconfirmed and external mathematical refereeing remains outstanding.

## Theorem manuscripts

| Manuscript | PDF | Source and scope |
|---|---|---|
| Eight-wall illumination | [PDF](eight-wall/manuscript.pdf) | [Full corrected proof, arbitrary real dimensions and interior endpoints](eight-wall/README.md) |
| Twenty-two-wall dark-room construction | [PDF](twenty-two-wall/manuscript.pdf) | [Explicit construction; likely independent rediscovery](twenty-two-wall/README.md) |
| Three-star surplus-four illumination | [PDF](three-star-surplus-four/manuscript.pdf) | [Fixed support, at most 21 walls and six transparent points](three-star-surplus-four/README.md) |
| Twelve-wall corridor illumination | [PDF](twelve-wall-corridor/manuscript.pdf) | [Specified four-parameter family; outer-chamber pairs](twelve-wall-corridor/README.md) |

## Historical and discussion notes

These are supporting records, separate from the theorem manuscripts.

| Note | PDF | Status and source |
|---|---|---|
| Construction and older restricted minimum | [PDF](notes/restricted-minimum-k4/note.pdf) | [Historical k≤4 coverage; does not cover the current k≤6 result](notes/restricted-minimum-k4/README.md) |
| Pocket-detection question | [PDF](notes/pocket-detection/note.pdf) | [Open question and conjectures, not a completed theorem](notes/pocket-detection/README.md) |

## Results without a standalone manuscript

The current k≤6 restricted minimum still needs a consolidated manuscript. Comb, long-neck/network, strict-fold and ten-wall spiral results remain in the [results inventory](../RESULTS.md) and linked proof records. Recent affine mechanisms and obstructions remain in the [November 8 update](../docs/UPDATE-2026-11-08.md). A theorem can have a completed proof record without a standalone PDF.

## Repository layout

```text
preprints/
  README.md                     Manuscript catalog and coverage
  provenance.json               Original paths and hashes for imported files
  eight-wall/                   Corrected eight-wall theorem
  twenty-two-wall/               Dark-room construction
  three-star-surplus-four/       Fixed-support lattice theorem
  twelve-wall-corridor/          Outer-chamber corridor theorem
  notes/
    restricted-minimum-k4/       Historical construction/minimum note
    pocket-detection/            Open-question discussion brief
research/                       Frozen proofs, reviews, scripts and evidence
manifests/                      Archive file and package records
```

[Import provenance](provenance.json) records each source and SHA-256. The eight-wall manuscript retains its own [provenance](eight-wall/provenance.json) and [verification record](eight-wall/verification.json).

Read each folder's README before rebuilding. Research remains paused; this organization adds no theorem or proof claim.
