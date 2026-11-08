UNILLUMINABLE ROOMS: MINIMAL EXAMPLES, CLASSIFICATIONS AND EXCEPTIONS
J. C. F. de Winter and George W. Tokarsky

This package contains the paper, its LaTeX source and figures, and the
programs and data behind the computations in the paper.


CONTENTS

  unilluminable_rooms.pdf    the paper
  unilluminable_rooms.tex    LaTeX source
  Fig01.png ... Fig19.png    figures (FigNN.png is Figure NN of the paper)
  run_checks.py              runs all checks of the computations
  requirements.txt           Python packages for the optional programs
  code/                      programs and their data (see below)
  data/hole_free_catalogue.json
                             coordinates of the catalogues of Appendix A
  validation/                output of the last run of run_checks.py
  SHA256SUMS.txt             checksums of all files


COMPILING THE PAPER

Keep unilluminable_rooms.tex and the nineteen figures in one folder and run
pdfLaTeX three times:

    pdflatex unilluminable_rooms.tex
    pdflatex unilluminable_rooms.tex
    pdflatex unilluminable_rooms.tex

The bibliography is part of the source file, so there is no BibTeX step. The
source is ASCII and uses only standard packages (amsmath, amssymb, amsthm,
graphicx, booktabs, array, geometry, microtype, enumitem, xcolor, hyperref).


RUNNING THE CHECKS

The checks need Python 3.10 or later and Node.js 18 or later. They use only
the Python standard library. From this folder, run

    python run_checks.py

If Node.js is not on the PATH, give its location:

    python run_checks.py --node /path/to/node

Run Python without -O or -OO, because the checks use assertions. The run
takes under a minute. It writes validation/checks.txt, validation/checks.json,
one log per check in validation/logs/ and a few further results in
validation/, and some programs rewrite their own output files under code/
with the same content. A failed check gives a nonzero exit code.

The default run checks the saved output of the longer searches (Sections
3.1 and 5, Theorems 4.3, 4.8 and 6.5). To repeat those searches first (about
fifteen minutes), run

    python run_checks.py --full-census


PROGRAMS AND RESULTS

Section 3, rooms with one source
    code/single_source/verify_single_source.py
    Geometry of the pinwheel, the cross and the star, and the 16 local
    repair patterns used in the proofs of Theorems 3.1 and 3.2.
    code/single_source/one_source_census.py
    All rooms with one source and at most 20 sides (Section 3.1): 1, 3, 4,
    19, 67, 84, 253, 783 and 1346 types for 12 to 20 sides.
    Output: one_source_census_N20.json.

Theorem 4.2 and Corollary 4.4, post rooms and partition rooms
    code/rooms_with_holes/enumerate_posts.py, verify_posts.py
    All 64 and 576 candidates: 14 rooms in 5 types with 18 sides, 84 rooms
    in 21 types with 19 sides, and 28 partition rooms in 8 types with 20
    sides. Output: post_rooms.json.

Theorem 4.3, several posts
    code/rooms_with_holes/post_search.py
    With 1, 2, 3 and 4 posts: 14 rooms in 5 types with 18 sides (one post),
    24 rooms in 6 types with 17 sides (two posts), 9 rooms in 4 types with
    16 sides (three posts), and no room with 15 or fewer sides (up to four
    posts). Output: posts_k*_n*.json.

Theorem 4.5, pinched rooms
    code/rooms_with_holes/enumerate_pinched.py
    All 256 repair choices: 14 rooms in 4 types with 22 sides. The type with
    a square hole has 21 maximal straight boundary segments (Remark 4.6).
    Output: pinched_rooms.json.

Remark 4.7, Wolecki's room
    code/rooms_with_holes/wolecki22_match.py
    Coordinates transcribed from Figure 1 of Wolecki's preprint; the room is
    pinched Type 2.

Theorem 4.8, one hole
    code/rooms_with_holes/hole_search.py
    Two sources and one hole that does not touch the outer boundary: no room
    with fewer than 26 sides, and 42 rooms in 12 types with 26 sides.
    Output: hole_rooms.json.

