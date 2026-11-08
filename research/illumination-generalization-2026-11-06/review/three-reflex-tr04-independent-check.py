"""Prescribed independent checks of TR04's enlarged geometry and transposition."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil
import ast,json,hashlib

HERE=Path(__file__).parent
base_tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':Q,'F':Q,'floor':floor,'ceil':ceil}
exec(compile(ast.Module(body=[f for f in base_tree.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-geometry>','exec'),ns)

def enlarged(a,l,w,A,b,c,h,H):
    return 0<a<w<A and 0<l<w and 0<b<h<H and 0<c<h and (a<l or c<b)

# Reuse our independent TR03 arithmetic construction unchanged except the
# geometry assertion under review; actual path predicates remain unchanged.
t=ast.parse((HERE/'three-reflex-tr03-independent-check.py').read_text())
defs=[f for f in t.body if isinstance(f,ast.FunctionDef) and f.name in
    {'fold','partition_roots','verify'}]
changes=0
for f in defs:
    if f.name=='verify':
        for statement in f.body:
            if isinstance(statement,ast.Assert) and ast.unparse(statement.test)=='0 < a < l < w < A and 0 < b < c < h < H':
                statement.test=ast.parse('enlarged(a,l,w,A,b,c,h,H)',mode='eval').body
                changes+=1
assert changes==1
ns.update(scope=ns,enlarged=enlarged)
exec(compile(ast.fix_missing_locations(ast.Module(body=defs,type_ignores=[])),
    '<own-TR03-construction-expanded-domain>','exec'),ns)
verify=ns['verify']

# Import only the already independently checked reviewer U/L formulas.
t=ast.parse((HERE/'three-reflex-tr01-independent-check.py').read_text())
defs=[f for f in t.body if isinstance(f,ast.FunctionDef) and f.name in
    {'point','L_vertical','L_horizontal','U_opposite','U_path'}]
ns.update(simple=ns['simple'],path_check=ns['path_check'],location=ns['location'])
exec(compile(ast.Module(body=defs,type_ignores=[]),'<reviewer-U-L>','exec'),ns)

def partial(label,params,S,T,region):
    a,l,w,A,b,c,h,H=map(Q,params);S=tuple(map(Q,S));T=tuple(map(Q,T))
    assert enlarged(a,l,w,A,b,c,h,H)
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    ns['simple'](P)
    assert ns['location'](P,S)==ns['location'](P,T)==1
    if region=='G':
        def G(p):return (p[0]<a and p[1]>b) or p[1]>=h or (p[0]>w and p[1]>=c)
        assert G(S) and G(T)
        path=ns['U_path'](a,w,A,H-h,H-b,H,(S[0],H-S[1]),(T[0],H-T[1]))
        path=[(x,H-y) for x,y in path]
    else:
        R=[(l,0),(A,0),(A,H),(w,H),(w,c),(l,c)]
        assert ns['location'](R,S)==ns['location'](R,T)==1
        path=ns['L_horizontal'](A-l,A-w,c,H,(A-S[0],S[1]),(A-T[0],T[1]))
        path=[(A-x,y) for x,y in path]
    return dict(label=label,region=region,parameters=params,source=S,target=T,
        **ns['path_check'](P,path))

G=(4,2,8,12,6,3,10,183)
cross=[verify('overlap-x-left',G,(1,7),(3,1)),
       verify('target-left-of-source',(12,4,20,28,12,8,20,680),(10,14),(6,2)),
       verify('overlap-x-upper',G,(3,10),(3,1)),
       verify('overlap-x-cut',G,(8,14),(3,1)),
       verify('equal-x-arms',(4,4,8,12,6,3,10,183),(1,7),(5,1)),
       verify('equal-floor-levels',(4,5,8,12,3,3,10,183),(1,7),(6,1))]
parts=[partial('new-G-right-c-seam',G,(1,7),(10,3),'G'),
       partial('new-G-opposite-arms',G,(1,7),(10,7),'G'),
       partial('new-R-left-bottom',G,(3,1),(10,14),'R'),
       partial('equal-x-G',(4,4,8,12,6,3,10,183),(1,7),(10,3),'G'),
       partial('equal-floor-G',(4,5,8,12,3,3,10,183),(1,7),(10,3),'G')]

wide=tuple(map(Q,(4,12,20,680,4,8,20,28)))
a,l,w,A,b,c,h,H=wide
transposed=(c,b,h,H,l,a,w,A)
assert enlarged(*transposed)
V=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
Vp=[(transposed[0],transposed[4]),(transposed[0],transposed[6]),
    (transposed[2],transposed[6]),(transposed[2],transposed[5]),
    (transposed[1],transposed[5]),(transposed[1],0),(transposed[3],0),
    (transposed[3],transposed[7]),(0,transposed[7]),(0,transposed[4])]
swapped=[(y,x) for x,y in reversed(V)]
assert any(swapped[j:]+swapped[:j]==Vp for j in range(10))
row=verify('transposed-wide-original',transposed,(2,14),(6,2))
# Swap/reverse the witnessed trajectory back to original S=(2,6),T=(14,2).
original_path=[(y,x) for x,y in reversed(row['path'])]
assert original_path[0]==(2,6) and original_path[-1]==(14,2)
back=ns['path_check'](V,original_path)
vertical_L=(A-w)/(2*c)
vertical_delta=vertical_L/(ceil(vertical_L*h/(2*a))+ceil(vertical_L*h/(2*(A-w)))+3)
assert H<c+2*A/vertical_delta
cross.append(row)
out=dict(status='PASS_INDEPENDENT_TR04_PRESCRIBED_REPLAY',
    method='Own prior independently checked arithmetic andU/L formulas; actual original geometry guards; noauthorcodeexecution.',
    cross_cases=cross,partial_cases=parts,transposed_back=back,
    reflections=sum(r['reflections'] for r in cross+parts),
    wall_leg_guards=sum(r['wall_leg_guards'] for r in cross+parts),
    search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('cross_cases','partial_cases')}))
