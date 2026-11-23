// d74 continuum certifier, C++ port of certify.py / geom.py (same algorithm, exact rationals).
// Written from d13 theory.md (Lemma A') only; no code of Astra's checker was read.
// Usage: cert ROOMFILE INDEX B [maxpieces] [tileS tileT]
//   Optional tile restriction (Astra's step 4 idea, re-derived): S restricted to the
//   pieces whose home cell index is tileS (or the closure-sharing pieces assigned to it),
//   T restricted to closed cell tileT.  Not used unless given.
// Output: per direction a progress line; at the end the live pieces with mutual partners.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <unordered_map>
#include <algorithm>
#include <memory>
#include <string>
#include <fstream>
#include <sstream>
#include <ctime>
#include <cmath>
using namespace std;
typedef long long ll;
typedef __int128 LL;

static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }
static LL gcd128(LL a, LL b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { LL t = a % b; a = b; b = t; } return a; }

struct Pt { ll X, Y, d; };   // (X/d, Y/d), d > 0, reduced
static Pt mk(LL X, LL Y, LL d) {
    if (d < 0) { X = -X; Y = -Y; d = -d; }
    LL g = gcd128(gcd128(X, Y), d);
    if (g > 1) { X /= g; Y /= g; d /= g; }
    if (d > (LL)4e15 || X > (LL)4e15 || X < -(LL)4e15 || Y > (LL)4e15 || Y < -(LL)4e15) { fprintf(stderr, "overflow\n"); exit(3); }
    return Pt{(ll)X, (ll)Y, (ll)d};
}
static bool eq(const Pt& a, const Pt& b) { return a.X == b.X && a.Y == b.Y && a.d == b.d; }
static bool ptless(const Pt& a, const Pt& b) {
    LL l = (LL)a.X * b.d, r = (LL)b.X * a.d;
    if (l != r) return l < r;
    return (LL)a.Y * b.d < (LL)b.Y * a.d;
}
struct Line { ll a, b, c; };  // a x + b y = c
// numerator of a x + b y - c at p (sign is the sign of the value, d > 0)
static LL ev(const Line& L, const Pt& p) { return (LL)L.a * p.X + (LL)L.b * p.Y - (LL)L.c * p.d; }
static int sgn(LL v) { return v > 0 ? 1 : (v < 0 ? -1 : 0); }
// intersection of segment P,Q (crossing L strictly) with L
static Pt cross(const Line& L, const Pt& P, const Pt& Q) {
    // line through P,Q: A x + B y = C with A = (Qy - Py), B = (Px - Qx) (scaled by dp*dq)
    LL A = (LL)Q.Y * P.d - (LL)P.Y * Q.d;
    LL B = (LL)P.X * Q.d - (LL)Q.X * P.d;
    // C = A*Px/dp + B*Py/dp ; scale A,B,C by dp
    LL C = A * P.X + B * P.Y;
    LL A2 = A * P.d, B2 = B * P.d;
    LL det = (LL)L.a * B2 - (LL)L.b * A2;
    LL x = (LL)L.c * B2 - (LL)L.b * C;
    LL y = (LL)L.a * C - (LL)L.c * A2;
    // reduce early
    LL g = gcd128(gcd128(x, y), det);
    return mk(x / g, y / g, det / g);
}
typedef vector<Pt> Poly;
// poly ∩ {sense * (a x + b y - c) <= 0}
static Poly clip(const Poly& poly, const Line& L, int sense) {
    int n = poly.size();
    if (!n) return poly;
    vector<int> s(n);
    bool allin = true, allout = true;
    for (int i = 0; i < n; i++) { s[i] = sense * sgn(ev(L, poly[i])); if (s[i] > 0) allin = false; else allout = false; }
    if (allin) return poly;
    if (allout) return Poly();
    Poly out;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        if (s[i] <= 0) out.push_back(poly[i]);
        if ((s[i] < 0 && s[j] > 0) || (s[i] > 0 && s[j] < 0)) out.push_back(cross(L, poly[i], poly[j]));
    }
    Poly ded;
    for (auto& v : out) if (ded.empty() || !eq(ded.back(), v)) ded.push_back(v);
    while (ded.size() > 1 && eq(ded.front(), ded.back())) ded.pop_back();
    return ded;
}
// twice the signed area, as a rational: sign only needed, plus value for stats (double)
static double area2d(const Poly& P) {
    double s = 0; int n = P.size();
    for (int i = 0; i < n; i++) { const Pt& a = P[i]; const Pt& b = P[(i + 1) % n];
        s += ((double)a.X / a.d) * ((double)b.Y / b.d) - ((double)b.X / b.d) * ((double)a.Y / a.d); }
    return s;
}
static bool nondeg(const Poly& P) {  // exact: some triangle fan has nonzero area
    int n = P.size();
    if (n < 3) return false;
    for (int i = 1; i + 1 < n; i++) {
        const Pt &a = P[0], &b = P[i], &c = P[i + 1];
        // (b-a) x (c-a) sign; use common denominators
        LL bx = (LL)b.X * a.d - (LL)a.X * b.d, by = (LL)b.Y * a.d - (LL)a.Y * b.d;   // /(a.d b.d)
        LL cx = (LL)c.X * a.d - (LL)a.X * c.d, cy = (LL)c.Y * a.d - (LL)a.Y * c.d;   // /(a.d c.d)
        // cross = bx*cy - by*cx ; magnitudes ~ (1e3*1e5)^2 = 1e16 ok in int128
        if (bx * cy - by * cx != 0) return true;
    }
    return false;
}

