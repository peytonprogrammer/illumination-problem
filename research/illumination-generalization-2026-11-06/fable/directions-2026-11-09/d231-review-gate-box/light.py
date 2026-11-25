"""Cheap pass: lattice data, Lemma 1 check, min width, exact hollowness per parity
coset, and an exact trace of every box hit found (soundness spot check)."""
import itertools, time
from fractions import Fraction as F
import gatebox as G

def analyse(name, V, S0, T, gmax, keep, log):
    t0 = time.process_time()
    refl, area = G.check_room(V); ys, S = G.slabs(V)
    log(f"\n## {name}: {len(V)} walls, {refl} reflexes, area {area}, S={S0}, T={T}")
    for it in G.itineraries(V, S0, T, gmax):
        visits, events = it; g = len(events)
        if g == 0 or not keep(events):
            continue
        Ld = G.lattice_data(it); mw = G.min_width(it, Ld['dual'], R=3)
        vy = 1 if events[0][0] > S0[1] else -1
        H = sum(vh for _, vh in visits)
        hits, sound = 0, 0
        for eps in itertools.product((0, 1), repeat=g + 1):
            uu = G.coset_hollow(it, S0, T, eps, Ld)
            if uu is None:
                continue
            hits += 1
            # recover p from u_1: u_1 = x0 + p*Y_1 - (c_0 + 2 w_0 k_0); solve via sigma-frame x_1
            sig = [1]
            for e in eps: sig.append(sig[-1] * (1 if e == 0 else -1))
            # p from the full u vector: use lattice parametrization through k search near
            p = None
            Phi = Ld['Phi']
            _, x0, u0, _ = G.coset_point(it, S0, T, eps, [0] * (g + 1))
            # find k with u(k)=uu by small search (lattice point is image of some k)
            for k in itertools.product(range(-6, 7), repeat=g + 1):
                if all(u0[i] + sum(Phi[i][j] * k[j] for j in range(g + 1)) == uu[i] for i in range(g)):
                    p, x, _, _ = G.coset_point(it, S0, T, eps, list(k)); break
            if p is None:
                log(f"  (hit not reached by |k|<=6, eps={eps})"); continue
            st, ev, Q = G.trace(V, S0, T, p, vy, H, ys)
            fo, onb = G.follows(it, ev) if st == 'ok' else (False, False)
            ok = st == 'ok' and fo and Q == (T[0], T[1])
            sound += ok
            if not ok:
                log(f"  SOUNDNESS FAIL eps={eps} p={p} st={st}")
        log(f"  g={g} {G.fmt_it(events)} | mu={[str(m) for m in Ld['mu']]} lemma1={Ld['lemma1_in'] and Ld['lemma1_cov']} "
            f"minwidth={mw[0]} ({float(mw[0]):.4f}) l={[str(x) for x in mw[1]]} lit-cosets={hits}/{2**(g+1)} traced-ok={sound}")
    log(f"  cpu {time.process_time() - t0:.2f}s")

if __name__ == "__main__":
    out = []
    def log(s): print(s); out.append(s)
    V7 = [(1, 0), (3, 0), (3, 2), (2, 2), (2, 3), (0, 3), (0, 1), (1, 1)]
    analyse("seven-cell", V7, (1, 2), (2, 1), 4, lambda ev: True, log)
    for (m, u) in [(3, 5), (3, 12), (4, 7), (6, 20), (10, 30)]:
        tiers = [(-1, 0, -2, 1), (0, m, -1, 1), (m, u - 1, 0, m), (u - 1, u, 0, m + 2), (u, u + 1, 0, m + 3)]
        analyse(f"parabola m={m} u={u}", G.room_from_tiers(tiers), (0, 0), (m, u), 4,
                lambda ev, m=m, u=u: [e[0] for e in ev] in ([m, u - 1], [m, u - 1, u, u + 1]), log)
    for (a, t, Bq) in [(1, 1, 1), (1, 1, 18), (1, 2, 3)]:
        b = a + Bq; D = b + a
        tiers = [(-a, 0, 0, 20*t), (0, a, 0, 8*t), (a, b, 7*t, 17*t), (b, D, 16*t, 24*t), (D, D + 3*a, 16*t, 25*t)]
        analyse(f"six-reflex a={a} t={t} B={Bq}", G.room_from_tiers(tiers), (7*t, 0), (20*t, D), 4,
                lambda ev, a=a, b=b, D=D: [e[0] for e in ev] in ([a, b], [a, b, D, D + 3*a]), log)
    open("light.log", "w").write("\n".join(out) + "\n")
