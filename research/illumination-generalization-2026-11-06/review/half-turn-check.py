"""Prescribed exact group/angle guards; no billiard or room discovery."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
IDENTITY = (1, 0, 0, 1)
REFLECTION = (1, 0, 0, -1)
HALF_TURN = (-1, 0, 0, -1)
QUARTER_TURN = (0, -1, 1, 0)


def multiply(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def power(a, n):
    result = IDENTITY
    for _ in range(n):
        result = multiply(result, a)
    return result


def closure(*generators):
    found = {IDENTITY}
    todo = [IDENTITY]
    while todo:
        a = todo.pop()
        for b in generators:
            c = multiply(b, a)
            if c not in found:
                found.add(c)
                todo.append(c)
    return found


def left_cosets(group, subgroup):
    return {frozenset(multiply(g, h) for h in subgroup) for g in group}


def main():
    group_guards = []
    for n, rotation, angles in ((2, HALF_TURN, (1, 3)),
                                (4, QUARTER_TURN, (1, 2, 3, 5, 6, 7))):
        group = closure(rotation, REFLECTION)
        assert len(group) == 2*n
        for m in angles:
            local = closure(REFLECTION, multiply(power(rotation, m), REFLECTION))
            cosets = left_cosets(group, local)
            expected = 1 if n == 2 or m % 2 else 2
            assert len(cosets) == expected
            for coset in cosets:
                assert {multiply(HALF_TURN, a) for a in coset} == set(coset)
                stabilizing_power = 1 if expected == 1 else 2
                assert {multiply(power(rotation, stabilizing_power), a)
                        for a in coset} == set(coset)
            group_guards.append({'N': n, 'angle_numerator': m,
                                 'local_group_order': len(local),
                                 'corner_lifts': len(cosets),
                                 'all_lifts_fixed_by_half_turn': True})
        for local in ({IDENTITY}, closure(REFLECTION)):
            for coset in left_cosets(group, local):
                assert {multiply(HALF_TURN, a) for a in coset} != set(coset)

    # Necessary turn summaries; do not assert geometric realizability.
    states = {(0, 0)}  # (sum of pi/4 angle numerators, even numerator count)
    summaries = []
    for walls in range(1, 22):
        states = {(total + m, even + (m % 2 == 0))
                  for total, even in states for m in (1, 2, 3, 5, 6, 7)}
        if walls < 3:
            continue
        for total, even in sorted(states):
            if total != 4*walls-8:
                continue
            odd = walls-even
            if odd == 0:
                assert walls % 2 == 0
                genus = (walls-2)//2
                sigma = walls
                quotient_genus = 0
                n = 2
            else:
                assert odd >= 2 and odd % 2 == 0
                assert (3*walls-even-6) % 2 == 0
                genus = (3*walls-even-6)//2
                sigma = walls+even
                quotient_genus = (odd-2)//2
                n = 4
            assert genus >= 1 and quotient_genus >= 0
            assert 2*genus-2 == 2*(2*quotient_genus-2)+sigma
            summaries.append({'W': walls, 'N': n, 'odd_corners': odd,
                              'genus': genus, 'Sigma': sigma,
                              'quotient_genus': quotient_genus})
    source_names = ('half-turn-quotient.md', 'genus-and-degree.md')
    result = {
        'status': 'EXACT_GROUP_AND_RIEMANN_HURWITZ_GUARDS_PASS',
        'angle_cases': len(group_guards),
        'angle_guards': group_guards,
        'necessary_inventory_summaries': len(summaries),
        'inventory_summaries': summaries,
        'source_sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                          for name in source_names},
        'whole_goal_complete': False,
        'limits': 'Finite algebra guards only; no proof of angle inventory '
                  'realizability, global illumination, or off-orbit degree bound.'
    }
    (HERE/'half-turn-check.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in
                      ('status', 'angle_cases', 'necessary_inventory_summaries',
                       'whole_goal_complete')}))


if __name__ == '__main__':
    main()
