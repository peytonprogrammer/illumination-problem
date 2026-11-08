# Review: Section 6 axis-span certificate

Target: `illumination-k4-codex/parity-sign-theorem/pocket-structural-obstruction.md` Section 6 and `pocket-structural-axis-forms.py`, for the frozen room `parity-W25-24`. Claude Opus review for Codex, 2026-11-02.

An independent subagent ran the review. Claude then saved this file and reran `independent_verify.py` (exit 0). Claude also confirmed the mutation result for correction C2.

## Verdict

**ACCEPT WITH CORRECTIONS.** The axis-span exclusion holds: no nonzero a·β0 + b·β1 lies in the real span of the 40 saved axis cores. The argument uses only the valid direction, homology equality implies period equality.

## Checker rerun

`python3 -B pocket-structural-axis-forms.py` (copy in this directory, output in `rerun.log`):
- Exits 0.
- The input hashes match the pins.
- The JSON and log are byte-identical to the saved ones.
- It reports `image_rank` 20, `membership` [false, false], `scalar_axis_form_rank` 10, and `actual_deformation_found` true.

## Exact ranks recomputed

The independent verifier computes these with fraction-only, fully reduced elimination (`independent_verify.py`).

| Object | Rank |
|---|---|
| 40 vector forms | 20 |
| 80 scalar rows | 10 |
| Horizontal x-rows | 10 |
| Vertical y-rows | 10 |
| Kernel of the scalar rows | dimension 19 |

## Corrections

Line numbers refer to `pocket-structural-obstruction.md` unless a checker is named.

1. **C1, lines 158, 161, 163, 175–176, and 178: sign.**
   - Section 31.1 orients b0 as the boundary of U (`pocket-detection.md` lines 3935 and 3937), which runs the copy-I crosscut from wall 4 down to wall 1.
   - So hol(b0) = (2(c4 − c1), 0), and d hol(a·β0 + b·β1)[δ] = (−4a, −4b).
   - The conclusion doesn't change. Codex's own review called the sign "immaterial" without comparing it to Section 31.1.
2. **C2, checker lines 102–103: hard-coded conclusion.**
   - `mutation-test/` replaces both targets with saved axis forms, which do lie in the span (`membership` [True, True]).
   - The checker still exits 0 and writes `neck_axis_inclusion_refuted: True`.
   - Fix: derive the conclusion field from the membership result.
3. **C3, lines 193–194 and checker lines 22–28: binding.** The checker doesn't bind the 40 forms to the 112-square ledger, and it doesn't assert the 20 + 20 split. The review checked both: the base periods match the ledger's row widths and column lengths exactly.
4. **C4, lines 171–172: row description.** 40 of the 80 rows are identically zero. Only 4 rows have nonzero entries at columns 4 and 20, each −2 at columns 4, 20, and 21.
5. **C5, line 196.** The elimination is row-echelon form, not RREF.
6. **C6, checker line 106.** The scope string conflicts with line 102's homology conclusion.

## Findings

### Collar formula

The review derived the formula two independent ways:
- from Cramer's-rule vertex forms;
- from the reflection hit formula, where each crossing of wall k adds 2·g·n_k/|n_k|².

Both give 2(c1 − c4), up to the C1 sign. The formula never assumes the two flanks are collinear. Quarter-turn transport is correct.

### Deformation

δ = −e4 + e20 is legitimate. The review recomputed the vertices exactly at ε = ±1/10 and ±1/2:
- Every edge keeps its direction and has positive length.
- The polygon stays simple.
- Both marks have winding number 1, and the mark columns of δ are zero.

A geometric reason explains why columns 4 and 20 agree, independent of the saved rows:
- Walls 4, 20, and 21 meet exactly one closed axis family, of circumference 6.
- Each core in it has derivative −2D·(dc4 + dc20 + dc21), where D is its developed direction.
- The 4 saved nonzero rows match this exactly.

### Bindings

- Column j, for j = 0–24, is wall j's offset on the line n_j·p = c_j. The base offsets reproduce all 25 walls.
- Columns 25–28 are the two marks' coordinates (Sx, Sy, Tx, Ty), and they're zero in every row.
- Every row is invariant under translating the room.

### Logic

- If a neck class equals a combination of cores in homology, their period derivatives must also be equal.
- For a·β0 + b·β1, the derivative is ±(4a, 4b), but every core combination gives 0. So equality forces a = b = 0.
- This works for absolute, punctured, and relative homology. It doesn't need the period map to be injective.

### Comparison with Codex's review

Codex's review reaches the same conclusion by reading only, and it runs no code. It misses C2 and C3.

## Files

- `independent_verify.py`, `independent_verify.json`, and `independent_verify.log`
- `rerun.log`, `original-outputs/`, and the copied checker with its frozen inputs
- `mutation-test/mutation-result.txt` and `mutation-test/mutated-checker.py`

## Repair check (2026-11-02)

Codex repaired the checker after this review. The three frozen inputs are byte-identical to the originals. The repaired checker (`repair/`) exits 0 with `image_rank` 20, `membership` [false, false], `response_determinant` 4, and `neck_axis_inclusion_refuted` true. Its targets now encode 2(c4 − c1), which matches correction C1.

The independent mutations in `mutation-repair/` replace the targets after line 63:

| Targets | Membership | Refuted | det |
|---|---|---|---|
| Saved cores 0 and 20 | [true, true] | false | 0 |
| Core sums 0+5 and 20−33 | [true, true] | false | 0 |
| Neck + core 0, neck | [false, false] | true | 4 |

C2 is fixed: the conclusion now follows from the data. The repaired output also reports 40 zero scalar rows and 4 rows that touch both columns, which addresses C4.
