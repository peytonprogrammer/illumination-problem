# Maintain the research record

Preserve failed approaches as well as successful results. Attach the exact input class, endpoint conventions, corner rules, parameter limits, and remaining cases to every mathematical claim. A failed mechanism is not a counterexample to a broader theorem.

## Where changes belong

| Change | Location |
|---|---|
| Reader-facing manuscript or supporting note | `preprints/`, with source and build instructions |
| Proof, review, checker, or supporting evidence | `research/`, retaining usable source paths |
| Result statement, scope, or source links | `RESULTS.md`, using the existing stable result IDs |
| Current file locations and hashes | `manifests/files.jsonl` |
| Large case data | A versioned release package, indexed in `manifests/packages.json` |
| Reading or reproduction instructions | `docs/` |

Bind reviews to exact source hashes and link mandatory corrections from the final theorem record. Add explicit supplements when a mathematical statement changes. Do not infer acceptance from a filename, a successful example, or a completed computation.

Keep source and delivered hashes distinct. Link published literature and preserve dependency license notices. New runtime environments and downloaded dependency bundles do not belong in Git. Existing archived dependencies retain their own notices; this archive has no project-wide license.

## Validate a change

```sh
python3 tools/update_catalog.py
python3 tools/update_catalog.py --check
python3 tools/archive.py verify-git
python3 tools/check_publication.py
python3 tools/test_archive.py
```

Review rendered PDFs and figures when they change. Update manuscript provenance after rebuilding. A historical check applies only to the exact version it tested.

Use a new release version for a changed dataset and update its file records and package checksums together. Add new result IDs only with a category, scope, and cited evidence. No novelty, universal minimum, external referee approval, or formal verification claim follows from packaging or a successful control run.
