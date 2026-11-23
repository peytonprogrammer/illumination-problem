"""Task 4-5: confusion tables and notable facts from results.jsonl.

Usage: python3 -B analyze.py   (writes summary.json, prints the tables)
"""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    return [json.loads(line) for line in open(os.path.join(HERE, "results.jsonl"))]


def key(pr):
    return ("separated" if pr["separated"] else "not separated", f'{pr["verdict"]}/{pr["method"]}')


def table(rows, pred=lambda r, p: True):
    c = Counter()
    for r in rows:
        for p in r["pairs"]:
            if pred(r, p):
                c[key(p)] += 1
    return {f"{a} | {b}": n for (a, b), n in sorted(c.items())}


def main():
    rows = load()
    out = {"rooms": len(rows)}
    out["rooms_by_base_level"] = dict(Counter(f'{r["base"]} L{r["level"]}' for r in rows))
    out["orbit_status"] = dict(Counter(f'{r["base"]} {r["orbit_status"]}' for r in rows))
    out["pairs_total"] = sum(len(r["pairs"]) for r in rows)
    out["confusion_all_pairs"] = table(rows)
    out["confusion_marks_pair"] = table(rows, lambda r, p: p["marks"])
    out["confusion_A_class_of_marks"] = table(
        rows, lambda r, p: p["p"] in r["classes"].get(p["class"], {}).get("points", []) and
        tuple(r["marks"][0]) in map(tuple, r["classes"][p["class"]]["points"]))
    out["confusion_by_base_level"] = {
        f"{b} L{l}": table(rows, lambda r, p, b=b, l=l: r["base"] == b and r["level"] == l)
        for b in ("R22", "R34") for l in (0, 1, 2)}

    cex, bugs, undecided, uncert = [], [], [], []
    for r in rows:
        for p in r["pairs"]:
            rec = {"room": r["id"], "moves": r["moves"], "W": r["W"], "p": p["p"], "q": p["q"],
                   "class": p["class"], "method": p["method"]}
            if p["verdict"] == "DARK" and not p["separated"]:
                cex.append(dict(rec, vertices=r["vertices"]))
            if p["verdict"].startswith("LIT") and p["separated"]:
                bugs.append(rec)
            if p["verdict"] == "UNDECIDED":
                undecided.append(dict(rec, separated=p["separated"], states=r["orbit_states"]))
            if p["verdict"] == "LIT?":
                uncert.append(rec)
    out["counterexamples_dark_not_separated"] = cex
    out["contradictions_lit_separated"] = bugs
    out["undecided"] = undecided
    out["uncertified_lit"] = uncert

    # rooms whose marked pair is dark
    dark_rooms = []
    for r in rows:
        mp = [p for p in r["pairs"] if p["marks"]][0]
        if mp["verdict"] == "DARK":
            A = r["classes"][mp["class"]]
            dark_rooms.append({"room": r["id"], "level": r["level"], "moves": r["moves"],
                               "W": r["W"], "r": r["r"], "area": r["area"], "k": r["k_marks"],
                               "nmin_degree": A["nmin_degree"], "primitive": r["primitive"],
                               "group_order": r["group_order"], "method": mp["method"],
                               "transparent": r["transparent_marks"]})
    out["dark_marked_rooms"] = len(dark_rooms)
    out["dark_marked_rooms_by_base_level"] = dict(Counter(f'{d["room"][:3]} L{d["level"]}' for d in dark_rooms))
    pert = [d for d in dark_rooms if d["level"] > 0]
    out["smallest_W_dark_perturbed"] = min((d["W"] for d in pert), default=None)
    out["dark_perturbed_W_le_21"] = [d for d in pert if d["W"] <= 21]
    out["dark_perturbed_by_k_degree"] = dict(Counter(
        f'{d["room"][:3]} k={d["k"]} deg={d["nmin_degree"]} prim={d["primitive"]}' for d in pert))
    out["dark_perturbed_rooms"] = pert

    # effect of the change in k on the marked pair
    eff = defaultdict(Counter)
    basek = {r["base"]: r["k_marks"] for r in rows if r["level"] == 0}
    for r in rows:
        if r["level"] == 0:
            continue
        mp = [p for p in r["pairs"] if p["marks"]][0]
        eff[f'{r["base"]} L{r["level"]} dk={r["k_marks"] - basek[r["base"]]:+d}'][mp["verdict"]] += 1
    out["marks_verdict_by_delta_k"] = {k: dict(v) for k, v in sorted(eff.items())}

    # primitivity and N_min degree of the marks' class over all rooms
    out["nmin_degree_vs_primitive"] = dict(Counter(
        f'prim={r["primitive"]} deg={r["classes"][[p for p in r["pairs"] if p["marks"]][0]["class"]]["nmin_degree"]}'
        for r in rows))
    out["W_range"] = [min(r["W"] for r in rows), max(r["W"] for r in rows)]
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=list)
    for k, v in out.items():
        if k in ("dark_perturbed_rooms",):
            continue
        print(k, ":", json.dumps(v, default=list)[:3000])


if __name__ == "__main__":
    main()
