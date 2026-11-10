# Light through a twelve-wall corridor

[Watch or download the video](twelve-wall-corridor.mp4) · [Read the manuscript](../../preprints/twelve-wall-corridor/manuscript.pdf) · [Transcript](narration.md) · [All explainers](../README.md)

**9:30 · 1920×1080 · 30 fps · narrated for math students.**

Proof map with one-pass/three-pass chart geometry, cap transfer, a five-reflection example and the exact continuous certificate-cover argument. Only lower-to-upper outer-chamber pairs.

Source authors: **Daniel Wang and Peyton Wang**. The manuscript is a working draft, not externally refereed; the video does not establish historical novelty or a universal minimum-wall result. Codex and Claude assisted the research and exposition. The authors remain responsible for the mathematics.

## Editable source

- `index.html` assembles the timeline and audio.
- `compositions/` contains the scene HTML, inline CSS, SVG diagrams, and GSAP JavaScript animations.
- `assets/audio/` contains the narration used by the project.
- `script.json`, `timeline.json`, and `narration.md` contain the script and timing data.
- `hyperframes.json` and `package.json` configure HyperFrames and pin its CLI version.
- `chapters.ffmeta` supplies the MP4 chapter markers; `video.json` records the manuscript, scope, and delivered checksums.

## Preview, check, and render

Install Node.js 22+, Python 3, and FFmpeg, then run from this directory:

```sh
npm run dev
npm run check
npm run render
```

The render command writes `renders/twelve-wall-corridor.mp4`, preserves the authored narration, and adds chapter metadata. It leaves the checked-in video unchanged. The first use downloads the pinned HyperFrames runtime; project-specific audio and diagrams are included. Rendered bytes may vary with browser, encoder, and platform versions.

## Chapters

- 0:00 — The question
- 1:00 — Normalize and reduce
- 1:43 — Build folding charts
- 3:39 — Transfer back to actual marks
- 4:53 — Prove that charts suffice
- 5:57 — Reduce the rational cases
- 7:41 — Cover every endpoint pair
- 8:46 — Conclusion
