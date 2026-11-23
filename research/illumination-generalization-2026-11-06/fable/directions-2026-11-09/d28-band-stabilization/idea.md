# Band stabilization: a route from "infinitely many rooms" to a finite check

Coordinator's idea, 2026-11-10. Unreviewed.

## Band lemma (elementary; proof sketch)

Let P be an orthogonal lattice room, (S, T) a pair of lattice points, and
y = c a horizontal lattice line that contains no vertex of P and is not the
row of S or T. The line meets P in chords of widths w_1, ..., w_m. Let
P[c, D] be P with a horizontal band of height D (D even) inserted at y = c:
the part above the line moves up by D, the chords become D-tall rectangles.
W, r, and parity classes are unchanged.

Claim: if (S, T) is lit in P by a path pi whose segments cross y = c with
primitive directions (q_j, p_j), p_j != 0, then (S, T) is lit in P[c, D] for
every D divisible by M(pi) = 2 lcm(w_i) lcm(p_j).

Reason: inside a chord rectangle of width w a segment of direction (q, p)
reflects off the two vertical walls; unfolded, its horizontal displacement
across the band is D q / p, which is a multiple of 2w, so it leaves the
band at the same point and in the same direction as it entered. The band's
vertical walls are straight continuations, so no corner lies in the band;
reflections there are at flat wall points, which the lit definition allows.
Above the band everything is translated by D. Vertical crossings (q = 0)
survive for every D. The same holds for vertical bands.

## Why it matters

The lemma relates darkness on *different* closed SL(2,Z) orbits (different
square-tiled surfaces), which no earlier step does. A room with W <= 20 has
at most r + 2 distinct horizontal wall levels and r + 2 vertical ones. Add
the rows and columns of S and T. A "skeleton" is the combinatorial type
together with these levels; a room with its pair is a skeleton plus a
vector of gap heights g and gap widths w. Finitely many skeletons exist for
W <= 20. So:

  Stabilization conjecture. For each skeleton there are an explicit
  threshold G and period Q such that the lit/dark status of (P, S, T) is
  unchanged when one gap above G changes by Q.

Stabilization plus a finite computation on rooms with all gaps <= G + Q
would prove the 20-wall statement. Dead end 5 ("no size bound reduces the
conjecture to a finite check") assumed area as the size measure; gap
vectors are a different one.

## Where it can break

- The lemma gives "lit at g => lit at g + k M(pi)". M(pi) depends on the
  witness through lcm(p_j). Stabilization needs witnesses whose crossing
  slopes have bounded numerators p, uniformly in the gap, or a different
  argument.
- Pairs with S or T inside a tall gap: choose the sub-band to remove so it
  avoids their rows (a gap of height >= 3D contains a free sub-band of
  height D). Shrinking needs lit-at-the-smaller-room witnesses with period
  dividing D: same issue.
- Changing a horizontal gap changes nothing about chord widths, but
  changing a vertical gap changes chord widths, so the periods couple.
- Dark side: the dark locus meets the real line {P[c, D] : D in R} in a
  closed set; finiteness (EMM) holds on compact segments, but D -> infinity
  is a cusp, where mass can escape.
