# Public publication differences — RC v0.2

Accepted master PDFs and TeX were read only. The public copies have distinct `_Public_RC_v0_2` names; accepted revision labels/dates stay unchanged. No scientific result, equation, plot or approved geographic/orbital image was edited.

## Per-document changes

### AtlasSAT_2A-1_Orbital_Analysis_RevD3_5.pdf

- 21 pages before and after.
- Updated cross-publication links. Added missing map-source notice details in unused space on page 9; one evidence-availability note in the bottom margin of page 21. No notice overlay was added to the landscape passage figure; its existing Sentinel/source credit was already adequate.
- PDF subject metadata identifies this public derivative; contact retained by author approval.
- Accepted SHA-256: `841d449c1ef2973a54c57afadf2d183ac86d09ae226fa25b7a0a3e600941f15d`.
- Public SHA-256: `39d6cfd09983e9cc1c28b123a8a85067295360cbecf72e3f346a617e56531781`.

### AtlasSAT_2A-2_Analytical_Derivations_v0.2.1.pdf

- 49 pages before and after.
- Repointed four local evidence links to included saved calculations, comparison CSV (two references) and assumptions. Converted two links to the unavailable full calculation companion/source register into same-colour textual references. Added short availability notes in the bottom margins of pages 3 and 49. Equations, tables and chapter layout remain unchanged.
- PDF subject metadata identifies this public derivative; contact retained by author approval.
- Accepted SHA-256: `ad8f9aa30ec4745450db275dc94020370b238a71517e0b46e5b106bcd96fc81e`.
- Public SHA-256: `6c2500de9e960373ad28aae6a85dbae60d073c58372a31aa4883ebeb4484c83c`.

### AtlasSAT_2A_Orbital_Analysis_OnePager_RevD3_4.pdf

- 1 pages before and after.
- Updated cross-report link; added exact WorldCover acknowledgement, printed OSM copyright URL, linked WorldCereal/Global-PCG-10 CC BY credits and DEM liability sentence in existing whitespace. Appended the Sentinel 2026 notice to the existing source footer. Original main content and footer positions remain unchanged.
- PDF subject metadata identifies this public derivative; contact retained by author approval.
- Accepted SHA-256: `72bacc92c926ed00828dc6e712f2492f6bd78e1d1c3fdc29327b900cad8ce858`.
- Public SHA-256: `43dc05eb49081c7c610d3c09b6d4681b65617e8229c42b0b046782a166a10bff`.

## Measured equivalence

All original PDF glyphs, including numerical values and mathematical characters, remain at their original positions to the 0.01 pt comparison precision. All page media boxes match. At 72 dpi, **66 of 71 pages are pixel-identical**. Differences occur only on one-pager page 1, report pages 9/21 and analytical-book pages 3/49, within the documented new-notice areas. The 15 accepted active figure files and the approved additional compact globe PNG are byte-identical to their preserved sources.

The scientific ≤72-hour daylight verdict, 312.22 h Sidi Bibi gap, timeline, maps, globe, Figure 4 and report Figure 9/page placement are preserved. No orbital, access, coverage, revisit or GIS analysis was run. Publication compilation, public examples and package checks are the only executions.

## Links and evidence boundary

Cross-PDF destinations refer to the three included derivatives. Active local evidence links resolve inside the public tree. The full calculation companion and original source register remain internal, with the preserved visible references explicitly qualified by [the public evidence index](studies/2A-orbital-analysis/documents/PUBLIC_EVIDENCE_AVAILABILITY.md). The public projection `documents/evidence/source_manifest_RevD3_5.json` describes only supplied figure assets; it does not pretend to be the full original private manifest. E01–E18 archive references do not imply that the complete internal archive is distributed.

## Rebuilding

All public TeX dependencies are supplied except documented external standard TeX software/fonts. Rebuilding succeeded in a separate relative-path build tree with Tectonic 0.17.0. A standard AMSFonts fallback was used for the local offline bundle; no fonts were substituted or distributed. See [build instructions](studies/2A-orbital-analysis/documents/BUILD_PUBLICATIONS.md) and [machine-readable QA](studies/2A-orbital-analysis/qa/publication_content_equivalence.json). The original accepted binaries were not replaced.
