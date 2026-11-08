"""Independent prescribed rotated-U paths in original TR05 rooms; no search."""
from fractions import Fraction as F
from pathlib import Path
import ast,json

HERE=Path(__file__).parent
old=ast.parse((HERE/'resumed-exact-check.py').read_text())
ns={'Q':F,'F':F}
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-geometric-predicates>','exec'),ns)
old=ast.parse((HERE/'three-reflex-tr01-independent-check.py').read_text())
names={'point','L_vertical','L_horizontal','U_opposite','U_path'}
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-specific-U-L>','exec'),ns)

def run(label,params,S,T):
    a,l,w,A,b,c,h,H=map(F,params);S=tuple(map(F,S));T=tuple(map(F,T))
    s,u=S;t,v=T
    assert 0<a<w<A and 0<l<w and 0<b<h<H and 0<c<h and (a<l or c<b)
    assert a<=s<=w and h<u<H and l<t<A and 0<v<c
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    ns['simple'](P);assert ns['location'](P,S)==ns['location'](P,T)==1
    alpha,omega,capwidth,base,HL,HR=H-h,H-c,H,A-w,A,A-l
    X,Y=(H-u,A-s),(H-v,A-t)
    prime=ns['U_path'](alpha,omega,capwidth,base,HL,HR,X,Y)
    # The same whole-room Euclidean isometry is its inverse in these coordinates.
    path=[(A-yp,H-xp) for xp,yp in prime]
    assert path[0]==S and path[-1]==T
    assert (a,h) not in path
    result=ns['path_check'](P,path)
    contacts=[]
    for p in path[1:-1]:
        walls=[(x,y) for x,y in ns['edges'](P) if ns['on'](x,y,p)]
        if walls:
            contacts.append(p)
            if p[1]==h:assert p[0]>s>=a
    # Independently trim at an earlier actual target if present; the explicit
    # fixtures below are required to reach it first at their final event.
    for p,q in zip(path[:-2],path[1:-1]):
        assert not ns['on'](p,q,T)
    return dict(label=label,parameters=params,source=S,target=T,
        target_prime_height=Y[1],source_prime_height=X[1],path=path,
        original_shelf_contacts=[p for p in contacts if p[1]==h],**result)

G=(4,12,20,28,4,8,20,28)
fixtures=[('source-at-a',G,(4,24),(14,2)),
          ('source-artificial-cut-w',G,(20,24),(14,2)),
          ('target-base',G,(8,24),(24,2)),
          ('source-level-base',G,(20,24),(24,2)),
          ('target-level-base',G,(4,24),(20,2)),
          ('both-levels',G,(20,24),(20,2)),
          ('very-thin-cap',(4,12,20,28,4,8,20,F(201,10)),(4,F(401,20)),(14,2)),
          ('near-roof',G,(4,F(2799,100)),(14,F(1,100))),
          ('overlap-x',(12,4,20,28,12,8,20,28),(12,24),(6,2)),
          ('equal-side',(8,8,20,28,12,8,20,28),(8,24),(10,2)),
          ('equal-level',(4,12,20,28,8,8,20,28),(4,24),(14,2)),
          ('thin-real',(F(2,3),F(5,3),F(7,3),F(11,3),F(1,5),F(2,5),F(3,5),F(4,5)),
           (F(2,3),F(7,10)),(2,F(1,5)))]
rows=[run(*fixture) for fixture in fixtures]
out=dict(status='PASS_INDEPENDENT_TR05_PRESCRIBED_ROTATED_U',rows=rows,
    reflections=sum(r['reflections'] for r in rows),
    wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    author_code_executed=False,search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
