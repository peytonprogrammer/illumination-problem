# Reflex-corner review and a restricted sector-density argument

[done] Reviewed Opus's Lemma 22/Corollary 23 and supplied an endpoint correction. [done] Opus independently accepted the restricted sector-density proof on 2026-11-01 and recorded it as Theorem 24. No billiard rays, new rooms or geodesic orbit catalogue were computed.

## Shadow formula: accepted, with one endpoint correction

Measure angles in units of pi for the algebra. Let 1<alpha<2, 0<=phi<=alpha, and 0<psi<alpha. The union of the image tests

    |psi−(±phi+2j alpha)|<1

is exactly the direct-image test |psi−phi|<1.

The image −phi can add only points with psi+phi<1, which already satisfy |psi−phi|<1. The image 2alpha−phi can add only points with phi+psi>2alpha−1. Because phi,psi<=alpha, this implies |psi−phi|<=2alpha−(phi+psi)<1, so those points are already covered too. All remaining images have distance at least alpha>1 from the open physical sector. Thus the shadow is exactly Opus's stated set:

- (0,phi−1] if phi>1;
- [phi+1,alpha) if phi<alpha−1;
- empty otherwise.

But its length is **at most** alpha−1, not always strictly less. The setting permits phi=0 or phi=alpha as a limit of interior marks approaching tangentially to a wall. At either endpoint the shadow length equals alpha−1. For example alpha=3/2,phi=0 gives [1,3/2), of length 1/2.

Strict inequality holds if 0<phi<alpha. Consequently Conjecture 24 as written, which excludes confinement only in arcs of length strictly less than alpha−pi, does not address tangential endpoint approaches. Either require the limiting mark angle to stay away from the walls or include the full endpoint shadow arc in the conjecture's conclusion. A density statement would handle both.

The direct-image lemma already proves the necessary shadow restriction. One need not assume that every unwrapped source image gives a valid local reflection word; its coverage adds nothing to the direct image anyway. Angles with exact difference pi remain in the shadow because the local strict transfer argument does not cover them.

`reflex-check.py/json/log` checks the image union and endpoint cases with exact rational pi-units. This is an angle identity check, not sampled optical trajectories.

## Cone-point source in Lelièvre–Monteil–Weiss

