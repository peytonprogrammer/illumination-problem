# Review: ferrers-two-windings.md (snapshot 2026-11-22 0835)

**Verdict: sound with gaps.** The two-integer construction is correct, and so are all bounds and the step to (1). Every replayed shot lands exactly on T. The gaps concern dependencies, the transpose statement, and wording, not the argument. Checks: `checks.py`, `checks.log` (22 PASS, 0 FAIL, 5.7 CPU-seconds, `python3 -B`, named rooms only, no searches).

Notation follows the note and d168. Widths w<u<v<W and heights c,d,e,h run top to bottom. Joints are at y3=d+e+h, y2=e+h, and y1=h. The source is a=ys−y3 above the first joint. The target is at depth b=h−yt, with 0<b<h. L=d+e+b and D=a+L.

## 1. Proof

- **Slope and residues.** With M=(z+2ui+2vj)/L, LM−2ui−2vj=z holds identically. So the developed position at the target is exactly z. The identities R₁=−2u(e+b)(i−i₀)/L and R₂=(ez−2vbj)/(e+b)−2ub(i−i₀)/L hold for i₀=d(z+2vj)/(2u(e+b)). The key step uses (d+e)(e+b)−bd=eL. All three identities pass on 3,000 random rational instances.
- **Rounding.** If j is nearest to ez/(2vb), then |ez−2vbj| ≤ vb. If i is nearest to i₀, then |i−i₀| ≤ 1/2. This gives |R₁| ≤ u(e+b)/L and |R₂| ≤ vb/(e+b)+ub/L, as stated. Tie-breaking is irrelevant.
- **Source correction.** Start at X−Ma with slope M−X/D. The developed position minus the unshifted one is X(1−t/D). It equals XL/D, X(e+b)/D, and Xb/D at the three joints and 0 at the target, as checked exactly. Because a>0, we have |XL/D|<w even when |X|=w. The correction terms satisfy |X|(e+b)/D < w(e+b)/L and |X|b/D < wb/L, both strict, so strictness doesn't need X≠0.
- **Gate criterion.** (u+w)(e+b)/L ≤ u is equivalent to w(e+b) ≤ ud. Also vb/(e+b)+(u+w)b/L ≤ v is equivalent to (u+w)b(e+b) ≤ veL. Both equivalences are exact. The true gate values are strictly below these bounds, so equality in (1) is allowed. The ledger room N1 attains equality, 2=2, and replays correctly.
- **Uniformity in b.** e+b<e+h, and b(e+b)/(d+e+b) is strictly increasing in b. So (1) implies both gate tests for every b in (0,h).
- **Same slope at both joints.** The construction is legal. In each band, the physical abscissa is the fold of the developed position modulo twice the band width. Subtracting 2ui or 2vj only re-indexes the unfolded copy. Assume |s| is less than the narrower width at a joint. Then both folds give |s| with the same signed velocity, so the path continues as one billiard trajectory. The two integers are independent. Nothing forces one slope to be a common period.
- **Legality and corners.** The ray only descends. It crosses each horizontal seam inside the opening and never meets a horizontal wall. The vertices (w,y3), (u,y2), and (v,y1) are excluded by the strict gates. A gate value 0 is a contact with the straight left wall at a non-vertex point. This occurs in N1, where the replay is legal. The bottom band is entered at depth below h−b>0, so the floor corners are never reached. The top-band fold holds because X−Ma ≡ x (mod 2w).
- **Transpose.** The diagonal swap maps the room to a Ferrers room. It maps the top cell to the bottom-right cell, and the reverse. Lighting is symmetric, so the transposed test closes the same open pair. In closed form, the transposed (1) is hu ≤ (e+h)(v−u) and (e+2h)wu ≤ v(u−w)(d+e+h). This agrees with the transposed room on 3,000 random rooms.

## 2. Exact tests

The d168 tracer is copied verbatim. Each check requires all of the following:

- The trace ends exactly at T.
- The gates and both bounds hold.
- The traced physical abscissa at each joint equals |gate|.

| Room (widths; heights c,d,e,h) | Pairs | Result | Max reflections |
| --- | --- | --- | --- |
| G, grid (0,2,10,23,230) | Note pair, 16 half-lattice, 6 random rational | 23/23 | 22,032 |
| N1 ledger (1,2,3,4; 1,1,1,1) | 1 half-lattice, 10 random | 11/11 | 20 |
| N2 d17 (3,4,9,12; 3,4,2,3) | 81 half-lattice, 10 random | 91/91 | 146 |
| A1 (1,3,5,7; 1,2,1,1) | all half-lattice, 10 random | 12/12 | 52 |
| A2 (2,5,9,12; 2,3,2,2) | all half-lattice, 10 random | 34/34 | 102 |
| T1 (3,4,12,13; 1,1,1,1), transpose only | all half-lattice, 10 random | 13/13 in both frames | 78 |

