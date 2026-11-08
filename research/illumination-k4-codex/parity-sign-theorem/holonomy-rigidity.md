# Conditional rigidity from absolute periods

[done] Elementary wall-reflection argument and exact checks on 34 frozen rooms.
[done] Independent Opus algebra review, with profile and presentation corrections incorporated. The reviewer inspected code without running it.

This proves a conditional rigidity statement, not the sign theorem. The missing premise is that darkness forces the period relations to persist.

## Statement

Fix the directions of the labeled walls of a strictly simple polygon. Their reflections generate a finite linear group G. In the canonical 45-degree case with horizontal, vertical and diagonal walls, G is D4, the order-eight symmetry group of a square.

Write the reflection in wall i as

    r_i(x)=R_i x+b_i,   b_i=2h_i n_i/|n_i|².

For a wall word w, composition gives

    r_w(x)=O_w x+b_w,
    b_(uv)=b_u+O_u b_v.

Call a word a return word if O_w=I. Its translation vector b_w is an absolute period of the unfolded surface. Assume these vectors span R².

Suppose a deformation, with the wall directions held fixed, changes every return-word vector by one common linear map A:

    delta b_w=A b_w    whenever O_w=I.                 (P)

Then A commutes with G. If G=D4, A=lambda I, and there is a vector a such that

    delta h_i=lambda h_i+n_i dot a,
    delta c_i=lambda c_i+a.

Thus the wall motion consists only of translation and uniform scale.

For an orthogonal family, G is the order-four reflection group, its commuting matrices are diagonal in the wall axes, and independent horizontal and vertical scaling remain possible. This is the expected larger family symmetry.

## Why return words are genuine periods

Use the usual unfolded surface with one polygon copy for each orientation in G. Every wall crossing changes the copy label by R_i. For any prescribed sequence of crossings, choose paths through each polygon copy joining wall-interior points and avoiding the vertices. These paths need not be straight. Such choices exist because the polygon interior is path-connected.

A return word ends in the original copy. Close the path to its starting point inside that copy. Its developed displacement is b_w, since the final orientation is I. It therefore represents an absolute period. No proposed billiard trajectory or new optical event is being introduced.

Conversely, a closed path avoiding the finitely many vertex lifts can be split at its wall crossings. Its developed displacement is the return-word translation. This also explains why the finite return generators below capture the period information needed here. Relations coming from vertex loops have zero translation.

## Proof

### 1. The common map must commute with the reflection group

Let k be a return word, and let w have orientation g. The conjugate w k w^(-1) is another return word. Its translation is

    b_(wkw^(-1))=g b_k.

Because g is fixed during the deformation, its variation is g delta b_k. Apply (P) to both return words:

    A g b_k=g A b_k.

The b_k span R², so A g=g A for every g in G.

In D4, commuting with the horizontal reflection makes A diagonal. Commuting also with reflection in a diagonal makes its two diagonal entries equal. Therefore A=lambda I.

### 2. Remove that common linear change

Define

    z(w)=delta b_w-A b_w.

The composition formula and A O_w=O_w A give

    z(uv)=z(u)+O_u z(v).

Condition (P) says z vanishes on every return word. Therefore z depends only on the orientation g=O_w: if O_u=O_v, the return word uv^(-1) gives z(u)-z(v)=0.

Here z(v^(-1))=-O_v^(-1)z(v), by applying the cocycle identity to vv^(-1). Hence the equal-orientation argument really does give z(uv^(-1))=z(u)-z(v).

Thus z is a vector-valued cocycle on the finite group G. It is a translation change. To see this directly, set

    a=(1/|G|) sum_(g in G) z(g).

For any h in G, summing z(hg)=z(h)+h z(g) over g yields

    a=z(h)+h a,
    z(h)=a-h a.

Apply this to each wall reflection:

    delta b_i-A b_i=(I-R_i)a.

When A=lambda I, substituting b_i and I-R_i gives

    2(delta h_i-lambda h_i)n_i/|n_i|²
       =2(n_i dot a)n_i/|n_i|².

Thus delta h_i=lambda h_i+n_i dot a. The intersection of two adjacent supporting lines then has velocity delta c_i=lambda c_i+a. This proves the statement.

The averaging argument is standard finite-group linear algebra. No novelty claim is made for that ingredient or for rigidity of fixed-angle torus-cover diagrams.

## Finite generators for an exact check