Theorems 5.1 and 5.2, hole-free rooms with two sources
    code/hole_free_census/room_search_shared_grid.py   triangular tiling
    code/hole_free_census/room_search.py               square tiling
    code/hole_free_census/enumerate_orthogonal.py      second square search
    code/hole_free_census/validate_census.py           exact checks
    The searches cover 77 source positions with at most 28 triangles and 35
    source positions with at most 22 squares. The checker verifies every
    room, the symmetry orbits, the search summaries and every identifier of
    data/hole_free_catalogue.json: T24-001 to T24-012, T25-001 to T25-089,
    and S34-001 to S34-014. Types allow reflections and exchange of the two
    sources.

Section 6 and Appendix B, rooms with many sources
    code/assemblies/verify_snakes.py, bent_snakes.py
    Straight snakes with 2 to 21 sources and bent snakes with 3 to 21
    sources: 12 sides per source.
    code/assemblies/verify_assemblies.py
    The branching tree (4 sources, 3 connectors, no hole) and the closed
    snake (4 sources, 4 connectors, one hole), both with 48 sides.
    code/hole_free_census/three_sources.py
    Theorem 6.5: no hole-free room with three sources and at most 35 sides
    (281 positions of the sources). Output: three_sources_summary.json.

Proposition 7.1 and Theorem 7.2, the 27-gon
    code/minimum27/example27/verify_example.py   the 27-gon
    code/minimum27/verify_minimum.js             the 13 finite cases (Node.js)
    code/minimum27/independent_cp_check.py       second program (OR-Tools)
    code/minimum27/enumerate27.js                all rooms with 27 sides
    code/minimum27/check_27gons.py               exact check, 15 types

Proposition 7.3, the nonagon
    code/nonagon/geometry.py, nonagon.json (checked by run_checks.py)

Example 7.5, the 42-gon
    code/symmetry_rooms/verify_symmetry_room.py
    Checks the hypotheses of Theorem 7.4 for the 42-gon and for a 32-sided
    room with a reflection symmetry.

Section 8, rings of trapezoids
    code/trapezoid_rings/verify_examples.py
    Exact reflections and label transport for the returns with 5, 5 and 19
    reflections.

Consistency checks
    code/consistency_checks.py
    The census checker rejects ten corrupted search summaries, and published
    rooms are located in the catalogues: the rooms of Figure 3 of Tokarsky's
    1996 letter are partition Type 5 and pinched Type 2; Thomson's rooms are
    pinched Type 4 (square hole), pinched Type 2 (triangular hole) and
    T24-012; Castro's 24-gon is T24-003, Tokarsky's 24-gon is T24-008,
    Tokarsky's rectilinear room of 1995 is S34-001, and Tokarsky's post room
    with 18 sides is post Type 3. It also checks that the three types with
    one source and 13 sides do not contain the pinwheel (Section 3.1).

Figures
    code/figures/make_paper_figures.py
    Draws Fig01.png to Fig19.png from the data files (needs Matplotlib and
    NumPy).

The programs check finite certificates and carry out the finite searches.
The general lemmas, and the bounds that reduce each classification to a
finite search, are proved in the paper.


COORDINATES

Rooms on the 45-45-90 tiling and on the square tiling use Cartesian integer
coordinates; sources and A-points have even coordinates. Other embeddings:

    27-gon       (u,v) -> (sqrt(3)*u/2, v/2)
    star, nonagon (u,v) -> (u + v/2, sqrt(3)*v/2)
    trapezoids   (x,y) -> (x, sqrt(3)*y)


OPTIONAL PROGRAMS

These need the packages in requirements.txt:

    python code/figures/make_paper_figures.py           Matplotlib, NumPy
    python code/assemblies/verify_assemblies.py         Matplotlib (plot)
    python code/assemblies/build_assemblies.py          NumPy, SciPy
    python code/minimum27/independent_cp_check.py       OR-Tools
    python code/trapezoid_rings/examples.py             NumPy, Shapely

build_assemblies.py finds a branching tree and a closed snake with an
integer linear program and writes them to code/assemblies/. The solver may
return valid assemblies that differ from those drawn in Figure 5;
verify_assemblies.py checks whichever assemblies are stored there.
