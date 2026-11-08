# Independent audit of the fast k=4 implementation

2026-10-31. Status: partial pass, with explicit limits. No ray search or origami orbit generation.

The saved 22-wall candidate passes independent physical geometry validation:
30 triangles, 15 whole unit squares, simple Jordan boundary, 22 walls, two interior
marks, four smooth non-A boundary points, no slits or boundary contacts.
Its local inventory is I=2, J=0, s_N=4, Q=12, N=30.
This finding takes priority over further exclusion enumeration. Darkness is now independently verified by the 2,592-state certificate in
independent-orbit-certificate.json; see candidate-22-proof.md.

## Accepted checks

- All 528 local vertex masks match an independent incident-sector computation.
- The 20 saved mark placements match an infinite dual-tiling distance computation.
- Every vertex of an eligible N<=38 room lies in [-64/3,64/3]^2, inside the
  enumerator's [-24,24]^2 window. Do not extend that window argument to N=44.
- 10,000 synthetic learn/assign/undo transitions preserve the certificate counts.
- Three saved old/new enumeration datasets have identical room sets, of sizes
  224, 260 and 1,356. These finite comparisons are implementation checks.
- An independent four-sheet rectilinear unfolding has 60 squares, 4 source sectors,
  4 target sectors, 40 blocked sectors and 12 clear sectors. Its genus is 10.

## Remaining limits

The clause bookkeeping test disables unrelated vertex updates; it does not establish
full undo-state correctness. Normal termination and coverage must be verified for
each actual enumeration before accepting an exclusion.

The cached U/Z clauses omit paths and source hashes, and learned witnesses appear
memory-only. Their disjointness passes, but actual clause-by-clause proof replay is
not possible from the saved files. The peer's checker regenerates clauses instead
of replaying those cache entries.

Fixed-epsilon around() asserts at the valid rational point (0,1/1000). This can
interrupt certificate creation. It does not by itself make emitted certificates
unsound: conservative supersets of incident triangles impose stronger tile
requirements, and wall() requires exactly two incident tiles. Exact incidence
predicates would remove the fragility.

## Reproduction

Run `.context/illumination-venv/bin/python -B .context/illumination-k4-codex/peer-fast-audit.py`.
The full machine-readable results, independent unfolding, and frozen input hashes
are in peer-fast-audit.json and peer-fast-inputs/manifest.json.
