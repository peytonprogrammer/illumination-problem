#!/usr/bin/env python3
"""summ.py FILE... -- compact summary of band output: per run, max over (g,pair) of minimal p, unlit (g,pair),
and the eventual period of the sequence g -> minp for each pair (smallest Q with minp(g+Q)=minp(g) for g>=G0)."""
import sys, collections
for fn in sys.argv[1:]:
    mp = collections.defaultdict(dict); sep = {}; hdr = ""
    for ln in open(fn):
        if ln.startswith("# points"): hdr = ln.strip()
        if ln[0] != "G": continue
        _, g, i, p, q, s = ln.split(); g, i, p, q, s = int(g), int(i), int(p), int(q), int(s)
        mp[i][g] = p
        if p < 0: sep[(g, i)] = s
    gs = sorted(next(iter(mp.values())).keys()) if mp else []
    allp = [(p, g, i) for i in mp for g, p in mp[i].items()]
    hist = collections.Counter(p for p, g, i in allp)
    mx = max(allp) if allp else None
    late = max(((p, g, i) for p, g, i in allp if g > gs[-1] // 2), default=None)
    print(f"{fn}: {hdr}")
    print(f"  pairs {len(mp)} g {gs[0]}..{gs[-1]}  max minp (p,g,pair) {mx}  max in upper half {late}  hist {dict(sorted(hist.items()))}")
    un = sorted(sep.items()); 
    if un: print(f"  no witness: {len(un)}; separated(proved dark) {sum(1 for k,v in un if v==1)}; unseparated {[(k) for k,v in un if v!=1][:12]}; sep list {[(k) for k,v in un if v==1][:12]}")
    pers = collections.Counter()
    for i in mp:
        seq = [mp[i][g] for g in gs]; n = len(seq); best = None
        for G0 in (0, 1, 2, 5, 10):
            for Q in range(1, (n - G0) // 3 + 1):
                if all(seq[k] == seq[k + Q] for k in range(G0, n - Q)): best = (G0, Q); break
            if best: break
        pers[best] += 1
    print(f"  eventual period of minp sequence (start index, period in steps of 2) -> #pairs: {dict(pers)}")
