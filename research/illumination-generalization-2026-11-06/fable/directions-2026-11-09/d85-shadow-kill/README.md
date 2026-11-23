# D85: shadow-budget kill test

**Verdict: not killed.** In every named room with a nonzero area range, |H_L(S)| is 0 at L = 2·diam, 4·diam and 8·diam. It doesn't grow with area at fixed r. The only nonzero counts are in the R22 control (|H| = 2, r = 9) and in R22-L1-005 at L = 2·diam (|H| = 1, gone by 4·diam). The largest |H_L|/r observed at L ≥ 2·diam is 2/9 ≈ 0.22 (R22).

## Method

- `shadow.py` enumerates every displacement D = (Dx, Dy) with both components even and |D| ≤ L. It traces the billiard path from S with unfolded displacement D in exact integer arithmetic. Crossing times i/|Dx| and j/|Dy| are compared as i·|Dy| vs j·|Dx|.
- A path is illegal when it touches a convex or reflex corner, or runs along a wall. The endpoint must be interior or smooth.
- Every legal path from S to a same-parity lattice point unfolds to one such D, so the disk enumeration is complete for length L.
- Targets: interior and smooth-wall lattice points with the parity of S, excluding S itself.
- diam: the largest distance between two corners of the room. L values are rounded to integers.
- `validate.py` compares `shoot` with `d8-perturbation-test/tracer.py` (Fractions) on 2400 random displacements in six room/source pairs. Result: 2400/2400 agree, 1375 legal ([validate.log](validate.log)).
- Total CPU: about 9 s.

## Results

| Room | Area | r | Classes | S | Targets | L (2, 4, 8 × diam) | \|H_L\| |
|---|---|---|---|---|---|---|---|
| R22 | 15 | 9 | 1 | (0,0) | 3 | 13, 25, 51 | 2, 2, 2: {(2,−2), (2,2)} |
| R22-L1-005 | 16 | 8 | 2 | (0,0) | 4 | 13, 27, 54 | 1, 0, 0: {(2,2)} at L=13 |
| U2 k=0 | 46 | 3 | 4 | (1,1) | 12 | 25, 51, 102 | 0, 0, 0 |
| U2 k=0 | 46 | 3 | 4 | (6,6) | 16 | 25, 51, 102 | 2, 0, 0: {(0,8), (2,8)} at L=25 |
| U2 k=2 | 62 | 3 | 4 | (1,1) | 16 | 38, 77, 154 | 0, 0, 0 |
| U2 k=2 | 62 | 3 | 4 | (14,6) | 24 | 38, 77, 154 | 0, 0, 0 |
| U2 k=4 | 78 | 3 | 4 | (1,1) | 20 | 53, 106, 213 | 0, 0, 0 |
| U2 k=4 | 78 | 3 | 4 | (22,6) | 32 | 53, 106, 213 | 0, 0, 0 |
| U2 k=6 | 94 | 3 | 4 | (1,1) | 24 | 68, 137, 274 | 0, 0, 0 |
| U2 k=6 | 94 | 3 | 4 | (30,6) | 40 | 68, 137, 274 | 0, 0, 0 |
| cross b=7 | 96 | 4 | 4 | (0,0) / (6,1) | 28 / 27 | 29, 58, 116 | 0, 0, 0 / 0, 0, 0 |
| cross b=9 | 128 | 4 | 4 | (0,0) / (8,1) | 40 / 37 | 37, 74, 148 | 0, 0, 0 / 0, 0, 0 |
| cross b=11 | 160 | 4 | 4 | (0,0) / (10,1) | 52 / 47 | 45, 89, 179 | 0, 0, 0 / 0, 0, 0 |
| cross b=13 | 192 | 4 | 4 | (0,0) / (12,1) | 64 / 57 | 53, 105, 210 | 0, 0, 0 / 0, 0, 0 |
| cross b=15 | 224 | 4 | 4 | (0,0) / (14,1) | 76 / 67 | 61, 121, 242 | 0, 0, 0 / 0, 0, 0 |
| cross b=17 | 256 | 4 | 4 | (0,0) / (16,1) | 88 / 77 | 68, 137, 274 | 0, 0, 0 / 0, 0, 0 |

"Classes" is the number of parity classes among interior points. All cross and U2 rooms have all four. U2 sources are (1,1) in the bottom-left corner and the centre of the return pocket, (6+4k, 6). Cross arm-end sources (b−1, 1) have parity (0,1); (0,0) has parity (0,0).

The R22 control passes: T = (2,2) is in H_L(0,0) at every L. The second point, (2,−2), is a smooth point on a vertical wall.

## Sensitivity at short L

The proxy is not vacuous: shorter L leaves area-growing shadows that close by 2·diam ([short-L.log](short-L.log)).

| Room, S | L = 0.5·diam | L = 1·diam |
|---|---|---|
| cross b=7, (6,1) | 20 | 3 |
| cross b=17, (16,1) | 60 | 17 |
| cross b=17, (0,0) | 0 | 0 |
| U2 k=6, (1,1) | 12 | 4 |
| U2 k=6, (30,6) | 30 | 14 |

So the length needed to light everything grows with the room, but at L = 2·diam the hidden set is empty in every named room tested.

## Limits

- H_L is an upper bound for H. A zero H_L proves H = ∅ for that source, so the zeros are exact.
- This covers two named families and two sources each. It says nothing about other rooms or sources, and it doesn't test the bound in rooms where H is nonempty, beyond the R22 control.

## Re-run

```
cd d85-shadow-kill && python3 -B shadow.py all && python3 -B validate.py
```

Logs: [control.log](control.log), [u2.log](u2.log), [cross.log](cross.log), [short-L.log](short-L.log), [validate.log](validate.log).
