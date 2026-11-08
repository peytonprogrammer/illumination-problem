"""ONE prescribed critical W20 input; exact first candidate then physical validation."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as Q
import importlib.util,json,hashlib,signal
R=Path(__file__).resolve().parent
eff=json.loads((R/'four-corner-critical-effort.json').read_text());end=datetime.fromisoformat(eff['deadline_utc'])
def deadline():assert datetime.now(timezone.utc)<end
signal.setitimer(signal.ITIMER_REAL,max(.001,(end-datetime.now(timezone.utc)).total_seconds()))
sp=importlib.util.spec_from_file_location('frozen_orbit',R/'marked-origami-orbit-check.py');O=importlib.util.module_from_spec(sp);sp.loader.exec_module(O)
# Reuse unchanged certified routines with THIS new prescribed input's deadline.
O.build.deadline=deadline;O.deadline=deadline
V=[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,13),(3,13),(3,15),(1,15),(1,16),(0,16),(0,12),(-1,12),(-1,10),(0,10),(0,8),(-1,8),(-1,6),(0,6)]
S=(2,2);T=(2,14);deadline();O.build.geo.simple(V);assert len(V)==20
assert O.build.geo.location(V,S)==O.build.geo.location(V,T)==1 and all(z%2==0 for p in(S,T) for z in p)
b=O.build.certify(V,S,T);state=O.encode(b);result,states=O.orbit(state,cap=50000)
out={'polygon':V,'source':S,'target':T,'walls':len(V),'triangles':b['triangles'],'source_component_squares':len(state[0]),'orbit_result':result,'whole_goal_complete':False,'discovery':True,'original_deadline':eff['deadline_utc']}
if result['status']=='LIT':
 A=((1,0),(0,1));gens={'T':((1,1),(0,1)),'U':((1,0),(1,1))}
 for letter in result['word']:A=O.build.mul(gens[letter],A)
 d=(A[1][1],-A[1][0]);g=b['source_root_matrix'];velocity=(g[0][0]*d[0]+g[1][0]*d[1],g[0][1]*d[0]+g[1][1]*d[1])
 witness=O.physical_trace(V,S,T,velocity,Q(result['horizontal_length']));out.update(status='FIRST_CANDIDATE_EXACT_ACTUAL_S_TO_T_PATH_VERIFIED',matrix=A,physical_direction=velocity,witness=witness)
else:out['status']='UNDECIDED_NO_VERIFIED_PATH_WITHIN_PRESCRIBED_ORBIT_CAP'
out['source_sha256']={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['marked-origami-orbit-check.py','marked-origami-builder-check.py','resumed-exact-check.py']}
out['finished_utc']=datetime.now(timezone.utc).isoformat();deadline();(R/'four-corner-critical-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('witness','polygon','source_sha256')}));print(json.dumps(out.get('witness',{}),default=str))
