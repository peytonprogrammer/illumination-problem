# D131: review of the passage-complexity note

Date: 2026-11-21. Reviewer: independent referee.

Reviewed file: `../d95-review-queue/snapshots/passage-complexity.2026-11-21-2125.md`. It's byte-identical to `qclass-closure/bbbb/passage-complexity.md` (checked with `diff`).

Context read: `reflection-complexity.md` (the determinant argument; not reviewed here), `stabilizer-orbits.md` (st279 rows), `shadow-budget.md` (B(r)), the d86 and d130 reviews, review-queue item Q11 and the coordinator-log entries that define K(r).

Own code: [checks.py](checks.py), log [checks.log](checks.log), 23 CPU-seconds. It uses two exact tracers that share no code:

- A passage tracer that applies the note's congruence once per band passage, in integers scaled by the slope denominator.
- A `Fraction` cell tracer that moves through unit cells, reflects at cell walls and stops at every reflex or convex corner. It knows nothing about bands.

The script builds only the named st279 rooms (m = 8, 16, 24, 32, 64, 128, 256). The only searches are over ray directions from S inside those rooms. One network fetch retrieved the EMM PDF (arXiv 1305.3015) to check a theorem number. No project information was sent.

## Verdict

**Sound with gaps.** The theorem holds as stated, for the fixed horizontal decomposition. The passage congruence, the slope-shift lemma, the 26k compression and the transfer of the determinant bound all check, both on paper and on 53,376 exact rays. The gaps concern the definition of K(6), the scope beyond the horizontal convention, and explicit constants. One downstream summary overstates the result (gap 1).

## 1. Passage definition and the phase congruence

The canonical horizontal decomposition cuts at y = m, m+1, m+2, giving exactly the four rectangles B1–B4. Each piece is a rectangle whose two vertical sides are walls over the whole open height range. So a passage meets corners only at its two horizontal ends. Inside it, every side contact is a smooth reflection, and the folded developed abscissa is exact. Exit − entry ≡ ds (mod 2u) on the developed circle fixes the exit position and the exit sheet. The legality test is the window or mirror test at the end, with exits at multiples of u being corners. One congruence per passage is enough.

Check: on all 18 lit witnesses in check C, the passage tracer and the cell tracer agree exactly on the target, the reflection count R and the passage count k.

The note doesn't say why one congruence suffices: every piece side is wall for the full band height. That's true for any canonical decomposition, but it's the load-bearing fact (gap 5).

## 2. Slope-shift lemma and the 26k bound

**Ratios.** The passage ratios d/u are 1 (B1 and B4 full), 1/3 (B2 and B3), 1/2 (S to y = 0 or y = m) and 1/4 or 3/4 (y = m+2 or y = 2m+2 to T). Then 12·d/u ∈ {12, 4, 6, 3, 9}, so 24d ∈ 2uℤ for every type. The modulus 24 is the least that works: 1/4 forces 8 | t and 1/3 forces 6 | t. The slope magnitude s is the same on every passage, because horizontal mirrors flip only v_y and vertical mirrors flip only v_x.

**Every signed event stays put.** By induction, the entry phase and sheet of each passage are unchanged. The exit phase moves by a multiple of 2u, so the exit position, sheet and event type are unchanged. Interiors stay legal by section 1. The argument doesn't care about revisits, vertical sense or mirror events, since each passage is one of the five types.

Check B: m = 8 and 16, s = a/b ∈ (0,24] with b ≤ 30, all four sign choices, 60 passages, 26,688 rays per m.

- The event lists (position, sheet, type, band) for s and s+24 are identical on 26,688/26,688 rays at both m. Among these rays, 20,880 enter the neck at m = 8 and 11,600 reach the upper square. Also 9,024 return down through an interface, 14,592 reflect off a middle-band mirror, and 26,592 have some mirror event.
- With the target row included, the outcome (status, target, k) is identical for s+24 on every ray. That covers 6,028 hits at m = 8 and 3,972 at m = 16.
- Controls behave as the ratios predict. s+12 keeps every interface event, because 12·d/u is even for 1, 1/3 and 1/2. It changes the target outcome on 3,972 and 3,528 rays, because 12·(1/4) = 3 is odd. s+8 breaks the event list on 76% and 64% of rays, because 8/3 ∉ 2ℤ. So shifting by 24 is necessary as well as sufficient.

