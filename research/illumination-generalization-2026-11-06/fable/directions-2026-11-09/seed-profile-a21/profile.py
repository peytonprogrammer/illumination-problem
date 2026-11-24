from pathlib import Path
from collections import Counter
from itertools import combinations
from math import gcd,lcm,ceil
from fractions import Fraction as F
from functools import cache
import json,subprocess
root=Path("a21")
rank=[]
dist=Counter()
for shard in range(84):
    done=json.loads((root/f"{shard}.done.json").read_text())
    for line in (root/f"{shard}.counts").read_text().splitlines():
        v=line.split()
        if v[0]=='HIST':
            r,h,c=map(int,v[1:]); dist[r,h]+=c
        if v[0]=='TOP':
            h,r,room,x,y,X,Y,p,q,m,b,*rows=map(int,v[1:])
            rank.append((-h,shard,room,y,x,Y,X,r,p,q,m,b,tuple(rows)))
rank=sorted(rank,key=lambda t:t[:2])[:20]
dirs=[(x,s-x) for s in range(1,41) for x in range(s,-1,-1) if gcd(x,s-x)==1]
def corners(rows):
    cells={(x,y) for y,row in enumerate(rows) for x in range(row.bit_length()) if row>>x&1}
    walls=[]
    for x,y in cells:
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if (x+dx,y+dy) not in cells:
                axis=0 if dx else 1
                walls.append((axis,(x+(dx>0)) if dx else (y+(dy>0)), y if dx else x))
    marks=sorted([(x,y) for x,y in cells if {(x-1,y),(x,y-1),(x-1,y-1)}<=cells],key=lambda xy:xy[::-1])
    return walls,marks
def trace(rows,S,T,p,q,m,b):
    walls,_=corners(rows)
    point=tuple(map(F,S)); speed=(p,q); path=[point]; time=F(m)
    while time:
        events=[]
        for a,k,v in walls:
            if not speed[a]:continue
            t=(k-point[a])/speed[a];z=point[1-a]+speed[1-a]*t
            if 0<t<=time and v<=z<=v+1:events.append((t,a))
        t=min((e[0] for e in events),default=time)
        hits={a for l,a in events if l==t}
        assert len(hits)<=1
        point=tuple(z+t*u for z,u in zip(point,speed));path.append(point); time-=t
        if hits:
            a=hits.pop(); speed=tuple(-u if j==a else u for j,u in enumerate(speed))
    assert path[-1]==T and len(path)==b+2,(S,T,p,q,m,b,path)
    return path
@cache
def allpaths(shard,room,rows):
    raw=subprocess.check_output(['./extract',str(root/f'{shard}.bin'),str(room)],text=True).splitlines()
    assert tuple(map(int,raw[0].split()))==rows
    _,marks=corners(rows)
    paths={}
    for (S,T),a in zip(combinations(marks,2),map(int,raw[1].split()),strict=True):
        p,q=dirs[a&511];sh=a>>9&3;p*=1-2*(sh&1);q*=1-2*(sh>>1);m=a>>11&127;b=a>>18
        paths[S,T]=(p,q,m,b,trace(rows,S,T,p,q,m,b))
    return paths
