#!/usr/bin/env python3
"""Verify the prescribed TR02 six-reflection witness in the ORIGINAL room."""
from pathlib import Path
from fractions import Fraction as F
import ast,json
r=Path(__file__).parent;old=ast.parse((r/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check'};ns={'Q':F}
exec(compile(ast.Module(body=[n for n in old.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'<reviewer-pure-guards>','exec'),ns)
P=[(4,4),(4,20),(20,20),(20,8),(12,8),(12,0),(28,0),(28,28),(0,28),(0,4)]
path=[(2,6),(4,F(54,7)),(0,F(78,7)),(4,F(102,7)),(0,18),(F(35,3),28),(28,14),(14,2)]
ns['simple'](P);result=ns['path_check'](P,path)
assert result['reflections']==6 and result['wall_leg_guards']==70
assert len([p for p in path[1:-1] if p[1]==28])==1
# Exact temporal/directional replay at fixed speed |vy|=1, |vx|=7/6.
clock=F(0);velocity=(F(7,6),F(1));events=[]
for i,(a,b) in enumerate(zip(path,path[1:])):
 dt=(b[1]-a[1])/velocity[1];assert dt>0
 assert b[0]-a[0]==dt*velocity[0];clock+=dt
 if i<len(path)-2:
  events.append({'point':b,'time':clock})
  walls=[(x,y) for x,y in ns['edges'](P) if ns['on'](x,y,b)]
  assert len(walls)==1
  x,y=walls[0]
  velocity=(-velocity[0],velocity[1]) if x[0]==y[0] else (velocity[0],-velocity[1])
assert clock==48 and velocity==(F(-7,6),F(-1))
out={'status':'PASS_ACTUAL_TR02_FIXED_WITNESS','polygon':P,'actual_S':[2,6],'actual_T':[14,2],'tau':'7/6','source_sign':1,'target_sign':1,'indices':[2,0,0,0],'portal_residuals':['7/3','-7','7'],'path':path,'events':events,'actual_target_time':clock,'roof_reflections':1,**result,'true_corner_contacts':0,'artificial_reflections':0,'scope':'One fixed input only; no whole metric/type/pair theorem.','whole_r3_complete':False,'whole_goal_complete':False}
r.joinpath('three-reflex-tr02-fixed-witness-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({'status':out['status'],'reflections':result['reflections'],'wall_leg_guards':result['wall_leg_guards'],'actual_target_time':str(clock)}))
