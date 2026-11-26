Advances: L1 — summing every sign class leaves a discrepancy linear in the horizontal travel, even with fixed heights inside V.

**Predictions recorded before running the scan.** The five observations were supplied in the brief. My zero-frequency predictions for the strict moderate window, in the requested order, are X/4 = 96.25, 216.25, 384.25, 160.25, 360.25. These are volume predictions, not fitted or blind estimates.

**Count and main term.** Use the d234 widths (1,N,1,e), middle height m and terminal height H. Count rays by (integer endpoint travel K, initial sign), as in scan_classes. In coordinates (s,z), s=K/X and z is the folded second ordinate. Fix the start sign, the affine folding branches in columns 1 and 3 (including their turns), the exit sign from column 2, and the terminal target image sign. Leave the complete middle and terminal windings j,i free. Developing across the four columns gives K = constant ±2mj ±2Hi (using absolute initial slope); the second ordinate has form z = constant ±(N+1)s ±2mj. Thus the lattice in (s,z) has determinant 4mH/X. The exact count sums its coset points in the gate intervals pulled back to (s,z), including the cutoff 0<s<R. These domains are polygons: the last gate couples z and s. Equivalently they are planar sections of boxes. Count a regular branch only once, using the scan's strict transmission convention.

Explicitly the zero-frequency term is X/(4mH) times the sum of the polygon areas, one per branch and terminal sign. For general R each area has the closed form |Σ det(v_i,v_{i+1})|/2 on its cyclic vertices (intersections of the branch and gate lines). In the requested moderate window it simplifies: only the upward start passes. At gate 2 write z=1+u, 0<u<m. For an upward exit, the admissible u interval has length min(s,m). For a downward exit, a floor bounce in column 3 can pass gate 3 over a length max(0,s−m). No roof intervenes since H=m+2>s. Thus the total length is s, and the two terminal images give main term X/(2mH) times the integral of s from 1 to m+1, or X/4. The five exact counts reproduced the brief: 81, 223, 384, 157, 360.

**Counterfamily, all classes included.** Keep m=2,H=4,a=4,t=1 and the d233 transverse supports for arbitrary even N>78. Then X=3N/2+1 and the d233 end-travel bound puts the family in V. Take R=3. No start reaches gate 1 before s=1, and only upward starts pass for 1<s<3. Write U=(N+1)s=(2K+s)/3. Choose j with −1<U−4j<3. On the lower half of this interval fold about 1, giving a downward exit from column 2. On the upper half keep the ordinate, giving an upward exit. Either way, a successful third crossing must be upward and equals U+s−4j: in the downward case it must first reflect about 1. The upper roof at 7 is out of reach. Thus, away from branch endpoints, the exact gates and both final images are

    −1 < U−4j < 3,     3 < U+s−4j < 7,     K−4j ≡ 2 or 4 (mod 8).

Set A=2K−12j. The target condition forces K even, hence A is a multiple of 4. The gates become −3<A+s<9 and 9<A+4s<21. For 1<s<3 only two cases survive:

| A | slope interval | allowed K mod 24 |
|---|---|---|
| 0 | (9/4,3) | 6,12 |
| 4 | (5/4,3) | 2,8 |

Indeed K−4j=(K+A)/3, and the listed residues also make j=(2K−A)/12 integral. A transition exactly at a folding endpoint changes at most O(1) counts here: for each of finitely many A it fixes s. Each row counts two residue classes in an interval of integers. Their total is (2/24)(3/4+7/4)X+O(1) = 5X/24+O(1). The zero-frequency prediction is 6X/24. The discrepancy is therefore −X/24+O(1), with m,H,R fixed. The discrepancy does not erase the main term in this family, but it disproves the proposed N-independent error.

**Stop.** A full-list miss would require every admissible coset to miss its section, including steep classes beyond this cutoff. This calculation establishes neither a full miss nor a separating fold. A different resonance-dependent leading coefficient would need its own positivity proof.
