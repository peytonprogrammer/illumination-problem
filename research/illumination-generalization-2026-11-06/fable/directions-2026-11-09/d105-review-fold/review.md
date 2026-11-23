# D105: review of qclass-closure/bbbb/fold-converse.md

Date: 2026-11-20. Reviewer: independent referee. Named rooms only, exact
integer arithmetic, about 2 CPU-seconds in total.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Step 2: the R22-type parity fold forces r ≥ 9 | Sound, with one fixable gap: the hypothesis must say the marked images are *separated*. |
| 2. Step 1: R34-base is dark by parity on Q, and deg Q→B = 19 is prime | Sound. The star count is reproduced exactly. |
| 3. Scope | Step 2 is vacuous on BBBB rooms at every r. It rules out nothing in the open core. |

## Claim 1: Step 2

### Riemann–Hurwitz and the bounds

Local degrees of Q→B are 1, 2, 3, and local degrees multiply through
Q→N→B, so N→B also has local degrees in {1, 2, 3}. N is a sphere. With p₁
poles, q regular points and z zeros, Σ(e−1) = q + 2z = 2m − 2 and
p₁ + 2q + 3z = 4m, so p₁ = z + 4. All q regular points lie over a, each
uses two sheets, so q ≤ m/2. Two distinct regular marked images give q ≥ 2.
Then z + 2 ≤ m ≤ 4(z+1)/3. Correct.

### r = kz + c₃ and the residual table

Over a zero of N, an upstairs local degree e gives 3e ≤ 3, so e = 1: k
reflex preimages. Over a regular point of N, 2e ≤ 3 forces e = 1. So all
ramification of Q→N lies over poles (Fact L), with c₂ + 2c₃ = 2k − 2, and
r = kz + c₃. Correct.

`step2.py` enumerates z ≤ 8, m < 40, 2 ≤ k ≤ 8 and all admissible c₃. The
residue at r ≤ 8 is exactly (z, m, k) = (2,4,2), (2,4,3), (2,4,4), (3,5,2),
(4,6,2), with q = 2 in every row. The table is complete. R22 is
(3, 5, 3) with c₃ = 0, c₂ = 4, r = 9, so the bound is sharp.

### Tetromino elimination

Every 4-cell placement with two reflexes (48 placements, T and skew only)
has exactly two regular sites, and their parities differ. T: (1,0), (2,0).
Skew: (1,0), (2,2). So the z = 2 row has no polygon base with q = 2 over one
class. Correct.

### The gap: separation

The main hypothesis says "two distinct regular marked images". The k = 2
step then claims "both mirror lifts of each mark collapse to one quotient
point". That doesn't follow. With q = 2 points p₁, p₂, the assignment
s→p₁, ιs→p₂, t→p₁, ιt→p₂ has two distinct images and no collapse. The step
needs **separation**: {f(s), f(ιs)} ∩ {f(t), f(ιt)} = ∅.

Separation is forced by the mechanism itself, so the gap is fixable. A
path in N from a regular a-point to a pole over x, smooth upstairs, returns
to its start. So Par(x) for a lift pair needs distinct images, and darkness
by this factor needs all four lift pairs separated. Add separation to the
Step 2 hypothesis, as the census-free paragraph already does. The
"physical position" wording is then unnecessary: q = 2 and separation give
the collapse directly, and the deck involution δ swaps s↔ιs and t↔ιt.

### Inner-degree-two axis argument

With collapse at both marks, δ exchanges halves at S and at T. By d91 and
d99 (2c, sound), δ lies over the identity of B, commutes with ι, and is an
axial reflection of the room fixing both marks. The open interior of a
simply connected room symmetric in a line meets that line in one interval.
So segment ST is interior and directly visible. Correct, given d91.

### Census route

km ≤ 16 ≤ 20 in every row, and d9 covers all strictly simple rooms of area
≤ 20 with W ≤ 22. Correct. It rests on d9, which has computer verification
but no line-by-line review.

