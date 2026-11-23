#!/usr/bin/env python3
"""Coverage table for part A: which rooms have every real interior pair decided.

Inputs (all under runs/partA/):
  partA-totals.json             aggregate of the main run (partA-aggregate.py)
  post/reduced16.txt            reduced rooms by normal-form class (partA-reduced.py)
  post/rescue120.out            survivors re-shot with bound 120
  post/c2big40.out              C2BIG rooms re-run with directions up to 40
A normalized room is fully covered when it is in class (i) or (ii) and every
pair of interior points of X was decided.  A reduced room is fully covered
when its normal form is.  Class (iii) rooms are partial.
Writes partA-coverage.md.  Usage: partA-final.py
"""
import json, os, re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "runs", "partA")
tot = json.load(open(os.path.join(HERE, "partA-totals.json")))

# survivors: every line in rescue120.out must be LIT
resc = [l.split()[0] for l in open(os.path.join(R, "post", "rescue120.out")) if not l.startswith("#")]
assert resc and all(x == "LIT" for x in resc), "rescue left survivors"
# C2BIG retry: all rooms done, no survivor
big = open(os.path.join(R, "post", "c2big40.out")).read()
big_rooms = sum(int(x) for x in re.findall(r" c2_done (\d+)", big))
big_unres = int(re.search(r"# unresolved_total (\d+)", big).group(1))
assert big_unres == 0

red = defaultdict(lambda: defaultdict(int))
for l in open(os.path.join(R, "post", "reduced16.txt")):
    m = re.match(r"W (\d+) area (\d+) normal-form class (\S+) rooms (\d+)", l)
    if m:
        red[(int(m.group(1)), int(m.group(2)))][m.group(3)] += int(m.group(4))

byW = defaultdict(lambda: defaultdict(int))
byA = defaultdict(lambda: defaultdict(int))
c2_notdone = 0
for key, r in tot["rows"].items():
    W, a = map(int, key.split(","))
    c2_notdone += r["c2"] - r["c2_done"]
    full = r["c1"] + r["c2"] + red[(W, a)]["i/ii"]
    part = r["c3"] + red[(W, a)]["iii"]
    assert r["reduced"] == red[(W, a)]["i/ii"] + red[(W, a)]["iii"], (W, a)
    for d, k in ((byW, W), (byA, a)):
        d[k]["rooms"] += r["rooms"]; d[k]["full"] += full; d[k]["partial"] += part
        d[k]["c3"] += r["c3"]; d[k]["c3_parity"] += r["c3_parity"]
# every class (ii) room that was not done inline is a C2BIG room (done by the retry)
# or has survivors (all rescued); check the counts add up
sv_rooms = c2_notdone - big_rooms
assert sv_rooms >= 0

out = ["# Part A coverage, all strictly simple rooms with W <= 22 and area <= 16", "",
       "Fully covered: every pair of distinct real interior points is decided.",
       "Partial: class (iii) rooms, or reduced rooms whose normal form is in class (iii).", ""]
for name, d in (("W", byW), ("area", byA)):
    out += [f"| {name} | rooms | fully covered | partial | class (iii) normalized | of which parity-obstructed |",
            "| --- | --- | --- | --- | --- | --- |"]
    for k in sorted(d):
        r = d[k]
        out.append(f"| {k} | {r['rooms']:,} | {r['full']:,} | {r['partial']:,} | {r['c3']:,} | {r['c3_parity']:,} |")
    s = defaultdict(int)
    for r in d.values():
        for kk, v in r.items():
            s[kk] += v
    out.append(f"| all | {s['rooms']:,} | {s['full']:,} | {s['partial']:,} | {s['c3']:,} | {s['c3_parity']:,} |")
    out.append("")
out.append(f"Class (ii) rooms not finished inline: {c2_notdone:,} ({big_rooms:,} C2BIG rooms finished by the bound-40 retry; "
           f"{sv_rooms:,} rooms with survivors, all {len(resc):,} survivor pairs (with grid survivors) lit at bound 120).")
open(os.path.join(HERE, "partA-coverage.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
