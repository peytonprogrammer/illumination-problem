"""Prescribed frozen-state tests of named B05 potential, not orbit discovery."""
from pathlib import Path
import gzip,hashlib,json,datetime,time
HERE=Path(__file__).resolve().parent
EFF=json.loads((HERE/'global-exchange-effort.json').read_text())
DEADLINE=datetime.datetime.fromisoformat(EFF['aggregate_deadline_utc'].replace('Z','+00:00')).timestamp()
raw=gzip.decompress((HERE.parent/'review/marked-origami-known22-closure.gz').read_bytes())
assert hashlib.sha256(raw).hexdigest()=='2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
N=60

def inv(p):
 q=[0]*len(p)
 for a,b in enumerate(p):q[b]=a
 return q

def comm(h,v):
 hi,vi=inv(h),inv(v)
 return [v[h[vi[hi[a]]]] for a in range(len(h))]

def feature(h,lab,Z):
 sources=[i for i,z in enumerate(lab) if z==1]
 out=[]
 for start in sources:
  a=start; trace=[]
  while True:
   a=h[a];trace.append(a)
   if a in Z:
    out.append({'source':start,'type':'zero','terminal':a,'trace':trace});break
   if lab[a]==2:
    out.append({'source':start,'type':'target','terminal':a,'trace':trace});break
   if a==start:
    out.append({'source':start,'type':'periodic','terminal':a,'trace':trace});break
 return {'R':sum(t['type']=='periodic' for t in out),'H':sum(t['type']=='target' for t in out),'traces':out}
rows=[];positive=None;nonzero=None
for idx in range(min(32,len(raw)//(3*N))):
 if time.time()>DEADLINE:raise TimeoutError('original B05 deadline')
 off=idx*3*N;h,v,lab=[list(raw[off+j*N:off+(j+1)*N]) for j in range(3)]
 C=comm(h,v);Z={i for i,c in enumerate(C) if c!=i};assert len(Z)==27
 hi,vi=inv(h),inv(v)
 vt=[v[hi[i]] for i in range(N)];hu=[h[vi[i]] for i in range(N)]
 assert comm(h,vt)==C==comm(hu,v)
 a,b,bt,au=feature(h,lab,Z),feature(v,lab,Z),feature(vt,lab,Z),feature(hu,lab,Z)
 assert all(t['H']==0 for t in (a,b,bt,au))
 D=bt['R']-b['R']+au['R']-a['R']
 row={'saved_index':idx,'horizontal_R':a['R'],'vertical_R':b['R'],'T_vertical_R':bt['R'],'U_horizontal_R':au['R'],'D':D,'h':h,'v':v,'labels':lab,'true_zero_indices':sorted(Z),'horizontal':a,'vertical':b,'T_vertical':bt,'U_horizontal':au}
 rows.append(row)
 if D and nonzero is None:nonzero=idx
 if D>0:positive=idx;break
out={'status':'PRESCRIBED_POTENTIAL_TEST_COMPLETE','named_candidate':'Phi=R_vertical,Psi=R_horizontal; H>=(9-r)*a+Delta_T Phi+Delta_U Psi','raw_sha256':hashlib.sha256(raw).hexdigest(),'states_checked':len(rows),'first_positive_D':positive,'first_nonzero_D':nonzero,'rows':rows,'new_orbit_discovery':False,'whole_goal_complete':False}
(HERE/'global-exchange-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'states_checked':len(rows),'first_positive_D':positive,'first_nonzero_D':nonzero,'summary':[{k:r[k] for k in ['saved_index','horizontal_R','vertical_R','T_vertical_R','U_horizontal_R','D']} for r in rows]},indent=2))
