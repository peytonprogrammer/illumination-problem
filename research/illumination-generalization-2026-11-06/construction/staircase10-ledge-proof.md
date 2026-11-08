# ST10-D: a genuine internal-ledge route with four reflections

Author hand proof, pending independent review. Candidate and symbolic control were declared in staircase10-ledge-candidate.md before this proof. This develops one new original-wall optical mechanism beyond ST10-A's outer-only horizontal contacts. It does NOT assert that ST10-A fails, or complete all-metric/all-pair staircase10.

## 1. An exact actual-endpoint four-word certificate

Use any original four-band nested staircase. Let actual S=(s,u),T=(t,v) satisfy

 0<u<y1, 0<s<w0,
 y3<v<H, 0<t<w3.

Define

 D=2y1-u+v,
 tau=(s+2w3-t)/D>0,
 q1=s-tau*(y1-u), q0=s-tau*(2y1-u),
 a=q0/tau, b=a+w3/tau.

Suppose the following simultaneous strict inequalities hold:

 q1>w1, q0>0, b>y3,                         (G1)
 q0-tau*y_j < w_j for j=1,2,3.             (G2)

Then there is a legal actual four-reflection path

 S -> C=(q1,y1) -> F=(q0,0)
   -> L=(0,a) -> R=(w3,b) -> T.

These are jointly evaluated at the ONE matched tau; none is selected as an independent portal ray. The equations by themselves do not prove G1/G2. Their necessity for this particular ordered word is geometric, and the positive family below establishes them uniformly rather than assuming legality.

## 2. All travel times and endpoint identities

Start with velocity(-tau,+1). The first elapsed time is y1-u>0. At C reflect from the actual horizontal ledge to velocity(-tau,-1) and descend for y1>0 to F. Since q0<q1<s<w0, G1 gives both contacts strictly between the relevant outer walls; q1>w1 places C in the genuine ledge interior (w1,w0)x{y1}. Both initial open legs are in the bottom rectangle, so no other wall or corner interrupts them.

At F reflect from the genuine floor to(-tau,+1). The time to L is a=q0/tau>0. At L the original outer left wall reverses horizontal velocity, giving(+tau,+1). The time to R is w3/tau>0. Finally R reverses horizontal velocity to(-tau,+1).

The matched target equation is

 tau*v=q0+2w3-t.

It implies

 v-b=(w3-t)/tau>0.

Thus 0<a<b<v<H. The final free leg has positive duration and ends at EXACT (t,v), not another target image. Each reflection changes just the normal velocity component and preserves the common speed sqrt(1+tau^2). No interior change of direction occurs.

## 3. All intermediate finite-wall and first-hit guards

The only nontrivial rising piece before L has x=q0-tau*y,0<=y<=a. If it reaches an internal seam y_j before L, its horizontal coordinate is positive and G2 puts it STRICTLY inside that original narrower mouth. Between successive seams x decreases, so once inside a band it cannot hit its right wall before the next seam. If y_j=a, the coordinate0 is a smooth point of the single actual maximal left wall, not a vertex. If y_j>a, G2 is automatically true but no passage on this pre-L piece is claimed at that height.

From L until R, x=tau*(y-a), so 0<=x<=w3. G1 makes b>y3. Hence at every earlier seam this x is strictly less than w3<=w_j, and at all earlier lower-band vertical walls it is strictly below their larger widths. In the top band it first reaches the genuine right wall x=w3 at height b in(y3,H). There is no earlier vertical or horizontal hit.

From R to T the physical height stays in(b,v] subset(y3,H); x decreases fromw3 to actualt>0. It stays in the top rectangle and hits no other wall or corner before T. Every earlier part has height<v (initial and descending parts have y<=y1<v, and the rising parts finish at b<v), so this is the FIRST actual T.

