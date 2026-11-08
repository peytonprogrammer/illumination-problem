# From neck patterns to exceptional-vertex gates

[done] This phase supplies an elementary finite-visit bound and a candidate common illumination mechanism. It does not close another room placement.

Every one of147 previously saved illuminated rooms now has an exact ray that encounters just one exceptional B/C vertex, at the optical midpoint. This includes104 rooms matching the12 current residual neck types, with examples of every type. The other43 rooms belong to earlier neck patterns. These rooms were selected by earlier positive-ray searches; this is evidence for a common mechanism, not a proof that every remaining completion has such a ray.

For a fixed primitive direction, a first-arrival ray has a justified reflection budget. With three exceptions it makes at most24 exceptional-vertex visits. There are still infinitely many primitive directions, so the result is not an all-direction decision procedure or darkness certificate. No literature-priority claim is made for the observation.

## What the wall and exception budget forces

`illumination_neck_budget.py` treats each local vertex fan as a table and propagates triangle domains. It combines the exact wall identity W=14+Q-E with W<=23, exactly three exceptions, N<=36, and E+m<=6. It also propagates the triangle-connectivity backbone: a triangle whose deletion separates already forced occupied triangles must be present. Triangles in potential components unreachable from the forced component must be absent.

These are necessary conditions. Local table consistency does not enforce the full selected room's Euler characteristic or connectivity, and does not prove a ray exists. No ray cuts are used inside this propagation; the12 input neck patterns themselves come from the earlier audited ray exclusions.

The procedure locates forced exceptions in several types. In types8–10, connectivity additionally forces triangle ((3,-1),(3,0),(4,0)), in the neighboring A-cell(2,0). This reduces that cell from57 possible absent/partial fans to28. Other neighbor domains often remain broad. The budget therefore does not yet force enough geometry for an illumination proof.

The audit independently checks17,440 local masks using triangle-fan connectivity, compares the budget support calculation against exhaustive products on200 fixtures (97 feasible), and checks the connectivity backbone against every selected subset on200 small graphs (120 feasible). All propagated constraints retain422 distinct valid room completions, drawn from saved rooms and their mark-exchanged half-turns, across all12 types. A readback comparison initially needed normalization of tuples to JSON lists; the corrected audit passes.

## Finite exceptional-visit lemma

Consider a simple canonical45–45–90 triangle room, with distinct interior A marks. Let J be the number of interior non-A vertices and S the number of straight-boundary non-A vertices. All other B/C vertices absorb rays. There is no restriction here on the number of full A stars or on the wall count.

Fix a nonzero primitive integer direction d=(p,q). Let r be the size of its orbit under the eight signed coordinate permutations D4. Thus r=4 for an axis or diagonal direction and r=8 otherwise.

**Claim.** A ray that reaches the target for the first time has at most

    K = r*J + (r/2)*S

exceptional-vertex encounters, counting repeated visits separately. For J+S=3, K<=24.

### Proof

1. Every canonical wall reflection has a D4 linear part and an even integer translation. Vertical and horizontal walls lie on x=c or y=c, with c integer. Diagonal walls lie on x+y=2c or x-y=2c. These reflections preserve the integer lattice and the labels A/B/C.
2. Unfold a hypothetical connecting ray. Its source and target images both have even integer coordinates. Therefore its direction is rational and can be represented by a primitive integer vector d. Normalize time so the unfolded velocity is d.
3. Its final primitive time L is a positive even integer: the displacement L*d has both coordinates even, and at least one component of primitive d is odd.
4. At every odd integer time before arrival, the unfolded ray is at a non-A integer vertex. Folding preserves the label, so the physical ray must encounter a B/C exception there; an ordinary B/C corner would absorb it. At even integer times the label is A. Primitivity permits no other integer-vertex times. The number of exceptional encounters is thus exactly L/2.
5. Record the physical exception point and the outgoing primitive velocity after any reflection there. Velocity always lies in D4*d. At an interior exception there are at most r such states. At a smooth boundary exception, the outgoing ray must enter the interior half-plane. From each opposite velocity pair at most one can do so, giving at most r/2 states. Tangential travel along the boundary is not legal.
6. The same outgoing state cannot occur twice before the target's first arrival. Billiard continuation from that regular interior point or smooth boundary point is deterministic. A repeated state would repeat the future trajectory and force an earlier target arrival, or a periodic orbit missing the target.
7. There are at most K available states, so L/2<=K. This proves the claim.

