"""Sufficient darkness certificate using finite reflection orbits of lattice points.
A failure is only an arithmetic possibility, never a ray witness.
"""
from collections import deque
from illumination_geometry import check,check_fan_angles,owners_of,edge
from illumination_paths import room

def reflection(e,m):
    a,b=e;dx=b[0]-a[0];dy=b[1]-a[1]
    if dx==0:return (-1,0,0,1,2*a[0]%m,0)
    if dy==0:return (1,0,0,-1,0,2*a[1]%m)
    if dx==dy:
        c=a[0]-a[1];return (0,1,1,0,c%m,(-c)%m)
    assert dx==-dy;c=a[0]+a[1];return (0,-1,-1,0,c%m,c%m)
def compose(a,b,m):
    aa,ab,ac,ad,ax,ay=a;ba,bb,bc,bd,bx,by=b
    return (aa*ba+ab*bc,aa*bb+ab*bd,ac*ba+ad*bc,ac*bb+ad*bd,(aa*bx+ab*by+ax)%m,(ac*bx+ad*by+ay)%m)
def apply(g,p,m):
    a,b,c,d,x,y=g;return ((a*p[0]+b*p[1]+x)%m,(c*p[0]+d*p[1]+y)%m)
def certify(data,m=8):
    assert m>=2 and m&(m-1)==0
    geometry=check(data,strict=False);walls,corners=room(data);generators=set(reflection(e,m) for e in walls);identity=(1,0,0,1,0,0);group={identity};todo=deque([identity])
    while todo:
        g=todo.popleft()
        for r in generators:
            h=compose(r,g,m)
            if h not in group:group.add(h);todo.append(h)
    ts=[tuple(map(tuple,t)) for t in data['triangles']];owners=owners_of(ts);cuts={edge(*e) for e in data.get('slits',[])};opens={e for e,os in owners.items() if len(os)==2 and e not in cuts}
    transparent=[]
    for p in {p for t in ts for p in t}:
        sizes,full=check_fan_angles(ts,p,owners,opens)
        if full or 4 in sizes:transparent.append(p)
    allowed={apply(g,p,m) for g in group for p in transparent};targets={apply(g,tuple(data['marked'][1]),m) for g in group};source=tuple(data['marked'][0]);possibility=None
    for a in range(m):
        for b in range(m):
            if a%2==0 and b%2==0:continue
            for k in range(1,m+1):
                p=((source[0]+k*a)%m,(source[1]+k*b)%m)
                if k>=2 and p in targets:
                    possibility=dict(primitive_direction_residue=[a,b],steps=k,endpoint_residue=p);break
                if p not in allowed:break
            if possibility:break
        if possibility:break
    return dict(modulus=m,reflection_group_order=len(group),target_orbit_size=len(targets),transparent_orbit_size=len(allowed),transparent_BC=geometry['transparent_vertices'],certified_dark=possibility is None,arithmetic_possibility=possibility,note='Possibility is an overapproximation; it does not prove illumination')
if __name__=='__main__':
    import json,sys
    print(json.dumps(certify(json.load(open(sys.argv[1])),int(sys.argv[2]) if len(sys.argv)>2 else 8),indent=2))
