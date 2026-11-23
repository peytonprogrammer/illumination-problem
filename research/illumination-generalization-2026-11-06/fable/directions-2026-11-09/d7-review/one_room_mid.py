"""Midpoint-targeted search on one undecided room. Usage: file.json index dmax"""
import sys, json, time
from geom import Triangle, Tile, Room
from shoot import Tracer, find_path_mid
d=json.load(open(sys.argv[1])); u=d['undecided'][int(sys.argv[2])]
tri=Triangle(d['n'],d['b']); F=tri.F
room=Room(tri,[Tile(tri,s,k,tuple(t)) for s,k,t in u['tiles']]); assert room.analyze()
T=tuple(u['T']); tr=Tracer(room); t0=time.time()
for dd in range(0,int(sys.argv[3])+1):
    r=find_path_mid(tr,F.zero,T,room.transparentE,dd)
    print('mid-depth',dd,r['found'],r['tried'],round(time.time()-t0),'s',flush=True)
    if r['found']:
        print('walls hit',len(r['walls_hit']),'image',r['image'],'mid',r['mid']); break
