# Light through comb rooms

[Watch or download the video](comb-illumination.mp4) · [Read the manuscript](../../preprints/middle-row-combs/manuscript.pdf) · [Transcript](narration.md) · [All explainers](../README.md)

**8:30 · 1920×1080 · 30 fps · narrated for math students.**

Central finite matching proof, path construction, remaining endpoint cases, and the height-two lattice corollary. Only spine and tooth-middle-row endpoints are covered.

Source authors: **Daniel Wang and Peyton Wang**. The manuscript is a working draft, not externally refereed; the video does not establish a universal minimum-wall result. Codex and Claude assisted the research and exposition. The authors remain responsible for the mathematics.

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

The render command writes `renders/comb-illumination.mp4`, preserves the authored narration, and adds chapter metadata. It leaves the checked-in video unchanged. The first use downloads the pinned HyperFrames runtime; project-specific audio and diagrams are included. Rendered bytes may vary with browser, encoder, and platform versions.

## Chapters

- 0:00 — The question
- 0:58 — Set up the match
- 2:33 — Prove finite termination
- 4:19 — Build the actual path
- 5:39 — A worked example
- 6:22 — Finish the endpoint cases
- 7:23 — A lattice consequence
- 7:45 — Scope and takeaway
