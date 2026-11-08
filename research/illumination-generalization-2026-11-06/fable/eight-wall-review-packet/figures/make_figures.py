#!/usr/bin/env python3
"""Draw the six normal forms and one exact example path per eight-wall class.

Every path is built by evaluating the formulas of theorem-and-proof.md with
exact rational arithmetic, then verified by an independent exact checker
(segment interiority, wall contact, reflection law, corner avoidance). The
script writes SVG files and paths.json next to itself. No search is used.
Run: python3 -I make_figures.py
"""
from fractions import Fraction as Fr
from math import floor
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


# ---------- exact geometry helpers ----------
def F(z, l):
    """Even triangular wave of period 2l with F(z)=|z| on [-l,l]."""
    r = z % (2 * l)
    return r if r <= l else 2 * l - r


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def on_closed_segment(p, a, b):
    return cross(sub(b, a), sub(p, a)) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def strictly_inside(poly, p):
    """Ray casting; returns False for boundary points."""
    edges = list(zip(poly, poly[1:] + poly[:1]))
    if any(on_closed_segment(p, a, b) for a, b in edges):
        return False
    inside = False
    x, y = p
    for a, b in edges:
        if (a[1] > y) != (b[1] > y):
            xx = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < xx:
                inside = not inside
    return inside


def open_segment_hits_edge(p, q, a, b):
    """True if the open segment (p,q) meets the closed edge [a,b]."""
    d = sub(q, p)
    e = sub(b, a)
    den = cross(d, e)
    if den == 0:
        if cross(sub(a, p), d) != 0:
            return False  # parallel, not collinear
        # collinear: overlap of the open (p,q) with closed [a,b]
        dd = d[0] * d[0] + d[1] * d[1]
        ta = ((a[0] - p[0]) * d[0] + (a[1] - p[1]) * d[1]) / dd
        tb = ((b[0] - p[0]) * d[0] + (b[1] - p[1]) * d[1]) / dd
        lo, hi = min(ta, tb), max(ta, tb)
        return hi > 0 and lo < 1
    t = cross(sub(a, p), e) / den
    s = cross(sub(a, p), d) / den
    return 0 < t < 1 and 0 <= s <= 1


def verify(poly, path):
    """Exact check of a specular path. Returns number of checks performed."""
    poly = [(Fr(x), Fr(y)) for x, y in poly]
    path = [(Fr(x), Fr(y)) for x, y in path]
    edges = list(zip(poly, poly[1:] + poly[:1]))
    checks = 0
    assert strictly_inside(poly, path[0]) and strictly_inside(poly, path[-1])
    assert path[0] != path[-1]
    checks += 2
    for i, p in enumerate(path[1:-1], 1):
        host = [(a, b) for a, b in edges if on_closed_segment(p, a, b)]
        assert len(host) == 1, ("contact not on exactly one wall", p, host)
        a, b = host[0]
        assert p != a and p != b, ("corner contact", p)
        din = sub(p, path[i - 1])
        dout = sub(path[i + 1], p)
        refl = (-din[0], din[1]) if a[0] == b[0] else (din[0], -din[1])
        assert cross(dout, refl) == 0 and dout[0] * refl[0] + dout[1] * refl[1] > 0, ("reflection law", p)
        checks += 3
    for p, q in zip(path, path[1:]):
        assert p != q
        for a, b in edges:
            assert not open_segment_hits_edge(p, q, a, b), ("segment meets wall", p, q, a, b)
            checks += 1
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        assert strictly_inside(poly, mid)
        checks += 1
    return checks


def fold_events(x0, tau, y0, y1, width, phys):
    """Contacts of x=phys(F_width(x0+tau*(y-y0))) for y in (y0,y1). phys maps a
    developed value in [0,width] to the physical x. Returns [(y, x)]."""
    out = []
    lo = x0 + tau * (y0 - y0)
    hi = x0 + tau * (y1 - y0)
    jlo, jhi = floor(min(lo, hi) / width) - 1, floor(max(lo, hi) / width) + 2
    for j in range(jlo, jhi + 1):
        if tau == 0:
            break
        y = y0 + (j * width - x0) / tau
        if y0 < y < y1:
            out.append((y, phys(F(j * width, width))))
    return sorted(out)


