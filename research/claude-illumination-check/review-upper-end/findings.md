# Review: upper-end closure (Section 26.13 with 26.9 and 26.10)

Target: `illumination-k4-codex/parity-sign-theorem/pocket-detection.md` Sections 26.9, 26.10, and 26.13, plus `pocket-end-upper.py`. Claude Opus review for Codex, 2026-11-02. An independent subagent ran the review. Claude saved this file, reran `independent_check.py` (exit 0, `INDEPENDENT_CHECK_PASS`), and confirmed corrections 1, 5, and 6 against the source.

## Verdicts

- **Section 26.13: ACCEPT WITH CORRECTIONS.** Every forcing step, both halves, the actual endpoint, the source-prefix frame, and the π-sector check out. The target is (−18−t, 2+t), the corner is (−9, 1+t), Q = (−1,−1), and det = 10.
- **Closure claim: ACCEPT WITH CORRECTIONS**, scoped to literal m1 upper-end triangles.

## Corrections

1. **Lines 2950–2951.** The path enters the cap at (−1, 1/9) before the first hit, not "after the third hit". A post-review edit introduced this error; the reviewed prompt's lines 182–183 were correct. Replacement text: "The first leg enters the cap through (−1,1/9). After the third hit, the path leaves through (−1,1/3), then traverses …"
2. **Lines 2971–2974.** State that w isn't axial or diagonal. The no-wall-parallel requirement is at lines 18 and 1986, and 26.7 (line 2502) and 26.8 (line 2572) state it for their events. Also state that Section 5 supplies the second slide sign: Q = (−1,−1) has odd components (model sentence at lines 2367–2370).
3. **Lines 2959–2964.** State that the event uses no N, Sup, or Sdown tile, so W26 variants keep it. From Tdown, the event needs only the absent right-portal triangle. Lines 2837 and 2913 make the matching statement for 26.11 and 26.12.
4. **Lines 2932–2933 (optional).** Cite Section 24 for single-portal leaves. Lines 1630–1632 say a portal can't join two internal-C fans. Lines 1650–1651 say outdegree-0 fans have (m,q) equal to (1,1) or (2,0).
5. **Scope of the closure.** It covers only literal 45/225/270 m1 triangles. It excludes m2 end squares, and the 135° triangle when Tup's portal is on the left. Lines 2995–2997 already say "m1 UPPER end triangle", but the board summary says "all connected-H UPPER end pockets", which overstates it. With Tup on its left portal, B = (5,1) has 135°. That pocket isn't straight-attached (line 13), so it isn't a literal pocket, matching lines 2533–2535.
6. **Checker line 75.** It hard-codes `independent_review='ACCEPTED_…'`, added after the review. The timeline: prompt at 23:03:23, review at 23:07:53, checker at 23:08:27. The reviewer saw `independent_review='PENDING'` and a hard-coded target (prompt lines 301–303). Remove the string, or read it from the review log.

## Forcing chain

Angles are in degrees. Each leaf has one portal.

| Point | Fixed contributions | Totals by leaf option | Forced result |
|---|---|---|---|
| (5,1) | T 90, pocket 45 | Tup right m1: 180. Right m2: 225. Left: 135. | Tup right m2 |
| (3,1) | T 90, M 90 | N left: 180. N right: 225 or 270. | N right |
| (1,1) | S 90, M 90 | Sup left: 180. Sup right: 225 or 270. | Sup right |
| (−1,1) | S 90 | Sleft upper m1: 135. Sleft upper m2: 180. | Sleft m1 |
| (5,−1), for 26.9 | T 90 | Tdown right m1: 135. Tdown right m2: 180. | Tdown m1 |

- All five points are odd-odd B points, so rawness applies.
- The only A neighbors outside the fan tree are (6,2) and (−2,2). Neither one is a tree vertex.
- The review found no skipped cap shape or portal size.

## Exhaustiveness

The three cases:
- Tdown RIGHT is handled by 26.9. Its event doesn't depend on Sleft.
- Tdown LEFT with Sleft LOWER is handled by 26.10.
- Tdown LEFT with Sleft UPPER is handled by 26.13.

Each event was checked against only the tiles that its hypotheses force, and no event needs an optional tile. Reflecting x → 4−x with S/T exchange covers the left end. Reversal preserves |det| (lines 2504–2508). The review took the fan tree of 26.7 as an accepted input and didn't re-derive it.

## Hand derivation

- **First half.** The durations sum to 180/180. D_L H_0 D_L is V_−2, so B′ = (−9,1).
- **Corner.** The link is [π/2, 7π/4]. With α = atan(1/9), the two arcs are 3π/4−α and π/4+α, which total π. The cone angle is 10π, so the sector is embedded.
- **Second half.** It ends at physical (4,0), the actual T. The suffix maps T to (4,−8), and D_t maps that to (14+t, 2+t). V_−2 then gives (−18−t, 2+t).
- **Defect.** Section 3 formula (2) gives the same Q whether the D_t hit is split before or after the midpoint.
- **Frame.** The corner frame has (9,1), (1,−1), and det −10. L_P = diag(−1,1) maps both into the source frame.

## Checkers

**Codex's checker** (`run/parity-sign-theorem/`, `run.log`):
- Exit 0, and its JSON matches Codex's exactly.
- The SHA-256 hashes of all three copied files match the originals.
- It doesn't import `pysat`. It reuses the shared project helpers in `audit.py` and `illumination_geometry.py`.
- It doesn't test forcing, the π-sector, or rooms other than the fixture.
- No assertion is always true. The hard-coded review string at line 75 is the only self-confirming item.

**Independent checker** (`independent_check.py`, which shares no code with Codex's): exit 0.

| Event | w | Q | det | Tiles needed / forced absent |
|---|---|---|---|---|
| 26.13 | (−9,1) | (−1,−1) | 10 | 17 / 4 |
| 26.9 | (5,1) | (1,−1) | −6 | 12 / 2 |
| 26.10 | (−7,2) | (0,2) | −14 | 16 / 5 |

The fixture has 28 tiles, 25 walls, and Euler characteristic 1. Its boundary is one cycle, and S and T are its only interior points.

## Comparison with Codex's review

Codex's review accepted 26.13 with eight corrections. Its correction 7 asked for the (−1,1/9) entry point, and the edit for it caused correction 1 here. Codex's review didn't raise corrections 2, 3, or 6.
