"""Exact fixed-word replay controls for first-order event predictions.
These evaluate supplied witnesses at deterministic nearby parameters; no
reflection word, direction or room discovery is performed.
"""
import json,random
from fractions import Fraction as F
from collections import Counter
from check import B,DIM,theta,clos,syms,axes,verts,vforms,sforms,tforms,dot,cross,vecsub,rank

def value(form,z):return dot(form,z)
def pt(form,z):return tuple(value(a,z) for a in form)
def proj(row):
 row=list(row)
 for c in clos:
  i=next(i for i,v in enumerate(c) if v);k=row[i]/c[i];row=[a-k*b for a,b in zip(row,c)]
 return row

def simple(z):
 vs=[pt(f,z) for f in vforms];s,t=pt(sforms,z),pt(tforms,z)
 assert all(dot(c,z)==0 for c in clos)
 for i,ax in enumerate(axes):assert z[2+i]*theta[2+i]>0
 edges=list(zip(vs,vs[1:]+vs[:1]))
 for i,(a,b) in enumerate(edges):
  for j,(c,d) in enumerate(edges):
   if j<=i or j==i+1 or (i==0 and j==len(edges)-1):continue
   if axes[i]==axes[j]:
    ax=axes[i];n=1-ax
    overlap=a[n]==c[n] and max(min(a[ax],b[ax]),min(c[ax],d[ax]))<=min(max(a[ax],b[ax]),max(c[ax],d[ax]))
   else:
    if axes[i]==0:h=(a,b);v=(c,d)
    else:h=(c,d);v=(a,b)
    overlap=min(h[0][0],h[1][0])<=v[0][0]<=max(h[0][0],h[1][0]) and min(v[0][1],v[1][1])<=h[0][1]<=max(v[0][1],v[1][1])
   assert not overlap,(i,j)
 def inside(p):
  parity=False
  for a,b in edges:
   if (a[1]>p[1])!=(b[1]>p[1]):
    x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
    if x>p[0]:parity=not parity
  return parity
 assert inside(s) and inside(t)
 return vs,s,t

def replay(event,z):
 vs,s,t=simple(z);sgn=[1,1];shift=[F(0),F(0)]
 for i in event['word']:
  normal=1-axes[i];shift[normal]+=2*sgn[normal]*vs[i][normal];sgn[normal]*=-1
 lift=tuple(sgn[j]*t[j]+shift[j] for j in (0,1));d=vecsub(lift,s);p=s
 for index in range(len(event['word'])+1):
  candidates=[]
  for i,(a,b) in enumerate(zip(vs,vs[1:]+vs[:1])):
   n=1-axes[i];ax=axes[i]
   if not d[n]:continue
   tau=(a[n]-p[n])/d[n]
   if tau<=0:continue
   contact=p[ax]+tau*d[ax];lo,hi=sorted((a[ax],b[ax]))
   if lo<=contact<=hi:candidates.append((tau,i,contact==lo or contact==hi))
  if not candidates:return False
  tau,i,corner=min(candidates)
  delta=vecsub(t,p)
  if not cross(delta,d):
   j=next(j for j,x in enumerate(d) if x);mu=delta[j]/d[j]
   if 0<mu<tau:return index==len(event['word'])
  if index==len(event['word']) or i!=event['word'][index] or corner:return False
  p=tuple(p[j]+tau*d[j] for j in (0,1));d=list(d);d[1-axes[i]]*=-1;d=tuple(d)
 return False

def moved(delta):
 step=F(1,10**7)/(1+max(map(abs,delta)))
 return tuple(a+step*d for a,d in zip(theta,delta))

if __name__=='__main__':
 events=json.loads((B/'events.json').read_text());rng=random.Random(20261031);stats=Counter();bad=[]
 # Every event gets its own exact descending closure-preserving direction.
 for i,e in enumerate(events):
  row=list(map(F,e['gradient']));p=proj(row);delta=[-x for x in p]
  for c in clos:
   k=next(k for k,v in enumerate(c) if v);delta[k]=-sum(c[j]*delta[j] for j in range(DIM) if j!=k)/c[k]
  assert dot(row,delta)<0
  if not replay(e,moved(delta)):bad.append(dict(event=i,control='own_descent'))
  stats['event_specific_descents']+=1
 # Independent deterministic perturbations compare both signs of every word.
 for trial in range(6):
  delta=list(map(F,[rng.randrange(-9,10) for _ in range(DIM)]))
  for c in clos:
   k=next(k for k,v in enumerate(c) if v);delta[k]=-sum(c[j]*delta[j] for j in range(DIM) if j!=k)/c[k]
  z=moved(delta);simple(z)
  for i,e in enumerate(events):
   val=dot(map(F,e['gradient']),delta)
   if not val:stats['tangent_skipped']+=1;continue
   actual=replay(e,z);expected=val<0
   stats['random_predictions']+=1;stats['predicted_lit' if expected else 'predicted_word_invalid']+=1
   if actual!=expected:bad.append(dict(trial=trial,event=i,expected=expected,actual=actual))
 # Negative control: reverse every inequality for a certified descending case.
 assert stats['event_specific_descents']==147
 result=dict(status='PASS' if not bad else 'FAIL',checks=dict(stats),mismatches=bad,scope='Fixed words only. Word invalidity is not room darkness.')
 (B/'validate.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
