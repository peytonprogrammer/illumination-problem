"""For every room found by enum_rooms (two stars + at most k extra tiles)
with W <= Wmax, search for an exact billiard path from S = 0 to T.

Depth schedule: images of T under words of length <= d in the wall
reflections, d = 0, 1, ..., dmax. A found path is exact (shoot.Tracer).
"Undecided" means no path with at most dmax reflections.

Usage: python3 lit_scan.py n b k Wmax dmax [--nonclean-only]
"""
import json
import sys
import time

from enum_rooms import enumerate_rooms
from shoot import Tracer


def main():
    n, b, k, Wmax, dmax = map(int, sys.argv[1:6])
    nonclean_only = "--nonclean-only" in sys.argv
    skip_shared = "--skip-shared-ctip" in sys.argv  # lit by Proposition R(a), no search needed
    rooms = {}

    def on_room(room, T, K):
        if room.W > Wmax:
            return
        if nonclean_only and room.clean:
            return
        if skip_shared:
            F = room.tri.F
            if any(F.smul(2, p) == T for p, l in room.vlabel.items() if l == "C" and any(t.V["A"] == F.zero and t.V["C"] == p for t in room.tiles)):
                return
        key = frozenset(t.key for t in room.tiles)
        if key not in rooms:
            rooms[key] = (room, T)

    t0 = time.time()
    enumerate_rooms(n, b, k, log=lambda *a: None, on_room=on_room)
    byW = {}
    for room, T in rooms.values():
        byW.setdefault(room.W, []).append((room, T))
    out = {"n": n, "b": b, "k": k, "Wmax": Wmax, "dmax": dmax, "levels": {}}
    for W in sorted(byW):
        lst = byW[W]
        lit_at = {}
        undecided = []
        for room, T in lst:
            tr = Tracer(room)
            S = room.tri.F.zero
            found = None
            for d in range(dmax + 1):
                res = tr.find_path(S, T, d)
                if res["found"]:
                    found = d
                    break
            if found is None:
                undecided.append({"T": list(T), "clean": room.clean, "corners": room.summary(),
                                  "tiles": [[t.s, t.k, list(t.t)] for t in room.tiles],
                                  "transparentE": len(room.transparentE)})
            else:
                lit_at[found] = lit_at.get(found, 0) + 1
        out["levels"][W] = {"rooms": len(lst), "clean": sum(r.clean for r, _ in lst),
                            "lit_by_depth": dict(sorted(lit_at.items())),
                            "undecided": len(undecided), "undecided_examples": undecided[:5]}
        print(W, len(lst), "lit", dict(sorted(lit_at.items())), "undecided", len(undecided),
              "clean among undecided", sum(u["clean"] for u in undecided), round(time.time() - t0), "s", flush=True)
    tag = ("-nc" if nonclean_only else "") + ("-noshared" if skip_shared else "")
    with open(f"lit-{n}-{b}-k{k}-W{Wmax}-d{dmax}{tag}.json", "w") as f:
        json.dump(out, f, indent=1, default=str)


if __name__ == "__main__":
    main()
