#!/usr/bin/env python3
"""Aggregate partA-cert job files into partA-totals.md and partA-totals.json.

Usage: partA-aggregate.py RUNDIR [RUNDIR ...]
Each RUNDIR holds job-*.out and job-*.counts files that end with "# DONE".
Rows are per (W, area).  Several RUNDIRs are merged only if they cover
disjoint areas (the script checks this).
"""
import glob, json, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SYM = {1: "id", 2: "mirror x", 4: "mirror y", 8: "rot180", 16: "diag", 32: "rot90", 64: "rot270", 128: "antidiag"}


def sym_name(mask):
    if mask == 1:
        return "none"
    return "+".join(v for k, v in SYM.items() if mask & k and k != 1)


def main(dirs):
    rows = defaultdict(lambda: defaultdict(int))
    hist = defaultdict(int)
    seen_areas = {}
    for d in dirs:
        outs = sorted(glob.glob(os.path.join(d, "job-*.out")))
        assert outs, d
        for f in outs:
            lines = open(f).read().splitlines()
            assert lines[-1] == "# DONE", f
            assert open(f.replace(".out", ".counts")).read().splitlines()[-1] == "# DONE", f
            for l in lines:
                t = l.split()
                if l.startswith("# T "):
                    area, W = int(t[3]), int(t[5])
                    if seen_areas.setdefault(area, d) != d:
                        sys.exit(f"area {area} appears in two run dirs")
                    for i in range(6, len(t), 2):
                        rows[(W, area)][t[i]] += int(t[i + 1])
                elif l.startswith("# sym"):
                    hist[("sym", int(t[3]), int(t[5]))] += int(t[7])
                elif l.startswith("# c2_index"):
                    hist[("c2_index", int(t[2]))] += int(t[4])
                elif l.startswith("# needmax"):
                    hist[("needmax", int(t[5]))] += int(t[7])
                elif l.startswith("# certified_dirs"):
                    hist["two_strip"] += int(t[3]); hist["union_find"] += int(t[5])
                elif l.startswith("# unresolved_total"):
                    hist["unresolved_total"] += int(t[2])
                elif l.startswith("# verify_fail"):
                    hist["verify_fail"] += int(t[2])
    tot = defaultdict(int)
    for r in rows.values():
        for k, v in r.items():
            tot[k] += v
    cols = ["rooms", "reduced", "c1", "c2", "c2_done", "c3", "c3_parity", "same", "same_lit", "diff", "diff_lit",
            "c2_pairs", "c2_lit", "g2_pairs", "g2_lit", "g3_pairs", "g3_lit"]
    md = ["| W | area | " + " | ".join(cols) + " |", "| --- | --- | " + " | ".join("---" for _ in cols) + " |"]
    for (W, area) in sorted(rows):
        r = rows[(W, area)]
        md.append(f"| {W} | {area} | " + " | ".join(f"{r[c]:,}" for c in cols) + " |")
    md.append("| all | all | " + " | ".join(f"{tot[c]:,}" for c in cols) + " |")
    md.append("")
    md.append("Symmetry of normalized rooms by certificate class (1 = X = Z^2, 2 = X larger, 3 = no direction):")
    md.append("")
    md.append("| class | symmetry | rooms |")
    md.append("| --- | --- | --- |")
    for k in sorted(k for k in hist if isinstance(k, tuple) and k[0] == "sym"):
        md.append(f"| {k[1]} | {sym_name(k[2])} | {hist[k]:,} |")
    md.append("")
    for k in sorted(k for k in hist if isinstance(k, tuple) and k[0] == "c2_index"):
        md.append(f"- class (ii) rooms with |X / Z^2| = {k[1]}: {hist[k]:,}")
    for k in sorted(k for k in hist if isinstance(k, tuple) and k[0] == "needmax"):
        md.append(f"- class (i) rooms whose last needed direction has max(p, q) = {k[1]}: {hist[k]:,}")
    md.append(f"- certified directions with 2 strips: {hist['two_strip']:,}; needing union-find: {hist['union_find']:,}")
    md.append(f"- unresolved pairs written to survivor files: {hist['unresolved_total']:,}; verify failures: {hist['verify_fail']:,}")
    open(os.path.join(HERE, "partA-totals.md"), "w").write("\n".join(md) + "\n")
    js = {"rows": {f"{W},{a}": dict(r) for (W, a), r in sorted(rows.items())}, "totals": dict(tot),
          "hist": {str(k): v for k, v in hist.items()}, "dirs": dirs}
    json.dump(js, open(os.path.join(HERE, "partA-totals.json"), "w"), indent=0)
    print("\n".join(md[-12:]))


if __name__ == "__main__":
    main(sys.argv[1:])
