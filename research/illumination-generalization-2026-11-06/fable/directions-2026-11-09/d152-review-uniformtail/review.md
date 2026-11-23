# D152: review of uniform-tail.md and stretch-stability.md (0310 snapshots)

Date: 2026-11-21. Reviewer: adversarial referee. Inputs are the read-only
snapshots `uniform-tail.2026-11-22-0310.md`, `stretch-stability.2026-11-22-0310.md`
and `stretch-control.2026-11-22-0310.py`. The snapshots are byte-identical to
the `qclass-closure/bbbb/` copies. Context: `length-periodicity.md`, the d110
review, `effective-chamber.md` (d124), `degree-gluing.md` (d114),
`resonant-gluing.md` (d112) and `parity-shortening.md`.

`checks.py` uses named rooms only. Lattice verdicts come from d8's complete
SL(2,Z)-orbit decider, imported unchanged. No room, direction or witness
search was run. Total CPU is 93 s (`checks.log`).

## Verdict

**Sound with gaps.** The dilation lemma is correct, and so are its lattice and
normalization caveats. The 20-wall construction and both named controls check.
The note misses one consequence: a reviewed result already refutes the uniform
hypothesis at W = 22. R22's arm slices change real darkness (gap 1). Nothing
in the notes refutes it at W ≤ 20. Astra's proposed descent theorem needs five
definitions fixed before it is a precise statement (gap 2).

## 1. The dilation argument

**Similarity is exact, corners included.** The map x ↦ mx sends the room P to
mP. It sends interior points to interior points, vertices to vertices and flat
boundary points to flat boundary points. A homothety preserves the reflection
law on every wall direction, including 45-degree walls. So legal paths
correspond bijectively, and a path stops at a corner of P exactly when its
image stops at a corner of mP. Thus D(B,L) = D(mB,mL) holds exactly for real
marks. `checks.py` shows the expected lattice shadow of this: in 2·R22 the
image pair (0,0)–(4,4) is the only unlit pair among 33 interior lattice
sources (3,000,000 orbit states, CAP).

**The telescoping stays inside the hypotheses, with one unstated step.** The
m unit steps from mL to mL+m use the tail at chamber data mB. That's
legitimate only because K is assumed uniform over *all integral rooms of the
type*, including non-normalized ones with door width mw. The intermediate rooms
mB at mL+j are dilates of B at the non-integral lengths L + j/m. The note
assumes they're admissible but doesn't prove it (gap 4). The proof is short:
with integral vertices and wall slopes 0, ∞ and ±1, a translated part makes a
new contact only at integral translation. So the set of bad lengths is a union
of closed intervals with integral endpoints. Admissibility at L and L+1 then
gives admissibility on [L, L+1].

The one-way version and the cross-chamber restriction also follow, as the note
states. The argument needs *any* two lengths with different verdicts on a slice,
not an adjacent pair. That's because the conclusion is constancy on the whole
slice from L = 1 (gap 5).

**The scope caveats hold.**

- **Normalized-only.** The endpoints mB at mL and at mL+m have every wall length
  divisible by m. So the hypothesis doesn't apply to the first and last unit
  steps. This is correct. For orthogonal rooms, a horizontal-only stretch
  diag(m,1) also preserves real darkness. It makes every intermediate length
  coprime to m normalized, which yields only D(L+1/p) = D(L+1−1/p) for primes
  p. Reaching the integral endpoints would need a semicontinuity statement in
  L, which the note doesn't claim. The caveat stands.
- **Lattice marks.** The rational-mark transfer is correct. Clear the
  denominators of a rational dark witness with m, and also ensure mL ≥ K. Move
  lattice darkness along the dilated slice, then scale the new lattice witness
  down to a rational one. The reverse direction is symmetric.

## 2. Consequence: R22's arm slices change darkness (W = 22)

