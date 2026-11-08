# B06 independent challenge

Decision: **ACCEPT the scoped negative result and bookkeeping lemmas. REJECT the proposed threshold-calibrated inequality.** No correction to the frozen final argument is required. Its restriction of the obstruction to formulas including r=9 is essential. The universal W<=21 theorem remains open.

Reviewer: Codex01a1a00f. This completes the bounded B06 assignment, with no native goal or budget mutation. The earlier budget waiver remains in effect. B05 dependencies are used at the scope stated below; this is not a retrospective acceptance of every B05 claim.

## Evidence and independent method

Read the seven pinned B06 files and seven pinned dependencies in full, including the source of the author checker. All 14 SHA256 pins match before and after verification. The decompressed known22 certificate also matches `2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346`.

The reviewer checker is `global-relational-exchange-independent-replay.py`; its complete output is `global-relational-exchange-independent-replay.json`. It imports no author code and does not execute the author checker. Its own walks use cyclic-list slicing: decompose a directional permutation into cycles, reverse the cyclic order for negative orientation, and cut each marked start's rotated cycle at its first stopping event. This independently reproduces 576 full saved records and 194 incidence rows across all nine supplied states. Every slot in every trace, start, orientation, terminal type and terminal slot agrees. The checker also independently reconstructs the prescribed words from raw saved state462, checks both orientations of the full T/U identities, and checks common relabelling of entire records.

The certificate is a binary array of existing 180-byte records (three 60-slot arrays), not JSON. The checker reads those records and selects lexicographic index462 and the pinned lexicographic root; it does not traverse or extend an orbit. All eight prescribed neighboring arrays agree with direct anchored word evaluation and the earlier pinned periodic-check arrays. The raw initial state agrees with the pinned label-descent audit. This establishes input provenance without treating an array-printing command as verification.

## Claim-by-claim decisions

### 1. Shared-zero definition and finite retained data — ACCEPT

For fixed full slot permutations h,v and fixed colors L, each nontrivial cycle of C=vhv^-1h^-1 identifies a genuine zero. For these controls there are exactly nine cycles of length3, hence27 zero slots. There are four source and four target starts, all regular C-fixed points. All60 slots remain in the connected cover. Thirteen color3 regular corner slots are retained and transparent; the checker distinguishes them from the27 true-zero slots rather than treating all40 color3 slots as absorbing.

The stopping convention is deterministic: first true zero, opposite-color mark, or return to the same actual starting mark. Passing another same-color mark is allowed. On a finite permutation cycle a stop always exists, since otherwise the start returns. Periodic records therefore retain every actual marked start, including multiple starts on one regular component. In A, all eight signed source-horizontal records return after four steps. They are not converted into fictitious zero hits.

For each orientation, the tensor indexed by source start, target start and their two terminal zero slots is well-defined. F sums its entries when both terminal slots lie in the same C-cycle but differ. A slot and orientation distinguish the incidences used by this definition. These are combinatorial incidence coordinates, not separately transported distinguished physical prong labels. The definition does not recover unrecorded physical sector data, a Euclidean reflection, or the entire geometry from F.

A common relabelling conjugates h,v,C and transports colors, starts, terminal slots and traces together; consequently it preserves F. Alternatively retaining the fixed N slot names bounds raw states by (N!)^2 for fixed L, including all incidences used here. N is fixed along this orbit but is not bounded uniformly across rooms. This finiteness supplies neither a degree bound nor a positive orbit weight. No inappropriate use of the smaller r!*(4!)^2 bound for extra sector data occurs.

### 2. Ordered-mark lemma — ACCEPT

Fix an orientation and a zero slot z on a p-cycle. Any start whose first stop is z lies after the previous zero in that cycle, within the same zero-free predecessor interval. Order two distinct opposite-color starts in that interval by distance to z. The one farther from z passes the nearer opposite-color start before reaching z. Its first stop therefore cannot be z. This proves n(S,e,z)n(T,e,z)=0. It applies without a darkness hypothesis, permits intervening same-color marks, and applies equally to negative orientation. Zero-free cycles contribute no zero incidences. Endpoint starts must be distinct and regular; the packet states and verifies these requirements.

### 3. Full-record anchored exchange, both signs — ACCEPT

Using right-to-left composition, put d=hv^-1. The raw moves give

- T: h'=h, v'=vh^-1=d^-1;
- U: h'=hv^-1=d, v'=v.

For T, the commutator is (vh^-1)h(hv^-1)h^-1=vhv^-1h^-1. For U, it is v(hv^-1)v^-1(vh^-1)=vhv^-1h^-1. Thus all zero-cycle sets, slot colors and stopping predicates remain exactly unchanged before canonical relabelling.

For every start and e in {+1,-1}, (v')^e=d^-e at T and (h')^e=d^e at U. Equality at every iterate proves equality of the entire trace and its first stopping event, not just equality of terminal totals. Therefore I_v(Ts,e)=I_d(s,-e), I_h(Us,e)=I_d(s,e), I_h(Ts,e)=I_h(s,e), and I_v(Us,e)=I_v(s,e). Swapping the orientation index proves F_(p^-1)=F_p and the scalar divergence 2F_d-F_h-F_v. Own replay verifies these identities record-by-record in all prescribed states.

The symbol d is a permutation word in this proof. These identities do not prove that a horizontal step followed by a vertical step is one optical trajectory. No such mixed-direction reachability inference is used.

### 4. Prescribed raw A/B/C0 arithmetic — ACCEPT

