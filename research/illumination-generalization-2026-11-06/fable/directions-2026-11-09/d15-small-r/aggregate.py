"""Sum the LEMMA / UNCOVERED / SUMMARY lines of verify.c outputs. Usage: aggregate.py files..."""
import sys, re, collections
tot = collections.defaultdict(collections.Counter); other = collections.Counter()
for fn in sys.argv[1:]:
    for line in open(fn):
        f = line.split()
        if not f: continue
        if f[0] in ("LEMMA", "UNCOVERED", "SUMMARY"):
            key = f[1] if f[0] == "LEMMA" else f[0]
            for kv in f[(2 if f[0] == "LEMMA" else 1):]:
                k, v = kv.split("=")
                if k.startswith("max"): tot[key][k] = max(tot[key][k], int(v))
                else: tot[key][k] += int(v)
        else:
            other[f[0]] += 1
for key, c in tot.items(): print(key, dict(c))
print("other lines", dict(other))