**26k bound.** Every ratio is at most 1, so d ≤ u. That gives horizontal travel ds ≤ 24d ≤ 24u. The note doesn't state the step d ≤ u (gap 5). Entries lie strictly inside a window or mirror, never at a side. So there are at most 24 side contacts per passage, not 25, plus at most one terminal mirror. The bound ≤ 26k is correct and slightly generous. Check: among the 10,000 hits with s ∈ (0,24], none has R > 26k. The largest R/k is 22.8.

## 3. Lower bound and "all but at most B(6) lit"

**Determinant.** The proof is the reflection-complexity argument with the same limits S₀ = (1/2,1/2) and T₀ = (3/2,5/4). Here S₀ is exact, and T_j/m is within (2+√m)/m in x and 2/m in y. The crossing is within 1/m of p. So δ = C/√m + 6R/m holds with one C for the whole row, and the bound is uniform in j. In units of 1/4 the mirrors sit at 0, 4, 8. Images of p are (0,0) mod 4, and images of T₀ are (2 mod 4, odd). So det ≡ 2·odd ≡ 2 (mod 4). D130 checked this determinant on named witnesses. Combined with the compression, every route with k passages yields a legal path with R ≤ 26k. So k ≥ R_min/26 = Ω(√m), uniformly in j.

**Explicit constant.** Check D evaluates the inequality with the actual errors. It forces R ≥ 1 only at m ≈ 10⁴ and R ≥ 98 at m = 10⁸. The forced k exceeds the trivial value 4 only from m ≈ 1.14 × 10⁸ (gap 4).

**Lit candidates.** The row has 2⌊√m/2⌋+1 targets. B(6) bounds the regular hidden targets from one source, uniformly over rooms with six reflexes. So all but B(6) targets are lit, and the lit proportion tends to one. The citation path is correct: shadow-budget.md, reviewed by d86 as "sound with fixable gaps", with the EMM fix applied. Review-queue item Q11 lists the EMM theorem number as unverified. I fetched arXiv 1305.3015: **Theorem 2.2** reads "Any closed P-invariant subset of H₁(α) is a finite union of affine invariant submanifolds." The citation is right, and Q11 can be closed for EMM. The Filip and marked-stratum citations remain from memory. B(6) is non-effective, so "sufficiently large m" has no explicit value. The note says so.

**Direct lighting at small m.** Check C confirms that every T_j is lit at m = 8, 16, 24 and 32: 3, 5, 5 and 5 of 3, 5, 5 and 5 targets. Each target has an explicit exact path, replayed by the cell tracer. Examples:

| m | T | direction (vx, vy) | k | R |
|---|---|---|---|---|
| 8 | (14,12) | (13, −8) | 5 | 3 |
| 16 | (26,22) | (41, 23) | 6 | 6 |
| 32 | (48,42) | (48, −29) | 5 | 3 |
| 32 | (50,42) | (49, 51) | 11 | 14 |

The fewest passages found per target range from 5 to 11. Every witness has R ≤ 26k. Each witness, replayed at s+24 and s+48, hits the same target with the same k. Its reflection count rises, for example from 3 to 61 to 119. These counts lie far above the vacuous bound, which is all you can expect at this size.

## 4. Scope