This counts exceptional encounters, not wall reflections. The distinction matters: a ray can reflect many times between two integer-vertex events.

### A complete bound for a fixed direction

In the unfolding, every reflected wall belongs to one of four line families:

    x in Z, y in Z, x+y in 2Z, x-y in 2Z.

Over primitive time L, the number of crossings of these families is at most

    L*(abs(p)+abs(q)+(abs(p+q)+abs(p-q))/2)
      = L*(abs(p)+abs(q)+max(abs(p),abs(q))).

Every legal reflection supplies one such crossing. A tangent along a wall is excluded, and simultaneous crossings at an integer vertex only overcount. Since L<=2K, every first-arrival connecting ray in this fixed direction has at most

    R = 2*K*(abs(p)+abs(q)+max(abs(p),abs(q)))

reflections. If a validated room's tracer has already exceeded this budget without reaching the target, that direction cannot illuminate it. This supplies a finite decision for the chosen rational direction, replacing an arbitrary bounce cutoff. It leaves the primitive direction itself unbounded.

For K=0, no connecting ray is possible: any positive even primitive duration contains an odd-time non-A encounter, but no exception can admit it. This recovers the existing strict-family darkness certificate rather than a new construction.

## The single-pass midpoint mechanism

If a ray encounters exactly one exception, L=2. The event at primitive time1 is therefore exactly halfway along its optical path. It can be a passage through an interior exception or a reflection at a smooth boundary exception. No global symmetry of the room or its unfolded surface is assumed.

Initially,122 of the147 saved rays had one encounter,23 had two, and two had three. The analysis reconstructs every integer-vertex encounter in two different ways and independently unfolds the physical segments; both agree, including L=2 times the encounter count and the absence of repeated outgoing gate states.

A first bounded probe uses a128-direction catalogue on the25 multi-encounter rooms. It finds21 one-pass alternatives after1,390 directional tests. One targeted follow-up checks previously untested primitive directions through component bound16 on the four remaining rooms. It finds all four alternatives after550 further tests (record indices below are zero-based):

| Saved record | Current neck type | New direction | Midpoint gate | Reflections |
| --- | --- | --- | --- | ---: |
| double-fan record62 | Earlier type | (11,-6) | (3,2) | 14 |
| double-fan record75 | 8 | (-7,-11) | (5,1) | 17 |
| double-fan record83 | 1 | (8,-3) | (0,-1) | 7 |
| double-fan record93 | 5 | (-8,-9) | (1,0) | 16 |

The result is147/147 exact single-pass witnesses in this saved population, including104/104 current-neck samples. It is not a universal single-pass theorem. Failure in either bounded catalogue would have remained unresolved, not a proof that multiple gate visits were necessary.

## Validation and reproduction

The directional audit checks490 affine edges against all four parity classes and all64 point-group products. It replays all147 original positive rays and all1,940 alternative-path direction tests with the independent triangle-event tracer. It also checks192 low-direction negatives,32 strict-dark directional controls, and three rejected out-of-scope inputs. All checks pass; no independent triangle trace reaches its event limit in the192 low-direction checks.

The new entry point is `illumination_exception_gate_bound.decide_direction(room,direction)`. It returns a positive witness or a negative answer for that one direction, under the stated geometric assumptions. It never concludes global darkness from a finite direction list.

Copy the frozen inputs in `neck-budget-proof-inputs-2-1.json` into a separately claimed directory, preserving relative subdirectories, then run:

```sh
PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -B <copy>/audit_illumination_neck_budget.py
PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -B <copy>/audit_illumination_exception_gate_bound.py
```

Receipts: `neck-budget-audit-2-1.json`, `exception-itineraries-2-1.json`, `single-gate-probe-2-1.json`, and `gate-bound-audit-2-1.json`. The old manifests and Claude-owned files remain unchanged. Claude's independent check of this new bound and mechanism is pending.

No new room geometries or exclusion guards were added in this phase. All probes and audits have stopped. The unresolved count remains12 neck types,102/105 outside sets excluded at target(2,1), and seven of ten whole placements excluded. No smaller room or full three-exception minimum is established.

**Next move:** prove or disprove single-pass midpoint-gate sufficiency for every valid completion of the12 residual neck types. The concrete task is to match source-to-gate and target-to-gate reflected visibility under the remaining budget; another large fan partition is not the current goal.
