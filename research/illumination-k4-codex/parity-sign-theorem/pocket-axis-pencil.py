"""Prescribed pencil-action algebra; no geometry, directions or paths searched."""
from fractions import Fraction as F
from pathlib import Path
import json
B=Path(__file__).resolve().parent

def mv(m,v):return [sum(a*b for a,b in zip(row,v)) for row in m]
def add(v,w,k=1):return [a+k*b for a,b in zip(v,w)]
def det(m):
    a=[[F(x) for x in row] for row in m];d=F(1)
    for i in range(len(a)):
        j=next(j for j in range(i,len(a)) if a[j][i])
        if i!=j:a[i],a[j]=a[j],a[i];d=-d
        p=a[i][i];d*=p
        for j in range(i+1,len(a)):
            q=a[j][i]/p
            a[j]=[x-q*y for x,y in zip(a[j],a[i])]
    return d

rows=[]
for r in [F(0),F(1,100),F(-1,100),F(1,7)]:
    for a in [F(2),F(48)]:
        for b in [F(2),F(6)]:
            h=[[1,0,0,0],[a,1,0,0],[0,0,1,0],[r*a,0,0,1]]
            v=[[1,b,0,0],[0,1,0,0],[0,r*b,1,0],[0,0,0,1]]
            xr,yr=[1,0,r,0],[0,1,0,r]
            assert mv(h,xr)==add(xr,yr,a) and mv(h,yr)==yr
            assert mv(v,yr)==add(yr,xr,b) and mv(v,xr)==xr
            for z in ([0,0,1,0],[0,0,0,1]):assert mv(h,z)==z and mv(v,z)==z
            assert det(h)==det(v)==1
            rows.append({'r':str(r),'a':str(a),'b':str(b)})
minors=[]
for p,q in [(0,0),(-2,-4),(2,6),(-8,12)]:
    m=[[-2,0,0,0],[0,-2,0,0],[p,q,0,2],[-q,p,-2,0]]
    d=det(m);assert d==16
    minors.append({'p':p,'q':q,'determinant':str(d)})
out={'status':'EXACT_AXIS_PENCIL_ACTION_PASS','matrix_settings':len(rows),
     'period_evaluation_minors':minors,'settings':rows,
     'scope':'Only prescribed4dimensional cohomology-action identities and minor controls. No geometry, rays, events, directions, words, rooms, cylinder enumeration or origami orbits.',
     'universal_event_proved':False}
(B/'pocket-axis-pencil.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='settings'},indent=2))
