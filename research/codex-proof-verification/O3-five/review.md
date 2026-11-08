# Independent review: O3 five-reflection proof

**Verdict: accept the new optical lemma and its conditional six-reflection
family application. No correction found.** Reviewed November 5, 2026 by the
diagnostics Codex at Daniel's request. This review concerns the frozen
`surplus-four-local/O3-R23-search/findings.txt` result, not subsequent O3/L70
work or the previously rejected ten-reflection candidate.

The mathematical conclusion is: every valid canonical triangle room containing
`H+B701` and omitting the five protected triangles `L7,D3,D4,B2,B6` has the
specified legal five-reflection S-to-T path, in particular every room in the
author's stated minimum/maximum envelope. Under the established **local
two-root e2+e1+b1 classification**, all O3 second-root partners except L70
illuminate within six reflections after the inherited short forcing cases.
This review does not independently reprove that upstream classification.

## 1. The path is physically legal

The prescribed path is

\[
(0,0)\to(-1,-2/5)\to(1,-6/5)\to(0,-8/5)
\to(1,-2)\to(2/7,-16/7)\to(2,2).
\]

I independently rebuilt the boundary of the **one supplied room** from its
32 canonical triangles. It has one simple boundary cycle, 24 atomic edges
and 20 maximal straight walls. The only full even-even lattice stars are
S=(0,0), U=(2,0), T=(2,2); independently obtained J=2 and s_N=4.
The room specification has two positive roots and three ordinary caps, so
Q=3+2+3=8, k=J+s_N=6, and Delta=Q+s_N-8=4. Its W=20 agrees with the ledger.

The five finite mirrors, in order, are:

| Contact | Protected maximal wall or subsegment | Contact condition |
|---|---|---|
| (-1,-2/5) | x=-1, -1<y<0 | Strict interior |
| (1,-6/5) | x=1, -3<y<-1 | Strict interior |
| (0,-8/5) | x=0, -2<y<-1 | Strict interior |
| (1,-2) | x=1, -3<y<-1 | Strict interior |
| (2/7,-16/7) | y=-x-2, 0<x<1 | Strict interior |

Exact segment/boundary intersections show that each claimed reflection is
the **first** boundary contact on its leg. There is no intervening wall,
overlap along a wall, or polygon-vertex contact. All five reflection laws
hold exactly. Actual T is absent from every earlier segment and is reached
on the final leg. Reverse and sigma/reversed physical paths also pass.

The potentially misleading contact `(1,-2)` is legal. B0 and B7 occupy
exactly its left half-plane; D3 and D4 would occupy the opposite half-plane
and are absent. Its angle is exactly 180 degrees, and it lies inside the
single maximal wall from `(1,-3)` to `(1,-1)`. It is not a polygon vertex.
The O3 apex `(0,-2)` has angle 135 degrees, but the path avoids it.

## 2. The hand derivation is correct

Launch with velocity `(-1,-d)`. The first four vertical-wall contacts are
`(-1,-d), (1,-3d), (0,-4d), (1,-5d)`. After the fourth reflection the
line is `y=d*x-6d`. Intersecting it with `y=-x-2` gives

\[
E=\left(\frac{6d-2}{1+d},-\frac{8d}{1+d}\right).
\]

Reflection across that diagonal changes direction `(-1,-d)` to `(d,1)`.
The outgoing line is `x=d*y+8d-2`. At target height y=2 it has
`x=10d-2`, so actual T forces **d=2/5**. This is strictly inside the
stated sufficient interval **1/3<d<3/7**.

The finite inequalities hold throughout that interval: source contact
`-1<-d<0`; first right contact `-2<-3d<-1`; left contact
`-2<-4d<-1`; second right contact `-3<-5d<-1`; diagonal contact
`0<(6d-2)/(1+d)<1`. The final bottom portal has `0<7d-2<1`, the
target-chamber entry has `1<9d-2<3`, and the final x=1 crossing has
`-1<3/d-8<1`. These keep the route in the required chambers. At the
root, every formula reproduces the stated rational contacts. Reflecting
actual T backward through the five mirror lines gives `(-10,-4)`, aligned
with the initial `(-5,-2)` direction.

## 3. One room really does imply the stated support lemma

I did not execute or import the author's verifier, discovery code, or
historical geometry engines. My checker uses a different implementation:
it clips each prescribed open segment against canonical triangles using
exact rational half-plane inequalities. It includes triangles touched
only at an intermediate mesh vertex, not just triangles containing a
sample point. Complete incident triangles at each bounce are split into
required and forbidden half-planes.

This independently yields **11 required triangles and five forbidden
triangles**, exactly matching the author's sets. Every required triangle
lies in H+B701. The forbidden set is precisely

`L7, D3, D4, B2, B6`.

Thus every open leg has a full interior neighborhood, and every bounce
has a complete occupied half-plane and empty opposite half-plane. Any
valid room in the stated support envelope preserves the actual path.
There is no unproved assumption that illumination is monotone under
arbitrary enlargement. The five protected absences are essential to this
certificate.

As sensitivity checks, the independent checker rejects a changed
non-specular contact and rejects admitting each of the five forbidden
mirror-mate triangles into the maximum envelope: six rejected mutations.
These are fixed proof checks, not discovery searches or new room trials.

## 4. The six-reflection family dispatch follows conditionally

I independently rechecked the actual prescribed paths behind all four
forcing implications, including their complete support requirements:

| Trigger | Rechecked path length |
|---|---:|
| E4 absent | 1 |
| L0 absent, E ordinary4 | 4 |
| L0 absent, E34 | 3 |
| L0 absent, E45 | 2 |

These paths allow the other local stars stated in their envelopes. They
justify reducing to E4 and L0 without importing an unjustified Tc5
restriction. With E as the second root, E23 is already handled by E4
absence; E34 and E45 are the active remaining windows.

Under the established root-window and ordinary-cap convention:

- L01 fits the five-path envelope; **L70 does not** because it contains L7.
- D01 and D12 fit the five-path envelope.
- D23 requires a different path. I independently recomputed the inherited
  four-path and its complete 15-required/3-forbidden support, including
  the fully interior `(1,-1)` crossing supplied by D23. It applies when
  ordinary Tc is empty or6. The inherited six-path independently gives
  14 required/four forbidden triangles and applies when ordinary Tc is5.
  These exhaust ordinary Tc because B and D are the two positive roots.
- Partners at R, E, Tc and N fit the new envelope, since their full stars
  are allowed while L is ordinary0 and D is ordinary empty/1/2. Including
  N67 in the support check is harmless even if an earlier bridge lemma
  has already disposed of it.

The checker verifies 18 symbolic active root windows, with L70 explicitly
excluded and D23 assigned to the rechecked four/six split. These are
support implications, **not counts or enumeration of completed rooms**.
The maximum length is six; forcing cases require at most four.

## 5. Limits and reproduction

Accepted here: the fixed room witness; its five-reflection optical
support lemma; the six-reflection bound for O3 partners **other than
L70**, conditional on the established local two-root classification.

Not accepted or established here: full O3 closure, subsequent L70 results,
all surplus-four cases, a universal 22-wall minimum, or the global
completeness of the earlier classification. Both Dsingle3 and Dsingle4
remove protected mirrors, so this witness gives no transfer to those
single-leaf cases. This is an independent mathematical review with exact
computational checks, not formal verification or expert refereeing.

Reproduce only this fixed audit:

```sh
python3 -B .context/codex-proof-verification/O3-five/check.py
```

`check.json` records exact outputs and SHA-256 hashes of its data sources.
The original proof and research artifacts were left unchanged.
