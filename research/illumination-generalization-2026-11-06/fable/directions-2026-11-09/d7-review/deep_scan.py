"""One enumeration pass for (n,b,k); for every valid room with W <= Wmax whose
stars share no C-tip (rooms that share one are lit by Proposition R2.1),
search exact paths with image depth 0..dmax. Writes a compact summary.
Usage: python3 deep_scan.py n b k Wmin Wmax dmax"""
import sys, time, json
from enum_rooms import enumerate_rooms
from shoot import Tracer, find_path_mid
n,b,k,Wmin,Wmax,dmax=map(int,sys.argv[1:7])
rooms={}
def on_room(room,T,K):
    if room.W>Wmax or room.W<Wmin: return
    F=room.tri.F
    cS=[t.V['C'] for t in room.tiles if t.V['A']==F.zero]
    if any(F.smul(2,c)==T for c in cS): return
    rooms.setdefault(frozenset(t.key for t in room.tiles),(room,T))
t0=time.time()
enumerate_rooms(n,b,k,log=lambda *a:None,on_room=on_room)
print('rooms',len(rooms),round(time.time()-t0),'s',flush=True)
summ={}; und=[]
for room,T in sorted(rooms.values(),key=lambda x:x[0].W):
    F=room.tri.F; tr=Tracer(room); dfound=None
    for d in range(dmax+1):
        if tr.find_path(F.zero,T,d)['found']: dfound=d; break
    if dfound is None:
        for d in range(1, 4):
            if find_path_mid(tr,F.zero,T,room.transparentE,d)['found']: dfound='mid%d'%d; break
    s=summ.setdefault(room.W,{}); s[str(dfound)]=s.get(str(dfound),0)+1
    print(room.W,dfound,round(time.time()-t0),flush=True)
    if dfound is None:
        und.append({'W':room.W,'T':list(T),'clean':room.clean,'tiles':[[t.s,t.k,list(t.t)] for t in room.tiles]})
print(json.dumps(summ),round(time.time()-t0),'s',flush=True)
json.dump({'n':n,'b':b,'k':k,'Wmax':Wmax,'dmax':dmax,'by_W_depth_found':summ,'undecided':und[:20],'n_undecided':len(und)},open(f'deep-scan-{n}-{b}-k{k}-W{Wmin}-{Wmax}.json','w'))
