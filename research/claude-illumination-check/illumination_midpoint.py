"""Exact affine half-turn tests on the existing square-tiled room unfolding.

A square map f acts in local coordinates as (x,y) -> (1-x,1-y).
All integer-offset affine maps with derivative -I are enumerated on each
connected component. DARK requires coverage of every source/target lift pair;
failure of this sufficient certificate says nothing about illumination.
"""
from collections import deque
from illumination_cover import build, inverse


def vertex_data(cover):
    n = len(cover['H'])
    parent = list(range(4*n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def join(a, b):
        parent[find(a)] = find(b)

    for i in range(n):
        for q, r, j in [(1, 0, cover['H'][i]), (2, 3, cover['H'][i]),
                        (3, 0, cover['V'][i]), (2, 1, cover['V'][i])]:
            join(4*i+q, 4*j+r)
    roots = sorted({find(i) for i in range(4*n)})
    number = {r: i for i, r in enumerate(roots)}
    ids = tuple(tuple(number[find(4*i+q)] for q in range(4)) for i in range(n))
    members = [[] for _ in roots]
    for i in range(n):
        for q in range(4):
            members[ids[i][q]].append((i, q))
    colors = []
    for group in members:
        labels = {cover['corners'][i][q] for i, q in group}
        assert len(labels) == 1
        colors.append(labels.pop())
    return dict(ids=ids, members=members, colors=tuple(colors))


def components(H, V):
    unseen = set(range(len(H)))
    result = []
    while unseen:
        first = min(unseen)
        group = {first}
        todo = [first]
        for i in todo:
            for j in (H[i], V[i]):
                if j not in group:
                    group.add(j)
                    todo.append(j)
        unseen -= group
        result.append(tuple(sorted(group)))
    return result


def half_turns(H, V, group):
    """A root image determines f by fH=H^-1 f and fV=V^-1 f."""
    invH, invV = inverse(H), inverse(V)
    root = group[0]
    result = []
    for image in group:
        f = {root: image}
        todo = deque([root])
        valid = True
        while todo and valid:
            i = todo.popleft()
            for P, invP in [(H, invH), (V, invV)]:
                j, value = P[i], invP[f[i]]
                if j in f:
                    if f[j] != value:
                        valid = False
                        break
                else:
                    f[j] = value
                    todo.append(j)
        if not valid or len(set(f.values())) != len(group):
            continue
        assert set(f) == set(group)
        if any(f[f[i]] != i for i in group):
            continue
        result.append(f)
    return result


def translations(H, V, group):
    """All grid-preserving derivative-I automorphisms on a component."""
    root = group[0]
    result = []
    for image in group:
        f = {root: image}
        todo = deque([root])
        valid = True
        while todo and valid:
            i = todo.popleft()
            for P in (H, V):
                j, value = P[i], P[f[i]]
                if j in f:
                    if f[j] != value:
                        valid = False
                        break
                else:
                    f[j] = value
                    todo.append(j)
        if valid and len(set(f.values())) == len(group):
            result.append(f)
    return result


def inspect_turn(cover, vertices, group, f):
    ids = vertices['ids']
    action = {}
    for i in group:
        for q in range(4):
            a, b = ids[i][q], ids[f[i]][(q+2) % 4]
            if a in action:
                assert action[a] == b
            action[a] = b
    centers = [i for i in group if f[i] == i]
    edges = [(i, side) for i in group for side, P in
             [('right', cover['H']), ('top', cover['V'])] if f[i] == P[i]]
    fixed = sorted(v for v in action if action[v] == v)
    regular = [v for v in fixed if vertices['colors'][v] != 3]
    admissible = not centers and not edges and not regular
    pairs = sorted((v, action[v]) for v in action if
                   vertices['colors'][v] == 1 and
                   vertices['colors'][action[v]] == 2)
    return dict(square_map=[f[i] for i in group], fixed_square_centers=centers,
                fixed_edge_midpoints=edges, fixed_vertices=fixed,
                fixed_unblocked_vertices=regular, admissible=admissible,
                source_target_pairs=pairs)


def analyze_cover(cover):
    H, V = cover['H'], cover['V']
    vertices = vertex_data(cover)
    colors = vertices['colors']
    groups = components(H, V)
    required, covered, records = set(), set(), []
    for group in groups:
        vs = {vertices['ids'][i][q] for i in group for q in range(4)}
        sources = sorted(v for v in vs if colors[v] == 1)
        targets = sorted(v for v in vs if colors[v] == 2)
        required.update((s, t) for s in sources for t in targets)
        turns = []
        for f in half_turns(H, V, group):
            record = inspect_turn(cover, vertices, group, f)
            turns.append(record)
            if record['admissible']:
                covered.update(map(tuple, record['source_target_pairs']))
        records.append(dict(squares=list(group), source_vertices=sources,
                            target_vertices=targets, involutions=turns))
        records[-1]['translation_automorphisms'] = len(translations(H, V, group))
    missing = required - covered
    return dict(status='DARK' if not missing else 'INCONCLUSIVE',
                certificate='all connecting segments have an absorbing fixed midpoint',
                cover_squares=len(H), surface_vertices=len(colors),
                source_lifts=colors.count(1), target_lifts=colors.count(2),
                required_lift_pairs=len(required), covered_lift_pairs=len(covered),
                missing_lift_pairs=[list(p) for p in sorted(missing)],
                components=records)


def analyze(data):
    return analyze_cover(build(data))


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    ap = argparse.ArgumentParser()
    ap.add_argument('room')
    ap.add_argument('--out')
    args = ap.parse_args()
    result = analyze(json.loads(Path(args.room).read_text()))
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2)+'\n')
    summary = {k: v for k, v in result.items() if k != 'components'}
    summary.pop('missing_lift_pairs')
    summary['involutions'] = sum(len(c['involutions']) for c in result['components'])
    summary['admissible_involutions'] = sum(t['admissible'] for c in result['components']
                                         for t in c['involutions'])
    print(json.dumps(summary))
