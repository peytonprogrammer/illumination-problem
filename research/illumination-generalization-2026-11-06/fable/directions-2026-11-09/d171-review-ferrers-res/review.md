# Review: ferrers-residual-inequalities.md (snapshot 2026-11-22 0855)

**Verdict: sound with gaps.** The d17 chord lemma holds for this word, and O1 and O2 meet it with equality. The RES certificate replays exactly. The union of the five tests doesn't cover all lengths, so LLLLLRLRLR stays PARTIAL, as the note says. Checks: `checks.py`, `checks.log` (37 PASS, 0 FAIL, 14.8 CPU-seconds, `python3 -B`, named rooms only).

Notation follows d170. Widths w<u<v<W and heights c,d,e,h run top to bottom. The chord test is C: d(v−u) ≤ e(u−w).

## 1. The d17 chord lemma (r3.md, Lemma C+ perp form)

**Instantiation.** r3.md states only "Lemma C+ applies when V2 is on or above the chord V1V3". The missing map is as follows.

- The hub is G=[0,v]×[0,h+e+d].
- Door 1 is [0,w]×{h+e+d}, with flat end (0,h+e+d) and mirror side x=0.
- Door 2 is {v}×[0,h], with flat end (v,0) and mirror side the floor.
- Both mirror sides are single walls. The open pair has S in the open top cell and T in the open cell (v,W)×(0,h), so both are arm points.
- G∖P is the rectangle (u,v]×(h+e,h+e+d]. K⊂P holds iff its corner V2=(u,h+e) is on the closed far side of the chord. Cross-multiplying gives exactly C, which is transpose-invariant (checked symbolically and on 3,000 rational rooms).
- K=G never occurs here, because h<h+e+d and w<v.

**Proof steps checked by hand.**

- **Existence (d15 Lemma C, perp).** F(κ)=κb(κ)+a(κ)−H has derivative b+β/κ>0 between jumps, since b ≥ L−w2 ≥ 0. Both jumps are downward and F is right-continuous. The infimum argument then gives a zero with a, b in the open windows. Both jumps point the same way, so they can't cancel at the zero.
- **Affine sign.** c<0 holds at every door point, floor point, and side point, so c<0 on each folded piece. This needs w1<H and w2<L, which hold here.
- **Corner avoidance.**
  - Equality on the chord is allowed. K is closed, and the path has c<0 strictly, so it never meets V2.
  - V1 and V3 are excluded by the strict windows.
  - The hub corner (0,0) is excluded because x°<L ⟺ (−a)(b−L)<LH.
  - The convex vertices (v,h+e) and (u,h+e+d) have c ≥ c(V2) ≥ 0.
- **Interior.** int K ⊂ int P. The door crossings are open-door points, and the reflections are relative-interior wall points.

**Exact tests.** Every window candidate with |k| ≤ 40 was traced, for all 4 sign pairs.

| Room (widths; c,d,e,h) | d(v−u) vs e(u−w) | Pairs | Valid candidates |
|---|---|---|---|
| O1 (2,3,4,5; 1,1,1,5) | 1 = 1 | 22 | 111/111 |
| O2 (2,3,4,6; 2,1,1,2) | 1 = 1 | 28 | 187/187 |
| S1 (2,3,4,6; 3,1,3,2) | 1 < 3 | 36 | 208/208 |
| N1 (1,2,3,4; 1,1,1,1) | 1 = 1 | 13 | 86/86 |

Every pair had a candidate for every sign pair. In the below-chord control D17 (r3.md pair (1,10)–(10,1)), 0 of 4 candidates are valid. This matches r3.md.

## 2. RES certificate

