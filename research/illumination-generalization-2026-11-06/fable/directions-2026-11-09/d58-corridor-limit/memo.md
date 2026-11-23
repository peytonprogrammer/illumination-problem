# Corridor-limit lemma for door pairs and the chain diagnosis

Date: 2026-11-18. Direction d58. Notation follows `../d17-r3/r3.md` (Lemma H)
and `../d57-witness-mining-r3/README.md` (Lemma U, the 578 open pairs).
Tags: PROVED (hand proof here), CITED (proved elsewhere), COMPUTED (exact
check in this directory), GUESSED.

## Results

- **The corridor-limit lemma is Lemma H read in phase form.** Lemma P below
  gives Lemma H's exact failure set as a phase condition. Lemma H fails only
  when T is within (1 - kappa) w / 2 of a corridor wall, at an integer
  resonance n = L h / (w D). A point on the corridor's midline never fails.
  PROVED.
- **Door pairs have no degeneration problem; they have a resonance problem.**
  For all 10 door pairs, Lemma H's hypotheses hold on the whole open type
  region (COMPUTED, `door_geom.py`). So Lemma H covers every thin-corridor
  face of d57's Lemma U for these pairs. The only open set is the resonance
  set, which accumulates at the thin face. PROVED, given the COMPUTED check.
- **A second family repairs single resonances.** In all 10 door pairs, the
  corridor of the far point is a dead end (COMPUTED). Lemma E (bounce off the
  dead end) lights the pair unless a second integrality condition also holds,
  apart from an unproved corner-coincidence part. PROVED for the window part.
- **The 10 door pairs aren't closed for all real parameters.** What remains is
  the double-resonance set: L h / (w D) and L (2 ell - h) / (w D) both
  integers, D > 2 ell - h, plus residue conditions, plus Lemma E's corner
  set. It's nonempty arbitrarily close to the thin face. Exact instances exist
  at w = 2^-4, 2^-8, and 2^-12 for 8 of the 10 pairs (COMPUTED). Each instance
  tested is still lit by a short path of 1 to 5 reflections (COMPUTED).
- **Chains break where a strip runs out of free integers, not after a second
  door as such.** A route through m doors needs m window conditions. Each
  strip with two full parallel walls contributes one free image index. With
  at least m + 1 indices, Kronecker density gives a valid path off a
  resonance set; a two-scale argument is this density statement. Where a
  route segment has no full channel (a cut hub, a hub that isn't convex),
  validity fails on open sets of lengths, and no arithmetic argument helps.
  PROVED for the density part (Lemma K); the rest is a diagnosis.
- **The lemma doesn't apply to the 22-wall dark pair.** In all 8 frames and
  both orders, Lemma H's hypothesis 2 fails: the viewer's channel never
  contains the corridor's door, or the order is wrong (COMPUTED,
  `check22.py`).
- **The 10-wall strategy isn't complete.** "Finite covering on a compact core
  plus corridor-limit lemma near degenerations" leaves the double-resonance
  set of the 10 door pairs, all 553 chain pairs, and the faces of the 15
  collinear pairs. Closed for all real parameters: 0 of 578.

## Setting

A room P is a strictly simple orthogonal polygon. A valid path touches no
vertex, convex or reflex. Unfolding is as in d15: a path is a straight
segment folded by reflections in wall lines.

Canonical frame (Lemma H, CITED from r3.md):

- The corridor E = [p, q] x [d, e] has sides {p} x [d, e] and {q} x [d, e] in
  the boundary of P. The door is (p, q) on the line y = d. Write w = q - p.
- T = (p + beta w, d + h) with 0 < beta < 1 and 0 < h <= e - d.
- S = (s1, d - D) with D > 0. The channel Q = [a, b] x [s2, d] lies in P,
  with a <= p, q <= b, a < s1 < b, and the open segments {a} x (s2, d) and
  {b} x (s2, d) in the boundary of P. Write L = b - a.
- The images of S in the channel are s'(e1, k) = a + e1 (s1 - a) + 2 L k.
  The images of T in the corridor are X(e2, m) = p + e2 beta w + 2 w m.