// ---------------------------------------------------------------- room
struct Room {
    set<pair<int, int>> cs;
    vector<pair<int, int>> cells;
    map<pair<int, int>, int> idx;
    bool has(int a, int b) const { return cs.count({a, b}); }
    int around(int x, int y) const { return has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y); }
    bool interiorLattice(int x, int y) const { return around(x, y) == 4; }
};

static ll floordiv(ll a, ll b) { ll q = a / b; if ((a % b != 0) && ((a < 0) != (b < 0))) q--; return q; }

struct Dir {
    const Room* R; int p, q; int ncell;
    // per cell, per fam: lo; bands K in [lo,hi), lines K in (lo,hi)
    vector<int> lo[2], hi[2];
    vector<int> bandBase[2];  // id of band (cell,fam,K) = bandBase[fam][cell] + (K - lo)
    vector<int> label;        // band id -> cylinder root
    vector<char> singular;    // line id -> 1 if singular ; line (cell,fam,K) id = bandBase + (K - lo) (K in (lo,hi)), same indexing
    int nb, ncyl;
    void rng(int a, int b, int fam, int& l, int& h) const {
        if (fam == 0) { l = q * a - p * (b + 1); h = q * (a + 1) - p * b; }
        else { l = q * a + p * b; h = q * (a + 1) + p * (b + 1); }
    }
    // segment (cell, fam, K2); continuation at both ends; returns false if hits corner
    struct Seg { int c, fam; ll K2; };
    void reflect(int fam, ll K2, char axis, ll w, int& nf, ll& nK2) const {
        if (axis == 'v') { nf = 1 - fam; nK2 = 4LL * q * w - K2; }
        else if (fam == 0) { nf = 1; nK2 = K2 + 4LL * p * w; }
        else { nf = 0; nK2 = K2 - 4LL * p * w; }
    }
    bool step(const Seg& s, const Pt& E, int sx, int sy, Seg& out) const {
        int a = R->cells[s.c].first, b = R->cells[s.c].second;
        bool xi = E.d == 1 || (E.X % E.d == 0), yi = (E.Y % E.d == 0);
        ll x = xi ? E.X / E.d : 0, y = yi ? E.Y / E.d : 0;
        int nf; ll nK; pair<int, int> nc;
        pair<int, int> H = {a + sx, b}, V = {a, b + sy}, D = {a + sx, b + sy};
        if (xi && yi) {
            bool h = R->cs.count(H), v = R->cs.count(V), d = R->cs.count(D);
            if (h && v && d) { nc = D; nf = s.fam; nK = s.K2; }
            else if (h && !v && !d) { reflect(s.fam, s.K2, 'h', y, nf, nK); nc = H; }
            else if (v && !h && !d) { reflect(s.fam, s.K2, 'v', x, nf, nK); nc = V; }
            else return false;
        } else if (xi) {
            if (R->cs.count(H)) { nc = H; nf = s.fam; nK = s.K2; }
            else { reflect(s.fam, s.K2, 'v', x, nf, nK); nc = {a, b}; }
        } else {
            if (!yi) { fprintf(stderr, "step: not on edge\n"); exit(4); }
            if (R->cs.count(V)) { nc = V; nf = s.fam; nK = s.K2; }
            else { reflect(s.fam, s.K2, 'h', y, nf, nK); nc = {a, b}; }
        }
        out = Seg{R->idx.at(nc), nf, nK};
        return true;
    }
    void chord(const Seg& s, Pt& A, Pt& B) const {
        int a = R->cells[s.c].first, b = R->cells[s.c].second;
        // k = K2/2.  x-candidates as rationals over 2q
        ll D2 = 2LL * q;
        ll x0n, x1n;  // over D2
        if (s.fam == 0) { x0n = max(2LL * q * a, s.K2 + 2LL * p * b); x1n = min(2LL * q * (a + 1), s.K2 + 2LL * p * (b + 1)); }
        else { x0n = max(2LL * q * a, s.K2 - 2LL * p * (b + 1)); x1n = min(2LL * q * (a + 1), s.K2 - 2LL * p * b); }
        // y = (q x - k)/p  (fam 0)  or (k - q x)/p (fam 1);  x = xn/D2, k = K2/2 = K2*q/D2
        auto Y = [&](ll xn) { LL num = s.fam == 0 ? ((LL)q * xn - (LL)s.K2 * q) : ((LL)s.K2 * q - (LL)q * xn); return num; };  // over D2*p
        A = mk((LL)x0n * p, Y(x0n), (LL)D2 * p);
        B = mk((LL)x1n * p, Y(x1n), (LL)D2 * p);
    }
    bool ends(const Seg& s, Seg out[2]) const {
        Pt A, B; chord(s, A, B);
        int vyUp = s.fam == 0 ? 1 : -1;
        bool ok1 = step(s, B, 1, vyUp, out[0]);
        bool ok2 = step(s, A, -1, -vyUp, out[1]);
        return ok1 && ok2;
    }
    vector<int> par;
    int find(int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; }
    int segid(const Seg& s) const { return bandBase[s.fam][s.c] + (int)((s.K2 - 2LL * lo[s.fam][s.c]) / 2); }
    // band (odd K2) id: bandBase + (K2-1)/2 - lo ; line (even K2) id: bandBase + K2/2 - lo  (separate arrays)
    int bandid(int c, int fam, ll K2) const { return bandBase[fam][c] + (int)((K2 - 1) / 2 - lo[fam][c]); }
    int lineid(int c, int fam, ll K2) const { return bandBase[fam][c] + (int)(K2 / 2 - lo[fam][c]); }

