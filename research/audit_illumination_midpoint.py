"""Independent half-turn completeness, fixed-point, and control audits."""
import itertools
import json
from pathlib import Path
from illumination_cover import build
from illumination_midpoint import (analyze, analyze_cover, components, half_turns,
                                   translations, vertex_data)
from illumination_sector_paths import trace, verify as verify_ray

BASE = Path(__file__).parent


def independent_vertices(c):
    """Edge equivalence graph; independent of the production union/find."""
    graph = {p: set() for p in itertools.product(range(len(c['H'])), range(4))}
    for i in range(len(c['H'])):
        for q, r, j in [(1, 0, c['H'][i]), (2, 3, c['H'][i]),
                        (3, 0, c['V'][i]), (2, 1, c['V'][i])]:
            graph[i, q].add((j, r))
            graph[j, r].add((i, q))
    groups = []
    remaining = set(graph)
    while remaining:
        root = min(remaining)
        todo = [root]
        group = {root}
        for p in todo:
            for q in graph[p]:
                if q not in group:
                    group.add(q)
                    todo.append(q)
        remaining -= group
        groups.append(frozenset(group))
    return {p: group for group in groups for p in group}


def verify_turn(c, component, values):
    group = component['squares']
    assert len(values) == len(group)
    f = dict(zip(group, values))
    assert set(values) == set(group)
    H, V = c['H'], c['V']
    for i in group:
        assert f[f[i]] == i
        # Equivalent gluing equations without computing inverse permutations.
        assert H[f[H[i]]] == f[i]
        assert V[f[V[i]]] == f[i]
        assert f[i] != i, 'fixed square center'
        assert f[i] != H[i], 'fixed vertical-edge midpoint'
        assert f[i] != V[i], 'fixed horizontal-edge midpoint'
    vertices = independent_vertices(c)
    action = {}
    for i in group:
        for q in range(4):
            a, b = vertices[i, q], vertices[f[i], (q+2) % 4]
            if a in action:
                assert action[a] == b
            action[a] = b
    pairs = set()
    for a, b in action.items():
        labels = {c['corners'][i][q] for i, q in a}
        target_labels = {c['corners'][i][q] for i, q in b}
        assert len(labels) == len(target_labels) == 1
        if a == b:
            assert labels == {3}, 'unblocked fixed vertex'
        if labels == {1} and target_labels == {2}:
            pairs.add((a, b))
    return pairs


def verify_dark(c, result):
    assert result['status'] == 'DARK'
    vertices = independent_vertices(c)
    expected_components = set()
    remaining = set(range(len(c['H'])))
    while remaining:
        group = {min(remaining)}
        todo = list(group)
        for i in todo:
            for j in (c['H'][i], c['V'][i]):
                if j not in group:
                    group.add(j)
                    todo.append(j)
        remaining -= group
        expected_components.add(frozenset(group))
    supplied = [frozenset(g['squares']) for g in result['components']]
    assert len(supplied) == len(set(supplied))
    assert set(supplied) == expected_components
    for v in set(vertices.values()):
        labels = {c['corners'][i][q] for i, q in v}
        assert len(labels) == 1
        if labels in ({1}, {2}):
            assert len(v) == 4, 'source/target must be regular'
    for component in result['components']:
        vs = {vertices[i, q] for i in component['squares'] for q in range(4)}
        sources = [v for v in vs if {c['corners'][i][q] for i, q in v} == {1}]
        targets = [v for v in vs if {c['corners'][i][q] for i, q in v} == {2}]
        covered = set()
        for record in component['involutions']:
            if record['admissible']:
                covered |= verify_turn(c, component, record['square_map'])
        assert set(itertools.product(sources, targets)) <= covered
    return True


def torus_fixture(block=True):
    """A 4x4 torus with four explicitly absorbing regular points.

    This is an abstract surface fixture, not a polygonal-room discovery.
    """
    index = lambda x, y: (y % 4)*4 + x % 4
    H = tuple(index(x+1, y) for y in range(4) for x in range(4))
    V = tuple(index(x, y+1) for y in range(4) for x in range(4))
    def label(x, y):
        p = (x % 4, y % 4)
        if p == (1, 0):
            return 1
        if p == (3, 0):
            return 2
        return 3 if block and p[0] % 2 == p[1] % 2 == 0 else 0
    corners = tuple(tuple(label(x+dx, y+dy) for dx, dy in
                          [(0, 0), (1, 0), (1, 1), (0, 1)])
                    for y in range(4) for x in range(4))
    return dict(H=H, V=V, corners=corners)


