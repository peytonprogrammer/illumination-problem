# Independent review of Opus’s W26 parity update

Status: PASS for all saved geometry and the six selected rigidity certificates.

## Results

The saved census contains 327 distinct room/mark classes: 12 at W24, 89 at W25, and 226 at W26. Independently checked every boundary for strict simplicity, permitted directions and noncollinear actual corners; checked that every non-A lattice point of the room is an actual corner, and that the only interior lattice points are the two marked A points. An independently implemented D4/even-translation/unordered-mark canonical key finds no duplicates. The saved W24 summary rows are identical to the W24 subset of the W26 summary. This last comparison is summary consistency, not independent historical geometry provenance.

Selected the minimum- and maximum-event certificate in each wall-count group, breaking ties by tag, before optical replay. Replayed exactly each supplied direction and its supplied side with Codex’s prior independent infinitesimal event model, adapted to accept the supplied ordered vertex cycle. No extra directions or sides were tried.

| Certificate | Supplied events replayed | Exact rank on closure | Symmetry kernel |
| --- | ---: | ---: | ---: |
| parity-W24-9 | 120 | 25 | 3 |
| parity-W24-1 | 176 | 25 | 3 |
| parity-W25-21 | 111 | 26 | 3 |
| parity-W25-66 | 174 | 26 | 3 |
| parity-W26-322 | 96 | 27 | 3 |
| parity-W26-179 | 170 | 27 | 3 |

All 847 supplied events match their corner, unfolded target and positively normalized gradient modulo closure. Each saved coefficient is strictly positive; each exact weighted sum vanishes on the closure subspace. The ranks leave precisely two translations and uniform scaling. Twelve corruption controls reject a flipped coefficient or functional sign. These certificates establish local isolation within the fixed canonical wall-direction family. They do not establish isolation against arbitrary changes of wall direction.

## Meaning

The update strengthens evidence for the parity sign conjecture: every variation outside symmetry should violate some corner-event inequality. A finite census does not prove that conjecture. Norm growth alone still does not supply the required signs (see isolation-review/findings.md).

The already certified simple orthogonal 22-wall room has transparent non-A points and is outside this parity subclass. These results neither improve its wall count nor prove a global minimum.

## Reproduce

`python3 -B .context/illumination-k4-codex/parity-cert-review/check.py`

Frozen inputs, source and SHA-256 manifest are adjacent. The prior source/pruning audit remains in `../parity-enum-review/`. The W26 exhaustive search was not repeated, its full raw output was not recanonicalized independently, and 321 certificates were not optically replayed. All-327 rigidity remains Opus’s reported result, with independent validation of this six-certificate sample.
