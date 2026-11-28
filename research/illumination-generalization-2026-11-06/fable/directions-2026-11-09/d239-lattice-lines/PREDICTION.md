# Prediction before the lattice-line test (coordinator, 2026-11-27 23:26 HST)

Idea: a lattice pair is lit exactly when one rational direction carries S to T through k primitive steps, with every lattice point in between not a corner. k is the step count.
H1: a pair in different parity classes is lit with k = 1.
H2: a pair in the same class is lit with k = 2, unless it is dark.
Payoff: if k stays at 1 or 2 in big rooms, a proof has a bounded combinatorial shape that doesn't depend on the turn word. If k grows with size, this idea is dead.
Test: lines.py on three named rooms, directions with |p|, |q| <= B, at most 6 steps. Control: the 22-wall room must show its dark pair unlit.
Prediction: H1 holds for every different-class pair in all three rooms, 50%. H2 holds for every same-class pair except the dark one, 35%.
