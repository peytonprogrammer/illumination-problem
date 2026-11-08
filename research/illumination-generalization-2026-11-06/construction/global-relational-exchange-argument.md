# B06: shared-corner incidence has exact exchange, but no positive charge

Author: Codex01a18403. Original aggregate allowance: 2026-11-07
16:21:00–16:35:00 UTC. This is one proposal and its prescribed-control challenge.
No new orbit, room or ray census, coefficient fitting or worker was used.
The universal canonical45 W<=21 illumination objective remains **unproved**.

## 1. Feature and its domain

Retain the entire connected square-tiled cover, permutations h,v of all N
square slots, all four actual source marks and all four actual target marks.
Composition is right-to-left. The genuine zeros are the nontrivial cycles of
C=v h v^-1 h^-1. In the orthogonal controls each such cycle has length three.
Every slot of each cycle is a forbidden true-zero incidence. Convex regular
corner labels remain present and transparent. No regular sheet is removed.

For a permutation p and orientation e=+1 or -1, follow p^e from each actual
mark until the first genuine zero, opposite-color mark or return to that same
starting mark. Other same-color marks may occur along the way. Keep the full
trace, endpoint order, terminal type and terminal slot. This convention records
regular periodic components explicitly, even when they contain several source
marks. It never replaces a regular return with a corner stop.

