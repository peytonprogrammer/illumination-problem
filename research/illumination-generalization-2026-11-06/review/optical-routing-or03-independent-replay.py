#!/usr/bin/env python3
"""Prescribed raw geometry and algebra for OR03; not an orbit census."""
from pathlib import Path
from fractions import Fraction as F
import json
P=[(-8,-200),(24,-200),(24,0),(16,0),(16,2),(0,2),(0,0),(-8,0)]
S=(4,-2);T=(6,-100)
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
E=list(zip(P,P[1:]+P[:1]))
assert all((a[0]==b[0]) != (a[1]==b[1]) for a,b in E)
# Orthogonal finite-edge intersection, including nonadjacent point touching.
def meet(a,b,c,d):
 if a[0]==b[0] and c[0]==d[0]:return a[0]==c[0] and max(min(a[1],b[1]),min(c[1],d[1]))<=min(max(a[1],b[1]),max(c[1],d[1]))
 if a[1]==b[1] and c[1]==d[1]:return a[1]==c[1] and max(min(a[0],b[0]),min(c[0],d[0]))<=min(max(a[0],b[0]),max(c[0],d[0]))
 if a[1]==b[1]:return meet(c,d,a,b)
 return min(c[0],d[0])<=a[0]<=max(c[0],d[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])
for i,(a,b) in enumerate(E):
 for j,(c,d) in enumerate(E):
  if j>i and (j-i)%len(E) not in(1,len(E)-1):assert not meet(a,b,c,d)
turns=[cross(sub(P[i],P[i-1]),sub(P[(i+1)%len(P)],P[i])) for i in range(len(P))]
assert sum(t<0 for t in turns)==2 and all(t for t in turns)
assert all(-8<p[0]<24 and -200<p[1]<0 and all(x%2==0 for x in p) for p in [S,T])
# Lower rectangle is convex: every point on S-T satisfies same strict bounds.
assert min(S[0],T[0])>-8 and max(S[0],T[0])<24
assert min(S[1],T[1])>-200 and max(S[1],T[1])<0
# Affine maps (sign,offset); generate translations plus sign by algebra.
def compose(g,h):return (g[0]*h[0],g[0]*h[1]+g[1])
r0=(-1,0);rb=(-1,-400)
assert compose(r0,rb)==(1,400) and compose(rb,r0)==(1,-400)
rows=[]
for eps in [-1,1]:
 for eta in [-1,1]:
  residue=(eps*2-eta*100)%400
  gap=min(residue,400-residue)
  assert gap>=98
  rows.append({'source_sign':eps,'target_sign':eta,'difference_residue':residue,'minimum_absolute_representative':gap})
assert min(x['minimum_absolute_representative'] for x in rows)==98
result={'status':'PASS_PRESCRIBED_OR03_GEOMETRY_AND_ALL_RESIDUES','room':P,'r':2,'actual_even_even_S':S,'actual_even_even_T':T,'actual_direct_segment_legal':True,'horizontal_group_generators':[r0,rb],'complete_group_form':'sign*y+400*n','all_difference_residues':rows,'all_exterior_words_excluded_from_width_criterion':True,'all_cuts':'0<=c<2: common c cancels; 2h_c<=4<98','claim_requires':'OR01 exterior-before-terminal-section guard','actual_dark_counterexample':False,'G8_refuted':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
