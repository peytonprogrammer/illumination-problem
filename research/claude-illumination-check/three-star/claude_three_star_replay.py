"""Independent check of the three-star, three-exception cases. Uses only Claude's code.

For each Codex shape: rebuild the support from Claude's reduction budget and compare it
with Codex's allowed cells and triangle-index digest; verify every saved ray guard with
Claude's exact checker; then replay each nonadjacent mark pair in Claude's relaxed
CP-SAT model (three fixed full stars, exactly three exceptions, walls <= 23).
"""
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from ortools.sat.python import cp_model
from claude_ray_guard_check import cell_tiles, check_path
from claude_relaxed_replay import incident, around, vertex_table
from claude_three_star_reduction import budget, neighbors


def build(full, allowed, cuts, fixed=None, max_walls=23, exceptions_exact=3):
    ts = sorted({t for c in allowed for t in cell_tiles(*c)})
    index = {t: i for i, t in enumerate(ts)}
    m = cp_model.CpModel()
    x = [m.new_bool_var('') for _ in ts]
    zero = m.new_constant(0)
    var = lambda t: x[index[t]] if t in index else zero
    for c in full:
        for t in cell_tiles(*c):
            m.add(var(t) == 1)
    corners, excs, vused = [], [], []
    for v in sorted({p for t in ts for p in t}):
        ring = around(v, incident(v))
        c, e, u = m.new_bool_var(''), m.new_bool_var(''), m.new_bool_var('')
        m.add_allowed_assignments([var(t) for t in ring] + [c, e], vertex_table(v, ring))
        m.add_max_equality(u, [var(t) for t in ring])
        corners.append(c); excs.append(e); vused.append(u)
    edges = {}
    for t in ts:
        for a, b in combinations(t, 2):
            edges.setdefault((a, b), []).append(t)
    eused = []
    for owners in edges.values():
        u = m.new_bool_var(''); m.add_max_equality(u, [var(t) for t in owners]); eused.append(u)
    m.add(sum(corners) <= max_walls)
    m.add(sum(excs) == exceptions_exact)
    m.add(sum(vused) - sum(eused) + sum(x) == 1)
    for facts in cuts:
        m.add_bool_or([x[i].Not() if v else x[i] for i, v in facts])
    if fixed is not None:
        for t in ts:
            m.add(var(t) == int(t in fixed))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = float(__import__("os").environ.get("CLAUDE_CAP", 600)); s.parameters.num_search_workers = int(__import__("os").environ.get("CLAUDE_WORKERS", 8))
    st = s.solve(m)
    res = dict(status=s.status_name(st))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res['walls'] = sum(s.value(c) for c in corners)
        res['room'] = [[list(p) for p in t] for t in ts if s.value(x[index[t]])]
    return ts, res


def main():
    shapes = json.loads((HERE/'three-star-shapes.json').read_text())['shapes']
    out = dict(shapes=[], cases=[], guard_failures=[])
    norm = lambda tri: {tuple(sorted(tuple(v) for v in t)) for t in tri}
    for si, sh in enumerate(shapes):
        full = [tuple(c) for c in sh['full_A_cells']]
        R = set(full) | neighbors(full)
        r = budget(full)
        allowed = {(x, y) for x in range(-12, 13) for y in range(-12, 13)
                   if min(abs(x-u)+abs(y-v) for u, v in R) <= r}
        same = allowed == {tuple(c) for c in sh['allowed_A_cells']}
        _, geo = build(full, allowed, [])
        out['shapes'].append(dict(shape=si, full=full, budget=r, support_matches_codex=same,
                                  geometry_without_marks_or_cuts=geo['status']))
        print(json.dumps(out['shapes'][-1]), flush=True)
        pairs = [p for p in combinations(full, 2)]
        for pair in pairs:
            adj = abs(pair[0][0]-pair[1][0]) + abs(pair[0][1]-pair[1][1]) == 1
            case = dict(shape=si, marks_cells=pair, adjacent=adj)
            if adj:
                case['status'] = 'ILLUMINATED_DIRECT (shared interior C on the segment)'
                out['cases'].append(case); print(json.dumps(case)); continue
            marks = [(2*c[0], 2*c[1]) for c in pair]
            cuts = []
            for f in sorted(HERE.glob(f'three-star-case-{si}-*.json')):
                d = json.loads(f.read_text())
                if {tuple(c) for c in d['summary']['marked']} != set(pair):
                    continue
                ts = sorted({t for c in allowed for t in cell_tiles(*c)})
                digest = hashlib.sha256(json.dumps([[list(v) for v in t] for t in ts]).encode()).hexdigest()
                case['digest_matches_codex'] = digest == d['summary'].get('triangle_index_sha256')
                index = {t: i for i, t in enumerate(ts)}
                for ri, rec in enumerate(d['records']):
                    room = norm(rec['room']['triangles'])
                    ok, why, touched = check_path(room, rec['witness']['path'], marks)
                    facts = dict(map(tuple, rec['tile_facts']))
                    bad = not ok or any(t in index and facts.get(index[t]) != int(t in room) for t in touched) \
                        or any(t not in index and t in room for t in touched) \
                        or any(v != int(ts[i] in room) for i, v in facts.items())
                    if bad:
                        out['guard_failures'].append(dict(file=f.name, record=ri, why=why))
                    cuts.append(list(facts.items()))
                    # Positive control: the saved room is feasible without cuts and has the claimed walls.
                    if ri < 3:
                        _, pc = build(full, allowed, [], fixed=room)
                        case.setdefault('positive_controls', []).append((pc['status'], pc.get('walls'), rec['counts']['walls']))
            case['cuts'] = len(cuts)
            _, res = build(full, allowed, cuts)
            case['status'] = res['status']
            if 'room' in res:
                case['walls'] = res['walls']; case['room'] = res['room']
            out['cases'].append(case)
            print(json.dumps({k: v for k, v in case.items() if k != 'room'}), flush=True)
    out['status'] = 'PASS' if not out['guard_failures'] and all(
        c['status'] == 'INFEASIBLE' or c['adjacent'] for c in out['cases']) and all(
        s['support_matches_codex'] for s in out['shapes']) else 'CHECK'
    (HERE/'claude-three-star-replay.json').write_text(json.dumps(out, indent=1, default=list)+'\n')
    print(json.dumps(dict(status=out['status'], guard_failures=out['guard_failures'])))


if __name__ == '__main__':
    main()
