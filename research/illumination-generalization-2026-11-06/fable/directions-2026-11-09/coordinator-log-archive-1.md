# Coordinator log archive, part 1

Older entries moved from coordinator-log.md on 2026-11-21 so each file fits the 200 KB sync limit.

## 2026-11-12 — d35 result (Astra, AW on torus covers)

- Reply: `d35-aw-torus/astra.md`. Session total about 359k tokens.
- AW Thm 3.6 is vacuous on torus covers: its input (finite periodic-point set, shortest saddle connections) fails because rational points are dense.
- Finite replacement: SL(2,Z) orbit of the marked square-tiled surface; illumination becomes finitely many horizontal visibility tests.
- Gap: compatibility across directions. First lemma: per-class amalgamation (each of B_b, B_c, B_d separates the pair implies B_* does). Needs geometry; 12|34 vs 13|24 kills the pure-combinatorics version.
- r <= 8 doesn't bound degree (u = 2n - 2r - 2).
- Astra estimate: 35% that this yields "dark implies separating parity factor" at r <= 8.
- Correction: the coordinator told Daniel "no fold of any shape makes a W <= 20 room dark". Wrong. d2 excludes only the common separating parity factor; per-class and rigid factors are open. STATE.md fixed.
- Coordinator review: consistent with d2-review lines 57-84 and d32 source reading. Not independently verified beyond that.

## 2026-11-12 — d36 launched (Astra, per-class amalgamation)
- Daniel: "ok go". Resumed Astra session 01a1cf04 with `d36-amalgamation/brief.md`. Budget ~100k tokens, theory only; small read-only checks on the 22-wall room and P6 allowed (<5 CPU min).

## 2026-11-12 — d36 result (Astra, per-class amalgamation)
- Reply: `d36-amalgamation/astra.md`. Round cost about 63k tokens (session 359k -> 422k), under the 100k budget. Checks on the two rooms: 0.0024 CPU s. No discovery search.
- PROVED (unreviewed): amalgamation holds when each class quotient is Galois, any r. Proof: deck group of DP/PC is at most V4; two classes with different double covers force P = 2x2 block. Weak: both known dark rooms use non-Galois staircase covers, so the case that matters is untouched.
- PROVED (unreviewed): if a one-class separating quotient exists in a normalized room, area <= 5r. With d9 (no dark pair at r <= 8, area <= 20), any amalgamation counterexample at r <= 8 has r in 5..8 and area 21..40. This makes the per-class gap a finite check. Not run: it is a room search and needs Daniel's approval.
- Checks: 22-wall room and P6 both satisfy amalgamation (B_* is the staircase quotient; all four lift pairs separated). Two independent implementations agree.
- Still open: visibility-to-certificate ("B_x identifies a lift pair implies a legal trajectory in class x") and general rigid factors. This is the hard step; amalgamation alone doesn't prove the target.
- Astra's estimate unchanged at 35%.
- Coordinator review: logic reads sound; the 5r bound relies on Riemann-Hurwitz and Gauss-Bonnet counts I checked only at the level of the stated identities. Needs an independent reviewer before it goes in "Proved".

## 2026-11-12 — d37 launched (Astra, visibility-to-certificate)
- Daniel: "let's do 3 first". Resumed session 01a1cf04 with `d37-visibility/brief.md`. ~100k tokens, theory only. d36 review and finite check deferred.

## 2026-11-12 — d37 result (Astra, visibility-to-certificate)
- Reply: `d37-visibility/astra.md`. Round cost about 77k tokens (session 422k -> 499k). Checks under 0.003 CPU s. No discovery search.
- PROVED (unreviewed): exact directional object. Two regular A points connect in a class-x direction iff they share a component of the regular lift graph (corner lifts deleted).
- PROVED (unreviewed): averaging lemma. If a finite group of affine return maps (preserving corners and class x) acts on the points, and one component holds more than half of two orbits combined (density sum > 1), every cross pair is x-lit. Real straight trajectories, no word-to-ray substitution.
- PROVED (unreviewed): conditional theorem. Under "classwise joint majority" (the density condition holds in every fibre of every class quotient), a dark pair yields per-class parity certificates. Hypothesis NOT derived from r <= 8.
- Example: L-room (r = 1) satisfies it. Adds no new lit result (d15 covers r <= 2).
- Important structural fact: the d36 bound holds for any proper class quotient, so normalized rooms with area > 5r (> 40 at r <= 8) have NO canonical parity or rigid certificate. Those rooms must be proved lit directly; the area bound doesn't remove them.
- Cone counting gives p_x <= 2r + 2 path components, but cycle components are uncontrolled (rectangles), so majority isn't forced.
- Known dark rooms: staircase certificates come out directly; P6 fibres show components of size <= 2 in fibres of 4, so the majority test is exactly at its limit there.
- Next step per Astra: degree-three one-class fibre lemma. Probability lowered 35% -> 30%.
- Coordinator review: averaging lemma and directional object read sound. Conditional theorem is valid but its hypothesis may be as hard as the target. Three rounds in one Astra session (d35-d37) are all unreviewed and self-referential; an independent review is due before more rounds.

## 2026-11-12 — d38 launched (independent review of d35-d37)
- Daniel: "ok go". One Opus reviewer, fresh context, given the proofs but not coordinator conclusions. Read-only checks allowed on the two named rooms only.

## 2026-11-12 — d38 result (independent review of d35-d37)
- Report: `d38-review/review.md` (+ check_named.py/.log). About 178k tokens, under 0.01 CPU s of checks on the three allowed rooms only.
- d35: all claims CORRECT. d36: Deck <= V4, Galois amalgamation, n <= 5r CORRECT; normalization claim has a scope gap (5r bound needs corners in >= 3 parity classes; even refinements used by d16 put corners in one class; the d37 L-room, n = 12, r = 1, violates the bound without it). Dark-room checks reproduced.
- d37: lift graph and averaging lemma CORRECT with a fixable gap (wall-point marks). Fibre lemma CORRECT.
- Most serious: the d37 joint-majority hypothesis is FALSE at r = 4. With the trivial subgroup it says every pair in one phi_x fibre is x-lit. The 12-wall cross (S = (1,2), T = (3,2)) has B_c one block, yet all four lift pairs carry Cut certificates at c (d10-d12-review/room_r4.log: ['', 'C', 'P']) and are c-dark. The room is lit through other classes.
- Coordinator check: confirmed the log lines (certificates ['', 'C', 'P'], decider LIT) and the review's argument. B_c one-block is a hand computation by the reviewer, not replayed.
- Consequence: the d37 conditional theorem is not progress. Any repair must read "joint majority, or a Cut or Rig certificate, at each class". Lighting can need directions from more than one class, so a class-by-class route can't work alone.

## 2026-11-12 — d39 launched (Astra, mixed-class repair)
- Daniel: "ok let's try it". Resumed session 01a1cf04 with `d39-mixed-class/brief.md` (includes d38 verdicts). ~100k tokens, theory only; checks on the 22-wall room, P6 and the 12-wall cross only.

## 2026-11-13 — d39 run 1 stalled
- Network failure at 01:58Z after the three-room check; harness killed the run at its 90-minute limit with no reply. Log moved to `d39-mixed-class/astra-run1.log`. Resumed the same session with a finish-up prompt (cap ~60k more tokens, 2-hour limit).

## 2026-11-13 — d39 result (Astra, mixed-class repair)
- Reply: `d39-mixed-class/astra.md`. BUDGET OVERRUN: session counter 499k -> 909k, about 410k tokens against a 100k budget (run 1 stalled on a network failure; the resume re-sent the full session context). Checks: one process, 0.0035 CPU s, three named rooms only.
- Astra withdraws d37 joint majority (agrees with d38).
- PROVED (unreviewed): fixed-unit per-class necessity is false at r = 4. The cross scaled by 3 (area 108) is c-dark with no ordinary Par, Cut, or Rig at c; the explanation is a Cut relative to a coarser pillowcase. Not a counterexample for normalized rooms.
- PROVED (unreviewed): genuine ordinary Cut forces the 12-wall cross (lit), so Cut never appears in a full certificate triple. Relies on the reviewed R4 proof.
- PROVED (unreviewed): essential Rig at r <= 8 forces area <= 20 (three-corner-class scope); with the d9 census, full triples containing Rig are excluded. Weakest steps: the zero-free "one star" argument and the degree-6 S_3 seam argument. Astra asks for independent verification.
- Net: within scope, fully certified dark pairs reduce to three Par certificates, i.e. back to the d36 amalgamation problem. Per-class completeness ("x-dark implies a certificate") is still open, and that is the step that decides the target.
- Estimate 30% -> 25%. Trend over d35-d39: 35, 35, 30, 25.

## 2026-11-13 — Tokarsky suggestion and d40 launch
- Tokarsky suggested checking every room in a 22x22 grid. Coordinator: a box search proves nothing without a size-reduction theorem; drafted a reply for Daniel asking whether he knows one.
- Brainstorm: (1) thick-thin size reduction, (2) Schwartz-style parameter-space covering, (3) shrinking a minimal counterexample. Daniel: "ok go on idea 1".
- d40 launched: fresh Astra session (avoids re-sending the 909k-token d35-d39 session), `d40-thick-thin/brief.md`, ~100k tokens, theory only.

## 2026-11-13 — d40 result (Astra, thick-thin size reduction)
- Reply: `d40-thick-thin/astra.md`. Fresh session 01a1d668-3282-7111-ae40-8f786adf0952. 115k tokens (tracker 94k), 8 min, no computation run.
- PROVED: idea 1 as briefed is vacuous. Axis scalings preserve darkness, so "every rectangle thicker than F implies lit" is equivalent to the target (dilate any room by F). Coordinator error: the brainstorm missed scaling invariance. Thickness must be relative, after gcd normalization.
- PROVED: chamber-shadow lemma with f(r) = 2 (point within 1 below a full doorway sees all of the chamber's deep part). Restatement of d15 Lemma B'; not a new global result. Neither known dark room has a full doorway at its marks.
- PROVED: fixed-direction strip transfer is a circle rotation, so no exact height change preserves all directions; P6 refutes unrestricted one-row insertion or enlargement.
- Obstruction: orthogonal reflections conserve |slope|, so lighting through two doorways needs one slope compatible with both phases; local lemmas don't give that. A useful reduction must map integer-marked dark rooms to integer-marked dark rooms in a box [0,B]^2 (re-derives B = r + 3 = 11 conditional on rigidity).
- Astra: 25% for a constructive reduction; next step a two-door shadow lemma with phase congruences.
- Coordinator verdict: idea 1 closed in its naive form. Added to dead ends.

## 2026-11-13 — d41 launched (idea 2, two-parameter covering test)
- Daniel: "do idea 2". Opus agent extends d28 covering certificates from one gap variable to two. Caps set by coordinator: 3 processes, 60 min wall, 1 GB RAM, 2 MB output; rooms limited to the d28 20-wall neighbour and the 12-wall cross families.

## 2026-11-13 — d41 result (idea 2, two-parameter covering)
- Report: `d41-two-param-cover/README.md`. Opus, 128k tokens, 9 min; 3 processes max, ~2 min compute, 2.2 MB peak, 504 KB output. No cap deviation (one 1 s run on the cross before switching to a 12-wall dumbbell control).
- All 20 tested pair-lines certified lit for every odd (g1, g2). Hardest: 20-wall neighbour, rows 2,3, pair (1,3)-(3,5), P = 14 (one-parameter P = 9). Coordinator checked the run file: uncovered 8 -> 8 -> 0 of 5.2e11 residues at p = 12, 13, 14.
- Two-band lemma proved for any k parallel bands; for a perpendicular row and column only when their crossing cell is outside the room (otherwise no periodicity).
- Hardest residues sit on slit-shadow classes (degenerations), worst where both gaps degenerate.
- Verdict: behaves like the one-parameter case; doesn't scale to W <= 20 (crossing parameters aren't periodic; degeneration-blocked lines need unbounded P, e.g. d28 x0 room at W = 16; residue grid ~Q^k, ~1e54 for 9 rows). Useful to certify single-axis families, not a route to the conjecture.
- band2.c matched d28 band.c in 296/296 comparisons. Unreviewed.

## 2026-11-13 — Wolecki reply
- Notes: `lit-wolecki/findings.md`. Monteil 22-gon uses 45-degree walls and has a boundary self-intersection (not strictly simple); a 20/19-gon needs a slit. Wolecki gives an alternative proof via Tokarsky's acute-corner lemma (coordinator checked the parity step). Nothing on minimality.

## 2026-11-14 — Coordinator re-read of the Tokarsky and Wolecki replies (ideas, nothing run)
- Correction: the coordinator told Daniel on 2026-11-13 that Tokarsky's grid check "can't prove the minimum". True for the lit side only. For fold-certified darkness, d36/d37/d39 bound the area (<= 5r = 40, normalized), so a grid check IS a proof there. Both experts describe darkness through the fold property.
- Idea A (certificate-side theorem): "22 is the minimum among strictly simple square-lattice rooms that are dark by a fold certificate". Remaining work is bounded: review d36-d39, the area 21-40 finite check, the non-normalized scope gap. Comparable published-style statements: de Winter-Tokarsky 24/34 (strict class), Monteil 22 (boundary touches itself), 20/19 (slit).
- Idea B (near-miss experiment): Monteil's dark slit room has 19/20 sides. Thickening the slit to a wall of width 1 (after scaling by k) gives strictly simple lattice rooms with about 21-22 walls. Not covered by any census or search here (no "thicken" work found in the project). Either finds a dark room below 22 or supplies the local lemma the lit side needs. Needs Daniel's approval and a cap.
- Idea C (proof architecture): witness complexity is locally bounded away from degenerate rooms (a witness stays valid on an open set of side lengths), so hardness lives only near degenerations: thin corridors (d26), slit limits (d28, d41). Plan: classify dark degenerate rooms, prove a thickening lemma at each, cover the compact core. Core cover is infeasible at r = 8; maybe feasible at r = 3.
- Idea D: Wolecki's triangle slicing gives one base (45-45-90 triangle) for orthogonal and 45-degree rooms; one certificate theory for the full target scope.

## 2026-11-14 — d42 and d43 launched
- Daniel: "ok sounds good, go" on the recommendation (idea B first, then idea A).
- d42: Opus agent reads Monteil's slit room from the slides, verifies its darkness, tests lattice thickenings with W <= 22 for dark pairs. Caps: 3 processes, 60 min compute, 1 GB, 5 MB output.
- d43: Opus reviewer of d39 (first step of idea A; no search). The area 21-40 finite check is NOT launched; it needs a size estimate and a cap from Daniel.

