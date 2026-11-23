# Review of d194 "First entry and the divisor that survives a seam cut"

Note: `snapshot.md`, sha256 `220ff73ab968…` (prefix 220ff73a confirmed).
Script: `checks.py` → `checks.log`. 12 exact checks, 0 failures, 12.8 CPU-s.
The script uses only parameters the note names. It runs no room, ray, direction, word or size search.

## Verdict

**PASS WITH CORRECTIONS.** Confidence: about 80%.

Every algebraic step I checked is exact: (2), the determinant conversion, the area chain, the step 2 contact formula, the step 3 far-wall complement, the step 4 frequencies f and g, and both step 5 divisor bounds. The first-entry proof is sound for a fixed integral template. The corrections are about stating uniformity and two implicit hypotheses. None of them breaks a claim.

## Checks (a)–(e)

### (a) Transverse first entry: correct

- With mouths sealed, the upper chamber is an integral rectilinear polygon. Its unfolding is square-tiled, so saddle connections have rational slope. An irrational slope from an integral mark hits no vertex, and the flow is minimal, so the ray enters a grounded cell.
- The ray can't enter through a sealed mouth before the first entry, since that mouth is the bottom of a grounded cell. The cell roof is a wall. So the first entry is through an open vertical side. This is correct.
- P-invariance holds: each strip passage has integral travel, and shifting speed by 2β·k advances the phase by 2βkw. P = lcm of the doubled heights works by induction on exits. It needs no bound on revisits.
- The exclusions are stated correctly: moving clipped mouth endpoints, and targets on or inside the union.
- Implicit step (Low 3): every component of the sealed upper chamber contains a grounded cell. This holds because the room is connected. Minimality is applied per component.

### (b) Eliminating distinct heights: correct

- H+β_j = (m+jn)/n. Multiplying (1) by 2u∏(m+jn) and reducing modulo T leaves P n S_b ∏_{j≠b}(j−b)n. Since gcd(n,T)=1, this gives T | P C_b S_b. The script confirms it on 35,883 integral instances of (1).
- Conversion: g·w ≡ n(jB₀−iAb) (mod T), with g = gcd(Am,B₀n). The script confirms it on 72,765 tuples, which gives T | P C_b p_last (jB₀−iAb).
- The induction-stop paragraph is right. Two full visits at height b with coefficients −1,+1 give S_b = 0, so (2) is vacuous. The note calls this a failure of the inference, not a dark pair. That label is correct.
- Independent offset: the Bézout step T | P₁C₁P₂C₂p₁p₂·gcd(w₁,w₂) is correct.

### (c) Two-return area bound for an inside-column source: correct, with constant caveats

- **Step 1.** The residues of kℓP have spacing C/q₀. Direct failure gives C/q₀ > (B+ℓ)η, so q₀ < C/(Bη). Restricting k to multiples of q₀ makes ℓkP ≡ 0 (mod C). This is correct. Here C = 2(H+b) depends on the lower box. It's bounded only through the comparable upper bound H ≤ H* (Medium 1).
- **Step 2.** From 2z ≡ e−s−(B+2j−ℓ)v (mod C), the contact is y = (e+s−(B+ℓ)v)/2 or y+Z, and the folded heights sum to Z. All three are verified exactly. Under (ii), one contact is ≤ Z/2 ≤ H. Under (i), each contact is legal either way. Root deletion with four progressions and the midpoint choice gives uniform clearance. Because y depends on v only, not on k, the contact choice is k-independent. This is the key point, and it holds.
- **Step 3.** A zero total advance mod 2H puts the far wall at a phase that is a multiple of H. So its height is y or H−y. Verified.
- **Step 4.** f = q₀Pjn/(2T) and g = q₀P(A/B₀ − jn/m). Both verified. The error budget E = 2C+2H is generous. The rules r < clearance/(4(2X+j+1)) and ρ < min(1/8, clearance/(4E), Br/(2E)) give a correction Eρ/B < r/2, and the gates stay legal. Correct.
- **Step 5.** For p ≠ 0: T | p q₀ P j B₀ m n, gcd(n,T) = 1 and gcd(m,T) = gcd(m,b) ≤ b, so T ≤ bKq₀PjB₀. For p = 0: m | q q₀PjB₀, and T = m(1+b/H). The script verifies both on 8,920 relations.
- **K.** K = 1+⌈8/(π²ρ³)⌉ makes the s = 2 tail 4/(π²Kρ³) < 1/2. That's below the constant term 1, so it suffices. d193 used 16, which gives a tail below 1/4. Both values are valid. The note should say which tail it targets (Low 1).
- **gcd(D,u)=1 conversion.** D = Am/g and u = B₀n/g, so D ≤ Am, u ≤ B₀n, n ≤ T/b and m ≤ T. Physical area ≤ AT² + VB₀(T/b)². Verified. This needs b ≥ 1, which holds in an integral template, but the note doesn't state it (Low 2). It also needs the anchored normalization, and the note says so.

