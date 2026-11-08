"""Retrieve one already-certified periodic state; test prescribed shear neighbors."""
from pathlib import Path
import ast,gzip,hashlib,json,time,datetime
HERE=Path(__file__).resolve().parent
D=datetime.datetime.fromisoformat(json.loads((HERE/'global-exchange-effort.json').read_text())['aggregate_deadline_utc'].replace('Z','+00:00')).timestamp()
mod=ast.parse((HERE/'global-exchange-check.py').read_text());ns={}
exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'B05-functions','exec'),ns)
inv,comm,feature=ns['inv'],ns['comm'],ns['feature']
raw=gzip.decompress((HERE.parent/'review/marked-origami-known22-closure.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()=='2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
N=60
for idx in range(len(raw)//(3*N)):
 if time.time()>D:raise TimeoutError('B05 original deadline')
 off=idx*3*N;h,v,lab=[list(raw[off+j*N:off+(j+1)*N]) for j in range(3)]
 C=comm(h,v);Z={a for a in range(N) if C[a]!=a};x=0;trace=[]
 while True:
  x=h[x];trace.append(x)
  if x in Z:break
  if x==0:break
 if x==0:break
else:raise AssertionError('saved periodic control absent')
base=(h,v,lab)
words=[[],['Ui'],['Ti'],['U'],['T'],['Ui','Ti'],['Ti','Ui'],['T','Ui','T']]
rows=[]
for word in words:
 hh,vv,ll=base;hh=list(hh);vv=list(vv)
 for letter in word:
  if letter=='T':hi=inv(hh);vv=[vv[hi[i]] for i in range(N)]
  elif letter=='U':vi=inv(vv);hh=[hh[vi[i]] for i in range(N)]
  elif letter=='Ti':vv=[vv[hh[i]] for i in range(N)]
  elif letter=='Ui':hh=[hh[vv[i]] for i in range(N)]
  assert comm(hh,vv)==C
 vi=inv(vv);diag=[hh[vi[i]] for i in range(N)];di=inv(diag)
 assert di==[vv[inv(hh)[i]] for i in range(N)]
 a,b,d=feature(hh,ll,Z),feature(vv,ll,Z),feature(diag,ll,Z)
 assert a['H']==b['H']==d['H']==0
 row={'word':word,'R_h':a['R'],'R_v':b['R'],'R_diag':d['R'],'D':2*d['R']-a['R']-b['R'],'h':hh,'v':vv,'h_trace':a,'v_trace':b,'diagonal_trace':d}
 rows.append(row)
out={'status':'PRESCRIBED_PERIODIC_NEIGHBOR_TEST_COMPLETE','raw_sha256':hashlib.sha256(raw).hexdigest(),'retrieved_index':idx,'root_periodic_trace':trace,'base_labels':lab,'true_zero_indices':sorted(Z),'rows':rows,'positive_D_words':[r['word'] for r in rows if r['D']>0],'new_orbit_discovery':False,'whole_goal_complete':False}
(HERE/'global-exchange-periodic-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'retrieved_index':idx,'root_trace':trace,'rows':[{k:r[k] for k in ['word','R_h','R_v','R_diag','D']} for r in rows]},indent=2))