    Dir(const Room* R_, int p_, int q_) : R(R_), p(p_), q(q_) {
        ncell = R->cells.size();
        nb = 0;
        for (int f = 0; f < 2; f++) { lo[f].resize(ncell); hi[f].resize(ncell); bandBase[f].resize(ncell); }
        for (int c = 0; c < ncell; c++) for (int f = 0; f < 2; f++) {
            int l, h; rng(R->cells[c].first, R->cells[c].second, f, l, h);
            lo[f][c] = l; hi[f][c] = h; bandBase[f][c] = nb; nb += h - l;
        }
        // lines: union-find over line ids (K in (lo,hi)) ; bad marks
        par.assign(nb, 0); for (int i = 0; i < nb; i++) par[i] = i;
        vector<char> bad(nb, 0), isline(nb, 0);
        for (int c = 0; c < ncell; c++) for (int f = 0; f < 2; f++)
            for (int K = lo[f][c] + 1; K < hi[f][c]; K++) {
                Seg s{c, f, 2LL * K}; int id = lineid(c, f, s.K2); isline[id] = 1;
                Seg o[2];
                Pt A, B; chord(s, A, B);
                int vyUp = f == 0 ? 1 : -1;
                if (!step(s, B, 1, vyUp, o[0])) bad[id] = 1; else { int j = lineid(o[0].c, o[0].fam, o[0].K2); int a = find(id), b = find(j); if (a != b) par[a] = b; }
                if (!step(s, A, -1, -vyUp, o[1])) bad[id] = 1; else { int j = lineid(o[1].c, o[1].fam, o[1].K2); int a = find(id), b = find(j); if (a != b) par[a] = b; }
            }
        vector<char> badroot(nb, 0);
        for (int i = 0; i < nb; i++) if (isline[i] && bad[i]) badroot[find(i)] = 1;
        singular.assign(nb, 0);
        for (int i = 0; i < nb; i++) if (isline[i] && badroot[find(i)]) singular[i] = 1;
        // bands
        for (int i = 0; i < nb; i++) par[i] = i;
        for (int c = 0; c < ncell; c++) for (int f = 0; f < 2; f++)
            for (int K = lo[f][c]; K < hi[f][c]; K++) {
                Seg s{c, f, 2LL * K + 1}; Seg o[2];
                if (!ends(s, o)) { fprintf(stderr, "band hits corner?\n"); exit(5); }
                int id = bandid(c, f, s.K2);
                for (int e = 0; e < 2; e++) { int j = bandid(o[e].c, o[e].fam, o[e].K2); int a = find(id), b = find(j); if (a != b) par[a] = b; }
            }
        for (int c = 0; c < ncell; c++) for (int f = 0; f < 2; f++)
            for (int K = lo[f][c] + 1; K < hi[f][c]; K++)
                if (!singular[lineid(c, f, 2LL * K)]) {
                    int a = find(bandid(c, f, 2LL * K - 1)), b = find(bandid(c, f, 2LL * K + 1)); if (a != b) par[a] = b;
                }
        label.resize(nb); set<int> roots;
        for (int i = 0; i < nb; i++) { label[i] = find(i); roots.insert(label[i]); }
        ncyl = 0; for (int c = 0; c < ncell; c++) for (int f = 0; f < 2; f++) for (int K = lo[f][c]; K < hi[f][c]; K++) {}
        // count cylinders among bands only: bands occupy all ids (lines share ids), all ids are bands
        ncyl = roots.size();
    }
    // labels at rational point (x,y) interior
    void labelsAt(const Pt& P, int out[2], int& n) const {
        n = 0;
        ll fx = floordiv(P.X, P.d), fy = floordiv(P.Y, P.d);
        for (int fam = 0; fam < 2; fam++) {
            // k = q x -/+ p y = (q X -/+ p Y)/d
            LL kn = fam == 0 ? (LL)q * P.X - (LL)p * P.Y : (LL)q * P.X + (LL)p * P.Y;
            bool found = false;
            for (int i = 0; i < 2 && !found; i++) for (int j = 0; j < 2 && !found; j++) {
                pair<int, int> c = {(int)(fx - i), (int)(fy - j)};
                auto it = R->idx.find(c); if (it == R->idx.end()) continue;
                int ci = it->second;
                // closed cell contains P?
                if ((LL)c.first * P.d > P.X || (LL)(c.first + 1) * P.d < P.X || (LL)c.second * P.d > P.Y || (LL)(c.second + 1) * P.d < P.Y) continue;
                if (!((LL)lo[fam][ci] * P.d < kn && kn < (LL)hi[fam][ci] * P.d)) continue;
                found = true;
                if (kn % P.d != 0) {
                    ll K = floordiv((ll)kn, P.d);
                    int lab = label[bandid(ci, fam, 2 * K + 1)];
                    if (!(n == 1 && out[0] == lab)) out[n++] = lab;
                } else {
                    ll K = (ll)(kn / P.d);
                    if (!singular[lineid(ci, fam, 2 * K)]) {
                        int lab = label[bandid(ci, fam, 2 * K + 1)];
                        if (!(n == 1 && out[0] == lab)) out[n++] = lab;
                    }
                }
            }
            if (!found) { fprintf(stderr, "labelsAt: no cell\n"); exit(6); }
        }
    }
    void singularLines(int c, vector<Line>& out) const {
        for (int f = 0; f < 2; f++) for (int K = lo[f][c] + 1; K < hi[f][c]; K++)
            if (singular[lineid(c, f, 2LL * K)]) out.push_back(f == 0 ? Line{q, -p, K} : Line{q, p, K});
    }
};

