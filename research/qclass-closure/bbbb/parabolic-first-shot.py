"""Two fixed pairs, two prescribed slices each. No direction enumeration."""
from math import lcm
from pathlib import Path
import sys

archive = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09'
sys.path.insert(0, str(archive/'d72-cylinder-test'))
import cyl

cross = {(x,y) for x in range(-7,7) for y in range(-7,7) if -2<=x<2 or -2<=y<2}
controls = [
    ('DB55',cyl.decomp.handbuilt()['DB55'],(2,2),(10,2),(3,2),10,(130,10,110)),
    ('cross7',cross,(6,0),(-6,0),(1,1),4,(56,56,572)),
]
def order(p):
    return lcm(*(len(c) for c in cyl.cycles(p)))

def direct(cells,s,t,p,q):
    if p==0:
        # Vertical reflection at a horizontal wall preserves the abscissa.
        assert s[0]!=t[0]
        return False
    for ex,ey in cyl.SHEETS:
        state=(s,(ex*p,ey*q))
        seen=set()
        while state and state not in seen:
            seen.add(state)
            state=cyl.vertex_step(cells,*state)
            if state and state[0]==t:
                return True
    return False

for name,cells,s,t,axis,delta,expected in controls:
    O=cyl.Origami(cells)
    basis=cyl.word(*axis)
    r,u=cyl.act(O.r,O.u,basis)
    periods=order(O.r),order(O.u),order(r)
    assert periods==expected
    for m in (0,delta):
        p,q=m,1
        for g,k in reversed(basis):
            if g=='T': p-=k*q
            else: q-=k*p
        result=direct(cells,s,t,p,q)
        assert result==(m!=0)
        print(name,periods,'m',m,'direction',(p,q),'lit',result)
