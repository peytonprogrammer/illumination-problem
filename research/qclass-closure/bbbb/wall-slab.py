"""Reclassify saved d15 residuals. No rooms or trajectories generated."""
from collections import defaultdict
from itertools import groupby, product
import json
from pathlib import Path
from runpy import run_path

ROOT = next(Path(__file__).resolve().parents[2].glob("illumination*/fable/directions*"))
ledger = run_path(str(ROOT / "d163-pattern-ledger" / "ledger.py"))


def intervals(cells, axis, index):
    values = sorted(c[1-axis] for c in cells if c[axis] == index)
    runs = []
    for _, parts in groupby(enumerate(values), lambda entry: entry[1] - entry[0]):
        row = [value for _, value in parts]
        runs.append((row[0], row[-1] + 1))
    return runs


def clears(cells, S, T, axis):
    if S[axis] == T[axis]:
        return False
    if S[axis] > T[axis]:
        S,T = T,S
    bands = [intervals(cells,axis,i) for i in range(S[axis]//2,(T[axis]+1)//2)]
    for seq in product(*bands):
        a,b=seq[0]
        c,d=seq[-1]
        if not (2*a<S[1-axis]<2*b and 2*c<T[1-axis]<2*d):
            continue
        runs=[x for x,_ in groupby(seq)]
        if len(runs)==1:
            return True
        if len(runs)==2 and (a==c or b==d):
            return True
        if len(runs)==3:
            l,h=runs[1]
            if (a==l and d==h and b<=h and c>=l) or (b==h and c==l and a>=l and d<=h):
                return True
    return False


def audit(r):
    recs=json.loads((ROOT/'d15-small-r'/f'cert_r{r}.json').read_text())
    by=defaultdict(list)
    for rec in recs:
        nx,ny,mask=(rec[k] for k in ('nx','ny','mask'))
        cells={(i,j) for j in range(ny) for i in range(nx) if mask>>(i+nx*j)&1}
        word=ledger['canon'](ledger['turns'](ledger['polygon_of_cells'](cells)))
        residual=[p for p in rec['uncovered'] if not any(clears(cells,*p,k) for k in (0,1))]
        by[word].append((nx,ny,mask,len(rec['uncovered']),residual))
    return by


if __name__=='__main__':
    for r in (3,4):
        for w, rows in sorted(audit(r).items()):
            print(w,len(rows),sum(t[3] for t in rows),sum(len(t[4]) for t in rows))
