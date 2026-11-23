Advances: L1 — Every two distinct real interior points of the DB55 top-line stretch are lit at fixed corridor length 3, for every integer box height H≥4.

# The length-three DB55 stretch

The room is the interior of the two closed boxes [0,5]×[0,H], [8,13]×[0,H] joined by [5,8]×[2,3]. In particular this covers the entire normalized odd-height family in the brief, including both marks moving with H. We use the four-copy translation unfolding with all physical corners forbidden. A straight open chord in a clean cylinder projects to a legal billiard path. An interior mark has four sign choices for its lifts.

## Two explicit cylinder decompositions

Take horizontal travel per unit vertical travel t=10k, with 13 not dividing k. Use the upward section y=5/2 in the middle band. Its circle coordinate u modulo 26 is x for rightward physical velocity and −x for leftward velocity. The folding function sends u back to [0,13].

From the section to the upper seam y=3 the phase advances t/2. Over a box the trajectory then makes an excursion up to the roof and back. This costs vertical travel 2(H−3). In the doubled width-five coordinate its horizontal advance is a multiple of 10, so it returns to the same abscissa and horizontal sense. Above the corridor it reflects immediately at the roof of the corridor. There is the identical rule at the lower seam, with a box excursion of vertical travel 4. Thus the next *upward* section coordinate is u+2t mod 26. For u nonintegral all seam, roof and floor abscissas remain nonintegral at these tests, since t/2 is an integer. Every intervening vertical-wall reflection is smooth. Every regular trajectory off the integral section levels reaches the section: in a box, moving vertically toward or away from the central band takes it to that band after at most one roof or floor reflection. There is no other horizontal wall in its way before the band.

Since gcd(2t,26)=2, the return permutes the thirteen intervals (2j,2j+1) in one cycle and their thirteen complements (2j+1,2j+2) in another. Within each unit interval the itinerary, including any box excursions, is constant: changes require a corner and every corner has integral transverse coordinate. After thirteen returns position and velocity agree. Suspending each cycle gives an open clean Euclidean cylinder. Its two rims correspond to even and odd u. This argument needs only those two cylinders and their closures, irrespective of maximality.

In developed coordinates the transverse invariant is X−tY modulo 2. On the upward section u≡X−tY+5t/2 modulo 2. The additive constant is integral. At a lift of (x,y) the invariant is ±x±ty modulo 2, because reflection in an integer-coordinate line introduces only an even translation. Negating both signs exchanges the two open cylinders whenever a lift is off their rims. Every lift of a physical interior point is regular, hence is in at least one cylinder closure. A point with an interior lift therefore lights *any* other interior mark: select its lift in the appropriate cylinder, unroll the cylinder, and join to the other mark in its interior or on its rim. For two interior lifts at equal transverse depth the core arc suffices. Opposite-rim regular points also admit a chord whose entire open segment is in the cylinder.

Apply this first at t=10 and then at t=20. If a pair survives, each mark has both x−10y and x−20y integral, hence 10y and x integral. Apply the cylinder argument once more at t=100. Now 100y and 5t/2 are even integers, so x parity identifies the rim. Different x parities give opposite rims of the same cylinder and are lit. It remains to join marks with **integer abscissas of equal parity and ordinates in tenths**.

## Exact shots on the exceptional grid

Same-box marks and two marks in the middle band see each other directly. A point physically in the corridor or on its open mouth and a point in a box are covered at every length by the reviewed rectangular chamber-to-strip lemma. Thus take opposite-box marks. Write a for the left abscissa and b for the right one, with 1≤a≤4 and 9≤b≤12. Top-bank points have y≥3 and bottom-bank points have y≤2, including interior points on those seam levels.

Use horizontal speed t=100k for a positive integer k, vertical speed of magnitude one, and trace the source toward the middle band. A bank leg of depth in tenths preserves its abscissa and horizontal sense at the seam, since its horizontal travel is a multiple of 10. The same holds from the last seam to a bank target. All nonterminal vertical-wall contacts in a bank are smooth. Start the left mark rightward. A terminal phase +b or −b in the middle circle gives the desired target with the appropriate outgoing horizontal sense. The following congruences are modulo 26.

- **Opposite banks.** Cross the middle once. Solve a+t≡b. This is possible since gcd(100,26)=2.
- **Same bank.** Cross the middle twice. Choose ε∈{+1,−1} and solve a+2t≡εb, possible since gcd(200,26)=2. The intermediate phase z=a+t must avoid the four physical abscissas 0,5,8,13, or equivalently z mod 13 must avoid 0,±5. As 2z≡a+εb mod 13, the bad doubled residues are 0,±3. At least one sign works. Indeed b−a is even and lies from 5 through 11, so the negative-sign choice can fail only at b−a=10. Then (a,b) is (1,11) or (2,12), whose sums 12 and 14 are both good. At the intermediate seam either the ray reflects on the solid corridor side or it enters a box, reflects at its horizontal cap and returns at the same phase. In the box even the one-way cap travel is a multiple of 10 horizontally, so the cap contact is regular. The second middle crossing reaches the required bank.
- **Exactly one mark strictly between seam levels.** Reverse the path and reflect x about 13/2 as needed to place the bank mark on the left. From its seam to the terminal level the vertical travel is j/10 with 1≤j≤9. Solve a+10jk≡b. Here gcd(10j,26)=2 for every such j. The shot terminates inside the middle band before the next seam.

These cases include y=2 or 3 by giving the corresponding bank leg zero travel. There is no requirement on the parity of the two ordinates. The proof uses H only through the integer periods of the rectangular excursions. [Chamber-to-strip proof](resonant-gluing.md) · [Named family coordinates](stretch-stability.md)

## Exact checks

The independent d109 polygon-edge tracer replayed the following prescribed directions, chosen by the displayed congruences. No alternative direction was tried.

| H | S | T | (horizontal, vertical) speed | Smooth reflections before arrival |
|---|---|---|---|---:|
| 5 | (1,1) | (9,1) | (1100,1) | 1490 |
| 7 | (1,51/10) | (11,43/10) | (200,−1) | 167 |
| 15 | (2,121/10) | (12,133/10) | (200,−1) | 807 |
| 7 | (2,11/10) | (10,61/10) | (1100,1) | 964 |
| 7 | (3,41/10) | (9,26/10) | (600,−1) | 150 |

As a separate check of the cylinder step, exact polygon-edge reflections from the section phases j+1/4, 0≤j<26, gave the predicted first upward return in all 156 prescribed cases (H=5,7 and t=10,20,100). The proof above covers the intervening phases and every H.

**First neighboring case outside this argument.** At length 2 the middle span is 12. For t=10 the return adds 20 modulo 24, leaving four transverse classes. Reversal pairs them but does not put each off-rim mark in every cylinder. Whether another construction closes that entire height stretch is a separate question.

**Scope.** This removes a normalized BBBB family of unbounded area 10H+3, including its real marks. The fixed short corridor is essential to the modulus 26 used here. In a more general two-box layout the central return can split into more than two cycles, or an intermediate visit can hit a corner for both target signs. Neither case is decided by this proof. No global area bound or all-length ledger word closure follows.

**Smallest W≤20 room this result does not cover.** At the ledger level the W=10 open staircase band LLLRLLLRLR has realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2). This note concerns the W=12 DB55 word on the stated length slice.