None of the notes compares two genuine two-chamber corridor lengths with
different all-real verdicts. `parity-shortening.md` correctly says R22's gaps
are all one, so it can't be shortened, and that R22-L1-005 isn't a corridor
comparison. Lengthening an R22 arm *is* a unit-cross-section insertion with a
fixed wall pattern:

| Room | Edit | W, r, area | Lattice verdict (d8 orbit) |
| --- | --- | --- | --- |
| R22-base | none | 22, 9, 15 | DONE, 5,184 states: (0,0)–(2,2) and 3 wall pairs dark |
| R22-L1-007 | bottom prong 1 → 2 | 22, 9, 16 | all 10 regular points pairwise lit |
| R22-L1-025 | right prong 1 → 2 | 22, 9, 16 | all 10 pairwise lit |
| R22-L1-012 | top arm (width 2) 1 → 2 | 22, 9, 17 | all 11 pairwise lit |

In the lengthened rooms, every ordered pair has an orbit witness, so the lit
verdicts are complete for lattice points. The run hit the 3,000,000-state cap
only because no early stop was requested. The witnesses weren't re-traced. The
d8 decider passed validation against an unfolding-free tracer (V2, 0
mismatches).

For real marks the reviewed capped-arm tail gives the far end of the slice.
Apply d114 qualitatively, or d124 explicitly with ℓ ≥ 36w[1+2F_(3m)]² and
m = 4·area(J). At that length every real interior pair of R22 is lit. For the
bottom prong, J = R22-L1-027 is strictly simple with W = 20, m = 56, and the
bound has 72 digits. The top arm avoids a flush mouth endpoint: both its mouth
corners are reflex, and m = 52. The dark mark (2,2) lies on that open mouth,
which the tail covers as a strip mark. R22 at arm length 1 has the reviewed
dark interior pair (0,0)–(2,2). So D(B,1) ≠ D(B,ℓ₀) on one W = 22 slice.

By the note's own lemma, no uniform K exists over that type and its dilates.
Concretely, K(mB) grows at least linearly in m. By the rational transfer, a
uniform D_lat tail fails there too. The note's all-gaps extension ("identical D
on a shape cell") is false at W = 22, since R22 is the all-gaps-one
representative of its own cell. This doesn't touch W ≤ 20, where no dark room
is known. It does mean a proof of uniform K(20) can't come from any W-blind
gluing or stretching theorem (gap 1).

## 3. The 20-wall three-chamber construction

For k = 0..8, `checks.py` builds three 3×3 chambers and unit corridors over
1 < y < 2 with X = Y = 3k+1. Each room has W = 20, r = 8, area 27+X+Y, and is
strictly simple. The wall gcd is 1 on each axis. The control X = Y = 3 has
horizontal gcd 3, which explains the 3k+1 choice. The reviewed d69 criterion
(normalized, r ≤ 8, area > 64) gives BBBB exactly for k ≥ 6, at area 65 and
above. The note says "for area > 64" but never states k ≥ 6 (gap 6).

Cutting X leaves a sealed sub-room with area 18+Y and extent 6+Y. With
m = 4(18+Y), the D124 all-real bound is 36[1+2F_(12(18+Y))]². This matches
the note. At X = Y it has 97 digits at k = 0 and 188 at k = 6, against X = 1
and X = 19. The lattice bound 4(1+F_(3m−1))² also fails, and so does the
hypothetical X > 4(6+Y). Neither cut meets any reviewed threshold, at any k.
The line y = 3/2 remark is correct. The note claims no darkness.

As a side check, interior lattice pairs are all lit at X = Y = 1, 4 and 16. The
BBBB members, with 65 or more cells, exceed orbit.c's 63-cell limit.

## 4. Named controls

