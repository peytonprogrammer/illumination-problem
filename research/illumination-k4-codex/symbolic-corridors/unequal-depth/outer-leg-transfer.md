# Transfer outer-simple paths through either endpoint cap

Codex01a18403. Candidate hand lemma; independent review required.

Normalize d=g=1. Choose flags lc,uc in {0,1} and effective depths

    A=a or 2h_--a, B=b or 2h_+-b.

Suppose there is a finite auxiliary connection from (s,-A) to (t,1+B) with the following structure. Before its first portal crossing at height0, it stays in the lower strip and reflects only at its vertical side walls. After its last portal crossing at height1, it stays in the upper strip and reflects only at its vertical side walls. Between these crossings it stays in the actual middle rectangle [1,3]x[0,1], and all its mirror contacts are on actual middle walls. Both portal crossings are strict. The auxiliary path is corner-free. Then actual S=(s,-a),T=(t,1+b) illuminate.

The initial and final strip portions have straight developments X_-(z),X_+(z) when their vertical side mirrors are unfolded. The middle portion need not have the same developed line; it may have ordinary reflections at the two middle ledges as well as at vertical walls. It does not revisit an outer strip before the final exit.

## Folding and endpoint-loop removal

If a lower cap is selected, replace the developed outer height by Y(z)=-2h_--z for z<-h_-, and by z otherwise. If unselected, leave it unchanged. This sends the auxiliary starting height -A to actual -a, fixes the strict portal, and introduces exactly one lower-cap contact. Side-wall contacts away from that cap remain actual smooth vertical reflections.

A smooth cap contact is an ordinary horizontal reflection. If the cap is also a side-wall corner, the triangular horizontal fold is even about that kink. Just as in the accepted cap-corner-removal proof, linearity of the initial outer development gives the actual source AGAIN at height z=-a, after the bad cap. Discard the prefix ending at that visit and retain the subsequent initial leg up to the same portal. The proof uses only linearity of X_- on the outer leg, not linearity through the middle.

At a selected upper cap, use Y(z)=2(1+h_+)-z for z>1+h_+, and z otherwise. If it is a corner, the final straight outer development reaches actual T already at z=1+b, BEFORE that corner; truncate there. Otherwise retain the smooth cap reflection and end at the auxiliary endpoint folded to actual T. The selected target horizontal image is unchanged by the triangular-wave symmetry, so the actual endpoint is t.

The lower retained interval ends at the portal0 and the upper retained interval starts at portal1. Thus their independent trims cannot overlap or remove any middle contact. The middle connection is left unchanged, with its actual smooth specular reflections. The folds preserve value and velocity near the two strict portals. Every retained contact is finite and legal, and all corner events were discarded. Truncate at any earlier actual T if necessary. This proves the lemma.

## Equal effective depths give a new sufficient condition

Assume 0<s,t<=1, the horizontal range remaining after the accepted common-core reduction. If ANY of the four effective sheet pairs satisfies A=B, then actual S,T illuminate.

Inspect the frozen accepted equal-depth proof, Sections2-7. Its paths for these horizontal marks are either vertical-only charts, or one of the explicitly described three-middle-reflection paths. Every such path has exactly the outer-simple structure required above: a single initial lower-strip leg with only vertical bounces, a middle path, and a single final upper-strip leg with only vertical bounces. The exceptional middle paths have no outer horizontal contact. Reflection/reversal to order s,t preserves this property.

Apply that equal-depth construction at depth A=B in auxiliary strips, choosing arbitrary auxiliary cap clearances beyond the marks; its formulas never use those auxiliary caps. Then apply the transfer lemma. Original actual cap heights need only satisfy the original interior inequalities. In particular this covers

    2h_--a = 2h_+-b,

as well as equality on either singly capped sheet and the original a=b case. This use of the equal-depth theorem is narrower than assuming every arbitrary auxiliary path transfers: its outer-simple property is explicitly checked from the frozen formulas.

The statement is sufficient. It does not prove general four-cap coverage, classify darkness, or establish a uniform reflection bound.

## Prescribed physical control

Take s=1/3,t=2/3,a=1/2,b=3/4,h_-=3/4,h_+=7/8. The original depths differ, but both selected effective depths equal1. The auxiliary equal-depth three-middle-reflection construction transfers to the actual path

    (1/3,-1/2) -> (7/12,-3/4) -> (7/3,1)
    -> (3,1/3) -> (8/3,0) -> (19/24,15/8) -> (2/3,7/4).

These are five actual reflections: lower cap, three middle walls, upper cap. The exact all-edge verifier in the frozen corner-removal-check.py validates containment, strict wall contacts and specularity, including the positive diagonal scaling and reversed path recorded in outer-leg-transfer-check.json. This is a prescribed control of the hand construction, not a ray search.
