"""Exact one-corner event geometry for a fixed canonical-direction room.
Reuses Codex's independently checked infinitesimal type. No peer code.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
import importlib.util,math
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('codex_dual_numbers',P/'inputs/dual.py');dual=importlib.util.module_from_spec(spec);spec.loader.exec_module(dual)
D=dual.D

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def matmul(A,C):return tuple(tuple(sum(A[i][k]*C[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def canon(row):
 den=math.lcm(*(F(x).denominator for x in row));ints=[int(x*den) for x in row];g=math.gcd(*ints)
 assert g;return tuple(x//g for x in ints)
def rref(rows):
 out=[list(map(F,x)) for x in rows];pivots=[];k=0
 for j in range(len(out[0])):
  i=next((i for i in range(k,len(out)) if out[i][j]),None)
  if i is None:continue
  out[k],out[i]=out[i],out[k];v=out[k][j];out[k]=[a/v for a in out[k]]
  for i in range(len(out)):
   if i!=k:
    v=out[i][j];out[i]=[a-v*b for a,b in zip(out[i],out[k])]
  pivots.append(j);k+=1
  if k==len(out):break
 return out[:k],pivots

def rank(rows):return len(rref(rows)[1])

class EventModel:
 def __init__(self,room):
  self.room=room;self.vertices=[tuple(v) for v in room['vertices']];self.W=len(self.vertices);self.dim=self.W+6
  self.steps=[sub(b,a) for a,b in zip(self.vertices,self.vertices[1:]+self.vertices[:1])];lengths=[math.gcd(*map(abs,d)) for d in self.steps];self.dirs=[(d[0]//l,d[1]//l) for d,l in zip(self.steps,lengths)]
  assert all(d in [(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b] for d in self.dirs)
  self.s,self.t=map(tuple,room['marked']);self.theta=tuple(map(F,self.vertices[0]+tuple(lengths)+self.s+self.t));self.zero=(F(0),)*self.dim
  def unit(i):return tuple(F(j==i) for j in range(self.dim))
  self.unit=unit;current=(unit(0),unit(1));self.vforms=[]
  for i,d in enumerate(self.dirs):self.vforms.append(current);current=tuple(add(current[j],scale(d[j],unit(2+i))) for j in (0,1))
  self.sform=(unit(self.W+2),unit(self.W+3));self.tform=(unit(self.W+4),unit(self.W+5))
  self.closure=[tuple([0,0]+[d[j] for d in self.dirs]+[0,0,0,0]) for j in (0,1)]
  self.crows,self.cpiv=rref(self.closure);assert len(self.cpiv)==2
  self.syms=[]
  for axis in (0,1):
   row=[0]*self.dim;row[axis]=row[self.W+2+axis]=row[self.W+4+axis]=1;self.syms.append(tuple(row))
  if all(not(dx and dy) for dx,dy in self.dirs):
   for axis in (0,1):
    row=[0]*self.dim;row[axis]=self.vertices[0][axis];row[self.W+2+axis]=self.s[axis];row[self.W+4+axis]=self.t[axis]
    for i,d in enumerate(self.dirs):
     if d[axis]:row[2+i]=lengths[i]
    self.syms.append(tuple(row))
  else:self.syms.append(self.theta)
  self.reflectors=[]
  for i,d in enumerate(self.dirs):
   n=(-d[1],d[0]);nn=dot(n,n);R=tuple(tuple(F(int(a==b))-F(2*n[a]*n[b],nn) for b in (0,1)) for a in (0,1));c=add(scale(n[0],self.vforms[i][0]),scale(n[1],self.vforms[i][1]));b=tuple(scale(F(2*n[j],nn),c) for j in (0,1));self.reflectors.append((R,b))
 def value(self,p):return tuple(dot(a,self.theta) for a in p)
 def mapped(self,O,shift,p):return tuple(add(add(scale(O[j][0],p[0]),scale(O[j][1],p[1])),shift[j]) for j in (0,1))
 def project(self,g):
  out=list(map(F,g))
  for c,k in zip(self.crows,self.cpiv):
   v=out[k];out=[a-v*b for a,b in zip(out,c)]
  return tuple(out)
 def delta(self,v):
  d=list(map(F,v))
  for c,k in zip(self.crows,self.cpiv):d[k]=-sum(c[j]*d[j] for j in range(self.dim) if j!=k)
  return tuple(d)
 def event(self,q,side,maxhits=2000):
  pos=tuple(D(a) for a in self.s);velocity=(D(q[0],-side*q[1]),D(q[1],side*q[0]));O=((F(1),F(0)),(F(0),F(1)));shift=(self.zero,self.zero);word=[];corner=None;cornerimage=None;cornerprefix=None
  for hit in range(maxhits):
   candidates=[]
   for i,a in enumerate(self.vertices):
    d=self.dirs[i];n=(-d[1],d[0]);den=n[0]*velocity[0]+n[1]*velocity[1]
    if not den.a:continue
    tau=(dot(n,a)-(n[0]*pos[0]+n[1]*pos[1]))/den
    if tau<=0:continue
    point=tuple(pos[j]+tau*velocity[j] for j in (0,1));along=sum((point[j]-a[j])*d[j] for j in (0,1));length=dot(self.steps[i],d)
    if 0<=along<=length:candidates.append((tau,i))
   if not candidates:return dict(status='NO_WALL')
   tau,i=min(candidates,key=lambda v:v[0]);pv=tuple(p.a for p in pos);dv=tuple(v.a for v in velocity);axis=next(j for j in (0,1) if dv[j]);delta=sub(self.t,pv)
   target=not cross(delta,dv) and 0<delta[axis]/dv[axis]<tau.a;end=delta[axis]/dv[axis] if target else tau.a;crossed=[]
   for j,v in enumerate(self.vertices):
    d=sub(v,pv)
    if not cross(d,dv):
     mu=d[axis]/dv[axis]
     if 0<mu<=end:crossed.append((mu,j))
   for mu,j in sorted(crossed):
    image=self.mapped(O,shift,self.vforms[j])
    if corner is None:corner=self.vertices[j];cornerimage=image;cornerprefix=len(word)
    elif self.value(image)!=self.value(cornerimage):return dict(status='SECOND_CORNER')
   if target:
    if corner is None:return dict(status='ORDINARY_TARGET')
    lift=self.mapped(O,shift,self.tform);A=tuple(sub(lift[j],self.sform[j]) for j in (0,1));C=tuple(sub(cornerimage[j],self.sform[j]) for j in (0,1));av=self.value(A);cv=self.value(C);assert not cross(av,cv) and 0<dot(av,cv)<dot(av,av)
    gradient=tuple(side*(A[0][k]*cv[1]+av[0]*C[1][k]-A[1][k]*cv[0]-av[1]*C[0][k]) for k in range(self.dim))
    return dict(status='EVENT',direction=q,perturb_side=side,corner=corner,word=word,corner_prefix_hits=cornerprefix,corner_image_forms=[[str(x) for x in row] for row in cornerimage],gradient=list(map(str,gradient)),row=canon(gradient),unfolded_target_minus_s=list(map(str,av)))
   pos=tuple(pos[j]+tau*velocity[j] for j in (0,1));R,b=self.reflectors[i];velocity=tuple(sum(R[j][k]*velocity[k] for k in (0,1)) for j in (0,1));shift=self.mapped(O,shift,b);O=matmul(O,R);word.append(i)
  return dict(status='CAP')
