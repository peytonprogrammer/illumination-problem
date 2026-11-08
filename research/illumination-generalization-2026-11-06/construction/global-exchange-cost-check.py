"""Exact actual shear traces on three prescribed stored-control images only."""
from pathlib import Path
import ast,json,datetime,time,collections
P=Path(__file__).resolve().parent
end=datetime.datetime.fromisoformat(json.loads((P/'global-exchange-effort.json').read_text())['aggregate_deadline_utc'].replace('Z','+00:00')).timestamp()
assert time.time()<end,'original B05 deadline'
ns={}; tree=ast.parse((P/'global-exchange-check.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'prescribed-functions','exec'),ns)
inv,feature=ns['inv'],ns['feature']
a=json.loads((P/'global-exchange-periodic-check.json').read_text()); lab=a['base_labels']; Z=set(a['true_zero_indices'])
def bag(p):
 return dict(collections.Counter(t['type']+':'+str(len(t['trace'])) for t in feature(p,lab,Z)['traces']))
rows=[]
for word in [[],['Ui'],['T','Ui','T']]:
 assert time.time()<end
 row=next(r for r in a['rows'] if r['word']==word);h,v=row['h'],row['v'];hi,vi=inv(h),inv(v)
 tv=[v[hi[i]] for i in range(len(h))];uh=[h[vi[i]] for i in range(len(h))]
 bags={'h':bag(h),'v':bag(v),'T_v':bag(tv),'U_h':bag(uh)}
 delta=collections.Counter(bags['T_v']);delta.update(bags['U_h'])
 for name in ['h','v']:
  for k,n in bags[name].items():delta[k]-=n
 rows.append({'word':word,'bags':bags,'crossed_cost_coefficients':dict(delta),'actual_T_v':feature(tv,lab,Z),'actual_U_h':feature(uh,lab,Z)})
out={'status':'EXACT_PRESCRIBED_COST_CHECK','rows':rows,'new_orbit_discovery':False,'whole_goal_complete':False}
(P/'global-exchange-cost-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['word','bags','crossed_cost_coefficients']} for r in rows],indent=2))
