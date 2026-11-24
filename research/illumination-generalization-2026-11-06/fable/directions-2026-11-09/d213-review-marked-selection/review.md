# D213: review of marked band selection

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [note-snapshot.md](note-snapshot.md).
Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
3.0 CPU-seconds under `nice -n 10` and reports 33 PASS, 0 FAIL.

To rerun it, use `nice -n 10 python3 -B checks.py`.

`checks.py` imports the d212 exact tracer, `seed_data`, signed `gate` and
`reaim` from [../d212-review-descent-skeleton/checks.py](../d212-review-descent-skeleton/checks.py).
Each lift builds the child with `insert_row`, recomputes the seed data in the
current parent, evaluates the signed gate, and traces the re-aimed ray
exactly. Only the three named rooms were used:

| Room | Shape | Marks |
| --- | --- | --- |
| Tiers | left-aligned widths 4, 5, 6 on y [0,2], [2,3], [3,5] | S=(1,1), T=(3,4) |
| Two-tier | widths 4, 4, 5, 5 by row, left aligned | S=(1,1), T=(2,3) |
| Offset staircase | x [0,3], [1,4], [3,6], [4,7]; heights 2, 1+x, 1+y, 2 | S=(2,1), T=(5, roof−1) |

Every traced ray is a template seed, an explicit re-aim of it, or the direct
chord. No room enumeration, room-size search, or direction search was run.
The t ≤ 200 sweep evaluates the note's interval formula arithmetically.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Template bound 121; conditional selection theorem | CORRECT WITH GAPS (scope) |
| 2 | Compatibility invariant, test (1), U=1 claim | CORRECT WITH GAPS (scope of U=1) |
| 3 | Determinant theorem, test (2), tiers example | CORRECT WITH GAPS (presentation) |
| 4 | Two-tier counterexample to "any successful first lift" | CORRECT (gate-level statement) |
| 5 | Ratio condition (3) and the √2 obstruction | CORRECT WITH GAPS (conditional, as stated) |
| 6 | Offset staircase: all sub-claims | CORRECT |
| | **Overall** | **CORRECT WITH GAPS** |

No mathematical error was found. The sweep in Claim 6 shows that the note's
selection family settles only 65 of the first 200 √2 rooms.

## Claim 1: template bound and conditional theorem

With r ≤ 8 there are at most r+2 wall levels and two mark levels per axis, so
at most 11 refined gaps. Compressing each to one gives a box of at most 11×11.
The compression is an increasing piecewise-linear homeomorphism per axis, so
the template stays strictly simple. Marks sit on cut levels and every gap
stays at least one, so both marks remain distinct interior lattice points.
The 11bB and 121bc bounds follow from the same count.

The conditional theorem is a valid implication. The chain lights the pair
directly from a template seed, and the last restoration is the single-band
parent that d212's selection hypothesis asks for. The strong-induction
variant is valid because a smaller parent is lit by hypothesis.

**Gaps.**

1. Low, scope. The examples in Claims 3 and 4 compress only y-gaps. The tiers
   room has x-gap [1,3] of width 2, and the two-tier room has x-gap [2,4].
   Their "templates" are not all-unit templates. The note says these are
   same-axis results, so this is a labeling point.
2. Medium, honesty of the base. As in d212, the theorem needs a census through
   121 and only 21 exists. The note states this.

## Claim 2: compatibility invariant

From s = U/D and s′ = (U+2QmN)/(D+mE) you get δ = mR/(DD′). Substituting
into d212's e(t) = [t − Db(t)/m]δ gives the displayed formula. The log checks
it exactly at 18,464 (stage, level) pairs from the named-room lifts.

Test (1) is correct. |t − Db/m| ≤ D gives |e| ≤ m|R|/D′. A nonintegral base
coordinate Ut/D is a multiple of g/D with g = gcd(U,D), so its clearance is at
least g/D. Integral coordinates need |e| < 1, which g/D ≤ 1 covers. Levels
inside earlier enlarged bands are ordinary unit steps of the current parent,
so the d212 gate covers them unchanged. In all 35 logged stages where (1)
held, the signed gate also held.

The exact-winding remark is immediate: R = 0 gives δ = 0.

**U=1.** A seed with transverse travel 1 never meets a transverse wall
strictly inside its path, so it is the direct chord inside one unit column.
With N = 0 the child path is again a straight chord with transverse
coordinate in (0,1) at every internal level, so every gate passes. The log
confirms this for five height pairs in the two-tier room.

**Gaps.**

1. Medium, scope of U=1. "In any order" holds for lifts on the axis where U=1.
   A lift on the other axis changes that axis's travel: a traversed x-gap of
   gain E makes the x-travel 1+E. Later y-lifts then have U ≠ 1. State the
   claim per axis.
