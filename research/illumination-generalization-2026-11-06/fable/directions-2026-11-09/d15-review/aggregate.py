"""Sum the attack results. Usage: python3 -B aggregate.py runs/run2"""
import json
import sys
from collections import Counter

prefix = sys.argv[1]
tot, r2, kinds, styles = Counter(), Counter(), Counter(), Counter()
for i in range(10):
    d = json.load(open(f"{prefix}_type{i}.json"))
    s = d['stats']
    mism = sum(v for k, v in d['tracer_check'].items() if k != 'compared')
    print(f"{i} {d['shape']:12s} rooms {d['rooms']} pairs {s['pairs']} engineered {s.get('pairs-engineered', 0)} "
          f"traces {s['traces']} skipped {s.get('traces skipped (over the reflection cap)', 0)} "
          f"max reflections {d['max_reflections']} failures {d['n_failures']} seconds {d['seconds']}")
    print("     ", {k: v for k, v in sorted(s.items()) if k.startswith('cert')})
    for c in (tot,) + ((r2,) if i < 8 else ()):
        c.update(s)
        c['rooms'] += d['rooms']
        c['failures'] += d['n_failures']
        c['tracer cross-checks'] += d['tracer_check'].get('compared', 0)
        c['tracer mismatches'] += mism
    kinds.update(d['pair_kinds'])
    for k, v in d['room_styles'].items():
        styles[k.split('/')[0]] += v
        styles[k.split('/')[1]] += v
print("\nall 10 types / the 8 two-reflex types")
for k in sorted(tot):
    print(f"  {k:58s} {tot[k]:>9} {r2[k]:>9}")
print("pair kinds", dict(kinds))
print("room styles and fields", dict(styles))
