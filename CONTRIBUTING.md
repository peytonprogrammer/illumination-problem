# Maintaining the research record

Preserve failed approaches as well as successful results. A failed mechanism is not a counterexample to a broader theorem. Keep exact input classes, endpoint conventions, boundary/corner rules, parameter limits and remaining cases attached to every claim.

Use stable result IDs in `manifests/results.json`. Add new statements and dated supplements rather than silently modifying a frozen proof. Bind independent reviews to exact source hashes; mandatory corrections/addenda must be linked from the final theorem record. Do not infer mathematical acceptance from a filename, an active goal, a successful sample, or a completed computation.

Keep generated formulas/certificates and large case data in versioned release archives, with complete source-path maps and SHA-256 values. Preserve the distinction between source and exported file hashes. Do not commit environments, credentials, nonresearch inputs, vendored packages or third-party book/paper downloads. Link published mathematical dependencies.

This is a snapshot archive, not automatic synchronization with the authors' working directories. A future snapshot needs a new manifest/release version and an explicit change record. Do not replace a released dataset in place.

No historical novelty, universal 22-wall minimum, external referee approval, or formal verification claim should be added without its own evidence. No project-wide license is assigned by this import.

Run `python3 tools/check_publication.py` before publishing changes to validate JSON, JSONL, SVG and PDF files. Review rendered PDFs and figures for layout errors. Record changed file hashes in a dated manifest. A historical check applies only to the exact file version it tested.
