"""Prescribed single calibration only: exact arithmetic, no ray search."""
from fractions import Fraction as Q
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
source = HERE.parents[2] / 'review/resumed-exact-check.py'
tree = ast.parse(source.read_text())
names = {'vec','det','dot','edges','on','location','intersect','simple','path_check'}
ns = {'Q': Q}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]), str(source), 'exec'), ns)
P = [(0,0),(48,0),(48,16),(16,16),(16,48),(0,48)]
S,T,U = (18,4),(14,40),(10,40)
ns['simple'](P)
assert all(ns['location'](P,z)==1 for z in (S,T,U))
assert 96*32+32*64 == 4*(48*16+16*32)

def H(x,y,c):
    width,base = (96,-16) if c=='b' else (32,16)
    return ((x+3*(y-base))%width,y)
def F(x,y,c):
    a,b = H(x,y,c)
    return ((-a)%(96 if c=='b' else 32),b)
assert F(*S,'b') == S
assert F(*T,'t') == U
assert F(*U,'t') == T
corners = [(0,0,'b'),(48,0,'b'),(48,16,'b'),(16,16,'b'),(16,48,'t'),(0,48,'t')]
corner_images = [H(*z) for z in corners]
assert corner_images == [(48,0),(0,0),(48,16),(16,16),(16,48),(0,48)]
# Full boundary functions: displacement is constant on each horizontal
# boundary. Vanishing modulo circumference proves pointwise identity on
# every subarc and hence respects all five actual boundary identifications.
boundaries=[]
for c,width,ys in [('b',96,(-16,16)),('t',32,(16,80))]:
    base = -16 if c=='b' else 16
    for y in ys:
        displacement = 3*(y-base)
        assert displacement % width == 0
        boundaries.append({'cylinder':c,'y':y,'shift':displacement,'circumference':width})
# The inverse has integral slope -3 and integral offsets, so the integer
# point set is preserved in both directions; these are algebraic checks.
assert 3*16 == 48 and -3*16 == -48
assert (-(-8)-3*36,36) == (-100,36)
portal_target = Q(18)+Q(16-4,40-4)*(14-18)
portal_seed = Q(18)+Q(16-4,40-4)*(10-18)
assert portal_target == Q(50,3)>16
assert portal_seed == Q(46,3)<16
ns['path_check'](P,[S,U])
path = [S,(0,Q(262,25)),(16,Q(406,25)),(0,Q(550,25)),(16,Q(694,25)),(0,Q(838,25)),(16,Q(982,25)),T]
result = ns['path_check'](P,path)
assert result == {'wall_leg_guards':42,'reflections':6}
assert Q(path[1][0]-S[0],path[1][1]-S[1]) == Q(-25,9)
time = sum((b[1]-a[1])/9 for a,b in zip(path,path[1:]))
assert time == 4
portal = path[1][0]+(16-path[1][1])*(path[2][0]-path[1][0])/(path[2][1]-path[1][1])
assert portal == portal_seed
out = {'status':'PASS_PRESCRIBED_CALIBRATION','checker_source':str(source),'checker_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_image':list(S),'target_image':list(U),'corner_images':corner_images,'boundary_identity_checks':boundaries,'path':[[str(x),str(y)] for x,y in path],'launch_direction':[-25,9],'time':str(time),'portal_x':str(portal),**result,'scope':'One formula-derived path and affine calibration; gluing and integer-set arguments also require the written hand proof. No universal orbit coverage or novelty established.','search':False}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
