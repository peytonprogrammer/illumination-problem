# D229 review: witness selection in the parabola and window families

Referee review of `note-snapshot.md`. Exact Fraction traces reuse the tracer
in `../d227-review-pinned-pairs/checks.py`. Every room, parameter point and
direction is hand-chosen. The run has no sweeps and no ray, direction, word or
room-size searches. `checks.log` ends with `FAILURES: 0`, using 0.02 s of CPU.

## Verdicts

| # | Claim | Verdict |
|---|-------|---------|
| 1 | Five-reflex parabola room: strictly simple, 5 reflexes, both marks pinned | CORRECT |
| 2 | Gate lemma, roof condition, winding choice, divisibility, error bound | CORRECT |
| 3 | Lit for all m≥3 and integer u≥m+2 | CORRECT |
| 4 | Seven-reflex witness is a bounded walk for all c | CORRECT |
| 5 | Bounded-template membership by extreme occurrences | CORRECT WITH GAPS (minor) |
| 6 | One-gap tails, affine tests, diagonal caveat | CORRECT |
| 7 | First open shape (figure-eight) | CORRECT |

## Claim 1

The tiers (−2,1), (−1,1), (0,m), (0,m+2), (0,m+3) at levels
−1, 0, m, u−1, u, u+1 give a 14-vertex polygon. The reflexes are (−1,0),
(0,m), (1,m), (m,u−1) and (m+2,u). At all 11 test points the room is
orthogonal and strictly simple with 5 reflexes. S=(0,0) and T=(m,u) are
interior, and each coordinate lies on a wall line.

## Claim 2

- **Gate lemma.** The fold of (−1,1) is a triangle wave of period 4. It is zero
  at every even integer, with slope (−1)^j at 2j. For |δ|<1, choose
  σ=sign(δ)(−1)^j. The ray then enters y=m at x=|δ| in the open gate (0,1).
  After entry its abscissa is |ps−2j|, a linear function from δ to m. It stays
  below m before s=D, so it misses every right wall and the corner (m,u−1).
  It meets x=0 once, only when δ<0, at height 2j/p in (m,D). That part of
  x=0 is a smooth wall.
- **Roof case.** The roof hit is at x=m−p. Since 0<p<m, it lies in the open
  roof face (0,m+3) and avoids (0,u+1).
- **Winding.** The nearest multiple of 2U to m² has error at most U<u. A zero
  error with U<m becomes 2U<U+m=u after j→j+1.
- **Divisibility.** Suppose U≥m and both 2U and 2(U+2) divide m². Then
  m²/2 is a positive multiple of lcm(U,U+2)≥U(U+2)/2>m²/2, which is
  impossible. The roof error is therefore nonzero and at most U+2<D.
  pV=m−δ follows from 2j=pm−δ and pD=m+2j. Then p<(m+1)/(m+2)<1<m.
- **Error bound.** The error is less than u (D=u) or D (roof) in every
  branch, so 0<|δ|<1 holds.

The traces confirm all of this: gate abscissa equal to |δ|, narrow-tier bounces
alternating x=±1, and upper reflections exactly at (0,2j/p) when δ<0 and at
(m−p,u+1) in the roof case.

## Claim 3

The tracer reaches T with the note's direction (σ(m+2j), D) at all 11 points:

| (m,u) | Case | Branch | D | j | δ |
|-------|------|--------|---|---|---|
| (3,5) | u=m+2, δ>0 | nearest | 5 | 2 | 1/5 |
| (4,6) | u=m+2, 2U\|m², U<m | j+1 | 6 | 5 | −2/3 |
| (6,9) | 2U\|m², U<m | j+1 | 9 | 7 | −2/3 |
| (4,12) | 2U\|m², U≥m | roof | 14 | 1 | −2/7 |
| (6,24) | 2U\|m², U≥m | roof | 26 | 1 | −2/13 |
| (5,24) | u=m²−1 | nearest | 24 | 1 | −13/24 |
| (5,25) | u=m² | nearest | 25 | 1 | −3/5 |
| (5,26) | u=m²+1 | nearest | 26 | 1 | −17/26 |
| (20,22) | m=20, u=m+2, 101 bounces | j+1 | 22 | 101 | −2/11 |
| (20,220) | m=20, roof | roof | 222 | 1 | −2/111 |
| (20,401) | m=20, u=m²+1 | nearest | 401 | 1 | −362/401 |

As a control, the direct chord at m=5 hits a corner at u=24 and u=25 and
reaches T at u=26. This matches "direct template exactly for u>m²".

## Claim 4

Launching at (−5c,1) gives the path (0,0) → (−c,1/5) → (8c,2). It crosses
y=1 at 3c. The room has 7 reflexes and both marks are pinned at c=1, 2 and 9.
Each path is the c=1 path with abscissas scaled by c. Axis scaling commutes
with reflections, so the cell sequence is independent of c.

## Claim 5

The argument is sound:

- Equal velocity signs force an even number of flips per axis, so the return
  map is a translation. Its vector is an integer combination of wall
  coordinates.
- With Δ fixed, each cleared face test and each time comparison is affine in
  the occurrence index. Its values at the first and last occurrence bound all
  the others.

In the (20,22) witness, the x=+1 and x=−1 phases have 51 and 50 occurrences.
The developed faces step by 4, the cleared tests have zero second differences,
and the event times have constant positive spacing.

Minor gaps, none affecting the conclusion:

- The convexity step needs the two consecutive exits to lie on distinct sides
  of the developed cell. Collinear subdivision faces need that stated.
- The S and T endpoint sectors enter only as "fix the endpoint sectors".
- "Polynomial comparisons" are polynomial jointly in the lengths and the
  exponent k, not linear. The note does not claim more.

## Claim 6

Only a coordinate on the varied axis carries g. Every product in a cleared
test pairs coordinates from opposite axes, so every test is affine in g. The
tail criterion (a>0, or a=0 and b>0; equalities identically zero) is right.
The diagonal caveat is right: in a two-gap cone the diagonal meets every
coordinate fiber at most once and is still unbounded.

Hand check (m=5, j=1, δ>0 word, varying the gap (m,u−1)): the gate tests are
35−2u>0 and 3u−35>0. Their slopes are −2 and +3, so this word has no tail.
They predict lit exactly for u in 12..17. The traces agree at u=11 (corner
(1,5)), 12 (T), 17 (T) and 18 (not lit by this word).

## Claim 7

- An SCC with a single simple cycle forces powers of that cycle.
- An acyclic condensation bounds the number of powered blocks by the number of
  states.
- A strongly connected component that is not one cycle has a vertex with two
  out-edges, so two distinct simple first-return cycles share a base state.
- (AB)^k needs 2k blocks.
- The quantifier for refuting a universal N(r) is stated correctly: the
  minimum number of blocks over all legal witnesses must be unbounded.
- Neither test family interleaves.

## Which lemma advanced

**L1**, pinned-pair lighting via bounded witness templates. The parabola room
was the non-Presburger example for one fixed itinerary. As a lighting
question it is now settled: every allowed (m,u) is lit by one of finitely many
bounded templates, each a power of the single narrow-tier cycle. The
non-Presburger domain belongs to the direct itinerary only, not to the lit
set. The one-gap tail test is a valid per-template tool. It gives no area
bound.

## First case still open

Witness selection in a recurrent strongly connected component with a branch,
the figure-eight. The question is whether a legal witness that interleaves two
first-return cycles can always be replaced by one with boundedly many blocks
aimed at the same pinned target. No pinned room family with r≤8 forcing
unbounded interleaving is known, and neither tested family has one. No N(r)
and no census area bound follow from this note.
