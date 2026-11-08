"""Independent quadrant/seam verification of prescribed controls only."""
from pathlib import Path
from collections import defaultdict, Counter
from fractions import Fraction as F
from itertools import combinations
import hashlib, json
HERE=Path(__file__).resolve().parent
PEER=HERE.parent/'shared-seam-test'
BASE={(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)}

def census(cells):
    masks=defaultdict(set)
    for x,y in cells:
        for dx,dy in ((0,0),(1,0),(0,1),(1,1)):
            masks[(x+dx,y+dy)].add((1-2*dx,1-2*dy))
    kinds={}
    for v,mask in masks.items():
        n=len(mask)
        if n==2:
            assert sum(x for x,y in mask) or sum(y for x,y in mask),('pinch',v)
        kinds[v]={1:'convex',2:'smooth',3:'reflex',4:'interior'}[n]
    # Independent undirected boundary construction and single-cycle proof.
    boundary=set()
    for x,y in cells:
        for nb,p,q in [((x-1,y),(x,y),(x,y+1)),((x+1,y),(x+1,y),(x+1,y+1)),
                       ((x,y-1),(x,y),(x+1,y)),((x,y+1),(x,y+1),(x+1,y+1))]:
            if nb not in cells: boundary.add(tuple(sorted((p,q))))
    adj=defaultdict(set)
    for p,q in boundary: adj[p].add(q);adj[q].add(p)
    assert all(len(v)==2 for v in adj.values())
    reached=set(); todo=[min(adj)]
    while todo:
        v=todo.pop()
        if v in reached:continue
        reached.add(v);todo.extend(adj[v]-reached)
    assert reached==set(adj),'holes or disconnected boundary'
    r=sum(k=='reflex' for k in kinds.values()); c=sum(k=='convex' for k in kinds.values())
    assert c-r==4
    # Unit-cell interior graph must be connected as well.
    seen=set();todo=[min(cells)]
    while todo:
        x,y=todo.pop()
        if (x,y) in seen:continue
        seen.add((x,y));todo.extend(n for n in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if n in cells-seen)
    assert seen==cells
    return {'walls':c+r,'reflex':r,'convex':c,'area':len(cells),'kinds':kinds,'edges':boundary}

def image(p,t):
    sx,sy,tx,ty=t;return sx*p[0]+tx,sy*p[1]+ty

def inverse(p,t):
    sx,sy,tx,ty=t;return sx*(p[0]-tx),sy*(p[1]-ty)

def cells_image(cells,t):
    sx,sy,tx,ty=t
    return {(sx*x+tx-(sx<0),sy*y+ty-(sy<0)) for x,y in cells}

def segments(edges):
    lines=defaultdict(set)
    for p,q in edges:
        if p[0]==q[0]:lines[('v',p[0])].add(min(p[1],q[1]))
        else:lines[('h',p[1])].add(min(p[0],q[0]))
    out=[]
    for (axis,coord),starts in lines.items():
        starts=sorted(starts);lo=prev=starts[0]
        for z in starts[1:]+[None]:
            if z is not None and z==prev+1:prev=z;continue
            out.append(((coord,lo),(coord,prev+1)) if axis=='v' else ((lo,coord),(prev+1,coord)))
            lo=prev=z
    return out

base=census(BASE);assert (base['walls'],base['reflex'])==(10,3)
assert {v for v,k in base['kinds'].items() if k in ('smooth','interior')}=={(0,0),(2,-2)}
fixtures=[('known22',[(1,1,0,0),(1,-1,0,0),(-1,-1,4,0)],22,0,0),
          ('shared24',[(1,1,0,0),(1,-1,0,0),(-1,-1,-2,0)],24,1,0),
          ('fourfold28',[(1,1,0,0),(1,-1,0,0),(-1,-1,-2,0),(-1,1,-2,0)],28,0,1)]
