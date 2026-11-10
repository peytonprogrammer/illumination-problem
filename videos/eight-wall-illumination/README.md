# When darkness is impossible

[Watch or download the video](eight-wall-illumination.mp4) · [Read the manuscript](../../preprints/eight-wall/manuscript.pdf) · [Transcript](narration.md) · [All explainers](../README.md)

**9:00 · 1920×1080 · 30 fps · narrated for math students.**

Proof map, detailed L-room mechanism, and selected U, corridor, and staircase constructions. The manuscript contains the full technical proof.

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

The render command writes `renders/eight-wall-illumination.mp4`, preserves the authored narration, and adds chapter metadata. It leaves the checked-in video unchanged. The first use downloads the pinned HyperFrames runtime; project-specific audio and diagrams are included. Rendered bytes may vary with browser, encoder, and platform versions.

## Chapters

- 0:00 — The question
- 0:59 — Classify the room
- 2:02 — The L-room engine
- 4:01 — Reuse the engine
- 5:49 — The staircase
- 7:52 — Assemble the theorem
