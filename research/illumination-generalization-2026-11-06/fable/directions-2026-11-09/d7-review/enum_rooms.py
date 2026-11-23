"""Exhaustive enumeration of rooms that contain two full stars plus at most
k extra tiles.

Bound, stated exactly: for the triangle (n, b), every strictly simple room
Q = St(S) u St(T) u K with S != T interior A points and |K| <= k. S is fixed
at the origin. T ranges over every A vertex of a tile at reflection distance
at most k + 1 from St(S), up to the 2n symmetries of St(S). K ranges over
every set of at most k tiles in which each tile is joined to St(S) u St(T)
through edges of K tiles (Redelmeier enumeration, each set once per T).
Validity is checked by geom.Room.analyze (pairwise compatibility is
enforced during growth).

Usage: python3 enum_rooms.py n b k [--maxT N]
"""
import json
import sys
import time

from geom import Triangle, Tile, star, mirror, compatible, Room, EDGES


class Universe:
    def __init__(self, tri):
        self.tri = tri
        self.tiles = {}
        self.nbrs = {}
        self.cache = {}

    def intern(self, t):
        return self.tiles.setdefault(t.key, t)

    def neighbors(self, t):
        r = self.nbrs.get(t.key)
        if r is None:
            r = [self.intern(mirror(self.tri, t, e)) for e in EDGES]
            self.nbrs[t.key] = r
        return r

    def compat(self, t1, t2):
        k = (t1.key, t2.key) if t1.key < t2.key else (t2.key, t1.key)
        v = self.cache.get(k)
        if v is None:
            v = compatible(self.tri, t1, t2)
            self.cache[k] = v
        return v


def sym_images(tri, p):
    F = tri.F
    out = []
    for k in range(0, 2 * tri.n, 2):
        out.append(F.mul(F.z(k), p))
        out.append(F.mul(F.z(k), F.conj(p)))
    return out


def t_candidates(U, tri, starS, k):
    F = tri.F
    dist = {t.key: 0 for t in starS}
    frontier = list(starS)
    cands = {}
    for d in range(1, k + 2):
        nf = []
        for t in frontier:
            for nb in U.neighbors(t):
                if nb.key not in dist:
                    dist[nb.key] = d
                    nf.append(nb)
                    A = nb.V["A"]
                    if A != F.zero:
                        canon = min(sym_images(tri, A))
                        cands.setdefault(canon, d)
        frontier = nf
    return cands