// ---------------------------------------------------------------- pieces
struct QP { int c; Poly W; };
typedef shared_ptr<const vector<QP>> QList;
struct Piece { int dim; Poly v; int home; QList Q; };

static Poly square(int a, int b) { return {mk(a, b, 1), mk(a + 1, b, 1), mk(a + 1, b + 1, 1), mk(a, b + 1, 1)}; }

static Pt rep(const Piece& f) {
    if (f.v.size() == 1) return f.v[0];
    if (f.v.size() == 2) { const Pt &a = f.v[0], &b = f.v[1]; return mk((LL)a.X * b.d + (LL)b.X * a.d, (LL)a.Y * b.d + (LL)b.Y * a.d, (LL)2 * a.d * b.d); }
    int n = f.v.size();
    for (int i = 1; i + 1 < n; i++) {
        Poly t = {f.v[0], f.v[i], f.v[i + 1]};
        if (nondeg(t)) {
            const Pt &a = t[0], &b = t[1], &c = t[2];
            LL D = (LL)a.d * b.d * c.d;
            LL X = (LL)a.X * b.d * c.d + (LL)b.X * a.d * c.d + (LL)c.X * a.d * b.d;
            LL Y = (LL)a.Y * b.d * c.d + (LL)b.Y * a.d * c.d + (LL)c.Y * a.d * b.d;
            return mk(X, Y, 3 * D);
        }
    }
    fprintf(stderr, "rep degenerate\n"); exit(7);
}

