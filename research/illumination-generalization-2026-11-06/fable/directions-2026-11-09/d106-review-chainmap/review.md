# D106: review of qclass-closure/bbbb/chain-map.md

Date: 2026-11-20. Reviewer: independent referee. Scope: the sections "Own-double
parity" and "Following on: a simultaneous growth test". The partition lemma and
the density section weren't reviewed. Named rooms only, exact integer and
rational arithmetic, about 4 CPU-seconds in total. No room, ray, direction or
reflection-word search.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Sublattice kill | Sound. The parity part is equivalent to the definition of BBBB and doesn't need n > 2r + 2. The coset extension is correct but excludes nothing that folding could use. |
| 2. Twist-overlap criterion | Sound as a sufficient test. The "iff" is about the existence of a common power, not about lighting. |
| 3. Scope | Neither claim removes a room or a pair from the open core. |

## Claim 1: sublattice kill

### The count

Each cell has four corners. A lattice point with k cells around it carries k
cell-corner incidences: convex 1, smooth 2, reflex 3, interior 4. Strict
simplicity rules out pinches, so k = 2 always means a smooth wall point. The
singular incidences therefore total (r + 4)·1 + r·3 = 4r + 4. "Regular" means
smooth or interior. That matches the note's R, and a smooth wall point is a cone
point of angle 2π on the double. If every cell had at most two regular corners,
the singular incidences would be at least 2n, so n ≤ 2r + 2. The contrapositive
is the note's claim. Any three corners of a unit square give difference vectors
(1,0) and (0,1) up to sign, so they generate Z². Correct.

Quantitative form: a coset of a proper subgroup holds at most two corners of a
unit square, since three would generate Z². So at least 2n incidences lie
outside the coset, at most 4r + 4 of them singular. An interior point has two Q
lifts and four incidences; a smooth point has one lift and two incidences. Each
regular Q lift therefore accounts for two incidences, which gives at least
n − 2r − 2 lifts outside. Correct. For r ≤ 8, 2r + 2 ≤ 18 < 21. Correct.

`count.py` checks this exactly on all 1,027 named rooms in
`d8-perturbation-test/rooms.json`. All are strictly simple with Euler
characteristic 1.

- Singular incidences equal 4r + 4 in every room, and the d68 identity holds in
  every class.
- 43 rooms satisfy n > 2r + 2, all BBBB. Every one has a cell with at least three
  regular corners and ⟨R − R⟩ = Z². For each proper subgroup of index ≤ 6, the
  number of regular Q lifts outside the best coset is at least n − 2r − 2. There
  are no violations.

### R22 and R34-base

| Room | n | r | 2r + 2 | n > 2r + 2 | q by class (00, 01, 10, 11) | max regular corners per cell | index of ⟨R − R⟩ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R22-base | 15 | 9 | 20 | no | 6, 2, 2, 0 | 2 | 1 |
| R34-base | 19 | 15 | 32 | no | 6, 0, 0, 0 | 1 | 4 |

R34-base fails the hypothesis, as the brief predicts. Its regular sites
(2,0), (4,0), (6,0), (8,−2) lie in (0,0) + 2Z², which is index 4. That agrees
with d105. R22 also fails the hypothesis, yet ⟨R − R⟩ = Z² there. The
hypothesis is sufficient, not necessary. Among the named rooms, 678 BBBB rooms
have n ≤ 2r + 2, and all of them still have ⟨R − R⟩ = Z².

### Does this exclude the parity mechanism?

Yes, but for a simpler reason than the coset argument. By d68 Lemma B, a class
has type Q exactly when it has no regular site. So BBBB means q_x > 0 in every
class, and the R34 mechanism needs three classes with q_x = 0. The exclusion is
the definition restated, at every area, with no use of n > 2r + 2. d105 already
recorded that R34 isn't BBBB.

The coset extension excludes more than folding can use. Reflections in integer
lines preserve x mod 2 and y mod 2, but not residues modulo an odd-index
sublattice. A folding-invariant residue argument must therefore use a subgroup
containing 2Z². Such subgroups are unions of parity classes, and BBBB excludes
them all. "Confinement to an odd-index sublattice" was never a darkness
mechanism, so excluding it doesn't remove a live alternative.

