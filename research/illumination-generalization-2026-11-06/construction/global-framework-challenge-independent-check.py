"""Prescribed R58 review; no optical discovery and no R58 author code execution."""
from fractions import Fraction as Q
from pathlib import Path
import ast,hashlib,json,math
HERE=Path(__file__).resolve().parent
source=HERE.parent/'review/resumed-exact-check.py'
names={'vec','det','dot','edges','on','location','intersect','simple','path_check'}
a=ast.parse(source.read_text());ns={'Q':Q}
exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(source),'exec'),ns)
p=[(-1000,-2),(-2,-2),(-2,-10),(2,-10),(2,-2),(10,-2),(10,0),(8,2),(2,2),(2,10),(0,10),(-2,8),(-2,2),(-1000,2)]
ns['simple'](p)
area=Q(abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in ns['edges'](p))),2)
boundary=sum(math.gcd(abs(b[0]-a[0]),abs(b[1]-a[1])) for a,b in ns['edges'](p))
interior=area-boundary/2+1
assert area==4100 and boundary==2056 and interior==3073
A=sum(ns['location'](p,(x,y))==1 for x in range(-1000,11,2) for y in range(-10,11,2))
assert A==512
sN=sum(ns['location'](p,(x,y))==0 for x in range(-1000,11) for y in range(-10,11) if x%2 or y%2)
J=int(interior)-A
assert J==2561 and sN==1028
S,T=(-998,0),(0,8)
assert ns['location'](p,S)==ns['location'](p,T)==1
assert ns['location'](p,(-499,4))==-1
path=[S]+[(Q(-998)+Q(2*j-1,2),Q(2*(-1)**(j+1))) for j in range(1,997)]+[T]
actual=ns['path_check'](p,path)
assert actual['reflections']==996
control=[(0,0),(Q(90,11),Q(20,11)),(Q(22,3),-2),(Q(58,9),2),(6,0)]
small=ns['path_check'](p,control)
assert small['reflections']==3
filled=[(-1000,-2),(-2,-2),(-2,-10),(2,-10),(2,-2),(10,-2),(10,2),(2,2),(2,10),(-2,10),(-2,2),(-1000,2)]
ns['simple'](filled);assert ns['location'](filled,control[1])==1
n=(1,2);v=(18,2)
ref=tuple(v[i]-2*Q(ns['dot'](v,n),ns['dot'](n,n))*n[i] for i in (0,1))
assert ref==(Q(46,5),Q(-78,5)) and ns['det'](ref,(-4,-9))!=0
pins=json.loads((HERE.parent/'review/global-framework-challenge-review-request.json').read_text())['source_sha256']
verified={f:hashlib.sha256((HERE.parent/'review'/f).read_bytes()).hexdigest()==h for f,h in pins.items()}
assert all(verified.values())
result={'status':'PASS','scope':'Prescribed exact paths and independent Pick/lattice count; hand proof supplies tiling without rerunning 8200-triangle reconstruction. Shared validator disclosed.','area':str(area),'boundary_lattice_points':boundary,'interior_lattice_points':int(interior),'interior_A':A,'J':J,'s_N':sN,'k':J+sN,'main_path':actual,'separate_control':small,'all_peer_pins_current':verified,'whole_goal_complete':False}
(HERE/'global-framework-challenge-independent-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
