# Final proofreading

- [done] Read all four pages of the main proof and both pages of the additional example.
- [done] Exact reconstruction confirms both boundary cycles, 22/30 wall counts, corner censuses, interior marked points, mark fibers and four reversal points in each room. Printed coordinate cycles agree up to cyclic order and reversal.
- [done] Inspected all six final page renders after corrections. Page numbering, diagrams, tables and margins are clear; no clipping or orphan pages.

## Wording corrected

1. Changed “may not pass through an actual corner” to “may not hit an actual corner” to state the path convention precisely.
2. Made the even-coordinate endpoint and repeated-halving instruction more explicit.
3. Used arbitrary signed (p,q) in the endpoint-velocity table, distinct from the positive (u,v) used in the worked example.
4. Clarified the retrace endpoint: during the retrace b would already have been visited; at its end the curve is at a, so the return is an interior visit.
5. Removed an unnecessary comment from the supplementary proof.

No change to the construction or mathematical conclusion. No new searches or mathematical changes. Existing separate mathematical peer review remains applicable; these are clarity edits, not a new peer review.

## Recheck

Run `venv/bin/python -B proofread.py` from this directory. See proofread.json for final PDF hashes and automated checks. Visual results are recorded above.
