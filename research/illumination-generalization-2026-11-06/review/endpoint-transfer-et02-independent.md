# ET02 independent challenge

Preliminary source status: author candidate-02.md read in full; final argument/request not yet present at review start. Decisions below are independently established for the explicitly supplied raw geometry, not acceptance of an unseen final packet. No author checker was executed. Own prescribed Fraction replay: endpoint-transfer-et02-independent.py/.json.

## Claim decisions

| Claim | Decision | Evidence and scope |
|---|---|---|
| Supplied polygon is strictly simple, orthogonal and has 14 maximal walls and r=5 | ACCEPT | Exact nonadjacent closed-segment disjointness and signed-turn audit; positive area 4724. No adjacent collinear walls. |
| S=(60,20), T=(20,60) are distinct actual interior even-even marks | ACCEPT | Exact interior parity; neither mark on any wall; integral even coordinates. |
| Direct S-to-T chord is degenerate only at C=(40,40) | ACCEPT | Both directed half-chords have their first boundary contact at C, with parameter 1/2; the other portions lie in the interior. |
| Some actual smooth wall always gives a one-reflection repair for every such pair in r<=8 | REJECT | Exhaustive actual-wall reflection table below fails on this qualifying r5 room. This is a finite analytic counterexample, not inference from a bounded direction search. |
| Proposed two-reflection route reaches actual T legally | ACCEPT | Complete actual first-hit and signed-specularity audit of S→(160/3,40)→(40,0)→T. |
| This is darkness or a refutation of all multi-reflection transfer | REJECT if asserted | The supplied actual pair is lit with exactly two reflections. Author candidate explicitly avoids this overclaim. |
| Failure entails at least nine distinct physical reflex corners | REJECT if asserted | This obstruction to one-reflection availability occurs at five reflex corners. No global darkness/rank/cycle conclusion follows. |

## Exhaustive hand algebra for all one-reflection words

For a horizontal support y=h, reflect the ACTUAL T to (20,2h-60). The only possible smooth reflection has developed segment parameter u=(h-20)/(2h-80) and contact (60-40u,h), when the denominator is nonzero. A legal one-reflection path requires 0<u<1, strict membership in the finite mirror, and unimpeded incoming/outgoing segments. For a vertical support x=k, the image is (2k-20,60), u=(k-60)/(2k-80), contact (k,20+40u), with the same strict requirements. Zero denominators here give parallel distinct supports, not an overlooked continuum of contacts.

Number walls 0 through 13 in the supplied boundary order.

| Wall | Support | Candidate contact / parameter | Decisive failure |
|---|---|---|---|
| 0 | y=0, x in [0,49] | (50,0), u=1/4 | Outside finite mirror |
| 1 | x=49, y in [0,19] | u=-11/18 | Negative first flight |
| 2 | y=19, x in [49,51] | (1240/21,19), u=1/42 | x>51 |
| 3 | x=51, y in [0,19] | u=-9/22 | Negative first flight |
| 4 | y=0, x in [51,80] | (50,0), u=1/4 | Outside finite mirror |
| 5 | x=80, y in [0,40] | (80,30), u=1/4 | Outgoing leg hits actual wall 6 at (60,40) before T |
| 6 | y=40, x in [40,80] | Both developed endpoints at y=20 | Parallel; no support contact |
| 7 | x=40, y in [40,80] | Both developed endpoints at x=60 | Parallel; no support contact |
| 8 | y=80, x in [0,40] | (30,80), u=3/4 | Incoming leg hits actual wall 6 at (50,40) first |
| 9 | x=0, y in [51,80] | (0,50), u=3/4 | Outside finite mirror |
| 10 | y=51, x in [0,19] | u=31/22 | Negative second flight |
| 11 | x=19, y in [49,51] | (19,1240/21), u=41/42 | y>51 |
| 12 | y=49, x in [0,19] | u=29/18 | Negative second flight |
| 13 | x=0, y in [0,49] | (0,50), u=3/4 | Outside finite mirror |

Every possible single smooth reflection belongs to exactly one of these finite walls and must obey the actual-target image identity. Contacts at true vertices are forbidden; no rejected equality is silently accepted. These are all supports of the actual room, not merely candidate corridor floors. Thus the stronger one-wall claim is false without asserting any bound on longer words.

## Positive two-reflection witness

At Q1=(160/3,40), the incoming displacement is (-20/3,20). Reflecting at the actual horizontal wall gives (-20/3,-20), positively proportional to Q2-Q1=(-40/3,-40), with factor 2. At Q2=(40,0), reflect that displacement to (-40/3,40); T-Q2=(-20,60) has positive factor 3/2. One common speed can therefore be assigned throughout.

Q1 lies strictly inside wall 6 and Q2 strictly inside wall 0. For the first two legs, each declared contact is the unique earliest boundary intersection, strictly in its wall interior. For the final leg the next boundary intersection occurs strictly after the actual T. The exact checker tests all 14 walls on every leg, so both thin notches and both sides of the inner corner are included. Neither earlier leg contains actual T. This validates endpoint identity, signed direction, positive times, true-corner avoidance and actual first target arrival.

The initial direction and reflection word change. This does not contradict the fixed-exterior two-sector obstruction. The route contains a nonincident floor reflection, consistent with the independently submitted remote-contact necessity. The first contact is on a wall incident to C; no new reflex vertex is visited or charged.

## Remaining implication

ET02 rules out a proposed universal ONE-reflection edge class. It supplies no complete replacement relation for arbitrary words or strict root-free intervals. A multi-reflection transfer needs proved physical availability and all actual endpoint/first-hit guards before a rank or a cycle argument applies. Neither five nor nine is a darkness threshold proved here.
