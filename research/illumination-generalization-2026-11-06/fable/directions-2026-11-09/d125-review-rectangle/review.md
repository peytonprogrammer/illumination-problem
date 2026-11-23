# D125: review of large-rectangle-access.md and rectangle-windings.md

Date: 2026-11-20. Reviewer: independent referee. The reviewed texts are
`large-rectangle-access.snapshot.md` and `rectangle-windings.snapshot.md`.
Both are identical to the live notes in `qclass-closure/bbbb/` at review time.

All computation is exact and uses `fractions.Fraction`. Python ran with `-B`,
under 0.1 CPU seconds in total. No room, ray, direction or reflection-word
search was run. Each traced slope is the matching root that the note's
construction prescribes for a named room. Files: [checks.py](checks.py),
[checks.log](checks.log). Every check passes.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Opposite doors: explicit H₀ = 8wPQ^d lights the pair | Sound |
| 1a | Bertrand primes, simultaneous approximation, choice of p and k | Sound |
| 1b | Forbidden-crossing count and modular clearance 1/(pD) | Sound |
| 1c | Sheet bookkeeping and IVT matching with fixed entry and exit sheets | Sound |
| 1d | Same-side extension, with the single compulsory midpoint crossing | Sound (conditional, as stated) |
| 1e | Scope paragraph (δ from effective-chamber.md) | Sound with fixable gaps (low) |
| 2a | Torus winding lemma, K bound independent of point denominators | Sound |
| 2b | Perpendicular gluing at frozen centers; finite-width sufficient test | Sound |
| 2c | Explicit bound for rational normalized centers, c ≥ 1/(d²·max) | Sound; useless in lattice rooms, as the note says |
| 2d | Uniform computable threshold under compact bounds | Sound with fixable gaps (low) |
| 3a | Limiting corner obstruction on the torus | Sound |
| 3b | Finite width: a path avoiding both far walls is the direct chord | Sound |
| 3c | Implied weight of the obstruction at finite width | Gap (medium): normalized only, not physical |
| 4 | Assembly with d110–d114 into a whole-room n₀(r) | Not plausible yet. Nothing is overclaimed |

## 1. Opposite doors (large-rectangle-access.md)

**Constants.** B = max(64, ⌈32/(ρ₀δ)⌉), k₀ = 4d+8, P = 2^k₀·B, Q = 32P and
H₀ = 8wPQ^d are explicit. The k₀ primes in (2ⁱB, 2ⁱ⁺¹B) have product above
B^k₀·2^(k₀(k₀−1)/2), which exceeds Q^d = B^d·2^((k₀+5)d). So at most k₀−1 of
them divide any D ≤ Q^d, and some p ≤ P avoids D. The list is fixed before D.
The pigeonhole over the Q^d+1 vectors of fractional parts gives
|cᵢ − Cᵢ/D| < 1/(QD). Irrational or large-denominator centers cause no loss.

**Matching and sheets.** In the vertical unfolding with period 2, a signed
height a encodes the physical height |a| and the vertical velocity sign. A
vertical-side reflection reverses only horizontal velocity. So q traversals
give the exact equation qρs + a(s) − b(s) = 2k, and q = p is odd for opposite
sides. The nominal slopes for consecutive k are 2/(qρ) apart. The middle half
of I has width δ/2 ≥ 4/(pρ), because pρδ > 32. So it holds two consecutive k.
Their residues B₁−A+2kD differ by 2D, which is nonzero mod p. At least one k
is allowed. At the ends of I the centered mismatch is at least qρδ/4 ≥ 8 in
size. The access legs move it by at most w/H. The IVT root keeps the same k
and both fixed sheets.

**Forbidden crossings.** Yⱼ has numerator (q−j)A + jB₁ + 2jkD over qD. Modulo
p this is j(B₁−A+2kD), nonzero for 0 < j < p. So Yⱼ sits at least 1/(pD) from
(1/D)ℤ. That grid holds every signed door approximant, its translates by 2,
and the corner heights 0 and 1. The error budget is w/(2H) + 1/(QD) for the
crossing and the same again for door half-width and approximation. With
H ≥ H₀ the total is at most 3/(16pD) < 1/(2pD) < 1/(pD). The count of
forbidden crossings is therefore zero, for every door on both vertical sides.
Horizontal contacts occur at interior abscissas, so they are smooth.

**Explicitness.** H₀ depends only on ρ₀, δ, d and w. It doesn't depend on W,
the door heights, or their denominators. For d = 2, ρ₀ = 1 and δ = 1/2,
H₀ = 2^79·w. With δ from effective-chamber.md, H₀ grows like
(T²)^(d+1)·2^O(d²), with T exponential in chamber area.