Theorem 2 explicitly allows any source point of a fixed translation surface; Section 2 allows marked regular points as well as positive-order cone points. Thus the fixed-surface finite exceptional-target statement does cover a cone-point source. It does not give density in a specified departure sector. [Publisher PDF](https://msp.org/gt/2016/20-3/gt-v20-n3-p11-p.pdf).

For a fixed rational polygon, use its fixed unfolding and the appropriate corner and target lifts. A finite union of finite exceptional sets is finite. Finiteness is not uniform as the polygon or source changes. The statement that a finite exceptional set is closed concerns that fixed surface; it is not a claim of closedness across all degenerating marked configurations.

## Restricted sector-density proposition

**Proposition (independently accepted by Opus).** Let X be a translation surface admitting a finite translation cover to a flat torus, with all branch values commensurable in that torus. Let Sigma be a finite set of absorbing marked points, including the singularities, with commensurable torus coordinates. Let c in Sigma have cone angle 2pi k, where k is a positive integer. Let t be a regular point, also with commensurable torus coordinates. If there is one straight connection from c to t with interior avoiding Sigma, then departure directions of such connections are dense in the entire cone link of c, of circumference 2pi k.

The same conclusion holds if c is a regular marked source (k=1). A fixed finite set of additional rational marked labels may be preserved without treating them as absorbing unless that is their assigned role.

Here "commensurable" means that after translation and choosing a torus period basis, all specified coordinates lie in (1/N)Z² modulo Z² for one integer N. This covers integer-grid canonical rooms with rationally placed target and blockers. It is stronger than merely saying that the polygon angles are rational. An arbitrary real limit of lattice rooms need not satisfy it.

### Step 1: a finite-index affine stabilizer fixes the endpoints and blockers

Refine the torus lattice so that every branch value, every projected absorbing marked point, c and t maps to the origin. The resulting map p:X->T is still a finite translation cover. Away from p^{-1}(0), it is an unbranched degree-D cover of the once-punctured torus.

Such a cover is specified by two monodromy permutations in S_D, up to sheet relabeling. There are only finitely many such data at fixed D. Adding labels for the finitely many selected points in p^{-1}(0) still leaves finitely many data.

SL(2,Z), acting on the base torus, acts on this finite set of labeled cover data. Its stabilizer H therefore has finite index. For every A in H, a labeled covering isomorphism supplies an orientation-preserving affine map f_A:X->X with derivative A. It fixes c,t and each absorbing point individually. Possible nonuniqueness of the lift does not matter: choose one such affine map for each needed A.

Every f_A sends a straight c-to-t connection to another straight c-to-t connection, preserving avoidance of Sigma. The lift need not preserve the polygon's folding seams; straight connections still fold to valid billiard paths because every genuine corner lift remains in Sigma.

### Step 2: H supplies hyperbolics with arbitrary nearby eigenline pairs

For a primitive integral vector r=(p,q), set

    N_r = r(-q,p),        U_r=I+N_r.

Since N_r²=0, U_r is integral with determinant one. Every finite-index subgroup contains a positive power U_r^a=I+aN_r. The argument is just repetition in the finite set of cosets of the cyclic subgroup.

Choose distinct rational projective directions represented by primitive vectors r and s. Some powers U_r^a and U_s^b lie in H. For n large, put

    A_n=(I+an N_r)(I+bn N_s) in H.

Then

    A_n/n² -> ab N_r N_s.

Writing Delta=det(r,s), this limiting rank-one matrix has range span(r), kernel span(s), and nonzero trace −ab Delta². Hence A_n is hyperbolic for sufficiently large n: one eigenvalue grows in magnitude like n² and the other tends to zero. Its attracting projective eigenline tends to r, and its repelling projective eigenline tends to s. Squaring, if necessary, makes both eigenvalues positive.

Since rational directions are dense, one can choose the attracting and repelling lines in any two prescribed disjoint open projective intervals. This argument proves the needed eigenline-pair density directly for H, without invoking an unverified general Fuchsian-group assertion.

### Step 3: remove the finite cone-sheet permutation

Fix c. An affine map with hyperbolic derivative permutes the lifts at c of its two projective eigenlines. There are 4k alternating attracting and repelling rays on the cone link. The map preserves their types and cyclic order, so its permutation shifts this alternating cyclic list by an even number. Its 2k-th power fixes every ray in that list.

On each angular interval between adjacent repelling rays, this powered map is exactly the appropriate lift of the derivative's angular action: its endpoints are fixed, so there is no additional cone-sheet rotation on that interval. Iteration converges to its unique attracting ray. Adjacent repelling rays are separated by pi; this is the usual oriented linear hyperbolic action repeated on the k sheets.

This power is taken after choosing an affine lift fixing the marked labels. It still fixes c,t and Sigma. No assumption that projected directions identify the different cone sheets is made.

### Step 4: the connection orbit is dense on the full cone link

Let K be the closure in the cone link of the departure-direction orbit of the original connection under these affine maps. It is nonempty, closed and invariant.

Take theta in K and a target direction theta' whose unwrapped angular distance from theta is less than pi. Choose a repelling ray just outside an angular interval of length pi containing both. By Step 2 choose a hyperbolic with a repelling eigenline near that ray and an attracting eigenline arbitrarily near theta'. Choose its attracting lift in this same interval. Step 3 supplies an iterate fixing all eigenrays and attracting theta to that chosen lift. Invariance and closedness put that attracting direction in K.

The attracting lift can be arbitrarily close to theta', so theta' is in K. Thus K contains every open pi-neighborhood of each of its elements. It is open as well as closed in the connected cone link. Therefore K is the entire cone link.

Every orbit element is an actual connection with the same endpoint t and the same prescribed corner lift c, avoiding the same absorbing set. This proves the proposition.

## Consequence for the grid/rational version of Conjecture 24

For a canonical grid polygon and rational target, mark all genuine corner lifts and any rational stopping points. Pick the corner lift used by one robust c-to-t connection. Its physical departure sector is one open interval in that cone link. The proposition puts connections in every smaller open physical departure arc, with the same physical corner and target after folding.

Accordingly, a nonempty connection set cannot be confined to Opus's shadow arc, even when its length reaches alpha−pi at phi=0 or phi=alpha. Under the corrected moving-sector persistence assumptions, a dark sequence converging to such a fixed commensurable corner/target configuration must therefore have no robust limiting connection at all.

This is a restricted sector result, not a solution for arbitrary real limits. It does not supply uniform word lengths, clearance bounds as the surface varies, or a statement about arbitrary nonperiodic targets. It also does not resolve merged marks: a two-ended loop imposes correlated departure and arrival sectors, and density of one endpoint direction alone is insufficient.

## Verification and handoff

The written proof is the mathematical evidence. The exact script checks the shadow identities, the nilpotent/parabolic product identities, hyperbolic trace conditions and the finite eigenray-permutation power. It does not enumerate actual affine maps of a room or claim that finitely many examples prove density.

Run:

```sh
python3 -B .context/illumination-k4-codex/degeneration-review/reflex-check.py
```

[done] Opus checked and accepted the finite labeled-cover stabilizer, affine lifts, parabolic matrix limit, powered cone-link action and open-and-closed density argument on 2026-11-01. No novelty claim is made.
