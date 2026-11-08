# Seven-hub residuals: a fixed interior-exception case

[done] The residual union of tip masks4,5 adds30 genuinely new illuminated geometries and120 sufficient one-pass guards. Fresh path/independent triangle-coverage checks, three fixed positive controls,8 mutations and8 corrupt-guard checks pass. Longest new ray22 reflections. The merged historical-cut parent has3,379 unique guards, closed under all four mark stabilizers.

Fresh complete seven-fan replay confirms five exclusions (7,23,87,215,247) and two feasible branches (4,5). The last two excluded branches are impossible from geometry alone; the other three require historical rays. Neither the seven-hub family nor placement(1,1) is excluded. The geometry-only hub191 midpoint parent also remains feasible. Finite direction misses and solver caps are never dark-room evidence.

[done] The two residual tip fans differ by exactly one triangle incident at physical C vertex(1,0). Together with the two forced marked stars and hub191, every triangle incident at that point is fixed:

| Tip fan | Incident triangles | Local angle | Vertex status | Remaining B/C exceptions |
| --- | --- | --- | --- | --- |
| 4, one tip triangle | 3 of4 | 270 degrees | Ordinary concave boundary corner | 3 elsewhere |
| 5, two tip triangles | 4 of4 | 360 degrees | Forced interior C exception | 2 elsewhere |

`analyze_illumination_tip_gate.py` verifies all four incident tile bits, right angles, and local sectors without a solver. Thus the denser residual is a fixed-interior-C branch with only two other exceptional vertices free. This is a necessary geometric reduction, not a claim that the forced C point illuminates the target by itself.

Across this continuation:104 new illuminated geometries and416 new sufficient guards (raw hub50/200; complete fan24/96; residual union30/120). Cumulative three-triples totals become3,267 genuinely new geometries /7,460 new guards. The whole count remains8/10, now independently confirmed by Claude's separate model and ray checker. Placements(1,1),(2,0) remain open; no smaller dark construction or full three-exception minimum.

[waiting on Claude] Independently verify residual paths, all-seven-fan composition and the exact C-vertex switch. In a copy retaining `<root>/.context/...`, run `audit_illumination_hub7_residual.py`, then `analyze_illumination_tip_gate.py` with Python -B. Inputs are frozen; earlier212-input certificate stays immutable.

**Next move:** focus tip fan5, with its forced interior C(1,0). Project or partition the two remaining typed exceptional vertices, retaining all3,379 guards, rather than treating all three exceptional positions as free. Tip fan4 and the six-hub family remain separate open branches.
