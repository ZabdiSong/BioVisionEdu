# BIOVISION validation report

Validated on 2026-10-06 using Chrome for Testing 151.0.7922.34 with Playwright. **118 automated checks passed**, with no uncaught browser errors, missing runtime requests or external runtime requests. Screenshot views were also inspected.

## Website checks

- All 16 lessons load five guiding questions, steps, a rendered model and three checks.
- Course and question IDs, options, correct-answer indices and explanations are consistent.
- Definition dialogs, five-question controls, ETC step clips and model selection/reset work.
- Incorrect answers show explanations and appear in review. Correct reviews reschedule; due reviews return at the scheduled time.
- Notes, tags, completion and bookmarks survive refresh.
- Search results navigate to the selected concept; all four model dialogs expose Blender downloads.
- Scope/difficulty limit question counts to available questions; a known-answer session returns its expected score.
- Adaptive practice raises difficulty after two correct answers and lowers it after an incorrect answer.
- A timed session resumes after refresh, expires, and reports unanswered questions.
- JSON export/import restores saved data; invalid backups are rejected without replacing current data. Malformed saved sessions are discarded and answer correctness is recomputed.
- Discussion drafts render user text safely and remain on the device.
- Sequence activities recognize both incorrect and correct orders and support movement controls.
- Main pages and Gallery views have no horizontal page overflow at 1440, 390 and 320 pixel widths.
- Actual course/3D rendering and a scored quiz work directly through `file://`, with external requests blocked.

Raw check results: [qa-results.json](qa-results.json). Optional reproduction source: `tools/verify_site.cjs`, using Playwright and a Chrome/Chromium browser supplied by the development environment. `PLAYWRIGHT_MODULE`, `CHROME_EXECUTABLE` and `BIOVISION_ROOT` may be specified when using custom installations. The website itself does not require these developer tools.

## Blender checks

The four native `.blend` files were created with Blender 4.2.0, reopened using Blender's own loader, and checked for nonempty meshes. Each corresponding GLB has a valid `glTF` header. No mesh has animation data. The reusable validation script is `tools/verify_models.py`.

| Native file | Mesh objects checked |
| --- | --- |
| chloroplast.blend | 9 |
| light-reactions.blend | 13 |
| mitochondrion.blend | 11 |
| respiratory-etc.blend | 13 |

The geometry is instructional, not an atomic model or a biological simulation.

## Practical limits

Responsive checks used desktop Chrome at mobile-sized viewports, not every physical phone or browser. Local-storage support and WebGL depend on the user's browser; the site provides a storage notice and 3D fallback where unavailable. Headless tests verify loading and interactions; they do not establish learning gains or validate the unfinished supplied animation content. No remote accounts, classroom service, GitHub repository or public deployment was tested or created.
