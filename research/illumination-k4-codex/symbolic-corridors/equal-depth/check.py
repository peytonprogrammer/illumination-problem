"""Exact affine coverage for fixed rational alpha; no trajectory sampling."""
from fractions import Fraction as F
from pathlib import Path
import json
import time

BASE = Path(__file__).parent
effort = BASE/'effort.json'
if not effort.exists():
    start = time.time()
    effort.write_text(json.dumps({'start':start,'deadline':start+840,
        'question':'Exact vertical-only affine coverage for alpha p/q, q=5,7',
        'limit_seconds':840},indent=2)+'\n')
deadline = json.loads(effort.read_text())['deadline']


def guard():
    if time.time() >= deadline:
        raise TimeoutError('aggregate 840-second effort deadline reached')


def val(line, x, y):
    a,b,c = line
    return a*x+b*y+c


def normalized(line):
    for c in line:
        if c:
            return tuple(x/c for x in line)
    raise ValueError('zero line')


def clauses(p,q):
    alpha = F(p,q)
    domain = [(F(0),F(0)),(F(1),F(0)),(F(1),F(1))]
    answer = []
    # For each upper chart shift: two compatible pairs of portal intervals.
    boxes = {0:[((1,2),(1,2),1),((2,3),(2,3),3)],
             2:[((1,2),(0,1),1),((2,3),(3,4),3)]}
    for shift, boxes_for_shift in boxes.items():
        for sign in (1,-1):
            for M in range(q):
                C = F(shift+4*M)
                e1 = (1-alpha,alpha*sign,alpha*C)
                e2 = (alpha,(1-alpha)*sign,(1-alpha)*C)
                ranges = []
                for e in (e1,e2):
                    values = [val(e,*P) for P in domain]
                    ranges.append(range((min(values)/4).__floor__()-1,
                                        (max(values)/4).__floor__()+2))
                for (i1,i2,middle_shift) in boxes_for_shift:
                    for j in ranges[0]:
                        for k in ranges[1]:
                            gs = [(e1[0],e1[1],e1[2]-i1[0]-4*j),
                                  (-e1[0],-e1[1],i1[1]+4*j-e1[2]),
                                  (e2[0],e2[1],e2[2]-i2[0]-4*k),
                                  (-e2[0],-e2[1],i2[1]+4*k-e2[2])]
                            # Reject only impossible necessary vertex maxima.
                            if any(max(val(g,*P) for P in domain) <= 0 for g in gs):
                                continue
                            answer.append({'shift':shift,'sign':sign,'M':M,
                                           'middle_shift':middle_shift,'guards':gs})
    return answer


def audit(p,q):
    candidates = clauses(p,q)
    lines = {normalized(g) for c in candidates for g in c['guards']}
    lines |= {(F(1),F(0),F(0)),(F(1),F(0),F(-1)),
              (F(0),F(1),F(0)),(F(1),F(-1),F(0))}
    lines = sorted(lines)
    xs = {F(0),F(1)}
    for i,(a,b,c) in enumerate(lines):
        guard()
        if b == 0 and a:
            x = -c/a
            if 0 <= x <= 1:
                xs.add(x)
        for A,B,C in lines[i+1:]:
            den = a*B-b*A
            if den:
                x = (b*C-c*B)/den
                if 0 <= x <= 1:
                    xs.add(x)
    boundaries = sorted(xs)
    test_xs = sorted(set(boundaries) | {(a+b)/2 for a,b in zip(boundaries,boundaries[1:])})
    count = 0
    uncovered = []
    selected = set()
    cell_masks = []
    for x in test_xs:
        guard()
        if x == 0:
            continue
        ys = {F(0),x}
        for a,b,c in lines:
            if b:
                y = -(a*x+c)/b
                if 0 <= y <= x:
                    ys.add(y)
        breaks = sorted(ys)
        test_ys = sorted(ys | {(a+b)/2 for a,b in zip(breaks,breaks[1:])})
        for y in test_ys:
            if y == 0:
                continue
            count += 1
            hits = {i for i,c in enumerate(candidates)
                    if all(val(g,x,y)>0 for g in c['guards'])}
            cell_masks.append(hits)
            hit = min(hits) if hits else None
            if hit is None:
                uncovered.append((str(x),str(y)))
            else:
                selected.add(hit)
    remaining = set(range(len(cell_masks)))
    cover = []
    while remaining and not uncovered:
        best = max(range(len(candidates)), key=lambda i:sum(i in cell_masks[j] for j in remaining))
        covered = {j for j in remaining if best in cell_masks[j]}
        assert covered
        cover.append(best)
        remaining -= covered
    return {'selected_cover':[candidates[i] for i in cover], 'p':p,'q':q,'status':'COVERED' if not uncovered else 'GAPS',
            'candidate_clauses':len(candidates),'distinct_lines':len(lines),
            'vertical_slabs_and_sections':len(test_xs)-1,'tested_sign_cells':count,
            'used_clauses':len(selected),'uncovered_sign_cells':len(uncovered),
            'first_uncovered':uncovered[:12],
            'note':'Sign-invariant affine decomposition includes all boundary sections; not room counts.'}


if __name__ == '__main__':
    results = []
    for p,q in ((1,5),(2,5),(1,7),(2,7),(3,7)):
        results.append(audit(p,q))
        out = {'status':'completed prefix','effort':json.loads(effort.read_text()),
               'results':results,'independent_review':False}
        (BASE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
        print(json.dumps(results[-1],default=str),flush=True)
