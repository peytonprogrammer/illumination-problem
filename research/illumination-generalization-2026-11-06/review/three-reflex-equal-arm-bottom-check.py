"""EA02/EA03 prescribed generalized-L independent ray checks; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil,gcd,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
REQUESTS=[HERE.parent/'construction'/('three-reflex-equal-arm-'+s+'-review-request.json')
          for s in ['bottom','oddpart']]
def pins():
 rows=[]
 for req in REQUESTS:
  for pin in json.loads(req.read_text())['source_pins']:
   actual=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
   assert actual==pin['sha256'];rows.append(dict(pin,actual=actual,passed=True))
 return rows
before=pins();request_pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in REQUESTS]
def v2(n):
 out=0
 while n%2==0:out+=1;n//=2
 return out
src=(HERE/'three-reflex-lower-equal-arm-check.py').read_text()
lower={'__file__':__file__,'v2':v2}
prefix=src.split('\ndef check')[0]
prefix=prefix[:prefix.index('REQUEST=')]+prefix[prefix.index("ns={'Q':Q,'F':Q}"):]
exec(compile(prefix,'<own-pure-wall-setup>','exec'),lower)
fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='check')
code=ast.get_source_segment(src,fn)
code=code.replace('and N%2 and h%2==0','and v2(N)<=v2(P) and h%2==0')
code=code.replace(' and L&(L-1)==0','')
exec(compile(code,'<own-full-Gamma-lower-selector>','exec'),lower)
ns=lower['ns'];fold=ns['fold']
# Explicit negative geometry control: the first frozen EA02 source lies on
# the open inner wall. It contributes no emitted ray or positive case count.
badpoly=[(2,1),(2,6),(20,6),(20,3),(16,3),(16,0),(22,0),(22,12),(0,12),(0,1)]
assert ns['location'](badpoly,(Q(2),Q(4)))==0
rows=[lower['check']('EA02-valid-common-odd-factor',2,3,21,9,1,3,6,12,(2,4),(26,2),Q(790,9)),
      lower['check']('EA03-native-depth-five',2,3,13,6,1,7,8,13,(2,4),(18,2)),
      lower['check']('EA03-native-depth-one',2,3,13,6,1,7,8,13,(2,4),(18,6))]
# Load only own UJ01 algebra and true-wall replay functions, no module tests.
replay_src=(HERE/'three-reflex-coprime-independent-check.py').read_text()
fn=next(n for n in ast.parse(replay_src).body if isinstance(n,ast.FunctionDef) and n.name=='replay_actual')
code=ast.get_source_segment(replay_src,fn)
code=code.replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity,roof_required):')
code=code.replace('velocity=(slope,Q(1))','velocity=initial_velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1','assert len(roofs)==len(horizontal)==int(roof_required)')
code=code.replace('roof=roofs[0]','roof=roofs[0] if roofs else None')
upper={'Q':Q,'ns':ns,'fold':fold,'floor':floor,'ceil':ceil,'gcd':gcd,'lcm':lcm,'v2':v2}
exec(compile(code,'<own-upper-wall-replay>','exec'),upper);upper['replay']=upper['replay_actual']
src=(HERE/'three-reflex-upper-joint-lattice-check.py').read_text()
for name in ['chart','physical','bezout','select']:
 fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name==name)
 code=ast.get_source_segment(src,fn)
 if name=='select':
  code=code.replace('assert N%2 and h%2==0','assert P==K and v2(N)<=v2(P) and h%2==0')
  code=code.replace('H0=gcd(n*g,N*f);V=f*(s-A)+n*z',
   'H0=gcd(n*g,N*f);V=f*(s-A)+n*z\n assert v2(H0)>=min(v2(g),v2(N))')
 exec(compile(code,'<own-general-L-upper-algebra>','exec'),upper)
params=(2,4,4,5,14,1,3,6,12);S=(2,8);T=(22,2)
selection=upper['select'](params,S,T)
assert selection['g']==1 and selection['H0']==1 and v2(14)==1
up=upper['physical']('EA02-upper-small-Gamma-denominator-retained',params,S,T,selection['final_slope'])
rows.append(dict(selection=selection,**up))
assert all(row['Gamma']==3 for row in rows[:3])
out=dict(status='PASS_EA02_EA03_VALID_LOWER_UPPER_FULL_DIVISOR_PHYSICAL_RAYS',
 source_pins_before=before,source_pins_after=pins(),request_pins=request_pins,
 rows=rows,cases=len(rows),reflections=sum(row['reflections'] for row in rows),
 wall_leg_guards=sum(row['wall_leg_guards'] for row in rows),
 rejected_first_EA02_calibration='S(2,4) is on x=a=2 original open wall',
 author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
