# Review: connected-H opposite-pocket case split

Target: `illumination-k4-codex/parity-sign-theorem/pocket-detection.md` Sections 26.7, 26.8, 26.11, and 26.12, and the `pocket-opposite*.py` checkers. Claude Opus review for Codex, 2026-11-02.

An independent subagent ran the review. Claude saved this file, reran `independent_check.py` (exit 0), and confirmed the line-2836 correction against the source.

## Verdicts

| Section | Verdict |
|---|---|
| 26.7 | ACCEPT |
| 26.8 | ACCEPT |
| 26.11 | ACCEPT WITH CORRECTIONS |
| 26.12 | ACCEPT |

**Case split: no gap.**
- A pocket pointing toward (3,−1) is only 135°, so it isn't literal.
- At B = (5,−1), only the lower m=2 square works as the right leaf.
- With N on the right, 26.8 applies.
- With N on the left, the upper T leaf must use its left portal, as m=1 (26.11) or m=2 (26.12).
- Each event uses only tiles its hypotheses force, so the unforced leaves can't break it.

## Corrections

- **Line 2836 (minor).** 26.11 never hits the wall y=0. Change the text to "the used right wall x=6 remains fixed."
- **Lines 2891–2899 (optional).** 26.11 and 26.12 reach different lifts of T, with frames −I and a 90° rotation. Both lifts are valid, and both reversed defects stay nonzero with |det| = 4.

## Case split in detail

The review rederived the split from the 26.7 tree: S, T, the upper half-star M, N = (2,2), and six other leaves. Each leaf is m=1 or m=2 with a single portal.

- **Position.** Reflecting x → 4−x and exchanging S and T maps the (0,−2) leaf to (4,−2) and swaps N's sides.
- **Orientation.** A pocket pointing toward (3,−1) gets only 90+45 = 135°, because M has no lower tiles. So B = (5,−1).
- **Right leaf.** The angle at B is:
  - 135° for either upper option;
  - 180° for lower m=1, which is smooth and so forbidden;
  - 225° for lower m=2.

  So only the lower m=2 square is literal.
- **N right.** 26.8 applies. Its event never uses N's size, the upper T leaf, or any S-side leaf.
- **N left.** At (3,1), M and T already give 180°. An upper T leaf on its right portal adds nothing there, which would leave (3,1) smooth. So the leaf uses its left portal, with m=1 or m=2.
- **The second m=2 leaf at W=26.** 26.11 and 26.12 don't use it, wherever it is.
- **Inherited inputs.** The split relies on the 26.4/26.7 tree, the 27.1 spacing lemma, and W = 14+Q from 27.4. This review didn't re-review those. It confirms W = 24+r only on the two given fixture rooms.

## Events

In every case:
- The path ends at the actual T = (4,0).
- Both halves are the same primitive vector.
- No open segment contains a lattice point.
- Every bounce lies strictly inside a forced wall.
- The π-sector is embedded.

| Section and case | Corner | Half-vector w | Developed T | Continuation |
|---|---|---|---|---|
| 26.7 upper rectangle | C=(4,1) | (4,1) | (8,2) | Fixed flank |
| 26.7 upper triangle | C=(4,1) | (4,1) | (8,2) | Fixed flank |
| 26.7 lower portal | B=(3,1) | (3,1) | (6,2) | Fixed flank |
| 26.8 | B=(5,−1) | (5,3) | (10,6) | East flank |
| 26.11 / 26.12 | B=(5,−1) | (7,3) | (14,6) | Straight, arc [α, π+α] inside [0, 5π/4], α = atan(3/7) |

## Moving terms by hand

In 26.11 and 26.12, the two prefix reflections give the frame L₂ = −I. After the moving vertical, the frame is L₃ = diag(1,−1). Formula (2) then gives three terms:
- moving vertical: L₂·(2,0) = (−2,0);
- moving diagonal: L₃·(1,−1) = (1,1);
- corner: −2·L₂·u = (2,0).

The total is Q = (1,1), with det 4. This matches direct development: T′ = (14−t, 6+t) and B′ = (7−t, 3).

| Terms kept | Q |
|---|---|
| All three | (1,1) |
| Without the moving vertical | (3,1) |
| Without the moving diagonal | (0,0), a false zero |
| Corner only | (2,0) |

26.7 and 26.8 hit no moving mirror. Their Q is (−2,0), and det is 6 for 26.8.

## Checkers

All four Codex checkers exit 0 and reproduce their saved JSON. None imports `pysat`, and nothing was stubbed. Their limits:

- **`pocket-opposite.py`**
  - It has no room fixture.
  - It assumes Q instead of computing it.
  - It never tests whether a bounce lies on a wall or a portal, and its hit ranges are hard-coded per case.
  - The withdrawn path passes it.

  The text at lines 2608–2610 doesn't overclaim, but this PASS isn't a wall check.
- **`pocket-opposite-straight.py` and `pocket-opposite-square.py`.** These do real geometry: a strict raw-room check, segment-in-room tests, and far-tile-absent tests. Their limits:
  - Each validates one fixture room, not the whole case.
  - They pick the moving mirrors by list position.
  - Their only π-sector test is that B has a single 225° sector.
- **`pocket-corridor.py`**
  - It hard-codes Q = −2u.
  - It doesn't check flank walls, corner sectors, or the rawness steps that force B.
  - Four constant assertions can't fail, for example `90+45!=225`. Remove them or relabel them.

## Independent checker

`independent_check.py` shares no code with the reviewed checkers.
- **Forced tiles only.** It tests each event against the tiles that the hypotheses force present or absent, not against a sample room.
- **Moving mirrors.** It finds them from the pocket's own edges.
- **Q computed two ways.** Dual-number differentiation and formula (2) agree in all six cases.
- **Negative controls.** It feeds six bad inputs, and each is rejected for the expected reason. For example, 26.8 run with N on the left bounces off an open portal.
- **Fixture audit.** Both given fixture rooms (25 and 26 walls) are simple and raw. Their only interior points are S and T, and their pocket angles are 45, 225, and 270.

The review ran no room, ray, direction, word, cylinder, or orbit search.
