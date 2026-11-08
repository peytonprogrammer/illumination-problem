#!/usr/bin/env python3
"""Prescribed ET01 algebra, author r2 geometry and r9 boundary guard; no search."""
from fractions import Fraction as F
from pathlib import Path
import json

def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def plus(a,t,v):return (a[0]+t*v[0],a[1]+t*v[1])
def first(P,p,v):
 hs=[]
 for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
  e=sub(b,a);d=cross(v,e)
  if not d:continue
  t=cross(sub(a,p),e)/d;u=cross(sub(a,p),v)/d
  if t>0 and 0<=u<=1:hs.append((t,i,u,plus(p,t,v)))
 t=min(x[0] for x in hs);return [x for x in hs if x[0]==t]
# Rational controls corroborate the universal hand real-parameter proof.
formula=[]
for vals in [(4,4,8,8,2,2,2,2),(10,12,20,30,2,3,4,6),(10,12,20,30,6,8,3,4)]:
 A,H,R,U,a,b,c,d=map(F,vals)
 assert a*d==b*c and 0<a<R-A and 0<b<H and 0<c<A and 0<d<U-H
 D0=2*H+d-b;t=(H-b)/D0
 sx,sy=A+a,H-b;tx,ty=A-c,H+d
 q=sx+t*(tx-sx)
 xH=tx+d*(q-tx)/(H+d)
 assert 0<t<F(1,2) and 0<tx<q<sx<R
 assert xH==A-2*c*t and 0<tx<xH<A
 iv=(q-sx,-sy);ov=(tx-q,ty)
 refl=(iv[0],-iv[1]);assert cross(refl,ov)==0 and refl[0]*ov[0]+refl[1]*ov[1]>0
 formula.append({'parameters':[str(x) for x in map(F,vals)],'floor_x':str(q),'interface_x':str(xH),'positive_floor_time':str(t)})
P=[(2,0),(8,0),(8,4),(4,4),(4,8),(0,8),(0,2),(2,2)]
S=(F(6),F(2));T=(F(2),F(6));B=(2,2);C=(4,4);Q=(F(5),F(0))
turns=[cross(sub(P[i],P[i-1]),sub(P[(i+1)%len(P)],P[i])) for i in range(len(P))]
assert sum(x<0 for x in turns)==2 and all(turns)
# Union of two overlapping rectangles proves simplicity and containment; verify finite wall path.
hh=first(P,S,sub(Q,S));assert len(hh)==1 and hh[0][0]==1 and 0<hh[0][2]<1 and hh[0][1]==0
iv=sub(Q,S);out=sub(T,Q);assert cross((iv[0],-iv[1]),out)==0 and (iv[0],-iv[1])==(-1,2)
assert first(P,Q,out)[0][0]>1
hh=first(P,S,sub(T,S));assert len(hh)==2 and all(x[3]==C for x in hh)
assert B in P and C in P and S[0]>B[0]==T[0] and T[1]>B[1]==S[1]
assert plus(Q,F(1,3),out)==(4,2) and plus(Q,F(2,3),out)==(3,4)
P9=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
def frame(p):return (p[0]-1,1-p[1])
assert frame((1,1))==(0,0)
assert frame((0,0))==(-1,1) and frame((2,2))==(1,-1)
assert (0,2) in P9 and frame((0,2))==(-1,-1)
out={'status':'PASS_ET01_PRESCRIBED_INDEPENDENT_CONTROLS','method':'Own exact reflections, positive proportionality and raw finite-wall first hits; no author code, search or new room campaign','formula_controls':formula,'author_r2':{'polygon':P,'r':2,'S':[6,2],'T':[2,6],'singular_chord_corner':[4,4],'forced_corridor_interior_boundary_point':[2,2],'both_axis_orientations_fail_full_corridor':True,'actual_legal_floor_path':[[6,2],[5,0],[2,6]]},'r9_guard':{'frame':'(x-1,1-y)','blocked_corner':[1,1],'transformed_source':[1,-1],'transformed_target':[-1,1],'forced_interior_point':[-1,-1],'original_boundary_corner':[0,2],'corridor_hypothesis_fails':True,'new_darkness_proof_claimed':False},'local_ET01_proved_by_hand':True,'universal_A8':'REJECTED_BY_ACTUAL_R2','nine_distinct_corners_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
