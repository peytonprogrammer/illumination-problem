# Novelty audit: the simple orthogonal 22-wall dark room

Audit date: 2026-10-31. Scope: historical and mathematical novelty of the verified candidate in `peer-fast-inputs/cand-2_2-1.json`. This audit does not search new rooms or trace rays.

## Judgment

**The specific construction is potentially new; historical priority is not established.** It is a verified strictly simple orthogonal room with 22 maximal straight walls and two distinct interior points that do not illuminate one another. It matches the published general 22-edge upper bound while imposing additional geometric restrictions. Its proof uses established ideas. We should describe it as a compact orthogonal construction and avoid claiming a new general record, a new physical mechanism, or the first simple 22-gon.

The earlier board statement that this “beats the strictly simple record of 24” is stronger than our literature evidence supports. We have checked particular published figures, not established a historical minimum for the entire class. No global optimality theorem follows from the candidate or this audit.

## Closest prior work

| Work | What the source establishes | Comparison and confidence |
|---|---|---|
| G. W. Tokarsky, *Polygonal Rooms Not Illuminable from Every Point*, American Mathematical Monthly 102(10), 867–879 (1995) | Foundational polygonal constructions, including the familiar 26-edge example. | Original full article was not recovered. Metadata verified; later primary accounts corroborate the triangle construction. We cannot exclude an overlooked orthogonal construction in its other figures. |
| David Castro, Quantum 7(3), January/February 1997, printed p.42 | Original reader letter gives a 24-edge modification of Tokarsky's example; reports research with Stan Wagon in spring 1996. | Original page read and rendered. The displayed room includes diagonal edges, so it differs from our orthogonal room. |
| G. W. Tokarsky and F. G. Boese, *Invisible Points in a House of Mirrors*, Mathematics Magazine 73(5), 364–369 (2000) | Theorem 1 gives invisible vertices; pp.366–367 discuss orthogonal invisible corners and a reflected-copy tiling corollary. | Public scan OCR read for the article. This is direct prior art for the general folding construction. Its corollary requires preservation of other base vertices; ours handles some smooth preimages through retracing, so the statements are not literally identical. Figure geometry is insufficiently preserved in OCR for an exact comparison. |
| Amit Wolecki, *Illumination in Rational Billiards*, arXiv:1905.09358 (2019; v3 November 2024) | Theorem 1.3 gives an upper bound of 22 edges. Section 3 uses Tokarsky's triangle recipe. Acknowledgments identify an independent unpublished 22-gon by Monteil. Remark 2.2 explains removable-corner continuation and retracing. | Source vector figure has 22 edges and a point contact, so its boundary is not a simple Jordan curve. It contains nonorthogonal walls. The figure PDFs in v1 and v3 are byte-identical. No lower bound or strict-simplicity record is established by Theorem 1.3. |
| Thierry Monteil, 2005 thesis, HAL tel-01287369 | Broad illumination, finite-blocking, translation-cover and symbolic-dynamics theory. | Full 123-page PDF recovered; contents, illumination introduction, relevant text and initial figures inspected. No 22-gon identified. This does **not** identify or exclude his unpublished example acknowledged in 2019. |
| Joseph O'Rourke, public *Art Gallery Visibility Theorems: An Introduction*, Fig.9.14, “Orthogonal Tokarsky polygon” | Supplies an existing orthogonal nonillumination example. | Primary vector outline has 34 maximal straight walls and a simple boundary. Our room has 12 fewer walls than this specific figure. The author page labels the forthcoming book 2026/2027; no claim about the earliest publication of this shape is needed. |
| Diana Davis, author-hosted *Billiards, Surfaces, and Geometry* manuscript, pp.114–115, Fig.87 | Current exposition of the classical room and later illumination theory. | Figure inspected; contains diagonal edges and differs from ours. It supplies no orthogonal 22-wall construction in the relevant section. |

## Exact figure comparison

The reproducible geometry receipt is `novelty-geometry-check.json`. Run:

```sh
python3 -B .context/illumination-k4-codex/novelty-geometry-check.py
```

The checker reconstructs Wolecki's 24 triangular tiles from the source vector figure, normalizes their repeated coordinates to the integer lattice with maximum residual below 9e-8, cancels shared edges, and counts boundary incidences. It finds a single degree-4 boundary vertex at normalized coordinate (2,0): the tip of an excluded triangular region meets the exterior boundary there. This is a contact in the mathematical figure, independent of stroke thickness. Both arXiv versions contain the identical figure file.

