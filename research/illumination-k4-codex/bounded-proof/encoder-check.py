"""Exhaustive small truth controls for cardinality and signed-literal PB encoders."""
from pathlib import Path
from itertools import product
import json
from pysat.card import CardEnc,EncType as CE
from pysat.pb import PBEnc,EncType as PE
from pysat.formula import IDPool
from pysat.solvers import Solver
HERE=Path(__file__).resolve().parent;tests=0
for bound in range(9):
 cnf=CardEnc.atmost(lits=list(range(1,9)),bound=bound,vpool=IDPool(start_from=9),encoding=CE.seqcounter)
 with Solver(name='glucose4',bootstrap_with=cnf) as s:
  for bits in product((0,1),repeat=8):
   got=s.solve(assumptions=[i if b else -i for i,b in enumerate(bits,1)])
   assert got==(sum(bits)<=bound);tests+=1
pbtests=0
lits=[1,2,-3,-4];weights=[4,4,1,2]
for bound in range(12):
 cnf=PBEnc.equals(lits=lits,weights=weights,bound=bound,vpool=IDPool(start_from=5),encoding=PE.adder)
 with Solver(name='glucose4',bootstrap_with=cnf) as s:
  for bits in product((0,1),repeat=4):
   total=sum(w*(bits[abs(l)-1] if l>0 else 1-bits[abs(l)-1]) for l,w in zip(lits,weights))
   got=s.solve(assumptions=[i if b else -i for i,b in enumerate(bits,1)])
   assert got==(total==bound);pbtests+=1
out=dict(status='PASS',cardinality_truth_checks=tests,signed_literal_weighted_equality_checks=pbtests)
(HERE/'encoder-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
