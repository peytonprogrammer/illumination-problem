"""Task 6 minimum: the two known 45-degree relaxed dark rooms over the (2,4,4) base O_h.

Uses d51's analyse() unchanged (lib/check51_orig.py, d11 rooms45.py copied to lib/).
Every verdict rests on d51 memo definitions (Par, Rig over O_h, Theorem U45), which are
UNREVIEWED.  Rooms:
  - Monteil's slit room (d42 coordinates, slit (3,1)-(3,2)), marks (2,2), (4,2);
  - Monteil's pinched 22-gon in d53's coordinates (boundary walk with Q = (4,4) twice),
    marks (2,4), (4,2).
Run: python3 -B check45.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import check51_orig as C51          # noqa: E402

SLIT_OUTER = [(0, 2), (1, 2), (1, 1), (2, 0), (2, 1), (4, 1), (4, 0), (5, 1), (5, 2), (6, 2), (5, 3), (4, 3),
              (4, 4), (3, 3), (2, 4), (2, 3), (1, 3)]
PINCH_D53 = [(1, 4), (1, 5), (2, 6), (2, 5), (3, 5), (4, 4), (3, 4), (3, 3), (4, 3), (4, 4), (5, 3), (5, 2),
             (6, 2), (5, 1), (4, 1), (4, 0), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3), (0, 4)]

if __name__ == '__main__':
    C51.analyse('monteil slit room (d42)', SLIT_OUTER, [(2, 2), (4, 2)], slit=[((3, 1), (3, 2))])
    C51.analyse('monteil pinched 22-gon (d53 coordinates)', PINCH_D53, [(2, 4), (4, 2)])