The checker extracts O'Rourke's orthogonal fill outline directly from the vector PDF converted by `mutool draw -F svg`. Its cyclic outline has 34 segments. The candidate's exact triangle union has 28 unit boundary edges; merging six straight-through grid vertices leaves 22 walls. Its boundary graph is one degree-2 cycle. The candidate's strict-simplicity and darkness proofs are also checked separately in the existing independent geometry and closed-orbit receipts.

These comparisons distinguish the displayed examples. They cannot establish absence of all equivalent earlier constructions.

## What is established, and what could be new

- **Established:** darkness in polygonal mirror rooms, square/triangle unfolding, lattice parity, reflected-copy constructions, and retracing at removable convex corners. Chernov–Galperin (2003), p.226, explicitly recounts the lattice-midpoint argument behind Tokarsky's lemma.
- **Established:** a published 22-edge upper bound. Our result does not improve that number.
- **Potential contribution:** this exact 15-square, strictly simple orthogonal 22-wall arrangement, with a short three-copy staircase proof and an independently reproducible finite certificate.
- **Possible explanatory refinement:** arranging smooth exceptions so they project only to removable convex corners. This may make a useful lemma or presentation, but has not been established as a new theorem distinct from prior folding theory.
- **Not proved:** 22 is minimal for all simple rooms, for all orthogonal rooms, or even all members of our larger assembly family.

## Coverage and remaining gaps

I screened all **43 records** returned by OpenAlex as citing Tokarsky (1995), plus the **one** returned as citing Wolecki's arXiv record. These are title/metadata screening counts, not 44 full-paper reviews. Relevant leads included Tokarsky–Boese, finite-blocking papers, visibility surveys and robot navigation. Database coverage is incomplete: Davis's book itself cites Wolecki but is absent from the one-item forward-citation list.

Additional checked leads include Chernov–Galperin's 2003 primary paper, the 2008 orthogonal visibility paper abstract, and the 2022 *Bouncing Robots in Rectilinear Polygons* paper. Bounded-reflection visibility, diffuse reflections and a robot trapped in selected directions do not by themselves establish an all-direction dark pair or a competing wall-count record. These were not conflated with the present problem.

Search families covered spelling variants of illumination/nonillumination/unilluminable, orthogonal/rectilinear/polyomino, 22-edge/22-sided/22-gon, staircase, Monteil, Tokarsky, Castro and Wolecki. Secondary pages supplied leads, not proof of priority. Absence from keyword results is weak evidence.

The decisive unresolved comparison is **Monteil's unpublished 22-gon**. Other material gaps are the original full Tokarsky (1995) paper and reliable figures for Tokarsky–Boese (2000). Obtaining those is more valuable for priority than further generic searches.

## Recommended claim and next move

Use: “We give a strictly simple orthogonal 22-wall room with a nonilluminating pair, together with a short folding proof and an independently checked finite certificate. The construction matches the known general 22-edge upper bound. We have not located this orthogonal realization in the sources reviewed.”

**Next move:** compare the coordinate list and three-copy picture with Monteil's unpublished example and the complete earlier Tokarsky figures before making a priority claim. The mathematical construction remains valid regardless of the outcome of that comparison.

## Primary source links

- Tokarsky (1995): https://doi.org/10.1080/00029890.1995.12004679
- Castro original letter: https://static.nsta.org/pdfs/QuantumV7N3.pdf#page=44
- Tokarsky–Boese (2000): https://doi.org/10.1080/0025570X.2000.11996877
- Public scan of the 2000 issue (OCR, not a publisher-hosted authoritative copy): https://www.scribd.com/document/522129195/Mathematics-Magazine-Vol-73-No-5-December-2000
- Wolecki v3: https://arxiv.org/html/1905.09358v3
- Wolecki v1 source: https://arxiv.org/e-print/1905.09358v1
- Monteil thesis: https://theses.hal.science/tel-01287369v1/document
- O'Rourke author page: https://www.science.smith.edu/~jorourke/AGVT/
- O'Rourke vector figure: https://www.science.smith.edu/~jorourke/AGVT/Templates/OrthoTokarsky.pdf
- Davis author manuscript: https://dianadavis.github.io/billiards-book.pdf
- Chernov–Galperin: https://rcd.ics.org.ru/upload/iblock/9bc/RCD080209.pdf
- Aanjaneya–Bishnu–Pal (2008): https://pages.cs.wisc.edu/~aanjneya/papers/DVPIROP/paper.html
- Çagırıcı–Bahoo–LaValle (2022): https://lavalle.pl/papers/CagBahLav22.pdf

## Follow-up: author comparison packet

`priority-followup.md` records additional checks and the remaining access gaps. `priority-comparison.txt` contains the local unsent Monteil inquiry, with the coordinate list mechanically extracted from the frozen candidate. His2026 author block verifies the delivery address. The historical-priority judgment remains unchanged.
