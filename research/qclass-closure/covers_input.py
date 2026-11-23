"""Format the complete saved D64 covering-room list for the all-pairs checker."""
import json
from pathlib import Path
source=next(Path(__file__).resolve().parent.parent.glob('illumination-generalization*/fable/directions*/d64-finite-case/data/covers.json'))
for room in json.loads(source.read_text())['rooms']:
    cells={tuple(p) for p in room['cells']}
    degrees={}
    for x,y in cells:
        for p in ((x,y),(x+1,y),(x,y+1),(x+1,y+1)):
            degrees[p]=degrees.get(p,0)+1
    if sum(v==4 for v in degrees.values())>=2:
        print(len(cells),sum(v in (1,3) for v in degrees.values()),
              *(v for p in sorted(cells) for v in p))
