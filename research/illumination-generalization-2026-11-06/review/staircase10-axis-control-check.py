"""One hand-prescribed oblique ray on the frozen axis-obstruction room."""
from fractions import Fraction as Q
from pathlib import Path
import ast,hashlib,json
ROOT=Path('.context/illumination-generalization-2026-11-06')
HERE=ROOT/'review'
source=HERE/'resumed-exact-check.py'
pin_files=[source,ROOT/'construction/axis-only-obstruction.md',HERE/'axis-only-independent.md',HERE/'axis-only-independent-acceptance.json']
pins={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pin_files}
names={'vec','det','dot','edges','on','location','intersect','simple','path_check'}
ns={'Q':Q}
exec(compile(ast.Module(body=[f for f in ast.parse(source.read_text()).body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<existing reviewer pure geometry/path guards>','exec'),ns)
P=[(0,0),(40,0),(40,12),(12,12),(12,16),(8,16),(8,20),(4,20),(4,40),(0,40)]
path=[(Q(38),Q(2)),(Q(0),Q(44,3)),(Q(8),Q(52,3)),(Q(0),Q(20))]
path += [(Q(4 if j%2 else 0),Q(20)+Q(4*j,3)) for j in range(1,14)]
path += [(Q(2),Q(38))]
ns['simple'](P)
check=ns['path_check'](P,path)
assert check=={'wall_leg_guards':170,'reflections':16},check
for a,b in zip(path,path[1:]):
 assert b[1]>a[1]
 assert abs((b[0]-a[0])/(b[1]-a[1]))==3
assert (path[1][0]-path[0][0])/(path[1][1]-path[0][1])==-3
seam_contacts={}
for Y in (12,16,20):
 xs=[]
 for a,b in zip(path,path[1:]):
  if a[1]<=Y<=b[1]:
   xs.append(a[0]+(Y-a[1])*(b[0]-a[0])/(b[1]-a[1]))
 assert xs and len(set(xs))==1
 seam_contacts[str(Y)]=xs[0]
assert seam_contacts=={'12':Q(8),'16':Q(4),'20':Q(0)}
assert (0,20) not in P and ns['location'](P,(Q(0),Q(20)))==0
# Every contact is on an actual maximal wall and is not a genuine corner.
contact_walls=[]
for z in path[1:-1]:
 hits=[(a,b) for a,b in ns['edges'](P) if ns['on'](a,b,z)]
 assert len(hits)==1 and z not in P
 contact_walls.append(hits[0])
assert any(a[0]==b[0]==8 for a,b in contact_walls)
assert all(a[0]==b[0] for a,b in contact_walls)
for p in pin_files:assert hashlib.sha256(p.read_bytes()).hexdigest()==pins[str(p)]
out={'status':'EXACT_PRESCRIBED_OBLIQUE_WITNESS_PASS','room_widths':[40,12,8,4],'room_heights':[0,12,16,20,40],'S':[38,2],'T':[2,38],'initial_velocity':[-3,1],'actual_first_target_vertical_time':36,'y_strictly_increasing':True,'seam_x':seam_contacts,'smooth_wall_seam_contact':[0,20],'non_axis_step_contact':[Q(8),Q(52,3)],'path':path,'contact_walls':contact_walls,**check,'source_pins':pins,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'One frozen axis-only-obstruction control is actually illuminated. No all-metric staircase or all-pair theorem follows.','new_direction_search':False,'new_room':False,'new_engine':False,'full_goal_complete':False}
(HERE/'staircase10-axis-control-check.json').write_text(json.dumps(out,default=str,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('path','contact_walls','source_pins')},default=str,indent=2))
