# Snapshot scope and provenance

The archive contains research statements, proofs, reviews, scripts, figures, failed approaches, and computational evidence. The [data catalog](DATA.md) gives current coverage and download sizes; [current-snapshot.json](../manifests/current-snapshot.json) contains the same counts in machine-readable form.

## File organization

- `preprints/` contains readable manuscripts and supporting notes, with their LaTeX sources and build instructions.
- `research/` preserves the research file layout. A filename or old status banner is not evidence that a claim was accepted.
- `manifests/files.jsonl` maps each research source path to its current Git location or case-package member.
- `manifests/packages.json` identifies the independent release downloads and their checksums.

The [results inventory](../RESULTS.md) links statements to their hypotheses and review records. Later corrections supersede earlier claims only at the scope stated in their sources. The universal minimum-wall problem, general ten-wall illumination, and the proposed full-affine-group bound remain unresolved by this archive.

## Provenance and review pins

Source and exported SHA-256 values are recorded separately. Use the exported hash to verify a delivered file. A historical review pin applies to the exact source version it names. A different hash does not establish that a later version received the same review.

Manuscript [import provenance](../preprints/provenance.json) identifies copied sources. The generated eight-wall manuscript has its own [source pin](../preprints/eight-wall/provenance.json) and [verification record](../preprints/eight-wall/verification.json). See [the manifest reference](../manifests/README.md) for field definitions.

## Dependencies and licenses

No repository-wide license has been assigned. Existing author and dependency notices remain applicable. Runtime environments, caches, generated executables, and selected downloaded dependencies are excluded as listed in [exclusions.json](../manifests/exclusions.json).

The retained historical Python SAT source subset includes its [license](../research/illumination-k4-codex/lower-bound-proof-audit/arithmetic/sources/python_sat-1.9.dev17/LICENSE.txt). The archived DRAT source retains its [license](../research/claude-illumination-check/k5-residual/own-drat/src/LICENSE). Some case packages contain downloaded dependency or literature artifacts; their existing notices apply. Inclusion does not relicense upstream material.

## Verification limits

File checks cover Git hashes, compressed package hashes, and package-member paths, sizes, and hashes. Named reproduction suites run fixed geometric controls. These checks do not re-prove every theorem, replay the entire certificate corpus, or provide external expert refereeing.

See [reproduction](REPRODUCIBILITY.md) for commands and dependencies.
