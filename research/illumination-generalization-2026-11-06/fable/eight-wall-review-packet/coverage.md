# Coverage ledger

Each row names a shape, a placement of the two interior points, the guard
that is needed, and where `theorem-and-proof.md` handles it. "L(v)" and
"L(h)" mean the vertical-only and horizontal-only paths of Theorem 2.1 in a
named L subroom.

## Shapes

| W | Shape | Normal form | Illumination |
| --- | --- | --- | --- |
| 4 | rectangle | Prop 1.2 | convex |
| 6 | L | Prop 1.2 | Cor 2.3 |
| 8, k=1 | U | Prop 1.2 | Thm 3.2 |
| 8, k=2 | staircase | Prop 1.2 | Thm 6.11 |
| 8, k=3 | T, independent floors (u = v included) | Prop 1.2 | Thm 4.1 |
| 8, k=4 | wide-middle offset corridor (a > B included) | Prop 1.2 | Thm 5.2 |

Classification: Prop 1.1 (c - r = 4) and Prop 1.2 (one turn word per k;
positivity gives the inequalities; k = 4 simplicity and the b < c
normalization).

## Placements and guards

| Shape | Placement | Mechanism | Guards |
| --- | --- | --- | --- |
| L | same rectangle, incl. seam points | direct | none |
| L | cross-arm | Thm 2.1, images E, q in (0, a) | contacts strictly between heights; (a, c) avoided by q < a |
| L | source on base (used only when the base is an internal seam) | Lemma 2.2 | same as Thm 2.1 |
| U | same arm column | direct | none |
| U | both y <= c, one y < c | direct in bottom rectangle | seam points interior over open mouths |
| U | both y = c, opposite mouths | Thm 3.1 with y_s = y_t = c | L = L_0, R = R_0, no arm contacts |
| U | opposite arms, y > c | Thm 3.1 | l_s < 2a, l_t < 2b (fixed point not a jump); u, v in (0, c); floor contact in (M/2, A - M/2); earlier inner-wall contacts above c |
| U | one high arm, other y < c | L(v) in Q = bottom + that arm | artificial top over the other mouth avoided; (a+M, c) or (a, c) smooth on it |
| T | same wing or stem | direct | segments along x = a, x = b interior |
| T | stem and a wing | L(h) in Q_L or Q_R | artificial vertical cut and reflex corner on it avoided |
| T | opposite wings, y_s >= v (u <= v) | direct in [0,A] x [v,C] | open segment above v |
| T | opposite wings, u < y_s < v | L(v) in Q = ([0,A]x[v,C]) U ([0,b]x[u,v]) | artificial bottom over (a, b) and (a, u) avoided |
| wide-middle | both y < c | L(v) in Q_low | artificial top over (a, A), (a, c) smooth, avoided |
| wide-middle | both y > b | L(v) in Q_up | artificial bottom over (0, B), (B, b) smooth, avoided |
| wide-middle | lower arm and upper arm | Thm 5.1 (rotation to B >= W) | (5.2), (5.3); seam points avoid (B, b), (a, c), (0, c); y strictly increasing |
| wide-middle | seam y = b and seam y = c | direct | open part strictly inside middle rectangle |
| wide-middle | lower arm and seam y = c | Lemma 2.2 in reflected Q_low | base point interior to P |
| wide-middle | seam y = b and upper arm | Lemma 2.2 in reflected Q_up | base point interior to P |
| staircase | both y < d | L(v) in Q_low | artificial top over (0, a), (a, d) smooth, avoided |
| staircase | both x < b | L(h) in Q_up | artificial right cut over (0, c), (b, c) smooth, avoided |
| staircase, F | cross, y_t > d | Thm 6.5 | (6.1), (6.2) with H_s'; two images; floor contact not in AZ |
| staircase, F | cross, y_t = d | Thm 6.6 | q in (0, b); target not a fold point |
| staircase, Rv | cross incl. x_s = b and y_t = d | Thm 6.8 | (6.1), (6.2); L > 2a; roof contact smooth or earlier arrival |
| staircase, Ft or Rh | all | transposition | isometry |
| staircase, any metric | all | Prop 6.10 | algebra, strict |

## Degeneracies handled explicitly