static bool splitPiece(const Piece& f, const Line& L, vector<Piece>& out) {
    int n = f.v.size();
    vector<int> s(n); bool neg = false, pos = false;
    for (int i = 0; i < n; i++) { s[i] = sgn(ev(L, f.v[i])); if (s[i] < 0) neg = true; if (s[i] > 0) pos = true; }
    if (!(neg && pos)) return false;
    if (f.dim == 2) {
        Poly A = clip(f.v, L, 1), B = clip(f.v, L, -1);
        vector<Pt> ch;
        for (int i = 0; i < n; i++) if (s[i] == 0) ch.push_back(f.v[i]);
        for (int i = 0; i < n; i++) { int j = (i + 1) % n; if ((s[i] < 0 && s[j] > 0) || (s[i] > 0 && s[j] < 0)) ch.push_back(cross(L, f.v[i], f.v[j])); }
        sort(ch.begin(), ch.end(), ptless);
        ch.erase(unique(ch.begin(), ch.end(), eq), ch.end());
        if (ch.size() != 2) { fprintf(stderr, "chord size %zu\n", ch.size()); exit(8); }
        out.push_back(Piece{2, A, f.home, f.Q});
        out.push_back(Piece{2, B, f.home, f.Q});
        out.push_back(Piece{1, ch, f.home, f.Q});
    } else {
        Pt M = cross(L, f.v[0], f.v[1]);
        out.push_back(Piece{1, {f.v[0], M}, f.home, f.Q});
        out.push_back(Piece{1, {M, f.v[1]}, f.home, f.Q});
        out.push_back(Piece{0, {M}, f.home, f.Q});
    }
    return true;
}

static double qarea(const vector<QP>& Q) { double s = 0; for (auto& w : Q) s += fabs(area2d(w.W)) / 2; return s; }

// returns nullptr-equivalent same pointer if unchanged
static QList updateQ(const QList& Q, const Dir& D, const int* lam, int nl, bool& changed) {
    changed = false;
    if (nl == 0) return Q;
    auto out = make_shared<vector<QP>>();
    for (auto& w : *Q) {
        int c = w.c;
        // runs
        vector<pair<int, int>> runs[2];
        bool full = true;
        for (int f = 0; f < 2; f++) {
            int cur = INT32_MIN;
            for (int K = D.lo[f][c]; K < D.hi[f][c]; K++) {
                int lab = D.label[D.bandid(c, f, 2LL * K + 1)];
                bool ok = true; for (int i = 0; i < nl; i++) if (lam[i] == lab) ok = false;
                if (!ok) full = false;
                if (ok && cur == INT32_MIN) cur = K;
                if (!ok && cur != INT32_MIN) { runs[f].push_back({cur, K}); cur = INT32_MIN; }
            }
            if (cur != INT32_MIN) runs[f].push_back({cur, D.hi[f][c]});
        }
        if (full) { out->push_back(w); continue; }
        changed = true;
        for (auto& r : runs[0]) {
            Poly W1 = clip(w.W, Line{D.q, -D.p, r.first}, -1);
            W1 = clip(W1, Line{D.q, -D.p, r.second}, 1);
            if (!nondeg(W1)) continue;
            for (auto& t : runs[1]) {
                Poly W2 = clip(W1, Line{D.q, D.p, t.first}, -1);
                W2 = clip(W2, Line{D.q, D.p, t.second}, 1);
                if (nondeg(W2)) out->push_back(QP{c, W2});
            }
        }
    }
    if (!changed) return Q;
    return out;
}

