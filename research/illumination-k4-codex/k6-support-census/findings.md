# Cheap k6 support census

[done] Pure combinatorial census. No SAT solving, optical guards, ray tracing or new room discovery.

At W<=21,k<=6,N<=41, I2 has cap P+m<=12 and I3 has cap P+m<=10.

| Full stars I | Full-support shapes | Marked pairs, same convention as k5 | Marked-pair symmetry orbits | Triangle universe |
|---|---:|---:|---:|---:|
|2|18|18|18|656–1024|
|3|18|43|38|104–440|
|Total|36|61|56|104–1024|

Relative to k5's 22 supports and 31 raw marked pairs, this adds 14 supports and 30 raw marked cases. There are four new I2 placements, all at Manhattan distance seven, and ten new I3 shapes. Five duplicate marked cases can be removed by stabilizers of their full-cell support, leaving 56 symmetry orbits. The primary comparison retains the existing raw-pair convention (61) to avoid silently changing the pipeline.

## Completeness

Let F be the set of full A cells, R=F union its axis neighbors, b=|R-F|, U the occupied cells, and H=U union R. The previously proved budget gives |H|<=I+cap. H is axis-connected: U is connected, and every cell of R attaches to its full cell in F. At most cap-b cells of H lie outside R. Thus every occupied cell is within cap-b axis steps of R; this is the encoder-style finite universe used here.

**I2.** The crude connected-H bound gives full-mark distance<=13, so the script checks every normalized displacement in that range. For distance d>=3, connecting the two mandatory neighborhoods requires at least d-3 outside cells. With b=8 and outside budget4 this forces d<=7. The d2 overlaps have b6 or b7 and are included. Every previously listed I2 case is retained.

**I3.** H has at most13cells, so every full cell is in the radius12 diamond about any chosen full root. Exhausting all triples in that diamond is complete. Keep b<=10. If the graph joining full cells at distance<=2 is disconnected, its external neighbor sets are disjoint between components. A two-cell component needs at least6external neighbors and a singleton4; three singletons need12. Therefore a retained disconnected overlap graph must have b=10 and outside budget zero. Its R must itself be connected. Rejecting disconnected R at b10 is consequently necessary, not an extra assumption.

The radius12 enumeration leaves306rooted triples and18symmetry classes. The same306rooted triples lie within radius5. Eight of the18classes have disconnected distance-two full-cell overlap graphs. These are NEW and would be lost by reusing k5's connected-overlap/radius4 premise. The other two new classes are overlap-connected b10 supports.

Every nonadjacent unordered marked pair of full cells is retained. Adjacent marked full cells are omitted only by the already accepted direct-segment theorem. The optional marked-pair orbit count uses simultaneous translations and D4 on the full support and the unordered pair.

Every allowed A cell contains eight distinct canonical triangles. The reported universe sizes are eight times the corresponding dilated-cell-universe counts, independently checked against triangles from the frozen geometry module. N<=41 bounds selected triangles, not the larger universe of possible triangles.

## Size comparison, not a runtime prediction

The old31rawcases have10,560possible-triangle incidences when universes are summed per marked pair. The new61have21,880. This is a combinatorial size comparison only; solver time can change nonlinearly. No new timing or full-tranche estimate was measured.

## Full table

|Case|I|b|Outside budget|Allowed cells|Triangle universe|Raw pairs|Pair orbits|
|---|---:|---:|---:|---:|---:|---:|---:|
|I2_1_1|2|6|6|128|1024|1|1|
|I2_2_0|2|7|5|109|872|1|1|
|I2_2_1|2|8|4|82|656|1|1|
|I2_3_0|2|8|4|90|720|1|1|
|I2_2_2|2|8|4|83|664|1|1|
|I2_3_1|2|8|4|90|720|1|1|
|I2_4_0|2|8|4|97|776|1|1|
|I2_3_2|2|8|4|92|736|1|1|
|I2_4_1|2|8|4|98|784|1|1|
|I2_5_0|2|8|4|104|832|1|1|
|I2_3_3|2|8|4|94|752|1|1|
|I2_4_2|2|8|4|99|792|1|1|
|I2_5_1|2|8|4|104|832|1|1|
|I2_6_0|2|8|4|109|872|1|1|
|I2_4_3|2|8|4|102|816|1|1|
|I2_5_2|2|8|4|106|848|1|1|
|I2_6_1|2|8|4|110|880|1|1|
|I2_7_0|2|8|4|114|912|1|1|
|I3_k6_0|3|10|0|13|104|3|3|
|I3_k6_1|3|10|0|13|104|2|2|
|I3_k6_2|3|10|0|13|104|3|2|
|I3_k6_3|3|10|0|13|104|3|3|
|I3_k6_4|3|10|0|13|104|2|2|
|I3_k6_5|3|10|0|13|104|2|2|
|I3_0|3|9|1|26|208|3|3|
|I3_k6_6|3|10|0|13|104|3|3|
|I3_1|3|9|1|26|208|2|2|
|I3_k6_7|3|10|0|13|104|2|2|
|I3_k6_8|3|10|0|13|104|3|2|
|I3_2|3|8|2|39|312|3|2|
|I3_3|3|9|1|25|200|2|2|
|I3_k6_9|3|10|0|13|104|3|2|
|I3_4|3|8|2|39|312|2|2|
|I3_5|3|8|2|39|312|3|2|
|I3_6|3|8|2|39|312|1|1|
|I3_7|3|7|3|55|440|1|1|

## Review and next stage

Independent peer verification of counts and completeness is requested. The peer-owned I4 branch has separately been closed by necessary geometry; its three certificates are independently replayed in ../k6-i4-review/. No I2/I3 geometry feasibility, darkness classification, or k6 exclusion is claimed here. Full SAT/guard continuation remains outside the approved cheap stage.

Reproduce from a copied directory with its frozen inputs: `python3 -B count.py`. This does not invoke the SAT encoder or any optical code.
