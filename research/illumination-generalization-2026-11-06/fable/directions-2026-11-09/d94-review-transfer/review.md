# D94: review of canonical-transfer.md and fiber-transport.md (snapshots)

Date: 2026-11-20. Reviewer: independent referee. Reviewed files:
`canonical-transfer.snapshot.md` (SHA-256 prefix `eeaa092a`) and
`fiber-transport.snapshot.md` (`4bf81bf8`). Both prefixes match the live
originals in `qclass-closure/bbbb/` and were rechecked after the review.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. canonical-transfer: a geometric fold need not give a proper canonical factor; the odd cross is a BBBB room with a degree-4 geometric quotient whose two regular fibers hold both mirror pairs | Sound. Every number reproduced exactly at b = 7, 9, 11. |
| 1b. canonical-transfer: equivalence (1)⇔(2)⇔(3), crossing bound, primitive-case kernel argument | Sound. |
| 2a. fiber-transport, degree 3 | Sound, as a necessary condition. |
| 2b. fiber-transport, degree 4 cube case | Sound, under its stated hypotheses. |
| 2c. At most two zeros for r ≤ 8 | Sound. |
| 3. "BL remains open; the decisive gap is primitive BBBB rooms" | First half accurate. Second half inaccurate (see below). |

## Claim 1: the odd cross ([cross.py](cross.py), [cross.log](cross.log))

My own code builds the cross [−b,b]×[−2,2] ∪ [−2,2]×[−b,b] on unit cells, with
the same corner monodromies g_(p,q) = σ_x,p σ_y,q as d93.

- n = 16b − 16 (96, 128, 160). There are 8 poles and r = 4 zeros.
- All four B_x have one block at b = 7, 9, 11. The room is BBBB.
- The deck group (centralizer of G) has order 4. It is exactly the positive
  lifts of x→−x, y→−y and the half-turn. Each acts freely on cells. No sheet
  bijection intertwines g_x with g_(x+t) for t ≠ 0, so no kernel element moves
  the poles. This agrees with |K| = 4.
- Π = K-orbits is a proper G-block system of block size 4. N = Q/K has degree
  n/4, z = 1 zero and z + 4 = 5 poles.
- Crossing 2-cycles per parity equal 4u_x exactly. At b = 7 they are
  40, 44, 44, 48, against the note's bound (n − 4r − 4k)/2 = 32. So condition
  (2) fails at every parity, as claimed.
- The lifts of S = (6,0) are the 2-cycles {(5,−1),(6,0)} and {(5,0),(6,−1)}.
  Their K-orbit has 4 two-cycles, mapping to a single block 2-cycle, that is,
  one regular point of N with a full unramified fiber. The same holds for
  T = (0,6), at a different block pair. Both lie over class (0,0).
- G is imprimitive, with three size-2 systems from the K involutions.
- The seed pair is lit. [rays.py](rays.py) finds 3,166 lighting directions
  with |p|,|q| ≤ 80 at b = 7, and 3,088 at b = 9.

Side observation: oddness of b matters. In a run at b = 30 (even), the four
B_x have 4, 2, 2, 2 blocks, so that cross is not BBBB.

The section-1 algebra checks. A crossing 2-cycle (a,b) with a ∈ β₁ and
b ∈ β₂ forces g(β₁) = β₂ and g(β₂) = β₁. That is a regular point of N.
Conversely, every upstairs cycle through a swapped block has even length, so
its length is 2. The count m = p_x + 3z_x + 2u_x, with p_x ≤ z + 4, z_x ≤ z
and kz ≤ r, gives the bound. The primitive-case argument is also sound. A
nonidentity centralizing involution gives size-2 blocks. A transitive
centralizer forces regular prime-cyclic monodromy, which needs p-cycles with
p ≤ 3. One wording point: in a primitive room with n > 2, no axial or
half-turn symmetry exists at all. The "no mark on an axis" bullet is a
consequence of that stronger fact.

## Claim 2: transport through a quotient

Lifting and corner avoidance check out:

- Branch values of f: Q→N lie among the poles of N. At a regular point or a
  zero of N, upstairs degrees 2e or 3e ≤ 3 force e = 1. Over non-poles of B
  nothing branches.