Trajectory-level check, which the note flags correctly: an unfolded segment
from S with primitive step w meets the lattice points S + kw. Their folded
classes alternate between class(S) and class(S) + w mod 2. Parity therefore
blocks a given trajectory only if the step class has no regular site at all,
which BBBB excludes. Whether the specific folded points S + kw are regular
depends on position, not on residues. Global generation of Z² says nothing
about that. Any dark pair in the core must be dark for positional reasons, not
for residue reasons.

## Claim 2: twist-overlap criterion

**The "iff".** Let A′ ⊂ Z/u be the times when F^i(s) ∈ I, and B′ ⊂ Z/v the times
when F^j(t) ∈ J. A common power k exists exactly when some i ∈ A′ and j ∈ B′
satisfy k ≡ i mod u and k ≡ j mod v. By the generalized Chinese remainder
theorem, that happens exactly when i ≡ j mod g. So it's equivalent to
(A′ mod g) ∩ (B′ mod g) ≠ ∅. Correct. `twist.py` compares the residue test with
a brute-force search over k < lcm(u, v) on 40,000 random rational rotations
with u, v ≤ 18. There are 0 mismatches.

**Legality of the pullback.** F^k(s) ∈ I and F^k(t) ∈ J, so a legal segment σ
joins them. F is an affine automorphism of Q. It maps cone points to cone
points of the same angle and fixes them, because cylinder boundaries are fixed
pointwise. So F^(−k)(σ) is a straight segment that misses every corner. Its
endpoints are F^(−k)F^k(s) = s and F^(−k)F^k(t) = t, the original lifts. F never
needs to preserve the set of marks. Straight segments on the double fold to
billiard paths, and passing through a smooth wall point is a reflection, which
is allowed. Correct.

Two small points, neither a gap:

- The example arcs "in one open cylinder of a different direction" work because
  the universal cover of an open cylinder is an open strip, which is convex. The
  two images are distinct because s ≠ t.
- If s lies on a saddle connection of F's direction, F fixes it (u = 1). The
  note excludes this by hypothesis, and the test still works in that case.

**Growth consequence.** On a leaf F rotates by C_s·p/u with gcd(p, u) = 1. The
images with i ≡ i₀ mod g step by g·p/u = p/(u/g), so they are u/g equally
spaced points with spacing C_s·g/u. An open arc longer than that spacing meets
every residue. Correct. Results of `twist.py`:

- Both arcs beat their spacing in 19,325 instances, and every one has a witness.
- One arc beats its spacing and the other meets its orbit at least once: no
  failures.
- At equality an open arc can miss a residue: with u = 6, g = 2 and the arc
  (0, 1/3) from phase 0, A = {1} and residue 0 is missed.

**Large periods don't force overlap.** Correct. With u = v, the orbits move in
lockstep and g = u, so each residue holds one position per endpoint. In
`twist.py`, with u = v = 10, 100 and 1000 and the phases offset by 1/2, the arcs
(0, 1/4) give disjoint A and B, and brute force finds no common power. This is
exactly the case where s and t lie on the same leaf. The relevant quantity is
u/g and v/g, not u and v.

## Claim 3: scope

The open core (RESULTS §11) is the lattice pairs in BBBB rooms with r ≤ 8 and
area ≥ 21. Its open lemma is that some off-class candidate is reached by a real
path.

- **(1) removes no room and no pair.** It rules out one proof route: darkness
  from a global residue. Within BBBB, the part that matters for folding (parity)
  is the definition of BBBB. The odd-index part never applied to billiards. What
  it adds: any dark pair in the core must be dark for positional reasons, along
  specific trajectories.
- **(2) removes a pair only when an explicit witness is given.** That means a
  multitwist F, a lift combination, and mutually visible arcs I, J with
  overlapping residues. The note exhibits no such witness, runs no computation,
  and proves no lower bound on overlap. So (2) removes nothing from the core yet.
  It gives a certificate format and a clean dark-pair necessary condition: A and
  B are disjoint for every (F, I, J) and all four lift combinations.
- **What remains:** the whole open core. A proof would need, for each such pair,
  a direction and arcs where u/g or v/g beats the arc spacing, or some other
  forced phase overlap. The note correctly says it has none.

## Re-run

```
cd d106-review-chainmap
python3 -B count.py R22-base R34-base > count.log
python3 -B twist.py > twist.log
```