- **Winding equations.** 11·19 ≡ 1 (mod 26). Every integer solution has i=19t+26k, j=8t+11k, M=209t+286k. Completeness is checked.
- **Source constraint and gates.** The developed source position is E−a(M+(Z−E)/L). This gives (1+a/L)E ≡ ±x+aM+aZ/L, and the nearest representative satisfies |E| ≤ 10L/(L+a)<10. The gate expressions at y=11 and y=10, and the bounds A and H, follow exactly.
- **Floor corner.** The floor coordinate is E(B−10)/L+const. The two source signs give ΔE ≠ 0 with |ΔE| ≤ 20. Their floor coordinates therefore differ by a nonzero amount below 100, so at most one sign meets a floor corner.
- **Exceptional depths.** There are 142, as the note says. At a₀=0 the intervals cover (13,100) at 141 of them. b=100/11 is the exception, with exactly the note's three intervals. For non-exceptional b, the spacing 200/11 is less than the t=0 interval length 23+B.
- **Reflection step.** RES is symmetric under (x,y)→(y,x). Any dark pair must sit at b=100/11 with z in a gap, so the reflected pair forces a ≥ 109/22. With a₀=109/22, one merged interval strictly contains (13,100).
- **Replay.** Each pair takes the note's construction with minimal |M| and both source signs, traced exactly.
  - 54 half-lattice pairs: 54/54.
  - 20 random rational pairs, half at exceptional depths: 20/20.
  - 4 pairs at b=100/11 with z in the a₀=0 gaps and a ≥ 109/22: 4/4.
  - Both routes occur, with at most 2,370 reflections.
  - Control: with a=1, the certificate correctly gives no candidate.

## 3. Union coverage

Five tests are in play: C, A (d170), Aᵀ, B (d168), and Bᵀ. A real room is uncovered exactly when it satisfies all of the following:

- d(v−u) > e(u−w), and
- [w(e+h) > ud or (u+w)h(e+h) > ve(d+e+h)], and
- [hu > (e+h)(v−u) or (e+2h)wu > v(u−w)(d+e+h)], and
- B and Bᵀ fail. For irrational lengths, d168's span condition (1) and its transpose must also fail.

Without Aᵀ, drop the third bracket.

- **Why the union isn't everything.** The first three lines involve only (w,u,v,d,e,h) and define a nonempty open cone. B can hold only if W ≤ w²+w−1, and Bᵀ only if c+d+e+h ≤ h²+h−1. So every lattice room in the cone with W ≥ w²+w and c+d+e+h ≥ h²+h is uncovered, and that set is infinite.
- **Real lengths.** (1) fails only on a null set, so the uncovered real set is null. It still contains all of these lattice rooms.
- **Uncovered lattice rooms (all five tests fail):**
  - U1 = (2,3,5,6; 7,1,1,3), from the family (2,3,5,W; c,1,1,3) with W ≥ 6 and c ≥ 7.
  - U2 = (1,2,3,4; 13,2,1,4).
  - U2b = (1,2,3,5; 1,2,1,4).
  - RES also fails all five tests. It is covered only by the note's whole-room certificate.
- **Effect of Aᵀ.** T1 = (3,4,12,13; 1,1,1,1) is covered by Aᵀ alone, so coverage is strictly smaller without it.

## Gaps

1. **High (scope, ledger).** C ∪ A ∪ Aᵀ ∪ B ∪ Bᵀ plus RES leaves an infinite lattice region uncovered, for example U1, U2, and U2b. The note doesn't claim otherwise. The ledger must not move the word to COVERED.
2. **Medium.** r3.md never writes out the instantiation for type 4991: which hub, which mirror sides, and why K⊂P ⟺ C. The instantiation in Section 1 should be added. r3.md also records only 540 tested perp configurations. This review adds 592 traced candidates with 0 failures.
3. **Medium (dependency).** Aᵀ rests on the transpose symmetry, which d170 argued but which the brief treats as unproved. The reduction to one open pair rests on d169 (d15 Theorem 3, interior points only).
4. **Low.** The a₀=109/22 endpoints (−71341/550, 126891/550) are endpoints of single intervals inside a partial merge. A wider enumeration gives a larger component. Only containment of (13,100) matters, and it holds. The note's checker `residual-windows.py` wasn't read; this review recomputed everything independently.
5. **Low.** "On the chord boundary for every placement" should read "on the chord", because equality is a property of the room.

## 4. Ledger verdict: LLLLLRLRLR

The word stays **PARTIAL**. The covered set is C ∪ A ∪ Aᵀ ∪ B ∪ Bᵀ ∪ {RES}. That rests on d169, d17 Lemma C+ (sound per Section 1), d168, d170, and Aᵀ. Without Aᵀ, drop it from the union. Rooms such as T1 then fall outside. Closing the word needs the cone in Section 3. This review didn't check the note's choice of LLLRLLLRLR as the smallest open word.
