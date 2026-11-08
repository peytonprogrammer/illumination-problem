"""One predeclared room, every native pair. Verification, not discovery."""
from pathlib import Path
from fractions import Fraction as F
from math import ceil
from itertools import combinations
import ast,json
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('coprime_check',HERE/'prescribed-check.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
ns=core.ns;fold=core.fold
old=ast.parse((core.BASE/'review/three-reflex-tr01-independent-check.py').read_text())
helpers={'point','L_vertical','L_horizontal','U_opposite','U_path'}
ns['F']=F
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef) and f.name in helpers],type_ignores=[]),'<existing-protected-U-L>','exec'),ns)
a,l,w,A,b,c,h,H=map(F,(4,12,16,20,1,5,7,8))
P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
R=[(l,0),(A,0),(A,H),(w,H),(w,c),(l,c)];ns['simple'](P)
points=[(F(x),F(y)) for x in range(0,int(A)+1,2) for y in range(0,int(H)+1,2) if ns['location'](P,(F(x),F(y)))==1]
def inG(p):return p[0]<a or p[1]>=h or (p[0]>w and p[1]>=c)
def inR(p):return ns['location'](R,p)==1
assert all(inG(p) or inR(p) for p in points)
rows=[]
for S,T in combinations(points,2):
 if inG(S) and inG(T):
  region='protected-U';path=ns['U_path'](a,w,A,H-h,H-b,H,(S[0],H-S[1]),(T[0],H-T[1]));path=[(x,H-y) for x,y in path]
 elif inR(S) and inR(T):
  region='protected-L';path=ns['L_horizontal'](A-l,A-w,c,H,(A-S[0],S[1]),(A-T[0],T[1]));path=[(A-x,y) for x,y in path]
 else:
  region='new-coprime-terminal';X,Y=(S,T) if S[0]<a else (T,S)
  assert 0<X[0]<a and b<X[1]<=h and l<Y[0]<A and 0<Y[1]<c
  row=core.replay('whole-room-terminal',4,5,1,5,7,8,X,Y);path=row['path'] if X==S else list(reversed(row['path']))
 # First-arrival truncation uses the same actual target, never a projected copy.
 first=None
 for j,(p,q) in enumerate(zip(path,path[1:])):
  if ns['on'](p,q,T):first=path[:j+1]+[T];break
 assert first is not None and first[0]==S and first[-1]==T
 result=ns['path_check'](P,first)
 rows.append({'S':S,'T':T,'method':region,'path':first,**result})
L=(A-w)/(2*c);dv=L/(ceil(L*h/(2*a))+ceil(L*h/(2*(A-w)))+3);vertical=c+2*A/dv
Lh=(H-h)/(2*a);dh=Lh/(ceil(Lh*w/(2*c))+ceil(Lh*w/(2*(H-h)))+3);horizontal=a+2*H/dh
assert H<vertical and A<horizontal
out={'status':'PASS_ALL_NATIVE_PAIRS_IN_ONE_PRESCRIBED_ROOM','geometry':[a,l,w,A,b,c,h,H],'native_points':points,'pair_count':len(rows),'expected_pairs':len(points)*(len(points)-1)//2,'new_terminal_pairs':sum(r['method']=='new-coprime-terminal' for r in rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'old_vertical_threshold':vertical,'old_horizontal_threshold':horizontal,'fails_both_old_thresholds':True,'rows':rows,'discovery_search_used':False,'general_proof_independent_review':'pending','whole_r3_goal_complete':False}
(HERE/'whole-room-prescribed-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('rows','native_points')},default=str))
