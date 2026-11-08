"""Complete provenance for the frozen k<=6 final CNFs. Standard library only.
No solver, encoder, discovery runner, tracer, or new optical search.
Existing independent geometry-prefix receipts are an explicit dependency.
"""
from pathlib import Path
from collections import defaultdict
from itertools import product
import gzip,hashlib,json,struct,time

ROOT=Path(__file__).resolve().parent
OWN=ROOT.parents[1]
PEER=OWN.parent/'claude-illumination-check/k6-run'
OLD=OWN/'k6-final-review'
ENC=OWN/'k5-proof-pilot/inputs/encode.py'
GEOM=OWN/'k5-proof-pilot/inputs/illumination_geometry.py'
START=time.monotonic()
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
 return h.hexdigest()
def save(n,d): (ROOT/n).write_text(json.dumps(d,indent=2)+'\n')
def norm_clause(xs):
 v=sorted(set(xs))
 return struct.pack('<'+'i'*len(v),*v)
def key(b): return hashlib.sha256(b).digest()
def neighbours(c): return {(c[0]+a,c[1]+b) for a,b in [(1,0),(-1,0),(0,1),(0,-1)]}
RING=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0))
def variable_map(case):
 # Independent fan construction of the encoder's finite triangle universe.
 full=set(map(tuple,case['full']));near=full|set.union(*(neighbours(c) for c in full))
 cap=(21-4*len(full)+12)//2;radius=max(0,cap-len(near-full));allowed=set(near)
 for _ in range(radius): allowed|=set.union(*(neighbours(c) for c in allowed))
 tris=[]
 for cx,cy in allowed:
  for i in range(8):
   tris.append(tuple(sorted(((2*cx,2*cy),(2*cx+RING[i][0],2*cy+RING[i][1]),(2*cx+RING[i+1][0],2*cy+RING[i+1][1])))))
 tris=sorted(set(tris));return {t:i+1 for i,t in enumerate(tris)}

