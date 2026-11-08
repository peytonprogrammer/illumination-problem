# Research sources

This directory preserves proofs, reviews, scripts, figures, and small supporting files in their research layout. Start with the [results inventory](../RESULTS.md) for statements and proof references, or the [manuscript catalog](../preprints/README.md) for readable PDFs.

| Source area | Main contents |
|---|---|
| [illumination-k4-codex](illumination-k4-codex/) | Lattice constructions, restricted minima, fixed-support proofs, and certificates |
| [claude-illumination-check](claude-illumination-check/) | Independent lattice checks, corridor proofs, and certificate reviews |
| [illumination-generalization-2026-11-06](illumination-generalization-2026-11-06/) | Orthogonal-room proofs, combs, necks, spirals, affine mechanisms, and reviews |
| [codex-proof-verification](codex-proof-verification/) | Cross-checks, scope assessments, and supporting proof records |
| [illumination-new-mechanisms](illumination-new-mechanisms/) | Proposed mechanisms and their evaluations |

The files at this directory's root are the original shared geometry, search, audit, and replay utilities and their fixtures. They remain together because their imports and source references use that layout.

Large evidence is stored in independent [case packages](../docs/DATA.md). The [file manifest](../manifests/README.md) maps each original source path to either a Git file or a package member. Use the [restoration command](../docs/REPRODUCIBILITY.md#restore-the-original-working-layout) when a script expects the original `.context/` layout.

A historical filename, pending banner, or successful fixture is not a theorem verdict. Use the linked statement and its scoped review record. The [named control suites](../tools/README.md) are the supported entry points for prescribed checks.
