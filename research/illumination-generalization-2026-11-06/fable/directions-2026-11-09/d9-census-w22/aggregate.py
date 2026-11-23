"""Aggregate the census jobs into totals per (W, area).

Reads runs/<dir>/job-*.counts (enumerator) and job-*.out (shooter), checks
that every job finished ("# DONE"), adds dark pairs from dark_rooms.json, and
writes census_totals.json plus a Markdown table on stdout.
usage: python3 aggregate.py runs/a20 NJ
"""
import glob
import json
import sys
from collections import defaultdict


def opn(path):
    """Open a text file, or its gzip-compressed copy path + '.gz'."""
    import gzip
    import os
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        return gzip.open(path + ".gz", "rt")
    return open(path)


def main():
    rdir, nj = sys.argv[1], int(sys.argv[2])
    cnt = defaultdict(lambda: defaultdict(int))
    glob_stats = defaultdict(int)
    khist = defaultdict(int)
    maxk = defaultdict(int)
    fixed = defaultdict(int)
    for j in range(nj):
        cf, of = f"{rdir}/job-{j}.counts", f"{rdir}/job-{j}.out"
        clines = open(cf).read().split("\n")
        olines = opn(of).read().split("\n")
        assert "# DONE" in clines and "# DONE" in olines, f"job {j} incomplete"
        for ln in clines:
            f = ln.split()
            if ln.startswith("# count"):
                a, w = int(f[3]), int(f[5])
                cnt[(w, a)]["rooms"] += int(f[7])
                cnt[(w, a)]["eligible_enum"] += int(f[9])
            elif ln.startswith("# fixed area"):
                fixed[int(f[3])] += int(f[4])
        for ln in olines:
            f = ln.split()
            if ln.startswith("# T "):
                a, w = int(f[3]), int(f[5])
                c = cnt[(w, a)]
                c["eligible"] += int(f[7])
                c["pairs"] += int(f[9])
                c["lit_by_shooting"] += int(f[11])
                c["survivors"] += int(f[13])
                c["rooms_with_lit_pair_k_ge7"] += int(f[15])
                c["lit_pairs_k_ge7"] += int(f[17])
                maxk[(w, a)] = max(maxk[(w, a)], int(f[19]))
            elif ln.startswith("# lit_pairs_W_k"):
                khist[(int(f[2]), int(f[3]))] += int(f[4])
            elif ln.startswith("# ") and len(f) == 3 and f[1] in (
                    "lit_but_separated", "unresolved_separated", "unresolved_not_separated",
                    "verify_fail", "rooms_with_lit_pair_k_ge7", "lit_pairs_k_ge7"):
                glob_stats[f[1]] += int(f[2])
            elif ln.startswith("# max_k_lit"):
                glob_stats["max_k_lit"] = max(glob_stats["max_k_lit"], int(f[2]))
    dark = json.load(open("dark_rooms.json"))
    for d in dark:
        cnt[(d["W"], d["area"])]["dark"] += 1
    for key, c in cnt.items():
        assert c["eligible"] == c["eligible_enum"], key
    rows = sorted(cnt)
    tot = defaultdict(int)
    print("| W | area | rooms | rooms with eligible pairs | pairs | lit by shooting | survivors | dark |"
          " max k (lit) | rooms with a lit pair, k >= 7 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for (w, a) in rows:
        c = cnt[(w, a)]
        for k in ("rooms", "eligible", "pairs", "lit_by_shooting", "survivors", "dark", "rooms_with_lit_pair_k_ge7"):
            tot[k] += c[k]
        if c["eligible"] == 0:
            continue
        print(f"| {w} | {a} | {c['rooms']:,} | {c['eligible']:,} | {c['pairs']:,} | {c['lit_by_shooting']:,} |"
              f" {c['survivors']} | {c['dark']} | {maxk[(w, a)]} | {c['rooms_with_lit_pair_k_ge7']:,} |")
    print(f"\nTotals: {dict(tot)}")
    print(f"Global: {dict(glob_stats)}")
    print("Fixed polyominoes processed per area:", dict(sorted(fixed.items())))
    byw = defaultdict(lambda: defaultdict(int))
    for (w, a), c in cnt.items():
        for k in ("rooms", "eligible", "pairs", "lit_by_shooting", "survivors", "dark", "rooms_with_lit_pair_k_ge7"):
            byw[w][k] += c[k]
    print("\n| W | rooms | rooms with eligible pairs | pairs | dark | rooms with a lit pair, k >= 7 | max k (lit) |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for w in sorted(byw):
        b = byw[w]
        mk = max((k for (ww, k) in khist if ww == w), default=-1)
        print(f"| {w} | {b['rooms']:,} | {b['eligible']:,} | {b['pairs']:,} | {b['dark']} |"
              f" {b['rooms_with_lit_pair_k_ge7']:,} | {mk} |")
    json.dump({"per_W_area": {f"{w},{a}": dict(c) | {"max_k_lit": maxk[(w, a)]} for (w, a), c in cnt.items()},
               "global": dict(glob_stats), "lit_pairs_by_W_k": {f"{w},{k}": v for (w, k), v in khist.items()},
               "fixed_polyominoes_per_area": fixed},
              open("census_totals.json", "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
