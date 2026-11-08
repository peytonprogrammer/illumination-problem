from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
from math import floor,ceil
import ast,json,hashlib
ROOT=Path(__file__).resolve().parent;E=json.loads((ROOT/'seam-four-band-effort.json').read_text());assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
source=ROOT.parent/'review'/'resumed-exact-check.py';tree=ast.parse(source.read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'};ns={'Q':F};exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names],type_ignores=[]),str(source),'exec'),ns)
# Only helper definitions from the author-side physical constructor, no main loop.
g={'ROOT':ROOT,'E':E,'ns':ns,'F':F,'floor':floor,'ceil':ceil,'datetime':datetime,'timezone':timezone}
tree=ast.parse((ROOT/'seam-four-band-physical-check.py').read_text());exec(compile(ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef)],type_ignores=[]),'author_helper_definitions','exec'),g)
def polygon(h,d,a,b):
 G=2*h+(4 if d is None else d+4);Y2=h+(4 if d is None else d+2);t=2*h+2
 V=[(0,0),(1,0),(1,1),(2,1),(2,3),(1,3),(1,t-1),(2,t-1),(2,t+1),(1,t+1),(1,G),(0,G),(0,Y2+2),(-b,Y2+2),(-b,Y2),(0,Y2),(0,h+2),(-a,h+2),(-a,h),(0,h)];return [tuple(map(F,q)) for q in V]
cap3=[(1,2),(0,F(2,3)),(F(1,2),0),(1,F(2,3)),(0,2),(1,F(10,3)),(-F(1,4),5),(-1,4),(-F(1,4),3),(1,F(14,3)),(0,6),(2,F(26,3)),(F(7,4),9),(1,8)]
cap4=[(1,2),(F(1,3),0),(0,1),(1,4),(0,7),(1,10)]
rows=[]
for h,d,a,b in ((3,None,1,17),(3,2,1,23),(3,1000000,1,37),(4,None,3,11),(4,2,17,2),(4,1000000,37,19)):
 V=polygon(h,d,a,b);ns['simple'](V);path=[tuple(map(F,q)) for q in(cap3 if h==3 else cap4)];check=ns['path_check'](V,path)
 for i,(p,q) in enumerate(zip(path,path[1:])):
  if ns['on'](p,q,path[-1]):assert i==len(path)-2
 rows.append({'h':h,'d':d,'a':a,'b':b,'polygon':V,'S':path[0],'T':path[-1],'path':path,**check})
for a,d in ((2,None),(3,None),(5,None),(37,None),(2,2),(37,1000000)):
 k=(a-1)//2+1;tau=F(3+2*k,a+2);assert 1<tau<F(5,3)
 z={'kind':'A0' if d is None else'A1','h':3,'d':d,'D':0};G=10 if d is None else d+10
 v={'virtual_depth':0,'n':0,'l':1,'r':2,'k':k,'tau':tau,'w':a,'tooth':0,'G':G,'Y':3,'H':3,'target_copy':8};rows.append(g['build'](z,v,23))
assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline']);out={'status':'ALL_LITERAL_CAPS_AND_ZERO_ARM_H3_FORMULAS_PASS','rows':rows,'paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'all_wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'accepted_validator_definitions_reused':True,'discovery':False,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False};(ROOT/'seam-four-band-caps-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
