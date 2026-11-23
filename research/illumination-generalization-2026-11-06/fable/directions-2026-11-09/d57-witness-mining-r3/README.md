# Witness mining for rooms with 3 reflex corners

Date: 2026-11-18. Direction d57. Notation follows `../d15-small-r/theorems.md`
and `../d17-r3/r3.md`.

## Results

- **The 10-wall theorem isn't proved.** None of the 578 open position-type
  pairs is closed on its full region of real parameters. All 578 stay open.
- **563 of the 578 pairs can't be closed by any finite set of itineraries.**
  This is PROVED by Lemma U, which follows, together with a combinatorial count
  (COMPUTED, `thin_corridor.py`). It covers all 553 chain pairs and all 10
  door pairs. Each has a thin-corridor degeneration where every lighting path
  needs at least 2 sqrt(d h / (H w)) - 2 reflections, with w -> 0.
- **The 15 collinear pairs have no such degeneration.** On the compact
  truncated region R(2, 4), 6 of them are closed by certified boxes (COMPUTED).
  The other 9 are 45% to about 100% covered at the 60 s cap (COMPUTED
  estimate). Two of them hit all 100 sample points but still have uncovered
  boxes.
- **Nothing is closed at a wider truncation.** At R(4, 8) with 25 s per pair,
  no collinear pair closes. Covered fractions are 0% to 78%.
- **Witness complexity grows like w^(-1/2) at thin corridors.** For example,
  in chain type 4991 the shortest path found needs 26 reflections at w = 1/256.
  At collinear type 125 it stays at 1 reflection under 3 degenerations.
- **Sanity passes.** No box that contains the dark pair of the 22-wall room is
  certified. All 307 itineraries valid in nearby rooms fail at the dark point.
- **Soundness checks pass.** The certifier accepted nothing that the
  independent replay rejected. That covers 3,295 point checks and 57,195 replays
  of certified boxes.

| Kind | Pairs | Lemma U applies | Truncated R(2, 4) closed | Truncated R(2, 4) partly covered |
| --- | --- | --- | --- | --- |
| Collinear | 15 | 0 | 6 | 9 |
| Door | 10 | 10 | 0 | 10 |
| Chain | 553 | 553 | 0 | 553 |
| Total | 578 | 563 | 6 | 572 |

Closed on R(2, 4) means: every two real interior points of the pair's
position types are lit in every room of the order type whose gaps lie in
[g/2, 2g], where g is the first x-gap. Each odd point coordinate must also lie
at least a quarter gap from both grid lines of its gap. The six pairs are
`125 (1,2)(5,2)`, `889 (1,4)(5,4)`, `892 (1,4)(5,4)`, `1695 (2,1)(2,7)`,
`7672 (1,4)(7,4)`, and `8115 (1,4)(7,4)`.

The per-pair table is `results_r3.tsv`.

## Method

### Parametrization

- Order types and position types are those of d15. The open list is
  `tools/cert_r3.json`. The kinds come from d17's `classify.py`
  (`tools/kinds.py` writes `kinds_r3.tsv`, which reproduces 15 / 10 / 553).
- Parameters are the grid gaps gx0, ..., gy0, ... (all > 0). Each odd point
  coordinate adds one offset from the lower grid line of its gap, with
  0 < offset < gap. An even coordinate equals its grid line.
- Every coordinate of the room, of S, and of T is a linear form with integer
  coefficients in these parameters. Scale is fixed by gx0 = 1.
- The type region is the open set {gaps > 0, 0 < offset < gap}, of dimension
  7 to 11. The truncated region R(D, dp) is the compact part with every gap in
  [1/D, D] and every offset in [gap/dp, gap (1 - 1/dp)].

### Itinerary validity

An itinerary is the sequence of maximal walls that a path hits. Its unfolded
end point T* is a linear form, by composing the wall reflections. The path is
valid exactly when these conditions hold.

1. T* - S has both components nonzero, with fixed signs.
2. The hit times along S -> T* increase strictly.
3. Each hit lands strictly inside its wall.
4. On each leg, every other wall of the current room copy is missed. Either
   its line is crossed outside the leg's time interval, or the crossing lies
   strictly outside the wall's closed extent.

