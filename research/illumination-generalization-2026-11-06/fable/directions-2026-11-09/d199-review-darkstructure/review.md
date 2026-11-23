# D199: review of the dark-structure proposal and its three-chamber snapshot

Date: 2026-11-23. Reviewer: independent referee.

Reviewed files: `proposal.md` and `snapshot.md` in this directory. Context:
`../PROGRAM.md` (top section), `../d154-review-r22arm/review.md` and its log,
`../d152-review-uniformtail/review.md` and its checks, RESULTS.md §11 (d152,
d153, d154) and §3.10 (Theorem FIN, d64).

Code: [checks.py](checks.py), log [checks.log](checks.log). It uses the
standard library only and runs in 0.5 CPU-seconds. It builds d152's named
three-chamber room for k = 6..300 and quotes R22's numbers from the d154 log.
It runs no ray, direction, word or room-size search, and no monodromy
enumeration.

## Verdict

**Correct with gaps.** The arithmetic and the covering-space steps are right,
and the snapshot honestly reports that the route's first implication fails. But
the proposed lemma's conclusion is unsatisfiable at W ≤ 20, so the lemma is a
restatement of the goal for this scope, and the snapshot names the wrong first
open case.

## Per-item verdicts

1. **The count r ≥ 3d ≥ 9: correct. "d154 established X for R22": correct
   with gaps.** The count is right, but d154 never states three zeros on N.
   They follow from d154's data by the proposal's saturation argument, which
   holds.
2. **N = 29 + 6k: correct.** Area, double area, pillowcase normalization and
   gcd(N, 6) = 1 all check for k = 6..300. An independent Riemann–Hurwitz count
   confirms the degree.
3. **d ≤ 8, so d ∈ {5, 7}: correct.** d154 §2's zero argument applies to any
   block system. The bounded quantity is the block size, which is the inner
   degree. The congruences k ≡ 1 (mod 5) and k ≡ 1 (mod 7) are right.
4. **Primitive for all k = 35j: correct, but understated.** Primitivity holds
   for every k with k ≢ 1 (mod 5) and k ≢ 1 (mod 7). That's 202 of the 295
   values of k from 6 to 300. The first primitive member is k = 7.
5. **Darkness gives no invariant relation: correct with gaps.** The analysis
   and the cyclic illustration are right. The first open case is misstated,
   and the snapshot doesn't say that the route's conclusion can never trigger
   at W ≤ 20.

## 1. The count and the R22 evidence

**The count is correct.** On the flat double Q of an orthogonal room, cone
angles are π at convex corners, 2π at regular points and 3π at reflex corners.
A point over a cone point of angle θ on N has angle e·θ, where e is the local
degree. Since 3π is the largest angle on Q, a 3π point on N has only
unramified preimages. So each of its d preimages is a distinct reflex corner.
Preimages of distinct points are disjoint, so three such points give
r ≥ 3d ≥ 9. The orthogonal-only scope is stated, and it's needed: 45° rooms
have other cone angles.

**d154 doesn't state X, but X follows from its numbers.** The d154 review
records only that the R22 staircase has inner degree 3 and that Σq = 2 + 2 + 0
= 4 = 2d − 2 over the three clean off-source classes. The three zeros need
one more step, which the proposal supplies:

- Each regular Q-point over a clean site lies over a pole with e = 2. It costs
  exactly one unit, not "at least one" as the proposal says. Four such points
  use the whole budget 2d − 2 = 4.
- A 3π point on Q lies over a zero with e = 1 or over a pole with e = 3. The
  second costs two units, and none are left.
- So all nine reflexes lie over zeros, three per zero. N has exactly three
  zeros. By Gauss–Bonnet it has seven poles.

`checks.log` confirms the arithmetic: n = 15, inner degree 3, outer degree 5,
saturated budget, 3 zeros and 7 poles. So X holds for R22 base. That's one
example. Nothing in the evidence suggests darkness forces X in general, as the
proposal's own objection 2 says.

**The conclusion is unsatisfiable at W ≤ 20.** Every orthogonal room with
W ≤ 20 has r ≤ 8 < 9. So "darkness implies X" at W ≤ 20 is equivalent to
"no orthogonal W ≤ 20 room has a dark interior lattice pair". The proposal
says the lemma "would exclude darkness at W ≤ 20". It doesn't say that the
lemma is the goal itself for this scope, so proving it is no easier than the
goal. This is the certificate-completeness gap that d154 gap 1 names.

