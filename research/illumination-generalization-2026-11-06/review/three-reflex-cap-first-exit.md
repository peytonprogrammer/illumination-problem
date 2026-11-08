# Actual cap returns: first-exit guards before any height inflation

Reviewer hand deduction, independent of author TR01/TR02/TR03. This audits a possible next premise rather than attributing an unmade claim to the author. It supplies a physical countercontrol to treating many shallow cap excursions as a single tall cap. No fixed-room search, new engine or discovery effort is used.

## Complete cap guard for a prescribed number of excursions

Use the ordered spiral, `epsilon=H-h>0`, cap rectangle `[0,A]x[h,H]`. Its lower edge is an actual reflecting wall ONLY on `(a,w)x{h}`. The intervals `[0,a)x{h}` and `(w,A]x{h}` are passages into the left and right arms. Their outer endpoints x=0,A are smooth vertical-wall points, not horizontal mirrors; x=a,w are true reflex corners.

Suppose a trajectory enters the cap upward at y=h with cap phase `xi`, folded coordinate `F_A(xi)` in `[0,a)`, and with horizontal unfolded speed tau>0 after normalizing |vy|=1. A prescribed N-excursion cap segment has lower-return phases

```
xi_j = xi + 2j epsilon tau,  j=1,...,N,
```

and roof phases `xi+(2j-1)epsilon*tau`, j=1,...,N.

For the segment to remain in this original cap and first exit through the right passage at its Nth lower return, it is necessary and sufficient that

```
a < F_A(xi_j) < w,        1<=j<N,
w < F_A(xi_N) <= A,
xi+(2j-1)epsilon*tau not in A Z,   1<=j<=N.
```

The initial fold must also have its specified physical injection velocity. An initial x=0 injection is a smooth vertical-wall contact and can be dealt with by the corresponding one-sided direction. At the final x=A exit a simultaneous smooth outer-wall contact is legal, with the reflected horizontal velocity. There is no horizontal reflection at that exit.

Proof: between consecutive lower returns the rectangle billiard unfolds to a straight line. Roof singularities occur exactly at roof phase multiples of A. All other vertical contacts in the open cap are on genuine outer walls. At a lower return in (a,w), the actual horizontal shelf reflects vy; at either passage the trajectory exits and cannot be assigned an extra cap bounce. At a or w it hits a true corner and cannot continue. This proves both directions for the cap segment. It proves neither later right/bottom matching nor actual target attainment; those remain independent obligations.

In particular, replacing `2epsilon` by `2N epsilon` in the accepted single-roof equation does NOT authorize those N excursions. The N-1 extra guards are material physical hypotheses.

## Parametric physical countercontrol to checking endpoints alone

Let `R=A-w>a`, choose any `x0` in `(0,a)`, and put `tau=A/(2epsilon)`. Take xi=x0, so each excursion advances cap phase by A. Then

```
F_A(xi_j) = A-x0 for odd j, and x0 for even j.
```

For EVERY odd N>=3, the initial and final mouth coordinates satisfy the required left-to-right strict portal bounds. Every roof phase folds to `A/2+x0` or `A/2-x0`, strictly between 0 and A because `R>a` and `w>a` imply A>2a. Thus all roof contacts are smooth. Nevertheless the trajectory exits through the right passage at j=1. The virtual N-excursion curve would reflect horizontally at that open passage, and later at a left passage. It is not a path in the original room.

This injection can come from an actual lower-column source, rather than an abstract cap boundary state. Choose epsilon so `4a epsilon/A<h-b`, and set

```
S=(x0,h-4a epsilon/A),   tau=A/(2epsilon), initial vy=+1.
```

The source is strictly interior. Its left-arm developed horizontal advance before h is exactly 2a, so it reaches the prescribed injection coordinate x0 with the upward injection direction and no corner. It then follows the smooth first roof excursion and exits right exactly as above. Rational choices can be uniformly scaled to integral walls and even-even actual S, so the effect is not excluded by the arithmetic target domain. No darkness or actual dark pair is asserted.

This is a family countercontrol to endpoint-only cap lifting. It does not refute a future multiple-excursion construction that explicitly proves every intermediate first-hit guard.

## Why increasing N loses a uniform source margin on one natural branch

On the cap branch with physical x strictly increasing throughout (no cap side-wall reflection), write its entry x0 in `(0,a)` and `Delta=2epsilon*tau`. For N>=2, the exact cap conditions reduce to

```
max(a-x0,(w-x0)/N) < Delta
    < min((w-x0)/(N-1),(A-x0)/N).
```

Here the final x<A restriction deliberately selects the no-side-contact branch. The first inequality places return 1 on the shelf and return N in the right passage; the second keeps return N-1 on the shelf and return N below A. Monotonicity then supplies all intermediate guards. Roof phases are interior automatically.

For N>2, a necessary consequence is

```
x0 > a - (w-a)/(N-2).
```

Thus arbitrarily many excursions on this branch force injection points toward the true reflex corner a, with a shrinking permissible source margin. For a fixed actual injection x0<a, N has a finite upper bound. This shows exactly why longer effective flight time does not by itself retain the fixed open slope component used in TR03. A proof can vary the injection and choose another branch, but must quantify that joint selection while avoiding the corner and preserving actual S,T.

## Handoff and scope

The author retains constructive short-roof selection. Reviewer challenge: if a next candidate inflates the cap flight time, include all intermediate shelf/roof guards, prove first exit occurs at its declared step, and supply exact signed right/bottom and original-target matching. The accepted TR03 theorem is unchanged. Full r3 and r<=8 remain open.
