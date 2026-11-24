# D226 review: d225 pinned x = 1 staircase pair

Date: 2026-11-23. Reviewer: Opus, independent. Note under review:
[../d225-attack-pinned-staircase/note.md](../d225-attack-pinned-staircase/note.md).
Checks: [checks.py](checks.py), output [checks.log](checks.log): 62 PASS,
0 FAIL, under 1 CPU-second at `nice -n 10`. The tracer is new code (polygon
boundary, exact `Fraction` arithmetic). It imports nothing from d212, d213 or
d225.

## Verdict

The closure holds as stated. For every real gain pair with x + y > 8, the x = 1
pair is lit on the whole sector 1/4 ≤ α ≤ 2/3. That sector contains the d215
strip near b = c and the band 2a + 2b ≤ c with α ≥ 1/4. Theorem B also holds:
the pair is lit outside K0, so the region a < 1/25 is closed.

The strip and band aren't closed for small rooms. The lattice rooms (0, 2) and
(0, 3), with areas 24 and 27, have no certificate. Both lie above the census
(area ≤ 21). A compact real residual inside x + y ≤ 8 also stays open.

The general pin blow-up lemma has three precision gaps (claim 4). They don't
affect this chart's theorems.

| Claim | Verdict |
| --- | --- |
| 1. Pin identification | CORRECT WITH GAPS (minor) |
| 2. Window cover, uniform for x + y > 8 | CORRECT |
| 3. Micro shifts and the two bounce certificates | CORRECT |
| 4. Crossing types and the general principle | CORRECT WITH GAPS |
| 5. Theorem B, K0 and a < 1/25 | CORRECT |
| 6. Strip fully covered | CORRECT for x + y > 8; NOT CLOSED below |

## Lemma M (re-derived)

Lemma M is the base of every certificate, so I re-derived it before the claims.
The reflection-group fold, the identity σ(1 + y + h3) = k − v, and the residue
conditions all hold. The tier-3 leg has no side bounce, because the exit lies
in (4, 6) and h3σ < 1. All 11 legal traces in §Traces match its three
predicted crossings exactly.

One precision gap: the "exactly these cases" direction holds only for the
first upward pass. If the middle crossing misses the gate, the ray reflects and
keeps going. The lemma doesn't show that it never reaches T later. Only the
"if" direction is used for coverage, so no theorem depends on this.

## Claim 1: pin identification — CORRECT WITH GAPS (minor)

- At α = 1/2, kα mod 6 and k mod 6 have joint period 12, and no residue passes.
  At α = 1/3 the period is 18, with the same result.
- k = 6 at α = 1/2 lands on (4, 3+x). k = 4 at α = 1/2, and k = 6 and k = 12 at
  α = 1/3, land on (3, 3+x).
- Exact traces at Q1 = (1/10, 1/10) give corner (3, 31/10) for k = 4 and corner
  (4, 31/10) for k = 6.
- Inside [1/4, 2/3] the pin set is exactly {1/3, 1/2}. That follows from the
  window cover in claim 2.

Gap: "block every k" means the corner kills only the winding that lands on it.
The other windings fail the downstream residue test, and only for their first
pass (see Lemma M). The pin is a pin of the one-pass family, not a proven dark
line. The note says "monotone family", so the statement is accurate. The
wording "corners block unbounced chords" overstates it.

Outside the sector, α = 3/4 is a third pin (period 24). The note handles it in
Theorem B; Q6 = (7, 1) traces the monotone k = 4 chord into corner (4, 10).

## Claim 2: window cover — CORRECT

- All four sector boundaries reduce to linear forms with matching
  coefficients: α = 1/2 ⇔ x = y, 1/3 ⇔ y = 2x+2, 1/4 ⇔ y = 3x+4, and
  2/3 ⇔ x = 2y+2.
- The windows k = 10 A (1/5, 3/10), k = 12 B (1/4, 1/3), k = 6 A, k = 6 B and
  k = 4 A (1/2, 3/4) match their residues. Their union covers [1/4, 2/3]
  except exactly {1/3, 1/2}.
- 1/4 and 2/3 lie strictly inside windows, so the closed sector boundary is
  covered.

Uniformity: for h0 = h3 = 1, α' = α exactly. The condition is then exact
membership of α in an open window plus σ = k/D < 1. No slack estimate enters.
The largest k is 12, so D > 12 ⇔ x + y > 8 covers every window at once. The
threshold is sharp for k = 12: at D = 12 the last crossing lands on a top-gate
corner. As a → 0 at fixed α, D grows, so nothing degrades. Only the corner
clearance shrinks, and the note uses exact legality, not clearance.

