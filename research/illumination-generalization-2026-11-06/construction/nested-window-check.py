#!/usr/bin/env python3
"""Exact prescribed construction checks, no slope/room discovery."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import json
import time

ROOT = Path(__file__).resolve().parent
effort = json.loads((ROOT / 'four-band-roof-effort.json').read_text())
deadline = datetime.fromisoformat(effort['aggregate_deadline_utc']).timestamp()
assert time.time() < deadline, 'Original A13 deadline expired'


def fold(q, w):
    r = q % (2 * w)
    return r if r <= w else 2 * w - r


def check(widths, heights, source, target):
    widths, heights = list(map(F, widths)), list(map(F, heights))
    s, ys = map(F, source)
    t, yt = map(F, target)
    m = len(widths)
    assert len(heights) == m + 1
    assert all(widths[l] > widths[l + 1] for l in range(m - 1))
    assert all(widths[l] * (heights[l + 1] - heights[l]) >= widths[l + 1] * heights[l]
               for l in range(1, m - 1))
    i = max(l for l in range(m) if heights[l] <= ys)
    j = max(l for l in range(m) if heights[l] <= yt)
    assert i < j and ys < yt and 0 < s < widths[i] and 0 < t < widths[j]
    constants = {i: F(0), i + 1: 2 * widths[i]}
    lo = (constants[i + 1] - s - widths[i + 1]) / (heights[i + 1] - ys)
    hi = (constants[i + 1] - s + widths[i + 1]) / (heights[i + 1] - ys)
    for l in range(i + 1, j):
        total = heights[l] - ys
        gap = heights[l + 1] - heights[l]
        center = gap * (constants[l] - s) / total
        k = (center / (2 * widths[l]) + F(1, 2)) // 1
        constants[l + 1] = constants[l] + 2 * k * widths[l]
        new_lo = (constants[l + 1] - s - widths[l + 1]) / (heights[l + 1] - ys)
        new_hi = (constants[l + 1] - s + widths[l + 1]) / (heights[l + 1] - ys)
        assert 0 < lo <= new_lo < new_hi <= hi
        lo, hi = new_lo, new_hi
    zlo, zhi = (s + (yt - ys) * tau - constants[j] for tau in (lo, hi))
    assert zhi - zlo >= 2 * widths[j]
    images = []
    for sign in [-1, 1]:
        q = (zlo - sign * t) // (2 * widths[j]) + 1
        images.append(sign * t + 2 * q * widths[j])
    image = min(images)
    assert zlo < image < zhi
    tau = (constants[j] + image - s) / (yt - ys)
    assert 0 < lo < tau < hi
    events = {ys: s, yt: t}
    for l in range(i, j + 1):
        bottom, top = max(ys, heights[l]), min(yt, heights[l + 1])
        qlo = s + tau * (bottom - ys) - constants[l]
        qhi = s + tau * (top - ys) - constants[l]
        for q in range(int(qlo // widths[l]) - 1, int(qhi // widths[l]) + 2):
            eta = ys + (q * widths[l] - s + constants[l]) / tau
            if bottom < eta < top:
                events[eta] = fold(q * widths[l], widths[l])
        if l > i:
            x = fold(s + tau * (heights[l] - ys) - constants[l], widths[l])
            if heights[l] in events:
                assert events[heights[l]] == x
            events[heights[l]] = x
            assert x < widths[l]
    points = [(x, y) for y, x in sorted(events.items())]
    corners = {(F(0), F(0)), (widths[0], F(0)), (F(0), heights[-1]),
               (widths[-1], heights[-1])}
    for l in range(1, m):
        corners.update([(widths[l - 1], heights[l]), (widths[l], heights[l])])
    assert len(corners) == 2 * m + 2
    assert not any(p in corners for p in points)
    contacts = 0
    for k, (x, y) in enumerate(points):
        assert time.time() < deadline
        if 0 < k < len(points) - 1:
            before, after = points[k - 1], points[k + 1]
            vin = (x - before[0]) / (y - before[1])
            vout = (after[0] - x) / (after[1] - y)
            assert abs(vin) == tau and abs(vout) == tau
            l = max(z for z in range(m) if heights[z] <= y)
            mirror = x == 0 or (x == widths[l] and y not in heights)
            assert vout == (-vin if mirror else vin)
            contacts += int(mirror)
        if k:
            xm, ym = (x + points[k - 1][0]) / 2, (y + points[k - 1][1]) / 2
            l = max(z for z in range(m) if heights[z] <= ym)
            assert 0 < xm < widths[l]
    return {'widths': list(map(str, widths)), 'heights': list(map(str, heights)),
            'S': list(map(str, source)), 'T': list(map(str, target)),
            'tau': str(tau), 'contacts': contacts, 'segments': len(points) - 1,
            'points': [[str(x), str(y)] for x, y in points], 'status': 'PASS'}


rows = [check([16, 8, 4, 2], [0, 1, 2, 3, 4], [15, F(1, 2)], [1, F(7, 2)]),
        check([16, 8, 4, 2], [0, 1, 2, 3, 4], [15, F(1, 2)], [1, 3]),
        check(list(range(10, 1, -1)), [0, 1, 2, 4, 8, 16, 32, 64, 128, 256],
              [8, 1], [1, 128])]
out = {'status': 'PRESCRIBED_CONSTRUCTION_PASS', 'rows': rows,
       'contacts': sum(r['contacts'] for r in rows),
       'within_original_deadline': time.time() < deadline,
       'independent_peer_acceptance': False, 'whole_goal_complete': False}
(ROOT / 'nested-window-check.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: out[k] for k in ['status', 'contacts', 'within_original_deadline']}))
