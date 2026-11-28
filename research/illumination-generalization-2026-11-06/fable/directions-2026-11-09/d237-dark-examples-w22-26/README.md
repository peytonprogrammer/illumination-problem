# d237: dark examples at W = 22 to 26 on immersed discs (approved by Daniel, 2026-11-26 09:23 HST)

Advances: L1 (tests the statement "dark implies fold", which with d52 gives the goal without an area bound). No lemma is claimed.

Payoff sentence: if a dark pair at W = 22 to 26 has no fold certificate, darkness has a second mechanism and "dark implies fold" is false as stated. If every dark pair found is fold-certified, the corpus of dark examples grows from about three to the number found, and "dark implies fold" becomes the theorem to target.

Prior work: d9/d29 (embedded rooms, W <= 24, area <= 19: one dark room, the 22-wall room, area 15); d55 (slit and pinched rooms: 5 dark pairs in 12.7 million, all fold-certified; certs.py); d52 (fold enumeration: at r = 9 exactly one fold-positive room with a delta >= 3 class); d30/d31 (W = 28 glued-copy room); d236 (pipeline and class definition; no dark pair at W <= 20, area <= 16).

## Class

The d236 class (d236-immersed-disc-control/README.md, section "Class"), with W in {22, 24, 26} and F <= 16. All three buckets are in scope: EMBEDDED, TOUCHING, OVERLAP.

## Gates

- G1: the pipeline finds the 22-wall room's pair DARK inside the census itself (EMBEDDED, W = 22, area 15), and no other dark pair among EMBEDDED discs with W <= 24. This must match d9/d29.
- G2: counts by (area, W, bucket) for W = 22 to 26 match the independent validator through area 11.
- G3: pilot at area <= 13, then forecast. If the forecast for area <= 16 exceeds 60 CPU-min, stop and report.
- A DARK verdict needs a complete orbit (FULL) and an independent reproduction with the validator's decider. CAP or a crash is UNDECIDED.
- Fold test: every dark pair goes to a certificate check (Theorem U, d55 certs.py adapted to abstract complexes). The verdict per pair is CERTIFIED, UNCERTIFIED, or CHECK FAILED. The certificate check is a second stage; it starts after the dark list is fixed.

## Predictions (written before any run)

- P(at least one dark pair besides the 22-wall room's) = 45%.
- P(some dark pair is UNCERTIFIED) = 5%.
- Guess: between 1 and 20 dark pairs in total.
- P(production inside 60 CPU-min) = 75%.

## Stop result

Stop after area 16 and the certificate stage. An UNCERTIFIED dark pair: reproduce it independently, then report to Daniel before any follow-up. Extending to area 17 or W = 28 needs a new approval.

## Outcome (2026-11-26 09:49 HST)

One dark pair, the known one. Among 8,741,965 immersed discs with W = 22, 24 or 26 and area <= 16 (5,748,169 EMBEDDED, 2,416,984 TOUCHING, 576,812 OVERLAP), 1,015,031 pairs of marks were decided by complete orbit. 1,015,030 are lit. The one DARK pair is the 22-wall room's pair (area 15, EMBEDDED, 2,592 states). 0 undecided. Production: 9.7 CPU-min (astra/README.md).

Gates: G1 PASS (the census itself rediscovers the 22-wall room's pair and no other dark embedded pair, matching d9/d29). G2 PASS, but thin: only 2 nonzero rows through area 11; the coordinator added area 12 (8 rows, 0 mismatches, validator 180 CPU-s). G3 PASS.
Coordinator cross-check (crosscheck.py, 2 CPU-s): 556 sampled production discs decided with the validator's unfolding and decider: 648 of 648 pairs lit. The dark disc: DARK, 2,592 states, complete. (My first cross-check matched the dark disc by a prefix and picked another disc; fixed to the exact line.)

Certificate stage: not run. The only dark pair is the 22-wall room's, whose fold certificate is already known. Nothing new to certify.

Predictions scored: at least one new dark pair (45%): FAILED, none. An uncertified dark pair (5%): none, held. Between 1 and 20 dark pairs: 1, held at the edge. Inside 60 CPU-min (75%): held.

Status: COMPUTED, cross-checked by a second implementation (counts through area 12, lighting on a sample and on the dark disc). Not reviewed.

Reading: the corpus of dark examples didn't grow. With d236, the 22-wall room's pair is the only dark pair among all immersed discs with W <= 26 and area <= 16. So this range holds no test of "dark implies fold" beyond the one example it already rested on. Darkness is isolated, not rare-but-present. The stop result applies. Larger area or W >= 28 needs a new approval.
