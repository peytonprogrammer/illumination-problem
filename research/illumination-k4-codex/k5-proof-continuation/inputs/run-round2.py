"""Five-exception continuation by exact orbit certificates, never a ray-radius scan.
Every added optical guard is checked by exact rational triangle requirements.
"""
from pathlib import Path
from collections import deque,Counter
from fractions import Fraction as F
import importlib.util,json,time,hashlib,threading,subprocess,shutil,sys
ROOT=Path(__file__).resolve().parent;PILOT=ROOT.parent/'k5-proof-pilot';LEGACY=ROOT.parent/'bounded-proof'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=load('pilot',PILOT/'pass.py');a=load('audit',ROOT.parent/'persisted-replay/audit.py');ow=load('ow',PILOT/'orbit-witness.py');o=ow.o
from pysat.solvers import Solver

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')

def orbit_direction(V,S,T,limit=5000,seconds=10):
 start_time=time.monotonic();r,u,lab,s0,frame=o.build(list(V),S,T)
 first=o.canon(r,u,lab,s0);seen={first};todo=deque([(first,((1,0),(0,1)),'')]);checked=0
 while todo:
  (R,U,lab),B,word=todo.popleft();checked+=1;i=R[0];distance=1
  while i!=0:
   if lab[i]=='block':break
   if lab[i]=='T':
    physical=o.ap(tuple(zip(*frame)),(B[0][0],B[1][0]))
    return dict(status='LIT',direction=physical,inverse_matrix=B,source_frame=frame,shear_word=word,horizontal_steps=distance,checked=checked,visited=len(seen))
   i=R[i];distance+=1
  if time.monotonic()-start_time>seconds:return dict(status='UNDECIDED_TIME',checked=checked,visited=len(seen))
  Ri,Ui=o.inv(R),o.inv(U)
  for rr,uu,inv,name in ((R,tuple(o.comp(U,Ri)),((1,-1),(0,1)),'T'),(tuple(o.comp(R,Ui)),U,((1,0),(-1,1)),'L')):
   nxt=o.canon(rr,uu,lab,0)
   if nxt not in seen:
    seen.add(nxt);todo.append((nxt,o.mul(B,inv),word+name))
    if len(seen)>limit:return dict(status='UNDECIDED_STATES',checked=checked,visited=len(seen))
 return dict(status='DARK_ORBIT_PENDING_INDEPENDENT_REVIEW',checked=checked,visited=len(seen))

def normalized_guard(path,room,tag,generation):
 s,t=map(tuple,room['marked']);v=(t[0]-s[0],t[1]-s[1]);q=tuple(sorted(map(abs,v),reverse=True))
 g=next(g for g in p.matrices() if (g[0]*q[0]+g[1]*q[1],g[2]*q[0]+g[3]*q[1])==v)
 def point(z):return (g[0]*(z[0]-s[0])+g[2]*(z[1]-s[1]),g[1]*(z[0]-s[0])+g[3]*(z[1]-s[1]))
 normalized=tuple(point(z) for z in path);need,forbid=a.path_requirements(normalized)
 mapped_room=sorted(tuple(sorted(point(z) for z in tri)) for tri in room['triangles'])
 guard=dict(U=sorted(need),Z=sorted(forbid),q=q,path=[[[c.numerator,c.denominator] for c in z] for z in normalized],room=mapped_room,source_case=tag,generation=generation)
 receipt=a.check_record(guard,q,True)
 return guard,receipt

def guard_clauses(records,pair,x):
 s,t=[tuple(2*c for c in z) for z in pair];clauses=set()
 for rec in records:
  q=rec['q']
  for origin,end in ((s,t),(t,s)):
   v=(end[0]-origin[0],end[1]-origin[1])
   for g in p.matrices():
    if (g[0]*q[0]+g[1]*q[1],g[2]*q[0]+g[3]*q[1])!=v:continue
    U=p.model.map_guard(rec['U'],g,origin);Z=p.model.map_guard(rec['Z'],g,origin)
    if U<=x.keys():clauses.add(tuple(sorted([-x[u] for u in U]+[x[z] for z in Z if z in x])))
 return clauses

