"""Exact chart tests in each pair's two archived D72 directions only."""
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from itertools import product
import json
import sys
import io
import runpy
from contextlib import redirect_stdout

base=next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*'))
sys.path.insert(0,str(base/'d72-cylinder-test'))
import cyl


def charts(O,direction):
    r,u=cyl.act(O.r,O.u,cyl.word(*direction))
    rows=cyl.cycles(r)
    order={s:j for j,row in enumerate(rows) for s in row}
    reflex={i for i,p in enumerate(O.ll) if cyl.incid(O.cells,p)==3}
    cut={j for j,row in enumerate(rows) if reflex.intersection(row)}
    covered=set()
    result=[]
    for j in cut:
        levels=[rows[j]]
        while True:
            row=levels[-1]
            assert order[row[0]] not in covered
            covered.add(order[row[0]])
            top=[u[s] for s in row]
            levels.append(top)
            # A singular rim can contain segments from several upper rows.
            if reflex.intersection(top):
                break
            assert all(r[a]==b for a,b in zip(top,top[1:]+top[:1]))
        points=defaultdict(list)
        obstacles=[]
        for h,row in enumerate(levels):
            for x,s in enumerate(row):
                p=O.ll[s]
                points[p].append((x,h))
                if 0<h<len(levels)-1 and O.marked[s]:
                    assert cyl.incid(O.cells,p)==1
                    obstacles.append((x,h))
        C=len(levels[0]);height=len(levels)-1
        assert not obstacles or (len(obstacles)==2 and all(2*h==height for x,h in obstacles)
                                  and 2*abs(obstacles[0][0]-obstacles[1][0])==C)
        result.append((C,points,obstacles))
    assert len(covered)==len(rows)
    return result


def midpoint_witness(chart,S,T):
    C,points,obstacles=chart
    for (x,y),(X,Y) in product(points.get(S,()),points.get(T,())):
        h=Y-y
        if not h:
            continue
        for k in range(4):
            d=X-x+k*C
            assert not (d%2 or h%2)
            if d%4==h%4==0:
                continue
            if any(min(y,Y)<b<max(y,Y) and ((x-a)*h+(b-y)*d)%(C*abs(h))==0 for a,b in obstacles):
                continue
            return d,h
    return None


def on_saved_leaf(O,S,T,v):
    r,_=cyl.act(O.r,O.u,cyl.word(*v))
    for step in (r,cyl.inv(r)):
        for start,p in enumerate(O.ll):
            if p!=S: continue
            at=start
            for length in range(1,2*len(r)+1):
                at=step[at]
                if O.marked[at]: break
                if O.ll[at]==T and length%4==2: return (length*v[0],length*v[1])
                if at==start and length%4==0: break
    return False


def orig(vec,v):
    x,y=vec
    for g,k in reversed(cyl.word(*v)):
        if g=='T':
            x-=k*y
        else:
            y-=k*x
    return x,y


def old_test(O,S,T,pair):
    # Reuse the two archived-witness tests, without running their census.
    return bool((old['witness_midpoints'](O,S,T,pair['lit']) |
                 old['cylinder_midpoint'](O,S,T,pair['cc']))-{'a'})


source=Path(__file__).with_name('two-class.py')
with redirect_stdout(io.StringIO()):
    old=runpy.run_path(str(source))
sys.path.insert(0,str(base/'d8-perturbation-test'))
from tracer import trace

def verify_displacement(cells,S,T,vec):
    for ex,ey in product((-1,1),repeat=2):
        end,ok,hits=trace(cells,S,(ex*vec[0],ey*vec[1]))
        if ok and end==T:
            mid=hits[len(hits)//2-1]
            assert len(hits)%2==0 and any((a-b)%2 for a,b in zip(mid,S))
            return mid,(ex*vec[0],ey*vec[1])
    raise AssertionError((S,T,vec))


data=json.loads((base/'d72-cylinder-test/cyl_H40.json').read_text())
rooms=dict(cyl.rooms())
total=Counter()
for name,report in data.items():
    if report['group']!='BBBB': continue
    O=cyl.Origami(rooms[name])
    cached=lru_cache(None)(lambda v:charts(O,v))
    counts=Counter()
    single=set()
    examples=[]
    for pair in report['pairs']:
        S,T=tuple(pair['S']),tuple(pair['T'])
        prior=old_test(O,S,T,pair)
        found=None
        for label in ('cc','lit'):
            v=tuple(pair[label][0])
            if len(cached(v))==1: single.add(v)
            for chart in cached(v):
                vec=midpoint_witness(chart,S,T)
                if vec:
                    found=v,orig(vec,v),bool(chart[2])
                    break
            if found: break
        leaf=next((vec for label in ('lit','cc') if (vec:=on_saved_leaf(O,S,T,tuple(pair[label][0])))),None)
        counts[prior,bool(found),bool(leaf)]+=1
        if leaf and not prior:
            verify_displacement(O.cells,S,T,leaf)
        if found and not prior:
            examples.append((S,T,found,verify_displacement(O.cells,S,T,found[1])))
    total.update(counts)
    print(name,sorted(counts.items()),'first additional certificate',examples[:1],'single geometric cylinder',sorted(single)[:1])
print('total',sorted(total.items()))


def shape(chart):
    C,points,obstacles=chart
    return C,max(y for positions in points.values() for x,y in positions),obstacles


v=(-4,1)
original=set(rooms['DBas'])
one,=charts(cyl.Origami(original),v)
assert shape(one)[:2]==(96,2)
for point in ((1,0),(3,0),(1,4),(3,4)):
    assert all(y in (0,2) for x,y in one[1][point])
print('DBas',v,shape(one),'all four prescribed mouth endpoints on rims')
# Fixed arithmetic control of the symbolic two-bay construction.
example=original | {(x,y) for x in (1,2) for y in (-3,-2,-1,4,5)}
one,=charts(cyl.Origami(example),v)
assert len(example)==58 and shape(one)[:2]==(116,2)
assert sum(cyl.incid(example,p)==3 for p in set(cyl.Origami(example).ll))==8
print('depths 2 and 3, area 58, reflexes 8:',shape(one))
for v in ((4,7),(7,4)):
    control=[shape(c) for c in charts(cyl.Origami(rooms['R22']),v)]
    assert control==[(30,1,[]),(30,1,[])]
    print('R22',v,control)
