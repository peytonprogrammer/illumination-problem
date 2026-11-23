"""Rebuild one undecided room from a deep-scan JSON and describe it.
Usage: python3 one_room.py file.json index [dmin dmax]"""
import sys, json, time
from geom import Triangle, Tile, Room
from shoot import Tracer
d=json.load(open(sys.argv[1])); u=d['undecided'][int(sys.argv[2])]
tri=Triangle(d['n'],d['b']); F=tri.F
tiles=[Tile(tri,s,k,tuple(t)) for s,k,t in u['tiles']]
room=Room(tri,tiles); assert room.analyze(), room.err
T=tuple(u['T'])
def f(p): z=F.cval(p); return (round(z.real,4),round(z.imag,4))
print('tiles',len(tiles),'W',room.W,room.summary(),'clean',room.clean,'T',f(T))
print('interior A',[f(p) for p in room.interiorA])
print('corners in order:')
print([ (room.vlabel[p], room.vang[p], f(p)) for p in room.corners])
print('transparent C:',[(room.vang[p]//tri.ang['C'],'int' if p not in room.bset else 'flat',f(p)) for p in room.transparentE])
if len(sys.argv)>4:
    tr=Tracer(room); t0=time.time()
    for dd in range(int(sys.argv[3]),int(sys.argv[4])+1):
        r=tr.find_path(F.zero,T,dd); print('depth',dd,r['found'],r.get('tried'),r.get('images'),round(time.time()-t0),'s',flush=True)
        if r['found']: print(r['walls_hit'], r['image']); break
