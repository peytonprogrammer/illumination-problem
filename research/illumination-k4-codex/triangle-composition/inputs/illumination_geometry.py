"""Exact integer geometry and independent certificates; no solver dependency."""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

DIRS = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def edge(a,b): return tuple(sorted((tuple(a),tuple(b))))
def label(p): return 'A' if not(p[0]%2 or p[1]%2) else 'B' if p[0]%2 and p[1]%2 else 'C'
def patch(x0,x1,y0,y1):
    out=[]
    for x in range(x0,x1):
        for y in range(y0,y1):
            corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
            a=next(p for p in corners if label(p)=='A'); b=next(p for p in corners if label(p)=='B')
            out.extend(tuple(sorted((a,b,c))) for c in corners if label(c)=='C')
    return sorted(out)
def edges_of(t): return [edge(a,b) for a,b in combinations(t,2)]
def owners_of(ts):
    out=defaultdict(list)
    for i,t in enumerate(ts):
        for e in edges_of(t): out[e].append(i)
    return dict(out)
def wedge_slots(t,p):
    rays=[]
    for q in t:
        if q!=p:
            d=(q[0]-p[0],q[1]-p[1]); m=max(map(abs,d)); rays.append(DIRS.index((d[0]//m,d[1]//m)))
    a,b=rays
    if (b-a)%8>4: a,b=b,a
    return [(a+j)%8 for j in range((b-a)%8)]
def local_sectors(ts,p,open_edges):
    """Angular components, in units of 45 degrees; walls separate components."""
    occupied=set(); transitions=set()
    for t in ts:
        if p not in t: continue
        slots=wedge_slots(t,p); occupied.update(slots)
        for j in slots[:-1]: transitions.add((j+1)%8)
    for e in open_edges:
        if p in e:
            q=e[0] if e[1]==p else e[1]; d=(q[0]-p[0],q[1]-p[1]);m=max(map(abs,d))
            transitions.add(DIRS.index((d[0]//m,d[1]//m)))
    if len(occupied)==8 and len(transitions)==8: return [], True
    seen=set(); sizes=[]
    for j in sorted(occupied):
        if j in seen: continue
        seen.add(j); todo=[j];size=0
        while todo:
            s=todo.pop();size+=1
            for n,r in [((s+1)%8,(s+1)%8),((s-1)%8,s)]:
                if r in transitions and n in occupied and n not in seen:
                    seen.add(n);todo.append(n)
        sizes.append(size)
    return sizes,False

def check_fan_angles(ts,p,owners,opens):
    """Independent check via tile fans, without the solver's angular-slot code."""
    incident={i for i,t in enumerate(ts) if p in t};graph=defaultdict(set);has_wall=False
    if not incident: return [],False
    for e,os in owners.items():
        if p not in e: continue
        if e in opens:
            a,b=os;graph[a].add(b);graph[b].add(a)
        else: has_wall=True
    if not has_wall: return [],True
    seen=set();angles=[]
    for i in incident:
        if i in seen:continue
        seen.add(i);todo=[i];angle=0
        while todo:
            j=todo.pop();q,r=[v for v in ts[j] if v!=p]
            dot=(q[0]-p[0])*(r[0]-p[0])+(q[1]-p[1])*(r[1]-p[1])
            angle+=2 if dot==0 else 1
            for k in graph[j]:
                if k not in seen:seen.add(k);todo.append(k)
        angles.append(angle)
    return sorted(angles),False

def check(data, strict=True):
    ts=[tuple(sorted(map(tuple,t))) for t in data['triangles']]
    assert len(set(ts))==len(ts), 'duplicate tile'
    legal=set(patch(min(p[0] for t in ts for p in t),max(p[0] for t in ts for p in t),min(p[1] for t in ts for p in t),max(p[1] for t in ts for p in t)))
    assert set(ts)<=legal, 'tile outside canonical reflection tiling'
    owners=owners_of(ts);cuts={edge(*e) for e in data.get('slits',[])}
    assert all(e in owners and len(owners[e])==2 for e in cuts), 'slit must separate two tiles'
    opens={e for e,os in owners.items() if len(os)==2 and e not in cuts}
    graph=defaultdict(set)
    for e in opens:
        a,b=owners[e];graph[a].add(b);graph[b].add(a)
        # Shared triangles must be exact geometric reflections across e.
        p,q=e;u=next(v for v in ts[a] if v not in e);v=next(v for v in ts[b] if v not in e)
        d=(q[0]-p[0],q[1]-p[1]); w=(u[0]-p[0],u[1]-p[1]);n=d[0]**2+d[1]**2
        dot=w[0]*d[0]+w[1]*d[1]
        reflected=tuple(Fraction(2*dot*d[k],n)-w[k]+p[k] for k in (0,1))
        assert reflected==v, 'reflection mismatch'
    seen={0};todo=[0]
    while todo:
        for j in graph[todo.pop()]:
            if j not in seen:seen.add(j);todo.append(j)
    assert len(seen)==len(ts), 'disconnected interior'
    vertices=sorted({p for t in ts for p in t}); interior=[];contact=[];turns=0; sectors={};transparent=[]
    for p in vertices:
        sizes,full=check_fan_angles(ts,p,owners,opens)
        if full:
            if label(p)!='A':
                transparent.append(p)
                if strict: raise AssertionError(('transparent non-A vertex',p))
            interior.append(p)
        else:
            if label(p)!='A' and 4 in sizes:
                transparent.append(p)
                if strict: raise AssertionError(('non-A on straight wall',p))
            turns+=sum(s!=4 for s in sizes)
            if len(sizes)>1:contact.append(p)
            sectors[str(p)]=sizes
    marked=list(map(tuple,data['marked']))
    assert len(marked)==2 and marked[0]!=marked[1] and all(p in interior and label(p)=='A' for p in marked), 'marks must be distinct interior A vertices'
    boundary=[e for e,o in owners.items() if len(o)==1]
    euler=len(vertices)-len(owners)+len(ts)
    simple=not cuts and not contact and euler==1
    if data.get('require_simple'): assert simple, 'boundary is not a simple Jordan polygon'
    return dict(simple_polygon=simple,tile_complex_euler=euler,tiles=len(ts),walls=turns,interior_A=[p for p in interior if label(p)=='A'],transparent_vertices=transparent,slit_edges=len(cuts),boundary_contacts=contact,atomic_boundary_faces=len(boundary)+2*len(cuts),sectors=sectors,certificate='PASS: reflection tiling, connected interior, two interior A points, all B/C sectors absorbing corners' if not transparent else 'GEOMETRY ONLY: transparent vertices invalidate the original darkness certificate')

def inside(p,poly):
    x,y=p;yes=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: yes=not yes
    return yes

def save(path,data): Path(path).write_text(json.dumps(data,indent=2)+'\n')
def draw(data,path,strict=True):
    from PIL import Image,ImageDraw
    ts=data['triangles'];owners=owners_of([tuple(map(tuple,t)) for t in ts]);cuts={edge(*e) for e in data.get('slits',[])}
    pts=[p for t in ts for p in t];x0=min(p[0] for p in pts);y0=min(p[1] for p in pts);x1=max(p[0] for p in pts);y1=max(p[1] for p in pts)
    scale=95;pad=65;im=Image.new('RGB',((x1-x0)*scale+2*pad,(y1-y0)*scale+2*pad+40),'#fafafa');d=ImageDraw.Draw(im)
    def xy(p): return ((p[0]-x0)*scale+pad,(y1-p[1])*scale+pad)
    for t in ts:d.polygon(list(map(xy,t)),fill='#e4ecf5')
    for e,os in owners.items():d.line(list(map(xy,e)),fill='#122d49' if len(os)==1 or e in cuts else '#b6c6d8',width=4 if len(os)==1 or e in cuts else 1)
    for p in set(map(tuple,pts)):
        x,y=xy(p);d.text((x+4,y+3),str(p),fill='#617185')
    for name,p in zip(('S','T'),data['marked']):
        x,y=xy(p);d.ellipse((x-6,y-6,x+6,y+6),fill='#c0392b');d.text((x+9,y-18),name,fill='#a0251c')
    result=check(data,strict=strict);d.text((pad,im.height-35),f"{result['walls']} walls | {result['tiles']} triangles | {result['slit_edges']} slit edges",fill='#122d49');im.save(path)

if __name__=='__main__':
    import sys
    data=json.loads(Path(sys.argv[1]).read_text()); print(json.dumps(check(data),indent=2))
    if len(sys.argv)>2:draw(data,sys.argv[2])
