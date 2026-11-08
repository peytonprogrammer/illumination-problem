# Necessary full-A-cell supports for the bounded proof

[done] This proof justifies the 22 support patterns and 31 marked pairs. The independently rebuilt list in `support-check.json` agrees with the earlier Codex list; neither peer executable nor peer model is used. The reductions are conservative at W<=23,k<=4 and therefore cover the present W<=21 threshold.

Let F be the I full A cells in the grid of A coordinates divided by two. Let P count nonempty partial A cells. The cell graph joins two occupied cells when selected triangles share an edge across their common cell side. Interior triangle connectivity implies this graph is connected. A full cell has degree at most four. For a contiguous partial A fan, its charge is at least the number of cell sides it touches: m triangles cost m, except a four-triangle half-star costs three and touches at most three sides. Thus Q dominates the sum of partial-cell graph degrees.

Let R=F union its four-neighbors, b=|R-F|, and let m count empty cells of R-F. Each empty external neighbor removes at least one potential full-cell graph edge; hence the sum of full-cell degrees is at most 4I-m. Connectedness requires at least I+P-1 graph edges, giving

    Q >= 2(I+P-1)-(4I-m) = 2P-2I-2+m.

A missing external neighbor yields a smooth C exception at a side midpoint of an adjacent full cell. Different missing cells can be charged to different such midpoints. Thus m<=s_N, and E+m=2J+s_N+m<=2k. Combining with W=2+6I+Q-E gives

    2(P+m) <= W-4I+E+m <= W-4I+2k.

At W<=23,k<=4 this yields P+m<=11 for I=2 and <=9 for I=3. At the present W<=21 it yields <=10 and <=8 respectively. Also b<=P+m. The number of occupied cells outside R is exactly P-(b-m)=P+m-b, so it is at most the corresponding cap minus b. Every occupied outside cell has a path to R through the connected cell graph; a shortest such path uses distinct outside cells. Its Manhattan distance from R is therefore at most that outside-cell count. Taking the full Manhattan neighborhood of R of that radius covers every eligible room.

The already proved Q>=4-s_N gives I<=3 at W<=21,k<=4. Thus only I=2 and I=3 require supports.

For I=2 the two full cells are the marked cells. Manhattan separation one is directly illuminated. Normalize the other offsets by the eight grid symmetries. At separation D>=3 their two four-neighbor crosses have b=8. Any cell path between them uses at least D-3 cells outside the crosses. The conservative outside-cell cap is 11-8=3, so D<=6. At separation two the two normalized offsets are (1,1) and (2,0). Taking every normalized offset of separation two through six gives the 14 I=2 supports.

For I=3, consider the graph on full cells joining pairs at Manhattan distance at most two. Different components have disjoint external neighbor sets. A single full cell has four external neighbors and any two have at least six, so a disconnected three-cell set has at least ten external neighbors. This contradicts b<=9. Therefore the full cells are overlap-connected. Starting from any one, the other two lie within Manhattan distance four. Exhausting the two additional positions in that finite diamond gives 138 overlap-connected rooted triples before the external-neighbor cap. Retaining b<=9 leaves 120 rooted triples and eight shapes up to translations/grid symmetries. The excluded 18 triples all have b=10; this accounts exactly for the earlier Codex/Claude count discrepancy (`provenance/root-count.json`). The independent finite reconstruction enumerates these full-star sets only; it is not a room search.

Every possible marked pair among the three full cells is retained unless its separation is one, which gives a direct segment. This produces 17 I=3 marked-pair cases. Together with the 14 I=2 cases there are 31 cases in 22 supports. The stronger W<=21 cap may immediately exclude some conservative supports; retaining them is harmless.

The CNF additionally enforces the stronger W<=21 outside-cell cap. This is a necessary condition for connected rooms, even though the SAT model initially permits disconnected assignments and rejects them separately. An UNSAT proof of that relaxation still excludes every eligible connected room.
