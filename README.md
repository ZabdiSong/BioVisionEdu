# BioVision EDU — Cellular Energetics

An interactive, local-first biology unit developed from the supplied BioVision HTML prototype, UI design, teaching outline and learner feedback. This edition completes **Unit 2 · The Cell: Chapters 9–10**, covering cellular respiration and photosynthesis.

## Open the website

Extract the complete package and open **index.html** in a current desktop browser. Keep the folders beside it. No account, API key, installation or internet connection is required for the learning activities. If your browser restricts local-file storage, use a local server:

```sh
python -m http.server 8000
```

Run that command inside the extracted folder, then open `http://localhost:8000`. WebGL is needed for interactive 3D; descriptions and downloads remain available without it.

## What works

- 16 concepts, five guiding questions per concept, step explanations, misconception checks and input/output tables.
- 48 original multiple-choice questions with shuffled choices, explanations and concept links; topic, difficulty, count and time settings.
- Adaptive practice: two consecutive correct responses raise the level; an incorrect response lowers it. Question selection favors weaker concepts. This is a transparent rule-based system.
- A mistake collection and scheduled review after 1, 3, 7, 14 and 30 days of consecutive correct answers.
- Four editable Blender schematics and GLB exports, with rotation, zoom, structure selection, transparency, cutaway and isolation controls.
- Two sequence activities, vocabulary popups, search, notes, bookmarks, tags, completion tracking and JSON progress import/export.
- Existing ETC demonstration clips and supplied project artwork.

## Reserved spaces

Missing lesson photos and unfinished personified/narrated animations have visible placeholders. No new animation was created. The uploaded ETC clips are short demonstrations, not complete lectures. Forum stores your own discussion drafts; shared posts, accounts and classrooms require a future connected edition. Written recall prompts are not automatically graded.

## GitHub upload

See [the Chinese upload guide](docs/GITHUB_UPLOAD_CN.md). Upload the extracted contents, with `index.html` at the repository root. A code repository is a source link; enabling GitHub Pages later provides a browser website link. This package has not been uploaded or published automatically.

## Project files

| Path | Purpose |
| --- | --- |
| `index.html`, `style.css`, `script.js` | Interface and navigation |
| `learning.js` | Local progress, review and quiz rules |
| `viewer.js` | Offline 3D interaction |
| `data/curriculum.json` | Editable lessons, questions and glossary |
| `data/curriculum.js` | Same data as a classic script for local-file use |
| `assets/models/` | Four `.blend`, four `.glb`, web mesh data and manifest |
| `assets/images/`, `assets/videos/` | Supplied artwork and ETC clips |
| `vendor/` | Bundled Three.js and its license |
| `tools/` | Reproducible content/model generators and optional checks |
| `docs/` | Study, upload, materials, models and validation documentation |
| `reference-design/` | Supplied prototype and UI PDF, for reference only |

## Editing

Edit the lesson content in `tools/build_curriculum.py`, then run `python tools/build_curriculum.py` to regenerate both data files and the curriculum summary. Keep `.json` and `.js` synchronized. To add finished media, replace the relevant placeholder in `script.js` with a local file in `assets/`; see the asset gap table.

For Blender generation, run `blender --background --python tools/build_models.py` with Blender 4.2 or newer. The schematics illustrate compartments and components; they are not molecular structures or scale models. Keep the Blender files, GLB files and web mesh bundle in sync after edits.

## Data and sources

Progress is stored in this browser's local storage, without remote transmission or cross-device synchronization. Export from MyBio before changing device or browser. The learning text and questions were written for this build and checked against the supplied Campbell Chapters 9–10. Full textbooks, private interview transcripts and unassigned media are not redistributed in the website package; their input paths are inventoried. See [the source review](docs/SOURCE_REVIEW_CN.md) and [validation report](docs/TEST_REPORT.md).

Three.js is distributed under its included MIT license. Supplied project artwork and original reference files retain their existing rights; this package does not assign a new license to them.