2. Low. "The next m and Q come from the original itinerary" needs the
   previous stage to pass the gate. That holds inductively, but say so.

## Claim 3: comparable-gap determinant theorem

The cancellation is exact. With current travels UA and AT+B and
cⱼU = 2QⱼNⱼ, R = cⱼU(AT+B) − (cⱼT+bⱼ)UA = U(cⱼB − bⱼA). The log checks the
identity on 864 grid cases. Test (2) is test (1) with gcd ≥ 1 dropped. The
threshold on T is the linear rearrangement. The first-lift argument is right:
the gate set in s′ is an open interval containing s₀, so zero in its closure
gives all of (0, s₀].

**Tiers example.** The room is strictly simple with r = 2, and marks 1 and 4
make every y-gap a unit. The direct seed has U = 2, D = 3. For
E₀ = 1..30, 57 and 100 the log confirms each of these:

- The first lift (N₀ = 0) passes the gate, is legal, and has slope 2/T.
- The second lift (E₂ = 6T+1, N₂ = 1, Q₂ = 6, m₂ = 1) has R = −2.
- Tests (2) and (1) hold, the gate passes, and the exact trace reaches T.

The threshold (mB|R| − B′)/(A′ − mA|R|) = −1/5 is negative, so every T works.
The U=1 offset example (T < (1+2Q)T + 1) is correct.

**Gaps.**

1. Low. The letter T is both the target mark and the first-lift travel. Rename
   the travel.
2. Low. The theorem keeps the template seed and its itinerary fixed, so it
   applies only to rooms whose later gains are affine in T with a common T.
   The note says this ("in this regime").

## Claim 4: two-tier counterexample

All parts check for n = 1, 2, 3:

- Exact replay through the lower band (N = 5n) is legal.
- The replayed parent has U = 1+40n, D = 2+80n, and a half-integral coordinate
  at the interface t = 1+80n, with Q = 5 and m = 1.
- No winding with s′ > 0 passes the upper gate (19, 31 and 43 windings).
- min |δ| equals 5/(12+160n), and |tδ| > 1/2 at the interface.
- N = 0 on both lifts passes the gate and is legal.

The claim is about the signed gate certificate, and that is what it shows.
The exact traces add a finding the note doesn't state: 9 of 19, 12 of 31, and
17 of 43 of those gate-failing re-aims are legal rays. The replayed seed's
lift is not geometrically dead. Only the certificate fails. The note's
conclusion, that the template-clearance argument can't be applied after an
arbitrary successful lift, is still right.

## Claim 5: ratio condition and √2 obstruction

The derivation is correct, with strict inequality. Inside an earlier band the
new band is not traversed, so the child path is straight there with slope s′
in the same local time. For a nonintegral crossing τ the levels ⌊τ⌋ and ⌈τ⌉
bracket the integer, because 0 < s < 1. For an integral crossing, τ±1 do.
The gate keeps each new crossing within one unit of the old one. Two
consecutive crossings then give |1/s′ − 1/s| < 2. All 31 gate-passing
staircase last stages in the log satisfy (3).

The √2 algebra is correct: matching the leading coefficients m₁/U₁ and
(m₁ + m₂√2)/U₂ forces √2U₁ = 2Q₂m₁N₂.

**Gap.** Medium. The two-crossing hypothesis isn't automatic in that setting.
With U₁ bounded and s₁ → 0, each traversal of band 1 has transverse travel
about U₁/m₁, so two interior crossings need roughly U₁ ≥ 2m₁. The note marks
the obstruction as conditional, so this is a reminder, not an error.

## Claim 6: offset four-tier staircase

**Structure.** For t in {1, 2, 5, 17, 100, 200} the room is strictly simple
with 6 reflex corners and x walls 0, 1, 3, 4, 6, 7. The marks add x = 2 and 5.
Only the two middle y-gaps are nonunit, and the compressed area is 18.

**Fixed-template impossibility.** The argument is correct. The suffix after
the last lower-band traversal (or the prefix before the first upper-band
entry) has axial travel at most D and transverse travel at least 1. So
s′ ≥ 1/D, while bounded winding gives s′ → 0.

**Direct chord.** The chord is legal for **every** t = 1..200, not only for
large t.

**First lift.** The set s = (3+6n)/D with 1/2 < s < 1 is not only sufficient.
The log shows the template gate set is exactly (1/2, 1) in both orders for
x in {1, 5, 17, 40, 100}. All 26 first lifts traced are legal.