# ---------- constructions ----------
def l_vertical_only(A, a, c, C, s, t):
    """Theorem 2.1: vertical-only path in the L ([0,A]x[0,c]) U ([0,a]x[c,C])."""
    xs, ys = s
    xt, yt = t
    assert a < xs < A and 0 < ys < c and 0 < xt < a and c < yt < C
    r = (yt - c) / (c - ys)
    h = -r * xs
    cands = []
    for e in (1, -1):
        m0 = floor((h - e * xt) / (2 * a))
        for m in (m0 - 1, m0, m0 + 1, m0 + 2):
            x = e * xt + 2 * m * a
            if 0 < abs(x - h) <= a:
                cands.append((abs(x - h), x))
    x = min(cands)[1]
    Xs, Xt = (xs, x) if x > h else (-xs, -x)
    q = (r * Xs + Xt) / (1 + r)
    assert 0 < q < a
    tau = (Xt - Xs) / (yt - ys)  # developed dx/dy
    path = [s]
    if Xs < 0:
        path.append((Fr(0), ys + (c - ys) * xs / (xs + q)))
    for y, x in fold_events(q, tau, c, yt, a, lambda v: v):
        path.append((x, y))
    path.append(t)
    return path


def u_opposite(a, b, M, c, HL, HR, s, t):
    """Theorem 3.1 in the U room; s in left arm, t=(a+M+xt,yt) in right arm."""
    A = a + M + b
    xs, ys = s
    xt, yt = t[0] - a - M, t[1]

    def first(thr, base, period):
        n = max(0, floor((thr - base) / period) + 1)
        return base + n * period, n

    tau0 = 2 * max(a, b) / c + 1
    k = max(0, floor((2 * c * tau0 - M) / (2 * A)) + 1)
    B = M + 2 * k * A
    Sg = ys + yt
    tau = tau0
    while True:
        L, n = first((ys - c) * tau, a - xs, 2 * a)
        R, m = first((yt - c) * tau, xt, 2 * b)
        nt = (L + R + B) / Sg
        if nt == tau:
            break
        assert nt > tau
        tau = nt
    ls, lt = L - (ys - c) * tau, R - (yt - c) * tau
    assert 0 < ls < 2 * a and 0 < lt < 2 * b
    u, v = c - ls / tau, c - lt / tau
    assert 0 < u < c and 0 < v < c and u + v == B / tau
    path = [s]
    # left arm: developed from xs rightward distance L, height drops 1/tau per unit
    for j in range(1, 2 * n + 1):
        dd = j * a - xs
        path.append((a if j % 2 else Fr(0), ys - dd / tau))
    # strip: developed X=a+d, Y=u-d/tau
    ev = []
    for j in range(1, 2 * k + 1):
        dd = j * A - a
        ev.append((dd, F(j * A, A), abs(u - dd / tau)))
    ev.append((u * tau, F(a + u * tau, A), Fr(0)))
    for dd, px, py in sorted(ev):
        path.append((px, py))
    # right arm: from (a+M, v) rightward developed distance R
    for j in range(1, 2 * m + 1):  # developed distance j*b from the right portal
        path.append((a + M + b if j % 2 else a + M, v + j * b / tau))
    path.append(t)
    return path, dict(k=k, tau=str(tau), u=str(u), v=str(v))


def wide_middle_opposite(a, B, A, b, c, C, S, T):
    """Theorem 5.1 (assumes B>=W=A-a; otherwise the caller rotates)."""
    W = A - a
    g = c - b
    xs, ys = S
    xt, yt = T
    assert B >= W
    Hs, Ht = b - ys, yt - c
    D = Hs + g + Ht
    k = 0
    while (Hs * (2 * k + 1) * A + g * xs) / (2 * B * g) < 1:
        k += 1
    K = (2 * k + 1) * A
    n = floor((Hs * K + g * xs) / (2 * B * g) + Fr(1, 2))
    Y = A - xt
    Zlo = xs + D * (2 * n * B + K - xs - W) / (Hs + g) - 2 * n * B - K
    m = floor((Zlo - Y) / (2 * W)) + 1
    tau = (2 * n * B + K + Y + 2 * m * W - xs) / D
    z = xs + Hs * tau - 2 * n * B
    w = xs + (Hs + g) * tau - 2 * n * B - K
    assert abs(z) < B and abs(w) < W
    path = [S]
    path += [(x, y) for y, x in fold_events(xs, tau, ys, b, B, lambda v: v)]
    path += [(x, y) for y, x in fold_events(z, tau, b, c, A, lambda v: v)]
    path += [(x, y) for y, x in fold_events(w, tau, c, yt, W, lambda v: A - v)]
    path.append(T)
    return path, dict(k=k, n=n, tau=str(tau), z=str(z), w=str(w))


