# D75: Referee review of the long-corridor theorem (qclass-closure/bbbb)

Date: 2026-11-19. Target: `.context/qclass-closure/bbbb/README.md`, `check.py`, `check.txt`.
Own code: `verify.py` (exact `Fraction` billiard tracer on the explicit polygon, no imports
from Astra/D69/D72 code; D72 JSON read as data only). Log: `verify.log`. CPU: about 9 s.

## Verdict

**Sound, with cosmetic and minor fixable presentation gaps. No fatal finding.** The general
theorem, the uniform threshold, the DB55 bound ℓ ≥ 450, and the 3 + 6k claim all check out.

## 1. Minimality step

- Citation verified. Masur–Tabachnikov, *Rational billiards and flat structures*, Theorem 1.8:
  "For all but countably many directions θ the flow Fθ is minimal on the surface M." The
  proof shows every infinite trajectory's ω-limit set is all of M. That is forward
  density, which is what the README needs.
- Sealing the portal with a mirror returns the original orthogonal chamber (hypothesis).
  Its 4-copy unfolding is a translation surface. Door endpoints are marked regular points
  or vertices. Excluding the countably many directions through developed vertices and door
  endpoints from the fixed mark makes the forward ray infinite, so Theorem 1.8 applies.
- "Crosses the interior of the portal": the upstream set of an open sub-segment, in the
  copies whose horizontal velocity points out through the portal, is open in M. Forward
  density reaches it. Correct.
- Corner and wall starts are handled in the uniformity section: the separatrix from a
  cone point (reflex corner, angle 6π) is a well-defined ray. After one regular point,
  the ω-limit argument applies. Correct.
- **Cosmetic (C1).** Cite "Theorem 1.8 and its proof (ω-limit argument)". The statement
  says "minimal", and the forward-ray version is in the proof. The README links the
  handbook without naming this.

## 2. Persistence

- Slopes are in (0, ∞), so every wall hit is transverse. A ray meets a door endpoint only
  by passing through it, and that set of slopes is excluded. No grazing case exists.
- A finite leg that avoids vertices and door endpoints has positive clearance. Its
  reflection word, its earlier non-door hits on the portal wall, and its first door hit
  persist on an open slope interval. "First portal hit" is well defined. Correct.

## 3. Phase matching

Checked by hand with initial vertical sign σ₀ and m horizontal-wall reflections. Then
ε₁ = σ₀(−1)^m and ε₁y₁(s) = σ₀y₀ + a·s + const, so (ε₁y₁)′ = a. The backward leg gives
(ε₂y₂)′ = −b, where ε₂ is minus the backward-leg sign. Vertical-wall reflections are at
fixed x, so a and b are constant. F is **affine** in s with slope ℓ + a + b, so the IVT step
is trivial.

- The phase convention (+y up, −y down, unfolded coordinate increasing by ℓs) is correct.
  It covers both physical vertical directions.
- The matched path enters and leaves the corridor at y ∈ (0, w). So the first and last
  corridor reflections are at 0 < x < ℓ, on smooth wall. The chamber legs are the
  stabilized legs. Corner-free. Correct.
- Threshold: (ℓ + a + b)(s₁ − s₀) ≥ 2w is sufficient. The stated ℓ ≥ 2w/δ follows because
  a, b > 0. Correct.
- The one-door blind-strip variant is correct as a sufficient condition. It uses only the
  +t phase, and −t would also do. **Cosmetic (C2):** "even at exact resonance" is
  undefined in this file.

## 4. Uniformity over marks

The worry was a slope width whose infimum over marks is 0. The compactness argument
avoids it.

- Each point of the closed rectangle product, including corners and portal points, gets
  three things: a fixed sign choice into its rectangle, one common generic s* for both
  ends, and an open set in (start, slope) space where the itinerary is constant. That set
  contains a relative neighborhood U × [s* − η, s* + η].
- Near a corner, the ray from p′ ∈ R near p, with signs pointing into R at p's active edges,
  moves away from those edges. It stays in R until it is past a time t₀. After t₀ it
  shadows the regular leg from p(t₀). This is the key step, and it holds.
- Finitely many neighborhoods give δ = min η > 0. The leg's horizontal travel a depends on
  the start but not on s, so the IVT works for every pair in the neighborhood.
- **Fixable, minor (F1).** The sentence "after that segment both trajectories have positive
  clearance" asserts joint continuity in (start, slope) without stating it. Add one line:
  "the map (start, slope) → itinerary is locally constant near (p(t₀), s*), and
  p′(t₀) = p′ + t₀(1, ±s) is continuous." The argument is complete in substance.
- Hypothesis note (C3): strict simplicity of the joined room is assumed for each ℓ.
  The proof never uses ℓ-dependence of it.

## 5. DB55 check (own exact code)

Polygon: [0,5]² ∪ [5,5+ℓ]×[2,3] ∪ [5+ℓ,10+ℓ]×[0,5].

| Check | Result |
|---|---|
| Legs from all 16 marks reach the door at s = 1/10 and 1/10 ± 1/450, same travel | 16/16, max travel 44 |
| ℓ = 450: matched slope from the README's F, full exact trace S→T, corner-free | 256/256 |
| ℓ = 451 | 256/256 |
| ℓ = 457 | 256/256 |
| ℓ = 1000 | 256/256 |
| Saved D72 directions at ℓ = 3, 9, 15, 21 (3 + 6k) | 64/64 each |

- In every case, an integer multiple of 2 lay inside [F(s₀), F(s₁)] (asserted).
- Derivation of 450 is correct. Vertical-side visits are at travel d + 5i, so heights
  have fractional part in {.1,…,.4,.6,…,.9}. The door hit comes within 5 visits, so travel
  is ≤ 44. A slope change of 1/450 moves heights by < 1/10. All DB55 vertices and door
  endpoints have integer heights at x ∈ 5ℤ, which covers corner avoidance. The interval
  length is 1/225, so 2w/δ = 450. Same-chamber pairs: 2·C(16,2) = 240. Total
  240 + 256 = 496. Correct.
- Insertion periods: the saved directions are (3,1)×36, (3,5)×8 (period 6), and
  (3,2)×20 (period 3). These match "20 period 3, 44 period 6".
- Observation, not a defect: at ℓ = 5 and 7, all 64 saved directions also still light the
  pairs, through different paths. The 3 + 6k claim is correct and conservative, as the
  README says.

## 6. Other sections (spot checks)

- Shear remark: 2u | L fixes both rims of a height-1 band. Lattice points lie on rims.
  The lcm(10, 2(10+ℓ)) and vertical lcm(10, 2) = 10 figures are right.
- D58 arc bounds: 1 + 1/20 + 1/16 = 1.1125, 1 + 1/20 + 3/16 = 1.2375, and 2 − 1/20 = 1.95,
  with the four phases inside. I did not re-derive the phases from D58 itself.

## Findings by severity

- **Fatal:** none.
- **Fixable gap:** F1, the uniformity paragraph. State joint local constancy in
  (start, slope) explicitly.
- **Cosmetic:** C1, cite the proof of Theorem 1.8 for forward density. C2, "exact
  resonance" is undefined. C3, the per-ℓ strict-simplicity hypothesis.
