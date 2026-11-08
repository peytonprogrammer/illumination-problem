"""Own fixed support/topology checks for peer critical-B partial reductions."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
helper=ROOT/'surplus-four-local/mixed-root-leaf-review/check.py';s=helper.read_text()
exec(compile(s[:s.index('BDR=')],str(helper),'exec'),globals())
source='third-surplus-review/local-mixed-project.json'
rows=[v for v in read(source)['families']['Bwest_Lcenter']['terms'] if v['source_line']==664]
assert len(rows)==1;t=rows[0];P=decode(t['path']);U,Z=path_requirements(P)
assert U==set(map(tri,t['required_triangles'])) and Z==set(map(tri,t['forbidden_triangles']))
assert P[0]==(0,0) and P[-1]==(2,2) and len(P)-2==12
from boundary_replay import on
for a,b in zip(P[:-2],P[1:-1]):assert not on((2,2),a,b)
peer=read('fourth-surplus-review/mixed-e2-e1/critical-B-check.json');guards={}
def guard(name,path,mi,ma):
 u,z=path_requirements(path);assert u<=mi and not z&ma,name
 us,zs=path_requirements([sigma(p) for p in path[::-1]])
 assert us==tr(u) and zs==tr(z)
 guards[name]={'reflections':len(path)-2,'required':sorted(u),'forbidden':sorted(z),'sigma':'PASS'}
for name,ss in [('Bwest',[1,2,3]),('Brectangle',[0,1,2,3])]:
 mi=H|fan('B',ss)|fan('L',[7,0])|C(['E-']);ma=mi|full('D')|full('R')|full('Tc')|full('N')
 guard(name,P,mi,ma)
 assert mi==set(map(tri,peer['two_whole_family_guards'][name]['minimum']))
 assert ma==set(map(tri,peer['two_whole_family_guards'][name]['maximum']))
 assert Z&fan('E',[3,4]) and Z&fan('E',[4,5])
beast=H|fan('B',[0,1,2])|C(['L+','E-','T-'])
five=decode(read('second-surplus-review/five-path-check.json')['five_path'])
sig13=decode(read('zero-surplus-L/cover-check.json')['paths']['thirteen_sigma']['path'])
guard('Beast_not_Nbplus',five,beast,beast|full('D')|full('R')|(full('N')-C(['Nb+'])))
guard('Beast_Nbplus',sig13,beast|C(['Nb+']),beast|full('D')|full('R')|fan('N',[4,5,6]))
# The ten previously independently accepted paths, rebuilt in OWN setup.
transfer={}
for name,path in paths.items():
 u,z=path_requirements(path);assert not (u|z)&full('D'),name
 transfer[name]='FULL_D_U_AND_Z_AVOIDANCE_PASS'
assert len(transfer)==10

def angle(ts,p):
 owners=g.owners_of(list(ts));opens={e for e,ii in owners.items() if len(ii)==2}
 aa,inside=g.check_fan_angles(list(ts),p,owners,opens)
 if inside:return 360
 assert len(aa)==1,(p,aa)
 return 45*aa[0]
forcing={}
for name,ss in [('west',[1,2,3]),('rectangle',[0,1,2,3])]:
 base=H|fan('B',ss)
 vals={n:angle(base|fan('L',fs),(-1,-1)) for n,fs in [('empty',[]),('reference',[0]),('outer',[0,1]),('center',[7,0])]}
 assert vals=={'empty':180,'reference':180,'outer':180,'center':225}
 assert all((-1,-1) not in t for n in ['D','R','E','Tc','N'] for t in full(n))
 forcing[name]=vals
windows=[]
for m in [3,4]:
 for start in range(8):
  ss={(start+i)%8 for i in range(m)}
  if 1 not in ss:continue
  kind='joined' if {7,0}<=ss else 'excluded' if {3,4}<=ss else 'no_join'
  if kind=='excluded':
   assert angle(H|fan('B',ss),(-1,-2))==180
   assert all((-1,-2) not in t for n in ['L','D','R','E','Tc','N'] for t in full(n))
  windows.append({'m':m,'start':start,'sectors':sorted(ss),'category':kind})
assert [sum(v['category']==k for v in windows) for k in ['no_join','joined','excluded']]==[3,3,1]
joined=[]
for label,ss,h in [('O3',[7,0,1],0),('O4',[6,7,0,1],0),('H4',[7,0,1,2],1)]:
 base=H|fan('B',ss);old=base|fan('D',[3]);new=base|fan('D',[2,3])
 assert angle(old,(1,-2))==angle(new,(1,-2))==270
 assert angle(old,(1,-1))==315 and angle(new,(1,-1))==360
 assert angle(new,(0,-1))==270+90*h
 assert angle(new,(2,-1))==270
 assert all(p not in t for n in ['L','R','E','Tc','N'] for t in full(n) for p in [(1,-2),(1,-1),(0,-1)])
 assert all(p not in t for t in fan('D',[2]) for p in [(-1,-1),(-1,1),(1,3),(3,3),(3,-1)])
 for c in [0,1]:
  J=3+h+c;n=2+h+c;Q=7+n;sN=12-Q
  assert J+sN==6 and n==J-1
 joined.append({'B':label,'old_shared_B':315,'new_full_B':360,'shared_C':270,'H_C':270+90*h,'new_D_H_C':270,'budget':'J3+h+c,n2+h+c'})
# The single declared local return, not a new optical itinerary.
entry=(F(3),F(16,11));oldexit=(F(3),F(19,12));newexit=(F(3),F(18,11))
contacts=[entry,(F(7,2),F(2)),(F(4),F(16,11)),(F(43,12),F(1)),newexit]
vv=[(11,12),(11,-12),(-11,-12),(-11,12)]
for a,b,v in zip(contacts,contacts[1:],vv):
 dv=sub(b,a);assert cross(dv,v)==0 and sum(x*y for x,y in zip(dv,v))>0
 assert all(3<=p[0]<=4 and 1<=p[1]<=2 for p in [a,b])
assert oldexit!=newexit and vv[-1]!=(-12,-11)
assert P[3:6]==[(F(7,2),F(2)),(F(86,23),F(40,23)),(F(38,11),F(2))]
u6,z6=path_requirements(paths['Ecenter6']);L7=fan('L',[7]);assert L7<=z6
out={'status':'INDEPENDENT_CRITICAL_B_PARTIAL_REDUCTIONS_CHECKS_PASS','whole_guards':guards,
 'ten_D_invariant_paths':transfer,'L_forcing':forcing,'seven_B_windows':windows,'three_joined_templates':joined,
 'E_square_attempt':'EXIT_POSITION_AND_VELOCITY_MISMATCH','Ecenter6_rescue':'BLOCKED_BY_L7',
 'retained_source_line':664,'source_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
 'fourth-surplus-review/mixed-e2-e1/critical-B.txt','fourth-surplus-review/mixed-e2-e1/critical-B-check.json',source,
 'surplus-four-local/mixed-root-leaf-review/check.py','surplus-four-local/mixed-root-leaf-review/review.txt']},
 'limits':'Only named retained664,4 whole envelopes,10 accepted paths,7 local windows,3 joins and prescribed local return. No peer checker execution/new completed room/path/direction/word or archive search. Hand transfer of six necessary rows reviewed separately.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
