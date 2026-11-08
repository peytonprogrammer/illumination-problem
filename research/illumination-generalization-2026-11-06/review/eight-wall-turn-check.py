"""Prescribed exact turn-word controls, not room or optical discovery."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
counts=Counter()
for i,j in combinations(range(8),2):
 k=min(j-i,8-j+i);counts[k]+=1
 word=tuple(-1 if t in (i,j) else 1 for t in range(8))
 assert sum(word)==4
 # Cyclic relabelling/reflection puts reflex positions at0,k.
 assert any(tuple(word[(s+direction*t)%8] for t in range(8))==tuple(-1 if t in (0,k) else 1 for t in range(8)) for s in range(8) for direction in (-1,1))
assert dict(counts)=={1:8,2:8,3:8,4:4}
reps={
 'U':(1,[(0,0),(10,0),(10,4),(7,4),(7,1),(2,1),(2,5),(0,5)]),
 'staircase':(2,[(0,0),(10,0),(10,1),(7,1),(7,3),(2,3),(2,6),(0,6)]),
 'unequalT':(3,[(4,0),(5,0),(5,2),(10,2),(10,4),(0,4),(0,1),(4,1)]),
 'offset-overlap':(4,[(0,0),(7,0),(7,1),(10,1),(10,5),(3,5),(3,3),(0,3)]),
 'offset-gap':(4,[(0,0),(3,0),(3,1),(10,1),(10,5),(7,5),(7,3),(0,3)]),
 'offset-equal-x':(4,[(0,0),(5,0),(5,1),(10,1),(10,5),(5,5),(5,3),(0,3)]),
 'offset-transpose':(4,[(0,0),(7,0),(7,3),(10,3),(10,5),(3,5),(3,1),(0,1)])}
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def hit(a,b,c,d):
 if a[0]==b[0] and c[0]==d[0]:return a[0]==c[0] and max(min(a[1],b[1]),min(c[1],d[1]))<=min(max(a[1],b[1]),max(c[1],d[1]))
 if a[1]==b[1] and c[1]==d[1]:return a[1]==c[1] and max(min(a[0],b[0]),min(c[0],d[0]))<=min(max(a[0],b[0]),max(c[0],d[0]))
 if a[1]==b[1]:a,b,c,d=c,d,a,b
 return min(c[0],d[0])<=a[0]<=max(c[0],d[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])
results=[]
for name,(k,v) in reps.items():
 assert len(set(v))==8
 e=[sub(v[(i+1)%8],v[i]) for i in range(8)]
 assert all((x==0) != (y==0) for x,y in e)
 turns=[cross(e[(i-1)%8],e[i]) for i in range(8)]
 neg=[i for i,x in enumerate(turns) if x<0]
 assert all(turns) and len(neg)==2 and min(neg[1]-neg[0],8-neg[1]+neg[0])==k
 assert sum(cross(v[i],v[(i+1)%8]) for i in range(8))>0
 for i,j in combinations(range(8),2):
  if (i-j)%8 not in (1,7):assert not hit(v[i],v[(i+1)%8],v[j],v[(j+1)%8]),(name,i,j)
 results.append({'name':name,'separation':k,'vertices':v,'reflex_indices':neg})
out={'status':'EXACT_TURN_WORD_AND_FIXED_GEOMETRY_CONTROLS_PASS','labelled_words':28,'word_counts':dict(counts),'representatives':results,'kind':'prescribed finite combinatorial controls, not optical search or universal metric proof','source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('eight-wall-frontier.md','eight-wall-turn-check.py')},'whole_goal_complete':False}
(HERE/'eight-wall-turn-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='representatives'}))