Choose one wall word P_g for each orientation g, with P_I empty and affine representative F_g(x)=g x+B_g. For each g and each wall i, let g'=g R_i. The return word P_g i P_(g')^(-1) has period

    L_(g,i)=B_g+g b_i-B_(g').

There are at most |G| W such periods, including zeros and duplicates. Their words generate the return-word subgroup: follow a wall word and insert the chosen representatives at each intermediate orientation; adjacent representatives cancel. Translation vectors add for return words. Therefore it is enough to impose delta L=A L on this finite list.

The implementation solves these equations exactly in the unknowns (delta h,A). It also verifies that their base periods span R².

## Marked points need an additional premise

Absolute periods do not determine the two interior marks. If their relative periods from the first vertex obey the same linear map,

    delta(s-c_0)=A(s-c_0),
    delta(t-c_0)=A(t-c_0),                             (M)

then the theorem gives delta s=lambda s+a and delta t=lambda t+a. Consequently the entire marked configuration changes only by similarity.

A continuously marked torus-cover diagram with fixed winding numbers supplies (P). Fixed rational torus profiles for c_0 AND both marks supply (M), including fixed local choices of their integer lifts. Fixing profiles for the marks alone does not fix their displacement from a moving reference vertex; c_0 can be a regular corner lift. Merely having some torus cover at each configuration is not being used as a substitute for this continuously identified data.

## Exact finite version

The same argument compares two wall systems, rather than their derivatives. If

    b_w(new)=A b_w(old)

for every return word and an invertible A, the conjugation argument again gives A g=g A. Define z(w)=b_w(new)-A b_w(old), average over G, and conclude

    h_i(new)=lambda h_i(old)+n_i dot a

in the D4 case. A negative lambda also represents a similarity, with a half-turn; nearby configurations with the original side labels have positive lambda. Corresponding exact relative-profile equations place the two marks under the same similarity. The infinitesimal statement concerns a tangent vector; integrating it along a path requires its hypotheses at every parameter value.

## Zero-period relations detect all nonsymmetry motions

At a parity base room all return periods are rational vectors. Choose two independent period vectors P and Q. For each return generator with period L_j, solve

    L_j=alpha_j P+beta_j Q

at the base room. The coefficients are rational. The absolute cycle

    kappa_j=Gamma_j-alpha_j Gamma_P-beta_j Gamma_Q

has zero holonomy at that room. Clear denominators to obtain an integral cycle, if required. These are piecewise loops or homology classes, not asserted billiard trajectories.

Suppose every such cycle keeps zero first-order holonomy. There is a unique linear map A taking P,Q to delta P,delta Q. The zero-relation equations imply delta L_j=A L_j for every generator. The rigidity theorem therefore forces similarity. Conversely, similarity preserves every zero-period relation.

Thus in the D4 case these zero-period differentials have kernel precisely the two translations and uniform scale. Their rank on W wall-offset coordinates is W-3. Adding the four marked relative relations from (M) gives rank W+1 on the full W+4 configuration chart. The added equations prescribe the four mark velocities; their dimension count is a consistency consequence, not evidence that darkness imposes (M).

This puts the remaining optical question in a concrete form: does any nonzero drift of these zero-period relations, modulo symmetry, force an admissible corner event with negative signed variation? Linear algebra alone does not give the required event or its sign.

### The existing ear motion breaks one three-period relation

For the already-frozen room parity-W25-24, the check selects return cycles with

    P=(0,4), Q=(-2,2), R=(0,8)=2P.

Under the known ear motion delta h_5=2, delta h_6=-1, their changes are

    delta P=(0,0), delta Q=(-2,2), delta R=(0,2).

Therefore the absolute zero-period cycle Gamma_R-2Gamma_P acquires drift (0,2). This is an explicit way a local wall change breaks the original period diagram. It does not prove that this change illuminates the marks; the separate diagonal-event certificate established that fact at first order in this fixed room.

## Checks and limits

`holonomy-rigidity.py` uses the 34 frozen polygon geometries. Every one has orientation group D4 and period span rank two. In each case the exact kernel of (P), including the four unknown entries of A, has dimension three. The zero-period relation matrices independently reproduce wall rank W-3 and marked rank W+1. Translation and scale vectors are checked explicitly. Adding the four marked-profile equations simply determines the four added mark variables.

Two prescribed controls check the scope: an orthogonal rectangle retains independent axis scales, and a twofold dilation of the first room leaves intrinsic cover degree28 unchanged while both area and lattice covolume grow by4. Both new checkers explicitly reject optimized Python mode, which would disable assertions. The algebraic degree formula and the latest zero-period corollary are not a separate peer numerical replay.

This is a check of the conditional theorem, not evidence that all dark deformations satisfy its premises. A dark deformation could change the cover, or leave the torus-cover locus, or move the marks outside fixed rational profiles. Excluding these possibilities is open.

Even actual local isolation would not by itself prove the stronger first-order sign theorem. An isolated zero set may have a degenerate linearization, as x²+y²=0 illustrates. This route could instead supply local isolation directly if the missing cover-preservation theorem were proved.
