"""Prescribed exact all-real linear-cell and physical controls for R51; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('r51',R/'coupled-two-tooth-check.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
p=c.make(1,3,2,1,-1,2,0,0)
verts=[(Q(0),Q(0)),(Q(1,5),Q(0)),(Q(1),Q(1)),(Q(0),Q(1,5))]
cc=c.cell(p,Q(1,2),Q(1,2));guards=[]
for g in cc['cell_guards']:
 vals=[c.value(g,a,b) for a,b in verts];assert min(vals)>=0 and max(vals)>0,(g,vals)
 guards.append({'numerator':g,'closure_vertex_values':vals})
box=(Q(1,2),Q(1,2),Q(7,12),Q(7,12));assert c.covers(cc,box)
rows=[]
for i in range(1,20):
 for j in range(1,20):
  a,b=Q(i,20),Q(j,20)
  if 5*a-4*b<1 and 5*b-4*a<1:rows.append(c.construct(p,a,b))
# Prescribed diagonal approach-to-boundary controls; exact affine scaling check.
for a,b in [(Q(1,1000),Q(1,1000)),(Q(999,1000),Q(999,1000)),(Q(1,2),Q(7,12)),(Q(7,12),Q(1,2))]:rows.append(c.construct(p,a,b))
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
scaled=[]
for cx,vy in [(Q(7),Q(3)),(Q(1000003),Q(1000009)),(Q(2,7),Q(13,11))]:
 a,b=Q(1,2),Q(7,12);z=c.construct(p,a,b)
 V=[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,13),(3,13),(3,15),(1,15),(1,16),(0,16),(0,12),(-b,12),(-b,10),(0,10),(0,8),(-a,8),(-a,6),(0,6)]
 V=[(cx*x,vy*y) for x,y in V];path=[(cx*x,vy*y) for x,y in z['path']];g.simple(V)
 scaled.append({'cx':cx,'vy':vy,**g.path_check(V,path)})
out={'whole_goal_complete':False,'status':'ALL_R51_CONTINUOUS_REGION_GUARDS_PASS','discovery':False,'params':p['params'],'region':['a>0','b>0','5a-4b<1','5b-4a<1'],'closure_vertices':verts,'strict_guard_count':len(guards),'guards':guards,'closed_box':box,'closed_box_all_guards_strict':True,'physical_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'rows':rows,'scaled_controls':scaled,'cell':cc,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['coupled-two-tooth-check.py','resumed-exact-check.py','minimal-prefix-physical-check.py']}}
(R/'coupled-two-tooth-region-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','cell','guards','source_sha256']})