results=[]
for name,ts,wantW,want3,want4 in fixtures:
    copies=[cells_image(BASE,t) for t in ts];m=len(copies)
    assert all(not(a&b) for a,b in combinations(copies,2))
    union=set().union(*copies);u=census(union);local=[census(c) for c in copies]
    junctions=defaultdict(list)
    for i,t in enumerate(ts):
        for p,k in base['kinds'].items():
            if k in ('convex','reflex'):junctions[image(p,t)].append((i,k))
    counts=Counter(); inherited=[]
    for p,inc in junctions.items():
        if any(k=='reflex' for i,k in inc):
            assert len(inc)==1 and u['kinds'][p]=='reflex';inherited.append(p)
        else:
            n=len(inc);counts[n]+=1
            assert u['kinds'][p]=={1:'convex',2:'smooth',3:'reflex',4:'interior'}[n]
    seam_count=0
    for i,j in combinations(range(m),2):
        common=set(local[i]['kinds'])&set(local[j]['kinds'])
        assert all(inverse(p,ts[i])==inverse(p,ts[j]) for p in common)
        shared=local[i]['edges']&local[j]['edges']
        seams=segments(shared) if shared else []
        seam_count+=len(seams)
        for p,q in seams:
            assert p in junctions and q in junctions
            for idx in (i,j):
                assert local[idx]['kinds'][p]==local[idx]['kinds'][q]=='convex'
                # This maximal contact is the whole maximal boundary wall.
                assert (p,q) in segments(local[idx]['edges'])
    t1,t2,t3,t4=[counts[i] for i in range(1,5)]
    assert (u['walls'],t3,t4)==(wantW,want3,want4)
    assert len(inherited)==m*base['reflex']
    assert u['reflex']==m*base['reflex']+t3
    assert u['walls']==m*(base['walls']-4)+4+2*t3
    assert t2+2*t3+2*t4==2*m-2
    assert 2*seam_count==t2+2*t3+4*t4
    assert seam_count==m-1+t4
    fibers={str(mark):{str(image(mark,t)):u['kinds'][image(mark,t)] for t in ts} for mark in ((0,0),(2,-2))}
    if name=='known22':assert u['kinds'][(0,0)]==u['kinds'][(2,2)]=='interior'
    if name=='shared24':assert all(k=='smooth' for k in fibers[str((2,-2))].values())
    results.append({'name':name,**{k:u[k] for k in ('walls','reflex','area')},'junction_counts':dict(counts),'seams':seam_count,'cycle_rank':seam_count-m+1,'fibers':fibers})
# Explicit nine small bases from the written area-bound proof. No generation.
small=[('strip'+str(n),{(i,0) for i in range(n)}) for n in range(1,5)]
small += [('L3',{(0,0),(1,0),(0,1)}),('square4',{(0,0),(1,0),(0,1),(1,1)}),
          ('T4',{(0,0),(1,0),(2,0),(1,1)}),('L4',{(0,0),(1,0),(2,0),(0,1)}),
          ('S4',{(0,0),(1,0),(1,1),(2,1)})]
small_results=[]
for name,cells in small:
    cc=census(cells);non={p for p,k in cc['kinds'].items() if k in ('smooth','interior')}
    residues={(x%2,y%2) for x,y in non}
    smooth=sum(k=='smooth' for k in cc['kinds'].values())
    assert smooth<2 or len(residues)>1
    small_results.append({'name':name,'area':len(cells),'smooth':smooth,'interior':sum(k=='interior' for k in cc['kinds'].values()),'residue_count':len(residues)})
for x in (F(0),F(1,2)):
    assert (x,0)!=(x-F(1,2),0)
# Match independently derived counts against both original and isolated replay.
for file in (PEER/'check.json',HERE/'peer-replay.json'):
    pp=json.loads(file.read_text());assert pp['status']=='PASS'
    for ours,theirs in zip(results,pp['fixtures']):
        assert all(ours[k]==theirs[k] for k in ('name','walls','reflex','area','cycle_rank'))
sources={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PEER/'findings.txt',PEER/'check.py',PEER/'check.json',HERE.parent/'research-note.tex')}
(HERE/'check.json').write_text(json.dumps({'status':'PASS','scope':'Independent code, three prescribed assemblies and nine supplied small bases only; general theorems need hand proof. No peer-code imports, discoveries, rays, archives or workers.','sources':sources,'fixtures':results,'small_bases':small_results},indent=2)+'\n')
print(json.dumps({'status':'PASS','fixtures':[(r['name'],r['walls'],r['reflex']) for r in results],'small_bases':len(small_results)}))
