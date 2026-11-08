"""Read-only frozen certificate audit: no solve or trajectory discovery."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,hashlib,importlib.util,json,sys,subprocess,time
ROOT=Path(__file__).resolve().parent;OWN=ROOT.parent
PEER=ROOT.parents[1]/'claude-illumination-check/k6-run'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')
def canonical(full,pair):
 keys=[]
 for swap in [False,True]:
  for sx,sy in product((-1,1),repeat=2):
   def f(p):
    x,y=(p[1],p[0]) if swap else p
    return (sx*x,sy*y)
   fs=[f(p) for p in full];ox=min(x for x,y in fs);oy=min(y for x,y in fs)
   sh=lambda p:(f(p)[0]-ox,f(p)[1]-oy)
   keys.append((tuple(sorted(sh(p) for p in full)),tuple(sorted(sh(p) for p in pair))))
 return min(keys)
cs=json.loads((PEER/'cases.json').read_text())
old=json.loads((OWN/'k6-support-census/count.json').read_text())
expected=[]
for c in old['cases']:
 for pair in c['mark_pairs']:expected.append(canonical(c['full'],pair))
actual=[canonical(c['full'],c['pair']) for c in cs]
from collections import Counter
assert Counter(actual)==Counter(expected)
assert len(cs)==61 and sum(len(c['full'])==2 for c in cs)==18
assert sum(len(c['full'])==3 for c in cs)==43
I4=json.loads((OWN/'k6-i4-review/check.json').read_text());assert I4['status']=='PASS' and len(I4['cases'])==3
write('coverage.json',dict(status='PASS',raw_pairs=61,I2=18,I3=43,
 I4='THREE_PREVIOUSLY_INDEPENDENTLY_VERIFIED_EQUALITY_SHAPES',
 support_source='Previously independently proved finite census; no new enumeration.',
 raw_pair_multiset_matches=True,pair_orbits=len(set(actual)),caps={'W':21,'k':6,'I_max':4,'P_plus_missing':[12,10,8]}))
print('coverage PASS61raw/56orbits + I4',flush=True)
# Check ALL immutable result receipts and file hashes, without accepting log text
# as a fresh proof replay. DRAT replay below is an explicitly bounded sample.
receipts=[]
for c in cs:
 d=PEER/'cases'/c['tag'];r=json.loads((d/'result.json').read_text())
 assert r['status']=='UNSAT' and r['drat']=='VERIFIED' and 'cube' not in r
 assert digest(d/'formula.cnf')==r['cnf_sha256']
 assert digest(d/'proof.drat')==r['proof_sha256']
 receipts.append(dict(tag=c['tag'],cnf=r['cnf_sha256'],proof=r['proof_sha256']))
print('all61receipt hashes PASS',flush=True)
# Regenerate every base CNF and compare its ENTIRE ordered prefix, ignoring
# only DIMACS header totals (saved files also contain optical clauses).
sys.path.insert(0,str(OWN/'k5-proof-pilot/inputs'))
e=load('frozen_encoder',OWN/'k5-proof-pilot/inputs/encode.py')
bindings=[]
for c in cs:
 case={'full':c['full'],'allowed':[(a+dx,b+dy) for a,b in c['full'] for dx in range(-14,15) for dy in range(-14,15) if abs(dx)+abs(dy)<=14]}
 cnf,pool,x,ts=e.geometry(case,wmax=21,kmax=6)
 with (PEER/'cases'/c['tag']/'formula.cnf').open() as f:
  header=next(f).split();assert header[:2]==['p','cnf']
  for i,cl in enumerate(cnf.clauses):
   saved=list(map(int,next(f).split()));assert saved[-1]==0 and saved[:-1]==cl,(c['tag'],i)
 bindings.append(dict(tag=c['tag'],base_clauses=len(cnf.clauses),triangles=len(ts),prefix='IDENTICAL'))
 print('base prefix PASS',c['tag'],len(cnf.clauses),flush=True)
write('encoder-binding.json',dict(status='PASS',encoder_sha256=digest(OWN/'k5-proof-pilot/inputs/encode.py'),cases=bindings,
 scope='Every base geometry clause bound; optical clause implementation and a saved guard sample checked separately, not complete fresh guard replay.'))
# Import only the two pure transformation functions and MATS assignment from
# the peer runner. Do not import runner, solver, search, tracer or library().
tree=ast.parse((PEER/'run.py').read_text());nodes=[]
for n in tree.body:
 if isinstance(n,ast.FunctionDef) and n.name in {'mapt','clauses'}:nodes.append(n)
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MATS' for t in n.targets):nodes.append(n)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(PEER/'run.py'),'exec'),ns)
a=load('independent_guard_checker',OWN/'persisted-replay/audit.py')
files=sorted((PEER/'cases').glob('*/guards*.jsonl'))
# Six explicitly fixed source files; each FIRST saved record, no directions chosen.
selected=[]
for tag in ['I2_00_02-pair0','I2_00_11-pair0','I2_00_12-pair0','I2_00_07-pair0','I3_00_01_02-pair0','I3_00_12_21-pair2']:
 fs=[f for f in files if f.parent.name==tag and f.stat().st_size]
 if fs:
  for f in fs[:2]:
   with f.open() as h:rec=json.loads(next(h))
   selected.append((f,rec))
guards=[];symmetry_checks=0
for f,rec in selected:
 receipt=a.check_record(rec,tuple(rec['q']),False)
 path=tuple(tuple(F(*xy) for xy in p) for p in rec['path'])
 U=a.triangles(rec['U']);Z=a.triangles(rec['Z'])
 # Independent D4/even-translation and reversal on the saved path itself.
 for swap in [False,True]:
  for sx,sy in product((-1,1),repeat=2):
   def fpoint(p):
    xx,yy=(p[1],p[0]) if swap else p
    return (sx*xx+4,sy*yy-2)
   def mapped(tris):return frozenset(tuple(sorted(fpoint(p) for p in t)) for t in tris)
   pp=tuple(fpoint(p) for p in path);need,absent=a.path_requirements(pp)
   star=a.incident(pp[0])|a.incident(pp[-1])
   assert need<=mapped(U)|star and absent<=mapped(Z)
   assert a.path_requirements(tuple(reversed(pp)))==(need,absent)
   # Bind the peer's pure clauses implementation to separately constructed
   # tile maps, including guards whose normalized q points in either direction.
   uu=mapped(U);zz=mapped(Z);universe=sorted(uu|zz);xmap={tri:i+1 for i,tri in enumerate(universe)}
   local_origin=pp[0];local_target=pp[-1]
   want=set()
   for o,t in [(local_origin,local_target),(local_target,local_origin)]:
    for mm in ns['MATS']:
     q=rec['q'];v=(t[0]-o[0],t[1]-o[1])
     if (mm[0]*q[0]+mm[1]*q[1],mm[2]*q[0]+mm[3]*q[1])!=v:continue
     def mp(tris):return [tuple(sorted((mm[0]*z[0]+mm[1]*z[1]+o[0],mm[2]*z[0]+mm[3]*z[1]+o[1]) for z in tri)) for tri in tris]
     uu2=mp(U);zz2=mp(Z)
     if all(tri in xmap for tri in uu2):want.add(tuple(sorted([-xmap[tri] for tri in uu2]+[xmap[tri] for tri in zz2 if tri in xmap])))
   got=ns['clauses'](rec,local_origin,local_target,xmap)
   assert got==want and got
   symmetry_checks+=1
 guards.append(dict(file=str(f.relative_to(PEER)),line=1,receipt=receipt))
write('guard-sample.json',dict(status='PASS',saved_guards=len(guards),isometries_and_reverse=symmetry_checks,records=guards,
 scope='Independent exact implication replay of first supplied records only; no claim to fresh replay of175601 guards.'))
(ROOT/'guard-sample.log').write_text('PASS '+str(len(guards))+' saved guards; '+str(symmetry_checks)+' D4/even-translation/reversal controls\n')
print('guard sample PASS',len(guards),symmetry_checks,flush=True)
# Three proof samples: small I2, median I2, and largest I3. Exact filenames
# are fixed here, not selected by outcome.
proof_rows=[]
with (ROOT/'drat-sample.log').open('w') as log:
 for tag in ['I2_00_07-pair0','I2_00_14-pair0','I3_00_01_02-pair0']:
  d=PEER/'cases'/tag
  proc=subprocess.run([str(OWN/'bounded-proof/drat-trim'),str(d/'formula.cnf'),str(d/'proof.drat')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  log.write('CASE '+tag+'\n'+proc.stdout+'\n');log.flush()
  assert proc.returncode==0 and 's VERIFIED' in proc.stdout,tag
  proof_rows.append(dict(tag=tag,status='VERIFIED',proof_bytes=(d/'proof.drat').stat().st_size))
  print('DRAT sample VERIFIED',tag,flush=True)
write('audit.json',dict(status='PASS',receipt_hashes=receipts,base_bindings=len(bindings),DRAT_samples=proof_rows,
 guard_samples=len(guards),isometries_and_reversals=symmetry_checks,coverage='61raw pairs+previous independent I4',
 limitations=['Only3freshDRATreplays; other58remain peer proof replays with independently bound hashes','Guard replay is sampled, not the full library','No unrestricted wall minimum or finite universal k bound inferred'],discovery_runs=0))
print('FINAL AUDIT PASS',flush=True)