Q3 = (19/10, 31/5) sits just above the threshold (D = 121/10, α = 39/121). The
k = 12 chord traces legal with crossings 241/121, 379/121 and 485/121.

## Claim 3: micro shifts and bounce certificates — CORRECT

- Floor shift +2(1 − α_i) and roof shift −2α_i, in units of the new
  σ' = k/(D'+2). These are affine identities in N_i.
- x = y, floor k = 4: r = 2 + 2/(3+x) ∈ (2, 3), and the budget 12/D' < 2 holds
  exactly when x > 0. μ = +1 unit past the type-R corner.
- The floor k = 4 open set is {y < x+2, x < 3y+2, x + y > 0}. That matches the
  note.
- y = 2x+2, floor k = 6: 6α' − 2 = 8/(8+3x), μ = 4/3, and the budget holds
  exactly when x > 1/3. The open set is {y < 2x+6, x < 2y, y ≠ x+2, x+y > 3}.
  That matches the note, including the case-B half (k = 6 ≡ 0).

Traces:

- Q1 = (1/10, 1/10) is near x → 0, with budget 3σ = 60/31 < 2. The trace is
  legal.
- Q2 = (2/5, 14/5) is just above x = 1/3, with first crossing 68/23, 1/23 from
  the gate end. The trace is legal.
- Q5 = (20, 22) is on the floor strip's edge y = x+2. The floor k = 4 chord
  hits corner (3, 23), as predicted. The monotone k = 6 chord covers the point.

## Claim 4: crossing types and general principle — CORRECT WITH GAPS

The types correctly describe the two pin corners of this chart. The general
lemma isn't stated precisely enough to apply to another chart without
re-deriving it. These are the gaps:

1. **μ must be the unfolded offset.** The note defines μ = (crossing − c)/σ.
   At the P0 corner (4, 3+x) the physical crossing is left of x = 4 on both
   sides. The ray reflects off x = 4 when r > 3, so a physical μ is never
   positive. The note's formula μ = (x − y + h0 − h3)/2 is the unfolded one.
2. **Type R has two orientations.** The corner (3, 3+x) is reached at r = 2
   moving right (legal side μ > 0) and at r = 4 moving left (legal side μ < 0).
   The table lists only μ > 0. The k = 12 chord at α = 1/3 is the r = 4 case.
   On y = 2x+2, the floor k = 12 chord fails and the roof k = 12 chord passes
   when x > 28/3. Q4 = (12, 26) confirms both: the roof k = 12 chord traces
   legal with middle crossing 35/11 (case B). The floor k = 12 chord reflects
   off the tier-1 roof and later dies at corner (6, 42). The note's theorems
   use k = 6 there, so nothing breaks, but the sign table is wrong for half
   the R cases.
3. **The general threshold omits non-pinned interfaces.** The lemma's
   threshold uses only the end-gate budgets g0 and g3. In Lemma M that's
   enough, because the top crossing is automatic and the residue test is
   bounce-invariant. In a chart with more interfaces, the bounce moves every
   non-pinned crossing by σ·2d0(1 − α_i) as well. That needs D' large against
   each non-pinned macro clearance, and the lemma doesn't state it. The
   "general tier widths" proof is asserted, not written.

Minor: "P− for k = 2" should be "k ≡ 2 (mod 6)". k = 2 never reaches
(4, 3+x), since 2α < 3. The first instance is k = 8 at α = 3/8.

The "not covered" list is accurate. The bounce shift
2e0d0 − 2(e0d0 + e3d3)α decreases in α, so a (−, +) pair of simultaneous pins
can't be fixed by end bounces.

## Claim 5: Theorem B and a < 1/25 — CORRECT

