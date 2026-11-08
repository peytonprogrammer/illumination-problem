# Complete prescribed TR02 feasibility audit on one existing spiral pair

The predeclared effort concerns ONLY the already used doubled spiral parameters(a,l,w,A;b,c,h,H)=(4,12,20,28;4,8,20,28), actual S=(2,6),T=(14,2). It tests the new TR02 spiral chart, not the expired A13 nested-staircase chart effort. No replacement metric or pair was searched.

## Exact reduction of every unbounded index

Here R=8,B=16,d0=14,g0=16,g1=12,d2=6,D=48. The target equation is

    48 tau =8n+56m+28+16k+32j+14 eT-2 eS.

Its right side belongs to4Z for every sign/indices, so every solution has tau in(1/12)Z. A change tau->tau+112 shifts n,m,k,j by196,32,84,21 respectively and leaves all three signed portal residuals and the target fold unchanged. These shifts give exactly48*112 on the right of the target equation. Thus every positive solution has a representative among1344 residues tau=i/12,0<=i<1344; any valid zero representative can be translated to positive slope. This is a proved fixed-input period, not a cutoff on physical reflections.

For each source sign and tau, strict first portal|eS*2+14tau-8n|<4 determines n uniquely when possible. The cap condition then determines the unique odd28 center (2m+1)28 when its residual has magnitude<8; otherwise it fails. The right condition similarly determines the unique16k center with residual magnitude<8. Finally test both exact target residues+/-14 modulo32. All equalities at strict endpoints are rejected; zero portal residuals remain included as smooth contacts. These rules exhaust all integer choices for this input.

The exact finite replay finds178 feasible witness residues. This establishes FEASIBILITY on this input only, and supplies no universal-feasibility conclusion or all-r3 theorem.

## Actual path, not just a root

The first witness has

    tau=7/6, eS=eT=1, (n,m,k,j)=(2,0,0,0),
    (z0,z1,z2)=(7/3,-7,7).

Its actual physical path starts at S with velocity(7/6,1), reflects successively at

    (4,54/7),(0,78/7),(4,102/7),(0,18),
    (35/3,28),(28,14),

and reaches actual T=(14,2) at time48, with velocity(-7/6,-1). There is exactly one top-wall reflection and otherwise only vertical-wall reflections. All six contacts are strict interiors of original finite walls. The inherited pure reviewer all-wall checker passes70 wall/leg guards, excludes every true corner, verifies specular velocity and the original actual endpoint. The endpoint lies below the initial source height and every ascending source-arm point stays in the left arm, so there is no earlier actual-target arrival; the descending height reaches2 only at the final point.

The roof phase is35/3, which is not a multiple of28. Thus this is an actual ordinary ray, not an algebraic candidate with a hidden roof-corner contact.

## Clock and scope

The effort used a conservative start equal to the author's earlier candidate publication,21:58:23.368830UTC, so all reviewer reading/setup was included. The nonrenewed deadline was22:12:23.368830UTC; the effort finished with the actual witness verified after343.203258seconds from that conservative start. No subprocess or restart remained live. The fixed result/replay and actual witness are saved separately; no further discovery under this effort is intended. Replaying the recorded fixed calculation is prescribed verification.

TR02's universal feasibility remains open. This audit cannot be used to infer that any other geometry, endpoint pair or turn type works, nor that the displayed word is minimal. The original ten-reflection stress witness remains a separate valid word. No new search engine, census, worker, fitting or git mutation occurred.
