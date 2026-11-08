# Verification and reproduction

The archive separates intact file delivery, prescribed computational controls, mathematical arguments, internal AI reviews, and external refereeing. A checksum or successful example replay does not prove a quantified theorem. Earlier pending/rejected statements are retained as history; later corrections supersede them only at their exact scope.

## Read ordinary files first

Proofs, code, review receipts, diagrams, and small supporting data are ordinary files under `research/`. Files originally placed in the bulk dataset solely because they belonged to generated case directories are now also directly browseable when at most 1 MiB. New/updated reviewed material is indexed in [the current update](UPDATE-2026-11-08.md).

`manifests/files.jsonl` preserves the original snapshot. Dated `files-*.jsonl` manifests are applied in filename order; the last record for an original `source_path` is its current version/location. Original and exported SHA-256 values are separate. `manifests/packages.json` identifies independently downloadable large-evidence packages. Every member has its own size/hash in the file manifests.

```sh
python3 tools/archive.py verify-git
python3 tools/test_archive.py
python3 tools/reproduce.py eight-wall
python3 tools/reproduce.py affine
```

`verify-git` checks current Git-stored research bytes, without running archived code. The two named reproduce suites execute prescribed controls in disposable copies, adapting historical workspace-path markers only in those copies. They do not perform research discovery or install solvers.

## Download only relevant large evidence

Browse [the package index](DATA.md), or list packages matching a readable research path:

```sh
python3 tools/archive.py list-data --prefix illumination-k4-codex/symbolic-corridors/
python3 tools/archive.py download --prefix illumination-k4-codex/symbolic-corridors/
python3 tools/archive.py verify-data --prefix illumination-k4-codex/symbolic-corridors/
```

Each package is an independent `.tar.zst` file. Unlike the original snapshot, these packages do not need concatenation or unrelated packages. Large cases may have several independent numbered packages. The tool downloads through authenticated `gh`, verifies compressed SHA-256, streams every member through its own size/hash check, and rejects duplicates, unexpected members, links and path traversal. Python 3, `gh` and `zstd` must be installed separately. Downloads do not change repository access.

Use `--all` explicitly to download/verify every current package. With no selection, `download`, `verify-data` and `restore` stop rather than silently downloading all data. A corrupted cached package is reported, not silently replaced.

## Restore a selected historical layout

```sh
python3 tools/archive.py restore --workspace /absolute/path/to/empty-workspace \
  --prefix illumination-generalization-2026-11-06/fable/eight-wall-review-packet/
```

The tool reconstructs selected current exported files under the destination's `.context/`, fetching only packages needed by that selection. A Git-only selection downloads no data. It refuses a nonempty workspace. Individual package members retain readable research-relative paths; restoration places them under `.context/`. Package files are installed only after their full package verifies.

Historical scripts can require additional source families, path adaptations or separately installed solvers. Restoring their files does not make every historical pipeline portable. No archived program executes automatically. See the named reproduction suites for the small controls tested on this release.

## File hashes and proof pins

The manifests record source and exported SHA-256 values separately. Use the exported hash to verify a repository file. A historical receipt applies only to the exact bytes it identifies. Numerical certificates retain their source bytes unless their manifest record specifies a change.

This publication verifies file coverage, packaging, checksums, selected control execution and delivery. It does not rerun all SAT/DRAT proofs, re-prove every theorem, confirm historical novelty or provide external mathematical review.

## File validation

Run `python3 tools/check_publication.py` from the repository root. This requires Poppler's `pdftotext` and `pdfinfo`. The tool parses JSON, JSONL and SVG files and checks PDF readability. Inspect rendered PDFs and figures separately for layout errors.

The latest file records are in `manifests/files-2026-11-08-z-update.jsonl`. Records in dated manifests supersede earlier records for the same source path. File checks and typesetting do not replace mathematical review.
