# A50: the entire last c1 h=2 branch illuminates

Author theorem pending independent review. Original aggregate deadline2026-11-07T06:43:01.613924Z retained. Universal canonical45W<=21 objective remains OPEN.

Domain: finite integer two-sided rectangular-spine combs with core width1, every tooth width1/height2, positive same-side gaps, opposite overlaps allowed and W<=21. This proof covers every distinct actual interior A pair with vertical separation4, namely h=(t-s)/2=2. Relative floor coordinates may be odd; original actual endpoints are preserved.

## 1. Exhaustive ENTIRE-room necessary normal forms

Any actual A point is on the seam whose absolute x is even, and at a selected tooth middle row: there is no integer x strictly inside a width1 core or tooth. A Euclidean isometry puts the pair on the LEFT seam x0 at relative heights s<t=s+4. Reverse vertically and exchange S,T if necessary so that s<=v=G-t. Let q=s. Selected bands are[s-1,s+1],[s+3,s+5]. Darkness forces every accepted A38 level

2, s+2, v+2, G-2=s+v+2

to be an opposite mouth ENDPOINT, never a smooth wall or tooth middle row.

### q>=2: both selected teeth nonflush

The selected charge is4 in2N_nonflush+N_flush<=8. At least three distinct levels require at least two opposite blockers. As in the accepted A42 charge proof, the only possibilities for the entire opposite attachment budget are2NF;1NF+1F with possibly one extra unused F; or1NF+2F. Two flush blockers alone cover only two eligible interior levels. Any unused attachment must also be charged.

For2NF, sorted levels are2,2+q,2+q+d,2+2q+d where d=v-s. If d>0, two disjoint height2 bands covering four levels must pair the lower two and upper two. Thus q2, giving A1 below with d>=1. If d0, paired adjacent levels force q2; the remaining outward band would end at the global roof and is flush, contradicting2NF. No2NF/d0 case remains.

For1NF+1F reflect to put the flush band at[0,2]. If d>0 the remaining three distinct levels cannot be supplied by one height2 band. Thus d0. The other two levels are2+q,2+2q and can share a band only when q2. This is B below. The possible unused flush unit cannot be placed: its right roof band would touch the existing opposite NF band, and left floor/roof bands overlap the selected bands. The opposite floor slot is already occupied. Therefore B has no extra attachment.

For1NF+2F the two flush bands are[0,2],[G-2,G]; the inner levels must be endpoints of the NF band. Their difference d is0 or2. For d2 choose s<=v, let mu=s+2>=4, and obtain C1. For d0 let mu=s+2; up to vertical reversal the NF band is[mu,mu+2]. A positive gap before the roof-flush band requires mu+2<G-2=2mu-2, hence mu>=5, giving C2. These cases exhaust the remaining full charge, with no extra tooth.

### q=1: one selected floor-flush tooth

Here s1, t5, G=v+5. The levels are2,3,v+2,v+3. A NF opposite band with2 as endpoint must be[2,4], whose middle3 is another listed level; this contradicts actual darkness by A38. Hence the opposite FLOOR-FLUSH[0,2] is forced. Similarly a NF band ending at the last level v+3 has middle v+2, also forbidden. Hence the opposite ROOF-FLUSH[v+3,v+5] is forced.

If v1 the two middle levels coincide at3. Any height2 band with3 as endpoint is[1,3] or[3,5]; these overlap the forced floor or roof band, respectively. Same-side positive gaps make either impossible. No dark case remains there.

If v>=2, the upper selected tooth is nonflush. Together with the selected floor-flush and forced opposite two flush teeth, the remaining charge allows at most ONE NF blocker (plus at most one further F). It must supply both inner levels3,v+2, so their difference v-1 must be2. Thus v3. This gives D below. An extra left roof-flush band[6,8] would touch the upper selected band[4,6], and all other flush slots are occupied. Thus no extra attachment is possible. Values v2 or v>=4 cannot satisfy the charge and endpoint cover.

### The five entire-room forms

All have core[0,1] x [0,G]. Every listed band supplies a unit-depth tooth on its named side.

A1: d>=1 integer; G=d+8; S=(0,2),T=(0,6); LEFT[1,3],[5,7]; RIGHT[2,4],[d+4,d+6].
B: G8; S=(0,2),T=(0,6); LEFT[1,3],[5,7]; RIGHT[0,2],[4,6].
C1: mu>=4 integer; G=2mu+2; S=(0,mu-2),T=(0,mu+2); LEFT[mu-3,mu-1],[mu+1,mu+3]; RIGHT[0,2],[mu,mu+2],[G-2,G].
C2: mu>=5 integer; G=2mu; same marks/LEFT/RIGHT bands as C1.
D: G8; S=(0,1),T=(0,5); LEFT[0,2],[4,6]; RIGHT[0,2],[3,5],[6,8].

