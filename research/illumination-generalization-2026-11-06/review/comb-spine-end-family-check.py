"""Prescribed whole-family formula controls, original R33 deadline."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('old',R/'comb-spine-end-prefix-check.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
assert datetime.now(timezone.utc)<datetime.fromisoformat(old.effort['deadline_utc'])
rows=[]
for n,q in ((0,0),(1,0),(0,1),(2,3)):
    old.deadline();tau=Q(36+28*q);k=9+7*q+(18+14*q)*n
    params=(1,1,1,Q(1,2)+n,Q(1,2)+n,Q(1,3),Q(2,3),2,8+8*q,11+8*q)
    w={'sigma_s':1,'sigma_t':1,'tau':tau,'k_s':k,'k_t':k,'j':3,'r_s':Q(1,3),'r_t':Q(2,3)}
    initial=old.actual_path(*params,w);right=Q(2+n);H=Q(11+8*q)
    teeth=[(Q(0),Q(1)),(Q(2),Q(3)),(Q(8+8*q),Q(9+8*q)),(Q(10+8*q),H)]
    poly=[(Q(0),Q(0)),(right,Q(0))]
    for i,(_,top) in enumerate(teeth):
        poly.append((right,top))
        if i<3:
            lo=teeth[i+1][0];poly.extend([(Q(1),top),(Q(1),lo),(right,lo)])
    poly.append((Q(0),H));old.own.simple(poly)
    result=old.own.path_check(poly,initial['path']);assert result['reflections']==4*k+7
    assert initial['path'][0]==(Q(3,2)+n,Q(7,3)) and initial['path'][-1]==(Q(3,2)+n,Q(25,3)+8*q)
    rows.append({'n':n,'q':q,'k':k,'tau':tau,'actual_source':initial['path'][0],'actual_target':initial['path'][-1],'path':initial['path'],**result})
out={'status':'ALL_FOUR_PRESCRIBED_COMPLETE_SPINE_END_FAMILY_CONTROLS_PASS','rows':rows,'total_reflections':sum(r['reflections'] for r in rows),'total_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{'comb-spine-end-prefix-check.py':hashlib.sha256((R/'comb-spine-end-prefix-check.py').read_bytes()).hexdigest()},'scope':'Four exact controls support a separate hand formula for every integer n,q>=0; no universal comb theorem.'}
(R/'comb-spine-end-family-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_sha256')}))
