"""Smooth-boundary endpoint extension of Codex event_geometry.EventModel.
The sole event change is <= at the final limiting target time; the target
is reached before recording a final wall reflection. See darkness.md.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,D,dot,sub,add,scale,cross,canon,matmul,rank

class BoundaryEventModel(EventModel):
 def event(self,q,side,maxhits=2000):
  pos=tuple(D(a) for a in self.s);velocity=(D(q[0],-side*q[1]),D(q[1],side*q[0]));O=((F(1),F(0)),(F(0),F(1)));shift=(self.zero,self.zero);word=[];corner=None;cornerimage=None
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
   target=not cross(delta,dv) and 0<delta[axis]/dv[axis]<=tau.a;end=delta[axis]/dv[axis] if target else tau.a;crossed=[]
   for j,v in enumerate(self.vertices):
    d=sub(v,pv)
    if not cross(d,dv):
     mu=d[axis]/dv[axis]
     if 0<mu<=end:crossed.append((mu,j))
   for mu,j in sorted(crossed):
    image=self.mapped(O,shift,self.vforms[j])
    if corner is None:corner=self.vertices[j];cornerimage=image
    elif self.value(image)!=self.value(cornerimage):return dict(status='SECOND_CORNER')
   if target:
    if corner is None:return dict(status='ORDINARY_TARGET')
    lift=self.mapped(O,shift,self.tform);A=tuple(sub(lift[j],self.sform[j]) for j in (0,1));C=tuple(sub(cornerimage[j],self.sform[j]) for j in (0,1));av=self.value(A);cv=self.value(C);assert not cross(av,cv) and 0<dot(av,cv)<dot(av,av)
    gradient=tuple(side*(A[0][k]*cv[1]+av[0]*C[1][k]-A[1][k]*cv[0]-av[1]*C[0][k]) for k in range(self.dim))
    return dict(status='EVENT',direction=q,perturb_side=side,corner=corner,word=word,gradient=list(map(str,gradient)),row=canon(gradient),unfolded_target_minus_s=list(map(str,av)))
   pos=tuple(pos[j]+tau*velocity[j] for j in (0,1));R,b=self.reflectors[i];velocity=tuple(sum(R[j][k]*velocity[k] for k in (0,1)) for j in (0,1));shift=self.mapped(O,shift,b);O=matmul(O,R);word.append(i)
  return dict(status='CAP')

 def boundary_row(self):
  matches=[]
  for i,(a,d) in enumerate(zip(self.vertices,self.dirs)):
   z=sub(self.t,a)
   if cross(z,d)==0 and 0<dot(z,d)<dot(self.steps[i],d):matches.append(i)
  assert len(matches)==1
  i=matches[0];d=self.dirs[i]
  area=sum(cross(a,b) for a,b in zip(self.vertices,self.vertices[1:]+self.vertices[:1]))
  normal=(-d[1],d[0]) if area>0 else (d[1],-d[0])
  row=add(scale(normal[0],sub(self.tform[0],self.vforms[i][0])),scale(normal[1],sub(self.tform[1],self.vforms[i][1])))
  assert dot(row,self.theta)==0
  assert all(dot(row,s)==0 for s in self.syms)
  return row,i,normal

if __name__=='__main__':
 room=json.loads((B/'room.json').read_text());out=[]
 for t in room['boundary_targets']:
  model=BoundaryEventModel(dict(room,marked=[room['marked'][0],t]));row,wall,normal=model.boundary_row()
  assert dot(row,model.unit(model.W+4))==normal[0]
  assert dot(row,model.unit(model.W+5))==normal[1]
  assert dot(row,model.unit(0))==-normal[0]
  assert dot(row,model.unit(1))==-normal[1]
  out.append(dict(target=t,wall=wall,inward_normal=normal,row=list(map(str,row))))
 result=dict(status='PASS',cases=out,scope='Active moving-wall normals checked exactly. Does not certify optical event validity or rigidity.')
 (B/'boundary-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
