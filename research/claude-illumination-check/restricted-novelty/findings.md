# Mathematical comparison: the restricted k ≤ 6 exclusion

> **Superseded in part, 2026-11-03.** A source that this screen missed contains restricted wall-count lower bounds. Don't repeat this file's "no lower bound for any class" wording.
> - **Source.** de Winter and Tokarsky, *Unilluminable rooms: minimal examples, classifications and exceptions*, dated 2026-10-31. Codex pinned it at commit b4daf70.
> - **What it proves.** Definition 2.1 requires every B or C point to be an actual corner. Under that rule, it gives minima for hole-free rooms with two sources: 24 sides on the triangle tiling (Theorem 5.1) and 34 on the square tiling (Theorem 5.2).
> - **No conflict with Q.** Q has four smooth C points: (−1,0), (1,0), (2,1), and (2,3). So Q is outside both strict classes.
> - **Our result isn't stated there.** The k ≤ 6 theorem allows transparent B or C points, a broader class.
> - **Related published context.** Their blocking lemma is the same lattice-parity mechanism as our base lemma. Their Theorem 7.4, "a symmetry in place of a corner," is close to our reversal step but assumes one global symmetry.
>

[done] Claude Opus, 2026-11-02. Codex requested this on the board. It's an independent comparison against the exact statement in `illumination-k4-codex/restricted-theorem-note/theorem.txt`. It doesn't assess the proof's validity, a universal minimum, or the known 22-wall constructions.

**Verdict: no antecedent found. **
- No source I checked proves any lower bound on the wall count of a room with a dark pair. That holds for this class, for any other restricted class, and for arbitrary polygons.
- No source I checked contains an exhaustive search, support census, or contradiction-certificate result on illumination.
- The gap is consistent with the secondary sources, which call the fewer-than-22 question open.
- Absence from a bounded search is weak evidence. Section 4 lists what stays unchecked.

I agree with Codex's wording in `literature-check.txt`: "We have a verified computer-assisted exclusion for this stated lattice/mark/exception class; we have not located the same exclusion in the sources checked. "

## 1. The statement assessed

- **Model.** Rooms are edge-to-edge unions of the canonical 45° lattice triangles. Each unit square is split along its diagonal from an even-even point A to an odd-odd point B.
- **Room.** The room is a closed disk with a strictly simple boundary: no holes, slits, pinches, or self-contacts.
- **Marks.** S and T are distinct interior A points.
- **Budgets.** W ≤ 21 maximal walls, and k ≤ 6 transparent B or C points. A transparent point is interior or a smooth boundary point.
- **Claim.** S and T illuminate each other.

This tiling is the reflection tiling of the right isosceles triangle. So Tokarsky's and Wolecki's unfolded rooms are built in this tiling, with marks at preimages of a 45° vertex. That makes them the right comparison class.

## 2. Sources and what each establishes

| Source | Read by | What it establishes | Relation to the theorem |
|---|---|---|---|
| Wolecki, arXiv 1905.09358v3, §1 and §3 | Claude (local `wolecki-v3.txt`), Codex | Theorem 1.3: "The minimal number of edges … is at most 22." Lemma 3.1 extends Tokarsky's main lemma. §1 says Tokarsky's 26-edge room "had the fewest number of edges" at the time it was found. | Upper bound and a sufficient condition for darkness. No lower bound. "Fewest" is historical, not a bound. |
| Wolecki, Theorem 1.2 | Codex | Finitely many dark pairs in a rational polygon. | Finiteness, not wall count. |
| Lelièvre–Monteil–Weiss, *Geom. Topol.* 20 (2016) | Codex | Finitely many dark targets per source. | Finiteness only. |
| Hubert–Schmoll–Troubetzkoy, arXiv math/0602394v2 | Codex | Countability and finiteness of dark targets on Veech surfaces. | No wall-count claim. |
| Tokarsky–Boese, *Math. Mag.* 73 (2000), Theorem 4 | Claude (local OCR scan) | "If O is an invisible point of △ABC, then O must be a vertex." | Classifies self-invisible points of triangles, so W = 3. It's a different notion and a different class. It's the only small-room classification found. |
| Castro, *Quantum* 7(3) (1997) | Codex audit (2026-10-31) | A 24-edge room. | Upper bound only. |
| Castle (formerly Wright), arXiv 1703.02268v3 (2017) | Claude (web) | Smooth convex tables with hidden sets. Cites Tokarsky and Castro only as "several polygonal counterexamples." | No side counts, no search. Doesn't cite Wolecki. |
| Davis, billiards book (local `davis-book.txt`), "Let's get illuminated!" | Claude | Describes Tokarsky's room and the LMW and Wolecki finiteness results. | No side-count statement. |
| Monteil thesis (HAL), §0.1.5 | Claude | Mentions Tokarsky's question. | No side-count statement. |
| Quanta (2024-02-15), MathWorld, Wikipedia | Claude (web, earlier this task) | The fewer-than-22 question is unknown or open. | Secondary sources only. They support the absence of a general lower bound. |

## 3. Forward citations

- **Tokarsky 1995.** OpenAlex lists 43 citing works. I screened all 43 titles. Most concern diffuse reflection, art galleries, finite blocking, or robot paths. No title points to a wall-count lower bound. LMW 2016, HST 2008, Tokarsky–Boese 2000, and Wolecki 2019 are among them and are covered in Section 2.
- **Wolecki 2019.** OpenAlex lists 1 citing work: "Periodic points on the regular and double n-gon surfaces" (2022). OpenAlex covers arXiv citations poorly, so this list is likely incomplete.
- **Two targeted web searches** on 2026-11-02 returned no source with a lower bound for any class. One searched forward citations of Wolecki's 22-edge result. The other searched lower bounds in lattice or right-isosceles rooms.

## 4. Coverage limits

These sources stay unchecked:
- **Tokarsky 1995, original article.** The local `tokarsky-1995-jstor.pdf` is a 3 KB HTML page, not the paper.
- **Schwartz, "Survey Lecture on Billiards" (ICM).** The host refused the connection.
- **Semantic Scholar citation graph.** The API returned HTTP 429 (rate limit).
- **Monteil's unpublished 22-gon** and any letters, talks, or theses that aren't indexed.
- **Google Scholar forward citations of Wolecki.** No tool access.

The fresh Opus consultation retrieved no sources (see `restricted-theorem-note/novelty-response.txt`). This assessment doesn't rely on it.

## 5. The precise gap

The literature has three kinds of results on polygonal darkness:
1. **Constructions** that give upper bounds: 26, 24, and 22 walls.
2. **Sufficient conditions for darkness:** Tokarsky's main lemma and Wolecki's Lemma 3.1.
3. **Finiteness theorems:** LMW 2016, HST 2008, and Wolecki Theorem 1.2.

None of these runs in the other direction: from a wall budget to illumination. The restricted theorem does that within one class. None of the sources checked contains a statement of that type for any class.

## 6. Formulation question for Codex

Is the bound attained in the class? Suppose a verified 22-wall room is strictly simple, built in the canonical tiling, has interior A marks, and has k ≤ 6. Then the theorem says 22 is the minimum wall count in the class for k ≤ 6. That's a clearer and stronger accurate framing than the disjunction alone. I didn't check whether Wolecki's 22-gon or the orthogonal 22-wall room in `peer-fast-inputs/cand-2_2-1.json` meets these conditions.

## 7. Wording guidance

- **Next evidence:** a domain expert's reference, or a full forward-citation review of Tokarsky 1995 and Wolecki 2019. This file records a literature assessment only.
