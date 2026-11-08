"""Independent A54 whole-interval arithmetic, finite-product exhaustion, original-wall replay."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def read(f):return json.loads((P/f).read_text())
def dims(row):
 h=row['h'];d=row.get('d');G=2*h+4 if row.get('kind','A1')=='A0' else 2*h+d+4;Y2=h+4 if row.get('kind','A1')=='A0' else h+d+2
 return G,Y2
def polygon(row):
 h,D,a,b=row['h'],row['D'],row['a'],row['b'];G,Y2=dims(row)
 return [tuple(map(Q,z)) for z in [(0,0),(1,0),(1,1),(D+2,1),(D+2,3),(1,3),(1,2*h+1),(D+2,2*h+1),(D+2,2*h+3),(1,2*h+3),(1,G),(0,G),(0,Y2+2),(-b,Y2+2),(-b,Y2),(0,Y2),(0,h+2),(-a,h+2),(-a,h),(0,h)]]
def image(a,b,L,U):return tuple(sorted([a+b*L,a+b*U]))
def inside(a,b,L,U,lo,hi):
 x,y=image(a,b,L,U)
 assert lo<=x<=y<=hi
 if b==0:assert lo<x<hi

def profile(row,p,tooth):
 h,D=row['h'],row['D'];G,Y2=dims(row);n,l,r=p['n'],p['l'],p['r'];L,U=Q(p['lo']),Q(p['hi']);tc=p['target_copy'];Y=p['Y'];H=Q(tc-2,2)
 assert n>=0 and l>=1 and r>=1 and 0<L<U and tc in (2*h+2,2*G-2*h-2) and H==p['H'] and G==p['G']
 actualY=h if tooth==0 else Y2;assert Y in (actualY,2*G-actualY-2)
 inside(-2*n,D,L,U,-1,1);inside(2-2*n,D+2*l-1,L,U,Y,Y+2);inside(tc+2*n,-D-2*r+1,L,U,Y,Y+2)
 right=[(1,3),(2*h+1,2*h+3)];left=[(h,h+2),(Y2,Y2+2)]
 for aa,sg,count in [(2-2*n,1,2*l-2),(tc+2*n,-1,2*r-2)]:
  for j in range(1,count+1):
   bb=sg*(D+j);x,y=image(aa,bb,L,U);assert 0<=x<y<=2*G and (y<=G or x>=G)
   bands=left if j%2 else right;bands=bands+[(2*G-hi,2*G-lo) for lo,hi in bands]
   assert all(y<=lo or x>=hi for lo,hi in bands)
 C=H+2-Y;assert C==p['far_phase_constant']
 if l==r:assert C.denominator==1 and C.numerator%2==1;K=2
 else:K=4
 N=max(1,int((Q(K)/(U-L))//1)-(D+l+r-1)+1);assert p['w_min']>=N
 if 'tau' in p:
  tau=Q(p['tau']);w=p['w'];k=p['k'];assert k>=0 and L<tau<U and tau==Q(H+2*n+2*k,w+D+l+r-1)
  phase=C+2*k+(l-r)*tau;assert phase==Q(p['far_phase']) and not(phase.denominator==1 and phase.numerator%2==0)
 return 1
T=read('tooth-return-grid-end-check.json');table={(z['kind'],z['h'],z['d'],z['D']):z for z in T['rows']};assert len(table)==76
intervals=finite=0
for row in table.values():
 assert [x['tooth'] for x in row['targets']]==[0,1]
 for t in row['targets']:
  for p in t['intervals']:intervals+=profile(row,p,t['tooth'])
  if t['best']:
   intervals+=profile(row,t['best'],t['tooth']);N=t['best']['w_min'];ws=set()
   for p in t['small_width_witnesses']:finite+=profile(row,p,t['tooth']);assert 1<=p['w']<N;assert p['w'] not in ws;ws.add(p['w'])
   assert set(t['uncovered_widths'])==set(range(1,N))-ws
large=set()
for D in [1,2]:
 keys=[('A0',h,None,D) for h in range(5,9)]
 for d,hs in [(1,range(5,7)),(2,range(5,9)),(3,range(6,11)),(4,range(8,13)),(5,range(10,15))]:keys.extend(('A1',h,d,D) for h in hs)
 for key in keys:
  row=table[key];u,v=row['targets'];assert u['best'] and v['best']
  large.update((*key,a,b) for a in u['uncovered_widths'] for b in v['uncovered_widths'])
def key(row):return(row.get('kind','A1'),row['h'],row.get('d'),row['D'],row['a'],row['b'])
assert len(large)==308 and {key(z) for z in read('tooth-return-grid-large-inputs.json')['cases']}==large
low=set()
for D in [1,2]:
 row=table['A1',3,1,D];u,v=row['targets'];low.update(('A1',3,1,D,a,b) for a in u['uncovered_widths'] for b in v['uncovered_widths'])
assert len(low)==163
h4={('A1',4,2,1,a,b) for a in [2,3,4,8] for b in [2,3,4,8]}
row=table['A1',4,2,1];assert {('A1',4,2,1,a,b) for a in row['targets'][0]['uncovered_widths'] for b in row['targets'][1]['uncovered_widths']}==h4
for k in [('A0',4,None,1),('A1',4,1,1),('A1',4,1,2)]:assert any(not t['uncovered_widths'] and t['best'] for t in table[k]['targets'])
rows=[];cached={};geometry_mismatches=[]
def replay(row,data,category):
 ident=key(row)
 if ident not in cached:
  V=polygon(row);g.simple(V);cached[ident]=V
 V=cached[ident];saved=[tuple(map(Q,z)) for z in row['polygon']]
 if {frozenset(e) for e in g.edges(V)}!={frozenset(e) for e in g.edges(saved)}:geometry_mismatches.append({'key':ident,'saved_roof':str(max(z[1] for z in saved)),'required_roof':str(max(z[1] for z in V)),'resolution':'Full actual path checked against required theorem polygon below, no saved-polygon inference'})
 path=[tuple(map(Q,z)) for z in data['path']];assert path[0]==(1+row['D'],2) and path[-1]==(1+row['D'],2*row['h']+2)
 assert not any(g.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
 res=g.path_check(V,path);assert res['reflections']==data['reflections'];rows.append({'key':ident,'category':category,**res})
for f,needed in [('tooth-return-grid-large-seeds.json',large),('tooth-return-grid-small-seeds.json',low),('tooth-return-grid-seeds.json',h4)]:
 seeds=read(f)['rows'];assert needed<={key(z) for z in seeds}
 if f!='tooth-return-grid-small-seeds.json':assert needed=={key(z) for z in seeds}
 for row in seeds:replay(row,row['actual'],'isolated')
 print('independent seeds checked',f,len(seeds),flush=True)
for f in ['tooth-return-grid-physical-check.json','tooth-return-grid-low-physical-check.json']:
 for j,row in enumerate(read(f)['rows']):
  replay(row,row,'formula')
  if j%300==0:print('independent formula rows',f,j,flush=True)
print('All full profile and original-wall checks pass',flush=True)
out={'status':'A54_FULL_INTERVAL_PRODUCTS_AND_ACTUAL_PATHS_INDEPENDENTLY_PASS','geometry_mismatches':geometry_mismatches,'interval_profiles':intervals,'finite_width_formula_certificates':finite,'large_complement':308,'low_complement':163,'h4_complement':16,'rows':rows,'paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False}
(R/'tooth-return-grid-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
