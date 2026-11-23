"""Read rim tree lengths in already archived chart directions (no direction generation)."""
from pathlib import Path
from collections import deque,Counter
from contextlib import redirect_stdout
import io,runpy
with redirect_stdout(io.StringIO()):
    old=runpy.run_path(str(Path(__file__).with_name('convex-cylinder.py')))
cyl=old['cyl']


def trees(O,v,stretch=None):
    charts=old['charts'](O,v)
    if len(charts)!=2 or any(c[2] for c in charts):return None
    r,u=cyl.act(O.r,O.u,cyl.word(*v))
    ri,ui=cyl.inv(r),cyl.inv(u)
    # Fix the transformed square-centre half-turn at one regular LL.
    i=next(i for i,p in enumerate(O.ll) if cyl.incid(O.cells,p)==4)
    cell,(ex,ey)=O.sq[i]
    other=O.idx[cell,(-ex,-ey)]
    target=O.r[O.u[other]]
    opp=[None]*len(r)
    opp[i]=ri[ui[target]]
    todo=[i]
    while todo:
        s=todo.pop()
        for t,z in ((r[s],ri[opp[s]]),(u[s],ui[opp[s]])):
            if opp[t] is None:opp[t]=z;todo.append(t)
            else:assert opp[t]==z
    assert all(opp[opp[s]]==s and O.ll[r[u[opp[s]]]]==O.ll[s] for s in range(len(r)))
    bottom=next(row for row in cyl.cycles(r) if any(cyl.incid(O.cells,O.ll[s])==3 for s in row))
    C=len(bottom)
    interior=bottom[:]
    while not any(cyl.incid(O.cells,O.ll[u[s]])==3 for s in interior):
        interior=[u[s] for s in interior]
    result=[]
    for row,top in ((bottom,False),(interior,True)):
        index={s:i for i,s in enumerate(row)}
        # Across this edge is a square in the other cylinder. Rotate it back.
        pairing=[index[opp[(u if top else ui)[s]]] for s in row]
        assert all(pairing[j]==i for i,j in enumerate(pairing))
        vertices=[i for i,s in enumerate(row) if O.marked[u[s] if top else s]]
        edges=[]
        for i,j in zip(vertices,vertices[1:]+[vertices[0]+C]):
            # A convex fixed point may be halfway along a unit interval? all are lattice points.
            mate=(pairing[i]+1)%C
            assert all(pairing[t%C]==(mate-1-(t-i))%C for t in range(i,j))
            leaf=any(cyl.incid(O.cells,O.ll[u[row[t%C]] if top else row[t%C]])==1 for t in (i,j))
            edges.append((i,j,mate,leaf))
        if stretch is not None:
            k=stretch
            points=[O.ll[u[s] if top else s] for s in row]
            delta=[int({a[0],b[0]}=={3,4}) for a,b in zip(points,points[1:]+points[:1])]
            assert all(abs(a[0]-b[0])==1 for a,b in zip(points,points[1:]+points[:1]))
            def length(t):
                laps,rem=divmod(t,C)
                return t+4*k*(laps*sum(delta)+sum(delta[:rem]))
            edges=[(length(i),length(j),length(m),leaf) for i,j,m,leaf in edges]
            assert length(C)==C+16*k
        result.append(edges)
    return (C if stretch is None else C+16*stretch),result


def complete(C,edges):
    # Open interval of signed differences 2x-(i+mate) on each tree edge.
    # Test all integer values and all half-integer gap representatives.
    return all(any(0 < (t-2*(i-m))%(2*C) < 4*(j-i) for i,j,m,_ in edges)
               for t in range(1,2*C))


if __name__=='__main__':
    for name,report in old['data'].items():
        if report['group']!='BBBB' and name!='R22': continue
        vs={tuple(pair[k][0]) for pair in report['pairs'] for k in ('cc','lit') if pair.get(k)}
        if name=='R22':vs={(4,7),(7,4)}
        O=cyl.Origami(old['rooms'][name]);count=Counter();good=[]
        for v in sorted(vs):
            t=trees(O,v)
            if t is None:continue
            C,sides=t
            flags=tuple(complete(C,edges) for edges in sides)
            count[sum(flags)]+=1
            if all(flags):good.append((v,C,[max(j-i for i,j,_,leaf in edges if leaf) for edges in sides]))
        print(name,count,'first full',good[:1])

if __name__=='__main__':
    O=cyl.Origami(old['rooms']['U2'])
    C0,base=trees(O,(-1,1),0)
    C1,once=trees(O,(-1,1),1)
    for side,(left,right) in enumerate(zip(base,once)):
        print('U2 rim',side,'(intercept, coefficient of k) for i,j,m')
        for e,g in zip(left,right):
            print([ (a,b-a) for a,b in zip(e[:3],g[:3]) ])
    # One prescribed replay of the insertion, independently reconstructing its rim pairings.
    stretched={(x+(4 if x>=4 else 0),y) for x,y in O.cells}|{(x,y) for x in range(4,8) for y in range(2)}
    C,sides=trees(cyl.Origami(stretched),(-1,1))
    assert C==108 and all(complete(C,t) for t in sides)
    print('area-54 literal insertion',C,[complete(C,t) for t in sides])