**Same-side extension.** For q = 2p and p ∤ j the same residue argument gives
spacing 1/(2pD), and the H₀ budget still fits. At j = p the height is
(a(s)+b(s))/2 + k for every even q, so the midpoint is compulsory. The stated
clearance test (distance > w/H from far-side centers, > w/(2H) from corners)
is the correct sufficient condition. The note states it as a condition, not
as a result.

**Scope paragraph (gap 6).** The δ values come from effective-chamber.md,
which d124 found sound with fixable gaps. Those charts are centered on slope
α = 1/φ² for vertical mouths. So they give a common interval for opposite
doors, as used here. See gap 3 for perpendicular doors.

## 2. Perpendicular doors (rectangle-windings.md)

**Torus lemma.** The transverse value det(v, γ_K(t) − A) = t·det(v,d) doesn't
depend on K. With integral u, u(v) = 1, the map x ↦ (det(v,x), u(x)) is
unimodular. So a collision at time t is exactly Kt ≡ c (mod 1). K = 0 violates
no congruence, since the original chord is clear. Irrational t forbids at most
one K. Rational t = a/b forbids at most one class mod b, never the class 0.
The h-procedure updates each congruence at most once, so h ≤ (2N+1)^N. Each
remaining congruence forbids at most one of N+1 consecutive multiples of h. So
a survivor K ≤ K₀ + (N+1)h exists. The bound uses only |F| and det(v,d). This
part is correct. The constants are liberal (N+1 would do for 2N+1).

**Gluing.** In ℝ²/2ℤ² the reflected images of all centers on all four sides,
plus the four corners, form F. The signs of a and b, with D positive, give
the required entry and exit velocities. I checked the fold sign for each of
the four cases. The direct chord lies in the open rectangle, so the lemma
applies.

**Finite-width test.** I rederived each term. The mismatch at the ends of I
is at least μ(Δₓ−e) − (τ+1)e. Since μ + τ ≤ τ_max, the term μΔₓ/[2(1+τ_max)]
suffices. Crossings move by at most e(1+τ) on vertical lines and e(1+1/τ) on
horizontal lines. Adding the half-width e gives c > e(2+max(τ,1/τ)), which the
stated bound implies. The endpoints' noninteger coordinates stay in their
grid intervals, so the crossed lines are the same.

**Explicit rational bound.** Crossing ordinates have denominator dividing
d·(dΔₓ), so c ≥ 1/(d²·max(1,Δₓ,Δᵧ)). This is correct. In a lattice room the
normalized denominator is about H, so c ~ 1/H² while e ~ w/H. The bound then
gives no threshold, as the note says.

**Uniform computability (gap 5).** The parameter set is compact, and the
menu of (v, K) is finite. Each margin function is continuous, and the
pointwise maximum is positive. So a common margin exists, and quantifier
elimination finds it in finite time. Two wording fixes apply. First, η ≥ η₀
keeps both designated centers away from all four corners of their walls, not
only the shared one. Second, the result needs η₀ in normalized units. Doors
at fixed physical distance from a corner have η → 0 as H grows. So the
theorem misses the main scaling regime of a lattice room.

## 3. The shared-corner obstruction

**Limit.** The corners are the four 2-torsion points of ℝ²/2ℤ². A return from
corner P is P → P+2u with u ∈ ℤ² nonzero. If u is primitive, then u ∉ 2ℤ², so
the midpoint P+u is a different corner. If u = g·u₀, the segment passes
P+u₀ at time 1/(2g). So every nonconstant return meets another corner in its
interior. Every member's normalized margin tends to 0, so no uniform menu
survives the limit. This is correct.

**Finite width.** Entering from the left wall, x can't decrease without a
right-wall hit. A first top contact before the door turns the velocity
downward, and only the bottom wall reverses it. A downward entry can never
reach the top. So a path avoiding both far walls is the open chord with
sB(s) = A(s). This is correct.

**Weight of the obstruction (gap 4).** The obstruction is to normalized
clearance, not to legal paths. Part C of checks.py takes left door
[H−3, H−1] and top door [1, 3], W = 3H/2, with entry and exit sheets
fixed downward and leftward. The direct chord is impossible on that branch.
The K = 1, v = (1,1) winding has slope s = (2H−3/2)/(2W−3/2). It hits the
bottom wall 5(1+s)/(4s) ≈ 3.125 units left of corner (W, 0), exactly. Then it
hits the right wall at height ≈ 2.083 and exits through the top door. The
trace reaches the target at H = 1000, 10⁹ and 2²⁰⁰. The note's c-test gives
0.52/H against e = 1/H, so it can't certify this path. The far-corner miss
has fixed physical size. The finite-width near-corner problem is a bounded
local check at the far corner, not a scaling limit.

## 4. Assembly into a whole-room n₀(r)

Neither note claims n₀(r). Both state the missing pieces. I find no
overclaim. Together with d110–d114 and effective-chamber.md, the proved cases
are:

- a long corridor between two bounded chambers (d110–d112, effective-chamber);
- a long capped arm on a fixed junction (d114, effective-chamber);
- a large rectangle with ρ ≥ ρ₀, door-free horizontal sides, and opposite
  doors into bounded single-door chambers (this note);
- perpendicular doors with normalized positions in a compact range (this note,
  non-explicit).

These cases don't assemble into n₀(r). The missing pieces are:

1. **A structure theorem.** No result shows that every large BBBB room with
   r ≤ 8 puts each pair into one of these cases with uniform constants. d113
   already refutes the corridor-or-compact dichotomy. The general case has
   several lengths growing at different rates.
2. **Perpendicular doors in lattice rooms.** No explicit or uniform threshold
   holds when doors stay at fixed physical offsets from corners.
3. **Common access charts for perpendicular doors.** See gap 3.
4. **Other placements.** Missing cases include a mark inside the rectangle
   with its partner outside, chambers with several doors, and chambers whose
   area grows with the room. Also missing: horizontal-side doors in the
   opposite case, ρ → 0, and the same-side midpoint when both predictions
   land in doors.
5. **Size.** H₀ is at least 2^79·w even with δ = 1/2. Any n₀ built this way
   leaves a residual census far beyond any CPU budget.

## 5. Replay

**Part A, opposite doors.** d = 4, w = 2, ρ₀ = 1, I = [1/4, 3/4], δ = 1/2.
Then B = 64, k₀ = 24, P = 2³⁰, Q = 2³⁵ and H₀ = 2¹⁷⁴. The room is
W = H = 7·2¹⁷² with width-2 lattice doors. L1 starts at 2H/7 (entry), L2 at
4H/7, R1 at 5H/7 (exit) and R2 at 6H/7. Each door has a depth-2 stub. The
marks are lattice points S = (−1, 2H/7+1) and T = (W+1, 5H/7+1). D = 7 meets
both approximation conditions. The first listed prime is p = 67, and k = 13
has residue 51 mod 67. The root s = (26 + 3/7)/(67 + 2/H) ≈ 0.39446 lies in I. The IVT sign change holds. All 66 values Yⱼ clear (1/D)ℤ by at
least 1/(pD). The minimum door and corner clearance is 0.0064 against the
proof's bound 0.0021. The exact trace from S reaches T with 66 vertical and
26 horizontal reflections. Each traced vertical contact height equals the
predicted yⱼ exactly. In a control, a door moved onto crossing 2 captures the
path into its stub.

**Part B, perpendicular doors.** W = H, ρ = 1, I = [3/4, 5/4], w = 2. The
designated centers are left a = 1/6 and top b = 1/6. The extra doors are at
bottom x = 2/3 and right y = 1/2, with common denominator 6. With v = (1,1), det(v,d) = 1/3,
|F| = 12, N = 24. Two collision congruences arise, giving h = 4, K₀ = 3 and K = 4. Neither
congruence blocks any K here. The prediction matches direct incidence for
K = 0..27. Then
D = (49/6, 53/6), with 16 intermediate crossings and c = 19/318 ≥ 1/318. The
explicit bound gives H > 1323.9. With H = W = 1326, the root is
s = 23427/21659. The exact trace reaches the target with the 16 predicted
reflections.

**Part C.** See section 3.

## Gaps, ranked

1. **High: no structure theorem (assembly).** Fix: state the multi-scale
   degeneration classification of r ≤ 8 rooms as the next lemma. Each limit
   type should be matched to a theorem with uniform constants.
2. **High: perpendicular doors at fixed physical offsets.** The uniform result
   needs normalized η₀, and the rational bound fails at denominator ~H. Fix:
   find an analog of the Dirichlet-plus-prime argument for two wall
   orientations, as the opposite-door note's "next question" asks.
3. **Medium: common chart for perpendicular doors.** effective-chamber.md
   charts sit near slope α for vertical mouths. A top-wall chamber rotated
   gives slope 1/α in the rectangle frame, so the intervals are disjoint. Fix:
   rerun the Fibonacci block argument at slope α while testing top-edge hits.
   Hits then occur on letter-one steps, and the transitivity proof carries
   over with an index shift.
4. **Medium: the corner obstruction is normalized only.** Fix: reword section
   "Exact failure at a corner". Add a corner-passage lemma. For a K = 1
   primitive winding, the far-corner miss is an explicit H-independent
   combination of A(s) and B(s). Legality then needs no door near the far
   corner, plus normalized clearance at the other crossings.
5. **Low: scope of η₀.** State that η ≥ η₀ applies at all corners of both
   designated walls. Note that fixed physical offsets violate it at large H.
6. **Low: notation and dependencies.** d, D and B each carry two or three
   meanings across the notes. The scope paragraph depends on
   effective-chamber.md (d124: sound with fixable gaps).
