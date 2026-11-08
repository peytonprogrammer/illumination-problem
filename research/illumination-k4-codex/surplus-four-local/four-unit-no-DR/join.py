"""Whole no-positive-D/R FOUR-unit cover with explicit forcing and b0 gates."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];reads=[src,Path(__file__)]
def read(p):reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t)))for t in ts}
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
old=read(BASE/'fourth-surplus-review/three-unit-b1-independent/check.json')['named_guards']
probe=read(HERE/'check.json');new=read(HERE/'roof-center-four/verification.json')
assert len(probe['rows'])==len({r['label']for r in probe['rows']})==208
allK=H|set().union(*(fan(k,range(8))for k in e['C']))
forcing=[]
def force(name,minimum,maximum):
 g=old[name];u,z=decode(g['required']),decode(g['forbidden'])
 assert u<=minimum and not z&maximum,name
 forcing.append({'guard':name,'reflections':g['reflections']})
force('forcing_missingB',H,allK-fan('B',[1]))
force('forcing_sigma_missingB',H,allK-fan('E',[4]))
for suffix,bs in [('ordinaryB',[1]),('centerB',[1,2]),('outerB',[0,1])]:
 force('forcing_missingT_'+suffix,H|fan('B',bs),(allK-fan('B',range(8))|fan('B',bs))-fan('Tc',[5]))
for suffix,es in [('ordinaryB',[4]),('centerB',[3,4]),('outerB',[4,5])]:
 force('forcing_sigma_missingT_'+suffix,H|fan('E',es),(allK-fan('E',range(8))|fan('E',es))-fan('L',[0]))
bridge_u,bridge_z,_=e['constraints']([(0,0),(2,2)],[])
assert bridge_u<=H|fan('N',[6,7]) and not bridge_z
u4,z4=decode(new['required']),decode(new['forbidden'])
assert new['status']=='PARENT_HAND_ROOF_CENTER_FOUR_AND_THREE_REMAINING_ENVELOPES_PASS'
results=[]
for row in probe['rows']:
 spec=row['spec'];mi=H|set().union(*(fan(k,ss)for k,ss in spec.items()));ma=mi|fan('D',[1,2])|fan('R',[3,4])
 if row['excluded_b0']:
  point=tuple(row['excluded_b0'][0]);assert all(x%2 for x in point)
  assert angle(mi,point)==angle(ma,point)==180
  results.append({'label':row['label'],'verdict':'EXCLUDED_b0_FIXED_B180','point':point})
 elif row['path']:
  g=old[row['path']];assert decode(g['required'])<=mi and not decode(g['forbidden'])&ma and g['reflections']<=13
  results.append({'label':row['label'],'verdict':'COVERED_ACCEPTED_GUARD','guard':row['path'],'reflections':g['reflections']})
 else:
  sigma=spec['N']==[6];u,z=(e['transform'](u4),e['transform'](z4))if sigma else(u4,z4)
  assert u<=mi and not z&ma
  results.append({'label':row['label'],'verdict':'COVERED_NEW_HAND_FOUR_PENDING_REVIEW','sigma':sigma,'reflections':4})
assert sum(r['verdict']=='EXCLUDED_b0_FIXED_B180'for r in results)==161
assert sum(r['verdict']=='COVERED_ACCEPTED_GUARD'for r in results)==44
assert sum(r['verdict']=='COVERED_NEW_HAND_FOUR_PENDING_REVIEW'for r in results)==3
bound=max(r.get('reflections',0)for r in results)
assert bound==5 and max(r['reflections'] for r in forcing)<=5
reads += [HERE/'argument.txt',HERE/'roof-center-four/argument.txt',BASE/'surplus-four-local/four-unit-DR-independent/review.txt',BASE/'surplus-four-local/four-unit-one-DR-independent/review.txt']
out={'status':'PARENT_COMPLETE_NO_DR_FOUR_UNIT_COVER_PENDING_INDEPENDENT_REVIEW','bound':bound,'forcing':forcing,'direct_N_bridge':True,'labels':208,'excluded_fixed_B180':161,'old_guard_cover':44,'new_four_cover':3,'results':results,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)},'limits':'Hand root/leaf/shape/classification and complete support cover, not completed room enumeration. Exact new FOUR verified separately, independent peer review pending. Combining accepted positiveDR result yields proposed wholelocalfourunit<=13, notfullDelta4.'}
(HERE/'join.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],'bound',bound,'208labels/161excluded/44inherited/3newfour;8forcing/directbridge')