| Control | Check | Result |
| --- | --- | --- |
| DB55, H = 5 and H = 7 | Chamber depths 5 and 5, corridor length 3. d112's L > 4d depends only on depth. | Both have the tail L ≥ 21. The geometry (W 12, normalized) checks. |
| DB55 pencil (1,2j) | Replay of the saved script | j = 25, 28: [blocked, lit] at H = 5, [lit, blocked] at H = 7, as stated |
| Cross b = 7 and b = 9 | Area 16b − 16, arm area 4(b−2) | 96 → 128 and 76 → 100. The diagonal pair (6,0)–(0,6) is lit in both. |
| Degrees and two-cycles | Replay | All six rows of the stretch-stability table match |

One wording issue: the review-queue line says "the cross has no common cutoff".
The note shows only that D124's *sufficient* bound changes with b. That isn't
the same claim (gap 7).

## 5. Scope, and Astra's proposed next theorem

**Scope.** The note proves a conditional equivalence (uniform tail ⇔ tail from
L = 1) on dilation-closed real-mark classes. It also exhibits a W = 20 room in
which induction through reviewed thresholds stalls. It proves no cutoff, no
darkness verdict and no census size, and it says so.

**The proposed theorem** says that given a dark pair, at least one of two
comparable corridor cuts preserves some dark pair in a smaller room. It's a
sensible target, and no named data contradicts it. R22 shows darkness can be
destroyed by *lengthening*. That's consistent with one-way descent. The theorem
isn't yet well-posed (gap 2). To make it precise, fix the following:

1. **Predicate.** Choose real or lattice marks. For a lattice predicate the
   shortened room may leave the normalized class. For a real predicate the
   resulting bounded rooms need all-real certificates, not a lattice census.
2. **"Comparable".** For example, require both lengths ≥ τ(W), or
   |X − Y| ≤ c. Say what happens when only one corridor is long. There the
   statement reduces to single-corridor descent. With a wall-only threshold,
   the dilation lemma would force that descent all the way to length 1 for real
   marks. The two-choice version doesn't telescope that way, because the
   choices mix and the result isn't a dilate.
3. **Step size.** Choose 1, 2 or a period. `parity-shortening.md` shows a
   uniform even step implies the unit step for real marks.
4. **Admissibility.** The shortened room must stay strictly simple with the
   same wall pattern. Shortening can collide parts in non-straight layouts.
   Either assume both cuts are admissible or let the theorem choose only
   admissible ones.
5. **Coverage.** Arms, indentations and rooms with no separating two-mouth
   corridor need their own move. R22's unbounded coordinates are arms.

## Gaps

1. **High.** The note doesn't record that its uniform-K hypothesis is refuted at
   W = 22 for arm insertions, and that its all-gaps extension is too. The
   evidence is R22 at arm length 1 (dark) against ℓ₀ (lit by d114 and d124).
   This doesn't affect W ≤ 20. It means uniform K(20) can only come from
   W ≤ 20–specific input, which makes this route about as hard as the main
   problem. The refutation assumes capped arms count as corridor insertions.
   If the class requires two genuine chambers, the all-gaps statement is still
   refuted.
2. **Medium.** Astra's descent theorem isn't well-posed as stated. It needs the
   five fixes in section 5.
3. **Low.** d124's capped-arm theorem has a low gap on planarity of the cap
   double. Section 2 inherits it. The top arm avoids the flush mouth endpoint
   that the bottom prong has.
4. **Low.** The note assumes admissibility of the dilated slice at non-integral
   base lengths without proof. A short integer-contact argument supplies it.
5. **Low.** The note says "adjacent lengths". Any two lengths on a slice with
   different verdicts refute a uniform K.
6. **Low.** The note doesn't state k ≥ 6 for the area > 64 BBBB criterion.
   Rooms with k ≤ 5 are normalized but not covered by it.
7. **Low.** The queue summary's "the cross has no common cutoff" overstates the
   note. The note shows only that the sufficient bound grows with b.

## Files

- `checks.py`: all checks. Run it with `python3 -B checks.py > checks.log`.
- `checks.log`: output, 93 s CPU, almost all in orbit.c.
