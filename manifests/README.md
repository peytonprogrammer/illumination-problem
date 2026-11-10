# Manifest reference

These files describe the current archive. Each research source path has exactly one record in `files.jsonl`; no dated overlays need to be combined.

| File | Contents |
|---|---|
| [files.jsonl](files.jsonl) | One JSON object per research file: source path, current location, size, and SHA-256 |
| [packages.json](packages.json) | Independent download names, release tags, member counts, sizes, and compressed SHA-256 values |
| [current-snapshot.json](current-snapshot.json) | Coverage totals derived from the file and package manifests |
| [results.json](results.json) | Stable result IDs, statements, scope, and source links corresponding to the results inventory |
| [exclusions.json](exclusions.json) | Runtime files and downloaded dependencies outside the selected archive |

The file manifest is large. Use `python3 tools/archive.py list-data --prefix RESEARCH/PATH` to find relevant packages, or stream its JSONL records when you need file-level details.

## File records

| Field | Meaning |
|---|---|
| `source_path` | Original research-relative path; restoration places it under `.context/` |
| `storage` | `git` for a checked-in file or `package` for a release-archive member |
| `path` | Current repository-relative location of a Git file |
| `package`, `member` | Package ID and exact tar-member path for a packaged file |
| `bytes`, `sha256` | Size and SHA-256 of the current delivered file |
| `source_bytes`, `source_sha256` | Size and SHA-256 of the source version recorded at export |
| `previous_export_bytes`, `previous_export_sha256` | Prior delivered version, when recorded |

Use current delivered hashes for integrity checks. A proof or review receipt can instead pin a source version. Its verdict does not automatically apply to different bytes.

## Result records

`R01` through `R29` group substantive conclusions rather than individual fixtures or certificates. A `recorded_status` refers to the scoped internal review in the cited record; it does not imply external refereeing or formal verification. Conditional mechanisms and negative results remain distinct from completed illumination theorems.

Run `python3 tools/update_catalog.py` after changing the file or package catalogs or the results inventory. It refreshes derived counts, download tables, and result descriptions. Run it with `--check` to detect drift without writing files. See [reproduction](../docs/REPRODUCIBILITY.md) for integrity checks.
