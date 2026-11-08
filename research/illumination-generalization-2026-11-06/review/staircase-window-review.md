# Independent acceptance: stated arbitrary-real staircase subclass

Verdict: ACCEPT construction/staircase-window-proof.md in its whole stated scope. For all 0<a<b<A and 0<c<d<H, every distinct actual interior pair illuminates if at least one of

    b²>=aA, b(d-c)>=ac, d²>=cH, d(b-a)>=ca

holds. These are explicit metric hypotheses, not unproved premises. There is no k, arithmetic, scale, reflection or denominator cap. The four-fail region and the complete W<=21 theorem remain open.

## Independent reconstruction before implementation inspection

I independently derived the first nested-window sufficient condition while developing the different wide-middle proof, and posted it to the board before reading this implementation. For a lower wide source with Hs=c-ys, the admissible source window has radius b/Hs about (2nA-xs)/Hs, NOT radius A/Hs. Under the middle affine map its radius is R=b(1+g/Hs). The target window about an even multiple2kb has radius a. Thus the necessary containment claim is |K-g*theta|+a<=R. The source proof has these correct widths and no hidden use of a wide middle band.

Nearest n at fixed sufficiently large K gives distance<=A*rho. The algebra A*rho+a<=b(1+rho) is exactly rho<=(b-a)/(A-b). The stated explicit k exceeds the required lower bound, so n>=1; even at a rounding tie I remains wholly positive since 2nA-xs-b> A-b>0.

The distinct second construction fixes n=1 and rounds K among nonnegative multiples2b. Since theta>0, nearest nonnegative rounding has distance<=b, including K=0. Hence rho>=a/b suffices. K=0 and equality do not invalidate positivity because containment puts the whole open J inside the already positive I. Equality of window endpoints never admits an endpoint slope: the chosen target image is strictly inside J.

## Target and every equality case

The target-image interval has length2a*D/(Hs+g)>=2a. The two target progressions have strictly smaller alternating gaps2xt and2(a-xt). Consequently an open interval of length2a still contains a strict target image. I independently checked the two-floor formula: each next image is strictly above Zlo; their minimum is strictly below Zlo+2a because the two progressions are distinct modulo2a. This closes the Ht=0 actual seam target, where a single-sign length argument would be insufficient.

The source equality xs=b is an actual interior mark below c. Its source interval and folds are still valid. At Ht=0 the last piece has zero length and the final point has 0<xt<a, so it is an interior portal mark and no final reflection is needed. The geometric threshold equalities b²=aA and the two rho regime endpoints are all included by nonstrict containment and strict image selection; no generic-parameter exclusion remains.

## Actual geometry, corner avoidance, and velocities

At the first portal, F_A(2nA+z)=|z| locally because |z|<b<A. At the second, F_b(2kb+w)=|w| locally because |w|<a<b. Thus both sides of either interface are the same local absolute-value function. This proves actual position and velocity matching with a single global slope, including a single legal reflection on the common smooth wall x=0 if z or w vanishes. No corner-excursion erasure or local path concatenation is invoked.

Strict |z|<b and |w|<a exclude both true reflex corners, and also exclude the other step endpoint corners at x=A and x=b respectively. All horizontal walls stay outside the strict source/target height interval. Remaining folds lie on actual x=0/A, x=0/b, or x=0/a finite wall portions. The height increases strictly and the final fold equals actual xt, so arrival is at the actual target and cannot occur earlier. Finiteness follows from finite slope and positive widths.

## Whole-pair coverage and transposition

I checked the two proposed L subrooms against all actual boundary segments. Qlow uses vertical-only reflections: every such wall is actual, while its artificial top cut and the actual reflex (a,d), smooth on it, are avoided. Qup uses horizontal-only reflections: every such wall is actual, while its artificial right cut and actual reflex (b,c), smooth on it, are avoided. All invoked L endpoints are strictly interior.

If neither all-y<d nor all-x<b condition holds, an actual mark with y>=d must have x<a, so its companion must have x>=b and hence y<c. This is exactly the quantified formula case, including xs=b or yt=d. No remaining seam case is silently covered by an interior-only theorem.

The threshold ordering reduces to b²>=aA exactly. The alternative b*g>=a*c gives rho>g/c>=a/b because actual ys>0. Transposition sends (A,b,a;c,d,H) to (H,d,c;a,b,A), producing the two other inequalities exactly and preserving Euclidean specularity. This proves the full stated OR of hypotheses.

## Verification level and limit

Full source and peer request pins were checked. The saved peer five controls/101contacts were read, not rerun. My new staircase-window-check.py independently constructs four different prescribed fixtures and checks266 exact guards/62 actual contacts using my own earlier pure finite-wall verifier. These include both rho threshold equalities, b²=aA, source xs=b and target Ht=0 simultaneously. No peer script was executed, no discovery or arithmetic census was replayed, and no formalization is claimed.

All four metric inequalities can fail for valid rooms. Their negations are not a darkness certificate. The remaining thin-middle staircase region and larger/diagonal-wall families still require a proof or genuine independently verified dark counterexample.