- **x < 1, y > 18+5x.** α' < 1/6 ⇔ y > 18+5x. The k-interval has length
  (2+2x)/(3α') > 4. Every open interval of length > 4 meets {0, 4} mod 6. The
  bound σ < (8+2x)/(3(4+x)) = 2/3 gives the budget. Q7 = (1/2, 21) traces
  legal with the floor k = 16 chord.
- **α < 1/4, x ≥ 1.** This is d215's construction, re-derived: the slope is
  below 3/(2+x) ≤ 1, and no x + y threshold is needed.
- **(2/3, 1).** The pieces (2/3, 3/4) k = 4, (3/4, 5/6) k = 12 B,
  (4/5, 9/10) k = 10 A and the α > 5/6 β-trick leave only α = 3/4. The roof
  k = 4 chord closes it for y > 1/2, which x + y > 8 implies. Q6 = (7, 1)
  traces legal with the roof chord. Q8 = (40, 2), α = 21/23, traces legal with
  the β-trick chord k = 16.
- **K0.** On x + y ≤ 8, a ≥ 1/9. On {x < 1, y ≤ 18+5x}, x + y < 24, so
  a > 1/25. Thus a < 1/25 lies outside K0, and the face at infinity has a
  closed neighborhood for this pair. "Closed" here means lit for all real gain
  pairs with a < 1/25. It isn't a uniform-clearance statement.

## Claim 6: is the strip fully covered? — CLOSED for x + y > 8 only

- The regions abut with no gap. In α, the open windows plus the two pin lines
  cover the closed sector. Each pin certificate needs only x > 0 or x > 1/3,
  and both hold when x + y > 8 on those lines. Theorem B starts where the
  sector ends.
- The remainder bookkeeping uses inequalities only. Of the 32 sector lattice
  points with x + y ≤ 8, the uncovered ones are (0, 0), (0, 2) and (0, 3).
  This matches the note.
- Among all 10 lattice rooms with x + y ≤ 3 (area ≤ 27), sector or not, the
  uncovered ones are the same three. (3, 0) is covered by the k = 4 chord.
- Census scope: area = 18 + 3(x + y). The census (area ≤ 21) covers only
  (0, 0), (0, 1) and (1, 0). (0, 2), area 24, lies on the pin line α = 1/3.
  (0, 3), area 27, lies at α = 2/7, inside the band. **Neither is in the
  census.** Rooms of area 22 and 23 don't exist in this family.
- Real points with x + y ≤ 8 aren't claimed, and some have no certificate here.
  For example, α ∈ [3/10, 1/3) with D ≤ 12 has no monotone chord. The floor
  k = 6 chord covers part of it. The note states this.
- The lattice residual of K0 outside the sector isn't enumerated. That's the
  rooms with x + y ≤ 8, plus x = 0 with y ≤ 18. The note states this too.

## Traces

All traces use the new tracer at 8 hand-picked points. Every direction is
prescribed by the note, or by claim 4's R-orientation derivation. There was no
search.

| Point | Chord | Result |
| --- | --- | --- |
| Q1 (1/10, 1/10) | floor k = 4 / mono k = 4, 6 | legal / corners (3, 31/10), (4, 31/10) |
| Q2 (2/5, 14/5) | floor k = 6 | legal |
| Q3 (19/10, 31/5) | mono k = 12 | legal |
| Q4 (12, 26) | roof k = 12 / floor k = 12 / floor k = 6 | legal / dark, corner (6, 42) / legal |
| Q5 (20, 22) | floor k = 4 / mono k = 6 | corner (3, 23) / legal |
| Q6 (7, 1) | roof k = 4 / mono k = 4 | legal / corner (4, 10) |
| Q7 (1/2, 21) | floor k = 16 | legal |
| Q8 (40, 2) | mono k = 16 | legal |

## Which lemma advanced

**L1**, pinned-pair route. This is the first closure on that route: one
pinned specified pair in one chart is lit for all real gains with x + y > 8.
That includes the entire face-at-infinity neighborhood a < 1/25. It is also
the first concrete instance of the micro move (an end-tier bounce) that
clears a pin with zero macro slack.

The general pin blow-up lemma isn't yet reviewable as a general statement,
because of the claim 4 gaps. It needs unfolded μ, the R orientations and
non-pinned clearances. It doesn't yet meet the PROGRAM stopping-rule target,
which is a general pinned-pair lemma or a sharp obstruction. No census
changes.

## First case still open

For this pair, the first open case is the lattice room **(x, y) = (0, 2)**,
area 24. It's the smallest room above the census with no certificate. It sits
on the pin line α = 1/3, where the floor bounce lands on the other pin, α' =
1/2, and the floor k = 6 chord needs x > 1/3. Next is (0, 3), area 27, where
the floor k = 6 chord exhausts the type-S budget (σ = 2/3). After those come
the real compact residual in x + y ≤ 8 and the unenumerated lattice residual
of K0.

For L1 in general, the first open step is the note's own: show that every
pin of the descent chord in a nondegenerate chart with r ≤ 8 has a type with
a legal side. Corrected R signs are needed, and the lemma must be stated for
multi-interface charts with non-pinned clearances.
