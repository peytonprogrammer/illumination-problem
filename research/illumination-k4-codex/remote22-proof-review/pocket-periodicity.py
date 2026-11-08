"""Four prescribed controls of the analytic rectangle-return identity."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'inputs'))
from exact import run
from boundary_replay import replay
base=json.loads((HERE/'inputs/one-room-geometry.json').read_text())['vertices']
rows=[]
for n in (0,1,2,13):
 h=1+F(10*n,13);V=[tuple(map(F,p)) for p in base];V[17]=(-1,1+h);V[18]=(-2,1+h)
 d,P=run(V,(0,0),(2,2),B=100,dirs=[(10,-13)])
 assert d==(10,-13) and P is not None
 assert replay(V,(0,0),(2,2),P)==14+2*n
 # Precisely the same outside path begins after the pocket's last side hit.
 original=json.loads((HERE/'inputs/witness-check.json').read_text())['path']
 old=[tuple(map(F,p)) for p in original]
 assert P[:2]==old[:2] and P[5+2*n:]==old[5:]
 rows.append({'n':n,'height':str(h),'reflections':len(P)-2,'outside_path_unchanged':True})
(HERE/'pocket-periodicity.json').write_text(json.dumps({'status':'PASS','controls':rows,'scope':'Four fixed controls of a separately proved general periodicity lemma; no direction or geometry discovery scan.'},indent=2)+'\n');print(rows)
