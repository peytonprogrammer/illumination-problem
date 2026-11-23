"""Task 4: horizontal-cylinder census on the SAVED 10368-state certificate of the 22-wall room.

Reads inputs/marked-origami-known22-closure.gz (copied unchanged from
.context/illumination-generalization-2026-11-06/review/; SHA-256 of the decompressed bytes is
checked against the value used by negative-control-audit.py). No orbit is regenerated.

State format (as in negative-control-audit.py): 3*60 bytes = h, v, labels. h[i] is the square to
the right of square i, v[i] the square above. labels[i] describes the lower-left vertex of square i:
1 = source lift, 2 = target lift, 3 = corner lift (all 27 zero squares and the 13 convex-corner
lifts), 0 = other regular vertex. Vertices are cycles of k = v h v^-1 h^-1 (k[i] = v[h[vi[hi[i]]]]);
a cycle of length 3 is a true zero (cone angle 6 pi).

Horizontal cylinders: union of h-cycles (strips of height 1); strip c and the strip above it are in
one cylinder iff the top line of c carries no true zero ('zeros only'), or no true zero and no
source/target lift ('S/T marked').

Run: python3 -B task4_cylinders.py   -> writes task4_cylinders.json
"""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHA = '2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
n = 60


def inv(p):
    q = [0] * n
    for i, j in enumerate(p):
        q[j] = i
    return q


def cyc(p):
    seen, out = set(), []
    for i in range(n):
        if i in seen:
            continue
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = p[j]
        out.append(c)
    return out


def cylinders(h, v, singular):
    """singular[i]: lower-left vertex of square i stops a cylinder. Returns list of cylinders,
    each a list of h-cycles from bottom to top, plus bottom/top boundary h-cycles."""
    hc = cyc(h)
    where = {x: k for k, c in enumerate(hc) for x in c}
    parent = list(range(len(hc)))

    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a

    above = {}
    for k, c in enumerate(hc):
        top = [v[i] for i in c]                       # squares whose lower-left vertex is on c's top line
        if not any(singular[j] for j in top):
            ks = {where[j] for j in top}
            assert len(ks) == 1 and len(hc[ks.pop()]) == len(c)
            k2 = where[top[0]]
            above[k] = k2
            parent[find(k2)] = find(k)
    groups = {}
    for k in range(len(hc)):
        groups.setdefault(find(k), []).append(k)
    out = []
    for ks in groups.values():
        # bottom strip: the one not above any other strip of the group
        tops = {above[k] for k in ks if k in above}
        bottom = [k for k in ks if k not in tops]
        assert len(bottom) == 1 or (not bottom and len(ks) >= 1)
        if not bottom:          # a cylinder with no singular line at all (torus): cannot happen here
            raise AssertionError('cylinder without boundary')
        order = [bottom[0]]
        while order[-1] in above:
            order.append(above[order[-1]])
        assert sorted(order) == sorted(ks)
        out.append([hc[k] for k in order])
    return out