// ---------------------------------------------------------------- intersection tests (exact)
static bool pointIn(const Pt& p, const Poly& P) {  // P convex ccw (dim 2)
    int n = P.size();
    for (int i = 0; i < n; i++) {
        const Pt &a = P[i], &b = P[(i + 1) % n];
        // line through a,b with outward normal; build integer line
        LL A = (LL)b.Y * a.d - (LL)a.Y * b.d, B = (LL)a.X * b.d - (LL)b.X * a.d;  // scaled by a.d b.d
        // value at p of A x + B y - (A xa + B ya)  => times p.d*a.d
        LL v = A * ((LL)p.X * a.d) + B * ((LL)p.Y * a.d) - (A * a.X + B * a.Y) * p.d;
        if (v > 0) return false;   // ccw: interior has (b-a) x (p-a) >= 0 <=> A x + B y <= ...
    }
    return true;
}
static Line lineThrough(const Pt& a, const Pt& b, int& ok) {
    LL A = (LL)b.Y * a.d - (LL)a.Y * b.d, B = (LL)a.X * b.d - (LL)b.X * a.d;
    LL A2 = A * a.d, B2 = B * a.d, C = A * a.X + B * a.Y;
    LL g = gcd128(gcd128(A2, B2), C);
    if (g == 0) { ok = 0; return Line{0, 0, 0}; }
    A2 /= g; B2 /= g; C /= g;
    ok = (A2 < (LL)4e18 && A2 > -(LL)4e18 && B2 < (LL)4e18 && B2 > -(LL)4e18 && C < (LL)4e18 && C > -(LL)4e18);
    return Line{(ll)A2, (ll)B2, (ll)C};
}
// do closed convex sets G (dim 0..2 vertex list) and W (2-dim ccw polygon) intersect?
static bool meets(const Poly& G, const Poly& W) {
    Poly R = G;
    int n = W.size();
    for (int i = 0; i < n; i++) {
        int ok; Line L = lineThrough(W[i], W[(i + 1) % n], ok);
        if (!ok) { fprintf(stderr, "line overflow\n"); exit(9); }
        // interior side of ccw polygon edge a->b: cross((b-a),(p-a)) >= 0. lineThrough gives A=(by-ay),B=(ax-bx): A x + B y - C = -(cross) ; keep <= 0
        R = clip(R, L, 1);
        if (R.empty()) return false;
    }
    return true;
}
static void bboxd(const Poly& P, double bb[4]) {
    bb[0] = bb[2] = 1e18; bb[1] = bb[3] = -1e18;
    for (auto& v : P) { double x = (double)v.X / v.d, y = (double)v.Y / v.d; bb[0] = min(bb[0], x); bb[1] = max(bb[1], x); bb[2] = min(bb[2], y); bb[3] = max(bb[3], y); }
}

// ---------------------------------------------------------------- main loop
// ---------------------------------------------------------------- d100 tile-pair mode
// Everything above this line is d74's cert.cpp verbatim (labels, clipping, splitting, Q update).
// Below: two-sided tile-pair driver written for d100.
//   Side 0: every piece of int P whose closure lies in closed cell a (open cell, interior open
//   edges, interior lattice corners); Q starts as closed cell b.  Side 1: same with a, b swapped.
//   Soundness: if (S,T) is dark with S in closed a, T in closed b, then S lies in a side-0 piece f
//   with T in UQ(f), and T in a side-1 piece g with S in UQ(g) (Lemma A' invariant). So f and g
//   witness each other in the mutual prune, and survive. Skipping a direction is always sound.
// Usage: cert2 ROOMFILE INDEX B CAP [A B] > out.  (D177: optional A B restricts to one tile pair.)  Prints PAIR and PROD lines.
struct BB { double x0, x1, y0, y1; };
static BB bbOf(const Poly& P) { double b[4]; bboxd(P, b); return BB{b[0] - 1e-9, b[1] + 1e-9, b[2] - 1e-9, b[3] + 1e-9}; }
static bool bbHit(const BB& a, const BB& b) { return a.x0 <= b.x1 && b.x0 <= a.x1 && a.y0 <= b.y1 && b.y0 <= a.y1; }