### Census-free route

- **Refinement.** If N has no regular point over x, every upstairs
  2-cycle (i j) of g_x has i, j in one block: the block orbit has length 1
  or 2, and length 2 would be a regular point. So Π merges every
  off-class transposition, and the finest such system Π' = B_b ∨ B_c ∨ B_d
  refines Π. Block orbits of g_x on Π' have length 1 or 3, so N' has no
  regular off-class point. Multiplicativity 2 = e(Q→N')·e(N'→N)·2 keeps
  the marks regular, and separation descends. m' ≥ m > 1. W-invariance
  of each B_x (R3.3) passes to the join. Correct.
- **Discrete case.** Each cardinal neighbor of S has the two S-cells on
  its side, so it has 2 or more cells and must be reflex. The only
  coincidence between S- and T-neighbors is axial distance 2. Then the
  midpoint has four cells, which contradicts corner-only. So the case is
  vacuous, not "directly visible". The note's sentence is true but misleading.
  The ninth reflex is a diagonal neighbor in class d, distinct from the
  eight b/c reflexes. Correct.
- **Proper case, k' = 2.** Separation with q' = 2 gives collapse, and the
  axis argument applies. Correct.
- **Outer degree four.** g_a has type (2,2). The two zeros sit in two
  off-classes, each as a (3,1). All four corner permutations are even, so
  the four edge involutions share one sign. Even involutions generate a
  subgroup of V₄, which has no 3-cycle. So all four are transpositions, and
  V, H are disjoint at a. At the mark over (12), the east cells share one
  label i ∈ {1,2} and the west cells the other. If g_b is a 3-cycle, it
  contains exactly one of 1, 2, and the vertex E or W on that side carries
  two cells with one label. The upstairs cycle containing them maps onto a
  3-cycle, so it is a reflex 3-cycle with three distinct labels. That's a
  contradiction. The other mark forces g_c = identity, but only one
  off-class is the identity. Correct. `step2.py` confirms the counts: 72
  S₄ tuples meet the type constraints, and none has the identity at both
  adjacent classes.

## Claim 2: Step 1

`step1.py` on `R34-base`: 19 cells, edge-connected, Euler characteristic
1, no pinch. 19 convex, 15 reflex, W = 34. Interior points (2,0), (6,0).
Smooth points (4,0), (8,−2). All four regular sites are even-even.

Parity darkness: reflections in integer lines preserve coordinate
parity. The unfolded displacement D is even-even and nonzero, so
g = gcd(D) ≥ 2. The first lattice point S + D/g lies strictly before the
target and is not even-even. Its folded image is a room lattice point
outside the only transparent class, hence a corner. The script also checks
the arithmetic step for every |u|, |v| ≤ 40. Correct.

Degree: n = 19 is prime, so G has no proper block system; d93 and the
closure in `step1.py` agree. For m = 1, N = B, and both marks map to the
a-pole of B. Proper-fold necessity fails. R34 is corner-only in classes b,
c, d, so it isn't a BBBB example. Correct as stated.

## Claim 3: scope

In a BBBB room every B_x is one block. A factor with no regular point over
an off-class x must be coarser than B_x, so it has m = 1. The R22-type
hypothesis, and even the one-class reading, therefore never holds in a
BBBB room at any r. Equivalently, Par(x) holds over some factor only when
B_x separates the lift pair, and a one-block B_x never does.

What Step 2 rules out: at r ≤ 8, no dark same-class interior pair is
certified by Par at all three targets over a single factor, with separated
regular marked images. Such rooms have all three off-classes of type Q or
proper. Q-class closure (d102) and d64 already close them computationally,
so Step 2 is a census-free reproof of part of a closed case. It says
nothing about the open core.

## Re-run

```
cd d105-review-fold
python3 -B step1.py > step1.log
python3 -B step2.py > step2.log
```
