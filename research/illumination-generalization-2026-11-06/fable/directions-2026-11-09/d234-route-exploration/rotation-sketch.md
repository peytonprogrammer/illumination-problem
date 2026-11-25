# Coordinator sketch: the x-list on the two-gate chart as one rotation (unreviewed)

Advances: L1. Status: a sketch and a guess. Nothing here is reviewed.

## Setup

Chart with column widths (1, N, 1, e), so X = N + 2 + e. Levels (-a, 0, 1, m+1, m+1+t, m+1+H). Slope s = K/X. Take the class that crosses all three gates upward, with 1 < s < m+1 so the two width-1 columns have no turn.

Unknown integers: j (complete periods in the middle column, period 2m) and i (periods in the last column, period 2H). With c the folded target class, K = c + 2mj + 2Hi. Two open conditions remain:

- L1 = K/X lies in the first-gate window (width about m).
- L2 = (N+1)K/X - 2mj lies in the second-gate window (width about min(s, m)).

The map (j, i) -> (L1, L2) is affine with determinant 4mH/X. So the legal chords of this class are the points of a rank-2 lattice coset, of covolume 4mH/X, inside a box of area about m^2/2.

## Count check (run before this note, prediction first)

Prediction: hits with 1 < s < m+1 number within a factor 3 of mX/(8H).
Result (scan_general.py, 0.3 CPU-s): residual m = 2, 3, 4 gives 81, 223, 384 against 24, 65, 128. Displaced target (e = 3N/2 - 1), m = 2, 3 gives 157, 360 against 40, 108.
Score: the factor-3 bound failed at 4 of 5 points (ratios 3.0 to 3.9). The scaling in mX/H held. The constant is wrong, probably because several sign classes contribute.

Consequence, as a guess: inside V the heights are small against N, so the box holds many lattice points unless the lattice is degenerate.

## Degenerate case is one rotation

Put g = gcd(m, H), L = lcm(m, H), and 2mj + 2Hi = 2gu. Then L1 = (c + 2gu)/X, and L2 mod 2L equals u*theta + const, where theta = 2g(N+1)/X - 2m*j1 and m*j1 + H*i1 = g. The u-range has length about mX/(2g). The window has relative length about g/(2H).

By the three-distance theorem, the class can miss only if theta/(2L) is within about 1/(qM) of p/q with q < 2H/g, M = mX/(2g). Worked out, this reads: (e+1)/X lies within about 2H/(DX) of a fraction with denominator D < 2H. Inside such a resonance the orbit is q arithmetic clusters at explicit positions, so hit or miss is an explicit inequality on the offset.

The residual is resonant: (e+1)/X = 1/3 - 1/(3X), which is the identity 3(N+1) = 2X + 1. Section A of l1-two-list-closure.md is the good-offset case of that resonance.

## Displaced target, exact scan (prediction first: lit at m = 2, 3, 4, P = 0.85)

Supports (0, N-1, N, 2N, 2N+1, 7N/2, 4N, 5N), N = 64m^2, levels of the residual. First hits V/X: m = 2: 644/641. m = 3: 1521/1441. m = 4: 4166/2561. Prediction held. The identity b = 2(d+e) isn't needed for lighting there.

## Limits of the sketch

- One sign class and moderate slopes only. The full list has steeper slopes with turns in the width-1 columns, so a miss of this class isn't a miss of the list. The exact scan decides a named point.
- The resonant set has size about 8H^2 values of e for fixed levels, so it isn't thin when H is near sqrt(N).
