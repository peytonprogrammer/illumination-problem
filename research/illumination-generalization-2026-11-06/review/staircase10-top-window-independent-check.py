"""Eight prescribed exact ST10-B proof checks; independent selector, no search."""
import ast,hashlib,json
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path('.context/illumination-generalization-2026-11-06');HERE=ROOT/'review'
inputs=json.loads((HERE/'staircase10-top-window-independent-inputs.json').read_text())
for p in inputs['author_pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
geo=Path(inputs['geometry_source']);assert hashlib.sha256(geo.read_bytes()).hexdigest()==inputs['geometry_sha256']
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold','nested_polygon'}
ns={'Q':Q,'F':Q}
exec(compile(ast.Module(body=[f for f in ast.parse(geo.read_text()).body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<existing reviewer pure physical guards>','exec'),ns)
def ceil(x):return -((-x)//1)
def period_center(x,w):return 2*w*((x/(2*w)+Q(1,2))//1)
def affine_image(J,s,T,C):return (s+J[0]*T-C,s+J[1]*T-C)
def strict_overlap(J,w):
 center=period_center(sum(J)/2,w[0]);a=w[1]
 out=(max(J[0],center-a),min(J[1],center+a))
 assert out[0]<out[1]
 return out,center

def check_case(row):
 w=list(map(Q,row['w']));y=list(map(Q,row['y']));s,u=map(Q,row['S']);t,v=map(Q,row['T'])
 assert u<=v and y[0]==0 and all(w[i]>w[i+1]>0 for i in range(3))
 assert all(y[i]<y[i+1] for i in range(4)) and y[3]<=v<y[4]
 H=y[4];E2=min(2*w[2],w[2]+w[1]*(y[2]-y[1])/y[1]);r=E2*y[3]/(2*y[2]);E3=min(2*w[3],2*r,r+w[3]-w[2])
 assert H*E3/y[3]>=2*w[3]
 if row['label'].startswith('B_exact_equality'):assert H*E3/y[3]==2*w[3]
 poly=ns['nested_polygon'](w,y);ns['simple'](poly)
 i=max(k for k in range(4) if y[k]<=u)
 if i==3:
  result=ns['path_check'](poly,[(s,u),(t,v)])
  return dict(label=row['label'],source_band=i,method='convex top direct',criterion_span=H*E3/y[3],**result)
 C={i:Q(0)};bounds={};sigma=Q(1);forced='prescribed_tau' in row
 if forced:
  tau=Q(row['prescribed_tau']);sigma=Q(row['prescribed_sigma']);C=dict(enumerate(map(Q,row['prescribed_C'])));nominal_eta=Q(row['nominated_eta'])
 else:
  if i==0:
   C[1]=2*w[0];T1=y[1]-u
   J=((C[1]-s-w[1])/T1,(C[1]-s+w[1])/T1);assert 0<J[0]<J[1]
   T2=y[2]-u;U=affine_image(J,s,T2,C[1]);overlap,K=strict_overlap(U,(w[1],w[2]));ell2=overlap[1]-overlap[0]
   assert ell2>=E2
   J=((overlap[0]+C[1]-s)/T2,(overlap[1]+C[1]-s)/T2);C[2]=C[1]+K
   bounds['ell2']=ell2
  elif i==1:
   C[2]=2*w[1];T2=y[2]-u
   J=((C[2]-s-w[2])/T2,(C[2]-s+w[2])/T2);assert 0<J[0]<J[1]
   ell2=2*w[2];bounds['ell2']=ell2
  if i<=1:
   T2=y[2]-u;T3=y[3]-u
   U=affine_image(J,s,T3,C[2]);R3=(U[1]-U[0])/2;assert R3>r
   overlap,K=strict_overlap(U,(w[2],w[3]));ell3=overlap[1]-overlap[0];assert ell3>=E3>0
   J=((overlap[0]+C[2]-s)/T3,(overlap[1]+C[2]-s)/T3);C[3]=C[2]+K
   nominal_eta=2*H-v;D=nominal_eta-u
   image_interval=affine_image(J,s,D,C[3]);assert image_interval[1]-image_interval[0]>2*w[3]
   bounds.update(R3=R3,ell3=ell3,terminal_span=image_interval[1]-image_interval[0])
  else:
   C[3]=2*w[2];T3=y[3]-u;J=((C[3]-s-w[3])/T3,(C[3]-s+w[3])/T3)
   assert 0<J[0]<J[1]
   nominal_eta=v;D=v-u;image_interval=affine_image(J,s,D,C[3]);assert image_interval[1]-image_interval[0]>=2*w[3]
  # Deliberately choose LAST strict image BELOW the upper endpoint, unlike author first above lower.
  image=max(sign*t+2*w[3]*(ceil((image_interval[1]-sign*t)/(2*w[3]))-1) for sign in (-1,1))
  assert image_interval[0]<image<image_interval[1]
  tau=(C[3]+image-s)/(nominal_eta-u);assert J[0]<tau<J[1] and tau>0
 for k in range(i+1,4):
  old=s+sigma*tau*(y[k]-u)-C[k-1]
  residual=s+sigma*tau*(y[k]-u)-C[k]
  assert abs(residual)<w[k]
  assert ((C[k]-C[k-1])/(2*w[k-1])).denominator==1
  assert ns['fold'](old,w[k-1])==ns['fold'](residual,w[k])
 assert ns['fold'](s+sigma*tau*(nominal_eta-u)-C[3],w[3])==t
 roof_phase=s+sigma*tau*(H-u)-C[3]
 roof_corner=(roof_phase/w[3]).denominator==1
 earlier=ns['fold'](s+sigma*tau*(v-u)-C[3],w[3])==t
 eta_end=v if earlier else nominal_eta
 if forced:
  assert roof_corner and earlier and eta_end==Q(row['actual_earlier_eta'])
 knots={u,eta_end}
 for Y in y[1:]:
  if u<Y<eta_end:knots.add(Y)
 for k in range(i,4):
  lo=max(u,y[k]);hi=min(eta_end,y[k+1]) if k<3 else eta_end
  if lo>=hi:continue
  A=s+sigma*tau*(lo-u)-C[k];B=s+sigma*tau*(hi-u)-C[k]
  for n in range(int(min(A,B)//w[k])-1,int(ceil(max(A,B)/w[k]))+2):
   eta=u+(n*w[k]+C[k]-s)/(sigma*tau)
   if lo<eta<hi:knots.add(eta)
 def at(eta):
  k=min(3,max(j for j in range(4) if y[j]<=eta))
  return (ns['fold'](s+sigma*tau*(eta-u)-C[k],w[k]),eta if eta<=H else 2*H-eta)
 path=[at(eta) for eta in sorted(knots)]
 assert path[0]==(s,u) and path[-1]==(t,v)
 result=ns['path_check'](poly,path)
 roofs=[];horizontal=[]
 for p in path[1:-1]:
  walls=[(a,b) for a,b in ns['edges'](poly) if ns['on'](a,b,p)]
  if walls:
   assert len(walls)==1 and p not in poly
   a,b=walls[0]
   if a[1]==b[1]:horizontal.append(p);assert p[1]==H;roofs.append(p)
 assert len(horizontal)<=1
 # The only possible visits to target height are eta=v and eta=2H-v; earlier check retained exactly.
 assert eta_end==v or (not earlier and eta_end==2*H-v)
 return dict(label=row['label'],source_band=i,tau=tau,initial_horizontal_sign=sigma,C=C,criterion_span=H*E3/y[3],bounds=bounds,nominal_target_time=nominal_eta-u,actual_first_target_time=eta_end-u,roof_phase=roof_phase,roof_corner_candidate=roof_corner,earlier_target_retained=earlier,ordinary_roof_reflections=len(roofs),path=path,**result)
rows=[check_case(row) for row in inputs['cases']]
for p in inputs['author_pins']:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
assert hashlib.sha256(geo.read_bytes()).hexdigest()==inputs['geometry_sha256']
out={'status':'PASS_EIGHT_PRESCRIBED_ST10_B_BOUNDARY_CONTROLS','rows':rows,'total_reflections':sum(r['reflections'] for r in rows),'total_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'source_pins':inputs['author_pins'],'geometry_sha256':inputs['geometry_sha256'],'input_sha256':hashlib.sha256((HERE/'staircase10-top-window-independent-inputs.json').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'independence':'Own exact overlap/last-target-image constructor; existing reviewer pure full original-wall path_check reused. No author code run.','universal_quantifiers_proved_by_samples':False,'new_search':False,'new_engine':False,'full_goal_complete':False}
(HERE/'staircase10-top-window-independent-check.json').write_text(json.dumps(out,default=str,indent=2)+'\n')
print(json.dumps({'status':out['status'],'total_reflections':out['total_reflections'],'total_wall_leg_guards':out['total_wall_leg_guards'],'rows':[{k:v for k,v in r.items() if k not in ('path','C')} for r in rows]},default=str,indent=2))
