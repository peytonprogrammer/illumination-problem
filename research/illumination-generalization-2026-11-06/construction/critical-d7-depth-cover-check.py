"""Exact interval cover, all strict common-depth indices; no sampled interpolation."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,signal
P=Path(__file__).resolve().parent;E=json.loads((P/'critical-d7-depth-cover-effort.json').read_text());end=datetime.fromisoformat(E['deadline']);left=(end-datetime.now(timezone.utc)).total_seconds();assert left>0;signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original deadline')));signal.setitimer(signal.ITIMER_REAL,left)
G=17;mouths={1:[(3,5),(12,14)],0:[(1,3),(7,9)]};charts=[];intervals=[]
def fold(y):
 z=y%(2*G);return (min(z,2*G-z),1 if z<G else -1)
try:
 for m in range(1,9):
  for sigma in (1,-1):
   for l in range(2*m):
    if datetime.now(timezone.utc)>=end:raise TimeoutError
    K=sigma*8-2+2*l*G
    if K<=0:K+=4*m*G
    L,U=Q(-1),Q(1);valid=True
    for j in range(1,2*m):
     y,sg=fold(2+Q(j*K,2*m));components=[];low=0
     for a,b in mouths[j%2]:components.append((low,a));low=b
     components.append((low,G));band=next(((a,b) for a,b in components if a<y<b),None)
     if band is None:valid=False;break
     slope=sg*(1-Q(j,m))
     if slope:
      a,b=sorted(((band[0]-y)/slope,(band[1]-y)/slope));L=max(L,a);U=min(U,b)
    if not valid or not L<0<U:continue
    idx=len(charts);charts.append({'m':m,'sigma':sigma,'K':K,'delta_interval':[str(L),str(U)]})
    # ANY integer n giving strict phase is legal; nearest-index selection is not required.
    for n in range(0,int((K+ m+2)/(2*m))+3):
     low=Q(m)*(2*n+L)/(Q(K,2)-L);high=Q(m)*(2*n+U)/(Q(K,2)-U);a=max(Q(0),low);b=min(Q(2),high)
     if a<b:intervals.append((a,b,a==0 and low<0,b==2 and high>2,idx,n))
 merged=[]
 for a,b,ac,bc,idx,n in sorted(intervals):
  if merged and (a<merged[-1][1] or (a==merged[-1][1] and (ac or merged[-1][3]))):
   if b>merged[-1][1]:merged[-1][1]=b;merged[-1][3]=bc
   elif b==merged[-1][1]:merged[-1][3]|=bc
  else:merged.append([a,b,ac,bc])
 gaps=[];cursor=Q(0);closed=False
 for a,b,ac,bc in merged:
  if a>cursor or (a==cursor and not (ac or closed)):gaps.append({'lo':str(cursor),'hi':str(a),'lo_included':not closed,'hi_included':not ac})
  cursor=b;closed=bc
 if cursor<Q(2) or not closed:gaps.append({'lo':str(cursor),'hi':'2','lo_included':not closed,'hi_included':True})
 out={'status':'EXACT_INTERVAL_COVER_COMPLETE' if not gaps else 'EXACT_CHART_MECHANISM_GAPS','charts':charts,'intervals':[{'lo':str(a),'hi':str(b),'lo_closed':ac,'hi_closed':bc,'chart':idx,'n':n} for a,b,ac,bc,idx,n in intervals],'merged':[[str(a),str(b),ac,bc] for a,b,ac,bc in merged],'gaps':gaps,'scope':'COMMON D/c in[0,2], allSTRICTindices notonlynearest; r>2known tail','original_deadline':E['deadline'],'discovery':True,'darkness_claimed':False,'whole_goal_complete':False}
finally:signal.setitimer(signal.ITIMER_REAL,0)
(P/'critical-d7-depth-cover-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['charts','intervals']}))