static vector<Piece> cellPieces(const Room& R, int c, const QList& Q) {
    int a = R.cells[c].first, b = R.cells[c].second;
    vector<Piece> v;
    v.push_back(Piece{2, square(a, b), c, Q});
    if (R.has(a + 1, b)) v.push_back(Piece{1, {mk(a + 1, b, 1), mk(a + 1, b + 1, 1)}, c, Q});
    if (R.has(a - 1, b)) v.push_back(Piece{1, {mk(a, b, 1), mk(a, b + 1, 1)}, c, Q});
    if (R.has(a, b + 1)) v.push_back(Piece{1, {mk(a, b + 1, 1), mk(a + 1, b + 1, 1)}, c, Q});
    if (R.has(a, b - 1)) v.push_back(Piece{1, {mk(a, b, 1), mk(a + 1, b, 1)}, c, Q});
    for (int dx = 0; dx < 2; dx++) for (int dy = 0; dy < 2; dy++)
        if (R.interiorLattice(a + dx, b + dy)) v.push_back(Piece{0, {mk(a + dx, b + dy, 1)}, c, Q});
    return v;
}

static bool step1(const Dir& D, vector<Piece>& pieces) {  // one direction on one side; returns any change
    vector<Piece> out; out.reserve(pieces.size() * 2); bool chg = false;
    for (auto& f : pieces) {
        vector<Line> lines;
        if (f.dim > 0) D.singularLines(f.home, lines);
        vector<Piece> parts = {f};
        for (auto& L : lines) {
            vector<Piece> nxt;
            for (auto& g : parts) if (!splitPiece(g, L, nxt)) nxt.push_back(g);
            parts.swap(nxt);
        }
        vector<QList> nq; bool any = false;
        for (auto& g : parts) {
            int lam[2], nl; D.labelsAt(rep(g), lam, nl);
            bool ch; QList Q2 = updateQ(g.Q, D, lam, nl, ch);
            if (ch) any = true;
            nq.push_back(Q2);
        }
        if (!any) { out.push_back(f); continue; }
        chg = true;
        for (size_t i = 0; i < parts.size(); i++) if (!nq[i]->empty()) { parts[i].Q = nq[i]; out.push_back(parts[i]); }
    }
    pieces.swap(out);
    return chg;
}

struct Info { BB pb, qb; vector<BB> wb; };
static Info info(const Piece& f) {
    Info I; I.pb = bbOf(f.v); I.qb = BB{1e18, -1e18, 1e18, -1e18};
    for (auto& w : *f.Q) { BB b = bbOf(w.W); I.wb.push_back(b); I.qb = BB{min(I.qb.x0, b.x0), max(I.qb.x1, b.x1), min(I.qb.y0, b.y0), max(I.qb.y1, b.y1)}; }
    return I;
}
// closure(g) meets UQ(f)
static bool hitQ(const Piece& f, const Info& fi, const Piece& g, const Info& gi) {
    if (!bbHit(fi.qb, gi.pb)) return false;
    for (size_t k = 0; k < f.Q->size(); k++) if (bbHit(fi.wb[k], gi.pb) && meets(g.v, (*f.Q)[k].W)) return true;
    return false;
}
static bool samePoint(const Piece& f, const Piece& g) { return f.dim == 0 && g.dim == 0 && eq(f.v[0], g.v[0]); }

static void prune(vector<Piece> side[2]) {
    vector<Info> I[2];
    for (int s = 0; s < 2; s++) for (auto& f : side[s]) I[s].push_back(info(f));
    vector<char> alive[2] = {vector<char>(side[0].size(), 1), vector<char>(side[1].size(), 1)};
    for (bool killed = true; killed;) {
        killed = false;
        for (int s = 0; s < 2; s++) for (size_t i = 0; i < side[s].size(); i++) if (alive[s][i]) {
            bool ok = false;
            for (size_t j = 0; j < side[1 - s].size() && !ok; j++) if (alive[1 - s][j]) {
                const Piece &f = side[s][i], &g = side[1 - s][j];
                if (samePoint(f, g)) continue;
                if (hitQ(f, I[s][i], g, I[1 - s][j]) && hitQ(g, I[1 - s][j], f, I[s][i])) ok = true;
            }
            if (!ok) { alive[s][i] = 0; killed = true; }
        }
    }
    for (int s = 0; s < 2; s++) { vector<Piece> o; for (size_t i = 0; i < side[s].size(); i++) if (alive[s][i]) o.push_back(side[s][i]); side[s].swap(o); }
}

static void pr(const Poly& P) { for (auto& v : P) printf(" %lld %lld %lld", v.X, v.Y, v.d); }

