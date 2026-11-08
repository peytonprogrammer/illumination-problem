# Verify and reproduce the archive

Run these commands from the repository root. File verification checks delivery and integrity. The named controls exercise fixed constructions; they do not prove the full mathematical statements.

## Dependencies

| Task | Required tools |
|---|---|
| Verify Git files, list packages, or refresh catalogs | Python 3, standard library only |
| Download and verify case packages | Python 3, authenticated GitHub CLI (`gh`), and `zstd` |
| Restore a selection containing only Git files | Python 3 |
| Run the eight-wall and affine controls | Python 3; the eight-wall runner also uses a POSIX shell |
| Validate PDFs and structured files | Python 3 and Poppler (`pdftotext`, `pdfinfo`) |
| Build a manuscript | Tectonic; see its folder's README for additional regeneration dependencies |

## Verify files and run fixed controls

```sh
python3 tools/archive.py verify-git
python3 tools/check_publication.py
python3 tools/reproduce.py eight-wall
python3 tools/reproduce.py affine
```

`verify-git` checks every Git research file against the current [file manifest](../manifests/README.md). `check_publication.py` parses JSON, JSONL, and SVG files and checks PDF readability. Inspect rendered PDFs and figures separately for layout errors.

The eight-wall suite runs twelve prescribed scripts. The affine suite checks four fixed shear paths and one fixed diagonal example. Both use disposable copies, adapt historical workspace-path markers in those copies, and leave archived files unchanged. Neither suite downloads case data or runs a discovery search.

## Download only the evidence you need

Browse the [data catalog](DATA.md), then select a research family or case:

```sh
python3 tools/archive.py list-data --prefix illumination-k4-codex/symbolic-corridors/
python3 tools/archive.py download --prefix illumination-k4-codex/symbolic-corridors/
```

A prefix is relative to the original research root, without `research/` or `.context/`. It can also be an exact source-file path. Downloads go to `.data-cache/` by default; use `--cache /path/to/cache` to choose another location.

Each package is a complete `.tar.zst` archive. The download command verifies its compressed SHA-256 and every member's path, size, and hash. Files from unrelated packages are not needed. A large case can span several packages.

To recheck cached packages:

```sh
python3 tools/archive.py verify-data --prefix illumination-k4-codex/symbolic-corridors/
```

Use `--all` explicitly to select the entire archive. A missing selection is an error for download, verification, and restoration. A corrupt cached package is reported rather than overwritten.

## Restore the original working layout

```sh
python3 tools/archive.py restore --workspace /absolute/path/to/empty-workspace \
  --prefix illumination-generalization-2026-11-06/fable/eight-wall-review-packet/
```

Restoration writes the selected files under the destination's `.context/`, using their `source_path` values. A selection of Git files needs no download. If selected files belong to a package, the tool verifies the whole package before installing those members. The destination must be empty.

Restoration preserves file layout; it does not install solvers or make every historical pipeline portable. A script can depend on other source families. Use the named control suites when you want the fixed checks supported by this checkout.

## Maintain catalogs

```sh
python3 tools/update_catalog.py
python3 tools/update_catalog.py --check
python3 tools/test_archive.py
```

The catalog updater derives download tables and snapshot counts from the file and package manifests. It also synchronizes the machine-readable result descriptions with `RESULTS.md`. `--check` reports stale generated files without writing them.

Source hashes, exported file hashes, and review pins have different roles; see [the manifest reference](../manifests/README.md). Passing file checks does not rerun the full SAT/DRAT corpus, establish novelty, or replace external mathematical refereeing.
