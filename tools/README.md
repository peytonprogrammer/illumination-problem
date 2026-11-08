# Archive tools

Run these tools from the repository root. They use Python 3 and the standard library; task-specific dependencies are listed in the [reproduction guide](../docs/REPRODUCIBILITY.md#dependencies).

| Tool | Purpose | Example |
|---|---|---|
| [archive.py](archive.py) | Verify Git research files; list, download, verify, or restore selected evidence | `python3 tools/archive.py verify-git` |
| [reproduce.py](reproduce.py) | Run the fixed eight-wall or affine controls in a disposable copy | `python3 tools/reproduce.py eight-wall` |
| [check_publication.py](check_publication.py) | Validate JSON, JSONL, SVG, and PDF readability | `python3 tools/check_publication.py` |
| [update_catalog.py](update_catalog.py) | Refresh derived counts, the data catalog, and result descriptions | `python3 tools/update_catalog.py --check` |
| [test_archive.py](test_archive.py) | Check archive integrity, safe extraction, and selective restoration behavior | `python3 tools/test_archive.py` |

The archive tool does not execute research scripts. The reproduction runner executes only its two named fixed suites. Files restored from historical research can require additional dependencies and source families.
