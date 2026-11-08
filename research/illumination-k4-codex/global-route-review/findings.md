# Which next step advances the22wall lower-bound question?

[done] 2026-11-01. The U-room branch is parked after its completed results. The next direct target is the five-exception canonical45 case, using a sharper support reduction and existing certified guards. This report separates direct progress from supporting theory.

## 1. What the U results actually close

Under the accepted Jordan point-collapse theorem, a dark sequence with distinct interior limit marks gives a decorated limit: a room with extra smooth boundary blockers. Its cost W+2B does not increase. Ordinary illumination of the underlying room cannot erase those blockers.

| Limit class | What is excluded | Remaining gap |
|---|---|---|
|Any U room, no retained blockers|Every interior pair connects by the new finite construction plus accepted L lemma|This alone does not cover a smooth-step limit|
|Symmetric U with mirror-symmetric upper marks, one retained blocker|Three-path theorem avoids every singleton; stable under small asymmetric changes|Does not cover arbitrary U/mark configurations|
|Unequal heights within condition(U), one retained blocker|Two paths have disjoint boundary contacts|Larger height differences and horizontal asymmetry remain|
|U room with several retained blockers|No general exclusion|At cost<=21, W=8 permits B<=6|

Thus these results close specific decorated-limit subcases, but no theorem reduces every hypothetical W<=21 dark room to one of them. Continuing arbitrary U lemmas has uncertain global return until that reduction exists. Park this branch rather than treating it as the main path to22minimality.

## 2. The parity sign theorem is also a supporting branch

The independently reviewed parity enumeration already excludes strictly simple parity rooms with two interior A marks at W<=22. The accepted folded-parity theorem excludes its whole class below22. A hypothetical canonical45 counterexample with W<=21 is therefore neither a parity room nor a folded-parity room.

A sign theorem ONLY for parity rooms does not itself eliminate a remaining W<=21 candidate. It becomes directly relevant if extended to non-parity dark rooms or combined with a proved classification/reduction to parity folds. Neither extension is established. Moreover the axis-neighbor270degree rule relies on non-A points being actual corners; transparent exceptions remove that premise in the unknown class.

The global isolation/degeneration program remains open. Its sufficiency for a finite normalized-lattice reduction is not a proved equivalence. Nothing here settles all polygon directions or arbitrary mark classes outside the canonical45/interior-A setup.

## 3. Audit of the requested fixed ring-subset analysis

I independently parsed the327frozen room/event/functional files, using Fraction rather than eval, and recomputed the selected rows. Numerical QR restriction, rank tolerance1e-7 and floating linear programs reproduce:

| Selected event corners | Numerically certifying rooms |
|---|---:|
|Both8-neighbor rings|327/327|
|Both axis-neighbor sets|293/327|
|Both diagonal-neighbor sets|43/327|
|Source ring only|72/327|
|Target ring only|35/327|

The axis rows have full rank in327/327. Each of the34positive-cone holdouts is numerically repaired by adding one diagonal corner's events. The actual eight axis neighbors are distinct genuine270degree corners in every saved room;2616exact corner-angle checks PASS.

This corroborates the scripts' empirical claim. These subset LPs are numerical, not new exact rational positive-span certificates. The earlier full-family exact certificates do not automatically certify a selected subset. No new geometry, optical directions or reflection words were discovered.

### Corner/wall decomposition

For the exported event convention, A=T'-s=2w and C=c'-s=w. Then

    g(delta)=sigma*d cross(A,C)=sigma*cross(w,2delta C-delta A).

Writing C=R_C*c+b_C-s and A=R_T*t+b_T-s gives

    g=sigma*cross(w,2R_C delta c-R_T delta t-delta s
                      +2delta b_C-delta b_T).

If w is the primitive half-direction, the corner-only coefficient has a factor2. If the peer's w denotes A instead, that factor is already included; specify the convention.128exact central-difference controls pass. Incident wall offsets determine delta c, so the corner motion is not an independent variable in the room chart. The wall terms remain coupled to the global word.

