"""Check the two d147 pencil relations on named BBBB rooms. No orbit search."""
from contextlib import redirect_stdout
from functools import reduce
from io import StringIO
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import runpy

with redirect_stdout(StringIO()):
    reference = runpy.run_path(str(Path(__file__).with_name('cross-factor-arcs.py')))
rt = reference['rt']
pencil = reference['pencil_components']

def rect(a,b,c,d):
    return set(product(range(a,b),range(c,d)))

def stretch(cells,axis,at,extra):
    result = set()
    for p in cells:
        k = p[axis]
        shifts = range(extra+1) if k==at else [extra if k>at else 0]
        for shift in shifts:
            q = list(p)
            q[axis] += shift
            result.add(tuple(q))
    return result

columns = [range(6),(2,3),(2,3),range(6),range(6),(2,3),(2,),range(3)]
cov = {(x,y) for x,col in enumerate(columns) for y in col}
rooms = {
    'U2': rect(0,9,0,2) | rect(0,2,2,9) | rect(7,9,2,7) | rect(5,7,5,7),
    'c4181s': stretch(stretch(cov,0,1,2),1,4,3),
    'DBas': rect(0,5,0,4) | rect(5,9,1,2) | rect(9,13,-1,5),
    'DB55': rect(0,5,0,5) | rect(5,8,2,3) | rect(8,13,0,5),
}
for name,cells in rooms.items():
    totals = Counter()
    first = {}
    rows = {}
    base_rows = {}
    for origin in product(range(2),repeat=2):
        room,t = rt.room_tuple(cells,origin)
        assert all(len(rt.class_congruence(t,[k])) == 1 for k in range(4))
        pts = sorted(x for x in rt.lattice_points(cells) if rt.status(cells,x)=='interior'
                     and tuple(i%2 for i in x)==origin)
        marks = {x:[u[0] for u in rt.lifts(room,t,x,origin)] for x in pts}
        products = [rt.mul(t[i],t[j]) for i,j in combinations((1,2,3),2)]
        orbit = {0}
        while True:
            updated = orbit.union(*(set(h[i] for i in orbit) for h in products))
            if orbit == updated: break
            orbit = updated
        if origin == (0,0): print(name,"boundary product orbit",len(orbit),"/",len(cells))
        for d in (1,2,3):
            families = []
            for e in (d-1,d+1):
                if e not in (1,2,3): continue
                i,j=sorted([d,e])
                h=rt.mul(t[i],t[j])
                if name=="DB55" and origin==(0,0) and d==1:
                    print("DB55 pencil cycle lengths", [len(c) for c in rt.cycles(h)])
                families.append((pencil(t[0],t[d],h),pencil(t[0],t[d],h,True)))
            for s,u in combinations(pts,2):
                masks = [tuple(reduce(int.__or__,(f(i,j) for i,j in product(marks[s],marks[u])),0)
                               for f in pair) for pair in families]
                assert all((cut & ~full)==0 for full,cut in masks)
                key = 'legal' if any(b for a,b in masks) else 'lost' if any(a for a,b in masks) else 'absent'
                rows.setdefault((s,u),[]).append(key)
                base_rows.setdefault((s,u),[]).append(any(b & 1 for a,b in masks))
                totals[key]+=1
                first.setdefault(key,(origin,d,s,u,masks))
    base_misses = [p for p,v in base_rows.items() if not any(v) and all(c%2==0 for c in p[0])]
    print(name,'all-three zero-power misses, even/even',len(base_misses),base_misses[:1])
    print(name,'pairs by number of legal classes', dict(Counter(v.count('legal') for v in rows.values())))
    missing = [(p,v) for p,v in rows.items() if 'legal' not in v]
    print(name,'missed in all classes',len(missing), missing[:2])
    print(name,dict(totals),'first loss',first.get('lost'))

# Direct incidence-graph replay of the DB55 counterexample's five residue slices.
def components(edges):
    neighbors = {}
    for x,y in edges:
        neighbors.setdefault(x,set()).add(y)
        neighbors.setdefault(y,set()).add(x)
    def reachable(seeds):
        seen = set(seeds)
        todo = list(seen)
        while todo:
            for y in neighbors.get(todo.pop(), ()):
                if y not in seen:
                    seen.add(y)
                    todo.append(y)
        return seen
    return reachable

room,t = rt.room_tuple(rooms['DB55'],(0,0))
a,b,c,_ = t
h = rt.mul(b,c)
ca = {x:('a',tuple(v)) for v in rt.cycles(a) for x in v}
cb = {x:('b',tuple(v)) for v in rt.cycles(b) for x in v}
sources,targets = ({ca[v[0]] for v in rt.lifts(room,t,p)} for p in ((2,2),(10,2)))
power = list(range(len(a)))
relaxed,legal = [],[]
for j in range(5):
    edges = [(ca[i],cb[power[i]]) for i in range(len(a))]
    cut = [(u,v) for u,v in edges if len(u[1])==len(v[1])==2]
    relaxed.append(int(bool(components(edges)(sources) & targets)))
    legal.append(int(bool(components(cut)(sources) & targets)))
    power = [h[k] for k in power]
assert power == list(range(len(a))) and relaxed == [1,1,0,0,1] and legal == [0]*5
print('DB55 five slices, unrestricted and cut:',relaxed,legal)