def run(case,index,pair,records,rounds=80,budget=90,peer_guards_used=False):
 tag=f'{case["tag"]}-pair{index}';folder=ROOT/'cases'/tag;folder.mkdir(parents=True,exist_ok=True);started=time.monotonic()
 cnf,pool,x,ts=p.model.geometry(case,wmax=21,kmax=5);old=p.frozen_guards(pair,x,cnf)
 added=set();initial=guard_clauses(records,pair,x)
 for clause in sorted(initial):cnf.append(list(clause));added.add(clause)
 status='OPEN_ROUND_LIMIT';generations=[];stats={};proof=[]
 existing=[int(z.name) for z in (folder/'generations').iterdir()] if (folder/'generations').exists() else []
 offset=max(existing,default=-1)+1
 print(json.dumps(dict(tag=tag,phase='start',prior_guards=old,extra_clauses=len(added))),flush=True)
 with Solver(name='glucose4',bootstrap_with=cnf.clauses,with_proof=True) as solver:
  for step in range(rounds):
   generation=offset+step
   remaining=budget-(time.monotonic()-started)
   if remaining<=0:status='OPEN_TIME_LIMIT';break
   timer=threading.Timer(min(30,remaining),solver.interrupt);timer.start()
   try:sat=solver.solve_limited(expect_interrupt=True)
   finally:timer.cancel()
   if sat is None:status='OPEN_SAT_TIMEOUT';break
   if sat is False:status='UNSAT_UNVERIFIED';proof=solver.get_proof();break
   assignment=set(solver.get_model());selected=[t for t,v in x.items() if v in assignment]
   room=dict(triangles=selected,marked=[[2*c for c in z] for z in pair],require_simple=True)
   geometry=p.model.check(room,strict=False);vertices=p.boundary(selected)
   assert len(vertices)==geometry['walls']<=21 and geometry['tiles']<=38 and len(geometry['transparent_vertices'])<=5
   gen=folder/'generations'/str(generation);gen.mkdir(parents=True,exist_ok=True)
   packet=dict(vertices=vertices,marked=room['marked']);write(gen/'vertices.json',packet);write(gen/'residual-room.json',dict(room=room,geometry_receipt=geometry))
   S,T=map(tuple,room['marked']);orb=orbit_direction(list(map(tuple,vertices)),S,T);write(gen/'orbit.json',orb)
   if orb['status']!='LIT':
    status='OPEN_'+orb['status'];generations.append(dict(generation=generation,status=status,packet_sha256=sha(gen/'vertices.json')));break
   try:
    # This replay follows exactly the direction supplied by the orbit proof.
    path=ow.trace_direction(vertices,S,T,orb['direction']);guard,receipt=normalized_guard(path,room,tag,generation)
   except Exception as error:
    status='OPEN_WITNESS_VERIFICATION_FAILED';write(gen/'receipt.json',dict(status=status,error=repr(error)));generations.append(dict(generation=generation,status=status));break
   write(gen/'path.json',dict(direction=orb['direction'],points=[[[c.numerator,c.denominator] for c in z] for z in path]))
   write(gen/'guard.json',guard);write(gen/'receipt.json',dict(status='PASS',**receipt))
   fresh=guard_clauses([guard],pair,x)-added
   assert fresh,('no new guard',tag,generation)
   # The just verified guard must falsify the current physical candidate.
   assert any(not any((lit in assignment) for lit in clause) for clause in fresh)
   for clause in sorted(fresh):solver.add_clause(list(clause));cnf.append(list(clause));added.add(clause)
   records.append(guard)
   with (ROOT/'learned.jsonl').open('a') as stream:stream.write(json.dumps(guard)+'\n')
   item=dict(generation=generation,status='VERIFIED_LIT_GUARD',walls=geometry['walls'],triangles=geometry['tiles'],exceptions=len(geometry['transparent_vertices']),reflections=len(path)-2,orbit_states=orb['visited'],packet_sha256=sha(gen/'vertices.json'),clauses=len(fresh))
   generations.append(item)
   if generation%10==0:print(json.dumps(dict(tag=tag,phase='learning',**item)),flush=True)
  stats=solver.accum_stats()
 cnf.to_file(str(folder/'formula.cnf'))
 if status=='UNSAT_UNVERIFIED':
  (folder/'proof.drat').write_text('\n'.join(proof)+'\n')
  with (folder/'proof-check.log').open('w') as log:
   try:checked=subprocess.run([str(LEGACY/'drat-trim'),str(folder/'formula.cnf'),str(folder/'proof.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=120)
   except subprocess.TimeoutExpired:checked=None
  if checked and checked.returncode==0 and 's VERIFIED' in (folder/'proof-check.log').read_text():status='VERIFIED_UNSAT'
 result=dict(tag=tag,status=status,peer_guards_used=peer_guards_used,seconds=round(time.monotonic()-started,3),W_cap=21,k_cap=5,N_cap=38,prior_guards=old,new_clauses=len(added),generations=generations,solver_stats=stats,cnf_sha256=sha(folder/'formula.cnf'))
 if status in ('VERIFIED_UNSAT','UNSAT_UNVERIFIED'):result['proof_sha256']=sha(folder/'proof.drat')
 write(folder/'result.json',result);print(json.dumps(dict(tag=tag,status=status,learned=len(generations),seconds=result['seconds'])),flush=True)
 return result

def main():
 assert not (ROOT/'summary.json').exists(), 'Use resume.py to preserve the existing generation history'
 for name in ('pass.py','orbit-witness.py'):
  shutil.copy2(PILOT/name,ROOT/'inputs'/name)
 for name in ('encode.py','illumination_geometry.py','branch-support.json','origami_frame.py'):
  shutil.copy2(PILOT/'inputs'/name,ROOT/'inputs'/name)
 shutil.copy2(ROOT.parent/'persisted-replay/audit.py',ROOT/'inputs/audit.py')
 first=json.loads((PILOT/'pass-summary.json').read_text());write(ROOT/'inputs/first-pass-summary.json',first)
 residual_tags={r['tag'] for r in first['results'] if r['status']=='RESIDUAL'}
 assert len(residual_tags)==10
 records=[json.loads((PILOT/'orbit-guard.json').read_text())]
 # Preserve known dark room under all initial newly available guard patterns.
 cases=json.loads((PILOT/'inputs/branch-support.json').read_text())['cases']
 controlcase=dict(next(c for c in cases if c['tag']=='I2_1_1'));allowed=set(map(tuple,controlcase['allowed']));allowed|={(x+dx,y+dy) for x,y in list(allowed) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))};controlcase['allowed']=sorted(allowed)
 cnf,pool,x,ts=p.model.geometry(controlcase,wmax=22,kmax=5);p.frozen_guards(controlcase['mark_pairs'][0],x,cnf)
 chosen={tuple(sorted(map(tuple,t))) for t in json.loads((PILOT/'inputs/cand-2_2-1.json').read_text())['triangles']}
 def control():
  clauses=guard_clauses(records,controlcase['mark_pairs'][0],x)
  with Solver(name='glucose4',bootstrap_with=cnf.clauses+list(map(list,clauses))) as solver:assert solver.solve(assumptions=[v if t in chosen else -v for t,v in x.items()])
  return dict(known_dark22_allowed=True,guard_records=len(records),new_clauses=len(clauses))
 write(ROOT/'controls.json',control());results=[]
 for case in cases:
  for i,pair in enumerate(case['mark_pairs']):
   if f'{case["tag"]}-pair{i}' not in residual_tags:continue
   results.append(run(case,i,pair,records))
   write(ROOT/'controls.json',control())
   summary=dict(status_counts=dict(Counter(r['status'] for r in results)),completed=len(results),expected=10,learned_guards=len(records)-1,first_pass_exclusions=21,results=results)
   write(ROOT/'summary.json',summary)
 print('COMPLETE',summary['status_counts'],'learned',summary['learned_guards'],flush=True)
if __name__=='__main__':main()
