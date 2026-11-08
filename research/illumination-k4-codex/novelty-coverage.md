# Literature audit coverage

Date: 2026-10-31. Target: historical novelty of `cand-2_2-1.json`; no ray searches, new rooms, or outward messages.

## Read and compared

- Wolecki arXiv v1 and v3: relevant introduction, theorem, convention, construction and acknowledgments. Source packages downloaded. Source figure PDFs are byte-identical, SHA-256 `62a56ffe13171f6755c99881aef1ebee5ba7463fbce75be468859d78abc2fa02`. v2 was not separately audited.
- Castro: original Quantum letter, printed page42 / PDF44, text and rendered figure. Visual reading resolves the research date as spring1996.
- O'Rourke: author page and vector PDF of Fig.9.14. Exact vector outline comparison; 34 walls. Not a census of every historical orthogonal example.
- Monteil: full 123-page thesis downloaded from HAL. Table of contents, keyword screening, relevant illumination introduction and initial figures reviewed. Did not read every thesis page in detail. Extracted text has missing letters; negative text searches cannot certify absence.
- Tokarsky–Boese (2000): article OCR on the public scan page, including Theorem1, pp.366–367 reflected-copy construction and corollary, later classification discussion. Publisher copy unavailable. Figures not audited geometrically from this OCR.
- Davis: current author-hosted full manuscript downloaded; relevant pp.114–115 and Fig.87 rendered/read, later Penrose section screened. Not a full-book read.
- Chernov–Galperin (2003): introduction and p.226 lemma explanation, original figure context. Not a competing compact-room construction found there.
- Bouncing Robots in Rectilinear Polygons (2022): abstract/introduction, related work and terminology screened. A robot trapped for particular directions is distinct from all-direction nonillumination.
- Directly Visible Pairs and Illumination by Reflections in Orthogonal Polygons (2008): author-page/primary-paper abstract screened; concerns visibility counts, diffuse reflection bounds and bounded specular visibility complexity. Full text not exhaustively reviewed.

## Citation and keyword coverage

- OpenAlex `cites:W2326163060`, per-page100: response count43, 43 returned. All titles/metadata screened; no claim of 43 full-text reads.
- OpenAlex Wolecki work `W2946528780`: citing response count1, one returned. Coverage incomplete: Davis's citing book is absent. No claim of exhaustive forward citations.
- Search families: orthogonal/rectilinear/polyomino + Tokarsky/illumination/unilluminable/nonilluminable; 22/22-sided/22-edge/22-gon + Monteil/Wolecki; staircase/folding; title searches for original papers; author sites and contemporary textbook/visibility leads.
- Secondary sources used as leads include Quanta, Wikipedia, MathWorld, MathOverflow and public posts. Record claims were assessed against primary works, not accepted from these summaries.

## Unresolved

- Monteil unpublished22: existence acknowledged in Wolecki; no geometry recovered.
- Tokarsky1995: metadata and primary follow-on descriptions verified; full original article remains unread. JSTOR file is HTML failure, not PDF.
- Tokarsky–Boese2000 original figures: OCR is insufficient for geometric identity comparison.
- Stewart1996/1997 and Tokarsky author videos: leads, not a completed primary figure audit in this turn.
- No certification of historical priority, orthogonal wall minimum, or simple-polygon wall minimum.

## Reproduction

`python3 -B .context/illumination-k4-codex/novelty-geometry-check.py` checks source figure geometry and candidate boundary. Source manifest and per-file digests are in `novelty-sources.json`. The checker normalizes Wolecki vector coordinates to their repeated integer-grid positions with a recorded small rounding residual; it is not a direct exact arithmetic interpretation of rounded PDF coordinates.

Local failed retrievals are retained with their actual byte signatures. A `.pdf` suffix does not imply a valid PDF. No new dependencies were installed; geometry checker uses the Python standard library and preexisting mutool-generated SVGs.

## Priority follow-up

Further Monteil author-site, Oberwolfach-summary and concrete-surface-wiki checks are recorded in `priority-followup.md`. The unpublished geometry remains unidentified. Original figure access gaps persist.