def classify_family(rows,paths,K):
    bx=max(v.bit_length() for v in rows);by=len(rows); choices=[]
    for axis in [0,1]:
        breadth=(bx,by)[axis]
        for j in range(breadth):
            mask=rows[j] if axis else sum((v>>j&1)<<y for y,v in enumerate(rows))
            if mask.bit_count()!=1 or not 0<j<breadth-1:continue
            # The center of a lattice row/column never contains an original mark.
            c=F(2*j+1,2);per=1;load=0;ok=True
            for p,q,m,b,path in paths.values():
                axial=abs((p,q)[axis]);side=abs((q,p)[axis])
                hits=sum(min(A[axis],B[axis])<c<=max(A[axis],B[axis]) for A,B in zip(path,path[1:]))
                # A bounce on the centerline at the strip side still crosses it once.
                if hits:
                    per=lcm(per,2*axial//gcd(side,2*axial))
                    if m*axial>K*breadth or hits>K:ok=False
                load=max(load,hits)
            choices.append((not ok,load,per,axis,j))
    return min(choices,default=None)
def svg(rows,path,i,ox,oy):
    bx=max(x.bit_length() for x in rows);by=len(rows);u=min(215/bx,202/by);sx=ox+(220-u*bx)/2;sy=oy+222
    def xy(x,y):return (sx+float(x)*u,sy-float(y)*u)
    parts=[f'<text x="{ox+5}" y="{oy+17}" font-size="15">#{i}</text>']
    for y,row in enumerate(rows):
        for x in range(row.bit_length()):
            if row>>x&1:
                X,Y=xy(x,y+1);parts.append(f'<rect x="{X:.2f}" y="{Y:.2f}" width="{u+.05:.2f}" height="{u+.05:.2f}" fill="#e4eaf1"/>')
    walls,_=corners(rows)
    for a,k,v in walls:
        A,B=(xy(k,v),xy(k,v+1)) if a==0 else (xy(v,k),xy(v+1,k))
        parts.append(f'<path d="M{A[0]:.2f},{A[1]:.2f} L{B[0]:.2f},{B[1]:.2f}" stroke="#283747"/>')
    pts=' '.join('%.2f,%.2f'%xy(*pt) for pt in path)
    parts.append(f'<polyline points="{pts}" stroke="#427ba6" stroke-width="1" opacity=".82" fill="none"/>')
    for pt,color in [(path[0],"#0d8752"),(path[-1],"#b51c43")]:
        X,Y=xy(*pt);parts.append(f'<circle cx="{X:.2f}" cy="{Y:.2f}" r="3.4" fill="{color}" stroke="white" stroke-width=".8"/>')
    return ''.join(parts)
audit=Path('audit.log').read_text().splitlines()
bincounts=Counter(); files={}
for line in audit:
    v=line.split()
    if v[0]=='BIN':
        r,h,c=map(int,v[1:]);bincounts[r,h]+=c
    else:files[int(Path(v[1]).stem)]=list(map(int,v[2:]))
assert bincounts==dist and len(files)==84 and sum(dist.values())==1604242406
K=max(v[2] for v in files.values());C=max(v[3] for v in files.values())
images=[];table=[];evidence=[];family=[]
for i,(nh,shard,room,y,x,Y,X,r,p,q,m,b,rows) in enumerate(rank,1):
    paths=allpaths(shard,room,rows);pp,qq,mm,bb,path=paths[(x,y),(X,Y)]
    assert (pp,qq,mm,bb)==(p,q,m,b)
    vwall=sum((B[0]-A[0])*(C0[0]-B[0])<0 for A,B,C0 in zip(path,path[1:],path[2:]))
    images.append(svg(rows,path,i,(i-1)%4*230,(i-1)//4*235))
    evidence.append(dict(rank=i,shard=shard,eligible_room=room,rows=rows,S=(x,y),T=(X,Y),direction=(p,q),steps=m,points=[[str(c) for c in pt] for pt in path]))
    table.append(f'| {i} | {shard}/{room} | {r} | ({x},{y}) → ({X},{Y}) | ({p},{q}) | {-nh} | {m} | {vwall} + {b-vwall} = {b} |')
    result=classify_family(rows,paths,K)
    if result:
        bad,load,period,axis,j=result
        family.append((i,len(paths),('x','y')[axis],j,period,load,not bad))
    else:family.append((i,len(paths),'-','-',0,0,False))
Path('paths.json').write_text(json.dumps(evidence,indent=1))
Path('hardest.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="920" height="1175" viewBox="0 0 920 1175"><rect width="100%" height="100%" fill="white"/><g font-family="sans-serif">'+''.join(images)+'</g></svg>')
Path('table.md').write_text('\n'.join(table))
Path('family.json').write_text(json.dumps(family))
print('K,C',K,C,'max m,b',max(v[4] for v in files.values()),max(v[5] for v in files.values()))
print('FAMILY',family)
print('TOP',*table,sep='\n')