### (d) d193-scope paragraph: correct

- **Δ ≠ 0 for 0 < w < D.** jB₀ = iAb with A, B₀, b > 0 forces i and j to share a strict sign or both be zero. So w ≤ 0 or w ≥ D+u. Exhaustive small check passes. This matches d193 Low 1.
- **k = 0.** w = D is the entire box. Matches d193 Low 2.
- **Family.** w = u = m(2m+1), D = (m+1)(2m+1), c = m, (p,q) = (1,2), with H = (m+1)/m, β = 1, P = 2. Equation (1) equals exactly 1, and gcd(D,u) = T = 2m+1 for m = 2..79. Matches d193 Low 5.
- The other two claims also hold. "w = 2m+1 absorbs L, no oddness needed" matches d193 Low 2. "Costs at least a power of H*" matches d193 Low 3.
- The note correctly says the two-return bound doesn't close the offset case.

### (e) First open case: correctly labeled, and the right next case

- The note states the failure as a failure of step 2's mechanism: both virtual contacts land in open gates for every usable v and sheet. It asserts no dark room, which is the correct label.
- This case is the exact complement of (i) ∪ (ii) within the pair type the note just covered. So it's the right next case for this mechanism.
- Two parallel residuals are listed elsewhere and are not ranked against it. One is the repeated full traversal of the terminal column, where (2) is vacuous. The other is targets inside grounded cells. The note should say that the H < b open-gate case is next *for the inside-column row*, not overall (Low 4).

## Corrections by severity

### High

None.

### Medium

1. **Step 1 and step 5 uniformity.** q₀ < C/(Bη) with C = 2(H+b). Write it as q₀ ≤ 2(H*+b_max)/(B_min η), so the bound T ≤ bKq₀PjB₀ is visibly uniform. Without this, a reader can't see that q₀ is independent of the lower box.

### Low

1. **K target.** State that K = 1+⌈8/(π²ρ³)⌉ gives an omitted mass below 1/2, which is less than the constant term. d193's 16 gives below 1/4. Either works.
2. **b ≥ 1.** State b ≥ 1 (integral template) where n ≤ T/b is used, both after (2) and in step 5.
3. **First entry.** Add that each component of the sealed upper chamber contains a grounded cell, by connectedness. Minimality is applied per component.
4. **Open-case ranking.** Say "first open case for the inside-column row". The repeated-terminal-traversal failure of (2) and targets inside grounded cells are separate residuals.
5. **Constants scale.** As in d193, the area bound is at least a fixed power of H*. Repeat this for the two-return bound, since ρ depends on the clearance, and the clearance scales with B/2 and Z_min.

## Scope

- Fixed marked integral upper template with aligned mouth edges, and the comparable bounds of d191–d192.
- First entry: targets strictly outside the closure of the grounded union.
- (2): terminal height visited once, with physical integer widths.
- Two-return bound: a source strictly inside a template-width right column, with a solid lower roof on the left wing, a target approach on the right, and either (i) a solid left side above the roof or (ii) H ≥ b.
- Moving clipped mouth endpoints, offsets that break gcd(D,u) = 1, and rectangular upper templates are out of scope. The two-rectangle theorem already covers rectangular upper templates.

## L1 advance

The advance is real but modest.
- First entry replaces d193's transverse-approach hypothesis with a lemma, for targets outside the grounded union.
- (2) extends the single-column divisor to itineraries through many distinct heights.
- The two-return bound closes the d193 Medium 1 gap for inside-column sources under (i) or (ii).
- No ledger word moves. The W = 10 word LLLRLLLRLR stays open, and its quoted realization matches d193.
- The W ≤ 20 estimate doesn't change from this note.

## First open case

H < b, with the non-target side of the column opening into another upper component, and both virtual contacts in open gates. It's labeled correctly as a mechanism failure, not a dark pair. It's the right next case for the inside-column row. Closing it needs a return in the other component that preserves the signed height, or that supplies a controllable replacement phase.
