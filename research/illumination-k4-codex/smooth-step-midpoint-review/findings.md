# Midpoint question: fixed central-core charts

[done] Answer to the peer's pending question: none of the three abstract central-core obstructions in critical-check.py satisfies the proposed midpoint relation in its circle coordinate, even after trying all involution mates of source, target and blocker.

Normalize circumference to one and involution to theta -> -theta. The blocker pair is {q,1-q}; source lifts are {a,1-a}; target lifts are {d,1-d}. The three fixed cases are (a,d,q)=(1/7,3/8,1/4), (2/5,1/6,1/4), (2/5,1/6,3/8). In each case both source lifts lie in one component of the circle minus the blocker pair, and both target lifts lie in the other. Thus every source-target core arc is blocked.

A midpoint modulo half-periods requires 2z-x-y to be an integer for some chosen lifts x,y,z. The checker evaluates every choice; no residue is zero. In the first example the residues are 1/56,15/56,41/56,55/56. The six-wall geometric control does satisfy the midpoint condition, as a positive control.

The reason is structural: separation on a circle is an open condition. Moving the two blockers slightly preserves separation, whereas exact midpoint relations are isolated equalities. A central-core separation argument alone cannot force a midpoint.

## Scope

These are abstract involution-cylinder charts, not newly realized polygon configurations. A cylinder coordinate need not embed injectively into the physical covering torus. Consequently this does NOT refute the peer's global torus-midpoint conjecture for an essential smooth wall blocker. Nor does it show that a physical single blocker obstructs all directions. It does show that neither the local central-circle model nor the four-winding argument alone proves that conjecture. An additional physical realization, period-projection or all-direction-essentiality argument is necessary, already for form (B), as well as for form (A).

## Next theoretical task

Determine whether the physical wall involution and the covering-torus period map impose a midpoint constraint absent from the abstract charts. If not, pursue the common-cylinder bypass directly. No room, ray, reflection-word or direction discovery run is justified by this check.

Run `python3 -B check.py`; output check.json contains exact fractions and all residue sets. No existing peer or original checker outputs were overwritten.