def enumerate_rooms(n, b, k, maxT=None, log=print, keep=3, wkeep=-1, on_room=None):
    nonclean = []
    tri = Triangle(n, b)
    F = tri.F
    U = Universe(tri)
    S = F.zero
    starS = [U.intern(t) for t in star(tri, S)]
    cands = t_candidates(U, tri, starS, k)
    log(f"(n,b)=({n},{b}) E={sorted(tri.E)} k={k}: {len(cands)} T candidates up to symmetry")
    best = {"all": None, "clean": None}
    examples = {"all": [], "clean": []}
    stats = {"T_tried": 0, "T_star_ok": 0, "sets": 0, "valid": 0, "by_W": {}, "by_W_clean": {}}
    t0 = time.time()
    order = sorted(cands.items(), key=lambda kv: kv[1])
    if maxT:
        order = order[:maxT]
    for T, d in order:
        stats["T_tried"] += 1
        starT = [U.intern(t) for t in star(tri, T)]
        keysS = {t.key for t in starS}
        if any(t.key in keysS for t in starT):
            continue
        if not all(U.compat(a, c) for a in starS for c in starT):
            continue
        stats["T_star_ok"] += 1
        keysT = {t.key for t in starT}
        U0 = starS + starT
        U0keys = {t.key for t in U0}
        okU0 = {}

        def ok_with_U0(t):
            v = okU0.get(t.key)
            if v is None:
                v = all(U.compat(t, u) for u in U0)
                okU0[t.key] = v
            return v

        def evaluate(K):
            stats["sets"] += 1
            room = Room(tri, U0 + K)
            if not room.analyze(check_pairs=False):
                return
            stats["valid"] += 1
            W = room.W
            if on_room is not None:
                on_room(room, T, list(K))
            stats["by_W"][W] = stats["by_W"].get(W, 0) + 1
            rec_ = {"W": W, "T": T, "tiles": len(U0) + len(K), "K": [[t.s, t.k, list(t.t)] for t in K],
                    "corners": room.summary(), "clean": room.clean, "interiorA": len(room.interiorA),
                    "transparentE": len(room.transparentE)}
            if not room.clean and W <= wkeep and len(nonclean) < 400:
                nonclean.append(rec_)
            for cls in ("all", "clean"):
                if cls == "clean" and not room.clean:
                    continue
                if cls == "clean":
                    stats["by_W_clean"][W] = stats["by_W_clean"].get(W, 0) + 1
                if best[cls] is None or W < best[cls]:
                    best[cls] = W
                    examples[cls] = [rec_]
                elif W == best[cls] and len(examples[cls]) < keep:
                    examples[cls].append(rec_)

        # Redelmeier on the tile graph with St(S) and St(T) contracted to
        # root nodes. Root = St(S). The node "T" (all of St(T)) must be in
        # the final set. Prune: a node set X can reach "T" only with at least
        # min_{x in X} distT(x) - 1 further tiles.
        distT = {t.key: 0 for t in starT}
        fr = list(starT)
        for dd in range(1, k + 2):
            nf = []
            for t in fr:
                for nb in U.neighbors(t):
                    if nb.key not in distT:
                        distT[nb.key] = dd
                        nf.append(nb)
            fr = nf
        INF = 10 ** 9
        Tnode = "T"
        seen = set(U0keys)
        init = []
        for t in starS:
            for nb in U.neighbors(t):
                if nb.key in keysT:
                    if Tnode not in seen:
                        seen.add(Tnode)
                        init.append(Tnode)
                elif nb.key not in seen:
                    seen.add(nb.key)
                    init.append(nb)
        TN = []
        for t in starT:
            for nb in U.neighbors(t):
                if nb.key not in U0keys:
                    TN.append(nb)

        def rec(untried, K, seen, haveT, mind):
            untried = list(untried)
            while untried:
                t = untried.pop()
                if isinstance(t, str):
                    if all(ok_with_U0(x) for x in K):
                        evaluate(K)
                        if len(K) < k:
                            new = []
                            s2 = set(seen)
                            for nb in TN:
                                if nb.key not in s2:
                                    s2.add(nb.key)
                                    new.append(nb)
                            rec(untried + new, K, s2, True, 0)
                    continue
                if len(K) >= k:
                    continue
                if not ok_with_U0(t) or not all(U.compat(t, x) for x in K):
                    continue
                md = min(mind, distT.get(t.key, INF))
                if not haveT and len(K) + 1 + md - 1 > k:
                    continue
                K.append(t)
                if haveT:
                    evaluate(K)
                if len(K) < k or not haveT:
                    new = []
                    s2 = set(seen)
                    for nb in U.neighbors(t):
                        if nb.key in keysT:
                            if Tnode not in s2:
                                s2.add(Tnode)
                                new.append(Tnode)
                        elif nb.key not in s2:
                            s2.add(nb.key)
                            new.append(nb)
                    rec(untried + new, K, s2, haveT, md)
                K.pop()

        keysS0 = min(distT.get(t.key, INF) for t in starS)
        rec(init, [], seen, False, keysS0)
    stats["seconds"] = round(time.time() - t0, 1)
    stats["by_W"] = dict(sorted(stats["by_W"].items()))
    stats["by_W_clean"] = dict(sorted(stats["by_W_clean"].items()))
    return {"n": n, "b": b, "k": k, "E": sorted(tri.E), "min_W_all": best["all"], "min_W_clean": best["clean"],
            "examples": examples, "stats": stats, "nonclean": nonclean}


if __name__ == "__main__":
    n, b, k = map(int, sys.argv[1:4])
    maxT = None
    if "--maxT" in sys.argv:
        maxT = int(sys.argv[sys.argv.index("--maxT") + 1])
    wkeep = int(sys.argv[sys.argv.index("--wkeep") + 1]) if "--wkeep" in sys.argv else -1
    res = enumerate_rooms(n, b, k, maxT, wkeep=wkeep)
    def conv(o):
        if isinstance(o, dict):
            return {str(kk): conv(v) for kk, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        return o
    out = f"enum-{n}-{b}-k{k}.json"
    with open(out, "w") as f:
        json.dump(conv(res), f, indent=1)
    print(json.dumps({kk: conv(v) for kk, v in res.items() if kk not in ("examples", "nonclean")}, indent=1))
    for cls in ("clean", "all"):
        for ex in res["examples"][cls][:2]:
            print(cls, ex["W"], ex["tiles"], ex["corners"], "clean", ex["clean"], "transpE", ex["transparentE"])
