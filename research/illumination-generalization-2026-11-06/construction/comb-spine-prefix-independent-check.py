from pathlib import Path
from fractions import Fraction as Q
import json,itertools
p=Path(__file__).parent;r=p.parent/'review'
def v(x):return tuple(map(Q,x))
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def on(a,b,z):return cross(sub(b,a),sub(z,a))==0 and all(min(a[i],b[i])<=z[i]<=max(a[i],b[i]) for i in (0,1))
def inside(poly,z):
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if on(a,b,z):return False
    parity=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>z[1])!=(b[1]>z[1]):
            x=a[0]+(z[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if x>z[0]:parity=not parity
    return parity

def check(data,scale=1):
    poly=[tuple(scale*q for q in v(x)) for x in data['polygon']]
    path=[tuple(scale*q for q in v(x)) for x in data['path']]
    source=tuple(scale*q for q in v(data['source']));target=tuple(scale*q for q in v(data['target']))
    assert path[0]==source and path[-1]==target and inside(poly,source) and inside(poly,target)
    walls=list(zip(poly,poly[1:]+poly[:1]));guards=0;reflections=0
    for a,b in zip(path,path[1:]):
        vel=sub(b,a);assert vel!=(0,0)
        assert inside(poly,tuple((a[i]+b[i])/2 for i in (0,1)))
        for c,d in walls:
            guards+=1;w=sub(d,c);den=cross(vel,w)
            if den==0:
                assert cross(sub(c,a),vel)!=0,'wall collinearity'
                continue
            t=cross(sub(c,a),w)/den;s=cross(sub(c,a),vel)/den
            if 0<=t<=1 and 0<=s<=1:
                assert t in(0,1),'intermediate wall hit'
                assert 0<s<1,'polygon corner'
        if b!=target:
            assert not on(a,b,target),'earlier actual target'
    for i,z in enumerate(path[1:-1],1):
        before=sub(z,path[i-1]);after=sub(path[i+1],z)
        contacts=[(a,b) for a,b in walls if on(a,b,z)]
        assert len(contacts)<=1
        if contacts:
            reflections+=1;a,b=contacts[0]
            expected=(-before[0],before[1]) if a[0]==b[0] else(before[0],-before[1])
        else:
            assert inside(poly,z);expected=before
        assert cross(expected,after)==0 and dot(expected,after)>0,'reflection law'
    assert reflections==data['reflections']
    return {'scale':scale,'reflections':reflections,'all_wall_leg_guards':guards,'actual_endpoints':True,'strict_all_corners':True}

controls=json.loads((r/'comb-spine-end-actual-controls.json').read_text())
first=json.loads((r/'comb-spine-end-prefix-check.json').read_text())
positive=[check(first['control']),check(first['control'],12),check(controls['odd_target_branch']),check(controls['tooth_end_repair']),check(controls['tooth_end_repair'],20)]
reject=[]
for orient in(1,-1):
  for ss,st in itertools.product((1,-1),repeat=2):
    counts={'source_portal_failure':0,'target_portal_failure':0,'integer_spine_failure':0,'success':0}
    he=Q(9*orient);be=Q(16,5) if orient==1 else Q(4,5)
    for ell in range(22):
      tau=(he-ss*Q(4,5)-st*be+2*ell)/Q(11,2)
      rs=(ss*Q(4,5)+tau/2)%2;rt=(st*be+tau)%8
      if not 0<rs<1:counts['source_portal_failure']+=1
      elif not 0<rt<4:counts['target_portal_failure']+=1
      elif ((rs+rt+4*tau-he)/32).denominator!=1:counts['integer_spine_failure']+=1
      else:counts['success']+=1
    assert counts['success']==0
    reject.append({'target_orientation':orient,'source_sign':ss,'target_sign':st,**counts})
result={'status':'PASS','method':'Independent exact prescribed arithmetic and all-wall path verifier; no discovery or peer-code import','positive_actual_paths':positive,'total_reflections':sum(x['reflections'] for x in positive),'total_all_wall_leg_guards':sum(x['all_wall_leg_guards'] for x in positive),'restricted_classes':176,'all_rejected':True,'rejection_breakdown':reject,'darkness_asserted':False,'whole_goal_complete':False}
(p/'comb-spine-prefix-independent-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
