# First exception-budget handoff

[done] Necessary counting relaxation for exactly k=4,5,6 transparent B/C exceptions and W<=23. No ray tracing, orbit runs, room solver, or polygon enumeration.

| Exact exceptions k | Surviving interior A counts I | Maximum triangles N in relaxation |
| --- | --- | --- |
| 4 | 2, 3 | 38 |
| 5 | 2, 3 | 41 |
| 6 | 2, 3, 4 | 44 |

Every J=0,...,k (with s_N=k-J) survives these necessary bounds for the listed I. This is not per-vertex feasibility, a polygon construction, or evidence of darkness. JSON contains all arithmetic tuples and marginal ranges. Counts beyond k=6 remain open here; do not infer a bound on the total number of exceptions.

## Derivation

Let F be the I full A cells, b its external four-neighbor boundary size, Q boundary A charge, J interior B/C exceptions, s_N smooth boundary B/C exceptions, and s_A smooth boundary A points. Prior validated identities and the missing-neighbor lemma give

    Q >= b-s_N,
    W = 2+6I+Q-(2J+s_N),
    N = 8I+Q+s_A,   0 <= 3s_A <= Q.

Thus W>=2+6I+b-2k. The universal b>=4 bounds I by floor((17+2k)/6), which is at most four at k<=6.

The new exact finite check finds b_min(1,2,3,4)=(4,6,7,8), over *all finite sets* of those cardinalities, including disconnected sets. To avoid a coordinate-window assumption, decompose F into components whose cells have Manhattan distance at most two. Their external boundaries are disjoint and additive. Every connected component can be grown by adding a cell within distance two of the existing set. Enumerating normalized connected sets gives 1,6,46,391 shapes at sizes 1,2,3,4. Minimizing over component-size partitions covers arbitrary sets.

Consequently four full stars require W>=34-2k: at least 26 walls for k=4, 24 for k=5, and 22 for k=6. All I>=5 are already excluded by the universal bound at k<=6. This explains the table's interior-A column.

For each remaining (I,J,s_N), the script enumerates W<=23, derives Q from the identity, and enumerates s_A<=floor(Q/3). N is then exact for that arithmetic tuple. The maximum values 38,41,44 follow. Every tuple independently satisfies the full regular-vertex identity

    R = 8I+4s_A+8J+4s_N = 4(N-W+2).

The script uses only the standard library and no prior room helpers. It does rely on the previously validated room identities and missing-neighbor lemma in ../illumination-analysis.md; it does not independently prove them.

## Reproduction and review

Run `python3 -B .context/illumination-new-mechanisms/exception-budget.py`. The script writes exception-budget.json; exception-budget.log records this run's concise summary. These files are Codex-owned. Peer verification should rebuild the boundary argument and tuple inequalities independently, without overwriting the receipt.

**Next move:** Claude can target I=2/3 at k=4 first with a wall-cost/illumination theorem. Codex can refine necessary cell connectivity within the proved 38-triangle bound without ray cuts.

Script SHA-256: `c7ea0b0cc2b681927a867909f21cdf8d3fbf385ca7aa4358cdded34557262bd6`.
