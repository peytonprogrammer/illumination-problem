"""Verify a supplied finite certificate; never discover or enqueue new orbit states.

Input JSON: {"states": [{"r": [...], "u": [...], "label": "..."}, ...]}.
A component certificate may instead be under components[*].states.
Only the ordinary absorbing-corner convention is accepted here.
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(state):
    if isinstance(state, dict):
        r, u, lab = state['r'], state['u'], state['label']
    else:
        r, u, lab = state
    n = len(r)
    assert n and len(u) == len(lab) == n
    assert sorted(r) == sorted(u) == list(range(n))
    assert set(lab) <= set('BST.')
    return tuple(r), tuple(u), ''.join(lab)


def canonical(state):
    """Independent rooted graph encodings, using all roots of a least-frequent color."""
    r, u, lab = normalize(state)
    n = len(r)
    color = min(Counter(lab), key=lambda c: (lab.count(c), c))
    encodings = []
    for root in range(n):
        if lab[root] != color:
            continue
        order = [root]
        position = {root: 0}
        for i in order:
            for j in (u[i], r[i]):
                if j not in position:
                    position[j] = len(order)
                    order.append(j)
        assert len(order) == n, 'disconnected component'
        encodings.append((tuple(position[r[i]] for i in order),
                          tuple(position[u[i]] for i in order),
                          ''.join(lab[i] for i in order)))
    return min(encodings)


def inverse(p):
    q = [None] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return q


def transforms(state):
    r, u, lab = state
    ri, ui = inverse(r), inverse(u)
    return [(r, tuple(u[ri[i]] for i in range(len(r))), lab),
            (r, tuple(u[r[i]] for i in range(len(r))), lab),
            (tuple(r[ui[i]] for i in range(len(r))), u, lab),
            (tuple(r[u[i]] for i in range(len(r))), u, lab)]


def check_horizontal(state):
    r, u, lab = state
    starts = 0
    for s, tag in enumerate(lab):
        if tag != 'S':
            continue
        starts += 1
        visited = {s}
        current = r[s]
        while current not in visited and lab[current] != 'B':
            assert lab[current] != 'T', 'certificate contains an illuminated state'
            visited.add(current)
            current = r[current]
    return starts


def verify(certificate):
    raw = json.loads(certificate.read_text())
    components = raw.get('components', [raw]) if isinstance(raw, dict) else [dict(states=raw)]
    spec = importlib.util.spec_from_file_location('codex_geometry_audit', HERE/'peer-fast-audit.py')
    geom = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geom)
    room_path = HERE/'peer-fast-inputs/cand-2_2-1.json'
    room = json.loads(room_path.read_text())
    initial = normalize(geom.direct_orthogonal_unfold(room))
    initial_key = canonical(initial)
    accepted = []
    for component in components:
        states = [normalize(s) for s in component['states']]
        if not states or len(states[0][0]) != len(initial[0]):
            continue
        keys = {canonical(s) for s in states}
        if initial_key not in keys:
            continue
        assert len(keys) == len(states), 'duplicate isomorphic states'
        checks = 0
        horizontal = 0
        for index, state in enumerate(states):
            horizontal += check_horizontal(state)
            for changed in transforms(state):
                assert canonical(changed) in keys, (index, 'not closed under shear')
                checks += 1
        accepted.append(dict(states=len(states), generator_closure_checks=checks,
                             horizontal_source_checks=horizontal))
    assert accepted, 'no certificate component includes independent physical unfolding'
    return dict(status='PASS', convention='stop at every actual polygon corner',
                input_sha256=hashlib.sha256(room_path.read_bytes()).hexdigest(),
                certificate=str(certificate), certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),
                independently_rebuilt_squares=len(initial[0]), certificates=accepted,
                scope='Finite set inclusion/closure verification only; no orbit generation or ray search.')


if __name__ == '__main__':
    result = verify(Path(sys.argv[1]))
    (HERE/'closed-orbit-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
