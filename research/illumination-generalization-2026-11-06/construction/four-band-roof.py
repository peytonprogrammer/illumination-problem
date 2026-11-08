#!/usr/bin/env python3
"""Bounded exact challenge to two prescribed four-band path charts."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
from math import gcd, lcm, ceil
import json
import signal
import time

ROOT = Path(__file__).resolve().parent
effort = json.loads((ROOT / 'four-band-roof-effort.json').read_text())
deadline = datetime.fromisoformat(effort['aggregate_deadline_utc']).timestamp()
if time.time() >= deadline:
    raise SystemExit('Original effort deadline expired')
signal.alarm(max(1, int(deadline - time.time())))


def fold_leg(x, velocity, duration, width):
    q = x + velocity * duration
    residue = q % (2 * width)
    out = residue if residue <= width else 2 * width - residue
    if out == 0:
        outgoing = abs(velocity)
    elif out == width:
        outgoing = -abs(velocity)
    else:
        outgoing = velocity if (q // width) % 2 == 0 else -velocity
    return out, outgoing


def chart(widths, s, t, roof):
    durations = [F(1, 2), F(1), F(1), F(3, 2) if roof else F(1, 2)]
    total = sum(durations)
    period = 2 * lcm(*(2 * w for w in widths))
    common = gcd(*widths)
    slopes = set()
    for sign_s in [-1, 1]:
        for sign_t in [-1, 1]:
            offset = sign_t * t - sign_s * s
            for n in range(-3, ceil(total * period / (2 * common)) + 4):
                tau = (2 * common * n + offset) / total
                if 0 < tau < period:
                    slopes.add(tau)
    records = []
    for tau in sorted(slopes):
        if time.time() >= deadline:
            raise SystemExit('Original effort deadline reached')
        for sign in [-1, 1]:
            x, velocity = s, sign * tau
            portals = []
            outcome = None
            for j, duration in enumerate(durations):
                x, velocity = fold_leg(x, velocity, duration, widths[j])
                if j < 3:
                    portals.append(str(x))
                    if x >= widths[j + 1]:
                        outcome = 'portal_' + str(j + 1)
                        break
            if outcome is None:
                outcome = 'target' if x == t else 'wrong_target'
            rec = {'tau': str(tau), 'initial_sign': sign,
                   'portals': portals, 'outcome': outcome}
            records.append(rec)
            if outcome == 'target':
                return {'status': 'CONNECTS_IN_CHART', 'roof': roof,
                        'period': period, 'necessary_slopes': len(slopes),
                        'tested': len(records), 'witness': rec}
    return {'status': 'COMPLETE_CHART_FAILURE', 'roof': roof,
            'period': period, 'necessary_slopes': len(slopes),
            'tested': len(records), 'records': records}


fixtures = [(4, 3, 2, 1), (5, 4, 3, 1), (6, 5, 4, 3), (7, 5, 3, 1),
            (7, 6, 5, 2), (8, 7, 6, 5), (8, 6, 4, 1), (9, 8, 7, 3),
            (9, 7, 5, 2), (10, 9, 8, 7), (10, 7, 4, 1), (10, 8, 5, 3)]
rows = []
failure = None
for widths in fixtures:
    for s, t in [(F(widths[0] + widths[1], 2), F(widths[-1], 2)),
                 (F(2 * widths[0] - 1, 2), F(1, 2))]:
        direct = chart(widths, s, t, False)
        roof = chart(widths, s, t, True) if direct['status'] != 'CONNECTS_IN_CHART' else None
        row = {'widths': widths, 'heights': [1, 1, 1, 1],
               'S': [str(s), '1/2'], 'T': [str(t), '7/2'],
               'direct': direct, 'roof': roof}
        rows.append(row)
        if roof and roof['status'] == 'COMPLETE_CHART_FAILURE':
            failure = row
            break
    if failure:
        break
signal.alarm(0)
result = {'status': 'JOINT_CHART_FAILURE' if failure else 'FIXTURES_CONNECT_NO_UNIVERSAL_CLAIM',
          'rows_checked': len(rows), 'rows': rows, 'failure': failure,
          'physical_darkness': False, 'whole_goal_complete': False,
          'within_original_deadline': time.time() < deadline,
          'ended_utc': datetime.now(timezone.utc).isoformat()}
(ROOT / 'four-band-roof.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'rows_checked', 'within_original_deadline']}))
if failure:
    print(json.dumps({k: failure[k] for k in ['widths', 'S', 'T']}))
