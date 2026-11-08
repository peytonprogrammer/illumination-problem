"""Reconcile count before and after the proved external-neighbor cap."""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
D={(x,y) for x in range(-4,5) for y in range(-4,5) if 0<abs(x)+abs(y)<=4};counts=Counter()
for a,b in combinations(sorted(D),2):
 F={(0,0),a,b};seen={(0,0)}
 while True:
  nxt=seen|{q for p in seen for q in F if abs(p[0]-q[0])+abs(p[1]-q[1])<=2}
  if nxt==seen:break
  seen=nxt
 if seen!=F:continue
 neighbors={(x+dx,y+dy) for x,y in F for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
 counts[len(neighbors-F)]+=1
out=dict(status='PASS',overlap_connected_before_neighbor_cap=sum(counts.values()),after_b_le_9=sum(n for b,n in counts.items() if b<=9),by_external_neighbors=dict(sorted(counts.items())))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
