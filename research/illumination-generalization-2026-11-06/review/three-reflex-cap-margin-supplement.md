# A cap first-exit bound for every horizontal phase branch

This supplements `three-reflex-cap-first-exit.md` without modifying its announced hash. The earlier shrinking-margin calculation selected a physically monotone-x cap branch. The bound here applies to ALL cap side-wall reflection words. It remains a necessary condition, not a target-attainment theorem.

## Quantified first-return lemma

Let a trajectory enter the original cap upward from the left mouth, with reduced signed phase `xi in (-a,a)`. Put `rho=a-|xi|>0`, its distance to the left-mouth true-corner phases. Let N be the number of roof contacts before its FIRST exit from this cap through the right mouth. There is no earlier left-mouth exit; intermediate lower returns must all reflect on the actual central shelf. Then

```
N <= floor(2A/rho).
```

There is no hypothesis on tau, rationality, number of cap side-wall contacts, or intermediate winding number.

Proof: take the cap circle circumference `C=2A` and rotation step `alpha=2epsilon*tau modulo C`. Set `M=floor(C/rho)+1`, so `C/M<rho`. Place the M+1 residues `0,alpha,...,M alpha` in M half-open equal circle-coordinate boxes. Two lie in the same box. Their difference gives an integer `n in {1,...,M}` with circle distance `dist(n alpha,C Z)<rho`. Consequently the nth lower-return phase, starting at xi, lies strictly in `(-a,a) modulo C`, the LEFT mouth. If a claimed first right exit had N>=M, its prescribed cap orbit would still be in the cap through this nth return; that return is instead an earlier or simultaneous left exit. Both are impossible. Hence `N<M`, which is the displayed bound. Coincident residues give distance zero and are included. Strict distance excludes the true-corner equality. A right-mouth phase cannot also be a left-mouth phase because a<w<A.

This uses explicit circle recurrence only to bound a forbidden cap itinerary. It does not assert that recurrence creates an actual S-to-T ray, that the right mouth is ever reached, or that any target fiber is met.

## Coupling the first-exit bound to the physical bottom leg

Consider a path from an actual lower-left source to an actual lowest-chamber target T=(t,v) which:

- enters the cap from the left mouth;
- has N original roof contacts and N-1 original central-shelf reflections before its first right exit;
- then descends through the right arm into the bottom chamber, with no further horizontal reflection before actual T.

Arbitrary vertical-wall reflections in all bands are allowed. Write `q` for the number of inner bottom x=l contacts on that last leg; `d=c-v`, `z=A-t`, `B=A-l`, `R=A-w` as before.

The cap elapsed time is exactly `2N epsilon`, so absolute horizontal travel yields

```
2N epsilon tau > w-a.
```

The bottom one-dimensional counting argument from `three-reflex-single-roof-necessity.md` does not depend on N and still gives `tau*d<2qB+z+R`. Combining with the first-return lemma gives

```
N(2qB+z+R) > d(w-a)/(2epsilon),
2qB+z+R > d(w-a)rho/(4A epsilon).
```

Thus even allowing arbitrarily many legitimate roof/shelf excursions does not support a uniformly thick injection interval and bounded bottom winding as epsilon shrinks. More precisely, if a proposed method keeps `rho>=rho0>0` and `q<=Q`, it necessarily has

```
epsilon > d(w-a)rho0 / [4A(2QB+z+R)].
```

At equality or below, that entire restricted mechanism is impossible. A valid all-short-cap proof must let the injection approach a true-corner phase, let the bottom winding increase, or change its horizontal-reflection pattern. It may do any of these, but joint selection and finite corner avoidance must be proved.

The accepted tall/wide conditional theorems are not challenged. Nor does this control exclude rays that leave the cap left, use another actual horizontal mirror, or follow an unrelated optical itinerary. It is not a full-room darkness claim.

## Review handoff

The author owns new constructive packets. This reviewer supplies the above all-branch necessary bound for independent challenge. It sharpens the earlier branch-specific cap-margin warning and prevents a shortcut that merely replaces the top height by N times its actual value. No discovery search, fixed-room census, new engine or renewed clock was used. Full r3/r<=8 remains open.