- **The note pair (1,115)–(115,1).** The values are j=20, i=75, M=2535/22, X=21/11, and slope 2189/19. The trace has exactly 5,490 side reflections, as the note claims.
- **Both d168 uncovered rooms now satisfy (1).** N1 does so with equality in the first test, and N2 satisfies 15 ≤ 16 and 105 ≤ 162.
- **Room T1.** T1 fails (1) directly but passes the transpose, with equality 36=36 in the second test. The shots are traced in the transposed room, then mapped back and traced in T1.
- **Control in the residual room RES.** The note's residual pair (5,55)–(55,5) is lit by the note's own shot, with gates 37/25, −41/25, and 39/5. Overall, 9 of 18 named RES pairs succeed. So the residual is a failure of the sufficient test only, as the note says.

## 3. Coverage of d168 ∪ d170 (lattice, both orientations)

Integer w<u<v<W and c,d,e,h ≥ 1. Write H=c+d+e+h. The room is covered if any of these 4 conditions holds:

- **A (d170):** w(e+h) ≤ ud and (u+w)h(e+h) ≤ ve(d+e+h).
- **Aᵀ:** hu ≤ (e+h)(v−u) and (e+2h)wu ≤ v(u−w)(d+e+h).
- **B (d168):** W/gcd(W, P0·h) > ⌊W/w⌋², where P0 = lcm(den d/(2u), den e/(2v)).
- **Bᵀ:** H/gcd(H, P0ᵀ·w) > ⌊H/h⌋², where P0ᵀ = lcm(den (v−u)/(2(e+h)), den (u−w)/(2(d+e+h))).

The outside region is the conjunction of the 4 negations:

- [w(e+h) > ud or (u+w)h(e+h) > ve(d+e+h)]
- [hu > (e+h)(v−u) or (e+2h)wu > v(u−w)(d+e+h)]
- W/gcd(W,P0h) ≤ ⌊W/w⌋²
- H/gcd(H,P0ᵀw) ≤ ⌊H/h⌋²

B can hold only if W ≤ w²+w−1, and Bᵀ only if H ≤ h²+h−1. So an explicit infinite part of the outside region is W ≥ w²+w, H ≥ h²+h, and both A and Aᵀ failing. Only B and Bᵀ involve c and W.

- **The ledger realization is now covered.** N1 = (1,2,3,4; 1,1,1,1) is covered by A, with equality, and by Aᵀ. N2 is covered by A. G, A1, and A2 are covered by A, and T1 by Aᵀ. The d168 rooms R1 to R4 are covered by B only.
- **Outside, named:**
  - RES = grid (0,10,11,13,100), which is (10,11,13,100; 87,2,1,10). All 4 tests fail. The first test of A fails as 110>22.
  - O1 = (2,3,4,5; 1,1,1,5). All 4 tests fail.
  - O2 = symmetric grid (0,2,3,4,6), which is (2,3,4,6; 2,1,1,2). All 4 tests fail. A fails as 6>3. B fails because den(24·2/6)=1.
- The outside region is where both narrow ends are wide relative to the adjacent middle height. Here w(e+h) > ud, or the corresponding transposed failure holds.

## Gaps

1. **Medium (dependency).** The reduction to the single open pair rests on d15 Theorem 3, the r=3 certificate with mask 4991. The note links the d168 review. The correct reference is d169, which reviews Theorem 3 and grades it sound with gaps, interior points only. Theorem 3 also has 1 order type for this word, so every realization is this staircase. The note should cite d169 and say this.
2. **Medium (statement).** "Either this test or its transpose suffices" is asserted without a proof or a closed form. The argument is the symmetry above, and the closed form is Aᵀ. Add both.
3. **Low.** Equality is allowed only because a>0 gives D>L. State this where strictness is claimed.
4. **Low.** A gate value 0 means a contact with the left wall exactly on a seam line at x=0. It's legal because the left wall is one edge. The note says this, but it should name the occurrence (N1).
5. **Low.** The residual paragraph names (5,55)–(55,5) as an example pair. The note's own shot lights it, so pick an example where nearest rounding fails, or say so.

## 4. Ledger: LLLLLRLRLR

These steps would make the word COVERED for lattice rooms with interior marks:

- **Accept the dependencies.** Accept d15 Theorem 3 (d169), d168 (test B), and this note (test A).
- **Close the outside region in Section 3.** Every room there, including RES, O1, and O2, needs all pairs of the top-cell and bottom-right-cell open pair lit. Either extend the construction or find a dark pair. The construction could be extended with adjacent integers, a source sign choice, or a floor bounce.
- **Boundary marks**, if the ledger counts them. Theorem 3 covers interior points only.

Until then, LLLLLRLRLR stays PARTIAL. The region it covers is now A ∪ Aᵀ ∪ B ∪ Bᵀ.
