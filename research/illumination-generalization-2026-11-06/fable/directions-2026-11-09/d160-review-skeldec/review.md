# d160 review: skeleton-decidability and time-pairing chart cover (snapshots 2026-11-22 04:55)

**Verdict: sound with gaps.** Every traced claim checks out exactly. The chart-cover argument is correct. The 6-wall L claim holds on all 448 grid rooms, and each per-wall condition is an exact iff there. The non-Presburger conclusion is right for words of length 0 and 1. It refutes only the Presburger route, not decidability. It doesn't contradict d132. The gaps concern how the decidability conclusion is framed, not any computation.

Files: `checks.py` and `checks.log`. Total CPU time is 1.7 s. The script loads the d159 polygon builder, tracer, `piece()` and `build_chart()` unchanged, and adds an exact tracer that detects arrival at T. It uses only named rooms: R22-base, R22-L1-005 and the note's L(x,y,z). The only direction enumerations are a 7-shot image list per L room and one fixed-room sweep in R22 (|p| ≤ 3, |q| ≤ 4).

## 1. Chart cover (time-pairing, "Complete charts including smooth endpoints")

- **R22 replay.** From (0,0) in direction (2,3), the ray reflects at (2,3) and then (4,0). The lattice status of both points is `smooth`, and neither is a vertex. The ray then reaches (14/3,1) in the open wall from (4,1) to (5,1).
- **Cut events.** The ray crosses x = 1 and x = 3 at y = 3/2, inside the open piece (1,2). At x = 2 and x = 4 the crossing is a cut endpoint. The vertical velocity flips once at each, + to − at (2,3) and − to + at (4,0). The incoming and outgoing germ cells are (1,2)→(2,2) and (3,0)→(4,0). All four are room cells, and the reflected side is the room side. The strict d159 column chart still rejects this ray at u = 2, so the new local rule is what admits it.
- **Consistency sweep in R22.** The sweep traces 8 reflections in each primitive direction from (0,0). It finds 88 smooth contacts, of which 14 are at lattice smooth points (cut endpoints), and 32 vertex stops. The note's local rule agrees with the tracer at every contact.
- **Argument.** Correct in both directions. A legal shot has finitely many legs, and each leg meets the finite cut grid in finitely many points, so subdividing it gives a chart. Conversely, checked germs at every event, plus interiors that stay in named cells, glue to a specular path with no corner contact. The axial clause is also right: a ray from an interior mark meets a smooth wall only normally.
- **Archived R22-L1-005 word.** For displacement (18,−12), the column-chart I_S is (−11/16, −11/17). The slopes tested inside it keep the same 11-letter physical word, and both endpoints fail. In R22 the same direction stops at the old reflex (1,−2). Both claims match the note.

## 2. The 6-wall L claim

The room is [−x−2, z+1] × [−2, y+1] with the open northeast quadrant removed. It has 6 walls in every case, and the marks are S = (−x, y) and T = (z, −1). Every ≤ 1-reflection shot points at T or at one of its 6 wall images. Each candidate is traced exactly, and the tracer's first wall must be the named wall.

- **Grid.** Odd x from 3 to 15 and odd y, z from 1 to 15 give 448 rooms. A shot with at most one reflection exists iff zy < 3x in all 448, with 0 mismatches.
- **Bottom wall covers the range.** No room is lit by another wall while the bottom shot fails. The notch walls never give a shot. Each stated wall condition is an exact iff on the grid, not only a necessary one:
  - direct: zy < x
  - bottom: zy < 3x
  - left: zy < x + 4
  - right: (z+2)y < x
  - top: z(y+2) < x
- **Boundary cases.**
  - In L(9,3,3) and L(15,5,3), zy = x, so the direct chord hits the reflex. The bottom and left shots still light the pair.
  - In L(3,3,3) and L(5,3,5), zy = 3x, and no shot with at most one reflection exists.
  - In L(3,1,1) and L(15,3,3), x = z(y+2), so the bottom bounce lands at (0,−2). That contact is legal and smooth, as the note says.
- **x ≥ 3 is needed.** With x = 1, the left wall lights L(1,1,3) and L(1,3,1) although zy ≥ 3. The note's hypothesis excludes this case correctly.

## 3. Non-Presburger conclusion, and what it kills

