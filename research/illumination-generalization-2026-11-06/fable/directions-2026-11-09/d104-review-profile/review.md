# D104: review of large-dark-profile.md

Date: 2026-11-20. Reviewer: independent referee. Reviewed file:
`.context/qclass-closure/bbbb/large-dark-profile.md`.

Sources read: `eight-sheet.md`, `midpoint-necessity.md`, `small-orbit-blocks.md`,
`bbbb-split.md`, `dark-locus.md` (rank statement), `shadow-budget.md` (B(r) statement),
`arithmetic-rigidity.md`, and reviews d78, d79, d82, d86, d89, d92, d93, d97, d99, d101,
plus d70 `RESULTS.md` §11.

Method: proof reading only. One exact arithmetic check (Python, integer only, under 1 s).
No room, ray, direction or word search. No R22 run was needed, because d82, d92 and d93
already reproduce every R22 number the note cites with independent code.

## Verdicts

| Task | Verdict |
| --- | --- |
| 1. Table rows | Every row matches its reviewed source. No row is stronger than the source. Three low-severity scope fixes are listed below. |
| 2. Arithmetic | 26, 148 and 28 are correct. n ≥ 120 is not vacuous: the n ≤ 36 bound applies only to rooms with a corner-only class, never to BBBB. |
| 3. Minimal missing statement | It is equivalent to "no dark pair in the stated range", that is, the core restricted to n ≥ 120. It is strictly weaker than the core in scope, and it is a restatement, not a reduction. |
| 4. Joint verdict | Accurate. No combination of the rows gives a contradiction. |

## 1. Table rows

**Row 1, affine action on Q.** Matches d92 and d93.

- G preserves cone angles, so G_s maps dark targets to dark targets (d92, claim 1).
  Hence each of G_s·t, G_s·ιt, G_ιs·t, G_ιs·ιt, and the four reversed ones, lies in a
  hidden set from a regular source. B(r) bounds those sets (shadow-budget.md proposition,
  d86 sound with a citation fix). The bound needs no lattice or area hypothesis.
- 2e(S) ≤ B(r)(B(r)−1), with the same bound at T, matches d92 claim 1 and d93 claim 1.
- "Cubic orbitals are not forced" matches d93's finding that the cubic single-orbital
  hypothesis holds only in R22.

**Row 2, coincidences on U.** Matches d79, d82 and the d78 combined statement.

- d ≥ n − 8 at n ≥ 120 needs normalization, r ≤ 8 and strict simplicity (three-sheet,
  eight-sheet). The note's preamble supplies all three.
- d ≥ ⌈2n/3⌉ at n ≥ 49 is d81 as reviewed by d82 and d101 (Q09).
- "Unreached" is (ii-geo). Darkness gives it directly, as d82 requires. The row doesn't
  claim (ii-alg).

**Row 3, primitive sheet action.** Matches d99 claims 1a to 1c.

- supp(g_x²) = 3z_x ≤ 24 and the Burness–Guralnick bound n ≤ 6z_x ≤ 48 give A_n ⊆ G at
  n ≥ 49. Then G is 2-transitive, so d = n − 1.
- The n ≥ 73 lit lift pair is sound but, per d99, nearly empty: such pairs exist in R22 at
  n = 15. "Its affine orbit misses all four dark edges" is automatic, because affine maps
  preserve lit and dark edges.

**Row 4, imprimitive sheet action.** Matches bbbb-split.md and d99 claims 2a to 2c.

- k ≤ r, z ≤ ⌊r/k⌋, z + 4 ≤ 8, I ≤ (k!)^(z+3), and kI ≤ 56 in degree two all match.
- "At least one endpoint has distinct regular mirror images" is d99 claim 2c. It uses
  d91's commutation of the deck involution with the mirror and strict simplicity.
- **Fix (low).** "The mirror-pair version" holds for f(s), f(ιs) as two specified points in
  every degree. Only for the unique maximal partition at n ≥ 120 is f(ιs) the quotient
  mirror of f(s), and that identification depends on d80. The source says so. The row
  should too, or say "the pair f(s), f(ιs)".

**Row 5, coordinates.** Matches d89, which asked for the d80 condition. The row carries it.

- 2 ≤ h < (r+1)/2 + 1 is the source's k < g/2 + 1 with g = r + 1. At r = 8 that's ranks
  2 to 5.
- The row omits "proper", "rational", "zero relative dimension" and "generic surface not a
  torus cover". The omissions make the row weaker, not stronger.
- **Fix (low).** The sequence corollary also depends on d80, through the mirror step.
  "Would also" inherits the condition only by reading. State it.

**R22 control.** Every number matches d92 (hidden sets, e = 2 at both ends), d87 (nine
corner certificates) and d82 (6 regular coincidences, all in class a).

- "Exactly" is correct. The lower inclusion uses R22's established darkness, and the saved
  legal witnesses give the upper inclusion (d93).
- **Fix (low).** Add that R22 isn't BBBB: its class (1,1) is discrete (d93), and r = 9. It
  controls mechanisms only, not the profile.

**Header.** The preamble fixes n ≥ 120, while rows 2 and 3 quote results from n ≥ 49 and
n ≥ 73. This is harmless, because those results hold a fortiori at n ≥ 120.

## 2. Arithmetic

The checks are exact, over n up to 5,000.

- 2⌈2n/3⌉ − 16 − ⌊n/2⌋ = 66 − 16 − 24 = 26 at n = 49. Its minimum over n ≥ 49 is 26.
- 2(n−8) − 16 − ⌊n/2⌋ = 224 − 16 − 60 = 148 at n = 120. Its minimum over n ≥ 120 is 148.
  This is R_other ≥ 2d − 2r − ⌊n/2⌋ with d = n − 8 and r = 8.
