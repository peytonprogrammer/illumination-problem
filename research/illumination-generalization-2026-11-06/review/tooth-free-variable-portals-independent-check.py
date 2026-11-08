"""A57 supplement exact prescribed independent first-hit and equality controls."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib,itertools
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('base',R/'tooth-free-core-independent-check.py')
# Load only independent function definitions, avoiding its top-level control writer.
import ast
ns={'Q':Q};tree=ast.parse((R/'tooth-free-core-independent-check.py').read_text())
spec=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);ns['g']=g
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['contour','trace']],type_ignores=[]),'own firsthit definitions','exec'),ns)
def matching(c,ds,dt):
 L=4*c+ds+dt;n=(0,0);steps=0;B=(14*(ds+dt)+L)/(4*c);B=-(-B//1)
 while True:
  tau=(28+2*sum(n))/L;nn=tuple(int(d*tau/2+Q(1,2)) for d in [ds,dt]);assert all(a<=b for a,b in zip(n,nn)) and sum(nn)<=B
  if nn==n:break
  n=nn;steps+=1;assert steps<=B+1
 delta=tuple(d*tau-2*k for d,k in zip([ds,dt],n));assert all(-1<x<1 for x in delta)
 assert 4*c*tau==28-sum(delta)
 return tau,n,delta,steps
rows=[];ties=0
for c,ds,dt in itertools.product([Q(1,7),Q(1),Q(11),Q(121)],[Q(0),Q(1),Q(3,2),Q(11)],[Q(0),Q(2,3),Q(3),Q(7)]):
 tau,n,delta,steps=matching(c,ds,dt)
 V=ns['contour'](c,ds+Q(1,103),dt+Q(5,109),Q(1,113),Q(100003));g.simple(V)
 path,_=ns['trace'](V,(c+ds,Q(2)),(c+dt,Q(8)),(Q(-1),(-1)**n[0]*tau),sum(n)+5)
 out=g.path_check(V,path);rows.append({'c':c,'Ds':ds,'Dt':dt,'tau':tau,'indices':n,'deltas':delta,'steps':steps,**out})
# Exact inadmissible fixed points with a negative portal equality exist; leastness matters.
# Generate a tie by Ds*tau=2n-1 and solve c from the closure equation.
for Ds,nt,n in itertools.product([Q(1),Q(2),Q(5)],[0,1,2],[1,2,3]):
 tau=Q(2*n-1,Ds);Dt=Q(2*nt,tau);c=(28+2*(n+nt)-tau*(Ds+Dt))/(4*tau)
 if c<=0:continue
 eq=(int(Ds*tau/2+Q(1,2)),int(Dt*tau/2+Q(1,2)))
 assert eq==(n,nt)
 actual=matching(c,Ds,Dt);assert actual[0]<tau and all(-1<x<1 for x in actual[2]);ties+=1
pins=json.loads((P/'tooth-free-variable-portals-review-request.json').read_text())['source_sha256']
for f,h in pins.items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'A57_VARIABLE_PORTALS_INDEPENDENT_FIRST_HIT_PASS','whole_goal_complete':False,'author_code_executed':False,'actual_paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'negative_equality_nonleast_fixedpoint_controls':ties,'source_pins':pins,'rows':rows}
(R/'tooth-free-variable-portals-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_pins']})
