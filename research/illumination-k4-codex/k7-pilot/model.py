"""Small orthogonal/exact-k adapter around the frozen audited geometry model.
Intentionally limited to this I2 pilot: its census window matches the base
encoder's coarse window. I3 needs a separately checked window adaptation.
"""
from pathlib import Path
from collections import defaultdict
import json
import sys
import time
from threading import Timer

ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'inputs'))
import encode as base
from pysat.pb import PBEnc,EncType
from pysat.solvers import Solver

def build():
    record=json.loads((ROOT/'case.json').read_text()); case=record['support']
    assert case['I']==2 and record['marked']['case_id']=='I2_1_1_p00'
    started=time.monotonic()
    cnf,pool,x,ts=base.geometry(case,wmax=20,kmax=7)
    squares=defaultdict(list)
    for tri,var in x.items(): squares[(min(p[0] for p in tri),min(p[1] for p in tri))].append(var)
    assert all(len(v)==2 for v in squares.values())
    for a,b in squares.values(): cnf.extend([[-a,b],[a,-b]])
    exceptions=[v for v in range(1,pool.top+1) if isinstance(pool.obj(v),tuple) and pool.obj(v)[0]=='exception']
    assert exceptions
    exact=PBEnc.equals(lits=exceptions,weights=[1]*len(exceptions),bound=7,vpool=pool,encoding=EncType.adder).clauses
    return {'base_cnf':cnf,'exact':exact,'pool':pool,'triangles':x,'squares':squares,
            'exceptions':exceptions,'seconds':time.monotonic()-started,'record':record}

def bounded_solve(solver,seconds,assumptions=()):
    if seconds<=0: return None
    solver.clear_interrupt()
    timer=Timer(seconds,solver.interrupt);timer.daemon=True;timer.start()
    try: return solver.solve_limited(assumptions=list(assumptions),expect_interrupt=True)
    finally:
        timer.cancel();solver.clear_interrupt()
