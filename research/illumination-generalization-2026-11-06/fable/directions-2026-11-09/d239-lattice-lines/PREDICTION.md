# Prediction before the lattice-line test (coordinator, 2026-11-27 23:26 HST)

Idea: a lattice pair is lit exactly when one rational direction carries S to T through k primitive steps, with every lattice point in between not a corner. k is the step count.
H1: a pair in different parity classes is lit with k = 1.
H2: a pair in the same class is lit with k = 2, unless it is dark.
Payoff: if k stays at 1 or 2 in big rooms, a proof has a bounded combinatorial shape that doesn't depend on the turn word. If k grows with size, this idea is dead.
Test: lines.py on three named rooms, directions with |p|, |q| <= B, at most 6 steps. Control: the 22-wall room must show its dark pair unlit.
Prediction: H1 holds for every different-class pair in all three rooms, 50%. H2 holds for every same-class pair except the dark one, 35%.

# Prediction before the census-wide fold test (coordinator, 2026-11-27 23:39 HST; approved by Daniel)

Scope: every stored census disc with at least two marks. d236 list (552,166 control discs, W <= 20, area <= 16) and d237 list (832,942 discs, W = 22 to 26, area <= 16). Then embedded W <= 20 rooms, area <= 16, from a copy of Astra's enumerator.
Limit of the test: the census holds one dark pair, and its room is already known to fold. So this run can't refute "dark implies folds". It measures how rare folding is among lit rooms, and it lists the folding rooms for step (A).
Payoff: if folding rooms are under 1% of rooms with marks, the dark room's folding is unlikely to be chance, and step (A) has a short explicit list to study. If folding is common (over 10%), the fold test separates nothing and the idea is dropped.
Prediction: under 1% of discs fold, 70%. Over 10%, 5%.

# Prediction before the certificate test (coordinator, 2026-11-27 23:41 HST)

Certificate FP for a same-class pair S, T (class a): an invariant partition of the cells (single cells allowed) whose quotient moves for the other three classes have no 2-cycles, with S and T over different base points.
Sketch of why FP forces darkness: every lattice point a path meets in another class is a corner or sends the base path straight back, so the path only meets class-a points over the base point of S.
Test: every same-class pair in both census lists, every invariant partition. The census has exactly one dark pair.
Prediction: FP holds for exactly that pair, 75%. If FP holds for a lit pair, my sketch is wrong.