- **Horizontal convention.** The headline holds: no K_hor(6) works for normalized, strictly simple six-reflex rooms with lit same-parity interior lattice pairs. Check A confirms the room facts: one boundary loop, 16 vertices, 6 reflex, gcd 1 on both axes, area 2m²+6. All marks have even coordinates and are interior from m = 8. S lies in the lower square and every T_j in the upper square.
- **Vertical convention on the same room.** The lemma doesn't transfer. The vertical pieces have ratios (m−1)/m, 1/(m+1), 1 and 1/(m+1), plus the partial passages. The phase-preserving modulus is then of order 2m(m+1). After compression a passage can still carry about m² reflections, so the determinant bound gives no passage bound. Check E searches slopes a/b with b ≤ 16, a ≤ 40m and at most 9 vertical passages. It finds bounded witnesses for some targets: 3/3 at m = 8, 4/5 at 16, 3/5 at 32, 3/9 at 64 and 1/11 at 128. It finds none at m = 256. All replay exactly, for example m = 16, T = (30,22), with 5 vertical and 13 horizontal passages. This search is incomplete, so whether vertical passages are bounded on this family is **open**. Neither the note nor this review settles it.
- **Per-pair or mixed choice.** The note says correctly that it doesn't exclude choosing the better decomposition for each pair, or a macro step that counts a first-return loop once. Transposing gives an obstruction for the vertical convention only in the transposed room. That room's horizontal decomposition is again unaddressed.
- **Downstream wording.** The coordinator-log entry for Q77 says "route-length finiteness is ruled out at three levels (menu, reflections, passages)." For passages, that holds only under a predetermined horizontal convention.
- **Decision follow-on.** The modulus 2·lcm(u_i) is correct for integral event heights. I checked the algebra of the dumbbell example. Given the crossing set (1+2U+L)/2 + gcd(U,L+1)ℤ, the open-door route fails exactly when U | L+1 and (L+1)/U is even, that is, when 2U | L+1. The Presburger argument is correct. I didn't build the dumbbell room, so the crossing formula itself is unverified. The cov279 3 | q and (1,5) control sentences weren't checked.

## Gaps

1. **Medium. The scope is narrower than the downstream summary.** The theorem refutes K(6) only for a fixed horizontal convention. On the same rooms the slope shift has no vertical analogue, and the search found bounded vertical witnesses for some targets. Fix: write the headline as K_hor(6), state that the vertical and per-pair versions are open, and correct the Q77 log line.
2. **Medium. K(6) is not defined in the note.** The definition lives only in the coordinator brief. The headline depends on its quantifiers: which rooms, which pairs, and whether K bounds some lighting route or every route. The note also uses "normal traversals" and "passages" as if they were the same thing. Fix: state "for every normalized strictly simple room with r = 6 and every lit same-parity interior lattice pair, some lighting route has ≤ K passages in the canonical horizontal decomposition". Use one term.
3. **Low. The existence step is non-effective, and it's avoidable.** B(6) has no value, so "sufficiently large m" is unknown, and the step rests on EMM, Filip and LMW. A direct construction at the exact heights m/2 and 5m/4+2 would remove that dependence. Check C finds such paths at every m ≤ 32. Fix: optional. Meanwhile, record that EMM Theorem 2.2 is verified.
4. **Low. The constant is not explicit.** The bound beats the trivial k ≥ 4 only for m ≳ 1.1 × 10⁸. Observed fewest-passage counts are 5–11 at m ≤ 32. Fix: say the bound is asymptotic, or give k ≥ c√m with c explicit, about 1/(26·400).
5. **Low. Two steps are unstated.** The first is why one congruence suffices: piece sides are wall over the full band height. The second is d ≤ u on every passage type, which gives ds ≤ 24u. Also, 24 contacts per passage suffice, not 25. Neither omission affects correctness.
6. **Low. The corner convention is implicit.** B(r) forbids convex corners. The determinant count treats a corner hit as two mirror replacements. "Simultaneous smooth-wall reflection" is not defined. Fix: state that both reflex and convex corners stop rays. That's the convention both tracers here use, and it's what B(6) bounds.

## What the checks confirmed

- The room has r = 6, is simple and has gcd 1 on both axes. The marks are even, interior and in opposite end squares for m = 8–64.
- The slope-shift lemma holds on 53,376 exact rays, with revisits, mirror events and both senses. The shift 24 is necessary: s+12 and s+8 fail as predicted.
- The congruence tracer and the cell tracer agree on every witness. R ≤ 26k holds on every hit.
- Every T_j is lit at m = 8–32 by an explicit replayed path, with 5–11 passages. The lower bound is vacuous at these sizes.
- EMM Theorem 2.2 is the finite-union theorem, as shadow-budget.md cites.

## Re-run

```
cd d131-review-passage
python3 -B checks.py > checks.log
```