Each condition is sign * (sum of products of two linear forms) > 0. Condition 4
is a disjunction of 4 such alternatives. Wall ends are vertices, so condition 4
also forbids every vertex. Walls on the line of the current or previous hit
are skipped, because the leg meets that line only at the hit point.

### Certification on boxes

- Box endpoints are dyadic rationals, stored as integers on the scale 2^24.
- A condition holds on a closed box when one alternative is positive on the
  whole box. The check first uses naive interval products, then a mean-value
  form: f(c) plus the gradient range times the half-widths. The gradient of a
  quadratic is linear, so its range is exact. All arithmetic is exact integer
  arithmetic.
- A box is certified when it lies in the open type region and one itinerary
  passes. Then every real point of the closed box is lit by that itinerary.
- The branch-and-bound driver (`bb.py`) works breadth-first. It reuses the
  centre-valid itineraries of the parent box. It mines new ones by float ray
  shooting only when none is valid at the centre. It splits along the variable
  that contributes most to the failing condition.
- Floats are used only for discovery: the shooter, and the re-trace that sets
  the true hit order. Every validity claim comes from the exact certifier.

### Independent replay

`replay.py` builds walls from unit cell edges with d15's
`raycast.wall_segments`, not from the maximal walls of `wm.py`. It follows the
billiard path from S with velocity T* - S in Fractions. It accepts only if the
path touches no vertex and ends exactly at T. For every closed pair, each
certified box was replayed at 4 random vertices and 1 random interior point.

### Boundaries and resonances

- **Inside a truncated region, resonances are covered.** The boxes are
  closed, and their union is all of R(D, dp). So the certificate includes every
  measure-zero set inside it, such as the resonance set of Lemma H.
- **Type boundaries aren't covered.** These are points on a grid line, gaps
  -> 0 or infinity, and offsets -> 0 or gap. Points on a grid line belong to
  other position types, which have their own certificates or open entries.
