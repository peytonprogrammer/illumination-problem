"""Independent A55 whole-interval/far-fiber audit and complete original-wall replay."""
from fractions import Fraction as Q
from pathlib import Path
import ast,importlib.util,json
R=Path(__file__).resolve().parent;P=R.parent/'construction'
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
a=ast.parse((R/'tooth-return-grid-independent-check.py').read_text());nodes=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['read','dims','polygon','image','inside','profile','key']]
for n in nodes:
 if n.name=='profile':n.name='virtual_profile'
exec(compile(ast.Module(body=nodes,type_ignores=[]),'own A54 verifier definitions only','exec'))
def profile(row,p,tooth):
 E=p['virtual_depth'];assert E in (0,2)
 if E==0:assert p['n']==0
 else:
  L,U=Q(p['lo']),Q(p['hi'])
  assert not any(L<i<U for i in range(int(L//1)-1,int(U//1)+2) if i%2)
  if 'tau' in p:
   tau=Q(p['tau']);assert not(tau.denominator==1 and tau.numerator%2==1)
 return virtual_profile(dict(row,D=E),p,tooth)
A=read('seam-four-band-chart-check.json');table={(r['kind'],r['h'],r['d'],r['D']):r for r in A['rows']};assert len(table)==27
expected={('A0',h,None,0) for h in range(5,9)}|{('A1',3,1,0),('A1',4,1,0)}
for d,hs in [(1,range(5,7)),(2,range(5,9)),(3,range(6,11)),(4,range(8,13)),(5,range(10,15))]:expected.update(('A1',h,d,0) for h in hs)
assert expected==set(table)
intervals=finite=0;complement=set()
for k,row in table.items():
 assert [t['tooth'] for t in row['targets']]==[0,1]
 for t in row['targets']:
  assert t['best'];N=t['best']['w_min'];intervals+=profile(row,t['best'],t['tooth'])
  for p in t['intervals']:intervals+=profile(row,p,t['tooth'])
  ws=set()
  for p in t['small_width_witnesses']:finite+=profile(row,p,t['tooth']);assert 1<=p['w']<N and p['w'] not in ws;ws.add(p['w'])
  assert set(range(1,N))-ws==set(t['uncovered_widths'])
 u,v=row['targets'];complement.update((*k,a,b) for a in u['uncovered_widths'] for b in v['uncovered_widths'])
assert len(complement)==82 and {key(z) for z in read('seam-four-band-inputs.json')['cases']}==complement
seeds=read('seam-four-band-seeds.json')['rows'];assert {key(z) for z in seeds}==complement
rows=[];cached={}
def replay(row,data,kind):
 if 'kind' not in row:row=dict(row,kind='A0' if row['d'] is None else 'A1',D=0)
 ident=key(row)
 if ident not in cached:V=polygon(row);g.simple(V);cached[ident]=V
 V=cached[ident];saved=[tuple(map(Q,z)) for z in row['polygon']];assert {frozenset(e) for e in g.edges(V)}=={frozenset(e) for e in g.edges(saved)},('actual geometry mismatch',ident)
 path=[tuple(map(Q,z)) for z in data['path']];assert path[0]==(1,2) and path[-1]==(1,2*row['h']+2)
 assert not any(g.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]));res=g.path_check(V,path);assert res['reflections']==data['reflections'];rows.append({'key':ident,'kind':kind,**res})
for r in seeds:replay(r,r['actual'],'isolated')
print('82 independent actual isolated paths pass',flush=True)
for j,r in enumerate(read('seam-four-band-physical-check.json')['rows']):
 replay(r,r,'formula')
 if j%200==0:print('Independent actual formula paths',j,flush=True)
for r in read('seam-four-band-caps-check.json')['rows']:replay(r,r,'local')
out={'status':'A55_FULL_INTERVAL_FIBER_PRODUCTS_AND_ACTUAL_PATHS_INDEPENDENTLY_PASS','interval_entries':intervals,'finite_width_entries':finite,'complement':82,'rows':rows,'paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False}
(R/'seam-four-band-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
