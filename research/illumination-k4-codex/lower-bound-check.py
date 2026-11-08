"""Check explicitly listed small bases; no room generation or billiard search.

Odd-vertex incidence counting reduces <=8 base walls to <=4 cells.
The nine entries are the standard connected polyominoes of size1 through4.
The completeness argument is given separately in the theory note.
"""
from pathlib import Path
from collections import Counter
import json
D=Path(__file__).resolve().parent
SHAPES={
 'monomino':[(0,0)],
 'domino':[(0,0),(1,0)],
 'straight triomino':[(0,0),(1,0),(2,0)],
 'L triomino':[(0,0),(1,0),(0,1)],
 'straight tetromino':[(0,0),(1,0),(2,0),(3,0)],
 'square tetromino':[(0,0),(1,0),(0,1),(1,1)],
 'T tetromino':[(0,0),(1,0),(2,0),(1,1)],
 'L tetromino':[(0,0),(1,0),(2,0),(0,1)],
 'S tetromino':[(0,0),(1,0),(1,1),(2,1)],
 'attaining staircase': [(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)]}
def census(cells):
 c=set(cells);pts={(x+dx,y+dy) for x,y in c for dx in (0,1) for dy in (0,1)};smooth=[];interior=[];corners=[];pinches=[]
 for x,y in sorted(pts):
  ns=c&{(x+dx,y+dy) for dx in (-1,0) for dy in (-1,0)}
  if len(ns)==4:interior.append((x,y))
  elif len(ns)==2:
   a,b=ns
   if abs(a[0]-b[0])+abs(a[1]-b[1])==1:smooth.append((x,y))
   else:pinches.append((x,y))
  else:corners.append((x,y))
 edges=Counter(tuple(sorted(e)) for x,y in c for e in [((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))])
 B=sum(n==1 for n in edges.values());assert len(c)==len(interior)+B/2-1
 all_noncorner=smooth+interior
 residues={(x%2,y%2) for x,y in all_noncorner}
 broad=not pinches and len(smooth)>=2 and len(residues)==1
 equal=len(smooth)==2 and all((smooth[0][i]-smooth[1][i])%2==0 for i in (0,1))
 reflex=sum(len(c&{(x+dx,y+dy) for dx in (-1,0) for dy in (-1,0)})==3 for x,y in corners)
 if broad: assert 3*len(c)<=4*reflex+4
 return dict(broader_certificate=broad,reflex=reflex,all_noncorner_residues=sorted(residues),cells=cells,area=len(c),walls=len(corners),lattice_boundary=B,interior_lattice_points=interior,smooth_lattice_points=smooth,mark_residues=[(x%2,y%2) for x,y in smooth],same_residue_pair=equal,certificate_hypotheses=not interior and not pinches and len(smooth)==2 and equal)
incidence_checks=0
for cells in SHAPES.values():
 for ox,oy in [(0,0),(0,1),(1,0),(1,1)]:
  c={(x+ox,y+oy) for x,y in cells}
  pts={(x+dx,y+dy) for x,y in c for dx in (0,1) for dy in (0,1)}
  occupancy=Counter(len(c&{(x+dx,y+dy) for dx in (-1,0) for dy in (-1,0)}) for x,y in pts if x%2 or y%2)
  assert 3*len(c)==sum(k*v for k,v in occupancy.items())
  if not occupancy[2] and not occupancy[4]:
   r=sum(len(c&{(x+dx,y+dy) for dx in (-1,0) for dy in (-1,0)})==3 for x,y in pts)
   assert 3*len(c)<=4*r+4
  incidence_checks+=1
rows={n:census(c) for n,c in SHAPES.items()}
assert not any(r['certificate_hypotheses'] for n,r in rows.items() if n!='attaining staircase')
assert rows['attaining staircase']['certificate_hypotheses']
assert rows['attaining staircase']['broader_certificate']
assert not any(r['broader_certificate'] for n,r in rows.items() if n!='attaining staircase')
assert all(r['walls']==8 for n,r in rows.items() if r['area']==4 and len(r['smooth_lattice_points'])==2 and not r['interior_lattice_points'])
# Color check is invariant under integer translations, reflections and rotations.
(D/'lower-bound-check.json').write_text(json.dumps(dict(status='PASS',incidence_identity_checks=incidence_checks,scope='Nine explicitly supplied bases, plus the attaining five-cell control. Completeness is a mathematical classification argument, not a generated search.',rows=rows,restricted_lower_bound_base=10,restricted_lower_bound_three_copy_room=22),indent=2)+'\n')
for n,r in rows.items():print(n,': walls',r['walls'],'interior',r['interior_lattice_points'],'smooth',r['smooth_lattice_points'],'residues',r['mark_residues'],'qualifies',r['certificate_hypotheses'])