The segment from (s', s2) to (X, d + h) crosses y = d at
xi = (h s' + D X) / (D + h). Lemma H, part 1: if p < xi < q, the segment
unfolds a valid path from S to T. CITED.

## Lemma P (phase form of Lemma H)

**Definitions.** kappa = h / D. For a viewer image x*, its phase is
phi(x*) = -h (x* - p) / (w D) mod 2, a point of the circle R / 2Z. The bad
arc is

    B(beta, kappa) = [beta, 1 - beta - kappa]        if beta <= (1 - kappa)/2,
                   = [-beta, beta - 1 - kappa]       if beta >= (1 + kappa)/2,
                   = empty                           otherwise.

B has length max(0, |1 - 2 beta| - kappa).

**Statement.**

1. A viewer image x* gives a valid path to some image of T if and only if
   phi(x*) is not in B(beta, kappa).
2. If kappa >= 1, or beta = 1/2, or |1 - 2 beta| <= kappa, every viewer image
   works.
3. With the channel images, S and T are lit by Lemma H unless all of these
   hold: n = L h / (w D) is a positive integer; kappa < 1; and both phases
   phi_+ = -n (s1 - p) / L and phi_- = -n (2 a - s1 - p) / L lie in B.

**Proof.** Fix x*. The condition p < xi < q is
(X - p) / w in (phi, phi + 1 + kappa), an open arc of length 1 + kappa.
The normalized T-images are +beta and -beta mod 2. They split the circle into
closed arcs [beta, 2 - beta] and [-beta, beta], of lengths 2 - 2 beta and
2 beta. The open arc misses both points exactly when it lies inside one of
these closed arcs. That's phi in B. This proves 1. If kappa >= 1, the arc has
length at least 2. It misses at most one point, and +beta and -beta differ
because 0 < beta < 1. The other cases of 2 make B empty.

For 3, the phases of s'(e1, k) are phi_e1 - 2 n k mod 2, where
n = L h / (w D). If n is irrational, each coset is dense, so it meets the
open complement of B. If n = r / s in lowest terms with s >= 2, each coset is
s points spaced 2 / s <= 1 apart. B is a closed arc shorter than 1 - kappa,
which is less than 1. So B contains at most ceil(s / 2) < s of them. If n is
an integer, each coset is the single point phi_e1. ∎

Lemma P reproduces Lemma H's "unless L h / (w D) is a positive integer and
D > h". It adds the exact residue set and two new facts. First, a failure
needs beta <= (1 - kappa) / 2 or beta >= (1 + kappa) / 2. So T lies within
(1 - kappa) w / 2 of a corridor wall. Second, the phases must also satisfy
|phi_+ - phi_-| <= |1 - 2 beta| - kappa on the circle.

**Corollary CL (corridor limit).** Fix every length except w, and fix beta.
Then S and T are lit for every w > 0 outside the discrete set
w_n = L h / (n D), n = 1, 2, .... At w = w_n they're lit unless
phi_+(n) and phi_-(n) both lie in B(beta, h / D). PROVED.

The same holds when the thin corridor is on the viewer's side, for example
d57's "bar height" face of type 122. D, L, and the channel can degenerate
freely, because Lemma H's hypotheses are combinatorial. Only the arithmetic
condition depends on lengths.

## Lemma E (bounce off a dead end)

**Extra hypothesis.** The far side [p, q] x {e} of E lies in the boundary of
P. Write ell = e - d, assume h < ell, and let h2 = 2 ell - h.

**Candidates.** As in Lemma H with h replaced by h2: the segment from
(s', s2) to (X, d + h2), crossing y = d at
xi2 = (h2 s' + D X) / (D + h2), and y = e at
x_ell = ((ell - h) s' + (D + ell) X) / (D + h2).

**Statement.**

1. If p < xi2 < q and x_ell is not in p + w Z, the segment unfolds a valid
   path from S to T. PROVED.
2. Some candidate has p < xi2 < q unless L h2 / (w D) is a positive integer,
   D > h2, and both E-phases lie in B(beta, h2 / D). PROVED (Lemma P with h2).
3. Two window candidates with the same s' and the same sign e2, at m and
   m + 1, don't both hit a corner. PROVED.

**Proof.** For 1, fold the part below y = d as in Lemma H. Above y = d the
segment lies in the strip d < y < d + h2. Fold it by the reflections in the
lines p + w Z and in y = e. The crossings with the side lines are at heights
other than e, so they're relative interior points of the corridor walls or
their mirror images. The crossing with y = e is at x_ell. It's a relative
interior point of the dead-end wall exactly when x_ell isn't a corner image,
which means x_ell isn't in p + w Z. The end point folds to T, because
2 e - (d + h2) = d + h. The folded part above the door stays in y > d, so it
doesn't leave E. Part 2 is Lemma P, because the T-images keep their
x-coordinates and only the height changes. For 3, moving from m to m + 1
moves x_ell by 2 w (D + ell) / (D + h2). Both hits would need
2 (D + ell) / (D + h2) to be an integer. It lies strictly between 1 and 2,
because h < ell. ∎

**What isn't proved.** The corner set of Lemma E isn't characterized. A
window candidate can hit a corner, and part 3 handles only windows that hold
two consecutive candidates. I expect the corner set to be a countable union
of proper hypersurfaces (GUESSED). In every test, the first window candidate
traced valid.

**Back-wall families B and BE.** If the viewer's channel ends behind S in a
full wall at y = c, the viewer has a second image depth D' = D + 2 (s2 - c).
Lemma P holds with D replaced by D', plus a corner condition at y = c (corner
images a + L Z). Its proof is the same as for Lemma E, part 1 (PROVED for the
window part). If the back wall has an opening, as with the chimney of type
122, validity also needs the back crossing to land on the wall part. That's an
open condition, not arithmetic.

## Application to the 10 door pairs

`door_geom.py` lists the Lemma H configurations of each door pair in all 8
frames and both orders (COMPUTED, `logs/door_geom.log`). Each pair has 2
configurations, mirror images of each other.

| Pair | Corridor of T is a dead end | Viewer channel's back side |
| --- | --- | --- |
| 119 (1,1)(3,5) | yes | full wall |
| 122 (1,3)(3,1) | yes | wall with an opening (chimney) |
| 122 (1,4)(3,1) | yes | wall with an opening |
| 1238 (1,5)(3,1) | yes | wall with an opening |
| 1238 (1,5)(4,1) | yes | wall with an opening |
| 971 (1,1)(3,5) | yes | full wall |
| 971 (1,1)(4,5) | yes | full wall |
| 971 (1,1)(5,5) | yes | full wall |
| 1275 (3,7)(5,3) | yes | wall with an opening |
| 719 (1,1)(3,5) | yes | full wall |

**Theorem D (door pairs, PROVED given the COMPUTED table).** For each of the
10 door pairs, S and T are lit for every real room of the type and every pair
of points of the position types, except on the set Z_H ∩ Z_E.

- Z_H: n1 = L h / (w D) is a positive integer, D > h, and both H-phases lie
  in B(beta, h / D).
- Z_E: either n2 = L (2 ell - h) / (w D) is a positive integer, D > 2 ell - h,
  and both E-phases lie in B(beta, (2 ell - h) / D); or every window
  candidate of Lemma E hits a dead-end corner.

For the 5 pairs with a full back wall, the window part of the residue also
needs the B and BE families to fail. That adds one more independent
integrality condition, L h / (w D') in Z (PROVED for the window part; the
corner parts are open).

**Exactly what remains.**

1. The double-resonance set Z_H ∩ Z_E^window. It has codimension 2 in the
   type region, and codimension 3 for the 5 pairs with a full back wall. It's
   nonempty for the 8 pairs where the design below fits. It contains points
   with w = 2^-12, so it reaches the thin face.
2. Lemma E's corner set inside Z_H, not characterized.
3. For 971 (1,1)(4,5), T lies on a grid line at h = ell / 2. So
   n2 = 3 n1 is an integer whenever n1 is. Here Lemma E gives nothing beyond
   Lemma H's resonance, and the back-wall families carry the load.

None of these sets is known to contain a dark pair. Every exact instance
tested is lit.

## Chains

**Model.** The route from S to T crosses door lines y = y_1 < ... < y_m. The
part of the route between consecutive door lines lies in a strip. A strip is
a full channel when both of its side lines are walls over its whole height.
Each full channel j of width w_j adds a free image index k_j with step 2 w_j.

**Lemma K (density for full-channel chains).** Suppose every strip of the
route is a full channel, including the strips of S and T. Let the unfolded
crossings be x = (x_1, ..., x_m), one per door line. Then the set of
reachable crossing vectors is c + Lambda, where Lambda is generated by one
vector per strip. If no nonzero linear functional takes integer values on all
generators, Lambda is dense in R^m. Then some candidate crosses every door
inside its window, and its folding is a valid path. PROVED: density is
Kronecker's theorem, and validity is Lemma H's folding argument applied strip
by strip.

**The count.** A route through m doors has m + 1 strips, so it has m + 1
indices for m windows. Kronecker density then holds off a resonance set of
codimension 1. On that set the closure of Lambda is V + (a lattice), and the
pair is lit if the window box meets c + closure. That's an inequality of the
same kind as Lemma P's. So the two-scale argument works for full-channel
chains, off a resonance set. It doesn't give "for all real parameters", for
the same reason Lemma H doesn't.

**Where the argument breaks.** It breaks at the first strip that isn't a full
channel, not at the second door as such.

- A hub with a cut corner (Lemma C+'s K condition) or a reflex vertex inside
  the hub: the folded segment can meet the vertex. The failure set is open in
  the lengths (r3.md's staircase example, type 4991 with V2 below the chord).
  No arithmetic choice of indices avoids an open set of bad slopes, because
  every candidate's slope lies in a narrow range set by the windows.
- A narrowing with a common wall (r3.md's "one-way jumps"): the junction door
  has one flat end and a full-period window of width 2 w2. The wide part is a
  full channel, so it still adds an index. The density argument survives
  there; the monotone argument of Lemma C doesn't. This is a correction to
  r3.md's diagnosis: the jump direction problem is specific to the
  intermediate-value method (GUESSED that density covers these cases off
  resonance; I didn't check the wall coverage in each of the 553 pairs).
- Two hubs joined by a corridor: one index serves two windows only when the
  hubs aren't full channels. With full-channel hubs the count is again
  m + 1 for m windows.

**What a chain lemma needs, precisely.**

1. A route whose every strip is a full channel. This is a combinatorial
   condition on the position types, not yet counted over the 553 chain pairs.
2. Non-resonance: no integer relation among the generator vectors, else the
   box-versus-closure inequality.
3. For routes that pass a non-full strip, a geometric condition like Lemma
   C+'s K condition, which fails on open sets of lengths. A different route
   is then needed, so the chain problem isn't only arithmetic.

## Tests

All checks use `fractions.Fraction`. The tracer `exact.trace` follows the
billiard path, rejects any vertex hit (convex or reflex), and requires an
exact end at T. Total CPU time is about 70 s, in one process at a time.

| Check | What ran | Outcome |
| --- | --- | --- |
| Tracer cross-check (`crosscheck.py`) | 5,868 candidates against d57's independent `replay.py`, including off-window neighbours | 0 disagreements; 2,690 valid |
| r3.md resonance example | type 122, direction (-1, 3) x 5 | 4 reflections, ends at T, as in r3.md |
| T1, thin corridor (`tests.py`) | 10 pairs, w = 2^-k, k = 1..12, generic lengths | 120 of 120 lit by a traced Lemma H path |
| T2, thin viewer gap | 10 pairs, D = 2^-k, k = 1..12 | 120 of 120 lit by a traced Lemma H path |
| Lemma P formula | every T1, T2, and T3 instance | agrees with exact window enumeration in all 284 |
| T3, single resonance | 22 instances, n = 2^(k-2), kappa = 1/16, beta = 1/20, k in {4, 8, 12} | H fails in 22 of 22, as predicted; E lights 20; the 2 others are 971 (1,1)(4,5) |
| T3, double resonance | 22 instances designed with ell = 2 h | H fails in 22; E also fails in 18, covering 8 pairs |
| Double-resonance follow-up (`double.py`) | 10 instances with k in {4, 8} | B lights 6; bounded image enumeration lights all 10 with 1 to 5 reflections |
| 22-wall dark pair (`check22.py`) | 8 frames x 2 orders | 0 Lemma H configurations |

**Reflection counts.** The shortest Lemma H candidate with |k| <= 8 doubles
with each halving of w. At w = 2^-12 it has 1,024 to 3,413 reflections (T1)
and 2,194 to 7,314 (T2). Lemma U's lower bound grows like w^(-1/2). The gap
comes from restricting |k|; shorter Lemma H paths use larger |k|.

**How the double-resonance instances are built.** Take L = 4, D = 16 h, so
kappa1 = 1/16, and w = 2^-k, so n1 = 2^(k-2). Set ell = 2 h, so h2 = 3 h and
n2 = 3 n1. Choose beta = 1/20. Then choose the door offset pi and the viewer
offset u with n1 u / L = 3/40 mod 2 and n1 pi / L = 7/40 mod 2. That puts the
H-phases at 1.90 and 1.75 and the E-phases at 1.70 and 1.25. All four lie in
their bad arcs [1.1125, 1.95] and [1.2375, 1.95]. This is a construction from
the formulas, not a search.

**The 22-wall dark pair.** Vertices R22 from `../d38-review/check_named.py`,
S = (0, 0), T = (2, 2). In 8 of the 16 frame-order cases the corridor point
isn't on the far side of the viewer. In the other 8, the viewer's channel is
[0, 4] or [8, 12] or [2, 10] in doubled units, and the door is [2, 10],
[0, 4], or [8, 12], so the channel never contains the door. Hypothesis 2 of
Lemma H fails, so Lemmas P, E, B, and K don't apply. The room is also a
lattice room, where every window family would be resonant at once.

## Assessment for 10 walls

| Kind | Pairs | Closed for all real parameters | Closed off an explicit set |
| --- | --- | --- | --- |
| Door | 10 | 0 | 10, off the double-resonance set and Lemma E's corner set |
| Chain | 553 | 0 | 0 proved; Lemma K applies only to full-channel routes, not counted |
| Collinear | 15 | 0 | 0; no thin corridor, and d57 closes 6 only on R(2, 4) |
| Total | 578 | 0 | 10 |

**Is "finite covering on a compact core plus a corridor-limit lemma" a
complete strategy?** No. Four gaps remain.

1. **Arithmetic sets that reach the faces.** Lemma H handles the thin faces of
   door pairs, but its exceptional resonance sets accumulate at those faces.
   A finite cover can't reach them there (Lemma U). The double-resonance set
   survives two families. A complete door argument needs either a family with
   no exceptional set or a proof that the exceptional sets of the available
   families can't all hold. The double-resonance instances were lit by
   chimney and back-wall bounces, which suggests the second route (GUESSED).
2. **Chains.** Lemma K covers only full-channel routes off resonance. Routes
   through cut hubs fail on open sets, so they need a different route.
3. **Points approaching walls.** Lemma P shows that resonant failures sit
   where T is within (1 - kappa) w / 2 of a corridor wall. As beta -> 0 the
   bad arc tends to length 1 - kappa, so this face is where the arithmetic
   gap concentrates. d57 doesn't cover the point-to-wall faces either.
4. **Other degenerations.** Long rooms (L -> infinity) make n large but don't
   remove resonance. Gaps that shrink without forming a corridor, such as a
   chimney width, aren't covered by Lemma U or by this memo, and nobody has
   probed them.

## Confidence

| Claim | Tag | Confidence |
| --- | --- | --- |
| Lemma P and Corollary CL | PROVED | High; it reproduces Lemma H and matches 284 exact enumerations |
| Lemma H applies to all 10 door pairs on the whole type region | COMPUTED | High; d17 classification, rechecked here |
| Lemma E, parts 1 to 3 | PROVED | High for 1 and 2; medium-high for 3 |
| Lemma E's corner set is small | GUESSED | Medium |
| Double-resonance set nonempty near the thin face | COMPUTED | High; exact instances at w = 2^-12 |
| Those instances are lit | COMPUTED | High for the 10 traced instances only |
| Lemma K | PROVED | Medium-high; a sketch, not checked numerically |
| Chain diagnosis (break at non-full strips) | Mixed | Medium; not counted over the 553 pairs |
| 22-wall pair outside the lemma | COMPUTED | High |

## Files

| File | Purpose |
| --- | --- |
| `exact.py` | Rooms with Fraction gaps, the exact tracer, canonical frames |
| `families.py` | Window candidates for H, E, B, BE; Lemma P failure formula |
| `build.py` | Door-pair instances in the canonical frame from target lengths |
| `door_geom.py` | Lemma H configurations, dead ends, and back walls of the 10 pairs |
| `tests.py`, `tests_lib.py` | T1, T2, T3 |
| `double.py` | Back-wall families and bounded image enumeration on double-resonance instances |
| `crosscheck.py` | Tracer against d57 `replay.py` |
| `check22.py` | Lemma H hypotheses on the 22-wall dark pair |
| `logs/` | Output of every run |

Every script runs with `python3 -B` from this directory and imports d57's
`tools/` and `replay.py` read-only.
