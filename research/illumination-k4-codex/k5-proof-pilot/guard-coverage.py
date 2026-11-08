from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('audit',ROOT.parent/'persisted-replay/audit.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
r=json.loads((ROOT/'orbit-check.json').read_text())['fixed_old_residual'];p=tuple(tuple(F(*c) for c in point) for point in r['path']);u,z=a.path_requirements(p)
room=json.loads((ROOT/'inputs/pilot/I2_1_1-pair0/residual-room.json').read_text())['room']['triangles'];guard=dict(U=sorted(u),Z=sorted(z),path=r['path'],room=room,q=[2,2],provenance='Exact orbit word '+r['shear_word']+'; one prescribed direction replay')
receipt=a.check_record(guard,(2,2),True);(ROOT/'orbit-guard.json').write_text(json.dumps(guard,indent=2)+'\n')
matrices=[(x,0,0,y) for x,y in product((1,-1),repeat=2)]+[(0,x,y,0) for x,y in product((1,-1),repeat=2)]
results=[]
s=json.loads((ROOT/'pass-summary.json').read_text())
for case in s['results']:
 if case['status']!='RESIDUAL':continue
 tag=case['tag'];packet=json.loads((ROOT/'cases'/tag/'residual-room.json').read_text())['room'];room=a.triangles(packet['triangles']);source,target=map(tuple,packet['marked']);matches=[]
 for origin,end in ((source,target),(target,source)):
  for g in matrices:
   if (end[0]-origin[0],end[1]-origin[1])!=(2*g[0]+2*g[1],2*g[2]+2*g[3]):continue
   def trans(raw):return frozenset(tuple(sorted((g[0]*p[0]+g[1]*p[1]+origin[0],g[2]*p[0]+g[3]*p[1]+origin[1]) for p in t)) for t in raw)
   U=trans(guard['U']);Z=trans(guard['Z'])
   if U<=room and not Z&room:matches.append(dict(origin=origin,matrix=g))
 results.append(dict(tag=tag,known_fixed_guard_matches=matches))
out=dict(status='PASS',new_guard_receipt=receipt,used=len(u),absent=len(z),results=results);(ROOT/'guard-coverage.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