- **Slices.** On z = y, the least odd lit x, traced near the threshold for odd y ≤ 41, equals the least odd x with y² < 3x. Litness is monotone in x on every row. For y = z = 6b+3, the traced least c is 6b²+6b+2 at b = 0 to 3. For the direct shot with y = z = 2b+1, the least c is 2b²+2b+1 at b = 0 to 4. The second difference of 6b²+6b+2 is 12, so no three graph points are collinear and the graph contains no infinite arithmetic progression.
- **Logic.** The argument is correct.
  1. The map (x,y,z) ↦ (edge lengths, S, T) is affine and injective, and Presburger sets are closed under affine preimage, slicing and congruence restriction.
  2. A Presburger relation would therefore give a Presburger least-c function on the slice.
  3. That function's graph would be semilinear and infinite, so it would contain an infinite arithmetic progression. It doesn't.

  So the lit relation for words of length 0 or 1 is not Presburger in joint room-and-mark coordinates.
- **Decidability is not killed.** The result rules out building a Presburger darkness formula from a fixed finite set of words. It says nothing against decidability. The natural replacement is less promising than the prompt suggests:
  - For a fixed word, legality is a Boolean combination of quadratic integer inequalities: determinants of affine forms in (ℓ, S, T). Singleton endpoint events add quadratic equalities.
  - Real closed fields decide the real relaxation only. Every word shares the same integer room and mark variables, so integrality can't be confined to fixed words.
  - Existential sentences over ℤ with quadratic constraints are undecidable in general, because any Diophantine system reduces to degree 2. Whether this determinant family is decidable is open.
  - Any fixed word set misses the actual question: cov279 shows that no length-independent word bound N(σ) exists.
- **d132 scope.** RESULTS.md (d70-writeup, finite-flat entry) states that on each rational polyhedral cell, all-word darkness is a finite union of affine flats, so integral darkness is Presburger. This is existence only, with no bound, no equations and no decision procedure. d134 closed d132 gap 1. d132 gap 2, the semialgebraic parameter map, is still listed as open.

  **No contradiction.** d132 concerns the all-word dark set. This note concerns the lit relation for words of length ≤ 1. On this L skeleton the all-word relation is universal (d157), so darkness is empty and Presburger. Together the two results say that truncations by word length can be non-Presburger while their limit is Presburger.

## 4. Scope

- **Proved:**
  - The chart cover with smooth cut endpoints.
  - On one named 6-wall skeleton, the lit relations for words of length 0 and of length ≤ 1 are not Presburger.
  - The turn-skeleton count 1, 1, 4, 8, 29, 79, 280, 912, 3260, total 4,574. Burnside and brute-force bracelet enumeration agree. This count is an enumeration of words, not rooms.
- **Not checked here:** the cov279 bound √q/12, the 6HD+5 bound, the shear-orbit area bound and the realizability induction.
- **Not claimed, and correctly so:** any decision procedure for a cell sentence, and any progress on W ≤ 20. The note's next target, effective dark-flat equations, follows correctly from the analysis.

## Gaps

1. **Medium: the note doesn't say plainly what non-Presburger kills.** State that it refutes only the bounded-word Presburger route, not decidability. Also state that real closed fields don't help, because integrality sits on the shared room and mark variables, and existential quadratic integer sentences are undecidable in general. The current text, "two different sources of decidability", is correct but leaves this implicit.
2. **Medium: the finite-flat result is cited as unconditional.** RESULTS.md still lists d132 gap 2 (semialgebraic parameter map) as open. Mark the "existential description of a formula for integral darkness" as conditional on it.
3. **Low: "bounded words" is proved only for N ≤ 1.** The note's phrase "a bounded existential choice of words" covers N = 1 only. Non-Presburger behavior for fixed N ≥ 2 on this skeleton is plausible but unproved. State the claim as "N ∈ {0, 1}" or add the general-N argument.
4. **Low: the wall conditions are exact, not only necessary.** On the grid, the left, right and top conditions are exact iffs. The note's "only if" is correct but weaker than the truth. Stating the iff would make the "nothing new" step a direct comparison.
5. **Low: the joint-interval lemma still assumes strict gates.** With singleton endpoint events a slope set can be closed or a single point, so the lemma's argument that strict clearance puts the slope in the interior doesn't apply. The one-sided test s₀ ∈ I_S remains exact. Say so in the coverage section.
6. **Low: the coverage direction is nearly tautological.** Every legal shot defines its own chart. The real content is the converse gluing step and the finiteness of open/singleton choices per word, which grows as 2^(number of events). Name the finiteness explicitly, since a decidability argument would iterate over these charts.