casefile=PEER/'cases.json';bindfile=OLD/'encoder-binding.json';auditfile=OLD/'audit.json'
cases=json.loads(casefile.read_text());bindings=json.loads(bindfile.read_text());audit=json.loads(auditfile.read_text())
assert bindings['status']==audit['status']=='PASS'
assert digest(ENC)==bindings['encoder_sha256'],'frozen encoder changed'
base={r['tag']:r for r in bindings['cases']};prior={r['tag']:r for r in audit['receipt_hashes']}
assert len(cases)==61 and {c['tag'] for c in cases}==set(base)==set(prior)
guardfiles=[OWN/'k5-proof-continuation/learned.jsonl',OWN/'k5-proof-continuation/peer-guards.json',OWN/'k5-proof-pilot/orbit-guard.json']+sorted(PEER.glob('cases/*/guards*.jsonl'))
paths=[casefile,bindfile,auditfile,ENC,GEOM]+guardfiles+[PEER/'cases'/c['tag']/'formula.cnf' for c in cases]
frozen=[]
for p in paths: frozen.append({'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)})
manifest={'status':'FROZEN','guard_files':len(guardfiles),'inputs':frozen,'scope':'CNF premises only; no fresh DRAT or complete physical-path replay'}
existing=ROOT/'frozen-inputs.json'
if existing.exists(): assert json.loads(existing.read_text())==manifest,'inputs changed since first freeze; reconcile before rerun'
else:save('frozen-inputs.json',manifest)
expected_hash={r['path']:r['sha256'] for r in frozen}
print('INPUTS FROZEN',len(paths),'guardfiles',len(guardfiles),flush=True)

states=[];total_added=0
for c in cases:
 tag=c['tag'];p=PEER/'cases'/tag/'formula.cnf';x=variable_map(c)
 assert len(x)==base[tag]['triangles'],'independent triangle universe mismatch'
 assert expected_hash[str(p)]==prior[tag]['cnf'],'final CNF differs from independently checked prefix receipt'
 wanted={};raw_added=0;columns=set();cnfhash=hashlib.sha256();header=None;clauses=0
 with p.open('rb') as f:
  for raw in f:
   cnfhash.update(raw);line=raw.strip()
   if not line or line.startswith(b'c'):continue
   if line.startswith(b'p'):
    assert header is None;h=line.split();assert h[:2]==[b'p',b'cnf'];header=tuple(map(int,h[2:]));continue
   xs=list(map(int,line.split()));assert xs[-1]==0 and 0 not in xs[:-1]
   clauses+=1
   if clauses<=base[tag]['base_clauses']:continue
   vals=xs[:-1];assert all(1<=abs(a)<=len(x) for a in vals),'non-tile literal in optical suffix'
   assert not set(vals)&{-a for a in vals},'tautological optical suffix'
   b=norm_clause(vals);h=key(b)
   if h in wanted:assert wanted[h]==b,'hash collision'
   wanted[h]=b;raw_added+=1;columns.update(vals)
 assert header is not None and clauses==header[1]
 assert cnfhash.hexdigest()==expected_hash[str(p)]
 st={'tag':tag,'case':c,'x':x,'wanted':wanted,'raw_added':raw_added,'unique_added':len(wanted),'matched':0,'base_clauses':base[tag]['base_clauses'],'cnf_sha256':cnfhash.hexdigest(),'cnf_variables':header[0]}
 states.append(st);total_added+=raw_added
print('FINAL SUFFIXES LOADED',total_added,'unique',sum(s['unique_added'] for s in states),flush=True)
# Controls target the acceptance predicate, not a new optical experiment.
control=next(s for s in states if s['wanted']);h,b=next(iter(control['wanted'].items()))
assert control['wanted'].get(key(b))==b
bad=norm_clause([len(control['x'])+1]);assert control['wanted'].get(key(bad))!=bad
assert control['wanted'].get(key(b''))!=b''
# Reversing a nonempty implication must not silently be accepted as the same clause.
xs=struct.unpack('<'+'i'*(len(b)//4),b);flipped=norm_clause([-a for a in xs]);assert flipped!=b
save('acceptance-controls.json',{'status':'PASS','known_clause_recognized':True,'out_of_universe_literal_rejected':True,'empty_optical_clause_rejected':True,'polarity_change_not_equal':True,'scope':'Provenance acceptance controls, not path validity tests'})

MATS=[]
for swap in (False,True):
 for sx,sy in product((-1,1),repeat=2):
  MATS.append((0,sx,sy,0) if swap else(sx,0,0,sy))
def transform(t,m,o):
 return tuple(sorted((m[0]*a+m[1]*b+o[0],m[2]*a+m[3]*b+o[1]) for a,b in t))
rulecache={}
def rules(q):
 if q not in rulecache:
  out=[]
  for i,st in enumerate(states):
   ss,tt=[tuple(2*a for a in p) for p in st['case']['pair']]
   for origin,end in [(ss,tt),(tt,ss)]:
    dx,dy=end[0]-origin[0],end[1]-origin[1]
    for m in MATS:
     if (m[0]*q[0]+m[1]*q[1],m[2]*q[0]+m[3]*q[1])==(dx,dy):out.append((i,m,origin))
  rulecache[q]=out
 return rulecache[q]
canonical_seen=set()
def canonical(t):
 t=tuple(sorted(map(tuple,t)))
 if t not in canonical_seen:
  assert len(set(t))==3 and all(all(isinstance(a,int) for a in p) for p in t)
  ax=[p for p in t if p[0]%2==p[1]%2==0];bx=[p for p in t if p[0]%2==p[1]%2==1]
  assert len(ax)==len(bx)==1 and abs(ax[0][0]-bx[0][0])==abs(ax[0][1]-bx[0][1])==1
  assert all(min(ax[0][j],bx[0][j])<=p[j]<=max(ax[0][j],bx[0][j]) for p in t for j in (0,1))
  canonical_seen.add(t)
 return t
records=0;rule_attempts=0;clause_candidates=0;file_rows=[]
with gzip.open(ROOT/'clause-witnesses.jsonl.gz','wt',encoding='utf-8') as out:
 for file_index,p in enumerate(guardfiles):
  before=sum(s['matched'] for s in states);n=0
  if p.suffix=='.jsonl':
   handle=p.open();source=((i,json.loads(line)) for i,line in enumerate(handle,1) if line.strip())
  else:
   handle=None;raw=json.loads(p.read_text());source=enumerate(raw if isinstance(raw,list) else[raw],1)
  try:
   for line_no,rec in source:
    records+=1;n+=1;q=tuple(rec['q']);assert len(q)==2 and q!=(0,0) and all(isinstance(a,int) and a%2==0 for a in q)
    assert rec['path'][0]==[[0,1],[0,1]],'source endpoint'
    last=rec['path'][-1];assert all(c[1]>0 and c[0]==q[j]*c[1] for j,c in enumerate(last)),'target endpoint'
    U=tuple(canonical(t) for t in rec['U']);Z=tuple(canonical(t) for t in rec['Z']);assert not set(U)&set(Z)
    for i,m,o in rules(q):
     st=states[i]
     if not st['wanted']:continue
     rule_attempts+=1;x=st['x'];uu=[]
     for t in U:
      k=x.get(transform(t,m,o))
      if k is None:break
      uu.append(-k)
     else:
      zz=[k for t in Z if (k:=x.get(transform(t,m,o))) is not None]
      packed=norm_clause(uu+zz);clause_candidates+=1;hh=key(packed)
      if hh in st['wanted']:
       assert st['wanted'][hh]==packed,'hash collision'
       del st['wanted'][hh];st['matched']+=1
       out.write(json.dumps({'case':i,'clause_sha256':hh.hex(),'guard_file':file_index,'record':line_no,'matrix':m,'origin':o},separators=(',',':'))+'\n')
  finally:
   if handle:handle.close()
  assert digest(p)==expected_hash[str(p)],'guard source changed during check'
  got=sum(s['matched'] for s in states)-before
  file_rows.append({'path':str(p),'records':n,'new_clause_witnesses':got,'sha256':expected_hash[str(p)]})
  print('GUARDS',file_index+1,'/',len(guardfiles),'records',records,'matched',sum(s['matched'] for s in states),'remaining',sum(len(s['wanted']) for s in states),'elapsed',round(time.monotonic()-START,1),flush=True)
missing=[]
for st in states:
 row={k:st[k] for k in ['tag','raw_added','unique_added','matched','base_clauses','cnf_sha256','cnf_variables']};row['unexplained']=len(st['wanted']);row['status']='PASS' if not st['wanted'] else 'FAIL'
 row['unexplained_clause_sha256']=[h.hex() for h in st['wanted']][:10]
 save(st['tag']+'.json',row)
 if st['wanted']:missing.append(st['tag'])
# Freeze read dependencies and every CNF again; no silent mid-run drift.
for r in frozen:assert digest(Path(r['path']))==r['sha256'],'input changed: '+r['path']
summary={'status':'PASS' if not missing else 'FAIL','cases':len(states),'raw_added_clauses':total_added,'unique_added_clauses':sum(s['unique_added'] for s in states),'matched_unique_clauses':sum(s['matched'] for s in states),'unexplained':sum(len(s['wanted']) for s in states),'failed_cases':missing,'guard_records_read':records,'guard_files':file_rows,'transformation_attempts':rule_attempts,'clause_candidates':clause_candidates,'elapsed_seconds':round(time.monotonic()-START,3),'checker_sha256':digest(Path(__file__)),'frozen_manifest_sha256':digest(existing),'witnesses_sha256':digest(ROOT/'clause-witnesses.jsonl.gz'),'dependencies':['Prior independent geometry-prefix proof and CNF hash binding','Earlier full physical guard verification, not repeated here','Prior full peer DRAT verification with Codex sampled replay'],'new_solver_calls':0,'new_optical_discovery':0,'peer_executable_imports':0}
save('summary.json',summary);print('FINAL',json.dumps({k:v for k,v in summary.items() if k!='guard_files'}),flush=True)
assert not missing,'unexplained final premises'
