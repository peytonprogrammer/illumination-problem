# Centered midpoint resonance: obstruction and two-reflection repair

Codex01a18403, 6 November 2026. Frozen parent milestone for independent review.

Let d,g,a,h_-,h_+>0, b=a+g, h_->a, h_+>b. In the stated corridor
P=[0,2d]×[-h_-,0] union[d,3d]×[0,g] union[0,2d]×[g,g+h_+],
take actual S=(d,-a) and T=(d,g+b).

## A. No vertical-wall-only connection

All vertical mirrors lie on integer multiples of d. Reflections x->2jd-x
preserve odd multiples of d, so unfolding a hypothetical vertical-only
trajectory gives a straight segment from (d,-a) to(L,g+b), with L an odd
multiple of d. Vertical velocity is constant positive. Since b=a+g,
H=a+g+b=2(a+g), and y=g occurs at half the elapsed time. The developed
x-coordinate there is(d+L)/2, an integer multiple of d. Folding by the
actual sequence of vertical reflections preserves integer multiples of d.
The physical upper-portal coordinate is therefore an integer multiple of d,
whereas entry into the upper chamber requires x strictly between d and2d.
No legal such connection exists. Vertical-only paths cannot leave and return
to these height bands because physical y is strictly increasing.
This proves failure of the full mechanism, not darkness.

## B. An actual two-reflection connection, for every allowed dimension

Write h=h_+. Set

    R=(2d,h-a),  C=(2d-db/h,g+h).

Then S -> R -> C -> T is legal. R is in the strict interior of the upper
right wall because h-a>g (h>b=a+g) and h-a<g+h. Also d<C_x<2d since
0<b/h<1. Thus C is a smooth top-wall point, not a corner.

The initial leg has direction(d/h,1), up to positive speed. Its crossings
of y=0 and y=g occur at

    x=d+da/h and x=d+d(a+g)/h=d+db/h,

both strictly in(d,2d), and it first hits a wall at R. Before y=0 the
segment lies inside the lower chamber; between0 andg it lies inside the
middle chamber; fromg toR it lies inside the upper chamber.

From R to C the displacement is(-db/h,b), with b=a+g>0. Thus its
horizontal slope is -d/h, reversing only the horizontal component at R.
This entire segment stays in the upper rectangle, reaching its top first
at C. From C to T the displacement is

    (-d(h-b)/h, -(h-b)),

with h-b>0. It reverses only the vertical component at C and ends at actual
T. The final open segment is strictly inside the upper chamber. T cannot
occur on the first leg (which has x>d after departure), nor the second leg
(which has x>d throughout). All three legs have positive length.

Both mirrors are actual exterior walls. The path uses no artificial wall,
no limiting trajectory, no integer/rational assumption and no minimum
clearance. The lower exterior height affects only S being interior.
The y-reflected and time-reversed construction handles a=b+g as well.

## Scope and strategy consequence

This closes the entire centered line b=a+g (and its reversal), not arbitrary
horizontal coordinates or all unequal depths. It proves that upper exterior
walls can be essential to repairing a folding obstruction, with arbitrarily
small target-to-cap clearance still allowed. It is not a dark counterexample
or a universal wall minimum. No global reflection bound is inferred.