Every normalization is an actual isometry and optional S/T reversal. D's relative odd marks remain the ORIGINAL actual A marks when the original floor has odd ordinate. These are necessary cases, not claimed dark examples.

## 2. A seven-reflection local shuttle for ALL B,C1,C2

Put mu4 for B, or use its stated mu for C1/C2. Use the following actual path, initial velocity(-3,1):

(0,mu-2),(-1,mu-5/3),(1,mu-1),(0,mu-2/3),
(1,mu-1/3),(0,mu),(2,mu+2/3),(-1,mu+5/3),(0,mu+2).

All eight legs have absolute slope1/3 and strictly increasing y. Each of the seven turns is on a vertical wall and changes only horizontal velocity sign. The first source far-wall turn is within(mu-3,mu-1). Its exit at x0 has ordinate mu-4/3, also strict in that source mouth. The two right core-wall turns are at mu-1 and mu-1/3, in the smooth interval(2,mu) since mu>=4. The intervening left core-wall turns at mu-2/3 and mu lie strictly between the selected mouths. The right tooth is entered at x1 at mu+1/3; its far turn at x2,mu+2/3 is smooth; its exit through x1 is at mu+1. The trajectory crosses the upper selected left mouth at mu+4/3, hits its far wall at mu+5/3 and reaches the actual T. These are all strict tooth passages.

The right floor-flush tooth ends at2, below all used right core mirrors. In C1/C2 the roof-flush tooth starts strictly above mu+2. B has no such roof tooth. Thus none removes a used mirror. All heights are between actual S,T, within the global core height range; no floor or roof is used. The upper target is reached first by strict height monotonicity. This proves illumination for EVERY parameter of B,C1,C2, including their smallest members. No finite seed or residue transfer is required.

## 3. Complementary seven-reflection shuttle for ALL A1 d>=2

Use

(0,2),(-1,7/3),(2,10/3),(0,4),(1,13/3),
(0,14/3),(1,5),(-1,17/3),(0,6).

Again initial velocity(-3,1), absolute slope1/3 and strictly increasing y give the exact specular law at all seven vertical turns. The source left far turn7/3 lies strictly in(1,3). The trajectory exits that source mouth at8/3, enters the right[2,4] tooth at3, turns at its actual far-wall point(2,10/3), and exits at11/3. The left core contacts4 and14/3 lie in(3,5). The right core contacts13/3 and5 lie strictly between the right teeth because the second begins d+4>=6. The upper left tooth is entered at16/3, its far turn17/3 is smooth, and the final segment reaches the actual T. All entries and exits are strict.

At d2 the unused second right mouth begins at height6; the only height6 point on this path is T at x0, not its corner at x1. Hence no equality case is omitted. This path was found in a cap with a rejection roof, but the argument directly checks the actual full20wall room for ALLd>=2. The artificial roof never participates. There is no inference of illumination under arbitrary attachment.

## 4. Exactly two isolated exceptions

A1 d1 and D have the following stored actual certificates:

| Case | Initial actual velocity | Reflections | All-wall leg guards |
|---|---|---|---|
| A1d1 | (-13,8) | 20 | 420 |
| D | (-7,4) | 8 | 162 |

Complete polygons, actual S,T, rational contacts and wall indices are in c1-h2-check.json, selected by case. Every leg was checked against every physical finite wall with exact Fractions; all contacts are unique wall interiors, obey the ordinary reflection law and arrive at the actual T first. Their independent replay remains necessary for final acceptance. The two exceptions total28reflections/582guards.

The original prescribed12case discovery also verified B and nine small C cases, totaling98reflections/2166guards across all12. Those ten extra paths suggested the seven-reflection formula and are now controls, NOT a finite-prefix dependency or a substitute for the all-parameter proof. The initially proposed floor formula for large mu is valid but unnecessary to this smaller complete argument. It is not used as an additional claimed theorem. The complementary A1 cap first witness had7reflections/128guards in its16wall auxiliary cap, not in every full20wall room; the explicit guards in section3 give the actual-family transfer.

## 5. Entire h2 closure and model join

The necessary entire-room classification in section1 plus sections2-4 covers EVERY actual h2 pair in this model. No finite prefix or real growth parameter is left undecided. Accepted A47/A48/A49 already cover every h>=3 same-seam actual A pair in c1 thin combs. Positive same-side gaps exclude h1. Thus independent acceptance of A50 would close EVERY actual interior A pair for the ENTIREc1 unitwidth/height2/W<=21 class.

Combined with the independently accepted complete c2 theorem and A39c>=3 theorem, this would settle the stated integer two-sided rectangular-spine comb class for EVERY integer core width c>=1, no transparent-exception/support/height/diameter cap. It would NOT settle arbitrary tooth widths/heights or arbitrary canonical45 polygons. The universal objective remains OPEN; this is a complete geometric subclass milestone, not goal completion.
