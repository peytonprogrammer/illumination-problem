# D234 outsider report

Advances: L1 (route choice only; no lemma claimed).
Independent ideator, 2026-11-25. No searches, censuses or tracers run; one reading audit done.

## Verdict

I offer one candidate: a cheap distinguishing test, not a proof route. I found no theory route with new leverage. L1 is an effective "dark implies fold" theorem for marked torus covers. Each idea I tried restated the finite SL(2,Z)-orbit test or hit the H(C) gap. My estimate that any theory route moves L1 within a week is 2% (guess).

## Candidate 1: immersed-disc control

**Leverage.** This is a distinguishing test. Every room hypothesis falls into one of three layers:

1. Stratum data: genus r + 1, square-tiled.
2. Reflection structure: V4 deck group, a genus-0 double with every cone point on the seam, and no pinches.
3. Planarity: the developed disc is embedded.

d140 shows that layer 1 alone allows dark pairs (an all-dark 8×8 genus-9 example; genus 9 is the r = 8 genus). Rooms have all three layers. Immersed orthogonal discs have layers 1 and 2 but not layer 3. Nobody has tested lighting on them. The test answers one question: is planarity load-bearing?

- If a non-embedded immersed disc with r ≤ 8 has an uncertified dark pair, darkness at r ≤ 8 has a non-fold mechanism intrinsically. Any L1 proof must then use embedding. Folds are already excluded for immersed discs (d52 says so explicitly).
- If none is found, a proof can be stated for immersed discs. That is weak evidence only.

**Closest earlier attempts.**

- d52 enumerated 13,876 immersed W-sets with n ≤ 9, but it checked certificates only, not lighting.
- d55 checked lighting only on slit and pinched rooms. Those are degenerate, and every dark pair it found was fold-certified.
- d140 and d141 covered abstract surfaces and half-turns.

What differs here: lighting on non-degenerate immersed discs, which sit between d140 and rooms.

**Cheapest test (hand check, done).** I predicted that every reviewed L1 tool holds verbatim for immersed discs, and that only the censuses (d9, d29, d64, d205, Q-class closure) use embedding.

Partial result, confirming the prediction:

- The d68 star identity, the d36 5r bound, the d105 counting and d52 are intrinsic. d52 says so explicitly.
- Chart descent uses embedding only to stay in the class. Its own note says, "Increasing coordinate changes separately in x and y preserve the boundary embedding" (l1-growth-modes.md). Such changes also preserve immersions.
- d231 Lemma 1 and the d228 sign cone are local.

I didn't audit every note, so "all tools are planarity-free" stays a guess.

Here is the decisive follow-on. Run a lighting check of non-embedded immersed discs with W ≤ 20 at small area, reusing the d52 enumerator and the d205 tracer. This is a census, so it needs Daniel's approval. Guessed cost: under one CPU-hour at area ≤ 16. Prediction: P(an uncertified dark pair) ≈ 5% (guess).

**Stop result.** Stop if the approved run finds no dark pair. Also stop if a full audit finds a reviewed L1 lemma that is false for immersed discs. In that case the control doesn't separate the layers.

**Probability it moves L1: 1%.** It can't prove L1; a positive result rules out every planarity-free route.

## Considered and dropped (overlap with earlier work)

- **Continued-fraction depth of witnesses.** Bounded axis switches with free partial quotients fit d129, d130 and d233, for example (a+1, 1) and (7+1040j, −2). Gap ratios have unbounded depth, so the quotients must follow the Euclidean algorithm on the gaps. That is band stabilization and multitwists (d28, d41, d156).
- **Per-direction component graph.** In class x, Γ_v has at most (f + 3r)/2 ≤ 2r + 2 path components after cutting at reflex points. Counting them doesn't force S and T together. Same ground as d149, d151 and d86.
- **Uniform spectral gap for origami curves.** This is effective EMM, which is ruled out. I know of no uniform gap result (guess).
- **Thick-part compactness.** Same ground as d115 to d123. It isn't effective.
- **Per-class corner budget.** Already in class-wall-budget.md. In cov4181, orbit exclusion blocks a class at zero reflex cost.
- **Rigid dark points.** Finitely many itineraries surround an isolated dark point, which bounds its height by their complexity. Nothing bounds that complexity (d233). This is d187.

## Overlap with the coordinator's held-back ideas

- My dropped Γ_v item overlaps "leaf-sharing per primitive direction" (d149, d151).
- My rigid-point item overlaps "diagonal scaling and rigid dark points" and "degeneration of flats".
- Candidate 1 overlaps none of the five. It complements the held-back W = 10 test: that test asks whether current tools reach any word, and mine asks which hypothesis a method must use.

## Most surprising reviewed result

d140: an abstract square-tiled surface of genus 9 (8×8) where all 64 pairs are dark. The darkness is midpoint blocking under a free half-turn. Genus 9 is exactly the r = 8 genus.

So stratum-level arguments (monodromy, EMM, Siegel–Veech) can't prove the goal alone; the reflection structure must do the work. d141 shows the mechanism in rooms: a free half-turn must be a physical symmetry. Immersed discs are the untested step between d140 and rooms.

## Recommendation

Don't open a theory route. If Daniel wants one more cheap structural signal, approve the immersed-disc lighting run. Otherwise choose between the area-22 falsification census and stopping to write up.