- **The limits gap -> 0, gap -> infinity, and point -> wall aren't
  covered.** A closed box can't contain such a face, because the conditions
  fail there. A full closure needs a separate argument at each face; see
  [What would close the rest](#what-would-close-the-rest).

## Lemma U (thin corridors force many reflections)

**Statement.** Let E = [p, p + w] x [c0, c1] lie in P, with both sides
{p} x [c0, c1] and {p + w} x [c0, c1] in the boundary of P. Let T be interior
to E, at distance h > 0 from each end of E that isn't a wall. Let S lie at
horizontal distance d > 0 from the strip p <= x <= p + w. Let H be the height
of P. Then every billiard path from S to T has at least
2 sqrt(d h / (H w)) - 2 reflections.

**Proof.** Let the path have direction angle phi, so |tan phi| is constant.
Its total horizontal travel X is at least d, so its vertical travel is
V = X |tan phi| >= d |tan phi|. Between two reflections on horizontal walls,
y is monotone in [0, H]. So there are at least V / H - 1 horizontal-wall
reflections. The path enters E only through an open end, and it then travels
vertically at least h to reach T. In that final part, its horizontal travel
is at least h / |tan phi|. Between vertical-wall reflections inside E, x is
monotone in an interval of length w. So there are at least
h / (w |tan phi|) - 1 vertical-wall reflections. Add the two counts and use
a + b >= 2 sqrt(a b). A horizontal path (tan phi = 0) can't enter E, and a
vertical one can't cover d > 0. ∎

**Consequence (PROVED).** Suppose a pair has such a corridor whose columns can
shrink while d, h, and H stay fixed. Then any finite itinerary set fails on
rooms with small enough w, so no finite set covers the type region.
`thin_corridor.py` checks the hypothesis on position types. The corridor must
contain the point strictly inside, and the other point's index range must miss
the corridor's closed column range. The check also allows S and T swapped and
the axes swapped. It holds for 563 of 578 pairs and fails for exactly the 15
collinear pairs. The witnessing corridor is in `results_r3.tsv`.

**Limiting room.** As w -> 0, the corridor becomes a slit, and the point in it
sits on the slit. This isn't a strictly simple room of the same type. A limit
argument must therefore be a parametric family with an image index m ~ 1/w,
not a finite witness. Lemma B (flat door end) and Lemma H (channel, off the
resonance set) are families of this kind. They fail on exactly these open
pairs. For door pairs, a family argument near the face looks plausible
(GUESSED). For chains, r3.md records that the one-way jump argument breaks
after a second door, so no candidate is known.

## Degeneration study

`degen.py` shrinks one gap, or a group of gaps, by eps = 2^-k with all else
fixed. Every gap is 1 and every offset is a half gap. At each eps it reports
two quantities. The first is the shortest itinerary that passes the exact
check and the replay. The second is the witness radius: the largest rho = 2^-j
such that a mined itinerary is certified on the box of relative half-width rho
around the point. COMPUTED. Mining stops at 40 reflections.

| Study | 1/eps = 1 | 4 | 16 | 32 | 64 | 128 | 256 | Lemma U bound at 256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Door 122, tab width | 1 | 1 | 2 | 3 | 5 | 7 | 11 | 8 |
| Door 122, bar height | 1 | 1 | 2 | 3 | 5 | 7 | 11 | 5 |
| Chain 4991, column 0 width | 1 | 2 | 6 | 8 | 13 | 18 | 26 | 16 |
| Collinear 125, gx1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | none |
| Collinear 125, gy1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | none |
| Collinear 125, all but gx0 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | none |

- For the thin-corridor studies, the count grows by about 1.4 per halving of
  eps. This matches the w^(-1/2) rate of Lemma U, and each count is at or
  above the bound.
- The witness radius shrinks from 2^-3 or 2^-4 to 2^-6 or 2^-8. A cover of
  dimension 9 to 11 then needs about rho^(-dims) boxes near the face.
- For collinear type 125, the radius stays at 2^-3 under all three
  degenerations. The single reflection is off the top of the bar, or off the
  chimney top when gx0 dominates.

## Pilots

- **Door type 122, pair (1,3)(3,1), 9 dimensions.** R(2, 4) is 21% covered
  after 182,497 boxes and 60 s. 11 itineraries were used, with at most 4
  reflections. The 1.5 s batch run reached 3%.
- **Chain type 4991, pair (1,7)(7,1), 11 dimensions.** No box was certified at
  the 1.5 s cap. An earlier 20,000-box depth-first run certified 6,476 small
  boxes with 9 itineraries of at most 3 reflections. Coverage stayed near 0%.
- **Collinear type 125, pair (1,2)(5,2), 7 dimensions.** R(2, 4) is closed by
  778 boxes and 5 itineraries, with at most 4 reflections, in 0.5 s. It's
  78% covered at R(4, 8) after 25 s.
- **All 563 door and chain pairs, 1.5 s each.** None closed. The mean covered
  fraction is 2%, and 520 pairs are at 0% by a 100-point estimate.

**Itinerary statistics on R(2, 4) (COMPUTED).** Consider the longest
certified itinerary per pair, over the 236 pairs with at least one certified
box. It has 0 reflections for 2 pairs, 1 for 12, 2 for 42, 3 for 85, 4 for
66, 5 for 22, 6 for 2, 7 for 3, and 8 for 2. The float miner was capped at 12
reflections, and every door and chain pair's pool reached that cap.

**Uncovered part of the 9 open collinear pairs.** `unc_probe.py` probed 400
uncovered boxes of pair 891 (1,4)(5,4). Every probed centre has a valid path
of 2 to 4 reflections. The one-bounce point (s1 + t1) / 2 is 0.25 to 0.56 of
the smallest gap away from every grid line. So the remainder isn't near a
degeneration or near a wall end. Within R(2, 4) it's a box-count limit, not a
structural obstacle (COMPUTED, for this pair only).

## Sanity: the 22-wall dark pair

`sanity22.py` uses vertices R22 from `../d38-review/check_named.py` with
S = (0, 0) and T = (2, 2). The room has 22 walls and 15 cells. Both points lie
on grid lines, so the parameters are the 11 free gaps, and the dark pair is
at all gaps = 1.

- At the dark point, mining with 8,000 rays and up to 20 reflections found no
  candidate. No itinerary passed the exact check.
- In 20 rooms with gaps perturbed by up to 2%, 307 itineraries passed the
  exact check. All 307 fail the exact check at the dark point, and all 307 fail
  the replay there.
- None of the 307 certifies on any box [1 - 2^-k, 1 + 2^-k]^11, k = 1 to 20.
- A 6,000-box cover of [1 - 2^-6, 1 + 2^-6]^11 certified 1,521 boxes. None
  contains the dark point; 43 uncovered boxes do.

## What would close the rest

- **Collinear pairs (15).** Witness complexity looked bounded in the probes.
  A face certifier could treat the faces: substitute gap = eps g or
  offset = eps g, and require the leading eps-coefficient of each condition to
  be positive on a box. It could then certify boxes that touch the faces.
  Together with gap-ratio charts that make the region compact, this could
  close the collinear pairs (GUESSED). No probe was run at the point -> wall
  faces.
- **Door and chain pairs (563).** Lemma U rules out finite witnesses. Each
  pair needs a family argument at its thin-corridor face, with finite mining
  only away from that face. The residue is then the region away from all faces
  plus the faces themselves. The pilots show that even the compact part costs
  about 10^6 boxes per pair in 9 to 11 dimensions with this certifier.

## Cap use

- CPU time: about 42 minutes in total. That includes 2 minutes in one early run
  that hung in a sampler and was stopped. The largest items are the
  door-and-chain batch at 14.6 minutes, the 60 s collinear runs at 9.4
  minutes, and the R(4, 8) runs at 6.3 minutes.
- At most 3 compute processes ran at a time.
- Disk: about 530 KB for the whole directory.
- RAM wasn't measured. The largest run processed 182,497 boxes and kept a
  frontier of at most that size. The estimate is under 300 MB (GUESSED).

## What isn't verified

- The correctness of the condition derivation in `wm.py` isn't proved. It's
  supported by agreement with the independent replay: 0 certifier-accepted,
  replay-rejected cases in 3,295 point checks (`crosscheck.py`), 127 in
  `test_tiny.py`, and 57,195 replays of certified boxes. The 181
  replay-accepted, certifier-rejected cases all have a different hit order
  with the same T*. The certifier fixes the order; the replay doesn't.
- Replays sample 5 points per certified box, not every vertex.
- The covered fractions of partly covered pairs are 100-point Monte Carlo
  estimates under a log-uniform gap measure.
- Lemma U is a hand proof, not machine-checked. The combinatorial hypothesis
  check is a 60-line script.
- The theorems of d15 and d17 and the darkness of the 22-wall pair are taken
  from those directions.

## Files

| File | Purpose |
| --- | --- |
| `wm.py` | Order type, parameters, itinerary conditions, interval certifier, float miner |
| `bb.py` | Branch-and-bound cover of R(D, dp) |
| `replay.py` | Independent exact replay and box replay |
| `run_cover.py`, `batch.py` | Single-pair and sharded cover drivers |
| `thin_corridor.py` | Lemma U hypothesis check; writes `thin_corridor_r3.tsv` |
| `degen.py` | Degeneration study |
| `unc_probe.py` | Probe of uncovered boxes |
| `sanity22.py` | 22-wall dark-pair sanity check |
| `crosscheck.py`, `test_tiny.py` | Certifier against replay |
| `assemble.py` | Builds `results_r3.tsv` |
| `kinds_r3.tsv` | Kind of each open pair, from `tools/kinds.py` |
| `tools/` | Copies of `raycast.py`, `cert_r3.json`, `classify.py`, `newlemmas.py`, `rooms.py` |
| `logs/` | JSON-lines output of every run |

Every script runs with `python3 -B` from this directory.