Listed in Section 7 of `theorem-and-proof.md`: seam endpoints, smooth-wall
contacts at seam heights (z = 0, w = 0), reflex corners at seam ends, convex
floor and roof corners, target reached early, rounding ties, equality in F
or Ft.

## Dependencies on accepted sources

Every lemma and theorem in `theorem-and-proof.md` is restated and proved in
the note itself. The provenance of each argument is listed in
`dependency-manifest.json` with the SHA-256 of the source file and of the
acceptance record. The chain is:

- classification: `review/eight-wall-frontier.md`, accepted with independent
  reconstruction;
- L: `illumination-k4-codex/single-boundary-blocker/l-monotone-proof.md`,
  accepted historically and re-derived in
  `review/all-real-L-dependency-review.md`;
- U: `illumination-k4-codex/two-reflex-blocker/all-heights.md`, re-derived in
  `review/all-real-U-dependency-review.md`;
- T: `review/uneven-T-theorem.md`, accepted with `construction/T-whole-review.md`;
- wide-middle: `review/wide-middle-onepass.md`, accepted with
  `construction/wide-middle-review.md`;
- staircase: window, roof, floor proofs and their reviews, then
  `review/whole-staircase-candidate.md` accepted by two reviewers
  (`review/whole-staircase-acceptance.json`, reviewer Codex01a1a00f;
  `construction/whole-staircase-independent-review.json`, agent Codex01a18403).

The overlap supplement (`construction/staircase-overlap-supplement.md`) and
the roof theorem's two-image selection are accepted but not needed by the
final chain; the note omits them.

## Unresolved issues

The packet author found no gap in the chain while re-deriving it. The
following are soft points that deserve a referee's attention; none is a
known error:

1. Theorem 6.8 Step 4 is the newest argument (2026-11-07) and has had the
   least review time: two AI reviewers plus the packet author.
2. Lemma 2.2 (source on the base of an L) was accepted as Section 5 of the
   wide-middle proof rather than as a separate statement. Theorem 6.6 uses
   the mirror version (target on the top of a narrow arm) and was accepted
   inside the floor proof.
3. Theorem 3.1 originally stated finiteness of the set of (L, R) values on a
   bounded slope interval without an explicit iteration bound. The subsequent
   referee addendum derives a finite index-consumption bound and an explicit
   room-dependent reflection bound for opposite-arm pairs. Both are now in
   the proof. This resolves that exposition concern; no uniform bound over
   all metrics is claimed.
4. The convention that a path may pass through S or T at intermediate times
   is used in Theorem 6.5 (the path may revisit S) and in truncations. A
   referee who requires first-passage at T can truncate; a referee who
   forbids passing through S again would need a separate argument, which the
   sources do not provide.

## Review limits

- All review is by AI agents (Codex and Claude) working from the same shared
  sources. No human mathematician has read these proofs.
- No statement is formalized in a proof assistant.
- The check scripts evaluate fixed rational inputs and symbolic polynomial
  identities. They are controls on the formulas, not proofs for arbitrary
  real parameters.
- The earlier search-based censuses that preceded these proofs (wide-middle
  Section 7 of the source) are not part of the argument and were not rerun.
- Unrelated earlier drafts by the packet author on general covering and
  spiral arguments (`fable/general-geometry-0*.md`) received reviewer
  findings F1 to F16. F1 to F10 were corrected; F11 to F16 remain
  unresolved. This packet does not use any of that material.

## Coordinator review corrections

A subsequent independent AI hand review checked the complete written chain,
with particular attention to roof-corner truncation, metric exhaustion, L seam
endpoints, U fixed-point termination, and classification. It found and corrected
a missing factor in the printed partial-window bound (the corrected bound follows
directly from Lemma 6.3), an omitted U high/seam case already covered by
Theorem 3.1, overly strict contact-height and seam-coordinate descriptions, and
a six/eight-edge typo. The proof-check runner now propagates Python failures.
No frozen research proof or historical acceptance receipt was edited. See
`../../coordination/general-proof-priority/final-review/eight-wall-review.md`.
This is additional AI hand review, not external refereeing or formal verification.

The mathematical referee addendum also supplies the U normal form's omitted
strict-simplicity argument for c>0. Positive edge lengths alone do not imply
this inequality. The theorem's admitted metric set is unchanged.