A is the exact saved state462. B applies Ui to A; C0 applies T,Ui,T in execution order, with no intermediate renaming. Own direct evaluation reproduces their supplied full h,v,L arrays. All three have N=60, r=9, H_pm=0.

| Control | F_h | F_v | F_d | D=2F_d-F_h-F_v |
|---|---:|---:|---:|---:|
| A | 0 | 10 | 10 | 10 |
| B | 10 | 10 | 0 | -20 |
| C0 | 10 | 0 | 10 | 10 |

At A in positive vertical orientation, the three shared C-cycles have loads:

- (2,7,6): source slots2,6 once each; target slot7 once;2 pairs.
- (22,51,29): source slot51 once; target slot22 once;1 pair.
- (33,45,35): source slot33 once; target slot45 twice;2 pairs.

Negative vertical orientation gives2+1+2 again, with individually different terminal slots preserved in the replay. For d, each sign also gives2+1+2, at cycles (8,11,9), (23,40,38), (26,43,27). Thus each sum is10. A's horizontal source components include (0,1,3,5) and (37,46,54,30), each containing two source starts; the four marked starts count separately in each sign. Their regular returns explain F_h=0.

The other six supplied states were also checked exactly, including the pinned lexicographic root. All recorded F, H_pm, divergence, cleared-denominator gaps, candidate-pass flags and the failed-control list agree. This review does not rerun the prior complete all-direction darkness certificate: its global darkness is inherited. The local counterexample to the candidate needs only the independently verified H_pm=0 and feature values at A.

### 5. Candidate domain, calibration and constant weights — ACCEPT the obstruction; REJECT the candidate

The proposed inequality is H_pm >= (9-r)F_h/(16N)+D on 1<=r<=9 and the entire finite labelled orbit of the initial physical representative. At A, r=9 makes the first term zero and the claim reads0>=10. The exact cleared-denominator gap is -9600. This conclusively rejects that stated inequality.

For Phi=lambda F_v and Psi=mu F_h with constant real coefficients, the three controls force

A: 10mu<=0; C0: 10lambda<=0; B: -10(lambda+mu)<=0.

Consequently lambda<=0, mu<=0 and lambda+mu>=0, so both are zero. No sign restriction on the constants was assumed and no coefficient fitting is needed. This excludes precisely nonzero constant crossed coefficients in a formula asserted at these r=9 states with vanishing threshold term.

It does not exclude r<=8-only inequalities, r-dependent coefficients vanishing at9, identity-dependent tensors, other potentials or weights, or the universal illumination conjecture. Neither an orbit-positive sum of F_h at low r nor a valid low-r pointwise inequality has been proved. The normalization16N has positive denominator and creates no positivity. Finite telescoping is legitimate on these raw labelled states but has no force without both missing ingredients. These r=9 controls alone do not establish failure within r<=8.

### 6. Physical domain and reflection descent — ACCEPT with stated scope

The incidence definition and permutation identities hold on the full raw labelled state space, so their proof does not need every shear to be an orthogonal-room unfolding. The final argument explicitly makes the stronger orbit-wide inequality a proposal; it does not derive it by applying a physical-room lemma to nonphysical shear states. It does not transport full reflection data through a finite quotient.

The accepted label-descent review supplies the necessary warning: a sheared full marked cover need not remain physically realizable as an orthogonal room, even though the orbit contains the original physical representative. Its regular-root half-turn determination has connected-component and actual-cover-point qualifications; none is used to assert a new physical classification here. A future pointwise geometric inequality would need its own orbit-wide justification. No such justification is supplied by B06.

The length3 zero-cycle setup concerns the orthogonal family. General canonical45 nonorthogonal corners are not covered by an r>=9 inference from this packet. Even in the orthogonal family, B06 proves no new wall bound.

### 7. Prescribed square and positive-theorem limits — ACCEPT

For the period48 square torus, S={12,36}x{12,36} and T={16,32}x{18,30} are full distinct four-point fibers. There are no zeros, so F is identically zero for every directional permutation and every shear. This is an r=0 control outside the proposed domain.

The three specified directions avoid opposite-color marks by exact invariants: horizontal preserves y, vertical preserves x, and (1,-1) preserves x+y modulo48. The corresponding S and T invariant sets are disjoint in each case. Both orientations return after48 unit steps. The direct segment (12,12) to (16,18) lies strictly inside the convex square and has primitive direction (2,3), so the room is illuminated. No search is needed to establish that segment.

This control proves only that the shared-zero feature has zero orbit weight at r=0 and needs separate treatment there. It refutes neither illumination nor a stated 1<=r<=9 candidate through an out-of-domain point. It supplies no low-reflex theorem.

## Exact missing positive implication and handoff

For orthogonal physical unfoldings with complete distinct actual endpoint fibers, the missing assertion is: persistent separation in every genuine straight direction forces at least nine reflex vertices, or some direction provides a finite corner-avoiding path to an actual target lift. For the proposed exchange route, a new valid orbit-wide inequality and a strictly positive orbit sum for its weight on every putative dark physical low-reflex orbit are both absent. A finite encoding or exact exchange identity proves neither. Arbitrary canonical45 nonorthogonal corners additionally need a separate structural argument.

All seven requested review questions are resolved at this scoped level. The bookkeeping lemmas and the precise retirement of the threshold-calibrated constant-crossed proposal are accepted. No qualifying dark counterexample, positive illumination theorem or new wall bound follows. Frozen sources, git state, native goal/accounting and the budget waiver are preserved. No new discovery, census, fitting or worker was used. The author's original discovery deadline was not restarted. The global goal remains unfinished.