## 2. The sheet count N = 29 + 6k

**Correct.** For every k from 6 to 300, `checks.py` builds the room and
confirms the following:

- Area 27 + X + Y = 29 + 6k, W = 20, r = 8, 12 convex corners, no pinch, and
  wall-length gcd 1 on both axes.
- The double has area 2(29 + 6k). The pillowcase, the double of the unit
  square, has area 2. So the degree is n = 29 + 6k.
- n ≡ 5 (mod 6) for every k, so gcd(n, 6) = 1.

**Independent check of the degree.** For Q → B, both spheres, the fiber sum
over the four sites is 2·reg + c + 3r = 4n. The ramification total is
reg + 2r = 2n − 2. Here reg = 2·(interior lattice points) + (smooth wall
lattice points). Both identities hold exactly for every k. d153's n = 83 at
X = Y = 28 (k = 9) matches 29 + 6·9.

**Notation.** The proposal uses N for the intermediate cover. The snapshot
uses N for the sheet count. The review writes n for the sheet count.

## 3. The block-size bound

**d154 §2 applies to an arbitrary block system.** A nontrivial block system
with blocks of size d and m = n/d blocks gives an intermediate cover
Q → N → B. Q → N has degree d, and N → B has degree m, with 1 < d < n.
Only the zero part of d154 §2 is used:

- N is a sphere, since it is covered by the sphere Q. By Gauss–Bonnet,
  #poles − Σ(m_i − 2) = 4, summed over zeros of angle m_iπ.
- A zero-free N is a four-pole pillowcase. Its lattice would contain Q's
  absolute periods 2ℤ², which forces N = B and contradicts d < n.
- So N has a zero. Its angle is 3π, because any larger angle would lift to
  more than 3π. All d lifts are distinct reflex corners, so d ≤ r = 8.

The cleanness hypothesis of d154 Lemma B isn't needed for this step. The step
inherits d154 gap 4: zero existence rests on the isogeny exclusion in
`exclusion-descent.md` and on normalization. The family is normalized, with
gcd 1 on both axes.

**Block size, not number of blocks, is bounded.** The bound d ≤ r comes from
lifts of a zero, which number d, the size of a block. Nothing bounds m: at
k = 6, d = 5 gives m = 13 blocks. The snapshot uses the right quantity. In
this family the confusion would be harmless. Because n is coprime to 6, any
divisor in 2..8 is 5 or 7, so "m ≤ 8" selects the same 101 values of k.
In general it wouldn't.

**Conclusion.** Within 1 < d ≤ 8 and d | n with gcd(n, 6) = 1, only d = 5 and
d = 7 remain. d = 5 needs k ≡ 1 (mod 5), and d = 7 needs k ≡ 1 (mod 7). Both
are admissible when k ≡ 1 (mod 35), for example k = 36. Either way at most
⌊8/d⌋ = 1 zero exists, so three zeros are impossible, as the snapshot says.
"The two remaining congruence classes" is loose: the classes overlap.

## 4. Primitivity

**Correct as stated, with no darkness hypothesis.** For k = 35j neither 5 nor
7 divides n, so no block size survives. A transitive group with no
nontrivial blocks is primitive.

**Understated.** The same argument gives primitivity for every k with
k ≢ 1 (mod 5) and k ≢ 1 (mod 7). That's density 24/35; `checks.log` finds
202 of 295 values for k = 6..300. The first primitive members are k = 7, 9,
10, 12, 13, 14, 17, 18, and each has prime n (71, 83, 89, 101, 107, 113, 131,
137). A transitive group of prime degree is primitive, with no input from
d154. The snapshot's "for instance" covers this, but the open case it names
follows the example rather than the smallest case.

## 5. Darkness and invariant relations

**The analysis is correct.** Darkness excludes straight, corner-avoiding
connections between marked lifts. A monodromy-invariant relation must survive
continuation of every sheet around every branch loop. Composing a branch loop
with a forbidden connection gives a bent path that darkness doesn't exclude.
The snapshot also notes correctly that the marks lie over sites, not over the
regular basepoint, so comparing them as sheets needs chosen germs and
transport.

**The cyclic illustration is correct.** ℤ/p acting on itself by translation
preserves the cycle graph with edges i ~ i ± 1. For p ≥ 5 that graph is
neither empty nor complete, yet the action is primitive. The bound p ≥ 5 is
needed: for p = 3 the cycle graph is complete. More generally, any primitive
group that isn't 2-transitive has connected, nontrivial invariant orbital
graphs. So an invariant "forbidden pair" relation alone can't yield blocks.

