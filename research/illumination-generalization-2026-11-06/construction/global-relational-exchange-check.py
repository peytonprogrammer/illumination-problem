"""B06 prescribed fixed-control replay, never generates a new orbit."""
from pathlib import Path
from collections import Counter
import hashlib,json,datetime,time
P=Path(__file__).resolve().parent
EFF=json.loads((P/'global-relational-exchange-effort.json').read_text())
DEADLINE=datetime.datetime.fromisoformat(EFF['aggregate_deadline_utc'].replace('Z','+00:00')).timestamp()
def guard():
 if time.time()>=DEADLINE:raise TimeoutError('B06 original aggregate deadline')
def inverse(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return q
def comm(h,v):
 hi,vi=inverse(h),inverse(v)
 return [v[h[vi[hi[i]]]] for i in range(len(h))]
def zero_cycles(C):
 seen=set();cycles=[]
 for i in range(len(C)):
  if i in seen or C[i]==i:continue
  cyc=[];j=i
  while j not in seen:seen.add(j);cyc.append(j);j=C[j]
  assert j==i;cycles.append(cyc)
 return cycles
def feature(p,labels,cycles):
 Z={z for cyc in cycles for z in cyc}; records=[]
 for color in [1,2]:
  other=3-color
  for sign,q in [(1,p),(-1,inverse(p))]:
   for start in [i for i,c in enumerate(labels) if c==color]:
    x=start;trace=[]
    while True:
     x=q[x];trace.append(x)
     if x in Z:kind='zero';break
     if labels[x]==other:kind='opposite';break
     if x==start:kind='periodic';break
     assert len(trace)<=len(p)
    records.append({'color':color,'sign':sign,'start':start,'terminal_type':kind,'terminal_slot':x,'trace':trace})
 F=0;same=0;inc=[]
 for sign in [1,-1]:
  for name,cyc in enumerate(cycles):
   a=Counter(r['terminal_slot'] for r in records if r['color']==1 and r['sign']==sign and r['terminal_type']=='zero' and r['terminal_slot'] in cyc)
   b=Counter(r['terminal_slot'] for r in records if r['color']==2 and r['sign']==sign and r['terminal_type']=='zero' and r['terminal_slot'] in cyc)
   overlap=sum(a[z]*b[z] for z in cyc);same+=overlap
   f=sum(a.values())*sum(b.values())-overlap;F+=f
   if a or b:inc.append({'sign':sign,'zero_id':name,'cycle':cyc,'source_slots':dict(a),'target_slots':dict(b),'shared_pairs':f})
 assert same==0,'ordered-mark same-slot lemma'
 H=sum(r['color']==1 and r['terminal_type']=='opposite' for r in records)
 return {'F':F,'H_pm':H,'same_slot_pairs':same,'incidences':inc,'records':records}
def analyze(name,h,v,labels):
 guard();C=comm(h,v);cycles=zero_cycles(C);assert all(len(c)==3 for c in cycles)
 assert len(h)==len(v)==len(labels)
 assert sorted(h)==sorted(v)==list(range(len(h)))
 assert labels.count(1)==labels.count(2)==4
 assert all(C[i]==i for i,c in enumerate(labels) if c in [1,2])
 n=len(h);hi,vi=inverse(h),inverse(v);vt=[v[hi[i]] for i in range(n)];hu=[h[vi[i]] for i in range(n)]
 assert comm(h,vt)==C==comm(hu,v)
 hh=feature(h,labels,cycles);vv=feature(v,labels,cycles);tv=feature(vt,labels,cycles);uh=feature(hu,labels,cycles)
 assert feature(inverse(hu),labels,cycles)['F']==uh['F']==tv['F']
 # Exact record identity, not only equality of the aggregate feature.
 def normalize(records):
  return sorted(records,key=lambda x:(x['color'],x['sign'],x['start']))
 swapped=[dict(record,sign=-record['sign']) for record in uh['records']]
 assert normalize(tv['records'])==normalize(swapped)
 D=tv['F']-vv['F']+uh['F']-hh['F'];r=len(cycles)
 # Clear the positive denominator for an exact integer comparison.
 gap=16*n*(hh['H_pm']-D)-(9-r)*hh['F']
 return {'name':name,'n':n,'r':r,'h':h,'v':v,'labels':labels,'zero_cycles':cycles,'F_h':hh['F'],'F_v':vv['F'],'F_diag':uh['F'],'D':D,'H_pm':hh['H_pm'],'candidate_gap_times_16N':gap,'candidate_domain':1<=r<=9,'candidate_pass':gap>=0,'horizontal':hh,'vertical':vv,'T_vertical':tv,'U_horizontal':uh}
def square_control():
 # The exact already prescribed square; only three prescribed directions.
 period=48
 S=[(x,y) for x in [12,36] for y in [12,36]]
 T=[(x,y) for x in [16,32] for y in [18,30]]
 rows=[]
 for w in [(1,0),(0,1),(1,-1)]:
  records=[]
  for color,marks,other in [(1,S,T),(2,T,S)]:
   for sign in [1,-1]:
    for start in marks:
     point=start;trace=[]
     for step in range(1,period+1):
      point=((point[0]+sign*w[0])%period,(point[1]+sign*w[1])%period);trace.append(point)
      if point in other:kind='opposite';break
      if point==start:kind='periodic';break
     else:raise AssertionError('fixed torus period')
     assert kind=='periodic' and step==48
     records.append({'color':color,'sign':sign,'start':start,'terminal_type':kind,'length':step})
  rows.append({'prescribed_direction':w,'F':0,'H_pm':0,'records':records})
 # Direct segment (12,12) to (16,18) stays strictly inside [0,24]^2.
 assert 0<12<16<24 and 0<12<18<24
 return {'room':[0,24,0,24],'S_fiber':S,'T_fiber':T,'true_zero_cycles':[],'r':0,'direction_rows':rows,'F_every_direction':0,'candidate_domain':False,'conclusion':'Zero-incidence feature has zero orbit weight for this lit r0 control; separate cornerless argument required.','direct_original_endpoint_segment':[[12,12],[16,18]]}
if __name__=='__main__':
 guard();old=json.loads((P/'global-exchange-periodic-check.json').read_text())
 rows=[]
 # Exactly the previously stored eight raw neighboring controls, no traversal.
 for row in old['rows']:rows.append(analyze('saved462:'+','.join(row['word']),row['h'],row['v'],old['base_labels']))
 audit_path=P.parents[1]/'codex-proof-verification/specialist-ideas/label-descent-audit.json'
 audit=json.loads(audit_path.read_text());h,v,labels=audit['initial_state'];rows.append(analyze('pinned_lex_root',h,v,labels))
 out={'status':'PRESCRIBED_RELATIONAL_FEATURE_CHECK','original_deadline_utc':EFF['aggregate_deadline_utc'],'input_sha256':{'global-exchange-periodic-check.json':hashlib.sha256((P/'global-exchange-periodic-check.json').read_bytes()).hexdigest(),'label-descent-audit.json':hashlib.sha256(audit_path.read_bytes()).hexdigest()},'rows':rows,'square_control':square_control(),'failed_named_controls':[r['name'] for r in rows if r['candidate_domain'] and not r['candidate_pass']],'whole_goal_complete':False,'new_orbit_room_or_ray_census':False}
 (P/'global-relational-exchange-check.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ['name','r','F_h','F_v','F_diag','D','H_pm','candidate_gap_times_16N','candidate_pass']} for r in rows],indent=2))
