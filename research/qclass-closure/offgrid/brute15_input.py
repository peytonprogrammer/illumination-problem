"""Generate the independent full connected-polyomino check at area 15."""
from pathlib import Path
import sys
base=Path(__file__).resolve().parent
s=next(base.parents[1].glob('illumination-generalization*/fable/directions*/d9-census-w22/enum_rooms.c')).read_text()
s=s.replace('fixed_nodes++; fixed_by_size[k]++;','fixed_nodes++; fixed_by_size[k]++; if (k != 15) return;')
s=s.replace('int V = 0, W = 0, pinch', 'int transparent = 0; int V = 0, W = 0, pinch')
s=s.replace('if (c == 1 || c == 3) W++;','if (c == 2 || c == 4) transparent |= 1 << (((X&1)<<1) | (Y&1));\n            if (c == 1 || c == 3) W++;')
s=s.replace('if (pinch || W > WMAX) return;', 'if (transparent==15 || pinch || W > WMAX) return;')
s=s.replace('if (!e) return;', '/* Keep every room, including rooms without any interior lattice marks. */')
for token in ('k != 15','transparent==15','Keep every room'):assert token in s
Path(sys.argv[1]).write_text(s)
