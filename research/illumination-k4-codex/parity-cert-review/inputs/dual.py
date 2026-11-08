"""Independent replay of supplied corner events using exact infinitesimals.
No peer code imports and no additional optical directions. Fraction arithmetic
reconstructs wall words, symbolic endpoint maps, derivative cones and ranks.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
from functools import total_ordering
import json,hashlib,math
B=Path(__file__).resolve().parent;IN=B/'inputs';DIM=28
@total_ordering
class D:
 def __init__(self,a=0,b=0):self.a=F(a);self.b=F(b)
 def __add__(self,o):o=dual(o);return D(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return D(-self.a,-self.b)
 def __sub__(self,o):return self+-dual(o)
 def __rsub__(self,o):return dual(o)+-self
 def __mul__(self,o):o=dual(o);return D(self.a*o.a,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def __truediv__(self,o):o=dual(o);assert o.a;return D(self.a/o.a,(self.b*o.a-self.a*o.b)/(o.a*o.a))
 def __eq__(self,o):o=dual(o);return (self.a,self.b)==(o.a,o.b)
 def __lt__(self,o):o=dual(o);return (self.a,self.b)<(o.a,o.b)
def dual(x):return x if isinstance(x,D) else D(x)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def vecadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vecsub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def unit(i):return tuple(F(j==i) for j in range(DIM))
def evaluate(a):return dot(a,theta)
def ptval(p):return tuple(evaluate(a) for a in p)
def ptgrad(p):return tuple(tuple(a) for a in p)
def canonical_row(r):
 if not any(r):return tuple(r)
 # Positive normalization preserves the one-sided inequality.
 den=math.lcm(*(x.denominator for x in r));ints=[int(x*den) for x in r];g=math.gcd(*ints)
 return tuple(x//g for x in ints)
def rank(rows):
 pivots={}
 for row in rows:
  r=list(map(F,row))
  for i,p in sorted(pivots.items()):
   if r[i]:r=[x-r[i]*y for x,y in zip(r,p)]
  if any(r):
   i=next(i for i,x in enumerate(r) if x);v=r[i];pivots[i]=[x/v for x in r]
 return len(pivots)