int main(int argc, char** argv) {
    if (argc < 5) { fprintf(stderr, "usage: cert2 ROOMFILE INDEX B CAP\n"); return 1; }
    Room R;
    {
        ifstream in(argv[1]); string line; int want = atoi(argv[2]), k = 0; bool got = false;
        while (getline(in, line)) {
            istringstream ss(line); int a, w; if (!(ss >> a >> w)) continue;
            if (k++ != want) continue;
            for (int i = 0; i < a; i++) { int x, y; ss >> x >> y; R.cs.insert({x, y}); }
            got = true; break;
        }
        if (!got) { fprintf(stderr, "no room\n"); return 1; }
        for (auto& c : R.cs) { R.idx[c] = R.cells.size(); R.cells.push_back(c); }
    }
    int B = atoi(argv[3]); size_t cap = atol(argv[4]);
    int onlyA = argc > 6 ? atoi(argv[5]) : -1, onlyB = argc > 6 ? atoi(argv[6]) : -1;  // D177
    vector<pair<int, int>> ds;
    for (int m = 1; m <= B; m++) for (int p = 1; p <= m; p++) for (int q = 1; q <= m; q++)
        if (max(p, q) == m && gcdll(p, q) == 1) ds.push_back({p, q});
    stable_sort(ds.begin(), ds.end(), [](pair<int, int> a, pair<int, int> b) { int ma = max(a.first, a.second), mb = max(b.first, b.second); if (ma != mb) return ma < mb; return a.first + a.second < b.first + b.second; });
    vector<unique_ptr<Dir>> dirs;
    for (auto& d : ds) dirs.emplace_back(new Dir(&R, d.first, d.second));
    int n = R.cells.size(), open = 0; long prods = 0;
    clock_t t0 = clock();
    for (int a = 0; a < n; a++) for (int b = a; b < n; b++) {
        if (onlyA >= 0 && (a != onlyA || b != onlyB)) continue;  // D177: one tile pair only
        vector<Piece> side[2];
        for (int s = 0; s < 2; s++) {
            int src = s ? b : a, tgt = s ? a : b;
            auto Q0 = make_shared<vector<QP>>(); Q0->push_back(QP{tgt, square(R.cells[tgt].first, R.cells[tgt].second)});
            side[s] = cellPieces(R, src, Q0);
        }
        int skipped = 0, used = 0;
        for (auto& D : dirs) {
            vector<Piece> keep[2] = {side[0], side[1]};
            bool chg = false;
            for (int s = 0; s < 2; s++) chg |= step1(*D, side[s]);
            if (!chg) continue;
            prune(side);
            if (side[0].size() > cap || side[1].size() > cap) { side[0].swap(keep[0]); side[1].swap(keep[1]); skipped++; continue; }
            used++;
            if (side[0].empty() || side[1].empty()) break;
        }
        prune(side);
        size_t np = 0;
        if (!side[0].empty()) {
            open++;
            vector<Info> I[2];
            for (int s = 0; s < 2; s++) for (auto& f : side[s]) I[s].push_back(info(f));
            for (int s = 0; s < 2; s++) for (size_t i = 0; i < side[s].size(); i++) {
                const Piece& f = side[s][i];
                for (size_t k = 0; k < f.Q->size(); k++) {
                    const Poly& W = (*f.Q)[k].W; bool keepW = false;
                    for (size_t j = 0; j < side[1 - s].size() && !keepW; j++) {
                        const Piece& g = side[1 - s][j];
                        if (samePoint(f, g) || !bbHit(I[s][i].wb[k], I[1 - s][j].pb)) continue;
                        if (meets(g.v, W) && hitQ(g, I[1 - s][j], f, I[s][i])) keepW = true;
                    }
                    if (!keepW) continue;
                    np++;
                    printf("PROD %d %d %d |", a, b, s ? b : a); pr(f.v); printf(" |"); pr(W); printf("\n");
                }
            }
        }
        prods += np;
        printf("PAIR %d %d live %zu %zu prods %zu dirs_used %d skipped %d cpu %.1f\n", a, b, side[0].size(), side[1].size(), np, used, skipped, (double)(clock() - t0) / CLOCKS_PER_SEC);
        fflush(stdout);
    }
    printf("DONE open_pairs %d products %ld cpu %.1f\n", open, prods, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
