"""Exact square-tiled unfolding of canonical 45–45–90 mirror rooms.

Each square is paired from two oriented triangles. H/V permutations cross its
right/top edge. Vertex decorations retain physical corner blockers and marks.
No floating-point geometry is used.
"""
from fractions import Fraction as F
from math import gcd
from illumination_geometry import edge,owners_of,check,label

D4=tuple((a,b,c,d) for a,b,c,d in [(1,0,0,1),(0,-1,1,0),(-1,0,0,-1),(0,1,-1,0),(1,0,0,-1),(-1,0,0,1),(0,1,1,0),(0,-1,-1,0)])
def mat(g,p):return (g[0]*p[0]+g[1]*p[1],g[2]*p[0]+g[3]*p[1])
def mul(g,h):return (g[0]*h[0]+g[1]*h[2],g[0]*h[1]+g[1]*h[3],g[2]*h[0]+g[3]*h[2],g[2]*h[1]+g[3]*h[3])
def inverse(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def then(p,q):return tuple(q[i] for i in p)
def reflection(e):
    (x,y),(xx,yy)=e;u,v=xx-x,yy-y;n=u*u+v*v
    r=(F(2*u*u,n)-1,F(2*u*v,n),F(2*u*v,n),F(2*v*v,n)-1)
    assert all(x.denominator==1 for x in r)
    return tuple(map(int,r))

def sector_blockers(ts,owners,opens):
    """Absorption belongs to an occupied boundary sector, including contacts."""
    result={}
    for p in {p for t in ts for p in t}:
        incident={i for i,t in enumerate(ts) if p in t};graph={i:set() for i in incident}
        for e in opens:
            if p in e:
                a,b=owners[e];graph[a].add(b);graph[b].add(a)
        remaining=set(incident)
        while remaining:
            first=next(iter(remaining));component={first};todo=[first];remaining.remove(first)
            while todo:
                for j in graph[todo.pop()]:
                    if j in remaining:remaining.remove(j);component.add(j);todo.append(j)
            has_wall=any(p in e and any(i in component for i in os) and e not in opens for e,os in owners.items())
            angle=len(component)*(2 if label(p)=='C' else 1)
            absorbing=has_wall and angle!=4
            if not has_wall:assert angle==8
            for i in component:result[i,p]=absorbing
    return result

def build(data):
    geometry=check(data,strict=False);ts=[tuple(sorted(map(tuple,t))) for t in data['triangles']];owners=owners_of(ts);cuts={edge(*e) for e in data.get('slits',[])};opens={e for e,o in owners.items() if len(o)==2 and e not in cuts};blocked=sector_blockers(ts,owners,opens);s,t=map(tuple,data['marked']);states=[(k,i) for k in range(8) for i in range(len(ts))]
    def adjacent(state,e):
        g,i=state
        if e in opens:return (g,next(j for j in owners[e] if j!=i))
        return (D4.index(mul(D4[g],reflection(e))),i)
    local={}
    for state in states:
        g,i=state;pts={p:mat(D4[g],p) for p in ts[i]};origin=tuple(min(q[k] for q in pts.values()) for k in (0,1));local[state]={p:tuple(q[k]-origin[k] for k in (0,1)) for p,q in pts.items()}
    diagonal={}
    for state in states:
        _,i=state;e=next(e for e in owners_of([ts[i]]) if all(e[0][k]!=e[1][k] for k in (0,1)));diagonal[state]=adjacent(state,e)
    square_of={};squares=[]
    for state in states:
        if state in square_of:continue
        mate=diagonal[state];assert mate!=state and diagonal[mate]==state
        assert set(local[state].values())|set(local[mate].values())=={(0,0),(1,0),(1,1),(0,1)}
        k=len(squares);squares.append((state,mate));square_of[state]=square_of[mate]=k
    H=[];V=[];corners=[];physical=[]
    for k,pair in enumerate(squares):
        for side,values,perm in [(0,{(1,0),(1,1)},H),(1,{(0,1),(1,1)},V)]:
            st=next(st for st in pair if values<=set(local[st].values()));e=edge(*(p for p,q in local[st].items() if q in values));neighbor=adjacent(st,e);expected={(0,0),(0,1)} if side==0 else {(0,0),(1,0)};assert expected<=set(local[neighbor].values());perm.append(square_of[neighbor])
        labels=[];ps=[]
        for q in [(0,0),(1,0),(1,1),(0,1)]:
            originals={(p,blocked[st[1],p]) for st in pair for p,v in local[st].items() if v==q};assert len(originals)==1;original,absorbing=next(iter(originals));ps.append(original);labels.append(1 if original==s else 2 if original==t else 3 if absorbing else 0)
        corners.append(tuple(labels));physical.append(tuple(ps))
    n=len(squares);assert n==4*len(ts) and sorted(H)==sorted(V)==list(range(n));H,V=tuple(H),tuple(V)
    # Corner identifications induced by every glued square edge agree in labels
    # and in the physical point downstairs (including slit/contact corners).
    for i in range(n):
        for a,b,j in [(1,0,H[i]),(2,3,H[i]),(3,0,V[i]),(2,1,V[i])]:assert corners[i][a]==corners[j][b] and physical[i][a]==physical[j][b]
    # At every nonabsorbing vertex there is one full turn, not a branch point.
    comm=then(then(then(inverse(H),inverse(V)),H),V)
    colors=tuple(c[0] for c in corners)
    for i in range(n):
        if colors[i]!=3:assert comm[i]==i,('nonabsorbing branch point',i,physical[i][0])
    return dict(H=H,V=V,colors=colors,corners=tuple(corners),physical=tuple(physical),states=tuple(squares),triangles=ts,geometry=geometry)


def interior_code(H,V,x,y):
    """Direct integer crossing order for primitive positive (x,y)."""
    assert x>0 and y>0 and gcd(x,y)==1
    events=sorted([(a*y,0) for a in range(1,x)]+[(b*x,1) for b in range(1,y)])
    code=tuple(range(len(H)))
    for _,which in events:code=then(code,V if which else H)
    return code

def left_code(H,V,x,y):return then(then(interior_code(H,V,x,y),V),H)
def visibility(cover,code):
    """Every NE source sector, continuing only through regular vertices."""
    colors=cover['colors'];sources=[i for i,c in enumerate(colors) if c==1]
    for source in sources:
        seen={source};i=source;steps=0
        while True:
            i=code[i];steps+=1
            if colors[i]==2:return dict(source_square=source,steps=steps,endpoint_square=i)
            if colors[i]==3 or i in seen:break
            seen.add(i)
    return None

def physical_direction(cover,square,x,y):
    for g,i in cover['states'][square]:
        points={p:mat(D4[g],p) for p in cover['triangles'][i]};origin=tuple(min(v[k] for v in points.values()) for k in (0,1))
        for p,q in points.items():
            if q==origin and cover['physical'][square][0]==p:
                a,b,c,d=D4[g];return (a*x+c*y,b*x+d*y)
    raise AssertionError('source sector missing')

def solve(data,max_states=20000,seconds=60,progress=None,quotient=False):
    """Close the finite Stern–Brocot permutation-pair system, or return UNKNOWN.

Cut(a⊕b)=Cut(a) V H Cut(b); hence Left(a⊕b)=Left(a) Left(b).
Seeds Left(0)=H and Left(infinity)=H^-1 V H use formal axis cuts.
Every positive rational occurs in this tree. Pair equality, or simultaneous
color-preserving conjugacy when quotient=True, preserves every descendant
visibility test; only one representative is needed.
Actual horizontal/vertical rays are checked separately using H and V.
"""
    import time
    from collections import deque
    from illumination_sector_paths import trace,verify
    started=time.monotonic();cover=build(data);H,V=cover['H'],cover['V'];checked={};n=len(H)
    def positive(code,x,y):
        seen=visibility(cover,code)
        if seen:
            direction=physical_direction(cover,seen['source_square'],x,y);ray=trace(data,direction,max_events=100000)
            assert ray['status']=='illuminated',('cover/path disagreement',direction,seen,ray)
            verify(data,ray)
            return dict(status='ILLUMINATED',quotient=quotient,cover_squares=n,primitive_cover_direction=[x,y],cover_witness=seen,witness=ray,seconds=time.monotonic()-started)
    for code,d in [(H,(1,0)),(V,(0,1))]:
        result=positive(code,*d)
        if result:return result
    from illumination_code_quotient import canonical
    def state_key(a,b):return canonical(a,b,cover['colors']) if quotient else (a,b)
    hi=then(then(inverse(H),V),H);queue=deque([(H,hi,(1,0),(0,1))]);visited={state_key(H,hi)};processed=0;complete=False;merged=0
    while queue:
        if processed>=max_states or time.monotonic()-started>=seconds:break
        low,high,u,v=queue.popleft();code=then(low,high);direction=(u[0]+v[0],u[1]+v[1]);processed+=1
        if code not in checked:
            result=positive(code,*direction)
            if result:result.update(processed_pairs=processed,discovered_pairs=len(visited),distinct_codes=len(checked)+1,merged_pairs=merged);return result
            checked[code]=direction
        for a,b,p,q in [(low,code,u,direction),(code,high,direction,v)]:
            key=state_key(a,b)
            if key in visited:merged+=1;continue
            visited.add(key);queue.append((a,b,p,q))
        if progress and processed%1000==0:progress(dict(event='orbit',processed_pairs=processed,discovered_pairs=len(visited),codes=len(checked),seconds=time.monotonic()-started))
    complete=not queue
    return dict(status='DARK' if complete else 'UNKNOWN',reason='finite permutation-pair system closed' if complete else 'state_limit' if processed>=max_states else 'time_limit',all_directions_covered=complete,cover_squares=n,processed_pairs=processed,discovered_pairs=len(visited),queued_pairs=len(queue),distinct_codes=len(checked),merged_pairs=merged,quotient=quotient,seconds=time.monotonic()-started)

if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    ap=argparse.ArgumentParser();ap.add_argument('room');ap.add_argument('--max-states',type=int,default=20000);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--out');ap.add_argument('--quotient',action='store_true');args=ap.parse_args();data=json.loads(Path(args.room).read_text());result=solve(data,args.max_states,args.seconds,lambda r:print(json.dumps(r),flush=True),args.quotient);result['room']=args.room
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
