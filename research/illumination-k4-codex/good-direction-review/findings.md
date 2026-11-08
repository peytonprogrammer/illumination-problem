# Review of Opus's denominator and monodromy note

## Arithmetic lemma

The primitive-coset criterion is correct: u+N Z^2 contains a primitive vector if and only if gcd(u_x,u_y,N)=1. Necessity is immediate. For sufficiency, keep a nonzero first coordinate a in its required congruence class. Primes dividing both a and N cannot divide the prescribed second coordinate, by the gcd hypothesis. For each other prime dividing a, choose the second-coordinate shift to avoid its one forbidden residue; the Chinese remainder theorem supplies such a shift. The two resulting coordinates are coprime. If the first residue is zero, choose a=N and the gcd hypothesis makes the second coordinate coprime to N. Here N=2D>=2.

A primitive numerator gives a finite segment whose interior misses every point of the (1/D)-grid, since both coordinate increments can be integral at a parameter lambda only when lambda is integral. With endpoints already in that grid, this part of the clean-segment argument is sound.

## A clean finite segment need not have a good direction

Opus calls a primitive direction v=(p,q) good at P when det(v,P)=p P_y-q P_x is nonintegral (equivalently his q P_x-p P_y is nonintegral). Good means the entire torus leaf avoids integer points. Clean means only the chosen finite segment avoids them. The clean-segment lemma does not imply a good direction.

**Coprime-denominator obstruction.** Suppose a source torus image P has denominator A and a target image Q has denominator B, with gcd(A,B)=1. Every integer direction v joining P to Q+2lambda satisfies

    det(v,P)=det(v,Q)+2det(v,lambda).

The left side belongs to (1/A)Z, and the right side belongs to (1/B)Z. Their intersection is Z. Hence every such connecting direction is bad. This applies to all reflected endpoint images because sign changes preserve the denominator bounds. No monodromy computation or direction enumeration is needed.

## Existing physical control

Use the SAME fixed L with boundary (0,0),(6,0),(6,3),(5,3),(5,4),(0,4), and z=(3,4). Our already prescribed marks are

    s=(12/7,16/7), t=(9/2,2).

Their torus denominators are 7 and 2. They have an ordinary direct connection inside the convex lower rectangle. Its primitive direction is (39,-4), with t-s=(39,-4)/14 and determinant det((39,-4),s)=96, an integer.

Moreover, the denominator lemma's hypothesis holds with D=14: for each target sign choice, u modulo28 is one of (-87,-60),(-87,-4),(39,-60),(39,-4), and gcd(u_x,u_y,28)=1. Thus the clean-segment arithmetic is available while every possible physical connecting direction fails the good-direction criterion. The complete leaf may encounter a grid point later, beyond the clean segment.

## Scope and revised target

This refutes unconditional existence of a good connecting direction from mere existence of a physical connection. It does not disprove the denominator lemma, the conditional good-direction argument under an additional global-essentiality assumption, or a global blocker-removal theorem. The physical example is lit and z is not essential.

The sufficient route 'find a common cylinder off its central core' remains valid when available, but it is stronger than necessary. A more precise monodromy task is to steer a clean FINITE segment to a lift of the actual target, without requiring its entire torus leaf to be corner-free. Direct copy/iota symmetry cannot steer a wrong physical endpoint because pi*g=pi.

No new ray, word, direction or room search was run. The fixed pair was taken from the already reviewed physical-midpoint packet. `check.py/json` records exact arithmetic and the finite-segment positive control.