**Overstatements and omissions.**

- *First open case.* The snapshot says the first open case "is already the
  primitive subfamily k = 35j". For the route's first step, the smallest
  primitive member is k = 7 (X = Y = 22, n = 71). For L1, the first open case
  in the family is k = 6 (X = Y = 19, area 65), the smallest BBBB member. That
  case isn't primitive (d = 5 is admissible), but the three-zero conclusion is
  still impossible there. So k = 6 is not easier.
- *The follow-on never triggers.* The snapshot says "the conditional
  three-zero follow-on is not triggered". At W ≤ 20 it can never be satisfied.
  For every k, the route can only work as a proof by contradiction: darkness ⇒
  X ⇒ r ≥ 9 ⇒ contradiction. So the route has to show these rooms are lit.
- *What remains is the full statement.* "Prove that every two distinct interior
  lattice marks there admit a legal straight connection" is complete lighting
  of those rooms. It's not a reduced problem.

## Errors and fixes

1. **Medium (proposal).** It presents X as a structure darkness might force.
   At W ≤ 20 the conclusion r ≥ 9 is impossible, so the lemma is equivalent to
   the goal for orthogonal lattice marks. *Fix:* state it as "darkness ⇒ X,
   and X is impossible at W ≤ 20", and say the hard step is certificate
   completeness (d154 gap 1).
2. **Medium (snapshot).** The first open case is misstated. *Fix:* for L1, k = 6
   (X = Y = 19); for primitivity, k = 7 (n = 71, prime).
3. **Low (snapshot).** Primitivity is stated only for k = 35j. *Fix:* "primitive
   iff k ≢ 1 (mod 5) and k ≢ 1 (mod 7), density 24/35; prime n gives
   primitivity directly".
4. **Low (proposal).** "Each costs at least one unit" should be "exactly one".
   It also attributes the three zeros to d154. *Fix:* say d154 gives inner
   degree 3 and Σq = 4, and the zeros follow by saturation.
5. **Low (snapshot).** The bound d ≤ 8 uses only the zero part of d154 §2, and
   that part inherits d154 gap 4. *Fix:* cite the isogeny exclusion and the
   normalization explicitly.
6. **Low (both).** N means the intermediate cover in one file and the sheet
   count in the other. "Two congruence classes" overlap at k ≡ 1 (mod 35).
7. **Observation.** Theorem FIN (d64) already lights every same-class interior
   lattice pair when some canonical N_x has 1 < deg N_x < n at W ≤ 20. If
   darkness forced such a canonical factor, the three-zero clause wouldn't be
   needed for those pairs. A block system from an arbitrary relation need not
   be canonical, so this doesn't close anything. But the route's second step
   adds little beyond step 1.

## Which lemma does this advance, and what is the first case still open?

**L1, as a reformulation only.** The proposal recasts orthogonal L1 at
W ≤ 20 as "darkness forces a proper pillowcase factor with three zeros". The
snapshot proves a darkness-free fact: for 24/35 of the three-chamber family,
the monodromy is primitive, so no proper factor of any kind exists. Darkness
certificates there can't be of factor type. That's a useful negative constraint,
but it doesn't bound area or light any pair.

The first open case in the family is **k = 6, X = Y = 19, area 65**: the
smallest BBBB member, which is beyond orbit.c's 63-cell limit (d152 §3). The
smallest case where the route's first step is impossible outright is
**k = 7, X = Y = 22, n = 71**.

What's the smallest W ≤ 20 room this result doesn't cover? It covers none, so
the answer is the smallest open BBBB room in the program. In this family,
that's k = 6.

## Recommendation

**Don't continue this route as framed.** Its first step, darkness ⇒ a proper
factor, is exactly certificate completeness. The snapshot shows it's
impossible for most of the test family: for primitive members, the only
consequence is "these rooms are lit", which is the goal. Its second step can
never hold at W ≤ 20.

Keep two items. Record the primitivity criterion (k ≢ 1 mod 5 and mod 7) as a
fact about the family. Record the general corollary of d154 §2: in a
normalized orthogonal room, a proper factor has block size dividing n and at
most r. For W ≤ 20 rooms with n coprime to every integer in 2..8, no
factor-type certificate exists. Any L1 argument for those rooms must use a
mechanism other than covering factors, such as the chart-descent or
band-chain routes in PROGRAM.md. Close the d199 stopping rule now, instead of
on 2026-11-26.