F lies strictly inside the true floor because0<q0<w0. L has0<a<H and is on the one maximal outer left wall. C and R are strict interiors of their true finite walls, as shown above. The strict seam guards exclude all inner reflex and outer ledge corners. There are precisely four ordinary reflections; no artificial cut or convex/reflex corner continuation is used.

This proves the certificate in section1 for every real input satisfying its explicit joint guards. It does not make those guards automatic for arbitrary actual S,T.

## 4. Uniform symbolic realization outside the earlier uniform tests

Take

 L>0, 25/72<rho<25/41,
 (w0,w1,w2,w3)=(L,rho*L,4rho*L/5,16rho*L/25),
 (y1,y2,y3,H)=(16rho*L/25,4rho*L/5,rho*L,L).

Write c=16rho*L/25=w3=y1 and F=L-2c. For EVERY e with0<e<c choose actual

 S=(L-e,e), T=(e,L-e).

Since rho<25/41, L-c>w1=y3. Therefore S is strictly inside the original bottom overhang (s>w1,0<u<y1), and T is strictly inside the top band (0<t<w3,y3<v<H). They are distinct because c<L/2, which follows already from rho<25/41<25/32.

For these actual endpoints the matched tau is EXACTLY1:

 s+2w3-t=L+2c-2e=2y1-u+v.

The candidate contacts reduce to

 C=(L-c,c), Fpoint=(F,0), Lpoint=(0,F), R=(c,L-c).

G1 follows from

 q1=L-c>w1 iff rho<25/41,
 q0=F=L-2c>0 since rho<25/32,
 b=L-c>y3 iff rho<25/41.

For G2, the three seam inequalities reduce respectively to

 L-3c<w1              iff rho>25/73,
 L-2c-w2<w2           iff rho>25/72,
 L-2c-w1<c            iff rho>25/73.

All are STRICT under the declared range, since25/72>25/73. No omitted inequality depends on a special choice of e. The first and final legs each have positive time c-e, the C-to-floor time is c, the floor-to-left time is F>0, and the left-to-right time is c. The actual final height is L-e as required.

Thus EVERY room and pair in this stated symbolic control has the legal four-reflection path. It includes native integral members by choosing rational rho, clearing width/height denominators, taking an even integer L and an even integer e in(0,c). Arbitrarily large scales and endpoint clearances are permitted; no geometric parameter sampling is used.

## 5. What the new route adds, and what it does not

The previous coverage ledger exhibits self-dual rho in(397/1024,5/8) outside B, dual B and bounding-triangle inclusion. Its overlap with(25/72,25/41) is the nonempty interval(397/1024,25/41). ST10-D therefore gives actual jointly guarded paths for its actual symmetric pairs within a region where the three uniform tests provide none. This is a positive internal-ledge mechanism, not a numerical example or merely a new target equation. For L250,rho1/2,e2 it yields actual contacts(170,80),(90,0),(0,90),(80,170) between actual(248,2) and(2,248); this calibration is derived from the theorem, not a discovered ray.

The word explicitly reflects at the ORIGINAL internal horizontal ledge y1, outside the outer-only horizontal programmes of ST10-A. The result does NOT establish that those outer-only programmes fail for any pair. It does not license reflecting at an arbitrary cut of an eight-wall subroom, transferring a corner-degenerate path, or concatenating separate local illuminating paths.

Most importantly, the family is a bounded symbolic prototype of an internal-ledge route. It is not an autonomous narrow-family research programme or a substitute for the all-metric milestone. The remaining general task is an ORIGINAL-ledge/word selection theorem for arbitrary residual actual endpoints, retaining all common-direction guards, or a complete failure of a proposed full route class. No such universal selection has been proved.

There is no claim for rho at either strict endpoint, for arbitrary source/target placements in this family, all staircase10, allr3/r<=8, mixed directions or universal wall minimality. No search, engine, census, fitting, worker, new clock, frozen-source edit or git change was used. Independent review is required before treating this as accepted.
