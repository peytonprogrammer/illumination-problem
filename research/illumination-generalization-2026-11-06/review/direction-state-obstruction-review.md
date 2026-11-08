# Independent review of the arithmetic direction-state obstruction

Verdict: ACCEPT both numbered claims in the frozen construction source, under the explicitly stated deterministic fixed-generator quotient assumptions. This is a proof-mechanism obstruction, not a dark pair or an uncapped illumination proof.

## Independent reconstruction

For the square of side B=8n^2, every finite reflected target image has the form (epsilon T_x+2Ba, delta T_y+2Bb). This follows separately in each coordinate by composing reflections in 0 and B. Subtract the actual S and divide by 2. The horizontal displacement is divisible by n; the vertical displacement is congruent to delta modulo n, hence is a unit modulo n, including composite n. If the primitive integer direction is (p,q), then qX=pY. Reduction modulo n therefore forces n to divide p. Neither coordinate can vanish: horizontal or vertical billiards in this square keep the other physical coordinate fixed, whereas both coordinates of S and T differ. Thus |p|>=n and |q|>=1. Their norm is at least sqrt(n^2+1). The direct interior segment has primitive direction (n,1), attaining this lower bound with no wall or corner contacts. Both endpoints have even integer coordinates, are strictly interior for every n>=2, and the square is a canonical triangle disk with four maximal walls.

The image argument is necessary for every actual path. Its use does not require that every reflected target image yield a valid path. Rationality of the launch direction follows from a nonzero integer image displacement; no irrational launch direction is omitted.

For the quotient claim, let F be a positive integer bound on its number of states. A shortest directed path from the state of e1 to any accepting state has no repeated state, so uses at most F-1 generators. Deterministic transition compatibility ensures that the corresponding generator word applied to e1 has that same accepting state, regardless of how the shortest path was found. Each generator is an invertible integer matrix of determinant one, preserves primitive vectors, and has induced infinity norm at most 2. The resulting vector therefore has infinity norm at most 2^(F-1) and Euclidean norm at most sqrt(2)2^(F-1). These bounds apply equally to negative generator powers because the inverse generators are individually included.

The reflection group of the square acts by signs in the minimal unfolding. Allowing signed coordinate permutations as in the source is a harmless larger set for this norm argument: all such transformations preserve Euclidean norm. Choose an integer n>sqrt(2)2^(F(4)-1). No direction in that accepting vector's stated Gamma orbit can illuminate the displayed square, by the preceding norm bound. This contradicts the exact accepting label. A direct (n,1) segment guarantees that an accepting direction and hence a reachable accepting state exist. The sharper designated-direction infinity bound is also valid.

## Limits and dispositions

- ACCEPT the exact minimum primitive direction norm for this family.
- ACCEPT impossibility of a W-uniform bounded deterministic quotient for the specified fixed SL(2,Z) generators and exact illumination labels.
- ACCEPT that bounded unweighted first-return graph types alone supply no such quotient or stopping rule.
- The proof does not exclude weighted states, parameter-dependent jump generators, arithmetic acceleration, a symbolic proof on an unbounded state space, or a uniform reflection-count theorem. Here zero reflections suffice.
- The uncapped W<=21 theorem remains open. Every displayed room is illuminated.

Method: independent exact hand reconstruction; no direction scan, ray tracer, orbit traversal, or peer script execution.
