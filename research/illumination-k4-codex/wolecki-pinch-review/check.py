"""Independent replay of frozen Wolecki pinch events; no new directions.
Uses Codex's previous exact dual/event machinery with explicit labeled vertices.
Coincident labels stay distinct throughout symbolic deformations.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,hashlib,math
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,D,dot,sub,add,scale,cross,canon,matmul,rank,rref
class PinchModel(EventModel):
 def __init__(self,room):
  self.room=room;self.vertices=list(map(tuple,room['vertices']))
  if sum(cross(a,b) for a,b in zip(self.vertices,self.vertices[1:]+self.vertices[:1]))<0:self.vertices.reverse()
  self.W=len(self.vertices);self.dim=self.W+6
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

def load(name):return json.loads((B/'inputs'/name).read_text())
def rationals(rows):return [tuple(map(F,r)) for r in rows]
def span_equal(a,b):return rank(a)==rank(b)==rank([*a,*b])
def coefficient_check(model,rows,clos,syms,certificate):
 coeff=[F(certificate['coefficients'][str(i)]) for i in range(len(rows))]
 assert all(c>0 for c in coeff)
 assert rank([*clos,tuple(sum(c*r[j] for c,r in zip(coeff,rows)) for j in range(model.dim))])==rank(clos)
 assert all(dot(r,s)==0 for r in rows for s in syms)
 rk=rank([*clos,*rows])-rank(clos)
 assert rk==model.dim-rank(clos)-rank(syms)==certificate['rank']==certificate['target']
 return dict(rows=len(rows),closure_rank=rank(clos),rank_on_closure=rk,symmetry_rank=rank(syms),positive_coefficients=len(coeff))

def main():
 model=PinchModel(load('room-wolecki22-pinch.json'));out=[];replayed={}
 assert model.W==22 and model.dim==28
 pinch=tuple(model.room['pinch']);labels=[i for i,v in enumerate(model.vertices) if v==pinch];assert len(labels)==2
 closed=[*model.closure,*[sub(model.vforms[labels[0]][j],model.vforms[labels[1]][j]) for j in (0,1)]]
 for radius in (12,18):
  supplied=load(f'funcs-room-wolecki22-pinch-R{radius}.json');metadata=load(f'events-room-wolecki22-pinch-R{radius}.json')['rows'];rows=rationals(supplied['funcs'])
  assert len(metadata)==len(rows)
  assert span_equal(rationals(supplied['clos']),model.closure)
  assert span_equal(rationals(supplied['syms']),model.syms)
  bydir={};statuses=Counter()
  for q in sorted({tuple(e['dir']) for e in metadata}):
   found=[]
   for side in (-1,1):
    e=model.event(q,side)
    statuses[e['status']]+=1
    if e['status']=='EVENT':found.append(e)
   bydir[q]=found
  unmatched=[];replayed[str(radius)]=[]
  for i,(e,row) in enumerate(zip(metadata,rows)):
   expected=canon(model.project(row));matches=[]
   for a in bydir[tuple(e['dir'])]:
    if list(a['corner'])==e['corner'] and a['unfolded_target_minus_s']==e['unfolded_target_minus_s'] and canon(model.project(tuple(map(F,a['gradient']))))==expected:matches.append(a)
   if not matches:unmatched.append(dict(index=i,meta=e,found=bydir[tuple(e['dir'])]))
   else:replayed[str(radius)].append(dict(index=i,**matches[0]))
  if unmatched:
   (B/'check.json').write_text(json.dumps(dict(status='MISMATCH',radius=radius,unmatched=unmatched),indent=2)+'\n')
   print('MISMATCH',radius,len(unmatched),'of',len(rows),flush=True);return
  families=[]
  for name,constraints in [('',model.closure),('-closed',closed)]:
   funcs=load(f'funcs-room-wolecki22-pinch{name}-R{radius}.json');certificate=load(f'posspan-room-wolecki22-pinch{name}-R{radius}.json')
   assert rationals(funcs['funcs'])==rows and span_equal(rationals(funcs['clos']),constraints)
   check=coefficient_check(model,rows,constraints,model.syms,certificate);check['family']='pinch_kept' if name else 'free_tips';families.append(check)
  out.append(dict(radius=radius,metadata_rows_matched=len(rows),supplied_directions=len(bydir),side_statuses=dict(statuses),families=families))
  print('PASS',radius,len(rows),'rows',flush=True)
 result=dict(status='PASS',cases=out,pinch_labels=labels,scope='Independent dual-sided replay of supplied directions only; exact signed gradients modulo closure, both closure families and rational positive dependencies. Geometric opening coverage requires boundary-check and written audit.')
 (B/'replayed-events.json').write_text(json.dumps(replayed,indent=2)+'\n')
 (B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