def staircase_floor(A, b, a, c, d, H, S, T):
    """Theorem 6.5 under F: reflected source, two images, floor corner avoided."""
    xs, ys = S
    xt, yt = T
    g = d - c
    assert (A - b) * g <= c * (b - a)
    Hs = c + ys
    Ht = yt - d
    D = Hs + g + Ht
    k = 1 + floor(A * g / (b * Hs)) + 1
    K = 2 * k * b
    n = floor((Hs * K + g * xs) / (2 * A * g) + Fr(1, 2))
    assert n >= 1
    Zlo = xs + D * (2 * n * A + K - xs - a) / (Hs + g) - 2 * n * A - K
    imgs = sorted(set(e * xt + 2 * m * a for e in (1, -1) for m in range(floor((Zlo - a) / (2 * a)) - 1, floor((Zlo + 3 * a) / (2 * a)) + 2)))
    above = [y for y in imgs if y > Zlo]
    Y1, Y2 = above[0], above[1]
    chosen = None
    for Y in (Y1, Y2):
        tau = (2 * n * A + K + Y - xs) / D
        if (xs + ys * tau) % A != 0:
            chosen = (Y, tau)
            break
    Y, tau = chosen
    z = xs + Hs * tau - 2 * n * A
    w = xs + (Hs + g) * tau - 2 * n * A - K
    assert abs(z) < b and abs(w) < a
    path = [S]
    # descending part: developed q from -ys to 0, x=F_A(xs+tau*(q+ys)), y=|q|
    ev = [(q, x) for q, x in fold_events(xs, tau, -ys, c, A, lambda v: v)]
    for q, x in ev:
        if q < 0:
            path.append((x, -q))
    path.append((F(xs + ys * tau, A), Fr(0)))
    for q, x in ev:
        if q > 0:
            path.append((x, q))
    path += [(x, y) for y, x in fold_events(z, tau, c, d, b, lambda v: v)]
    path += [(x, y) for y, x in fold_events(w, tau, d, yt, a, lambda v: v)]
    path.append(T)
    return path, dict(k=k, n=n, tau=str(tau), images=[str(Y1), str(Y2)], used=str(Y))


def staircase_roof(A, b, a, c, d, H, S, T, image_index=0):
    """Theorem 6.8 under Rv. image_index selects which admissible target image
    inside the window is used (0 = lowest). Returns the path and whether the
    earlier-arrival truncation of Step 4 was used."""
    xs, ys = S
    xt, yt = T
    g, h = d - c, H - d
    Qv = min(Fr(2), 1 + b * g / (a * c))
    assert H * Qv >= 2 * d, "Rv fails"
    Hs, Ht = c - ys, yt - d
    T0 = Hs + g
    v = 2 * h - Ht
    D = T0 + v
    theta = (2 * A - xs) / Hs
    K = 2 * b * floor(g * theta / (2 * b) + Fr(1, 2))
    R = b * T0 / Hs
    Ulo, Uhi = max(g * theta - R, K - a), min(g * theta + R, K + a)
    assert Uhi - Ulo > a
    Zlo, Zhi = xs + D * (Ulo + 2 * A - xs) / T0 - 2 * A - K, xs + D * (Uhi + 2 * A - xs) / T0 - 2 * A - K
    assert Zhi - Zlo > 2 * a
    imgs = sorted(set(e * xt + 2 * m * a for e in (1, -1) for m in range(floor(Zlo / (2 * a)) - 2, floor(Zhi / (2 * a)) + 3)))
    inside = [Y for Y in imgs if Zlo < Y < Zhi]
    Y = inside[image_index]
    tau = (2 * A + K + Y - xs) / D
    z = xs + Hs * tau - 2 * A
    w = xs + T0 * tau - 2 * A - K
    assert abs(z) < b and abs(w) < a
    Beta = w + tau * h
    path = [S]
    path += [(x, y) for y, x in fold_events(xs, tau, ys, c, A, lambda q: q)]
    path += [(x, y) for y, x in fold_events(z, tau, c, d, b, lambda q: q)]
    truncated = (Beta % a == 0)
    if truncated:
        assert F(w + tau * Ht, a) == xt
        if Ht > 0:
            path += [(x, y) for y, x in fold_events(w, tau, d, yt, a, lambda q: q)]
    else:
        path += [(x, y) for y, x in fold_events(w, tau, d, H, a, lambda q: q)]
        path.append((F(Beta, a), H))
        # descending leg: eta in (d+h, d+v), y = 2H - d - (eta - d)... use developed eta
        for eta, x in fold_events(w, tau, d, d + v, a, lambda q: q):
            if eta > d + h:
                path.append((x, 2 * H - d - (eta - d)))
    path.append(T)
    return path, dict(tau=str(tau), K=str(K), z=str(z), w=str(w), Beta=str(Beta), truncated=truncated, images_in_window=len(inside))