Let n(A,e,z) count color-A starts whose first stop is genuine-zero slot z.
Use the single unweighted relational feature

    F_p = sum_e sum_zero_cycles_Z sum_{z,z' in Z; z!=z'}
              n(S,e,z) n(T,e,z').

This records whether both colors approach the same zero through different
slots. Total return counts, total zero stops and stopping lengths do not retain
that relation. All incidence records are saved; F is their nonnegative integer
aggregate. No claim that F determines the entire ordered-mark geometry is made.

**Ordered-mark lemma.** The same-slot term n(S,e,z)n(T,e,z) is zero.
To prove it, use the permutation cycle containing z. Two starts first reaching z
without another zero lie in the same zero-free predecessor interval. If they
have opposite colors, the earlier start meets the later opposite-color start
before z, contrary to its claimed first stop. Distinct actual marks are
essential. A cycle with no zero makes no zero-incidence contribution.

All names can be retained in the raw N-slot state, with h,v permutations of
that same fixed set. This gives the conservative finite bound (N!)^2 with fixed
color labels. It is neither a degree bound nor an enumeration. It retains the
slot distinctions actually used here rather than applying the accepted
r!*(4!)^2 bound to extra sector data that that bound does not cover. F is also
invariant under common relabelling of the slots: zero cycles, traces and the
inequality z!=z' are transported together. No distinguished physical prong,
full transported reflection or other infinite-valued structure enters F.

## 2. Exact anchored transition identities

The anchored transformations are

    T(h,v)=(h,v h^-1),    U(h,v)=(h v^-1,v).

Direct multiplication gives

    C(Ts)=(v h^-1)h(h v^-1)h^-1=C(s),
    C(Us)=v(h v^-1)v^-1(v h^-1)=C(s).

Thus zero cycles and all fixed slot labels remain the same before common
relabelling. Put d=h v^-1, so d^-1=v h^-1. Write I(p,e) for the complete
trace/terminal record array just defined. Then, literally as permutation walks,

    I_h(Ts,e)=I_h(s,e),    I_v(Us,e)=I_v(s,e),
    I_v(Ts,e)=I_d(s,-e),   I_h(Us,e)=I_d(s,e).

The entire arrays agree, including regular returns and opposite-color stops.
Summing both orientations implies F_(p^-1)=F_p. Consequently

    F_v(Ts)=F_d(s)=F_h(Us),
    Delta_T F_v + Delta_U F_h = 2F_d-F_h-F_v.

These are algebraic identities on the full labelled cover. The symbol d names
a permutation in these identities; it does not assert that separately taking
a vertical step and then a horizontal step is one legal optical ray. No
mixed-direction reachability is used to prove illumination.

The finite raw state space permits telescoping a finite-valued potential.
It does not make every sheared marked surface a physical orthogonal room.
The accepted label-descent review explicitly rules out that inference. The
candidate below was proposed on the whole orbit of a physical representative;
it was not derived by applying a physical-room lemma to every sheared state.

## 3. Candidate fixed before checking

The recorded proposal was, for 1<=r<=9,

    H_pm(s) >= (9-r) F_h(s)/(16N)
               + Delta_T F_v(s) + Delta_U F_h(s).

Here H_pm counts source starts reaching an actual target in either horizontal
orientation before a true zero. Threshold r=9 was deliberately included for
calibration. The candidate also needs a separate proof of positive orbit sum
of F_h for every dark physical orbit with 1<=r<=8. No such positivity proof
has been obtained. The normalizing factor 16N supplies none.

## 4. Three fixed controls give a hand-checkable obstruction

Use only the existing 60-slot known22 certificate, raw SHA256
`2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346`.
Take A=saved state462, B=U^-1 A, and C0 obtained by applying T,U^-1,T
in that execution order to A. These were already prescribed B05 controls;
the B06 check generates no orbit. Each has r=9 and H_pm=0.

| Control | F_h | F_v | F_d | 2F_d-F_h-F_v |
|---|---:|---:|---:|---:|
| A | 0 | 10 | 10 | 10 |
| B | 10 | 10 | 0 | -20 |
| C0 | 10 | 0 | 10 | 10 |

At A the proposed inequality reads 0>=10, which is false. Its failure is not
caused by dropping periodic components: all four source starts return
regularly in both horizontal orientations. The positive horizontal source
cycles include 0->1->3->5->0 and 37->46->54->30->37. Target starts still
have zero-terminated horizontal traces. Thus F_h=0 is real absence of shared
source/target zero incidence in that direction.

For an independently reproducible small incidence check at A, its vertical
positive-orientation shared loads are:

| Zero cycle | Source terminal multiplicities | Target terminal multiplicities | Pairs |
|---|---|---|---:|
| (2,7,6) | 2:1, 6:1 | 7:1 | 2 |
| (22,51,29) | 51:1 | 22:1 | 1 |
| (33,45,35) | 33:1 | 45:2 | 2 |

Negative orientation contributes 2+1+2 again, giving F_v=10.
For d, positive shared loads are 2,1,2 at cycles (8,11,9),
(23,40,38), (26,43,27); negative shared loads are also 2,1,2
at those cycles. All arrays and ordered traces, including the other prescribed
controls and pinned lexicographic root, are saved in the check JSON.

**The constant-weight repair is also excluded.** Keep this SAME feature and
set Phi=lambda F_v, Psi=mu F_h for arbitrary real constants. Its divergence is

    D=lambda(F_d-F_v)+mu(F_d-F_h).

At the three r=9 controls, any inequality H_pm>=(9-r)a+D requires

    A: 10mu<=0,
    C0: 10lambda<=0,
    B: -10(lambda+mu)<=0.

Therefore mu<=0, lambda<=0 and lambda+mu>=0, forcing lambda=mu=0.
This symbolic necessary-condition argument uses no coefficient fitting.
Neither reversing the overall sign nor unequal nonzero constant crossed
weights repairs the threshold-calibrated formula.

## 5. Prescribed square: a separate lack of force

For the previously prescribed square [0,24]^2, retain torus period48 and
actual fibers S={12,36}x{12,36}, T={16,32}x{18,30}.
There are no genuine zeros, so F_p=0 for every direction. Its orbit weight
is identically zero. This r=0 control is outside the candidate domain; it
demonstrates that a corner-incidence weight alone cannot cover the cornerless
case. It is not a counterexample to illumination or to the stated candidate.

The three prescribed horizontal, vertical and (1,-1) directions have only
regular returns before any opposite-color hit. Nevertheless the original
points (12,12),(16,18) connect directly inside the square, in primitive direction
(2,3). No new direction search was needed for this direct segment.

## 6. Result, limits and exact remaining implication

**No positive inequality was obtained. Retire this threshold-calibrated
shared-zero aggregate with constant crossed potentials.** The exact feature,
ordered-mark lemma, transition identities and three-control obstruction are
the reviewable results of this bounded effort.

The r=9 obstruction does not disprove a formula restricted to r<=8,
coefficients that vanish at r=9, identity-dependent tensor potentials, or all
relational exchange methods. The square only requires a separate r=0
argument. No low-wall dark counterexample, new wall bound or novelty claim
has been established.

The missing positive implication remains: for a full physical unfolding with
distinct actual endpoint fibers and persistent all-direction separation,
prove r>=9 (and separately handle canonical45 nonorthogonal corners), or
construct an actual connecting path. Neither the algebraic exchange nor
finiteness of label bookkeeping supplies that implication.

Dependencies are the six independently accepted scoped label-descent claims,
the frozen known22 source/control arrays, and the established interpretation
of their anchored permutations. B06 reruns only nine prescribed raw states,
not the complete darkness certificate. Full known22 darkness is inherited
from its prior certificate acceptance; the local contradiction above needs
only the displayed H_pm=0 values. Final independent B06 review is pending.
