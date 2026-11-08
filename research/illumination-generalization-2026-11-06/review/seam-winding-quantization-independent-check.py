"""A59 independent finite post-quantization tables and prescribed actual winding paths."""
from pathlib import Path
from fractions import Fraction as Q
import ast,importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
ns={'Q':Q,'g':g};tree=ast.parse((R/'tooth-free-core-independent-check.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='trace'],type_ignores=[]),'own firsthit','exec'),ns)
def allphases(q,H):
 lo=q*H-(1+q)/2;hi=q*H+(1+q)/2
 return [(q*H-n)/(1+q) for n in range(max(0,int(lo//1)),int(hi//1)+2) if lo<n<hi]
def first(q,H):
 n=int((q*(H-Q(1,2))+Q(1,2))//1);return n,(q*H-n)/(1+q)
def contour(c,h,G,Y,ws,wt,a,b):
 t=2*h+2;V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,t-1),(c+wt,t-1),(c+wt,t+1),(c,t+1),(c,G),(0,G),(0,Y+2),(-b,Y+2),(-b,Y),(0,Y),(0,h+2),(-a,h+2),(-a,h),(0,h)]
 return [tuple(map(Q,z)) for z in V]
shapes=[('A0',3,0),('A0',5,0),('A1',3,2),('A1',3,6),('A1',3,7),('A1',3,10)]
tables=[];paths=[];rotation=0
for kind,h,d in shapes:
 G=2*h+4 if kind=='A0' else 2*h+d+4;Y=h+4 if kind=='A0' else h+d+2;t=2*h+2
 # Derive constraints from actual opening orientations and local fold derivative.
 constraints=[]
 for image in [t,t+2*G,-t,-t-2*G]:
  mean=Q(2+image,2);H=Q(abs(image-2),2);res=mean%(2*G);assert res not in [0,G]
  physical=g.fold(mean,Q(G));derivative=1 if res<G else -1
  if physical in [h,Y]:protected=-1
  elif physical in [h+2,Y+2]:protected=1
  else:raise AssertionError('nominal not actual mouth endpoint')
  role=1 if image>2 else -1
  constraints.append((H,protected*derivative*role))
 qs=[];qt=[]
 for numerator in range(1,2*G+1):
  q=Q(numerator,2*G)
  if all(sign*m<=0 for H,sign in constraints for m in allphases(q,H)):qs.append(str(q))
  if all(sign*m>=0 for H,sign in constraints for m in allphases(q,H)):qt.append(str(q))
 tables.append({'kind':kind,'h':h,'d':d,'source':qs,'target':qt,'pairs':len(qs)*len(qt),'source_illumination_signs':[(str(H),s) for H,s in constraints]})
 for j in [0,1,3]:
  for role in ['source','target']:
   c=Q(11,3);H=Q(h+2*j*G if role=='source' else h+2+2*j*G);q=Q(2);n,m=first(q,H);assert m>0
   tau=Q(H+n,3*c);ws=2*c if role=='source' else c/7;wt=c/7 if role=='source' else 2*c
   V=contour(c,h,G,Y,ws,wt,Q(1,191),Q(100103));g.simple(V)
   S=(c,Q(2 if role=='source' else t));T=(c,Q(t if role=='source' else 2));v=(Q(1),(-1)**n*tau*(1 if role=='source' else -1))
   expected=n+2+4*j+(role=='target');path,_=ns['trace'](V,S,T,v,expected);out=g.path_check(V,path);paths.append({'kind':kind,'h':h,'d':d,'j':j,'far_physical_endpoint':role,'H':H,'n':n,'tau':tau,**out})
 # Prescribed rational orbit controls, not a substitute for all-real Cesaro proof.
 for den in range(2,42):
  for num in range(1,den):
   q=Q(num,den);theta=2*G*q
   if theta.denominator==1:continue
   for H0 in [h,h+2]:
    assert any(first(q,Q(H0+2*j*G))[1]>0 for j in range(theta.denominator));rotation+=1
assert sum(z['pairs'] for z in tables)==37
expected=[(['1/4','1'],['1']),(['5/28','1'],['1/4','1']),(['1/4','1'],['1/3','1']),(['1/4','5/8','1'],['1/8','3/8','1']),(['4/17','1'],['2/17','6/17','1']),(['1/5','1/4','3/5','1'],['7/20','2/5','1'])]
assert [(z['source'],z['target']) for z in tables]==expected
pins=json.loads((P/'seam-winding-quantization-review-request.json').read_text())['source_sha256']
for f,h in pins.items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'A59_INDEPENDENT_ACTUAL_WINDINGS_AND_EXACT_RATIO_TABLE_PASS','whole_goal_complete':False,'author_code_executed':False,'selected_ratio_pairs':37,'tables':tables,'actual_paths':len(paths),'reflections':sum(z['reflections'] for z in paths),'wall_leg_guards':sum(z['wall_leg_guards'] for z in paths),'rational_orbit_controls':rotation,'paths':paths,'source_pins':pins}
(R/'seam-winding-quantization-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['tables','paths','source_pins']})