# ---------- SVG ----------
def svg_room(poly, paths, title, fname, labels=(), width=420):
    xs_ = [float(p[0]) for p in poly]
    ys_ = [float(p[1]) for p in poly]
    W, Hh = max(xs_) - min(xs_), max(ys_) - min(ys_)
    sc = (width - 40) / max(W, Hh)
    height = Hh * sc + 60

    def P(p):
        return f"{20 + (float(p[0]) - min(xs_)) * sc:.2f},{height - 30 - (float(p[1]) - min(ys_)) * sc:.2f}"

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height:.0f}" font-family="Helvetica,Arial" font-size="11">',
           f'<text x="20" y="16" font-size="13">{title}</text>',
           f'<polygon points="{" ".join(P(p) for p in poly)}" fill="#f4f4f4" stroke="#222" stroke-width="2"/>']
    for p in poly:
        out.append(f'<circle cx="{P(p).split(",")[0]}" cy="{P(p).split(",")[1]}" r="2.5" fill="#222"/>')
    colors = ["#1f5fbf", "#c23b22", "#2a8a3c"]
    for i, (path, name) in enumerate(paths):
        col = colors[i % 3]
        out.append(f'<polyline points="{" ".join(P(p) for p in path)}" fill="none" stroke="{col}" stroke-width="1.4"/>')
        for p in path[1:-1]:
            cx, cy = P(p).split(",")
            out.append(f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{col}"/>')
        for p, lab in ((path[0], "S"), (path[-1], "T")):
            cx, cy = P(p).split(",")
            out.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{col}" stroke="#fff"/>')
            out.append(f'<text x="{float(cx) + 5:.1f}" y="{float(cy) - 5:.1f}" fill="{col}">{lab}</text>')
        out.append(f'<text x="20" y="{height - 10 + 0:.0f}" fill="{col}">{name}</text>')
    for p, lab in labels:
        cx, cy = P(p).split(",")
        out.append(f'<text x="{float(cx) + 3:.1f}" y="{float(cy) - 3:.1f}" fill="#555" font-size="10">{lab}</text>')
    out.append("</svg>")
    (HERE / fname).write_text("\n".join(out) + "\n")


def main():
    results = {}

    # --- L ---
    A, a, c, C = Fr(4), Fr(3, 2), Fr(1), Fr(3)
    polyL = [(0, 0), (A, 0), (A, c), (a, c), (a, C), (0, C)]
    s, t = (Fr(3), Fr(1, 2)), (Fr(1, 2), Fr(5, 2))
    pL = l_vertical_only(A, a, c, C, s, t)
    results["L-vertical-only"] = dict(room=dict(A=4, a="3/2", c=1, C=3), S=["3", "1/2"], T=["1/2", "5/2"], reflections=len(pL) - 2, checks=verify(polyL, pL), path=[[str(x), str(y)] for x, y in pL])
    svg_room(polyL, [(pL, "Theorem 2.1 vertical-only path")], "L room (W=6)", "fig-L.svg")

    # --- U ---
    a, b, M, c, HL, HR = Fr(1), Fr(3), Fr(2), Fr(1, 2), Fr(2), Fr(4)
    A = a + M + b
    polyU = [(0, 0), (A, 0), (A, HR), (a + M, HR), (a + M, c), (a, c), (a, HL), (0, HL)]
    s, t = (Fr(1, 7), Fr(3, 2)), (a + M + Fr(11, 4), Fr(7, 2))
    pU, infoU = u_opposite(a, b, M, c, HL, HR, s, t)
    results["U-opposite-arms"] = dict(room=dict(a=1, b=3, M=2, c="1/2", H_L=2, H_R=4), S=[str(s[0]), str(s[1])], T=[str(t[0]), str(t[1])], reflections=len(pU) - 2, checks=verify(polyU, pU), **infoU)
    svg_room(polyU, [(pU, f"Theorem 3.1 path, {len(pU) - 2} reflections, one floor contact")], "U room (k=1)", "fig-U.svg")

    # --- T (independent floors): opposite wings via L subroom Q ---
    a, b, A, u, v, C = Fr(4), Fr(5), Fr(10), Fr(1), Fr(2), Fr(4)
    polyT = [(a, 0), (b, 0), (b, v), (A, v), (A, C), (0, C), (0, u), (a, u)]
    S, T = (Fr(1, 2), Fr(11, 10)), (Fr(9), Fr(21, 10))
    # Q = ([0,A]x[v,C]) U ([0,b]x[u,v]); map y -> C - y gives L with A'=A, c'=C-v, a'=b, C'=C-u.
    # In that L the source must be in the wide lower part: T' = (9, C-21/10) is lower-right, S' upper-left.
    Sp, Tp = (T[0], C - T[1]), (S[0], C - S[1])
    pLq = l_vertical_only(A, b, C - v, C - u, Sp, Tp)
    pT = [(x, C - y) for x, y in pLq][::-1]
    results["T-opposite-wings"] = dict(room=dict(a=4, b=5, A=10, u=1, v=2, C=4), S=["1/2", "11/10"], T=["9", "21/10"], reflections=len(pT) - 2, checks=verify(polyT, pT), path=[[str(x), str(y)] for x, y in pT])
    svg_room(polyT, [(pT, "Theorem 4.1 opposite wings: vertical-only path in Q")], "T room with u<v (k=3)", "fig-T.svg")

    # --- wide-middle with separated arms a > B ---
    a, B, A, b, c, C = Fr(3), Fr(2), Fr(6), Fr(1), Fr(2), Fr(4)
    polyWM = [(0, 0), (B, 0), (B, b), (A, b), (A, C), (a, C), (a, c), (0, c)]
    S, T = (Fr(1), Fr(1, 2)), (Fr(5), Fr(3))
    W = A - a
    if B >= W:
        pWM, infoWM = wide_middle_opposite(a, B, A, b, c, C, S, T)
    else:  # rotate by 180 degrees about (A/2, C/2), exchange marks, map back
        rot = lambda p: (A - p[0], C - p[1])
        pR, infoWM = wide_middle_opposite(A - B, W, A, C - c, C - b, C, rot(T), rot(S))
        pWM = [rot(p) for p in pR][::-1]
        infoWM["rotated"] = True
    results["wide-middle-opposite-arms"] = dict(room=dict(a=3, B=2, A=6, b=1, c=2, C=4), S=["1", "1/2"], T=["5", "3"], reflections=len(pWM) - 2, checks=verify(polyWM, pWM), **infoWM)
    svg_room(polyWM, [(pWM, "Theorem 5.1 three-piece path (arms separated, a>B)")], "Wide-middle offset corridor (k=4)", "fig-wide-middle.svg")

    # --- staircase floor chart under F ---
    A, b, a, c, d, H = Fr(6), Fr(4), Fr(3), Fr(3), Fr(4), Fr(6)
    polySF = [(0, 0), (A, 0), (A, c), (b, c), (b, d), (a, d), (a, H), (0, H)]
    S, T = (Fr(5), Fr(1)), (Fr(1), Fr(5))
    pSF, infoSF = staircase_floor(A, b, a, c, d, H, S, T)
    results["staircase-floor-F"] = dict(room=dict(A=6, b=4, a=3, c=3, d=4, H=6), S=["5", "1"], T=["1", "5"], reflections=len(pSF) - 2, checks=verify(polySF, pSF), **infoSF)
    svg_room(polySF, [(pSF, "Theorem 6.5 floor chart (condition F)")], "Staircase (k=2), floor chart", "fig-staircase-floor.svg")

    # --- staircase roof chart under Rv: generic image and the roof-corner truncation ---
    A, b, a, c, d, H = Fr(8), Fr(4), Fr(3), Fr(3), Fr(4), Fr(8)
    polySR = [(0, 0), (A, 0), (A, c), (b, c), (b, d), (a, d), (a, H), (0, H)]
    S, T = (Fr(7), Fr(1)), (Fr(9, 7), Fr(5))
    pSR0, info0 = staircase_roof(A, b, a, c, d, H, S, T, 0)
    assert not info0["truncated"]
    # find the admissible image whose roof coordinate Beta is a multiple of a (Step 4 case)
    trunc = None
    for idx in range(info0["images_in_window"]):
        p, inf = staircase_roof(A, b, a, c, d, H, S, T, idx)
        if inf["truncated"]:
            trunc = (p, inf)
            break
    assert trunc is not None
    pSR1, info1 = trunc
    results["staircase-roof-Rv-generic"] = dict(room=dict(A=8, b=4, a=3, c=3, d=4, H=8), S=["7", "1"], T=["9/7", "5"], reflections=len(pSR0) - 2, checks=verify(polySR, pSR0), **info0)
    results["staircase-roof-Rv-earlier-arrival"] = dict(room=dict(A=8, b=4, a=3, c=3, d=4, H=8), S=["7", "1"], T=["9/7", "5"], reflections=len(pSR1) - 2, checks=verify(polySR, pSR1), **info1)
    svg_room(polySR, [(pSR0, f"Theorem 6.8, generic image: one roof contact (tau={info0['tau']})"),
                      (pSR1, f"Step 4: Beta={info1['Beta']} in aZ, T reached before the roof (tau={info1['tau']})")],
             "Staircase (k=2), roof chart under Rv", "fig-staircase-roof.svg", width=460)

    # --- overview of normal forms ---
    forms = [("Rectangle W=4", [(0, 0), (3, 0), (3, 2), (0, 2)]),
             ("L W=6", [(0, 0), (3, 0), (3, 1), (1, 1), (1, 2.5), (0, 2.5)]),
             ("U k=1", [(0, 0), (4, 0), (4, 2.6), (2.8, 2.6), (2.8, 0.8), (1, 0.8), (1, 2), (0, 2)]),
             ("Staircase k=2", [(0, 0), (4, 0), (4, 1), (2.5, 1), (2.5, 2), (1.2, 2), (1.2, 3), (0, 3)]),
             ("T k=3 (u<v)", [(1.2, 0), (2, 0), (2, 1.2), (4, 1.2), (4, 2.5), (0, 2.5), (0, 0.6), (1.2, 0.6)]),
             ("Wide middle k=4 (a>B)", [(0, 0), (1.3, 0), (1.3, 1), (4, 1), (4, 2.6), (2.2, 2.6), (2.2, 1.8), (0, 1.8)])]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="380" font-family="Helvetica,Arial" font-size="12">',
           '<text x="10" y="18" font-size="14">Normal forms of strictly simple orthogonal rooms with at most eight walls (Proposition 1.2)</text>']
    for i, (name, poly) in enumerate(forms):
        ox, oy = 20 + (i % 3) * 290, 60 + (i // 3) * 160
        sc = 40
        pts = " ".join(f"{ox + x * sc:.1f},{oy + 120 - y * sc:.1f}" for x, y in poly)
        out.append(f'<polygon points="{pts}" fill="#f4f4f4" stroke="#222" stroke-width="2"/>')
        for j, (x, y) in enumerate(poly):
            nxt, prv = poly[(j + 1) % len(poly)], poly[j - 1]
            turn = (nxt[0] - x) * (prv[1] - y) - (nxt[1] - y) * (prv[0] - x)
            col = "#c23b22" if turn > 0 else "#222"
            out.append(f'<circle cx="{ox + x * sc:.1f}" cy="{oy + 120 - y * sc:.1f}" r="3" fill="{col}"/>')
        out.append(f'<text x="{ox}" y="{oy + 145}">{name}</text>')
    out.append('<text x="10" y="370" fill="#555">Red dots mark reflex corners. k is the shorter cyclic edge distance between the two reflex corners.</text></svg>')
    (HERE / "fig-normal-forms.svg").write_text("\n".join(out) + "\n")

    (HERE / "paths.json").write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "path"} for k, v in results.items()}, indent=1))


if __name__ == "__main__":
    main()
