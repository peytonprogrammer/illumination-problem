"""Independent arithmetic/dependency audit only; no optical rerun or discovery."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
p=ROOT/'fourth-surplus-review/local-four-closure/manifest.json';d=json.loads(p.read_text());pins={}
for rel,h in d['source_sha256'].items():
 q=ROOT/rel;actual=hashlib.sha256(q.read_bytes()).hexdigest();assert actual==h,rel;pins[rel]=actual
for row in d['cases']:
 for rel in row['evidence']:assert rel in pins,rel
# Generate weighted integer partitions independently, rather than using row count.
def parts(n,lo=1):
 if n==0:yield ()
 for i in range(lo,n+1):
  for r in parts(n-i,i):yield(i,)+r
arithmetic={(b,es)for b in range(5)for es in parts(4-b)}
assert len(arithmetic)==12
excluded={(1,(3,)),(0,(4,))}
expected=[(4,()),(3,(1,)),(2,(2,)),(2,(1,1)),(1,(1,2)),(1,(1,1,1)),(0,(1,3)),(0,(2,2)),(0,(1,1,2)),(0,(1,1,1,1))]
assert set(expected)==arithmetic-excluded
bounds=[13,13,32,13,14,13,13,19,13,13]
assert [r['bound']for r in d['cases']]==bounds and max(bounds)==d['reflection_bound']==32
# Verify every original single-e2 residue has an explicit already-accepted closure.
s=ROOT/'surplus-four-local/single-e2-closure.json';c=json.loads(s.read_text());assert c['remaining_reduced_cases']==0 and len(c['cases'])==7
assert max(r['reflections']for r in c['cases'].values())==32
for r in c['cases'].values():
 for field in ('proof','independent_review'):
  q=ROOT/r[field];assert q.exists();pins[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
# Pin canonical prose correction and current final statements, too.
for rel in ['surplus-four-local/four-unit-no-DR/review-reconciliation.txt','fourth-surplus-review/local-four-closure/theorem.txt','fourth-surplus-review/local-four-closure/coverage.txt','fourth-surplus-review/local-four-closure/manifest.json']:
 q=ROOT/rel;pins[rel]=hashlib.sha256(q.read_bytes()).hexdigest()
pins[str(Path(__file__).resolve().relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_LOCAL_TEN_TYPE_JOIN_ACCEPTED','weighted_partitions':sorted(arithmetic),'excluded':sorted(excluded),'case_bounds':bounds,'maximum':32,'manifest_pins_current':len(d['source_sha256']),'source_sha256':pins,'limits':'Dependency and hand completeness audit; accepted component optics reused explicitly. Locality premise essential; remote rows and global join open. Not formal verification.'},indent=2)+'\n')
print('PASS all12 weighted partitions /2 exclusions /10 covered;32 manifest pins current; max32')