def small_complete_audit():
    systems = maps = 0
    for n in range(1, 5):
        perms = list(itertools.permutations(range(n)))
        for H, V in itertools.product(perms, repeat=2):
            systems += 1
            for group in components(H, V):
                brute_turns, brute_translations = set(), set()
                for values in itertools.permutations(group):
                    f = dict(zip(group, values))
                    if all(f[f[i]] == i and H[f[H[i]]] == f[i] and
                           V[f[V[i]]] == f[i] for i in group):
                        brute_turns.add(values)
                    if all(f[H[i]] == H[f[i]] and f[V[i]] == V[f[i]] for i in group):
                        brute_translations.add(values)
                actual = {tuple(f[i] for i in group) for f in half_turns(H, V, group)}
                actual_translations = {tuple(f[i] for i in group)
                                       for f in translations(H, V, group)}
                assert actual == brute_turns
                assert actual_translations == brute_translations
                maps += len(actual)
    return dict(permutation_systems=systems, half_turns_checked=maps)


def main():
    small = small_complete_audit()
    toy = torus_fixture()
    positive = analyze_cover(toy)
    assert positive['status'] == 'DARK' and positive['covered_lift_pairs'] == 1
    verify_dark(toy, positive)
    negative = analyze_cover(torus_fixture(False))
    assert negative['status'] == 'INCONCLUSIVE'
    rejected = 0
    for corruption in ('map', 'blockers', 'missing_component'):
        changed = json.loads(json.dumps(positive))
        cover = toy
        if corruption == 'map':
            good = next(t for t in changed['components'][0]['involutions']
                        if t['admissible'])
            good['square_map'][0] = good['square_map'][1]
        elif corruption == 'blockers':
            cover = torus_fixture(False)
        else:
            changed['components'] = []
        try:
            verify_dark(cover, changed)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(('accepted corruption', corruption))
    rooms = []
    names = ['illumination-20', 'illumination-22',
             'illumination-search-simple-unrestricted',
             'transparent-one-exhaust-survivor',
             'transparent-simple-screen-survivor',
             'cover-mixed-sector-1', 'cover-mixed-sector-2']
    witnesses = [(names[3], (-4, -11)), (names[4], (-2, -9)),
                 (names[5], (5, 3)), (names[6], (5, 3))]
    for name in names:
        data = json.loads((BASE/(name+'.json')).read_text())
        c = build(data)
        r = analyze(data)
        (BASE/f'midpoint-{name}.json').write_text(json.dumps(r, indent=2)+'\n')
        assert r['status'] == 'INCONCLUSIVE'
        assert r['required_lift_pairs'] == 64 and r['covered_lift_pairs'] == 0
        vertices = vertex_data(c)
        independent = independent_vertices(c)
        assert {frozenset(g) for g in vertices['members']} == set(independent.values())
        for comp in r['components']:
            for t in comp['involutions']:
                if t['admissible']:
                    verify_turn(c, comp, t['square_map'])
        rooms.append(dict(room=name, cover_squares=r['cover_squares'],
                          covered_pairs=r['covered_lift_pairs'],
                          required_pairs=r['required_lift_pairs'],
                          translations=[g['translation_automorphisms'] for g in r['components']],
                          involutions=sum(len(g['involutions']) for g in r['components'])))
    for name, direction in witnesses:
        data = json.loads((BASE/(name+'.json')).read_text())
        ray = trace(data, direction, 1000)
        assert ray['status'] == 'illuminated'
        verify_ray(data, ray)
    pilot = json.loads((BASE/'midpoint-inverse-pilot.json').read_text())
    pilot_maps = 0
    for room in pilot['rooms']:
        name = f"midpoint-holes-{room['nx']}x{room['ny']}-room.json"
        c = build(json.loads((BASE/name).read_text()))
        result = analyze_cover(c)
        assert result['status'] == 'INCONCLUSIVE'
        for comp in result['components']:
            for record in comp['involutions']:
                if record['admissible']:
                    verify_turn(c, comp, record['square_map'])
                    pilot_maps += 1
    partial = json.loads((BASE/'midpoint-holes-partial-room.json').read_text())
    witness = json.loads((BASE/'midpoint-holes-partial-witness.json').read_text())
    verify_ray(partial, witness['witness'])
    assert analyze(partial)['covered_lift_pairs'] == 8
    summary = dict(status='PASS', exhaustive_small_audit=small,
                   positive_abstract_torus_fixture=positive['status'],
                   unblocked_torus_fixture=negative['status'],
                   corrupted_certificates_rejected=rejected,
                   exact_physical_witnesses_verified=len(witnesses), rooms=rooms,
                   inverse_pilot_rooms=len(pilot['rooms']),
                   inverse_pilot_physical_pairs=sum(r['physical_point_pairs'] for r in pilot['rooms']),
                   inverse_pilot_admissible_maps_checked=pilot_maps,
                   partial_coverage_counterexample=dict(covered=8, required=32,
                       direction=witness['witness']['direction'], bounces=witness['witness']['bounces']),
                   scope='Midpoint certificate test only; abstract torus is not a room.')
    (BASE/'midpoint-final-audit.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
