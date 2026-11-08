# Accepted-checker reproducibility audit

Codex01a1a00f. All14accepted independent verification programs reproduced
their frozen JSON outputs byte-for-byte in a fresh temporary copy. All117
original source/certificate files in the snapshot scope remained unchanged.
The run completed in6.49seconds. See result.json for individual commands,
exit codes, output hashes and recorded standard output; run.log preserves
live execution progress. The temporary copy was removed after verification.

This audit executes only the reviewer-owned equal-depth and finite-resonance
checkers, unequal-depth midpoint/repair/cap-sheet/completeness controls,
centered/phase/exterior/twist checkers, centered source reconciliation,
14prescribed rational failures, the fixed-room continuum verifier, and
receipt integrity checker. It never executes peer discovery or writer code.
Each subprocess has a300second timeout with process-group termination.
This is exact replay of already prescribed proof controls, not discovery.

The final isolated integrity command also reproduces its133checks and
explicitly retains whole_unequal_depth_theorem_accepted=false. Thus the
accepted packets are reproducible, but the full objective remains incomplete.
No current packet proves the universal case with all six normalized
parameters rational and no denominator bound. The peer owns that construction;
its next frozen lemma is required for the remaining independent review.

Reproduce:

    python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/reproducibility-audit/run.py

The runner writes only its own result.json and a temporary copy. It preserves
all original frozen proof/checker outputs. If a live peer source changes
during a future run, the runner reports changed_originals rather than
silently accepting a new snapshot; reconcile that source before using it.
