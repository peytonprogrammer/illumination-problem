"""Fixed-fixture controls for extracting directions from orbit certificates."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ow',ROOT/'orbit-witness.py');ow=importlib.util.module_from_spec(spec);spec.loader.exec_module(ow)
spec=importlib.util.spec_from_file_location('audit',ROOT.parent/'persisted-replay/audit.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
# Bind the instrumentation to the frozen original: only expose a derivative frame.
s=(ROOT/'inputs/origami_dark.py').read_text().replace('if v==S and sstart is None: sstart=s','if v==S and sstart is None: sstart=s; source_frame=g').replace('return r,u,lab,sstart','return r,u,lab,sstart,source_frame')
assert s==(ROOT/'inputs/origami_frame.py').read_text()
fixture=json.loads((ROOT/'inputs/pilot/I2_1_1-pair0/vertices.json').read_text());room=json.loads((ROOT/'inputs/pilot/I2_1_1-pair0/residual-room.json').read_text())['room'];room=audit.triangles(room['triangles'])
V=list(map(tuple,fixture['vertices']));S,T=map(tuple,fixture['marked']);r=ow.direction(V,S,T)
assert r['status']=='LIT'
path=ow.trace_direction(V,S,T,r['direction']);need,forbid=audit.path_requirements(tuple(path));assert need<=room and not forbid&room
r['physical_reflections']=len(path)-2;r['path']=[[[c.numerator,c.denominator] for c in p] for p in path]
controls=[]
for S,T in [((1,1),(2,2)),((2,2),(1,1)),((1,2),(2,1))]:
 V=[(0,0),(3,0),(3,3),(0,3)];out=ow.direction(V,S,T);assert out['status']=='LIT';p=ow.trace_direction(V,S,T,out['direction']);controls.append(dict(S=S,T=T,certificate=out,reflections=len(p)-2))
# Prescribed mixed shear controls. Endpoints are constructed from each fixed
# integer matrix, so this tests composition order without searching directions.
mixed=[]
for word in ('TL','LTL','TTLL','TLTL'):
 V=[(0,0),(40,0),(40,40),(0,40)];S=(20,20)
 rr,uu,ll,ss,frame=ow.o.build(V,S,(21,21));B=((1,0),(0,1))
 for ch in word:B=ow.o.mul(B,((1,-1),(0,1)) if ch=='T' else ((1,0),(-1,1)))
 d=ow.o.ap(tuple(zip(*frame)),(B[0][0],B[1][0]));T=tuple(S[k]+d[k] for k in (0,1))
 assert all(0<c<40 for c in T)
 rr,uu,ll,ss,frame=ow.o.build(V,S,T);state=ow.o.canon(rr,uu,ll,ss)
 for ch in word:
  rr,uu,ll=state
  if ch=='T':uu=tuple(ow.o.comp(uu,ow.o.inv(rr)))
  else:rr=tuple(ow.o.comp(rr,ow.o.inv(uu)))
  state=ow.o.canon(rr,uu,ll,0)
 rr,uu,ll=state;i=rr[0];found=False
 while i!=0:
  if ll[i]=='block':break
  if ll[i]=='T':found=True;break
  i=rr[i]
 assert found,(word,d,T)
 p=ow.trace_direction(V,S,T,d);assert len(p)==2
 mixed.append(dict(word=word,matrix=B,direction=d,target=T,horizontal_LIT=True,direct_replay=True))
result=dict(status='PASS',fixed_old_residual=r,rectangle_controls=controls,mixed_shear_controls=mixed,scope='One previously classified fixed residual and three rectangles; exact orbit direction extraction and prescribed direction replay only. No new residual classification or direction scan.')
(ROOT/'orbit-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