- The per-class bound is 2n − 32 − 3⌊n/2⌋. It equals n/2 − 32 for even n and
  (n+3)/2 − 32 for odd n. Both forms increase with n. The values are 28 at n = 120,
  30 at 121 and 29 at 122, so the minimum over n ≥ 120 is 28. The bound covers every
  class, so it covers each off-class too.

**Why n ≥ 120 and not n ≤ 36.** The bound n ≤ (r+4) + 3r ≤ 36 (d97) comes from the d68
counting identity applied to a class whose points are all corners. A BBBB room has a
regular point in every class, so the identity gives no bound there. BBBB rooms with r ≤ 8
have unbounded area: the crosses reach n = 96 to 256 at r = 4, DB55 stretches give
n = 501 + 80j, and arithmetic-rigidity.md records that no area bound exists. The profile
uses n ≥ 120 because two inputs need it: three-sheet plus eight-sheet for d ≥ n − 8, and
d80 for row 5. The note never says this. **Fix (low):** add one sentence. Say also that
21 ≤ n ≤ 119 lies outside the profile.

## 3. Minimal missing statement

The statement: for each nondirect pair in the stated range, some compatible marked start on
U reaches a regular coincidence by a straight segment whose two projections avoid room
corners.

Write MMS for this statement. Write Core₁₂₀ for "no BBBB, strictly simple, normalized room
with r ≤ 8 and n ≥ 120 has a dark distinct same-parity interior lattice pair".

**Core₁₂₀ implies MMS.** A nondirect pair that is lit has a lighting path. By Lemma MP
(d101: sound, needs strict simplicity), its half-length point is a lattice point over the
source pole. That point is interior or smooth, never a corner. The midpoint-necessity
argument turns the two halves into a straight segment on U from a marked start to a
coincidence at that point. The coincidence is regular, and both projections avoid corners.
The midpoint may equal S or T; the statement allows that.

**MMS implies Core₁₂₀.** At a regular coincidence c, the off-diagonal germ is y = −x in a
flat chart of Q at c. The two projected segments reach c from opposite sides at equal
speed. The first half followed by the reverse of the second is therefore straight at c.
Both halves avoid corners. Regular points over poles are 2π points, interior lattice points
or smooth wall points, and they don't obstruct. So the concatenation is a legal billiard
path from S to T. This converse is elementary, but no reviewed note writes it out.
midpoint-necessity.md states only the forward direction.

So MMS ⇔ Core₁₂₀, pair by pair. Lit pairs satisfy MMS automatically, so quantifying over
all nondirect pairs adds nothing. MMS is darkness negated in U-language. It isolates no
smaller missing step.

**Against the full core.** The core asks for no dark same-class pair in any BBBB room with
r ≤ 8, so it covers areas from 21 upward.

- Core ⇒ MMS holds by the argument above.
- MMS ⇏ core. MMS says nothing at 21 ≤ n ≤ 119. Condition (i) is open at 21 to 48, and
  d ≥ n − 8 is unproved at 49 to 119.

MMS is therefore strictly weaker in scope. Both might still be true; "strictly" means no
known implication from MMS to the core.

One further scope caveat: normalization can turn lattice marks into non-lattice marks
(d101, Q07), so lattice pairs of non-normalized rooms fall to G2, not to MMS.

**Comparison with the RESULTS open lemma.** That lemma asks for an *off-class* coincidence
reached by a real path, under d ≥ 2n/3 from n ≥ 21. Pair by pair it is strictly stronger
than MMS, which allows source-class coincidences, including S and T themselves.

**Fix (moderate).** Rename "minimal missing statement" to "equivalent restatement at
n ≥ 120". State both implications and the range. Note that the off-class open lemma
implies it, but not conversely.

## 4. Joint verdict

The verdict "no contradiction follows from the reviewed results" is accurate. I checked
every pairing of rows:

- **Row 1 against row 2.** The 148 or more unreached coincidences are points on U. A
  coincidence unreached on U need not be hidden on Q from either endpoint. d86 gives the
  exact cov4181 example. So the count doesn't feed B(r).
- **Row 3 against row 1.** A_n acts on sheets by continuation. The affine stabilizer can
  have tiny image (d93), and d99 1c identifies the needed affine return with d92's open
  mirror-suborbit question.
- **Row 4 against row 1.** Descent gives upper bounds only. On the cross every quotient
  mirror suborbit has size 1 (d99), so the bounds are compatible with small orbits.
- **Row 5.** It constrains sequences only and leaves a single room untouched.
- **Rows 1 to 5 together.** No row supplies a lower bound that grows with n on an affine
  orbit, and no row turns an algebraic coincidence into a legal path. Those are the only
  two ways the listed upper bounds could collide.

The sentence "A coincidence can project to a visible point while the two marked
trajectories cannot reach it simultaneously" matches d86. The last sentence, "existence of
a room satisfying the whole profile remains open", is correct.

## Corrections, in priority order

1. **Moderate.** Relabel the minimal missing statement as an equivalent restatement of the
   core at n ≥ 120. Give both implications, the converse concatenation step and the range.
2. **Low.** Explain n ≥ 120: three-sheet plus eight-sheet, and d80. Say the n ≤ 36 bound is
   Q-class only, and that 21 ≤ n ≤ 119 is outside the profile.
3. **Low.** Row 4: f(ιs) is the quotient mirror only for the maximal partition at n ≥ 120,
   conditional on d80.
4. **Low.** Row 5: make the d80 condition explicit for the sequence corollary.
5. **Low.** R22 control: say R22 isn't BBBB (discrete class (1,1), r = 9).
