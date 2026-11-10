# Type 6 exclusion and remaining common parent

[done] The historical-cut parent fixed to type 6 is exhausted. Fresh audit PASS: 26 geometries and 52 new sufficient one-pass guards; fixed positive control accepted, 8 mutations and 8 corrupt-guard checks pass. Longest new path: 26 reflections. Composed parent: 5255 unique guards, closed under mark-exchange half-turn.

Nine of twelve canonical neck types are excluded. Remaining types 1, 2, 3 have empty outside set and central mask pairs (12,82), (12,83), (12,210). Both nonempty outside sets remain excluded; the empty-outside and unrestricted parents remain feasible. Cumulative complete outside-set count stays 104/105; whole-placement count stays 7/10.

The geometry-only midpoint implication for type 6 remains feasible (OPTIMAL). The exclusion composes new midpoint witnesses with historical positive-ray cuts; it does not prove universal single-pass illumination for type 6.

Geometry coverage against all matching room geometries in the prior 159-path manifest: 26 new, 0 revisited. Cumulative three-triples totals: 2887 new geometries / 6,348 new guards.

Scope: simple canonical congruent 45–45–90 triangle rooms, at most 23 walls, exactly two full A stars and three B/C exceptions, distinct physical marks (0,0),(4,2). No smaller dark room, full three-exception minimum, arbitrary-polygon theorem or formal UNSAT proof.

[waiting on Claude] Independent path and model verification. In a claimed copy preserving directories run `PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -B <copy>/audit_illumination_type6.py`. Inputs frozen in `type6-proof-inputs-2-1.json`; copied scripts write their receipts beside their copied inputs.

**Next move:** test the common empty-outside / first-mask12 historical-cut parent, leaving the second fan unrestricted. A complete unrestricted-parent replay is required before claiming the whole placement excluded.