def main():
    raw = gzip.decompress((HERE / 'inputs' / 'marked-origami-known22-closure.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SHA
    assert len(raw) % (3 * n) == 0
    N = len(raw) // (3 * n)
    st = Counter()
    ncyl = Counter()
    ncyl_marked = Counter()
    one_cyl = []
    s_leaf_states = Counter()
    s_cyl_profile = Counter()
    t_in_s_cylinder = Counter()
    t_location = Counter()
    s_cyl_lines = Counter()
    cyl_count_when_S_regular = Counter()
    s_leaf_hcycle_len = Counter()
    for s in range(N):
        off = s * 3 * n
        h, v, lab = raw[off:off + n], raw[off + n:off + 2 * n], raw[off + 2 * n:off + 3 * n]
        assert sorted(h) == sorted(v) == list(range(n))
        hi, vi = inv(h), inv(v)
        k = [v[h[vi[hi[i]]]] for i in range(n)]
        zero = [False] * n
        for c in cyc(k):
            if len(c) > 1:
                assert len(c) == 3
                for x in c:
                    zero[x] = True
        assert sum(zero) == 27 and Counter(lab) == Counter({3: 40, 0: 12, 1: 4, 2: 4})
        assert lab[0] == 1
        cyls = cylinders(h, v, zero)
        ncyl[len(cyls)] += 1
        marked = [zero[i] or lab[i] in (1, 2) for i in range(n)]
        ncyl_marked[len(cylinders(h, v, marked))] += 1
        if len(cyls) == 1:
            one_cyl.append(s)
            st['one_cyl_states_with_S_on_interior_line'] += any(lab[i] == 1 for strip in cyls[0][1:] for i in strip)
            st['one_cyl_states_with_T_on_interior_line'] += any(lab[i] == 2 for strip in cyls[0][1:] for i in strip)
        # source lifts on closed regular horizontal leaves
        hc = cyc(h)
        regular_s_leaves = [c for c in hc if any(lab[i] == 1 for i in c) and not any(zero[i] for i in c)]
        square0_regular = any(0 in c for c in regular_s_leaves)
        st['square0_source_leaf_regular'] += square0_regular
        if regular_s_leaves:
            st['states_with_some_source_on_regular_leaf'] += 1
            s_leaf_states[sum(lab[i] == 1 for c in regular_s_leaves for i in c)] += 1
            for c in regular_s_leaves:
                s_leaf_hcycle_len[len(c)] += 1
                assert not any(lab[i] == 2 for i in c)
                st['regular_source_leaves_containing_target'] += any(lab[i] == 2 for i in c)
                cy = next(C for C in cyls if any(c == strip for strip in C))
                height = len(cy)
                circ = len(cy[0])
                level = next(j for j, strip in enumerate(cy) if strip == c)
                bottom_line = cy[0]                       # bottom line of the cylinder: carries zeros
                top_line = [v[i] for i in cy[-1]]         # top line of the cylinder: carries zeros
                interior_lines = [strip for strip in cy[1:]]
                t_int = sum(lab[i] == 2 for strip in interior_lines for i in strip)
                t_bot = sum(lab[i] == 2 for i in bottom_line)
                t_top = sum(lab[i] == 2 for i in top_line)
                s_cyl_profile[(height, circ, level)] += 1
                t_in_s_cylinder[(t_int, t_bot, t_top)] += 1
                lines = [bottom_line] + interior_lines + [top_line]
                s_cyl_lines[tuple('/'.join('%s:%d' % (key, val) for key, val in sorted(Counter(
                    'Z' if zero[i] else lab[i] for i in line).items(), key=str)) for line in lines)] += 1
            t_regular = [c for c in hc if any(lab[i] == 2 for i in c) and not any(zero[i] for i in c)]
            st['of_these_states_T_also_on_regular_leaf'] += bool(t_regular)
            sc = {id(C) for C in cyls for c in regular_s_leaves if any(c == strip for strip in C)}
            tc = {id(C) for C in cyls for c in t_regular if any(c == strip for strip in C)}
            st['of_these_states_S_and_T_cylinders_disjoint'] += sc.isdisjoint(tc)
            cyl_count_when_S_regular[len(cyls)] += 1
        # where do the target lifts sit in this state (zeros-only cylinders)?
        for C in cyls:
            for j, strip in enumerate(C):
                for i in strip:
                    if lab[i] == 2:
                        t_location['T on bottom (zero) line' if j == 0 else 'T on interior regular line'] += 1
    out = dict(
        states=N,
        horizontal_cylinders_zeros_only=dict(sorted(ncyl.items())),
        horizontal_cylinders_with_S_T_marked=dict(sorted(ncyl_marked.items())),
        one_cylinder_states=len(one_cyl),
        one_cylinder_state_indices=one_cyl[:50],
        counts=dict(st),
        number_of_source_lifts_on_regular_leaves_per_state=dict(sorted(s_leaf_states.items())),
        regular_source_leaf_length_distribution=dict(sorted(s_leaf_hcycle_len.items())),
        source_cylinder_profile_height_circumference_level={str(k): v for k, v in sorted(s_cyl_profile.items())},
        target_lifts_in_source_cylinder_interior_bottom_top={str(k): v for k, v in sorted(t_in_s_cylinder.items())},
        target_lift_locations_all_states=dict(t_location),
        source_cylinder_line_labels_bottom_to_top={' | '.join(k): v for k, v in s_cyl_lines.items()},
        label_key='Z = true-zero vertex, 0 = other regular, 1 = source lift, 2 = target lift, 3 = convex-corner lift',
        cylinder_count_in_states_with_S_on_regular_leaf=dict(sorted(cyl_count_when_S_regular.items())),
    )
    (HERE / 'task4_cylinders.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