Raw direction spread is insufficient for signed positive span: choosing signs by a half-plane can put all signed rotated directions into one half-plane even when the original directions cover every angle. Thus mark-isolation reasoning alone cannot supply the missing coupled sign theorem. The peer's subsequent corner-part failures are consistent with this warning, but that new re-export was not independently audited here.

## 4. A sharper bound removes the apparent new k5 support branch

Use the accepted identities at W<=21:

    I<=floor((15+2k)/6),
    P+m<=floor((21-4I+2k)/2),
    N<=floor(4(19+2k)/3).

At k5 the coarse I bound is4. But for I4 the second bound is P+m<=7. Every full-cell external axis neighbor is either a partial occupied cell or a missing required neighbor, so its count b obeys b<=P+m.

**Four-cell lemma:** every four-point set F in Z^2 has b=|neighbors(F)-F|>=8.

Here is a complete finite proof. Every nonempty set has at least4external neighbors (one beyond each coordinate extremum, all distinct). Join full points at Manhattan distance<=2. Different graph components have disjoint external-neighbor sets. Thus a hypothetical b<=7 set has only one overlap component. Root one point at0; the other three lie in the Manhattan radius6 diamond, since a spanning path has at most3edges of length2. Exhausting all95284choices of those three points is therefore complete. Exactly1564are overlap-connected, and every one has b>=8. The b8 configurations have36rooted listings,3classes under grid symmetries/translations. Output and exact support code are in `check.json` and `check.py`. This proof is computer-assisted. Claude independently accepted it by growing all 391 translation-normalized connected four-sets, obtaining the same 1,564 rooted sets and minimum boundary eight.

Consequently I4 is impossible at k<=5,W<=21, leaving I=2,3. The new caps are:

| k cap | I2: P+m | I3: P+m | I4: P+m | N cap |
|---:|---:|---:|---:|---:|
|4|10|8|6|36|
|5|11|9|7 (impossible)|38|
|6|12|10|8|41|

The k5 I2/I3 caps11/9 are exactly the old conservative W<=23,k4 support caps. Therefore the already independently reconstructed22supports and31nonadjacent marked pairs cover W<=21,k<=5. The triangle/cell universe, outside-cell budget and cardinality caps must be regenerated for k5; blindly reusing the stronger old W21,k4 constraints would be unsound. The parameterized encoder computes these from wmax,kmax already.

This is support coverage, not a five-exception exclusion. It directly reduces the next missing bounded case and does not require any new ray discovery.

## 5. Five-exception continuation

The original 21-wall pilot residual is independently LIT: the supplied 44-reflection witness passes exact Codex verification. Its universal guard has 20 required-used and 12 required-absent triangles. The original packet is frozen under `../k5-proof-pilot/inputs/pilot/`.

Daniel approved the full 31-case proof pass. Regenerated five-exception models yield 21 checked UNSAT proofs and ten unresolved geometric residuals, with no timeouts. The known 22-wall dark room remains allowed at W22,k5, including the new guard. Full table, receipt bindings and coverage are in `../k5-proof-pilot/findings.md`; no complete k5 exclusion is claimed.

A useful implementation advance extracts a rational direction directly from a successful labeled-origami orbit state. On the old pilot it yields a 14-reflection path in direction (−1,6), with exact physical replay and mixed-shear controls. This avoids a separate direction scan; it does not eliminate the ten remaining residuals by itself.

## Next move

Claude classifies the ten stable residual packets. Independently verify each fixed connecting witness, derive a universal guard, and resume affected proof branches while preserving each input generation. Keep the non-parity classification and global degeneration gaps explicit.

## Completed continuation

The k≤5,W≤21 branch is now closed: all31markedcases have accepted machine-checked refutations. The full17,868newguard library passes independent exact physical and universal checks; known22control remains allowed. See `../k5-proof-continuation/findings.md`, `certified-summary.json` and `manifest.json`. The closest-mark certificate uses its standalone replacement. Remaining live-peer I2replays do not change the local completed receipt total. The next bounded frontier is k=6; unrestricted reduction remains open.
