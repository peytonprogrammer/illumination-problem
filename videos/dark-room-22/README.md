# The 22-sided dark room

[Watch or download the video](dark-room-22.mp4) · [Read the manuscript](../../preprints/twenty-two-wall/manuscript.pdf) · [Transcript](narration.md) · [All explainers](../README.md)

**8:37 · 1920×1080 · 30 fps · narrated for math students.**

Construction, parity obstruction, seam reversals, and the no-help argument. The [updated manuscript](../../preprints/twenty-two-wall/manuscript.pdf) also proves that this is the only dark pair among distinct real interior points. Its cylinder argument is explained in the [illustrated companion](../../preprints/twenty-two-wall/explainer.html); it is not part of this video.

Source authors: **Peyton Wang and Daniel Wang**. The manuscript is a working draft, not externally refereed; the video does not establish a universal minimum-wall result. Codex and Claude assisted the research and exposition. The authors remain responsible for the mathematics.

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

The render command writes `renders/dark-room-22.mp4`, preserves the authored narration, and adds chapter metadata. It leaves the checked-in video unchanged. The first use downloads the pinned HyperFrames runtime; project-specific audio and diagrams are included. Rendered bytes may vary with browser, encoder, and platform versions.

## Chapters

- 0:00 — The question
- 0:55 — The construction
- 2:12 — The folding map
- 3:04 — The parity proof
- 5:16 — The seam endpoints
- 6:37 — Why reversals cannot help
- 7:52 — The result