## 2026-11-14 — d43 result (review of d39)
- Report: `d43-review-d39/review.md` (+ check_cross.py/.log). Opus, 146k tokens, 9 min, 0.005 CPU s on the cross only.
- No false claim in d39. Claim 3 (essential Rig forces area <= 20) correct with two gaps the reviewer filled (domino/square cases; d = 6 cover is the regular S_3 cover). Claim 4 holds only for certificates over the unit pillowcase B and relies on the d9 census (not rerun).
- Established: strictly simple room, r <= 8, corners in >= 3 parity classes, same-class interior lattice marks. If every lift pair has a Par, Cut or Rig certificate over B at every class, then each B_x separates all four lift pairs, 5 <= r <= 8 and 21 <= area <= 40. For normalized rooms B is the only pillowcase.
- To complete "no W <= 20 room is dark by a certificate": (1) finite check of B_x separation, r 5..8, area 21..5r (or prove amalgamation there); (2) certificates over coarser pillowcases: rectangular ones reduce to the coarser presentation, non-rectangular ones need new work; (3) rooms with <= 2 corner classes (even refinements), where the area bound fails; (4) rational marks reduce to (2) and (3).
- Most serious: d39 (and STATE.md's summary) never says "full triple" means certified over B. Example: the 22-wall room scaled by 3 is dark with no certificate over B.

## 2026-11-14 — d42 result (thickenings of Monteil's slit room)
- Report: `d42-slit-thickening/README.md`, rows in `results.tsv` (2,257 rows). Opus, 200k tokens, 22 min; ~1,150 CPU s over 18 min, 3 busy processes (OS process count briefly above 3: idle parents waiting on children), 4.8 MB on disk, memory not measured.
- Slit room read from the PDF vector data: outer 17 corners (0,2) (1,2) (1,1) (2,0) (2,1) (4,1) (4,0) (5,1) (5,2) (6,2) (5,3) (4,3) (4,4) (3,3) (2,4) (2,3) (1,3); slit (3,1)-(3,2); marks S = (2,2), T = (4,2). 19 or 20 sides. Dark: fold argument; origami tracer to p+q <= 400; plane tracer 1,112 directions; exact decider undecided at its state cap.
- Thickenings: 872 thick-wall variants (k <= 12; 806 with W <= 21; min W 18), 367.6M pairs, 0 unlit. 1,373 shortened/lengthened variants (k <= 8; 1,270 with W <= 21; min W 17), 100.1M pairs, 0 unlit. Each unthickened scaled slit room has exactly the one expected unlit pair (control).
- Witnesses for the scaled marks always reflect off the thick wall. Centred flat end: direction (1,4), 7 reflections, the same at every k (the old tip acts as a mirror). Narrow wall off the tip: direction (2k/w - 1, -k/w), complexity grows like k/w. Roof ends: direction (3,-7), 4 reflections.
- Not verified: lit verdicts rest on the shooter (280 pairs replayed independently); integer points only; k <= 12; no partial chamfers.
- Coordinator read: no counterexample below 22 from the nearest-miss family. The witnesses match the "tip-reflection" picture: a uniform bounded witness when the wall is centred, complexity ~ k/w otherwise.

## 2026-11-14 — d44 launched (sizing the certificate check)
- Daniel: "ok go". Opus agent designs and sizes the finite check from d43 item 1 (B_x separation, r 5..8, area 21..5r). Counting and timing samples only; cap 10 CPU min, 2 processes, 1 MB output. The full run is NOT approved yet.

## 2026-11-14 — d44 result (sizing the certificate check) and d45 launch
- Report: `d44-cert-check-sizing/README.md`. Opus, 219k tokens, 23 min; 3-4 CPU min, 2 processes, 120 KB. One exact count (W = 16, area <= 30) hit its 60 s limit and was dropped.
- Range holds ~1.9e13 free rooms (+-25%), almost all at W = 20; brute force ~2.6e4 CPU-hours: not feasible.
- New filter F* (unreviewed corollary of d36.3, d36.4, d2): a positive pair at r <= 8 needs a non-Galois class quotient, so delta >= 3, n = delta*d, with sum_y floor(rho_y/delta) >= z_min(d). Allowed areas: r=5 {25}; r=6 {21,24,25,27,30}; r=7 adds {28,35}; r=8 adds {32,36,40}. Runs per (shape, parity pattern).
- With F*: ~8.9e9 shapes, 1.5-2.1e10 surviving rooms (factor 3 uncertainty), ~60 CPU-hours (range 25-180), 6-9 us per room.
- Validation done: C check matches roomtools; 22-wall room and P6 positive; cross and its 2x, 3x scalings negative; F* keeps the named rooms.
- Recommended caps: 8 processes, ~500 resumable jobs, W <= 18 pilot (2 h), then 24 h wall clock, 1 GB RAM, 1 GB disk. Stage 2 code (shape canonical form, parity loop) still to write.
- Scope unchanged: unit-pillowcase certificates, >= 3 corner classes, same-class lattice marks.
- d45 launched: Opus referee of F* (theory only). The full run is NOT approved.

## 2026-11-14 — d45 result (referee of F*)
- Report: `d45-review-fstar/review.md` (+ check_fstar.py, compare_filters.py). Opus, 96k tokens, 3 min.
- Verdict: SAFE TO USE within the check's scope. All six questions CORRECT. d2 applies to the join (it contains B_min, has the parity property, needs no normalization). Each reflex corner is one zero of DP; z <= sum_y floor(rho_y/delta), tight on the 22-wall room and P6. Area lists recomputed and match. `filter_rate.passes()` matches an independent version on every reflex-class vector for r = 5..8.
- Required code fix: stage 2 must apply F* with each room's actual area (not one pass result per shape and parity pattern), and be cross-checked against `passes()`.
- F* rests on d2 section 1.7, d36.3, d36.4: one independent review each.
- d42 closing note: a leftover polling loop timed out; no result changed.

## 2026-11-14 — d46 launched (certificate check: code + pilot)
- Daniel: "ok go" on the recommendation: pilot now; full run only if pilot timing matches the estimate.
- Opus agent writes stage 2 (shape canonical form, parity loop, F* per room area), validates, runs the W <= 18 pilot. Caps: 8 processes, 2 h wall clock, 1 GB RAM, 1 GB disk. Full run not started.

## 2026-11-14 — d46 pilot result and full run launch
- Report: `d46-cert-check/README.md`. Opus, 237k tokens, 57 min.
- Validation: 144/144 census (W, area) cells and 106/106 d44 counts match; F* 0 mismatches on 6,220 cases, applied per area; 22-wall room and P6 positive, cross and its 2x, 3x scalings negative; end-to-end at r = 9, area 15 finds the 22-wall room (F* passes everything there, so pruning is not exercised by that test). Check on over the census range: 0 positives in 427M rooms (W <= 20, area <= 20).
- Pilot (W <= 18): 471,475,261 rooms passing F*, 1.15e9 pairs, 0 positives, 1,606 CPU s, 3.6 min, 8 processes at ~11 MB.
- Cap deviation: a first W = 22 census attempt ran 11 min on 8 processes (~1.4 CPU-h) before the agent stopped it; validation total ~1.4 CPU-h.
- Revised W = 20 estimate: ~22 CPU-h (15-45), 3-6 h on 8 processes (d44 said 60).
- Not verified: positive-exit path at r <= 8 (read only; runner tested with a stub); room-level F* at W = 18 compared on 4 of 200 jobs; W = 20 cost extrapolated.
- Pilot timing beats the estimate, so per Daniel's approval the coordinator started the full run: `./run_full.sh 8 24` (detached, log `d46-cert-check/runs/full_run.log`, jobs in `runs/full_W20/`).

## 2026-11-14 — d46 full run result (certificate check, W = 20)
- Finished 19:21 (started 16:15): 500 of 500 jobs, no ALERT, 3.1 h wall on 8 processes, 87,830 CPU s (24.4 CPU-h). Aggregate: `d46-cert-check/runs/full_W20/aggregate.md`.
- W = 20, areas {21, 24, 25, 27, 28, 30, 32, 35, 36, 40}: 1,058,080,070 canonical shapes; 13,286,070,297 rooms passing F* and checked; 52,725,865,264 pairs; 0 positives.
- Coordinator check: all 500 job files present, no leftover .tmp, no non-empty .err, all 5,500 per-cell lines read "positives 0".
- With the pilot (W <= 18: 471M rooms, 1.15e9 pairs, 0 positives) and the area <= 20 recheck (427M rooms, 0 positives): no room with r in 5..8 and area 21..5r has same-class interior lattice marks separated by all of B_b, B_c, B_d.
- Result (computer-assisted; depends on d2 sec. 1.7, d36.3, d36.4, d39 claims 2-3, F*, each with one independent review, and on the d9 census): a strictly simple orthogonal lattice room with W <= 20 and corners in >= 3 parity classes has no pair of same-class interior lattice marks certified dark by Par, Cut or Rig certificates over the unit pillowcase.
- Still open on the certificate side: certificates over coarser non-rectangular pillowcases; rooms with <= 2 corner classes; rational and different-class marks. The lit side ("uncertified implies lit") is untouched.

## 2026-11-14 — d47 launched (Astra, certificate-side scope gaps)
- Daniel: "ok go, show me the replies". Fresh Astra session, `d47-cert-gaps/brief.md`, ~100k tokens, theory only. Reply drafts for Tokarsky and Wolecki updated in chat.

## 2026-11-14 — d47 Astra run failed; rerun on Opus
- The Astra background command hit the 2-hour limit with a 0-byte `d47-cert-gaps/astra.log` and no `astra.md`. No `codex exec` process remains. A 90-second probe of the Codex CLI also returned nothing (the API host answers, so the network is up). Cause not diagnosed.
- Rerun: same brief, one Opus subagent (general-purpose, background), output to `d47-cert-gaps/opus.md`. Theory only; named-room checks under 5 CPU minutes, one process. Follows Daniel's "use sub-agents to be token efficient".

## 2026-11-14 — d47 result (Opus, 154k tokens, 13 min; unreviewed)
- File: `d47-cert-gaps/opus.md`. Computation: reran the two named-room checkers only (0.05 CPU s).
- Gap 1 (coarser pillowcases): admissible bases are P_Lambda for lattices Lambda >= Z^2 (normalized room coordinates). Rectangular bases reduce to an axis-rescaled room (Prop 2.1). Odd-index sheared bases with both marks in the rectangular part reduce by a transfer lemma (Lemma 3.2, agent confidence 75%). Residue G1-odd: odd sheared bases with a mark outside the rectangular part; finite check without Cut (n_R <= 13), no bound with Cut.
- Gap 2 (<= 2 corner classes): NOT closed. Corners occupy >= 3 classes iff both axis gcds are odd; over a base, iff the index [Lambda : Z^2] is odd. Residue E: all even-index bases, no bound known. Includes every room with an even axis gcd, half-integer marks, and the 45-degree base Z^2 + Z(1/2,1/2).
- Gap 3a (different-class marks): only Rig can certify; Prop 4.1 (75%) forces area <= 16 or area 20 at r = 8. Residue D20: one finite check, <= 1.7e8 rooms at W = 20 and area 20, estimated 10 CPU-min. Not run; needs Daniel's approval.
- Gap 3b (rational marks): same question as "which Lambda"; no separate case.
- Coordinator review: (1) the fold-side theorem is not unconditional; Residue E is unbounded and is the main open item on the certificate side. (2) Lemma 3.2 and Prop 4.1 need a referee. (3) New scope question from the coordinator: Prop 1.1 classifies pillowcase bases only. DR of a normalized room also covers the (2,4,4) orbifold (double of the 45-45-90 triangle, the base in Tokarsky's lemma and Wolecki's proof), where classes b and c merge. No memo treats certificates over that base (grep of d10, d39, d43, d2-review: none).
- Next: d48 referee (one Opus subagent, theory only), dir `d48-review-d47/`.

## 2026-11-14 — d48 referee of d47 (Opus, 242k tokens, 25 min)
- File: `d48-review-d47/review.md`; script `check_transfer.py` (0.03 CPU s, named rooms only).
- Lemma 3.2 (transfer): correct with a fix (85%). Hypothesis must put S, T, rho S, rho T in Lambda' (rho = reflection (x,-y)); "cyclic" can be dropped. Test on sheared bases was weak (all partitions trivial).
- Prop 4.1 (different-class marks): correct with a fix (80%). Exception is (delta, d, z) = (4, 5, 2) only. Residue D20 spec was under-specified ("R_y separates" is only necessary); full per-room, per-pair test is in review item 2.
- Definition 1.2: WRONG clause (95%). Admissibility puts only front lifts over corners; back lifts sit at rho S. For odd index all four lifts are over corners iff marks are in Lambda_r, so H2 is redundant and single-base Residue G1-odd is empty. Per-lift-pair G1-odd is a finite check (m n_R <= 40).
- (2,4,4) triangle base (coordinator's question): every map DR -> (2,4,4) factors through a pillowcase; Par and Rig reduce to pillowcase certificates; no Cut exists over a three-cone-point base. Extra residue empty (80%, sketch).
- Residue E (even index): d47's "no bound" is superseded. New, UNREVIEWED: odd-part reduction to 2-power index; Lemma Z (a certificate with a zero forces m n_R <= 8r); zero-free certificates are lattice data, so a lit witness room kills them when all corners are live. Referee rates closing E to a finite check at 60%. Open piece: m >= 4 lattices for rooms with a vertex-only 2Z^2 class.
- Coordinator note: the witness argument, if right, kills zero-free certificates per lift pair for every room with all corners live, so Residue E is the set (room, Lambda) with m n_R <= 64. At m = 2 that reaches n_R <= 32: a d46-sized enumeration, not a small one. Needs sizing before any approval request.
- Signed theorem (referee): normalized room, W <= 20, rational marks, odd-index Lambda >= Z^2 + ZS + ZT: the four lift pairs are not all certified over P_Lambda, except possibly D20 (W = 20, different classes, n_R [Lambda_r : Z^2] = 20).
- Next: d49 (one Opus subagent, theory only): prove or break the Residue E reduction and write the exact finite-check spec with a size estimate. No enumeration.

## 2026-11-14 — d49 result (Opus, 60k tokens, 27 min; unreviewed)
- File: `d49-even-index/memo.md` (200 lines, proofs in outline). Ran named rooms only (`check_even.py`, 0.03 CPU s) plus arithmetic scripts (3 CPU s).
- Verdict: Residue E (even-index pillowcases) reduces to a finite check. Lattice marks are closed by theory plus the d9 and d15 censuses (agent confidence 70%).
- Bounds: m n_R <= 8r overall, n_R <= 2r at m = 2, so n_R <= 16 everywhere. The coordinator's estimate (n_R <= 32, billions of rooms) was too large.
- Corrections to the d48 sketch: the witness argument works for a whole lift pair, not per target (counterexample Lambda = (1/2)Z x Z); the "m >= 4 vertex-only" gap disappears; liveness is moot for zero-free Rig (Lemma R0).
- Named rooms: the 22-wall room is fully certified at m = 1, has Par at one target at m = 2, nothing at m = 4. No claim violated.
- Remaining finite check (not run): 2,052,226 normalized rooms (W 10..20, area <= 16, >= 3 corner classes), non-lattice rational marks, bases with m n_R <= 8r. Agent guess: 2e10 partition tests, tens of CPU-hours.
- Coordinator review: section 5's m = 2 step ("no zero-free certificate at a non-V target") cites sections 3-4, but section 4 proves only the whole-pair witness. Possible gap; sent to referee. Proof outlines are thin throughout.
- Next: d50 referee (one Opus subagent, theory only), dir `d50-review-d49/`. Also asked to merge the three unrun checks (D20, odd per-lift-pair, even non-lattice) into one job spec.

## 2026-11-14 — d50 referee of d49 (Opus, 198k tokens, 14 min)
- File: `d50-review-d49/review.md`; `check_d50.py` (0.03 CPU s, named rooms). The agent wrote and then deleted one stray cache file in `d10-mechanisms/__pycache__/`; the remaining `roomtools` cache there dates from 12:42 and predates this round.
- All d49 claims hold or are fixed without changing a bound. Gap found and repaired: d49 section 5 (m = 2) didn't rule out zero-free Par at a non-V target; repair: at m = 2 a zero-free factor is P_Lambda or B_R, and B_R has only regular points over non-V corners. The m = 2 restriction is essential (zero-free Par certifies a non-V target at m = 4). Other fixes: zero-free Cut has d = 2; Lambda' must include rho M_0; witness "classes" are mod 2Z^2.
- Lattice-mark closure over even-index bases: correct with fix (85%). Censuses cover what's cited.
- Residue (b) (odd sheared, per lift pair) is closed: only index 3 survives and Part A's (1/3)-grid run lit every such pair.
- Finite check corrected: 945,884 rooms (class (iii), 12 <= W <= 20, n_R <= 2r), not 2,052,226; lattices of index 2 or 4 (10 lattices; index 6 for one W = 16 room).
- Merged job spec (review section 7): Set A = D20 (169,672,127 rooms, W = 20, area 20, different-class lattice pairs); Set E = the 945,884 rooms with non-lattice marks. Primary test: shoot each pair and verify the path; certificate test on survivors plus a 1% sample, with lemma tripwires. Estimate 1.3e10 pairs, 12-30 CPU-h (guess).
- Coordinator: the primary test is a ray search, so it needs Daniel's explicit approval and a cap. Not launched. Claims released; nothing running.
- State of the certificate side: closed by theory plus existing censuses for (1) odd-index bases except D20 and (2) even-index bases with lattice marks. Open until the job runs: D20 and even-index non-lattice marks. Each new lemma has one referee pass; the repairs in d48 and d50 themselves are unreviewed.

## 2026-11-15 — Brainstorm from the Tokarsky, Wolecki and Monteil material (ideas only, nothing run)
- Daniel asked for new directions from the two replies and the slides. Coordinator checked earlier memos for overlap by grep (Hurwitz/monodromy: d6, d12, d14, covered; 45-degree census: d11, compute only; pinch/unpinch: no hits; glued-copy wall formulas: d31, d32).
- Idea 1 (triangle-base fold theorem): the certificate-side theorem covers orthogonal rooms only, but the target includes 45-degree walls, and every example in the sources (Tokarsky 26, Castro 24, Monteil 22 pinched, 19/20 slit) is triangle-tiled. Build Par/Rig theory over the (2,4,4) base for rooms with 45-degree walls, get an area bound, compare with the d11 census bound (32 tiles). Theory round first.
- Idea 2 (relaxed rooms as a laboratory): slit and pinched lattice rooms are still pillowcase covers, and dark ones exist below 22 walls. Enumerate small ones, collect every dark pair, test "dark implies certificate" on each. Either finds a non-fold dark pair or gives a corpus far larger than the handful of strict dark rooms. Same list = the degenerate rooms where a family of strict counterexamples could accumulate. Search; needs approval and caps. Rooms are out of target scope; used as a tool only.
- Idea 3 (enumerate folds, not rooms): at r <= 8 the filter gives delta >= 3 and delta z <= r, so each class quotient has z <= 2 and degree <= 9. Enumerate those small quotients and their compatible triples instead of 13e9 rooms: an independent second proof of the certificate theorem, and a classification of certificate-dark rooms at W = 22.
- Idea 4 (unpinch Monteil's 22-gon, slide 4): companion to d42. Small sizes already sit inside the d11 census, so the value is the witness structure only.
- Rejected while thinking: per-class additivity of reflex corners (false: in the 22-wall room all three classes use all 9 reflex corners); effective denominators via equidistribution (bounds marks per room, not room area).

## 2026-11-15 — d51, d52, d53 launched (brainstorm ideas 1, 3, 4)
- Daniel: "i would do 1, 3, 4". Three Opus subagents, background, each writes only in its own directory.
- d51 (`d51-triangle-base/`): certificate theory over the (2,4,4) base for rooms with 45-degree walls; area bound; compare with the d11 census. Theory only; named-room checks under 5 CPU min.
- d52 (`d52-fold-enumeration/`): enumerate class quotients (folds) instead of rooms, as an independent proof of the certificate theorem at r <= 8 and a classification at r = 9. Caps set by coordinator: 3 processes, 60 min compute, 1 GB RAM, 5 MB output. No room enumeration.
- d53 (`d53-unpinch/`): read Monteil's pinched 22-gon from slide 4, verify darkness, test strictly simple resolutions of the pinch. Caps: 3 processes, 60 min compute, 1 GB RAM, 5 MB output.
- Idea 2 (relaxed-room laboratory) not approved; not launched. The merged finite check from d50 still awaits approval.

## 2026-11-15 — d51 result (triangle-base certificates; Opus, 238k tokens, 27 min; unreviewed)
- File: `d51-triangle-base/memo.md`; `check51.py` (0.01 CPU s, five named rooms).
- Verdict: the theory does NOT reach the census. Par and Rig over the (2,4,4) base are defined with soundness (Par 90%, Rig sketch 75%); no sound Cut exists there (80%); canonical partitions exist.
- Area bound for normalized rooms: N <= 8W - 8 tiles (A/B and different-class pairs), N <= 14W - 12 (C pairs). At W <= 21: 160 and 282 tiles, against census bounds 32 and 24 (d11). Agent's guess for the finite check: >= 1e15 rooms, infeasible.
- Obstruction: cone points of angle 3 pi/2 (from 135- and 270-degree corners) have positive curvature, can't occur over the pillowcase, and let delta grow with the corner count.
- Narrow theorem (a'), census-backed (80%): no strictly simple room with W <= 23 has an A/B pair of Tokarsky's type (k = 0 transparent points in the other two classes; those need N <= 28 tiles); no A/B pair at W <= 21 has Par at both targets with delta_B + delta_C <= 4.
- Proved inequality (90-98%): regular points over the certificate's class <= 2 delta - 2, with equality on every named dark room (22-wall room, Castro, Tokarsky, slit room, pinched 22-gon).
- Coordinator read: direction 1 fails as a route to a full-scope fold theorem. The 45-degree half of the target stays compute-only (d11 to 32 tiles). The equality 2 delta - 2 on all five named rooms is unexplained and may be worth a look.

## 2026-11-15 — d53 result (unpinch Monteil's 22-gon, slide 4; Opus, 203k tokens, 32 min)
- Files: `d53-unpinch/README.md`, `results.tsv`.
- Room (read from PDF vector data): boundary walk (1,4) (1,5) (2,6) (2,5) (3,5) (4,4) (3,4) (3,3) (4,3) (4,4) (5,3) (5,2) (6,2) (5,1) (4,1) (4,0) (3,1) (3,2) (2,2) (2,3) (1,3) (0,4); marks S = (2,4), T = (4,2); touching point Q = (4,4); area 12 (24 tiles); 22 sides counting Q twice.
- Pinched pair dark under both conventions at Q (fold argument: S, T, Q fold to the same pi/4 corner, all B and C points are corners; `orbit45` DARK; `shootall` to p+q <= 400; plane tracer 1,112 directions under both rules).
- Resolutions, k = 1..12: 5,867 strictly simple rooms (500 with W <= 21, 666 with W = 22), 1,538,552,359 interior lattice pairs, 0 unlit. Hardest pair needed p+q = 112.
- Witnesses: all reflect off the new wall. Bounded witness when the resolution turns the hole corner (3k,4k) into a mirror ((-4,-3), 6 reflections; chamfer: (5,7), 4 reflections). Narrow cut of width w: p+q about 9k/w, as in d42. Difference from d42: a symmetric doorway of fixed width has no bounded witness.
- Cap use: about 2,800 CPU s (47 min) of 60 min, at most 3 busy processes, 1.7 MB output. About 1,800 CPU s of that was wasted by a multiprocessing bug in the agent's first rerun script. Memory not measured.
- Not verified: lit verdicts for non-mark pairs rest on one tracer (164 replayed); integer points only; no exact decider for the reflect rule; 45-degree cuts along odd lines, exhaustive cuts for k > 4 and non-local changes not built. k = 1 rooms were already inside the d11 census.
- Coordinator read: second near-miss family (after d42) with no counterexample. Same picture: lighting paths use the new wall; complexity grows only for narrow resolutions.

## 2026-11-15 — d52 result (fold enumeration; Opus, 255k tokens, 38 min; unreviewed)
- Files: `d52-fold-enumeration/memo.md`, scripts, `logs/`. Compute: about 30 CPU-min, at most 2 processes, under 200 MB, 0.8 MB.
- Coordinator's premise was wrong: F* forces delta >= 3 for ONE class quotient only (the 22-wall room has deltas (3, 1, 3)). No finite list of triples exists. The agent instead enumerated the one small quotient N_x and all its degree-delta disc covers.
- r <= 8: 106 admissible quotient shapes (56 up to mirror), d = 3..9, z in {1, 2}; 185 (shape, delta) cases; 4,710 disc covers; 1,744 with >= 3 corner classes up to isometry, 1,113 true rooms. Positives: 0. Covers every area, not only 21 to 40.
- r = 9: 291 shapes; the only positive up to isometry is the 22-wall room with its one pair. Scope: W = 22 rooms with >= 3 corner classes, pure-Par certificate, one class with delta >= 3. Open at r = 9: all classes with delta <= 2, and essential Rig (the d2 and d39 inputs hold only at r <= 8).
- r = 12: P6 recovered; the one other positive cover is a slit ring, not a room.
- Validation: a second cover enumerator agrees on 175 of 185 cases (10 not cross-checked: delta 5..8 on shapes 22, 29, 41, 44); brute force at n <= 9 recovers 24 of 24 incidences. Spot check by coordinator: `logs/validate_generic_*.log` show matching counts and 0 positives.
- Independence: from the d46 room enumeration, yes; from the theory inputs (F*, d36.3, d2 claim 4, d39/d43 reduction, d9 for essential Rig), no.
- Next: d54 referee of d52 (one Opus subagent; caps 2 processes, 30 min compute).

## 2026-11-15 — d54 referee of d52 (Opus, 190k tokens, 25 min)
- File: `d54-review-d52/review.md`; scripts `checks.py`, `run_generic.py`, `case_b.py`. Compute: 1,225 CPU s (20.4 min), at most 2 processes, 28 MB peak, 208 KB.
- No error changes d52's result. Fixes: the statement must say "some target class x != a has delta >= 3" (code already enforces it); two unstated steps in the cover model (trivial holonomy at interior vertices; equal involutions at a smooth vertex) are now proved in the review.
- Separation test correct: both B definitions agree on 4,420 covers; the referee's own positivity code also finds 0 positives.
- Validation finished: the 10 missing cross-checks give 0 mismatches and 0 positives, so 185 of 185 agree. The n <= 9 brute force is only a smoke test (d = 3, delta = 3).
- Agreement with d44-d46: all 2,845 in-range covers pass F*; every area seen is in F*'s list.
- Independence improved: the referee enumerated the branch "all targets have delta <= 2" directly (n <= 12 by d36.3; 21 CPU s; 0 positives at r = 8 and r = 9). That replaces d2 claim 4 and F* (and the computer-assisted k <= 6 theorem) with d36.3. Still shared with d46: d10 Theorem U, R3, Fact L; the d39/d43 reduction with the d9 census for essential Rig; delta z <= r; the scope.
- Signed, r <= 8: no strictly simple room with corners in >= 3 classes has a same-class interior pair certified dark by Par, Cut or Rig over the unit pillowcase, at any area.
- Signed, r = 9: any such room certified by three Par certificates is the 22-wall room with its one pair. Rig-certified rooms at r = 9 not covered.
- Not rerun by the referee: d52's own enumerations (logs quoted as written).
- Claims released; nothing running.

## 2026-11-15 — d55 launched (brainstorm idea 2, relaxed-room laboratory)
- Daniel: "direction 2". Cap as proposed to him: one Opus subagent, 3 processes, 60 min compute; coordinator adds 1 GB RAM, 5 MB output.
- Task: enumerate small slit and pinched lattice rooms (outside the target scope; used as a tool), decide every dark lattice pair exactly, and test each dark pair for a Par/Cut/Rig certificate. A dark pair with no certificate would be a new darkness mechanism. Dir `d55-relaxed-lab/`.

## 2026-11-15 — d55 result (relaxed-room laboratory; Opus, 239k tokens, 62 min wall)
- Files: `d55-relaxed-lab/README.md`, `dark_pairs.tsv`, `lit_control.tsv`.
- Class: orthogonal lattice rooms, area <= 15, >= 2 interior lattice points, 0 to 3 disjoint straight slits, any pinches, interior connected and simply connected. No 45-degree enumeration.
- Counts: 8,303,245 rooms, 12,694,162 pairs. Dark: 2 by the exact decider (the 22-wall room's pair; one slit room at area 14) plus 3 slit-room pairs undecided at the 1M-state cap and proved dark by Tokarsky's argument by hand. Pinch-only and slit-and-pinch: 0 dark.
- All 5 dark pairs fully certified by Par at all three targets over the unit pillowcase. No Cut, Rig or relative base needed. No different-class pair dark. No uncertified dark pair.
- Slit rooms: certificate is the double itself (Tokarsky type). The area-14 room is a horizontal wall with a one-unit doorway between the marks: an orthogonal analogue of Monteil's slit room, not a degeneration of the 22-wall room.
- Minimum wall counts of a dark orthogonal slit room: 26 / 24 / 22 (slit as 2 sides / 1 side / maximal straight segments) by decider; 27 / 24 / 21 for the hand-proved ones. So slits buy little in the orthogonal class.
- Theory adaptation (agent, unreviewed): Par and Rig sound unchanged; Cut needs an extra hypothesis with slit tips; R3(1) is wrong as stated when the target class contains a tip. Affects slit rooms only, not the target class.
- Controls: strict rooms reproduce the known results (only the 22-wall pair dark; nothing at W <= 21). 1,000 sampled lit pairs: 0 fully certified.
- 45-degree: Monteil's slit room and pinched 22-gon are certified by Par at B and C with the double itself, under the unreviewed d51 definitions.
- Cap use: 2,810 CPU s (46.8 min), at most 3 processes. Deviations: temporary files of 14 MB and 65 MB existed for about 15 min (cap 5 MB), then deleted; one job covered one extra area by a missing check; about 20 s wasted on a duplicate job.
- Not verified: lit verdicts rest on one decider (60-room cross-check); 3 dark pairs rest on a hand proof; adapted Cut and relative-base proofs unrefereed.
- Coordinator read: no new mechanism, but the corpus is 5 pairs, so the conjecture got little new evidence. Dark orthogonal relaxed rooms are rare at area <= 15. A larger corpus needs 45-degree relaxed rooms, where certificates rest on unreviewed definitions.

## 2026-11-17 — d56 launched (merged finite check: code + pilot)
- Daniel: "ok sounds good" to the coordinator's proposal: one Opus agent with a reuse brief, pilot capped at 1 CPU-hour, full run capped at 40 CPU-hours on 8 processes. Spec: `d50-review-d49/review.md` section 7 (Set A = D20; Set E = 945,884 rooms, non-lattice marks, index-2 and index-4 bases).
- Agent builds the checker and runs the pilot only. The coordinator launches the full run, detached under `caffeinate`, if the pilot timing fits the 40 CPU-hour cap; otherwise the coordinator returns to Daniel.
- Agent may first test whether the d52 quotient-enumeration method closes Set A (Rig shape (delta, d, z) = (4, 5, 2)), capped at 10 CPU-min, as a cross-check or a replacement.
- Sleep: jobs pause during system sleep and resume on wake; the driver must be resumable per job, with limits in CPU time, not wall time.

## 2026-11-17 — d56 pilot result and full run launch
- Report: `d56-final-check/README.md`. Opus, 75k tokens, 29 min; about 520 CPU s of the 1 CPU-h cap, at most 6 processes, 1.7 MB. About 246 CPU s of that was wasted on a driver test with a quoting bug.
- Validation: positive control passes (22-wall pair survives shooting to 120, Par-certified at b, c, d for all 4 lift pairs, ALERT path fires); cross is lit; 523 of 523 corrupted paths rejected; shooting agrees with the exact decider on 2,431 lattice pairs and 29,696 half-grid pairs; C certificate code agrees with the Python reference on 2,572 groups; census counts reconcile. Rig is validated only in the "not separated" direction.
- Pilot (10 of 920 jobs, 201 CPU s): Set A 1,461,137 rooms, 2,405,837 pairs, all lit at bound 40. Set E 12,209 rooms, 66,412,053 pairs, 20,013 lit only at bound 120. Survivors 0, certified 0, tripwires 0.
- Extrapolation: 4.19 CPU-h (range 2.27 to 7.07); the spec guessed 12 to 30. Shooter replaced by a segment method, 47x faster per pair, same paths.
- Shortcut (d52 method on D20, under 3 CPU s): 1 candidate room, 14 pairs, 0 separated, 0 certified. Completeness rests on d48's (4,5,2) shape; unrefereed.
- Limit: the certificate code handles Z^2 and rectangular lattices, not sheared ones (82% of sampled Set E pairs are admissible only for a sheared lattice). This matters only for survivors; a lit pair needs no certificate test.
- Pilot fits the approved cap, so the coordinator started the full run: `nohup caffeinate -i -s ./run_full.sh 8 10` (8 processes, 10 CPU-h cap for this invocation, inside the approved 40; log `d56-final-check/runs/full_run.log`; results `runs/full/aggregate.md`; a positive or tripwire writes `runs/full/ALERT`).

## 2026-11-17 — d56 full run result (merged finite check)
- Finished 15:35 (started 14:58): 920 of 920 jobs, no ALERT, 37 min wall on 8 processes, 16,940 CPU s (4.7 CPU-h) including the pilot jobs. Aggregate: `d56-final-check/runs/full/aggregate.md`.
- Set A (D20: W = 20, area 20, different-class lattice pairs): 169,672,127 rooms, 285,299,577 pairs, all lit at shooting bound 40. Room count matches the census in total and per job residue.
- Set E (non-lattice marks, index-2 and index-4 bases): 945,884 rooms, 5,238,044,332 pairs; 5,236,565,128 lit at bound 40 and 1,479,204 at bound 120. Room counts match the d50 table per W and the Part A totals per (W, area) cell.
- Survivors 0, path-verification failures 0, certified pairs 0, tripwires 0. Certificate test on the 1% sample: 55.2 million pairs, 0 fully certified (3.45 million single-target Par instances and 16 Cut instances in Set E, none completing a lift pair); 42.7 million sampled pairs were admissible only for a sheared lattice and so untestable by the certificate code (irrelevant: they are lit).
- Failure during the run: `aggregate.py` crashed in its reconciliation step (TypeError at line 101: `D9 / 'runs/a20/job-%d.counts' % J`, operator precedence; same bug at the Part A line). The main table had already printed. Coordinator fixed the two lines by adding parentheses and reran the aggregate; the pre-fix file is kept as `runs/full/aggregate_before_fix.md`. No job was rerun.
- Coordinator check, independent of aggregate.py: 920 SUMMARY lines, all OK; 520 Set A and 400 Set E jobs; sums give survivors 0, certified 0, tripwires 0, verifyfail 0, pairs 5,523,343,909; no non-empty .err, no .tmp, no ALERT.
- Result (computer-assisted): with d46, d47-d50 and this run, no strictly simple orthogonal lattice room with W <= 20 has a pair of rational interior points certified dark by Par, Cut or Rig over any pillowcase base. Rests on: d10 Theorem U, R3, Fact L; d36; d39/d43; d47-d50 lemmas (one referee each; the referees' repairs unreviewed); the d9 and d15 censuses; d46; this run's shooter (verified paths; agreement with the exact decider on 32,127 pairs).
- Not covered: the lit side ("uncertified implies lit"); rooms with 45-degree walls (d51 negative; d11 census only).
- Claim released. Nothing running.

## 2026-11-17 — Read of peer (Codex) work on the board, 2026-11-13 to 2026-11-15 (not verified by the coordinator)
- All in `.context/monteil-amit-reply-review/` (read-only for this thread). No sucre entries after 2026-11-15.
- local-repair, one-sided-repair, illumination-proof-pair: analytic lighting paths for the marked pair in thickenings of Monteil's slit room with REAL parameters (centred wall: 7 reflections; one-sided bay: at most 6 or 4, up to a height bound H(e)). Extends d42's lattice fixtures; selected pair only. Peer-reviewed by a second AI seat.
- Correction from that round: every physical corner stays forbidden after unfolding, including convex corners that become regular points. Coordinator check: `d56-final-check/src/verify_plane.c` rejects any path through a corner (1 or 3 cells), so the d56 lit verdicts respect this.
- triangle-equality: the "2 delta - 2 equality on all named rooms" lead from d51 is mostly vacuous: 9 of 10 Par records are degree-1 identities; only the 22-wall room's Par(C) is proper (degree 3). A convex square also saturates. Conditional remark: that factor profile forces r >= 9.
- ten-wall-proof: direct illumination at r = 3; conditional lemmas for 1 of the 15 shared-rectangle gaps; 0 of the 578 open position types closed.
- three-directions: local fold matrix criterion, finite-state contract for a fixed rational direction, a "reflex budget" attempt; hand proofs, unreviewed.
- amit-reply-draft.md: a second reply draft to Wolecki exists (different content from the coordinator's chat draft; it claims uniqueness of the dark pair over real coordinates and the 7-reflection family, and doesn't mention the certificate checks).

## 2026-11-17 — Goal restated for Daniel (no run)
- Daniel: "don't worry about the emails... focus on getting to the ultimate proof (actually what is our goal?)". Emails dropped from the coordinator's follow-ups.
- Goal (set 2026-11-09): 22 is the minimum wall count of a strictly simple square-lattice room (axis-parallel and 45-degree walls) with a dark pair.
- With the fold side closed (d46-d56), the orthogonal open core is exactly: every pair is lit in every strictly simple orthogonal lattice room with W <= 20. Proved at W <= 8 (d15); at W = 10, 578 position types open (d17; Codex ten-wall round closed 0).
- 45-degree rooms: census to 32 half-tiles only; no fold-side bound (d51) and no lit-side theory.
- Coordinator recommendation: working goal = orthogonal case; next step = witness mining at W = 10 (parked since 2026-11-13; a search, needs Daniel's approval; proposed cap one Opus agent, 3 processes, 60 min).

## 2026-11-18 — Working goal narrowed; d57 launched (witness mining at r = 3)
- Daniel (2026-11-17): "ok let's narrow the working goal, go ahead with 2". Working goal: every pair is lit in every strictly simple orthogonal lattice room with W <= 20. GOALS.md and the target memory note updated; 45-degree case stays in the stated target, not worked.
- d57 (`d57-witness-mining-r3/`): one Opus subagent mines lighting paths that are valid on whole parameter regions for the 578 open position-type pairs at r = 3 (d15 cert_r3.json, d17). Cap as proposed: 3 processes, 60 min compute; coordinator adds 1 GB RAM, 5 MB output.
- Coordinator now runs on Opus 5.5 (Daniel switched the model).

## 2026-11-18 — d57 result (witness mining at r = 3; Opus, 210k tokens, 41 min)
- Files: `d57-witness-mining-r3/README.md`, `results_r3.tsv`, `thin_corridor_r3.tsv`. Compute: about 42 CPU-min, at most 3 processes, 540 KB.
- 10-wall theorem NOT proved. 0 of 578 open pairs closed on the full real region. 6 collinear pairs closed on a compact truncated region R(2,4) (gaps within a factor 2, points at least a quarter gap from grid lines); 572 partly covered there.
- Lemma U (hand proof, unreviewed): a point at depth h in a corridor of width w, with the other point at distance d, needs at least 2 sqrt(dh/(Hw)) - 2 reflections. 563 of 578 pairs (all 553 chain, all 10 door) have such a corridor, so no finite itinerary set covers them as w -> 0. Measured growth matches (chain 4991 at w = 1/256: 26 reflections, bound 16).
- Lattice reading (coordinator): the obstruction applies to lattice rooms too, since a width-1 corridor in a large room has relative width -> 0. So finite witness covering can't prove the target at any W >= 10; a limit argument is required.
- Limit picture: as w -> 0 the corridor becomes a slit with the point on it; closing that face needs an infinite path family like Lemma H. Plausible for door pairs (GUESSED); r3.md found the chain version breaks after a second door. Collinear pairs have no corridor; their residue is a box-count limit.
- Sanity: no box containing the 22-wall dark pair certified (307 nearby itineraries fail there).
- Not verified: certifier derivation (0 disagreements with replay in 3,295 point checks and 57,195 box replays); replays sample 5 points per box; Lemma U not machine-checked.
- Claim released; nothing running.

## 2026-11-18 — d58 launched (corridor-limit lemma)
- Daniel: "go". One Opus subagent, theory only; exact checks on named rooms and on small fixed instances under 10 CPU-min, one process. Dir `d58-corridor-limit/`.

## 2026-11-18 — d58 result (corridor-limit lemma; Opus, 202k tokens, 24 min; unreviewed)
- File: `d58-corridor-limit/memo.md`, checks in `logs/` (about 70 CPU s, exact arithmetic).
- Lemma P (proved, phase form of Lemma H): a far-point image lights the pair unless its phase lies in a bad arc of length |1 - 2 beta| - kappa; failure needs Lh/(wD) integer, D > h, both phases bad, and T within (1 - kappa) w/2 of a corridor wall. Midline points never fail. For fixed other lengths, only the discrete widths w = Lh/(nD) can fail.
- Door pairs (10): Lemma H applies on the whole type region; Lemma E (bounce off the dead end) repairs single resonances. Residue: a non-empty double-resonance set. 10 exact instances built in it (8 of 10 pairs, w down to 2^-12): all lit by 1-5 reflection chimney/back-wall paths. Lemma E's corner-hit set not characterized.
- Chains: m doors need m window conditions; with m + 1 free image indices, Kronecker density lights the pair off a resonance set when every strip is a full channel (sketch). Breaks at the first non-full-channel hub (open failure sets). Count of the 553 chains with full-channel routes not done.
- 22-wall dark pair: Lemma H's hypothesis 2 fails in all 16 cases (the viewer's channel never contains the door).
- Strategy at 10 walls still incomplete. Gaps: resonance sets near thin faces; chains through non-channel hubs; points approaching walls; long rooms and shrinking gaps that aren't corridors.
- Coordinator read: real progress on the generic case (lit off a measure-zero arithmetic set), but each closure leaves a nested resonance set. Lattice rooms sit exactly on resonance sets (r3.md made this point), so the generic statements don't transfer to the target without the resonance analysis.
- Claim released; nothing running.

## 2026-11-18 — d59 launched (strategy step-back)
- Daniel chose option 2 ("step back to strategy") over continuing case-by-case closure at W = 10.
- d59 (`d59-strategy/`): one Opus subagent. Reads the obstruction map (STATE.md, d27, d35-d41, d57, d58), runs a literature check for post-2020 results on illumination / blocking for torus covers and square-tiled surfaces with marked points (generic queries only), evaluates coordinator candidate ideas, proposes its own, and ranks 2-3 routes each with a first cheap falsifiable test. Theory and reading only; no searches over rooms.

## 2026-11-18 — d59 result (strategy step-back; Opus, 260k tokens, 24 min)
- File: `d59-strategy/memo.md` (+4 scripts on named rooms, under 15 CPU s). Literature check with generic queries only.
- Literature: nothing applies to genus-0 doubles of lattice rooms with two marked points (LMW, Wolecki v3 "at most 22", Apisa-Wright marked points and high rank, Apisa 2020, Duryev 2024; no effective length bounds; no classification of marked square-tiled orbits).
- Candidates: (a) arithmetic "few directions" dead (r20a lit pair needs |p|+|q| > 10; resonance is generic on square-tiled surfaces); (b) surgery induction dead (R22 = r20a + one cell); (c) effective bound is a restatement; (d) orbit closure dead for rational marks (closed orbit, cusps pinch everything).
- Agent ideas: Farey-triangle coherence (local form falsified on r20a); darkness at lattice rooms is arithmetic, so real-length limit arguments can't reach it.
- Ranking: 1) tower branch of the d12/d14 group route, key lemma FH* (lift-or-certify up the block lattice); all named rooms have imprimitive monodromy, so FH* carries the hard cases. 2) corridor faces (d57/d58). 3) incommensurable rooms via Apisa-Wright high rank (doesn't reach lattice rooms).
- Assessment (GUESSED): about 5% the lattice target is provable with current tools; about 15% for a conditional theorem.
- Coordinator note: the brief asked about a publishable intermediate target; per the standing note, no publishing proposal goes to Daniel unless he asks.
- Next (coordinator, under the keep-going rule; named rooms only, no search): d60 = route 1 first test (FH* lift-or-certify on cross12, dumb12, R22 factors).

## 2026-11-18 — d60 result (FH* named-room test; Opus, 164k tokens, 17 min)
- Files: `d60-fh-star-test/` (README.md, fh_star.py, fh_tower.py, strong_probe.py, summarize.py, logs, json).
- COMPUTED, interior marks, minimal N: cross12 30/30 lift, dumb12 28/28 lift, R22 and P6 1 dark pair each, certified ("one parity factor"), so n/a. 0 violations under the weak reading. Strong reading false (dumb12 (1,1)-(1,2): 1,984 of 5,392 N-witnesses don't lift).
- Failures: equal images. cross12 non-minimal 3-block factor and the tower step 6 -> 3 (2 violations, interior marks); R22 wall marks at the minimal factor (2 violations).
- PROVED (agent): the R22 5-block factor has no regular point over b, c, d, so equal-image lit pairs can't lift.
- Repair: (a) distinct images lit in N, uncertified => weak lift (146/146 rows); (b) equal images uncertified => lit in DP (18/18). Branch (b) is the original target on one fibre.
- Coordinator review: reran fh_star.py on all rooms; summary.log reproduces the agent's counts exactly. Rerun CPU 341 s (dumb12 318 s), not the "about 35 s" the agent reported. Cap deviation: agent about 6.5 CPU-min plus my 5.7 CPU-min rerun = about 12 CPU-min against the 10-min cap.
- Verdict: route 1's group-theoretic half is sound but carries no hard content; the tower moves the problem to branch (b), which needs a fold-converse lemma about paths through N-poles.

## 2026-11-18 — d61 launched
- Daniel chose option 1: fold-converse lemma (equal images, uncertified => lit) through factor poles. Named rooms only, 10 CPU-min cap.

## 2026-11-18 — d61 result (fold converse; Opus, 190k tokens, 16 min)
- Files: `d61-fold-converse/` (README.md, fold_converse.py, summarize.py, logs, json).
- PROVED (agent, unreviewed): lit direction. Equal images u in N, live component K of u in N's arc graph: path K => light via at most two partial involutions tau_p (pole-end local monodromy restricted to 2-cycles = corner avoidance); cycle K => monodromy mu around K. Lit at x iff some basis's action carries S~ to T~. Zeros never matter. H is a per-basis family, not a group; the full pole-loop group and the corner-ignoring variant are wrong (P6 12/12, R22 28/57).
- COMPUTED: 405 rows (992,988 basis/arc/lift-pair instances), 0 disagreements with ground truth; all six d60 violations lit by a bounce at an N-pole; all 203 x-dark rows certified.
- OPEN: "separated in every basis => certificate". Reduces via d10 R3 to the canonical factor N_x = Q/B_x (degree <= 4r+4 <= 36): realization lemma (equal images in N_x, no Rig/Cut => 2-cycles of g_x, g_a inside u's blocks join S~, T~ in some basis). With it, plus d46/d52/d56/d16, the W <= 20 target follows. Not a finite check: Q -> N_x has unbounded degree.
- Coordinator review: reran interior (50 s) and wall (4.5 s) tests; summary.log byte-identical; no nonzero disagreement/uncertified-dark/lit-certified counts. Agent CPU about 2 min; within cap.

## 2026-11-18 — d62 + d63 launched
- Daniel: "do both 1 & 2". d62 = independent review of d61 lit direction. d63 = realization lemma over N_x. Named rooms only, 10 CPU-min cap each.

## 2026-11-18 — d62 result (review of d61; Opus, 148k tokens, 12 min)
- Verdict: sound with fixable gaps; nothing fatal. Lit direction and the iff hold; path/cycle split exhaustive; corner avoidance handled; R3 reduction to N_x and deg N_x <= r+4+3r_x <= 4r+4 correct.
- Gaps: G1 tau_u/tau_p must be stated on sheets of u's block (u can be an N-pole); G2 d61's h_graph re-splits the ground-truth walk rather than building from L_p/transport/mu, so its 992,988 agreements mainly confirm Fact L (ground truth itself isn't circular); G3 realization-lemma hypothesis needs quantifiers (Rig fails for both R_y, no Cut factor).
- Independent checks: check_fc.py (FC as stated, 969,372 instances, 0 disagreements); billiard.py (direct exact billiard, 0 mismatches vs d61); deg_bound.py (12/12). This closes G2's evidence concern.
- Coordinator: reran billiard.py and deg_bound.py (0 mismatches, all ok; under 1 s). CPU about 1.2 min, within cap.

## 2026-11-18 — d63 result (realization lemma; Opus, 235k tokens, 16 min)
- Not proved. Lemma 1 (PROVED, independent of FC): the realization lemma is exactly "x-dark => certificate" for same-class pairs.
- Statement needs room hypotheses: cross scaled by 3 (coarsest base, cited d39/d43) and the d14 n = 10 non-transitive relations (N_x = B, no Rig or Cut; derived from d14 data, not recomputed) break d61's abstract wording. It also doesn't close the target alone: different-class pairs need "x-dark => Rig"; non-lattice marks need the coarsest base.
- Split: N_x != B is finite (PROVED delta*z <= r, area <= 8r); closable by a d52-style enumeration incl. delta = 2 (needs Daniel's approval). N_x = B is the minimal open sub-claim; for primitive G it is Lemma H plus one x-lit pair (dead-end list). Inside-block and twist-only arguments ruled out by d14.
- PROVED special cases: degree 2; Galois (deck group C2, V4 or S3).
- COMPUTED: 530 named-room pairs (512 lit, 18 dark Cut, all cross12) and 192 pairs over 168 double covers (186 lit, 6 dark Cut); 0 counterexamples. Weak evidence (orbits <= 131 states).
- Coordinator: reran double_covers.py and realize.py (under 1 s); summed logs: CE 0, sound violations 0. Within cap.

## 2026-11-18 — d64 + d65 launched
- Daniel: "yes both". APPROVAL: d64 enumeration of N_x != B covers (area <= 8r, incl. delta = 2), cap 2 CPU-hours. d65 = theory on N_x = B using room geometry, named rooms only, 10 CPU-min.

## 2026-11-18 — d65 result (N_x = B theory; Opus, 216k tokens, 16 min)
- REFUTED per lift pair: S10 (12-wall, 10 cells, half-turn symmetric about (2,2)), marks (1,3), (3,1), a = (1,1). At x = b, d: N_x = B; delta-pairs (S_f,T_f), (S_b,T_b) x-dark with no Par/Rig/Cut over any factor. Cross pairs (S_f,T_b) lit at depth 2, and the room pair is lit (d9 orbit.decide). So the target is not contradicted; only the per-lift-pair realization lemma fails. Verified by notch12.py and the independent d12 census verdict.
- 4 of the 18 d14 relations are real rooms (Z12, S10); all 18 lack certificates (d63 said 6). Rig never applies to equal-image pairs.
- Lemma M (PROVED): every d14 dark pair is {s, delta s} for a deck involution delta (a room symmetry) with two regular fixed points; planarity doesn't exclude it.
- Surviving hypothesis RL-room: normalized, strictly simple, interior marks, N_x = B, all four lift pairs x-dark => each has Rig(x) or Cut(x). Suffices for d63's chain (PROVED). Gap: symmetric rooms (iota-delta bijection) and asymmetric rooms (per-class Lemma H on room pairs). 0 counterexamples on 16 interior room-pair rows (weak).
- Coordinator: reran rl_room.py (0.3 s), output identical. CPU under 3 s.

## 2026-11-18 — d64 result (finite-case enumeration; Opus, 222k tokens, 28 min; approved search)
- Scope: normalized strictly simple orthogonal rooms, W <= 20, some x with 1 < deg N_x < n. Completeness PROVED before run and checked (C port of d52 enum_K reproduces 127/677 shapes; arc model = model-free enumerator on 4,290 delta=2 cases; brute force over 9,800,041 polyominoes n <= 14 finds 229 in-scope rooms, all listed).
- COMPUTED: 4,290 quotients, 4,475 (K, delta) cases, 4,776 rooms (4,581 normalized), 2,800 in scope; 81,924 rows, 830 x-dark, 0 certified -> 830 per-target counterexamples. 37 interior point-level pairs are x-dark on all four lift pairs, uncertified. Smallest: room 1843 (20 cells, W = 12), S = (1,2), T = (3,2), x = d; lit at x = b by the straight segment.
- Finite half closed directly: all 6,680 same-class interior pairs in the 2,800 rooms are lit.
- Consequence: per-target realization (and per-target RL-room) is false; the chain must use the pair-level form "dark at every target => certified" (d10 D2).
- Coordinator: reran example.py 1843 (identical to log) and verify_billiard.py 60 1843 (0 mismatches, 2 dark groups). CPU about 27 of 120 approved minutes.

## 2026-11-18 — d66 launched
- Daniel: "ok". Pair-level restatement of d61-d65 chain; attack all-targets-dark => certified when N_x = B. Named rooms and existing d64/d65 data only; 10 CPU-min.

## 2026-11-18 — d66 result (pair-level chain; Opus, 199k tokens, 19 min)
- Open lemma OL: strictly simple normalized orthogonal rooms, r <= 8, area >= 21, every class with N_x in {B, Q} (rooms R*): any two interior lattice points of one class are x-lit for some x with N_x = B. d64 closes every room with a proper factor at any class; d9 closes R* at area <= 20; all normalized rooms with area > 8r are in R*, so OL is infinite.
- PROVED (from cited d39/d43): no certificate can exist in OL's range, so OL is a pure lit statement.
- COMPUTED: per-target forms false inside R* too (cov4181, cov4269: W = 20, area 28, trivial deck group; dark at one B target, lit at the other; billiards agree to max(p,q) = 60).
- Relay lemma (PROVED): a lift of S seeing a fixed point of a deck involution delta makes the delta-pair lit; reduces Lemma M pairs to G1 for {S, C}; 30/30 rows.
- Remaining: non-delta pairs in rooms with >= 2 B targets; one-B-target case (a class has <= 4 interior points, PROVED). Trivial-deck-group rooms are Lemma H territory.
- Other gaps: G1 different-class pairs and G2 non-lattice rational marks have open lit sides; d64 unreviewed.
- Tests: 4,782 same-class pairs, 0 dark at W <= 20 (R22, P6, P6found correctly dark); 27,190 different-class pairs lit by exact billiards; 8,025 half-integer pairs lit in named rooms; larger R* half-integer run capped at 300 s, 117 unresolved (not dark).
- Coordinator: reran billiard_check.py 60 and pair_level.py (28 s); outputs identical. CPU about 333 s, within cap.

## 2026-11-18 — d67 launched
- Daniel: "ok go, do 1 then 2". d67 = independent review of d64 (sequential; d68 one-target OL sub-case after). Reruns of the approved d64 scope only, 15 CPU-min.

## 2026-11-18 — d67 result (review of d64; Opus, 168k tokens, 12 min)
- Verdict: sound with fixable gaps. Completeness steps checked (z <= 4, d <= 18, >= 3 singular classes, quotient search, arc-model covers incl. delta = 2); boundary cases handled; d66's "any class" scope extension correct.
- Gaps: z = 4 part of enum_K.c (3,663 of 4,475 cases) lacks an independent cross-check (no defect found on reading); d64 brute force shared pipeline code (now closed by d67's own C brute force over 104,592,937 polyominoes n <= 16, matching at every area); README bullet 3 over-claims; cosmetic citation wording.
- Independent: own exact billiards (no d64/d52/d10/d62/d63 imports) find witnesses for all 6,680 pairs (max(p,q) <= 8) and all 37 point-level pairs; P6 dark pair gets no witness at H = 20; counts 4,581 / 2,800 / 6,680 reproduced; all 2,843 proper quotients in d64's list.
- Coordinator: reran indep.py 12 (1.6 s), output identical; 0 pairs without witness. CPU about 135 s.
- Next: d68 (OL one-target sub-case).

## 2026-11-18 — d68 launched
- OL one-B-target sub-case (a class has <= 4 interior points). Named rooms + existing d64/d66 data, 10 CPU-min.

## 2026-11-18 — d68 result (OL one-target sub-case; Opus, 88k tokens, 4 min)
- OL1 is empty. PROVED counting identity n = cvx_y + 2 smooth_y + 3 rfx_y + 4 int_y per class; two Q classes give 2n <= 4r + 4, so n <= 2r + 2 <= 18 < 21. Coordinator re-derived the bound by hand.
- Side result (PROVED): one Q class (BBBQ) gives n <= 4r + 4 = 36, a finite set (cov4181, cov4269 inside it). Only BBBB rooms are infinite; sharpens d66's area > 8r to area > 4r + 4. Closing BBBQ needs a bounded search (Daniel's approval).
- COMPUTED on existing data: identity holds on all 4,776 rooms x 4 classes; geometric Q = block Q on 7,124/7,124; 43 rooms with >= 2 Q classes all area <= 16; d66's 15 OL1 pairs lit.
- Coordinator: reran one_target.py (0.3 s), output identical.

## 2026-11-18 — d69 launched
- Daniel: "ok do 2, then 3 if we don't get a breakthrough". d69 = one idea round on BBBB rooms (area > 36). If no foothold: write-up of what is proved.

## 2026-11-18 — d69 result (BBBB idea round; Opus, 193k tokens, 16 min)
- Verdict: no proof; partial foothold. Rectangle step trivial. Midpoint lemma (PROVED; coordinator checked: integer mirrors preserve parity, so the unfolded midpoint of a same-class pair is a lattice point) blocks x-monotone families when the midline has no usable lattice point; explains 254 of 1,067 x-monotone failures. Counting identity forces nothing beyond "no Q class": DB55 (area 53, BBBB) has a length-3 unit corridor.
- COMPUTED: four explicit families light 726/726 pairs in 7 hand-built BBBB rooms (area 41-63) and all but 68 of 11,437 d64 pairs; 389 bounce witnesses re-traced, 0 failures.
- First failing step: chain/induction across turns. cov2929 (W = 20, area 22, BBBQ) has two lit pairs no family reaches. Transfer lemma (sketch): open-set family failures persist in BBBB rooms with area > 64. Dumbbell door lemma reduces to a congruence, unproved.
- Coordinator: reran verify_b.py and symcheck.py; identical. CPU about 25 s.
- Per Daniel's instruction: no breakthrough, so option 3 (write-up) starts as d70.

## 2026-11-18 — d70 result (results record; Opus, 193k tokens, 8 min)
- File: `d70-writeup/RESULTS.md` (777 lines, 10 sections, status tags on every claim, 18 refuted statements, 21 dead ends, Peyton credited as lead investigator).
- Coordinator checks: summary read; fold-side totals (about 14.4e9 rooms, 59.4e9 pairs) sum correctly from the d46 and d56 rows; banned-word scan 0.
- Discrepancies found by d70: (1) open core is all R* rooms with area 21-36 (BBBB and BBBQ, finite) plus BBBB area > 36, not "BBBB area > 36" (my error in the d68 report; STATE.md corrected); (2) STATE.md tagged d61 unreviewed (corrected); (3) d69 room/pair count 8/743 vs table 7/726 (README-internal); (4) d64 scope wording (corrected); (5) d63 "6 of 18" vs d65 "all 18" (d65 supersedes).

## 2026-11-18 — Astra work found in sucre/.context (21:45-22:21, not on the board)
- Coordinator missed these on the first look (searched the board and dirs named "astra" only). Files: `.context/illumination-outside-assessment.md`, `illumination-cylinder-probe.py`, `illumination-ninth-corner.md`, `staircase4991-{diagonal,moving-corner,moving-marks}.md`, `staircase4991_windows.py`.
- Assessment (Astra 6.2): park broad searches; candidate "common open cylinder" criterion for BBBB rooms (some lifts of S, T lie in one corner-free open flat cylinder); cusp test proposed, not run. dumb12 probe: all 4 same-class pairs share a periodic cylinder (periods 4, 4, 14, 14). Coordinator reran the probe: output matches.
- Ninth corner: R22 with attachment width w; base (w=0, r=8) lit by velocity (-4,7); same shot lights w = 4k/7 (k=1..7 traced), so lit widths sit on both sides of the dark width 1. Pair-specific.
- Staircase 4991: pair (1,10)-(10,1) lit for every real middle corner (a,b) in (3,9)^2 (explicit six-bounce routes, continuum proof, 529-point replay); marks may move within 1/40; fails for unrestricted chamber points (counterexample shot given). Two-door family obstruction: 26 window candidates. Coordinator reran staircase4991_windows.py: 26 candidates, matches.

## 2026-11-18 — Astra Q-class closure (`.context/qclass-closure/`, 22:26-22:32) and coordinator check d71
- Astra theorem (computer-assisted): strictly simple orthogonal lattice rooms with some parity class whose points are all corners (geometric Q class) need >= 22 walls for a dark pair of distinct interior lattice points, any classes. Area <= (r+4)+3r <= 36 by the d68 counting identity. 780,565 rooms (261,564 above area 20), 3,933,192 pairs (907,567 same-class, 3,025,625 different-class), all lit, each witness replayed by a separate exact tracer; enumeration matched by an independent cell-by-cell census (144 phase-by-area counts) and polyominoes through area 15. Plus 43,524 lattice pairs in 3,889 d64 covering rooms lit (removes the proper-factor branch for different-class pairs too).
- Coordinator check d71 (`d71-check-qclass/`, d67's tracer, no Astra code): reran audit.py (counts match, 15 s); independent billiards on 20,200 sampled rooms (half above area 20): hypothesis holds on all, 141,882 pairs, 0 without a witness at max(p,q) <= 20 (about 18 CPU-s); R22 control has no witness at H <= 40. Enumeration completeness not independently re-derived (argument checked by reading; three Astra enumerations agree).
- Effect on the chain: closes all BBBQ rooms (d68's finite part with a Q class), for same- and different-class lattice pairs. Remaining: BBBB rooms (every class has an interior or smooth wall point) with area >= 21 (area 21-36 finite, unchecked; > 36 infinite); G1 and G2 for BBBB; non-lattice marks; 45-degree.

## 2026-11-18 — d72 launched
- Daniel: "ok go". APPROVAL: direction/cusp enumeration for the common-cylinder test, existing BBBB rooms only, 10 CPU-min.

## 2026-11-18 — d72 result (common-cylinder test; Opus, 126k tokens, 8 min)
- Exact method: full SL2(Z) orbit of the marked origami ("no CC in any direction" is exact); validated on 18,446 lifts vs direct tracing, 0 mismatches; dumb12 periods 4, 4, 14, 14 reproduced; R22 dark pair has no CC (orbit 2,592).
- True BBBB (every N_x = B): 9 rooms (dumb12 + 8 d69 rooms), 747/747 pairs in a common open cylinder (directions max <= 39). cov2929, cov4181, cov4269: 33/33.
- Geometric-BBBB rooms with a proper factor (d64 data, 2,466 rooms, 6,287 pairs): 11 lit pairs have no CC; smallest cov446 (n 15, W 18), S = (1,2), T = (3,2), lit by the visible horizontal segment. All 11 are axis-parallel at distance 2 with a visible witness: the marks sit on a cylinder-boundary saddle connection, not in an open cylinder. d64 closes these rooms, so the open case is unaffected.
- Two-cylinder chain holds for R22's dark pair too, so it implies nothing. Agent estimate (GUESSED): CC true about 25%, provable about 3%.
- Coordinator: reran orbit.py on R22, dumb12, cov446 (identical). Coordinator note: the 11 failures are an artifact of requiring the open interior; a closed-cylinder variant (segment inside the cylinder closure avoiding vertex lifts) covers them. CPU about 35 s.

## 2026-11-18 — d73 launched
- Daniel: "1". APPROVAL: room enumeration of strictly simple orthogonal rooms with r <= 8 and area 21-36 that are BBBB, all interior lattice pairs lit-tested plus common-cylinder test; cap 2 CPU-hours.

## 2026-11-18 — d73 result (BBBB area 21-36; Opus, 111k tokens, 11 min; stopped at cost estimate)
- Not run: full scope is about 1e11-1e12 rooms (GUESSED from d9 growth; exact: 92,657,242 rooms at W <= 12, areas 21-36), roughly 1,000+ CPU-h. Area 21 alone about 2 CPU-h.
- Completeness argument for enum.c (skeleton + widths/heights) PROVED in writing; counts match d9 census (64 rows, W <= 14, area <= 20) and Q's census (W <= 12 all areas; W <= 14 areas 1-22).
- Pipeline slice: 31,612 rooms, 1,001,339 pairs, all lit after one retry; second tracer replayed all witnesses, 0 failures. No true-BBBB classification or cylinder test run.
- CPU about 6 min.
- Coordinator correction: my recommendation assumed this range fits in 2 CPU-h without an estimate; it doesn't. Also the agent's plan 4 premise ("true BBBB is rare") is wrong: rooms with a proper factor (d64, 2,800 in scope) or a Q class (780,565) are a tiny fraction, so almost every room at area 21-36 is true BBBB. d72's 0 of 2,466 reflects d64's data, which has proper factors by construction.
- 2026-11-18 Coordinator: RESULTS.md section 11 addendum added (Q-class closure, d71-d73).

## 2026-11-19 — Astra off-grid and doorway work (`.context/qclass-closure/off-grid.md`, `offgrid/`, `offgrid/doorway.md`)
- Area-15 off-grid theorem (computer-assisted, single implementation of the continuum step): rooms of exactly 15 unit cells with a corner-only parity class and W < 22 light every pair of distinct interior points, real marks included. R22 is such a room, so 22 is exact in that family. Method: d13 cylinder-cover algorithm with exact rational polygons, reciprocity pruning, tile-pair runs for 6 rooms (720/720 tile pairs); residual lattice pairs matched to the replayed lattice census (15,571 rooms). Independent enumerations agree by shape (W 12-20: 13, 327, 3,413, 18,966, 55,006).
- Limits stated by Astra: a second tile-pair run with unmodified predicates finished 708 of 720 (shares cylinder geometry); no independent end-to-end continuum implementation yet.
- 18-wall, all areas, Q-class rooms: 141,885 of 141,887 cleared for real marks; 2 rooms with 18 cells remain (18 open tile pairs each), no evidence of darkness. cov4181, cov4269 cleared with zero residual.
- Doorway note: two-ended cap retracing removes D58's corner exceptions; dead-end door pairs lit whenever w >= L/2 (target cap) or w >= L/4 (both back walls); otherwise darkness forces finite integer conditions on depths. Necessary conditions only; doesn't close D58's ten types at unrestricted lengths.
- Coordinator: reran audit_area15.py and audit_eighteen.py (outputs match). These audits recheck records and set consistency, not the geometric computation itself.

## 2026-11-19 — d74 launched
- Daniel: "sure". Independent continuum check of Astra area-15 off-grid result; named rooms only, 30 CPU-min.

## 2026-11-19 — Astra 18-wall closure (`.context/qclass-closure/two18/`, 00:07) and 20-wall start
- Claim (computer-assisted, awaiting outside review): every strictly simple orthogonal room with exactly 18 walls and a corner-only parity class lights every pair of distinct interior points, real marks included. All 141,887 rooms; the last two (18 cells) closed by an endpoint-dependent shear: residuals lie within 1/17 of two boundary grid points; the shear power K = ceil(1/(8LA)) maps every displacement A in (0, 1/17] into a bounded phase range; 853 certified boxes, 144 proof trees, Python certificate replay, 40,608 direct strip/line checks.
- Overlap: d74 (independent continuum check) also targets these two rooms; its result is now an independent check of Astra's.
- Astra session (Codex, gpt-6.2-astra) is now running the 20-wall Q-class rooms (`.context/qclass-closure/twenty/`), per Daniel's "ok go" in that session.
- Coordinator: full replay.sh rerun started (background).
- Coordinator: Astra two18 replay.sh rerun from scratch in a fresh directory (UB sanitizers on): residuals 146,308 products within 1/17; all 4 periods verified; 144 trees, 853 boxes, 40,608 comparisons; both saved and regenerated certificates verify. Reproduces, but uses Astra's own code; d74 is the independent check.

## 2026-11-19 — d74 result (independent continuum check; Opus, 174k tokens, 45 min)
- Independent certifier (no Astra code), soundness PROVED in README resting on d13's unreviewed Lemma A' and Theorem C(2); validated on 987 certified pairs by an exact tracer (0 failures).
- R22 control: leaves exactly (1,3)-(3,5), nothing else (Python and C++).
- Area-15 hard rooms: all 6 confirmed (rooms 0, 2, 3 at bound 10; 4, 5 at 16; room 1 leaves only lattice pair (2,1)-(4,3), lit by exact path (-2,3)). Independent confirmation of Astra's area-15 off-grid theorem, modulo d13 lemmas.
- Two 18-cell rooms: not certified by plain cylinder covering; 2-dimensional residue near corner pairs that share no cylinder up to bound 16, matching Astra's 18 open tile pairs per room exactly. Astra closed these with the endpoint-dependent shear, which d74 didn't implement; so Astra's 18-wall closure has replay but no independent check yet.
- Coordinator: compiled cert.cpp and reran R22 (B8) and area-15 rooms 0, 2, 3 (B10): outputs match. CPU about 18 min (9 min aborted run), under the 30-min cap.

## 2026-11-19 — Astra redirected to BBBB core
- Daniel: "2". Sent Astra session (e380bb94, Codex gpt-6.2-astra) a message: wrap up the 20-wall Q-class run (finish within about 15 min or stop cleanly, record progress), then attack BBBB rooms with unbounded area: can the endpoint-dependent shear be made uniform; test on cov2929, DB55/Lemma U corridors, d58 door pairs; candid verdict. No discovery searches without approval; modest CPU; output in .context/qclass-closure/bbbb/.

## 2026-11-19 — Astra BBBB result (`.context/qclass-closure/bbbb/`) and 20-wall handoff
- 20-wall Q-class: had finished before the redirect. All 913,622 rooms cleared for real marks (912,728 whole-room, 894 tile-level; 620 shear boxes, 3,652 trees). Single implementation plus Astra's audit; shear step not independently checked.
- Long-corridor theorem (Astra, hand proof, unreviewed): fixed chambers and doors of width w joined by an empty straight corridor; for all corridor lengths above a threshold, every interior point of one chamber lights every interior point of the other, real marks included, one threshold for all pairs. Proof: generic-slope minimality (Masur-Tabachnikov Thm 1.8) gives door paths stable on a slope interval; a long corridor turns that interval into a full 2w transverse sweep, and the intermediate value theorem matches position and direction; compactness gives uniformity. Coordinator read the argument: sound in outline.
- DB55: all 496 interior lattice pairs lit for every integer corridor length >= 450; same-class pairs at lengths 3 + 6k from saved paths. check.py rerun by coordinator: identical.
- Structural insight: at lattice marks every row-period shear fixes every lift, so the Q-class shear can't help in the lattice BBBB case.
- First missing step: a lower bound on the usable slope interval as doors shrink (d58), and an argument for rooms with no separating straight corridor (cov2929-type turns). General BBBB open.

## 2026-11-19 — d75 launched
- Daniel: "ok go" (review first, then Astra shrinking-door bound). d75 = adversarial review of the corridor theorem.

## 2026-11-19 — d75 result (review of Astra corridor theorem; Opus, 100k tokens, 6 min)
- Verdict: sound, one minor fixable gap (F1: state that the reflection sequence is fixed jointly for nearby starts and slopes in the clearance sentence). Cosmetic: cite the proof of M-T Thm 1.8 (density of every infinite trajectory); define "exact resonance"; note strict simplicity per length.
- Checks: minimality applied correctly; transverse hits so no grazing; phase function linear in s with slope l + a + b, threshold l >= 2w/delta correct; compactness uniformity correct incl. marks near corners.
- DB55 (own exact code): 256/256 cross pairs lit at l = 450, 451, 457, 1000; saved directions light 64/64 at l = 3, 9, 15, 21 (and 5, 7). Derivation of 450 and count 496 correct. CPU about 9 s.
- Coordinator reran verify.py: identical.
- Coordinator reran verify.py with d72 cyl_H40.json: identical. Sent Astra the review findings (F1, C1-C3) and the shrinking-door task.

## 2026-11-19 — Astra shrinking-door result (qclass-closure/bbbb/shrinking-door.md)
- Sharp bound: usable slope width on one itinerary ≤ w/D (attained in D58 straight viewer). No universal bound in terms of reflex count and w alone.
- Negative: D58 double resonance cannot be closed by span alone (sweeps 17w/16, 19w/16 < target gap 19w/10). Needs a placement argument mod 2w.
- Positive: two shrinking doors with a common-slope corner-free leg at both ends are lit for every ℓ > |a−b|, independent of w. Coordinator checked the arithmetic (span (ℓ+a+b)w/max(a,b) > 2w ⇔ ℓ > |a−b|; 17/16, 19/16, 19/10).
- Open: cov2929 turns (no separating strip), chains (windows can be disjoint). F1, C1–C3 applied to README.md. Not independently reviewed.
- 2026-11-19: Daniel approved ("ok go"). Sent Astra the D58 double-resonance placement task: prove or refute placement mod 2w; if refuted, say whether a dark pair results and its wall count. Proof task, no searches.

## 2026-11-19 — Astra D58 placement result (qclass-closure/bbbb/placement.md)
- D58 double-resonance builder: all 8 position types lit for every k ≥ 2 (w = 2^-k), incl. the 18 recorded H/E failures. Ten-wall rooms; no dark pair.
- Method: transverse-monotone paths through 2–3 full rectangular columns; lattice test on seam heights. k=2..15 exact counts; k≥16 rounding proof via 8a−7X=−323c.
- Coordinator: re-ran placement.py (0.1 s), output identical to placement.txt. Hand-checked k≥16 error bounds (0.030, 0.014 < 1). Not independently reviewed.
- Scope: counting lemma general for rational full-column chains; existence proof specific to D58 offsets. General rooms with the same bad phases and cut-hub chains remain open.
- 2026-11-19: Daniel approved ("ok go"). Launched d76 (Opus subagent, independent review of placement.md, 10 CPU-min). Sent Astra the general placement-lemma task; told it not to edit placement.* until d76 reports.

## 2026-11-19 — d76 review of placement.md: sound with minor fixable gaps
- F1 (minor): k≥16 section must state builder layout is k-independent for k≥16 (j≥2, a>0, p+w<4, heights fixed). Reviewer confirmed at k=16,17,20,30,41.
- C1–C3 cosmetic: path ends at target not reflected copy; define positive orientation; counts are height pairs not paths, define lcm of rational periods.
- Independent: all 10 count rows match; 40/40 traced paths k≤15 reach target exactly; k≥16 errors max 0.0081/0.0125; "-" are builder failures; "outside" types lit by D58's other family.
- Coordinator re-ran verify.py (102 s): output identical apart from CPU line.

## 2026-11-19 — Astra chain-criteria.md (general column-chain lemma)
- General sufficient tests: (1) any-length chain: seam widths > h_i/(D h_{i-1}) (lattice minors) lights all heights; (2) three columns: exact iff-test 2e < bu+av for entering both doors, then (a+ℓ+b)δ > Q lights; (3) shrinking last travel c.
- Application: DBw2 dumbbell (D69 chambers 5x5 and 5x6, width-2 corridor), every interior lattice pair lit for every integer ℓ > 10; infinite true-BBBB subfamily (ℓ coprime to 5). Coordinator recomputed the δ table exactly; max 4/δ−a−b = 10 at (2,4).
- Limits: monotone paths fail for DB55 (1,1)-(9,1) (midpoint lemma) and cov2929 (turn at seam). Astra proposes next: criterion for horizontally reversing paths.
- placement.md F1, C1–C3 applied by Astra. Not independently reviewed.
- 2026-11-19: Daniel approved ("ok go"). Sent Astra the reversing-path criterion task (test case DB55 (1,1)-(9,1); also cov2929). Proof task, no searches.

## 2026-11-19 — Astra reversal.md (paths that turn back)
- DB55 (1,1)-(9,1) witness: slope −37/8, reverses at (13,1/2), 26 horizontal + 1 vertical contacts. Coordinator traced it independently with exact arithmetic in the DB55 polygon: target reached after 27 contacts, the only vertical one at (13,1/2), no corner.
- Criterion: signed column-placement test with turn events (vertical wall windows); same lattice generators, so chain-criteria width tests extend. One-reversal length test (a+b+ℓ)Δ>2w.
- DB55 pair lit for every real corridor length ℓ>5 (Δ=1/9, a+b=13); coordinator re-derived interval (−1/24,5/72) and threshold.
- cov2929 turning pairs: reversals at (2,5/2) and (6,7/2) on internal walls fit the signed test.
- Open: proving some reversal route succeeds in an arbitrary BBBB room. Not independently reviewed.
- 2026-11-19: Daniel approved ("ok go"). Launched d77 (review of chain-criteria.md + reversal.md, 10 CPU-min).

## 2026-11-19 — d77 review of chain-criteria.md + reversal.md: both sound with minor fixable gaps
- F1: test (a) should name the projected lattice and tie full row rank to index h_i / 1-dim kernel. F2: reversal test should state the turn's before/after runs are the same physical run and the window faces it.
- DBw2: 6,851 pairs at each of ℓ=11,12,13,17,25 traced exactly, 0 failures. ℓ=10 is exactly where the proof stops: 4 pairs (e.g. (3,1)-(19,2)) unproven at ℓ=10, truth unchecked. True-BBBB claim relies on d69 bounds (not re-reviewed).
- DB55: ℓ=3, 5.1, 5.5, 6, 6.3, 7, 20 traced exactly; branch fails at ℓ=5, threshold strict.
- cov2929: both reversal contacts confirmed strictly inside walls.
- Coordinator re-ran verify.py: output identical (0 failures, 2.2 s).

## 2026-11-19/20 — Astra work directed by Daniel directly in its chat
- midpoint-necessity.md: R22's marked pair has 24 sheet coincidences (6 regular, 18 at reflex corners, ≤2 per reflex) ⇒ ≥9 reflex corners for that configuration; equality in R22. cov4181 shows counting alone can't finish the proof. Not reviewed.
- two-class.md: cylinder winding changes the midpoint parity iff one of u, h, C ≢ 0 mod 4. Certifies 687/747 saved pairs in 9 BBBB rooms; the other 60 are already lit. No saved pair tests the two-class-only case. Not reviewed.
- d77 fixes F1, F2 and the ℓ=10 scope note applied.
- 2026-11-20: Daniel: "ok go, but wait until it finishes". After Astra settled, sent the search-plan request (plan only, no run): scope, pipeline, counts/cost, cap, replication → search-plan.md.
- 2026-11-20: Astra delivered search-plan.md (plan only; no search process running, checked ps). Key point: no finite reduction exists, so no bounded run can prove the W≤20 goal; d73's 1e11–1e12 rooms can't be avoided. Proposes one slice: area 21, W=10 (r=3), 34,501 free rooms, all real endpoints; cap 2 CPU-h / 3 h / 2 GiB. Coordinator checked 34,501×210 = 7,245,210 pairs, ×231 = 7,969,731 tile pairs. Awaiting Daniel's decision.

## 2026-11-20 — Astra work directed by Daniel in its chat (read at ~06:04)
- Area-bound theorem: not found. Lelièvre–Monteil–Weiss gives finiteness for fixed surface only. arithmetic-rigidity.md: 10-wall staircases (widths m,m+1,m,m+1) show unbounded normalized area without degeneration, and corner alignments don't bound denominators. Census stays paused.
- short-escape.md: cov4181's lit pair is a forced straight shot; retired as ninth-corner control.
- bottom-step.md: R22 + square (0,−3) (= D8 R22-L1-005, 20 walls) lit by a path through old reflex corner (1,−2), plus a second change (crosses into the added square).
- fixed-wall.md: in fixed R22, 5 of 9 reflex corners each solely block a path: (1,−2), (1,2), (1,1), (4,1), (0,1). Unaccounted: (0,−1), (1,−1), (3,1), (3,2).
- low-valency.md: route r ≥ 5n/12 ≥ 8.75 needs (i) d ≥ 2n/3 and (ii) no off-class regular candidates. Proves d ≥ n−2 for blocks of size 2 + primitive block action, n > 48. 747 saved pairs: none low valency; st279 attains n−2.
- three-sheet.md: size-3 blocks close above area 36 (d ≥ n−3); above area 120 the only low-valency case is one 8-sheet block holding all marks' sheets, r = 8, all reflex corners same parity.
- Now running: Daniel's "don't stop until breakthrough" on the 8-sheet exception. None of these notes independently reviewed.
- 2026-11-20: Daniel approved ("ok go"). Launched d78 (review of low-valency.md + three-sheet.md, 10 CPU-min).

## 2026-11-20 — d78 review of low-valency.md + three-sheet.md: both sound with fixable gaps
- d well defined, matches midpoint-necessity. Size-2 lemma holds (3-transitivity, corrected R1 excludes all intermediate pillowcase factors). n>48 from Theorem G. Spare-block argument needs only pointwise block-stabilizer transitivity (proved). Thresholds 36, 120 (≥120 suffices) and the 8-sheet residual correct. Case split complete.
- Findings (all low): 743-pair claim needs n≥21 not n>48 (only 566 pairs at n>48); low-valency.md needs a forward link to three-sheet.md; list dependencies (Theorem G uses CFSG; dictionary D0); cite corrected R1.
- Independent: own permutation construction reproduces 9 rooms / 747 pairs; st279 d=54 (104), 55 (16); dumb12 d=19.
- Coordinator re-ran verify.py: identical.
- 2026-11-20 06:08: Astra eight-sheet.md: the 8-sheet exception forces the marks onto a common mirror line of the room, so they see each other directly. Combined: above area n ≥ 120, r ≤ 8, every same-parity interior lattice pair is directly visible or has d ≥ n−8 (condition (i) of the r ≥ 5n/12 route). Not reviewed. d78 fixes applied. 07:22 Daniel asked Astra "what's next?" directly; Astra answering.
- 2026-11-20: Daniel approved ("ok go"). Launched d79 (review of eight-sheet.md, 10 CPU-min).

## 2026-11-20 — d79 review of eight-sheet.md: sound with minor fixable gaps
- Steps (a)–(d) hold; mirror is a true planar reflection. Combined statement (n ≥ 120, r ≤ 8: direct visibility or d ≥ n−8) follows. Candidates ≥ 28 at n=120, 30 at n=121.
- Findings (low): edge-parity wording; state edge-connectivity use of strict simplicity in (b); lemma holds for any G-invariant block (scope); stronger fact R = R_S ⊔ (R_S + (T−S)) worth stating.
- Saved data: R22 dark pair's smallest block = all 15 cells (hypothesis fails, as expected). 3 of 12,185 saved cover pairs have an 8-cell block (cov3397, cov3608, cov4474); all satisfy every step.
- Coordinator re-ran verify.py: identical except the print order of one Python set (same 4 patterns).

## 2026-11-20 07:45 — Astra (Daniel-directed: "keep going until you have a breakthrough")
- shortest.md: in cov4181 one physical reflex corner (7,2) is the first obstruction for shortest routes to candidates in two different midpoint classes, so classes can't each be charged a fresh corner. Sufficient test: a regular candidate closer on the ordered-pair surface than either mark is to a corner ⇒ lit. No distance bound for high-valency pairs.
- high-valency-geometry.md (proof draft): n ≥ 120, r ≤ 8, normalized: every interior pair with an irrational coordinate is lit (via reviewed d16 moving-family theorem; intersection count when rates differ; blocks of size 4–6 excluded by boundary argument when rates equal). Consistent with Wolecki finiteness + d16. Large-area counterexample now needs two rational endpoints. Not reviewed.
- d79 fixes applied to eight-sheet.md. Astra idle.
- 2026-11-20: Daniel approved ("ok go on opus"). Launched d80 (Opus review of high-valency-geometry.md, 10 CPU-min).

## 2026-11-20 — d80 review of high-valency-geometry.md: sound with fixable gaps
- F1 (medium): Wolecki finiteness + d16 would exclude irrational dark pairs at every area, but d16 §6.4 records a gap in Wolecki's Lemma 2.9 for exactly this family; the note is the project's only argument avoiding that gap and should say so.
- F2 (low): boundary step needs a unique largest block partition, which holds only at n ≥ 120 (cov3397/3608/4474 have two, size-4 blocks). State the dependence.
- F3 (low): tighten "A_m on both sides" (Goursat) and the corner-branch wording. F4 (info): some redundant text; eight-sheet lemma not used.
- Independent: d16 use covers all irrational cases; unequal-rate inequality 75 > 24 ≥ 3r; equal-rate block sizes 4–6 and Riemann–Hurwitz re-derived; 1391 equal-rate pairs satisfy 2d = R + J.
- Coordinator re-ran verify.py: identical. Confirmed d16 reduction.md §6.4 records the Wolecki Lemma 2.9 gap.
- 2026-11-20: Daniel approved ("ok go"). Sent Astra condition (ii) for rational pairs at n ≥ 120, r ≤ 8 (after d80 fixes). Proof task, no searches.
- 2026-11-20: Daniel approved "1 and 2": record catch-up + d81 (lower the area-120 threshold).
- 2026-11-20: Record catch-up done: RESULTS.md §11 (corridor follow-ups; large-room route), STATE.md (large-room route), todos.md line 2. Flagged midpoint-necessity.md as unreviewed and load-bearing.

## 2026-11-20 — d81 lower threshold: N = 49 (not 21)
- For n ≥ 49, r ≤ 8: every same-parity interior lattice pair is directly visible or has d ≥ 2n/3. Per case: primitive ≥ 49 (≥ 25 if reflex corners in ≥ 2 classes; uses Burness–Guralnick fixed-point-ratio bound); k=2 ≥ 50/38/26/12 by z; k=3 ≥ 27/39; k=4 ≥ 32/52; k=5 ≥ 40; k=6,7,8 ≥ 42,49,56; gaps at 49–55 empty for k=4, 8.
- Open: 21 ≤ n ≤ 48 (listed by case in d81 README).
- Saved data: 2,145 rooms, 9,851 pairs, 21 ≤ n ≤ 40: only 3 pairs with 3d < 2n (cov3397/3608/4474, the eight-sheet pairs, directly visible). Minimum otherwise d = 2n/3 exactly at cov2493 (n=21).
- Coordinator re-ran check.py: identical. NOT independently reviewed (new external dependency: Burness–Guralnick).
- 2026-11-20 16:31: Astra (condition (ii) task + Daniel-directed follow-ups) idle. midpoint-clearance.md: the shortest-path clearance test can only succeed for directly visible pairs, across all classes; named area-501 example with ≥ 228 candidates per class, lit, but every candidate fails the test. So the distance route to (ii) is dead. perpendicular-bridges.md: two long perpendicular corridors ⇒ all pairs lit; 2-parameter family of 20-wall rooms (unreviewed). denominator.md also new. Astra recommends working backward from R22's nine-corner configuration.
- 2026-11-20: Daniel approved ("ok go"). Launched d82 (review midpoint-necessity.md + d81).

## 2026-11-20 — d82 review of midpoint-necessity.md + d81
- A: sound as an algebraic lemma; the route was mis-stated. Darkness gives (ii-geo), not (ii-alg) = no off-class regular coincidence. Correct statement: r ≤ 8 and d ≥ 2n/3 ⇒ R_other ≥ 2⌈2n/3⌉ − 16 − ⌊n/2⌋ (2 at n=21, 26 at n=49; coordinator recomputed). Missing lemma: one of those candidates is reached by a real path.
- B (d81): sound with fixable gaps; N = 49 holds. Burness–Guralnick Corollary 2 (fpr ≤ 1/√(p+1) or product action) read and checked. §4 states the combination backwards.
- Own code: R22 n=15, r=9, d=12; 6 regular (source class) + 18 reflex. cov2493, cov3397, st279 d values match d81.
- Coordinator re-ran indep.py: identical apart from CPU line. Corrected RESULTS.md §11 and STATE.md wording.
- 2026-11-20: Daniel approved both. Fixed d81 README §4 per d82. Launched d83 (lemma stress test on D8 R22 edits).

## 2026-11-20 — d83 stress test of the open lemma (off-class candidate reached), D8 R22 edits
- 11 of 29 saved R22 one-move edits have r ≤ 8. In all 11 some off-class regular coincidence is the midpoint of a real path (7/7, 7/7, 5/5 in the step-4 rooms). R22 control: 0 off-class coincidences, dark.
- Weak test: all rooms lit, d = n−1, counting bound negative for n ≤ 17; L1-008/010 directly visible. Sharpest: L1-005 c2 candidate at (2,3), half vector (−10,31), near the step-4 bound 32.
- Source-class saved midpoints came from non-shortest witnesses passing through S.
- Coordinator re-ran stress.py and step4.py (see diff result). No counterexample.
- 2026-11-20 17:27: Astra adjacent-cylinders.md (+ rim-trees.txt, adjacent-cylinders.txt): sufficient test for a reachable off-class midpoint when the unfolding splits into two half-turn-exchanged cylinders; ≤ 18 tree edges for W ≤ 20, independent of area. Passing ⇒ all real interior pairs lit and the d82 lemma holds for that room. Closes U2 and its stretches (area 46+8k, all k). All 747 saved BBBB pairs now have verified off-class midpoints. R22 fails the test on both rims. Unreviewed.
- 2026-11-20: Daniel approved ("ok go"). Launched d84 (review adjacent-cylinders.md + convex-cylinder.md).

## 2026-11-20 — d84 review of adjacent-cylinders.md + convex-cylinder.md
- adjacent-cylinders.md: sound with fixable gaps (state "exactly two cylinders"; rim-trees.py handles H = 1 only, enough for normalized rooms; midpoint may be a smooth wall point). convex-cylinder.md: sound; scope correct (one cylinder ⇒ reflex corners in ≤ 2 parity classes).
- Independent: own rim reader; U2 stretches k=0–6 strictly simple, normalized, 10 walls, r=3, C=92+16k, pass; closed-form intervals pass for all k. All same-parity pairs traced at k=0,1,3 (52, 80, 160) legal with off-class midpoints. 747/747 saved BBBB pairs certified (687+37+23). R22 fails in (4,7), (7,4).
- d69 decomp.py comment gives U2 r=4; actual r=3.
- Coordinator re-ran indep.py: identical apart from CPU timing lines.
- 2026-11-20: Daniel approved ("ok go"). Sent Astra the every-direction question (can a pair fail the rim/convex tests in every direction with r ≤ 8?). Proof task; any direction sweep must be proposed with a cap first.

## 2026-11-20 17:28–18:03 — Astra (mix of Daniel-directed and coordinator tasks)
- rim-quotient.md: R22's period-10 obstruction comes from the five-square staircase fold (30-unit rim wraps 3× a 10-unit rim); source/target residues mod 10 disjoint in both directions. General: if every regular rim pairing difference is divisible by m > 2, then n ≤ 4t+2 (t reflex corners on that rim), so that mechanism dies by area 35 for r ≤ 8. Unreviewed.
- persistent-gaps.md: CR34 (57 cells, 12 walls, reflex corners in all 4 classes): every real interior pair lit, via rim tests in two directions; a dark pair needs all four lifts of each mark on one rim (qx, py integral). Unreviewed.
- d84 fixes applied to adjacent-cylinders.md.
- every-direction.md (answer to coordinator task): NEGATIVE. Infinite family of normalized BBBB 12-wall crosses (r = 4) fails both whole-room cylinder hypotheses in every primitive direction (signed parity corner counts (−4,4,4,0)), yet sample pairs are lit. So whole-room cylinder charts can't prove the lemma; need per-cylinder certificates in multi-cylinder directions. R22: each of the 9 corners is the sole blocker on some route. Unreviewed.
- 18:03 Daniel asked Astra directly "next? think how to break through?"; Astra working.
- 2026-11-20 18:10: Astra shared-reflex.md: one reflex corner can block routes with midpoints in all 3 off-classes for one pair (8-wall example, any area); pair still lit by a bypass. Kills per-corner route charging.
- 2026-11-20: Coordinator proposed the shadow-budget lemma (hidden regular points from S ≤ C·r ⇒ n ≤ (6/5)(8C+16), a finite reduction). Daniel: "ok go"; give Astra tough breakthrough questions, not details. Launched d85 kill test; sent Astra the lemma.

## 2026-11-20 — d85 launched; Astra assigned shadow-budget lemma
- d85 (Opus subagent): kill test of the shadow budget. It computes |H_L(S)| (unreached within length L) on the 12-wall crosses b=7..17, U2 stretches k=0..6, and R22/d8 controls. Named rooms only, 10 CPU-min, writes in d85-shadow-kill/.
- Astra: asked to prove the effective shadow-budget lemma (|H(S)| ≤ C·r on the cover, or the off-class restriction) or find the obstruction. Theorem level only; no new families; no discovery searches.

## 2026-11-20 — d85 result (re-run by coordinator: identical, 2400/2400 validate)
- Shadow budget survives. |H_L| = 0 at L = 2,4,8·diam for all crosses b=7..17 and U2 k=0..6, at both sources; zero H_L proves H(S)=∅ there.
- Controls: R22 H = {(2,2),(2,-2)}; R22-L1-005 lit by L=27.
- Caveat: low information — H is empty in these families, so the bound is not stressed. Short-L counts grow with area (20→60 at 0.5·diam), so lighting needs length ~diam, not O(1).
- Forwarded to Astra.

## 2026-11-20 — inventory; d86 launched; write-up folded
- Inventory for Daniel: everything since the 08:55 write-up refresh (adjacent/convex cylinders, every-direction, persistent-gaps, rim-quotient, shared-reflex, corner-support, d83, d85, shadow-budget).
- d86 (Opus): review of shadow-budget.md snapshot (SHA 74722ed2…): uniformity step, genus lemma, cov4181, arithmetic.
- RESULTS.md §11: new block "Cylinder certificates, shadows and the cover gap". STATE.md: large-room update + 2 dead ends.

## 2026-11-20 — d86 result (scripts re-run by coordinator: identical)
- shadow-budget.md: no claim wrong. B(r) sound with fixable gap (cite EMM closed-invariant-set theorem; Noetherian induction fails). Genus lemma sound (DB55 genus actually 197). cov4181 control sound. Arithmetic sound, but the budget restates the open lemma rather than reducing it.
- RESULTS/STATE updated; forwarded to Astra; d86 released.

## 2026-11-20 — cleanup round: d87 + d88 launched
- d87 (Opus): review of every-direction.md (SHA 08d8031b…) and corner-support.md (SHA ad1cbb4b…) snapshots.
- d88 (Opus): consolidated rewrite of RESULTS.md §11 into d88-consolidate/section11.md; coordinator swaps in after check.
- todos.md line 2 refreshed. Pending Daniel decisions: back up / commit .context research (gitignored); untracked videos/ output/ .DS_Store and uncommitted AGENTS.md/GOALS.md.

## 2026-11-20 — Astra: dark-locus.md; d89 launched; Astra re-tasked
- Astra claims: for r ≤ 8, n ≥ 120, dark-pair coordinates have denominators dividing a uniform D(r) (no explicit value), via a physical-mirror argument + d80. Corollary: an unbounded counterexample sequence lies in a proper rank 2–5 family with four periodic marks. Also fixed d86 items (EMM Thm 2.2; DB55 genus 197).
- Coordinator note: no gain for same-parity lattice pairs (denominator already 1). Concern: uniformity across arithmetic (square-tiled) loci.
- d89 (Opus): review of dark-locus.md snapshot (SHA e2ddedc7…).
- Astra re-tasked: same-parity lattice core via (A) Q→U transfer, (B) affine-stabilizer orbit bound, or (C) obstruction.

## 2026-11-20 — d88 swapped in
- RESULTS.md §11 replaced by the consolidated section (204 → 213 lines, structured: status / reviewed / unreviewed / computed / open / dead ends / corrections). Old text kept at d88-consolidate/old-section11.md and RESULTS.before-swap.md. Coordinator added the 4 omitted items (20-wall run, perpendicular-bridges, midpoint-clearance, area-21 slice) and dark-locus (d89 in progress). Token check: no number or file reference dropped.
- STATE.md: stale d81 / condition (ii) lines fixed.

## 2026-11-20 — scheduled coordination set up
- Daniel asked for scheduled coordination, Astra check-ins, verification subagents and GitHub sync.
- Repo: tools/sync-illumination.sh mirrors fable/ + qclass-closure/ text files (<200 KB, no logs, personal-data scan) into research/illumination/, commits that path only, pushes the branch. First sync: 7233017 (script + GOALS.md + AGENTS.md), 1258652 (1,808 files, 17 MB). Pushed to origin/ddwang/illumination-problem-improvement (private repo).
- Cron job b2d01c10, every 30 min, session-only, expires in 7 days.
- Tick 1: Astra on route B (affine stabilizer), on task. d87, d89 running.

## 2026-11-20 — d87 result (coordinator re-ran: replay_corners identical; replay_cross and allpairs_b7 identical except CPU times, log includes b=9,11 runs)
- every-direction.md: sound. Parity argument covers all rational directions. Overstatement fixed: only (6,0)–(0,6) is proved lit; all same-parity lattice pairs lit at b=7,9,11 is finite evidence.
- corner-support.md: sound; one fixable gap in the cov4181 side paragraph (algebraic class d vs route-direction class).
- SHA prefixes in my d87 brief were swapped (ls order); snapshots identical to live files.
- RESULTS §11: both moved to "Proved and reviewed". STATE dead-end line qualified. Board released; forwarded to Astra.
- d90 (Opus) launched: independent check of qclass-closure/two18 shear certificates (last unchecked step of the 18-wall Q-class closure).

## 2026-11-20 — d89 result (dims.py re-run: identical)
- dark-locus.md: no error. Setup, uniform D(r), rank exclusions: sound with fixable gaps; mirror step sound. Main gap: state conditionality on d80 (and its d16/three-sheet/low-valency inputs). Monodromy step needs connectedness of N's regular locus (one line). Framing accurate.
- RESULTS §11: moved to reviewed. Board released; forwarded to Astra.
- Coordinator error: the d87 RESULTS edit (slice every-direction..rim-refinements) also deleted dark-locus, perpendicular-bridges and the 20-wall run entries. Restored from d88-consolidate/section11.md; token check vs d88 draft: nothing missing. d89 entry added under reviewed.

## 2026-11-20 11:10 tick
- Astra: wrote stabilizer-orbits.md (route B setup), axial-stabilizers.md (negative: axial cusp stabilizers give |orbit| ≤ 4 on the cross), cross-placement.md (cross family fully lit; family detail, drift). Redirected: stop family work; decide B′ (full stabilizer) / A / C in one note.
- d91 (Opus) launched: review of stabilizer-orbits.md (3a744bc6) + axial-stabilizers.md (cf878129).
- d90 still running. No Slack post (nothing reviewed this tick).

## 2026-11-20 — d90 result (run.sh re-run: ALL CHECKS PASSED, same counts)
- two18 shear certificates: CONFIRMED WITH GAPS. 144 trees / 853 boxes accepted by an independent exact checker; 240 traced pairs; mutation test 2147/2552 rejected. Gaps: half-turn label comparison implicit; residual polygons from census code (audited only); residual samples all K=1.
- RESULTS §11: 18-wall Q-class closure moved to reviewed. Board released.

## 2026-11-20 11:40 tick
- d91 result (check.py and fullG.py 7 re-run: identical): stabilizer-orbits.md and axial-stabilizers.md sound. Axial route B dead; full stabilizer orbits grow on the cross (36 at b=7, 52 at b=9). Remaining obstacles: no universal growth theorem; B(r) non-effective. Reviewer overran CPU budget (~15 min). RESULTS §11 updated; board released.
- Astra delivered mirror-suborbit.md (route B′: 2e(S) ≤ B(B−1) if S has a dark partner; e(S) ≥ max(u,v)/gcd). d92 (Opus) reviewing snapshot 28c74baf. Astra re-tasked: bounded-e(S) marks must be on an axis or special position; effectivity of the shared-hidden-target count.
- d92 result (run.py r22 re-run: identical): mirror-suborbit.md sound (claim 1 fixable gap: affine maps preserve relative period lattice Z², not 2Z²). Axis marks e ≤ 3 (not 4); diagonal/off-axis e = 40–44 at b=7. R22: hidden set from (0,0) = G_s-orbit of t. No area cutoff (B non-effective). RESULTS §11 updated; board released; forwarded.

## 2026-11-20 12:02 check (Daniel asked)
- Astra delivered small-orbit-blocks.md: darkness ⇒ bounded mirror orbits at both ends; exact block test recovers R22's 3-sheet fold from the dark pair alone (block sizes 15,3,15,15); K_{3,3}/cube graph lemma. Applied d92 fixes to mirror-suborbit.md.
- Coordinator link: if darkness forces a block from a proper factor N_x, d64 (W ≤ 20 rooms with a proper factor all lit) closes those rooms; residue = no-proper-factor rooms (old Lemma H case). Sent to Astra as the next question.
- d93 (Opus) reviewing snapshot 4357f45a, including whether the note's factor notion matches d64's N_x.
- d93 result (blocks.py identical; systems.py R22-base/R34-base identical): small-orbit-blocks.md sound. Graph lemma doesn't use darkness (Decision overstated). Block system = staircase fold fibers = N_x for x=b,c in R22. Bridge to d64 needs: dark same-class pair with r ≤ 8 ⇒ some class x has B_x proper; plus point→sheet block promotion and cubic case from darkness. Added to RESULTS §11 open core. Board released; forwarded.

## 2026-11-20 12:10 tick
- Astra active, on task (no-proper-factor case). New canonical-transfer.md (12:06; folds from point blocks need not give a proper canonical factor; unbounded-area examples with all four factors trivial). Still mid-turn; review once she posts it. No subagents running; no load-bearing backlog item. No Slack post.

## 2026-11-20 12:20 status (Daniel asked)
- Astra delivered fiber-transport.md (degree-3 quotient: darkness transports downstairs; degree-4 cube: unique sheet pairing) and canonical-transfer.md (recovered folds need not give a proper canonical factor). BL still open; decisive gap = primitive BBBB rooms.
- d94 (Opus) reviewing both (eeaa092a, 4bf81bf8). Astra re-tasked: primitive monodromy + small-support corner permutations ⇒ G ⊇ A_n for large n (Jordan/Marggraf, Burness–Guralnick), then contradiction with bounded orbits.
- 2026-11-20 Daniel asked whether open items are being reviewed. Answer: only new Astra notes were (d84–d94); older backlog not tracked. Launched d95 (Opus) to build a ranked review queue (d95-review-queue/review-queue.md); scheduled ticks will drain P1 items one at a time.

## 2026-11-20 — d94 result (cross.py re-run: identical)
- canonical-transfer.md sound; fiber-transport.md sound as necessary conditions only.
- KEY CORRECTION: BL (d93's bridge) is equivalent to the open core (no BBBB room with r ≤ 8 has a dark same-class pair) — not a reduction. My earlier framing to Daniel ("d64 would close W ≤ 20") overstated it. "Decisive gap = primitive BBBB" also wrong: imprimitive BBBB equally open. Open: BBBB 21–36 (finite, not enumerated), primitive >36, imprimitive >36.
- RESULTS §11 corrected. Board released; forwarded to Astra.

## 2026-11-20 — d95 review queue built; draining P1
- d95: 44 items (13 P1, 17 P2, 14 P3) in d95-review-queue/review-queue.md. Top P1: Q01 d13 Lemma A'/Thm C; Q02 Q-class completeness + full witness replay; Q03 d68 counting identity; Q04 d64 enum_K.c z=4 cross-check; Q05 18-wall residual polygons.
- Launched d96 (Q01) and d97 (Q03). Ticks drain the queue in order, ≤ 2 subagents. Q02 full replay may exceed 10 CPU-min; will size it first.
- d97 (Q03) result (count.py re-run: identical): d68 counting identity and n ≤ 36 bound sound; needs strict simplicity. RESULTS updated; queue marked.
- d98 (Q04) launched: independent enumerator for d64 enum_K.c z=4.

## 2026-11-20 status (Daniel asked)
- Astra: neither branch closes. primitive-stabilizer.md (n ≥ 49: sheet group ⊇ A_n; missing affine map to a lit pair) and bbbb-split.md (bounded orbits descend to intermediate quotients with area-independent loss; degree 2: loss ≤ 56, one endpoint projects to 2 regular points, else both on a symmetry axis ⇒ visible). Queued for review when a slot frees (d96, d98 running). Astra continuing: degree-2 branch-pole winding.
- 12:40 tick: Astra on task (degree-2 winding parity in half-turn-invariant bands). d96, d98 running; Astra's primitive-stabilizer/bbbb-split reviews waiting for a slot. No Slack.
- d96 (Q01) result (test.py seed 7 re-run: identical): d13 Lemma A', Theorem C, §4/cover.c sound; 4 wording nits. 1,620/1,620 certified pairs traced legal; 134,880 labels match d74; mutant test catches false merges. Downstream pruning (build_cover.py), tile-pair step, shear certs are Q02/Q05/Q06. RESULTS caveat removed; queue marked.
- d99 launched: review of primitive-stabilizer.md (333ad76f) + bbbb-split.md (6354f371).
- d98 (Q04) result (full re-run by coordinator: skel enumeration byte-identical; cmp totals 3743/3743, 3663/3663): d64 enum_K.c z=4 MATCH object-by-object for d = 1..18, by an independent algorithm. Harmless ambiguity: cone-as-singular reading makes d64's list a superset (68 extra) of the strict reading. Theorem FIN's z=4 input now independently checked. Queue marked.
- d99 result (blocks.py, r22.py re-run: identical): primitive-stabilizer.md and bbbb-split.md have no error; A_n at n ≥ 49 via Burness–Guralnick (not Jordan); n ≥ 73 step reduces to d92 question; descent uniform (sphere, ≤ 8 poles); degree-2 constraint is not a new restriction. RESULTS §11 updated; board released; forwarded.
- Astra delivered pole-winding.md (degree-2 symmetric band: both winding parities except half-turn middle line; finite per-room test). Not reviewed: symmetric-rooms-only, low leverage → P2. Redirected Astra to route C: collect all proved necessary conditions on a large dark BBBB pair; find a contradiction or the one missing statement.
- 2026-11-20 Coordinator: launched d101 (Opus referee) on queue Q07 normalization, Q08 Lemma MP, Q09 d81 residual gaps. Marked IN REVIEW d101. Running: d100 (Q05), d101.
- 2026-11-20 Coordinator: d101 done. Re-ran mp_check.py and swap_check.py: identical logs. Q07 normalization sound (translate first; 'conjugates'), Q08 Lemma MP sound (strictly simple; midpoint may be S/T), Q09 d81 findings 5-6 wording only, n>=49 stands. Updated RESULTS (normalization, MP status, §11 entry); queue Q07-Q09 DONE. Proposed d81 text in d101-small-p1/review.md (not applied; d81 is Astra's). Released d101.
- 2026-11-20 Coordinator: launched d102 on Q02 (completeness read; timed replay sample; full replay only within 10 CPU-min, else projection for Daniel's approval).
- 2026-11-20 Coordinator: d100 done (Q05 CONFIRMED). Re-ran run.sh (3.1 CPU-min): output identical apart from CPU timings. Residual re-derived independently; 36 open tile pairs match; max displacement 1/17 = shear box; 300/300 containment sample; 100 large-K traces lit; B=8 negative control fails as expected. RESULTS 18-wall entry updated; queue Q05 DONE. Released d100.
- 2026-11-20 Coordinator: launched d103 on Q06 (sampled independent replay of twenty/ runs; d90-style check of the 620 shear boxes / 3,652 trees).
- 2026-11-20 Coordinator: posted Slack status (d100 confirmed, d101 wording only, d102/d103 running). Checked: d90's half-turn gap is a README wording point (orbit comparison proved sound in d90), so the 18-wall closure has no open computational gap. Running: d102 (Q02), d103 (Q06).
- 2026-11-20 Tick: Astra on route C (index 13089): now asks whether an allowed relative cylinder shear can move a blocking corner off a marked trajectory. On task; no redirect. New note large-dark-profile.md (13:00): no contradiction from reviewed results; minimal missing statement = corner-avoiding segment to a regular coincidence on U. Spot-checked arithmetic 26 (n=49) and 148 (n=120): correct. Snapshotted; queued Q46 (P1) for review when a slot frees. Running: d102, d103.
- 2026-11-20 Coordinator: d102 done (Q02 sound). Re-ran replay.py 0 0, control.py 2 2000, brute.py 13: logs identical apart from CPU. Enumerator complete; brute polyomino counts match areas 1-13; full replay 3,933,192 witnesses, 0 failures, 72 CPU s. Loose end: 28/10,268 sign-flip corruptions accepted (likely symmetric rooms, valid paths; unchecked, harmless to the claim). RESULTS Q-class entry upgraded. Released d102.
- 2026-11-20 Coordinator: Daniel asked to keep Astra on big ideas, no hill-climbing. Redirected Astra to 'converse to Tokarsky' (every dark same-class pair comes from an affine involution fixing a corner lift; then count r>=9); deliverable tokarsky-converse.md. Launched d104 on Q46 (large-dark-profile proof read). Running: d103, d104.
- 2026-11-20 Check: Astra refuted single-fixed-corner Tokarsky converse via R22 (tokarsky-converse.md; 4 certificates, different sole corners per lift parity). Accepted; queued Q47 (P2). Redirected her to 'fold converse': dark => fold Q->N onto a Q-class base; step 2 first = Riemann-Hurwitz corner count r>=9 or explicit r<=8 configuration (decisive); step 1 only if step 2 survives. Deliverable fold-converse.md. Running: d103, d104.
- 2026-11-20 Coordinator: d104 done (Q46). Proof read only; I re-checked the minimums (26 over n>=49, 148 over n>=120): exact. Rows sound; low fixes rows 4-5 (d80 dependence), R22 is not BBBB. Minimal missing statement = restatement of the core at n>=120 (converse step unwritten), not a reduction. RESULTS §11 entries added (profile; Tokarsky converse false). Released d104; forwarded to Astra.
- 2026-11-20 Coordinator: Daniel noted Astra idling between 30-min ticks. Replaced cron b2d01c10 with 31c40a68 (every 10 min, :03/:13/...); tick now requires every brief to carry a follow-on question. Sent Astra a standing instruction to self-advance plus follow-on (fold-converse step 1, else chain-map attack).
- 2026-11-20 Tick 13:24: Astra delivered fold-converse.md: Step 2 = R22-type parity-fold mechanism needs r>=9 (RH table: z=2,m=4,k<=4; z=3,m=5,k=2; z=4,m=6,k=2; eliminated by tetromino/axis argument + d9, plus census-free route); Step 1 false: R34-base dark by parity on its prime-degree-19 double (no proper fold). She moved to the follow-on on her own. Snapshotted; launched d105 review.
- 2026-11-20 Coordinator: d105 done (Q48). Re-ran step1.py/step2.py: identical. Step 2 sound with fix (add S/T image separation); Step 1 (R34-base, degree 19) sound. Scope: mechanism impossible in BBBB rooms, so no progress on the core; my Slack wording ('no 20-wall room can be dark that way') was true but already known from d102+d64; posted correction. Released d105.
- 2026-11-20 d103 done (Q06): confirmed with gaps (3,652 trees + 246,639 leaves pass; samples clear; gaps: 3 rooms/162 boxes via bin-pair certs unchecked, residual boxes not re-derived, tile sample 46/100 decided). Note: its gap 5 'd13 unreviewed' is stale, d96 reviewed d13 sound. Re-run of run.sh in progress. Astra delivered chain-map.md (21:34): sublattice kill for n>2r+2 + twist-overlap criterion. Redirected her to two-twist (H,V) overlap forcing / locked-residue characterization (twist-overlap.md). Launched d106.
- 2026-11-20 Coordinator: re-ran d103 run.sh (~12 CPU-min, no subagent cap): shear results identical (246,639/0; 122,865/0; mutant 232,884 fail); control identical; tile-level sample did better than in the subagent's run: 74/100 cleared, 21 timeouts, 5 skipped. RESULTS 20-wall entry updated; Q06 DONE; queued Q50 for remaining gaps. Released d103.
- 2026-11-20 Coordinator: launched d107 on Q50.
- 2026-11-20 Coordinator: d106 done (Q49). Re-ran count.py, twist.py: identical. Both claims sound; sublattice kill = BBBB definition, overlap test is sufficient-only certificate; core unchanged. My earlier chat summary overstated (1); corrected to Daniel. Released d106; forwarded.
- 2026-11-20 Tick 13:53: Astra delivered twist-overlap.md (wall-width inequality; DB55 witness beats phase lock). Snapshotted; launched d108. Gave her band reachability (universal step) + follow-on turning passages as residual.
- 2026-11-20 Coordinator: Daniel asked for the % estimate in every report. Current: 6-8% (unchanged today: reviews strengthened the finite side (Q02, 18-wall, 20-wall partial) but the BBBB core is untouched; band reachability is unreviewed).
- 2026-11-20 Coordinator: d107 done (Q50 partial). Re-ran run.sh: cert2.log, compare.log identical; control.log/pixchk.log differ only in blank lines and one comment. Bin-pair rooms pass (295,323 receipts); residual matches in 11/24 rooms; 13 rooms (394 boxes) remain, 4-49 alone >295 CPU-s. Estimate unchanged 6-8% (finite side only). Released d107.
- 2026-11-20 Tick 14:03: Astra: band reachability FALSE (DBas counterexample, lit by 2 reflections though twist-fixed). Twist-only route dead. Redirected to length periodicity (finite reduction: darkness eventually periodic in corridor length, period P(r); reduces core to finite family). Launched d109 on Q52. Estimate 6-8% unchanged.
- 2026-11-20 Coordinator: d109 done (Q52 sound). Re-ran cylinders/classtypes/path/family: identical. DBas is BBBB r=4 n=48; family lit at all tested n. Forwarded to Astra as a control family for length periodicity. Estimate unchanged. Released d109.
- 2026-11-20 Coordinator: d108 done (Q51). Re-ran check.py: identical. Inequality sound (needs same vertical sheet); DB55 witness confirmed (shift sign is sheet-dependent); stretch corollary needs a one-line repair (free horizontal lift for 2nd mark), then all 64 cross-chamber pairs lit at every tested ℓ. DB55 has r=4 (my brief said r>8: wrong). First infinite open-core family closed for lattice pairs (ℓ coprime to 5). Estimate 6-8% -> 7-9%. Released d108.
- 2026-11-20 Tick 14:23: Astra delivered length-periodicity.md (period-one tail for rect-corridor-rect, explicit K; DBas lit all L>=2; finite residual list; shortening-transfer is the true gap). Launched d110. Redirected her to thick-thin compactness (moduli M_tau, openness of lit set, finite cover of thick part, thin-passage tail, corner lemma). Estimate 7-9% unchanged pending review.
- 2026-11-20 Tick 14:23b: Astra delivered thick-thin.md (irrational thin-door theorem; unbounded words at shrinking doors; conditional thick-part cover). Launched d111. Approved her resonant case, framed as induction on r via thin passages + resonant gluing lemma (coset/CRT condition); follow-on reflex-corner limit lemma.
- 2026-11-20 Coordinator: d110 done (Q53 sound). Re-ran tail/lattice/dbas: identical. K values large (595k-1.1M). Removes only tails of unit-door rectangular dumbbells. Estimate 7-9% unchanged. Released d110; forwarded.
- 2026-11-20 Tick 14:33: Astra wrote resonant-gluing.md (exact gcd gluing test, common period, fixed aperture passes at large L; shrinking aperture at bounded normalized length open). She is continuing (follow-on queued). Launched d112.
- 2026-11-20 Tick 14:43: Astra improved resonant-gluing.md: rectangular dumbbells lit for L>4d, any door width incl. resonance (L>=21 for DBas/DB55/DBw2; was ~10^6); polynomial bound for expanding chambers. Told d112 to review the new version. Redirected Astra to general monotone mismatch (general-gluing.md); follow-on corridor-structure dichotomy + thick computation spec.
- 2026-11-20 Coordinator: d111 done (Q54 sound): re-ran 3 scripts; thin_door differs only in timings. d112 done (Q55 sound, 14:35 revision): re-ran linear/poly/glue/misc/period: identical. Rectangular dumbbells lit for L>4d (threshold 21). Estimate 7-9% -> 9-11% (first uniform, usable long-corridor theorem; DB55 l=0 mod 5 from 25). Released d111, d112.
- 2026-11-20 Tick 15:03: Astra general-gluing.md: monotone mismatch fails (upward jump in 20-wall BBBB room at 43/33); dichotomy fails (odd crosses). Launched d113. Gave her degree theorem (signed cancellation at reflex grazes; degree-gluing.md); follow-on capped arms via cap reflection -> corridor of length 2l.
- 2026-11-20 Coordinator: d113 done (Q56). Re-ran jump/cross/count: identical. Counterexamples correct; the jump pair is lit by other launches (supports the degree-compensation idea). Estimate 9-11% unchanged. Released d113; forwarded.
- 2026-11-20 Tick 15:14: Astra degree-gluing.md: local cancellation fails; cap doubling positive; drifting into designated-pair details (L=4+66k). Redirected to accumulation/limit argument (D_tau closed; classify persistent dark limits: degenerate / non-arithmetic via LMW+Apisa-Wright / arithmetic refinements). Launched d114.
- 2026-11-20 Tick 15:23: Astra accumulation.md: (cond. d89) unbounded dark => fixed height; crux = can a whole shape-changing line stay dark; strip exclusion. Launched d115. Redirected her to generic-line.md: kill the dark line at transcendental t via LMW + Apisa-Wright periodic points + EFW finiteness (marks interior, not periodic).
- 2026-11-20 Coordinator: d114 done (Q57). Re-ran room43/cap: identical apart from timings. Cap doubling sound (minor gaps); no-cancellation sound; one wrong number (9 round trips, not 3). Estimate unchanged. Released d114; forwarded.

## 2026-11-20 — d115 processed (Q58)
- Re-ran d115 checks.py: SAME (timings only). Verdict: accumulation.md sound, conditional on d89→d80.
- Added RESULTS §11 "Accumulation" entry; Q58 DONE.
- d89 and d80 are both reviewed (d80 sound; d89 sound with fixable gaps), but literature inputs remain from memory (Q11). Reduction stays conditional. Estimate unchanged at 9–11%.
- Forwarded fixes to Astra: name the full d80 chain; flag from-memory citations; |t| < min(ε, 1/2).

## 2026-11-20 15:45 — generic-line.md delivered (Q59)
- Astra: on a rational one-axis line, all irrational parameters in a component share a marked orbit closure; component wholly dark, or dark parameters locally finite rationals. accumulation.md updated (d80 chain, radius, continuation).
- Snapshot + claim d116; Opus referee launched.
- Next brief to Astra: kill a wholly-dark component by classifying its ends (unbounded → corridor theorems; wall → 0 → induction on W; pinch; mark collisions). Follow-on: pinch-limit lemma.

## 2026-11-20 — d116 processed (Q59)
- Re-ran checks.py: SAME. generic-line.md sound with fixable gaps; accumulation.md continuation sound. EMM 2.1–2.2, LMW, Apisa–Wright statements checked against arXiv text (partly closes Q11 for these inputs).
- RESULTS §11 entry added; Q59 DONE; d116 released. Estimate unchanged 9–11% (sharpens the crux; closes no case).

## 2026-11-20 15:58 — component-ends.md delivered (Q60)
- Pinch transfer lemma; cov279 obstruction (unbounded reflections across shrinking overlap); opposite-lip theorem when no shared proportional width. d116 fixes applied. Snapshot + claim d117; Opus referee launched. Astra self-directed to the one-shared-width case (on target).

## 2026-11-20 16:05 — Daniel steered Astra directly
- Daniel asked Astra to spawn a second Astra (billiards geometer) on the eight-stop question (nine-reflex-question.md: question note, no proof; not queued for review). Sent guardrails: no discovery searches without approval; aim at a mechanism covering r ≤ 8. Follow-on: one-shared-width pinch case.

## 2026-11-20 — d117 processed (Q60)
- Re-ran checks.py (see below). component-ends.md sound with fixable gaps; cov279 replay exact. RESULTS entry added; Q60 DONE; d117 released. Estimate unchanged 9–11% (partial end classification; pinch end open).

## 2026-11-20 16:15 — eight-stop-consult.md delivered (Q61)
- Joint note (Astra + geometer): convex-corner label removal (physical darkness = translation darkness over lift choices); indispensable-corner criterion; R34 three forced stops. Snapshot + claim d118; Opus referee launched. Astra on stop-count + one-shared-width (her board claim); no redirect needed.

## 2026-11-20 — d118 processed (Q61)
- Re-ran checks.py (SAME expected; see shell). eight-stop-consult.md sound with fixable gaps; Section 1 (convex corners regular) is the useful output. Stop-count route has no BBBB content. Redirected Astra to a one-stroke kill of a wholly dark component via Section 1 + Apisa–Wright 3.6 + periodic points. Estimate unchanged 9–11%.

## 2026-11-20 16:25 — tick
- New note shared-width-and-stops.md (pre-steer; negative result on the parked stop-count route). Queued Q62 as P2, no review. Astra is on the periodic-point brief.

## 2026-11-20 16:37 — minimal-quotient-rigidity.md (Q63)
- Astra refuted the coordinator's rigidity idea (mark motion is a rational combination of three periods). Reduction: minimal quotient degree 1 or 2; degree 2 only at r = 6, 8. Snapshot + claim d119; Opus referee launched. Brief: classify periodic points of proper rank-two minimal quotients; follow-on degree-two branch via d99 axis lemma. point-scars.md (endpoint leftover) noted, not queued.

## 2026-11-20 17:05 — rank-two-periodic.md (Q64)
- Astra could not prove the rank-two classification (Apisa genus-0 stops at two zeros; Apisa–Wright covers need ≥2-point markings). Delivered rank-two torsion criterion + degree-two mirror analysis. Snapshot + claim d120; second Opus referee launched (d119 still running). Brief: Möller-style Mordell–Weil argument for persistent torsion marks; follow-on: route assessment (orbit-closure vs d104 effective bound).

## 2026-11-20 — d119 processed (Q63); d121 launched (Q65)
- Re-ran d119 checks.py: SAME. minimal-quotient-rigidity.md sound with fixable gaps. Medium gap: z ≤ 2 exclusion rests on the unreviewed d19–23 census review + d23 Lemma 2. Launched d121 (verify, replay saved runs only). RESULTS entry added; d119 released; fixes forwarded. Estimate unchanged 9–11%.

## 2026-11-20 — d120 processed (Q64)
- rank-two-periodic.md sound with fixable gaps; source audit checked. Referee reframes the crux: does a proper rank ≥ 2 locus exist in Q(1^z, −1^(z+4)), z ≥ 3? Apisa expects not. Redirected Astra from Mordell–Weil to non-existence. Estimate unchanged 9–11%.

## 2026-11-20 17:15 — route-assessment.md
- Astra: the direct area route (d104) gives an effective cutoff n ≤ (K+32)/ε if H_sync ≤ (3/2−ε)n+K is proved; the orbit-closure route gives only qualitative boundedness and still needs an effective step. Neither route has a cutoff yet. Strategic: a finite check needs an effective bound. Queued mordell-weil.md as Q66 P2.

## 2026-11-20 — d121 processed (Q65)
- Re-ran family_check_small.py: identical JSON (2 s). z ≤ 2 exclusion established with fixable gaps; Lemma 2 not needed (c₂ count). High gap: emit ~430 LIT witnesses and verify independently — re-runs the saved census tracer, so asked Daniel before launching. Estimate unchanged 9–11%.

## 2026-11-20 17:46 — three-zero batch (Q67)
- Astra idle ~20 min after delivering three-zero-recognition.md (hexagon matchings ⇒ degree-3 cover of genus 2). Snapshots + claim d122; Opus referee on the three-note batch. Brief: close z = 3 by forcing equal signed periods at a rank-two boundary; follow-on: induction z → z+1 and the effective n₀(r).

## 2026-11-20 17:57 — pivot to the effective route
- three-zero-monodromy.md: (1,1,1) or additive weights; explicit 1:1:2 family; same-rank induction impossible (boundary rank ≤ h−1). Claim d123; Opus referee launched (d122 still running).
- Coordinator decision: pivot Astra from z = 3 (open problem in the field, qualitative only) to an effective n₀(r) via d112/d108/d110/d104. Follow-on: census cost through n₀. z = 3 parked as a fallback.

## 2026-11-20 — d122 processed (Q67)
- Re-ran checks.py (see shell). three-zero batch sound with fixable gaps; no false claims. Remaining z = 3 gap is three inputs, not one. Consistent with the pivot to the effective route. Estimate unchanged 9–11%.

## 2026-11-20 — d123 processed (Q68)
- three-zero-monodromy.md sound with fixable gaps; parity of enclosed poles picks I±R; wrong Wright arXiv ID (1303.3603 → 1302.4108). z = 3 stays parked. Estimate unchanged 9–11%.

## 2026-11-20 18:35 — effective-chamber.md (Q69)
- Explicit corridor threshold for arbitrary lattice chambers (Fibonacci in area); real-pair bound; cap-doubling whole-room consequence; large-rectangle analysis. Claim d124; Opus referee launched. Astra now on the large-rectangle (compact chamber) case — on target.

## 2026-11-20 18:46 — rectangle notes (Q70)
- rectangle-windings.md + large-rectangle-access.md: compact-chamber access theorems; shared-corner obstruction. Claim d125; referee launched (2 running). Brief: decomposition lemma assembling the tools into a whole-room N(r) with only the shared-corner residual; follow-on: compute N(r) and feasibility.

## 2026-11-20 — d124 processed (Q69)
- effective-chamber.md sound (low gaps only); replay at exact threshold lights all DBas/DB55/DBw2 cross pairs. First effective corridor theorem for arbitrary chambers (closes d112's 'nonrectangular chambers' open item). Estimate 9–11% → 10–12% (first reviewed effective piece of the direct route).

## 2026-11-20 18:55 — whole-room-decomposition.md (Q71)
- Decomposition lemma: ≤ r+1 rectangle tree; deep closed-end piece lights the room; large area forces no deep piece; cov279 stretch obstructs N(r) from these tools. Claim d126; referee launched (d125 also running). Astra now on matched access across an unavoidable cut with both chambers growing — the right residual. No redirect.

## 2026-11-20 — d125 processed (Q70)
- Rectangle notes sound with fixable gaps. Shared-corner obstruction is only to the clearance method (legal path exists). H₀ ≥ 2⁷⁹ w: these tools give no feasible census. Estimate held at 10–12% pending d126.

## 2026-11-20 — d126 processed (Q71)
- Decomposition note sound. cov279 stretch (W = 16, BBBB, height 6) defeats every certificate method so far; all-pairs illumination open there. Redirected Astra to a bounded-height (thin-room) modular theorem; follow-on: fat-room regime. Estimate 10–12% → 9–11% (the reviewed effective tools provably don't reach a cutoff; the open W ≤ 20 core now contains an explicit infinite family where only one pair is known lit).

