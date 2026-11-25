"""Lattice-only pass (no tracing): Lemma 1 check, covolume, min width, exact
hollowness per parity coset. Remaining named parameter points."""
import itertools, time
import gatebox as G
out = []
def log(s): print(s); out.append(s)
def go(name, V, S0, T, keep):
    t0 = time.process_time()
    for it in G.itineraries(V, S0, T, 4):
        ev = it[1]; g = len(ev)
        if g == 0 or not keep(ev): continue
        Ld = G.lattice_data(it); mw = G.min_width(it, Ld['dual'], R=3)
        lit = sum(G.coset_hollow(it, S0, T, e, Ld) is not None for e in itertools.product((0, 1), repeat=g + 1))
        log(f"{name} g={g} {G.fmt_it(ev)} | lemma1={Ld['lemma1_in'] and Ld['lemma1_cov']} covol={Ld['covol']} "
            f"minwidth={mw[0]} ({float(mw[0]):.4f}) l={[str(x) for x in mw[1]]} lit-cosets={lit}/{2**(g+1)}")
    log(f"  cpu {time.process_time()-t0:.2f}s")
for (m, u) in [(3, 5), (3, 12), (4, 7), (6, 20), (10, 30)]:
    tiers = [(-1, 0, -2, 1), (0, m, -1, 1), (m, u - 1, 0, m), (u - 1, u, 0, m + 2), (u, u + 1, 0, m + 3)]
    go(f"parabola m={m} u={u}", G.room_from_tiers(tiers), (0, 0), (m, u), lambda ev, m=m, u=u: [e[0] for e in ev] == [m, u - 1])
for (a, t, Bq) in [(1, 1, 1), (1, 1, 18), (1, 2, 3)]:
    b = a + Bq; D = b + a
    tiers = [(-a, 0, 0, 20*t), (0, a, 0, 8*t), (a, b, 7*t, 17*t), (b, D, 16*t, 24*t), (D, D + 3*a, 16*t, 25*t)]
    go(f"six-reflex a={a} t={t} B={Bq}", G.room_from_tiers(tiers), (7*t, 0), (20*t, D),
       lambda ev, a=a, b=b, D=D: [e[0] for e in ev] in ([a, b], [a, b, D, D + 3*a]))
open("light2.log", "w").write("\n".join(out) + "\n")