- Singularities of Q map to singularities of N. A pole of Q has degree 1, so
  it maps to a pole of N. A zero of Q has degree 3 = d·e, so it maps to a zero
  (d = 3) or a pole (d = 1).
- So a segment in N that avoids N's cone points lifts to k segments that avoid
  Q's cone points. Each lift is a billiard path in the room. Its endpoints are
  lifts of S and T, which are interior points of the double, not seam points.
- A geodesic from an interior point can't run along a seam (wall) without
  first meeting a corner, so grazing paths cause no gap.
- The converse fails, as the note says. Example: over class (0,0), N = Q/K for
  the cross has a pole whose preimages are regular points of Q, at the cross
  center. A legal upstairs path through the center projects through a pole of
  N.

Degree 3: Lγ(I) and J are 2-subsets of a set of size at most 3, so they meet.
Darkness therefore forces darkness of u, v in N's own flat metric. It does not
force billiard darkness in a polygon unless N is a double. In that case u and v
are seam points, outside d15's hypotheses, as the note says.

R22 consistency check: the staircase images are u = (0,0) (bottom wall) and
v = (2,2) (right wall) of the 5-cell staircase. They are dark in all 15,728
primitive directions with |p|,|q| ≤ 80, and so is the R22 seed. A rectangle
control lights in 3,900 directions. This is evidence only, not a proof.

Degree 4: Lγ(I) = B∖J follows. For a cube orbital on A ∪ B, each Lγ avoids
cube edges, so Lγ = M, the nonneighbor matching. Pulling an offending edge
back to the seed by an affine map preserves legality. Test 1 holds: the loop
γ·γ₀⁻¹ is homotopic, in N minus the branch values, to a small loop around one
branch value. Test 2 holds: open cylinders contain no branch values.

The task's phrase "sheet pairing" means a bijection of fiber points A→B, not
of sheets. The results only cover k = 3 and k = 4 with both mirror pairs in
fibers. They give no sufficient condition for light.

Zero count: a zero of N has d = 3, so e = 1. Its k preimages are k distinct
reflex zeros of Q, so z ≤ ⌊r/k⌋ ≤ ⌊8/3⌋ = 2.

## Claim 3: the summary

"BL remains open" is accurate. "The decisive gap is primitive BBBB rooms" is
not, for three reasons:

1. **BL is not a bridge in the remaining cases.** BL holds trivially when some
   class is proper. Q-class closure covers every W ≤ 20 room with a discrete
   class. So at r ≤ 8, BL is equivalent to this statement: every BBBB room
   lights all same-class interior lattice pairs. That is OL's BBBB core itself.
2. **Imprimitive BBBB is equally open.** The cross shows that a proper
   geometric fold with mirror fibers can coexist with BBBB. fiber-transport
   gives only necessary conditions, and only for k = 3 or 4 with both mirror
   pairs inside fibers. Nothing covers k ≥ 5, fibers that split a mirror pair,
   or the d93 step from affine point blocks to sheet blocks.
3. **A finite slice is unrun.** BBBB rooms with area 21–36 were never
   enumerated (STATE.md).

## What remains for BL

At r ≤ 8 the four-class trichotomy is complete. A class is discrete (Q-class
closure), universal, or proper (d64). So BL reduces exactly to this: no BBBB
room with r ≤ 8 has a dark same-class interior lattice pair. It splits into
three parts:

- BBBB rooms with area 21–36, which are finite and closable by an approved
  enumeration.
- Primitive BBBB rooms with area > 36. Here every sheet relation propagates to
  the universal partition, and no fold or deck symmetry exists.
- Imprimitive BBBB rooms with area > 36. Here darkness must be shown
  incompatible with every proper block system. The k = 3 and k = 4
  obstructions are only partial tools for this.

Even with BL, different-class pairs (G1) and non-lattice marks (G2) remain.

Rerun: `python3 -B cross.py 7 9 11; python3 -B rays.py 30; python3 -B rays.py 80`.
Each run takes under 3 CPU-seconds, uses exact integer permutations, and
covers named rooms only.
