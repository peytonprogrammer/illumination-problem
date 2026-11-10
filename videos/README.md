# Illumination explainer videos

Narrated mathematical explainers with the editable HyperFrames projects used to make them.

| Video | Length | Manuscript | Editable project |
|---|---:|---|---|
| [The 22-sided dark room](dark-room-22/dark-room-22.mp4) | 8:37 | [PDF](../preprints/twenty-two-wall/manuscript.pdf) | [Source and transcript](dark-room-22/README.md) |
| [When darkness is impossible](eight-wall-illumination/eight-wall-illumination.mp4) | 9:00 | [PDF](../preprints/eight-wall/manuscript.pdf) | [Source and transcript](eight-wall-illumination/README.md) |
| [Light through comb rooms](comb-illumination/comb-illumination.mp4) | 8:30 | [PDF](../preprints/middle-row-combs/manuscript.pdf) | [Source and transcript](comb-illumination/README.md) |
| [Why a longer corridor guarantees a route](long-neck-illumination/long-neck-illumination.mp4) | 9:00 | [PDF](../preprints/long-neck-networks/manuscript.pdf) | [Source and transcript](long-neck-illumination/README.md) |
| [Light through a twelve-wall corridor](twelve-wall-corridor/twelve-wall-corridor.mp4) | 9:30 | [PDF](../preprints/twelve-wall-corridor/manuscript.pdf) | [Source and transcript](twelve-wall-corridor/README.md) |
| [The ten-wall spiral puzzle](ten-wall-spirals/ten-wall-spirals.mp4) | 10:00 | [PDF](../preprints/ten-wall-spirals/manuscript.pdf) | [Source and transcript](ten-wall-spirals/README.md) |

The spiral video explains the tall-or-wide all-real theorem and the separate coprime thin-cap native-pair theorem. The long-neck video explains the two-chamber proof and briefly summarizes the separate conditional network theorem. The twelve-wall corridor video maps the analytic and computer-assisted proof for lower-to-upper outer-chamber pairs. The eight-wall video is a proof map with selected constructions. The comb video covers the central matching proof and its stated endpoint class. The dark-room video covers the parity and reversal arguments. Read each manuscript for the exact theorem and full proof.

## What HyperFrames source means

The native source is HTML/CSS/JavaScript: `index.html` mounts scenes from `compositions/`, whose SVG diagrams and paused GSAP timelines define every frame. Narration audio, scripts, timings, chapter markers, and project configuration are included. Open a project's README for preview and render commands. Python is used only by the shared delivery-render helper; it is not needed to edit scene HTML.

[manifest.json](manifest.json) binds each MP4 to its duration, scope, HyperFrames version, manuscript source hash, and delivered video checksum. Each film's `SOURCES.md` identifies its mathematical source. These videos explain working manuscripts; they do not replace mathematical refereeing.
