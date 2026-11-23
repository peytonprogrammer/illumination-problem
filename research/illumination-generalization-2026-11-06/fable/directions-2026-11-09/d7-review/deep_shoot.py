"""Re-enumerate rooms for (n,b,k) with W == Wtarget, keep those with no path of
depth <= dskip, then search deeper up to dmax. Prints room structure.
Usage: python3 deep_shoot.py n b k Wtarget dskip dmax [--save name]"""
import sys, time, json
from enum_rooms import enumerate_rooms
from shoot import Tracer
n,b,k,Wt,dskip,dmax=map(int,sys.argv[1:7])
rooms={}
def on_room(room,T,K):
    if room.W==Wt:
        rooms.setdefault(frozenset(t.key for t in room.tiles),(room,T,K))
enumerate_rooms(n,b,k,log=lambda *a:None,on_room=on_room)
print('rooms with W',Wt,':',len(rooms),flush=True)
out=[]
for room,T,K in rooms.values():
    F=room.tri.F; tr=Tracer(room)
    if any(tr.find_path(F.zero,T,d)['found'] for d in range(dskip+1)):
        continue
    z=F.cval(T)
    rec={'tiles':len(room.tiles),'corners':room.summary(),'T':list(T),'Tf':[round(z.real,4),round(z.imag,4)],
         'transparent':[(room.vlabel[p],room.vang[p]//room.tri.ang[room.vlabel[p]],'interior' if p not in room.bset else 'flat',[round(F.cval(p).real,4),round(F.cval(p).imag,4)]) for p in room.transparentE],
         'interiorA':len(room.interiorA),'tile_keys':[[t.s,t.k,list(t.t)] for t in room.tiles]}
    print(rec['tiles'],rec['corners'],'T',rec['Tf'],'interiorA',rec['interiorA'],'nTransparent',len(rec['transparent']),flush=True)
    t0=time.time(); rec['result']=None
    for d in range(dskip+1,dmax+1):
        res=tr.find_path(F.zero,T,d)
        pass
        if res['found']:
            rec['result']={'depth':d,'image':list(res['image']),'walls_hit':res['walls_hit'],
                           'walls':[[list(P),list(Q),j] for P,Q,j in tr.walls]}
            break
    print('   result', rec['result'] and rec['result']['depth'], round(time.time()-t0),'s',flush=True)
    if rec['result']: rec.pop('tile_keys')
    out.append(rec)
if '--save' in sys.argv:
    json.dump(out,open(sys.argv[sys.argv.index('--save')+1],'w'),indent=1)
