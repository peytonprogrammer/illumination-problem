"""TR05 prescribed exact replay. Reuses disclosed U formulas, no discovery."""
from fractions import Fraction as F
from pathlib import Path
import ast
import json

BASE = Path(__file__).parent.parent
ns = {'F': F}
for file, names in [
    (BASE/'review/three-reflex-tr01-independent-check.py',
     {'point', 'L_vertical', 'L_horizontal', 'U_opposite', 'U_path'}),
    (BASE/'construction/three-reflex-tall-prescribed-check.py', {'wave', 'validate'}),
]:
    tree = ast.parse(file.read_text())
    exec(compile(ast.Module(body=[n for n in tree.body
                                 if isinstance(n, ast.FunctionDef) and n.name in names],
                            type_ignores=[]), str(file), 'exec'), ns)
ns['fold'] = ns['wave']


def run(label, geometry, source, target):
    a,l,w,A,b,c,h,H = map(F, geometry)
    s,u = map(F,source)
    t,v = map(F,target)
    assert 0<a<w<A and 0<l<w and 0<b<h<H and 0<c<h
    assert a<l or c<b
    assert a<=s<=w and h<u<H and l<t<A and 0<v<c
    U = ns['U_path'](H-h,H-c,H,A-w,A,A-l,(H-u,A-s),(H-v,A-t))
    path = [(A-y,H-x) for x,y in U]
    assert path[0]==(s,u) and path[-1]==(t,v)
    # Stop at the first actual T, if the accepted formula already passed it.
    clipped=[path[0]]
    for p,q in zip(path,path[1:]):
        dx,dy=q[0]-p[0],q[1]-p[1]
        theta=(t-p[0])/dx if dx else (v-p[1])/dy
        if 0<theta<=1 and (p[0]+theta*dx,p[1]+theta*dy)==(t,v):
            clipped.append((t,v))
            break
        clipped.append(q)
    assert clipped[-1]==(t,v)
    timed=[(F(0),clipped[0])]
    for p,q in zip(clipped,clipped[1:]):
        dt=abs(q[0]-p[0])+abs(q[1]-p[1])
        assert dt>0
        timed.append((timed[-1][0]+dt,q))
    poly=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    refs,guards=ns['validate'](poly,timed,(s,u),(t,v))
    for x,y in clipped[1:-1]:
        if y==h:
            assert x>a or x>=w
        assert (x,y)!=(a,h)
    return {'label':label,'geometry':geometry,'source':source,'target':target,
            'reflections':refs,'finite_wall_checks':guards,'path':clipped,'status':'PASS'}


if __name__=='__main__':
    G=(4,12,20,28,4,8,20,28)
    cases=[
        ('upper-interior',G,(10,24),(14,2)),
        ('s-equals-a',G,(4,24),(14,2)),
        ('s-equals-w',G,(20,24),(14,2)),
        ('t-equals-w',G,(10,24),(20,2)),
        ('both-portal-levels',G,(20,24),(20,2)),
        ('target-in-base',G,(4,24),(24,2)),
        ('source-level-base',G,(20,24),(24,2)),
        ('overlapping-x-arms',(12,4,20,28,12,8,20,28),(12,24),(6,2)),
        ('a-equals-l',(12,12,20,28,12,8,20,28),(12,24),(14,2)),
        ('b-equals-c',(4,12,20,28,8,8,20,28),(4,24),(14,2)),
        ('thin-cap',(4,12,20,28,4,8,20,F(201,10)),(4,F(401,20)),(14,2)),
    ]
    rows=[run(*c) for c in cases]
    out={'status':'PASS','prescribed_cases':len(rows),'cases':rows,
         'reflections':sum(r['reflections'] for r in rows),
         'finite_wall_checks':sum(r['finite_wall_checks'] for r in rows),
         'formula_reuse':'Read-only AST extraction of reviewer TR01 U/L functions, own TR03 all-wall guards; not an independent implementation.',
         'search_used':False,'whole_r3_complete':False,'whole_goal_complete':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
