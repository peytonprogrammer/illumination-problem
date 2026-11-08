"""Independent joint source/grid cap orbit, four prescribed actual rays."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
assert source.count('extension-sourcewide-')==3
source=source.replace('extension-sourcewide-','extension-jointshift-').replace("['candidate.md','proof.md','check.py']","['candidate.md','proof.md','check.py','check.json']")
changes={
 'delta=gcd(P*C,N);Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1':
 'sourceG=gcd(d0,P*D,P*d2);Qsrc=Q(P,sourceG);delta=gcd(P*C,N*sourceG);Lam=lcm(P,N,K);assert delta<K*sourceG and gcd(Lam*d2,L)==1;assert all((Qsrc*x).denominator==1 for x in (D,d2,D-d2)) and (Qsrc*d0/P).denominator==1',
 'point=(A-X0)/(2*e*delta)':'point=(A-X0)*sourceG/(2*e*delta)',
 'M=nearest*pow(P*C//delta,-1,N//delta)%(N//delta)':'M=nearest*pow(P*C//delta,-1,N*sourceG//delta)%(N*sourceG//delta)',
 'tau=tau0+2*e*P*M;n+=d0*M':'tau=tau0+2*e*Qsrc*M;n+=(d0//sourceG)*M',
 'cap_gcd=delta,slope=':'cap_gcd=delta,source_grid_gcd=sourceG,source_grid_coefficient=Qsrc,effective_cap_gcd=Q(delta,sourceG),slope='
}
for old,new in changes.items():
 assert source.count(old)==1,old
 source=source.replace(old,new)
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_joint_source_grid_constructor'}
exec(compile(source,'<own-physical-constructor-with-joint-cap-orbit>','exec'),ns)
before=ns['capture']()
fixtures=[
 ('CE07-nominated',4,1,2,3,8,1,4,6,7,(2,4),(26,2),1),
 ('CE07-source-h',4,1,2,3,8,1,4,6,7,(2,6),(26,2)),
 ('CE07-upper-cap',4,1,2,3,8,1,4,5,7,(2,6),(26,2)),
 ('CE07-P3-half-step',2,3,2,5,16,1,4,6,7,(2,4),(24,2))]
rows=[ns['ray'](*f) for f in fixtures]
row=rows[0];assert (row['slope'],row['finalJ'],row['M'],row['target_shift'],row['source_grid_coefficient'])==(Q(291,2),36,3,2,Q(1,2))
assert rows[-1]['source_grid_coefficient']==Q(3,2)
old=[(8+16*j)%64 for j in range(4)];assert old==[8,24,40,56] and all(not 24<x<40 for x in old)
out=dict(status='PASS_INDEPENDENT_CE07_JOINT_GRID_ACTUAL_RAYS',request_present=ns['REQUEST'].exists(),source_pins_before=before,source_pins_after=ns['capture'](),rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),old_cap_orbit=old,author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows')}))