**Interval criterion.** Correct. Before the unit band e(t) = jδ, and after it
e(t) = −jδ measured from the target. The level-j window for js nonintegral is
(⌊js⌋/j, (⌊js⌋+1)/j). For js integral it is ((js−1)/j, (js+1)/j). The
intersection over j ≤ H is the Farey pair (l, u). For t = 1..80, in both
orders and for every first-stage n, the passing windings of the generic d212
gate equal the note's interval set exactly. All 31 gate-passing last lifts
are legal by exact trace.

**Exact-replay gcd criterion.** Correct, including the Bézout step. It agrees
with brute force over n and N for t = 1..200 in both orders.

**Mod-42 theorem.** Correct. D ≡ 21 (mod 42) gives Ds = 15 + 30k ≡ 3
(mod 6). 5y ≡ ±1 (mod 42) gives |6N − ys| = 1/7. The gate errors are at most
H/(7(D+y)) < 1/7. The log confirms:

- 360 arithmetic pairs (x, y) in the class pass the interval test with the
  note's N.
- Four traced pairs pass the gate, are legal, and have
  |s′ − 5/7| = 1/(7(D+y)): (17,17), (17,25), (67,59) upper-first, (101,59).
- √2 members t = 731 (f = 1033 ≡ −17) and t = 1319 (f = 1865 ≡ 17) pass the
  gate and trace legally.

The smallest member, x = y = 17, has area 120. The phrase "every member with
area above 121" is accurate but the theorem covers all members.

**Parity.** Correct. Reflection in integral walls preserves parity, so the
developed x-displacement is odd. Exact replay needs Ep = 6Nq with E and p odd,
which is impossible. Legal last-stage seeds in odd/odd rooms in the log all
have odd p.

**Infinitely many √2 members.** Correct. ⌊√2t⌋ mod 42 = ⌊42{w}⌋ with
w = k√2 + 17√2/42, so the condition is a window of length 1/42. The log finds
47 hits among k < 2000, against about 48 expected. Members with t < 3000 and
f ≡ ±17 are 731, 1319, 2453 and 2537.

### Sweep of the interval test, t ≤ 200

This evaluates the note's criterion on the named √2 family only.

| Outcome | Count of t |
| --- | ---: |
| Passes for some n, lower band first | 46 |
| Passes for some n, upper band first | 36 |
| Passes in either order | 65 |
| Of those, exact replay available | 15 |
| Fails in both orders, every n | 135 |

Passing t start at 18, 23, 25 and 30. The failing list is in the log. It
includes every t from 1 to 17, and 42 failing t have both gains odd, such as
15, 21, 29 and 31. No t ≤ 200 is in the mod-42 class, so those 65 passes come
from other n and windings.

At three failing t the log traces the nearest winding and its two neighbors
for every first-stage n:

| t | Re-aims traced | Legal |
| ---: | ---: | ---: |
| 5 | 3 | 0 |
| 17 | 12 | 3 |
| 100 | 60 | 6 |

So at t = 17 and 100 some gate-failing re-aims of this family still light the
pair. As in Claim 4, the certificate is stricter than geometry. The direct
chord lights every t ≤ 200 anyway, so no lighting question is open here.

## Lemma advanced

The note advances the **marked selection** input of the orthogonal part of
**L1**, as reviewed in d212. Three items are now proved and checked:

- The ordered-chain reduction to a 121-area template census (Claim 1).
- The exact gate algebra across stages (Claim 2).
- A determinant-based preservation theorem for affinely comparable gains
  (Claim 3).

It also gives an exact, checkable selection test for one named irrational
family, with a proved infinite subclass (Claim 6). The note doesn't claim
general marked selection, and it is still open. Nothing here changes the
census dependency: the census still reaches only area 21.

## First case still open

The first open case is the offset staircase at **t = 15**: gains 15 and
⌊15√2⌋ = 21, area 126 > 121. Both gains are odd, so exact replay is
impossible by the parity argument. The interval test fails for every
first-stage slope in both orders:

| Order | n | s | (l, u) | Window for 3+6n+6N | Integers ≡ 3 (mod 6) |
| --- | ---: | --- | --- | --- | --- |
| lower first | 2 | 15/19 | (11/14, 4/5) | (31.43, 32.00) | none |
| upper first | 2 | 3/5 | (13/22, 14/23) | (23.64, 24.35) | none |
| upper first | 3 | 21/25 | (5/6, 16/19) | (33.33, 33.68) | none |

The note's family therefore supplies no passing one-band parent here. Closing
it needs a seed with another itinerary in a one-band parent, or a weaker
certificate than the strict gate. The pair is lit by the direct chord, so this
is a gap in the selection proof, not a dark pair. In general orthogonal rooms
the uniform selection at h₀ = 2 stays open, as the note says.
