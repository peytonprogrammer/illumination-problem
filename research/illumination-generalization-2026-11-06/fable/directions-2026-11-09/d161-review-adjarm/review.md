# d161 review: adjacent rectangular arms illuminate each other

Snapshot: `d95-review-queue/snapshots/adjacent-arm-illumination.2026-11-22-0512.md`.
Checks: [checks.py](checks.py), output in [checks.log](checks.log). The run takes 4.0 CPU seconds and uses exact `Fraction` arithmetic. The tracer stops at every vertex, convex or reflex.

## Verdict

**Sound with gaps.** The local theorem and the whole-room case split are correct. Every constructed shot traced correctly: 80,459 half-lattice pairs and 6,000 random rational pairs in four explicit rooms, plus 1,500 seam pairs, with 0 failures. The gaps concern the definition, the stated condition and scope, not the proof.

## 1. Definition

"Full-side" means each arm's cross-section equals one whole side of the hall. Each side carries zero or one arm, so 0–4 arms. Adjacent arms meet only at the shared hall corner. That corner becomes a reflex vertex with three room quadrants, so the room is strictly simple. `polygon()` asserts strict simplicity for all 16 subsets (log §1).

Wall counts for the 16 subsets:

| Arms | Shape | Walls | Reflex |
|---|---|---|---|
| none, one, or two opposite | rectangle | 4 | 0 |
| two adjacent | L | 6 | 1 |
| three | T | 8 | 2 |
| four | plus | 12 | 4 |

A single arm or two opposite arms only lengthen the rectangle. The class is therefore exactly the rectangles, L's, T's and plus-signs, with independent dimensions. The T and plus can be asymmetric, but no other combinatorial type occurs. The phrase "asymmetric crosses, independently varied depths" is accurate. It doesn't widen the class.

## 2. Proof

- **Direct case.** The crossing height (XY−UV)/(X+V) lies in (−U,0) when XY<UV. The chord then crosses the top door in (−V,0). Correct.
- **Window.** The image chord crosses the open right door exactly when XY/V < Z < XY/V + H(1+X/V). The algebra is correct, and the interval is open.
- **Gap rule.** The images {2jH±U} have gaps 2U and 2H−2U, both strictly below 2H because 0<U<H. The first image strictly above the lower endpoint a is at most a+(max gap) < a+2H ≤ b. The claim holds, including X=V, where the window length is exactly 2H. The run hit 1,703 X=V pairs with no failure. Log §2 confirms that one progression alone can land exactly on b at X=V, for example U=1, H=2, Y=1 gives 5 against the window (1,5). The note's remark on prescribed signs is correct.
- **Corner avoidance.** The chord crosses x=0 once, strictly inside (−H,0). Every arm contact has 0<x<X, so no contact reaches a mouth lip or the cap. The chord never touches the hall corner (0,−H), which is reflex when a bottom arm exists. The tracer confirms that every contact lies on a parallel side of the chosen arm, beyond its mouth.
- **Reversal.** X<V and XY≥UV force Y>U. The swap (x,y)→(y,x) exchanges the arms, and the upper-arm window has length W(1+Y/U) > 2W. Paths are reversible because the stopping rule is symmetric. The three alternatives XY<UV, X≥V and Y≥U cover the domain, since X<V and Y<U imply XY<UV. XY=UV falls into a reflected case. The run hit 761 such pairs with no failure.
- **Reversal is needed.** Using only the S-arm window fails for 479 half-lattice pairs across the four rooms (log §4).
- **Real points.** The argument uses no lattice facts. Random rationals with denominators up to 997 pass (log §5). Reflection counts are unbounded as V or U tends to 0. The run observed 831.
- **Whole-room cases.** Hall–hall, hall–arm, same-arm and opposite-arm pairs lie in an open convex bar. Mouth points belong to the closed hall. A mouth point and a point in an adjacent arm lie in the closed rectangle formed by the hall and that arm, and the open chord lies in its interior. Hall corners are always boundary points. All of these were traced.
- **6-wall L.** The roles X=z, U=1, V=x, Y=y, W=x+2, H=2 are correct. The largest gap max(2x,4) is below 2A=2x+4. The window holds yz<Z<yz+A(1+y).

## 3. Exact tests

- **L(3,3,3).** Z=13 and the window is (9,29). The traced path is (−3,3) → (0,9/4) → (−5,1) → (3,−1), an exact match. The mouth crossing is (−1,0). The direct shot hits the notch wall. None of the 6 one-reflection images gives a legal shot, which agrees with d160.
- **P_7 control.** The window is (8,20), Z=10 and the image is (6,−8). The contacts are (24/7,−2) and (36/7,2), and the mouth crossings are (2,4/3) and (12/7,2). All match the note.
- **Exhaustive runs.** The rooms are L(3,3,3), a T with depths 4/1/5, P_7, and a plus with hall 3×4 and depths 1/6/3/2. They give 7,503, 4,465, 53,956 and 14,535 pairs, all lit by the note's shot.

## 4. R22 and DB55

- **R22-base (22 walls).** The line y=1/2 meets the room in (−1,1) and (3,5). The note's "4<x<5" is wrong: the second component is two cells wide. The line x=3/2 is also disconnected. The cell (0,1) is in the room and (1,0) is outside, as stated.
- **DB55 (12 walls).** The line y=1 meets (0,5) and (8,13). Every vertical section is connected, so the failure is horizontal only.
- **The condition.** The real membership condition is "hall plus full-side arms". "Every axis-parallel line meets the interior in at most one interval" is orthoconvexity. It is necessary, not sufficient. The S-tetromino and a 3-step staircase are orthoconvex with 8 walls, and neither is in the class. Excluding R22 and DB55 is valid. Wall count alone excludes R22, since 22 > 12.

## 5. Scope

The whole-room theorem covers 3 nontrivial shapes with 6, 8 and 12 walls. It reaches none of the 14–20-wall rooms that carry the W ≤ 20 question. Of the 8-wall shapes it covers only T. Odd crosses are BBBB rooms, but [cross-placement.md](../../../../qclass-closure/bbbb/cross-placement.md) already lights them. The theorem gives no new BBBB room. The reusable content is the local adjacent-arm chart inside larger rooms, and DB55 shows that chart doesn't reach parallel mouths. This review doesn't change the W ≤ 20 estimate.

## Gaps

1. **Medium: scope wording.** The class is exactly the rectangles, L's, T's and plus-signs, with at most 12 walls and 4 reflex vertices. The note should state this. "Structural theorem" overstates a result that covers 3 shapes, and the plus case was already known.
2. **Medium: imprecise condition.** "Where this stops" presents one-interval sections as the structural condition. That property is necessary, not sufficient. Define membership as hall plus full-side arms, and give orthoconvexity as a consequence.
3. **Low: R22 coordinate.** The second component at y=1/2 is 3<x<5, not 4<x<5.
4. **Low: DB55 wording.** "Failure is possible already in a normalized BBBB room" means the hypothesis fails, not illumination, and DB55 is lit. The sentence "Swapping axes preserves the requirement…" is unclear. Say instead that DB55 fails only in horizontal sections and the condition is rotation-invariant.
5. **Low: larger-room use.** "Applies pairwise in larger rooms" should list the exact requirements. The door is the whole side of a clear central rectangle. The arm's parallel walls run unbroken from the mouth to the mark depth, in whichever arm supplies the reflections.
6. **Low: unbounded words.** The construction is explicit, but its reflection count is unbounded as a mark approaches a mouth (831 observed). Any later use for word or length bounds must account for this.
