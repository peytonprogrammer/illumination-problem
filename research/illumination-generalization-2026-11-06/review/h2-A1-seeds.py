"""R47 exactly five residual fixed rooms, first positive only, original aggregate deadline."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as Q
import importlib.util,json,time
R=Path(__file__).resolve().parent;eff=json.loads((R/'h2-A1-effort.json').read_text());deadline=datetime.fromisoformat(eff['deadline_utc']).timestamp()
def guard():
 if time.time()>=deadline:raise TimeoutError('R47 original aggregate deadline')
sp=importlib.util.spec_from_file_location('ownorbit',R/'marked-origami-orbit-check.py');o=importlib.util.module_from_spec(sp);sp.loader.exec_module(o);o.build.deadline=guard
# Existing independent finite builder/orbit definitions only. No top-level writer executed.
def poly(b):return [(0,-4),(1,-4),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(2,1),(2,3),(1,3),(1,5),(0,5),(0,3),(-b,3),(-b,1),(0,1),(0,0),(-2,0),(-2,-2),(0,-2)]
rows=[]
for b in [1,2,3,4,8]:
 guard();V=poly(b);S=(1,-2);T=(1,2);o.build.geo.simple(V);bb=o.build.certify(V,S,T);positive,_=o.orbit(o.encode(bb),cap=1500);assert positive['status']=='LIT',('Not darkness',b,positive)
 A=((1,0),(0,1));gens={'T':((1,1),(0,1)),'U':((1,0),(1,1))}
 for letter in positive['word']:A=o.build.mul(gens[letter],A)
 chart=(A[1][1],-A[1][0]);g=bb['source_root_matrix'];vel=(g[0][0]*chart[0]+g[1][0]*chart[1],g[0][1]*chart[0]+g[1][1]*chart[1]);witness=o.physical_trace(V,S,T,vel,Q(positive['horizontal_length']))
 rows.append({'D':0,'a':2,'b':b,'polygon':V,'source':S,'target':T,'direction':vel,'orbit':positive,**witness});print(json.dumps({'b':b,'states':positive['state_count'],'reflections':witness['reflections']}),flush=True)
out={'status':'ALL_FIVE_R47_FIXED_FIRST_POSITIVE_CERTIFICATES_PASS','discovery':True,'original_deadline_utc':eff['deadline_utc'],'finished_utc':datetime.now(timezone.utc).isoformat(),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False}
(R/'h2-A1-seeds.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
