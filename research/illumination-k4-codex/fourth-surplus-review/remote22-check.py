"""Check named inherited guards against three prescribed leaf additions only."""
from pathlib import Path
from fractions import Fraction as F
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OLD=ROOT/'third-surplus-review'
tri=lambda t:tuple(sorted(map(tuple,t)))
read=lambda p:json.loads(p.read_text())
checker=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
paths={};sources={}
def retain(file,rows,family=None):
 p=OLD/file;raw=p.read_bytes();sources[file]=hashlib.sha256(raw).hexdigest();data=json.loads(raw)
 if family:data=data['families'][family]
 terms=data['terms']
 for line in rows:
  matches=[t for t in terms if t['source_line']==line]
  assert len(matches)==1,(file,family,line,len(matches))
  paths[f'{file}:{family or ""}:{line}']=matches[0]['path']
retain('remote-B-project.json',[3597,3039,515])
retain('center-half-project.json',[907,958,515,3777,2534,652,361,3224,2642])
retain('local-e2-project.json',[3580], 'L_Hupper3_Nrminus')
retain('local-e2-project.json',[664], 'B_Hwest3')
retain('local-e2-project.json',[664], 'B_rectangle4')
for file in ['healed-frozen.json','half-fan-frozen.json','center-residue-frozen.json']:
 p=OLD/file;raw=p.read_bytes();sources[file]=hashlib.sha256(raw).hexdigest()
 for key,t in json.loads(raw)['hits'].items():paths[f'{file}:{key}']=t['path']
additions={
 'L_center_left':tri(((-2,2),(-2,1),(-3,1))),
 'L_center_right':tri(((-2,2),(-2,1),(-1,1))),
 'L_quarter_left_extra':tri(((-2,2),(-3,1),(-3,2))),
 'L_quarter_right_extra':tri(((-2,2),(-1,1),(-1,2))),
 'B_center_lower':tri(((-2,-2),(-1,-2),(-1,-3))),
 'B_quarter_upper_extra':tri(((-2,-2),(-1,-1),(-2,-1))),
 'B_quarter_lower_extra':tri(((-2,-2),(-1,-3),(-2,-3))),
}
results={}
for name,raw in paths.items():
 path=[tuple(F(*x) for x in p) for p in raw]
 assert path[0]==(0,0) and path[-1]==(2,2)
 u,z=checker['path_requirements'](path)
 conflicts=[a for a,t in additions.items() if t in z]
 results[name]={'reflections':len(path)-2,'blocked_additions':conflicts,'required_triangles':sorted(u),'forbidden_triangles':sorted(z),'path':raw}
out={'status':'FIXED_GUARD_COMPARISON','scope':'Only previously named proof rows and their retained coordinates; no archives, room assignments, new paths, or discovery. Absence of a blocked addition alone is not a family cover.','sources':sources,'additions':additions,'paths':results}
(HERE/'remote22-check.json').write_text(json.dumps(out,indent=2)+'\n')
for name,v in results.items():print(name,v['blocked_additions'])
# Hand-listed symbolic implications. These are not whole-room assignments.
slots={n:tri(t) for n,t in read(ROOT/'zero-surplus-L/guard-incidence-check.json')['cap_options'].items()}
core=set().union(*(checker['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,m):
 return {tri((a,(a[0]+dirs[i%8][0],a[1]+dirs[i%8][1]),(a[0]+dirs[(i+1)%8][0],a[1]+dirs[(i+1)%8][1]))) for i in range(start,start+m)}
def oldpath(label,file,key=None):
 p=ROOT/file;data=read(p);sources[file]=hashlib.sha256(p.read_bytes()).hexdigest()
 raw=data['paths'][key]['path'] if key else data['path']
 paths[label]=raw
oldpath('old13','zero-surplus-L/cover-check.json','thirteen')
oldpath('L11','first-surplus-review/square-exchange-check.json','L_thirteen')
oldpath('centerL3','first-surplus-review/residual-cover-check.json')
def guard(label):
 return checker['path_requirements']([tuple(F(*x) for x in p) for p in paths[label]])
implications={}
def implication(name,root_a,root_start,root_m,leaf_a,leaf_start,present,absent,path):
 root=fan(root_a,root_start,root_m);leaf=fan(leaf_a,leaf_start,2)
 owncaps={n for n,t in slots.items() if root_a in t}
 fixed=core|root|leaf|{slots[n] for n in present}
 possible=core|root|leaf|{t for n,t in slots.items() if n not in owncaps and n not in absent}
 u,z=guard(path)
 implications[name]={'status':'PASS' if u<=fixed and not z&possible else 'FAIL','path_key':path,'missing':sorted(u-fixed),'blocked':sorted(z&possible),'root':[root_a,root_start,root_m],'leaf':[leaf_a,leaf_start,2],'present':present,'absent':absent}
basepresent=['B+','E-','T-'];baseabs=['B-','E+','T+']
# All south-facing critical L cases except the rectangular parent need centerL3.
for label,st,m in [('south_triple',6,3),('south_full',5,4)]:
 for ls in ([1] if m==3 else [0,1,2]):
  implication(label+'_leaf'+str(ls),(-2,0),st,m,(-2,-2),ls,basepresent,baseabs,'centerL3')
implication('south_rectangle_Nbminus',(-2,0),6,4,(-2,-2),1,basepresent+['Nb-'],baseabs+['Nb+','Nr-','Nr+'],'L11')
# North-quarter parent + centered leaf: L11 covers every bottom/empty N slot.
for n in ['Nb-','Nb+','empty']:
 implication('north_quarter_'+n,(-2,0),7,3,(-2,2),5,basepresent+([] if n=='empty' else [n]),baseabs+[x for x in ['Nb-','Nb+','Nr-','Nr+'] if x!=n],'L11')
# Full-north parents with single H half: old13 if N is not bottom-facing.
for lab,m in [('north_triple',3),('north_outward_half',4)]:
 implication(lab+'_Nnotbottom',(-2,0),0,m,(-2,2),5,basepresent,baseabs+['Nb-','Nb+'],'old13')
 for n,record in [('Nb+','remote_right_Nb+'),('Nb-','remote_right_Nb-')]:
  receipt='healed-frozen.json' if m==3 else 'half-fan-frozen.json'
  implication(lab+'_'+n,(-2,0),0,m,(-2,2),5,basepresent+[n],baseabs+['D-','D+','R-','R+']+[x for x in ['Nb-','Nb+','Nr-','Nr+'] if x!=n],receipt+':'+record)
# B parents with only a quarter at the remote-facing west C.
for lab,st,m,fam in [('B_west_triple',1,3,'B_Hwest3'),('B_rectangle',0,4,'B_rectangle4')]:
 implication(lab,(0,-2),st,m,(-2,-2),7,['L+','E-'],['L-','E+'],f'local-e2-project.json:{fam}:664')
out['sources']=sources;out['symbolic_implications']=implications
(HERE/'remote22-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('SYMBOLIC IMPLICATIONS')
for n,v in implications.items():print(n,v['status'],'missing',v['missing'],'blocked',v['blocked'])
