# Final QA — Public RC v0.2

**PASS for manual publication review. No Git initialization, repository creation, commit, push or publication was performed.** No project licence was introduced or changed. No GMAT, orbital/access/coverage/revisit or GIS analysis was rerun.

| Check | Result / evidence |
|---|---|
| Preservation | All **4,340** protected original files retain their intake path/size/SHA-256: outputs 3,615; accepted master 650; RC v0.1 67; original root files 8 |
| Publications | Three distinctly named public derivatives included with paired TeX; page counts **1 / 21 / 49** |
| Scientific content | All original glyphs/positions retained at 0.01 pt; every original page media box equal; all equations, numbers, conclusions and the negative ≤72-hour verdict retained |
| Rendered comparison | **66/71 pages pixel-identical at 72 dpi**; five differ only in documented added-notice areas; the five changed pages visually inspected |
| Figures | **16/16** supplied accepted assets byte-identical; no map, coastline, locator, globe, timeline or Figure 4 edit |
| Publication build | All three TeX sources compile with Tectonic 0.17.0 in an independent relative-path build tree; all required publication assets supplied; standard AMSFonts fallback documented |
| PDF/local links | All active relative PDF, Markdown, HTML-image and TeX dependency targets resolve; original external URLs/contact destinations preserved |
| Public tests | **39/39 PASS**, isolated Python **3.12.14**, NumPy **2.5.4**, SciPy **1.18.1** |
| Numerical examples | All three public example JSON payloads exactly equal RC v0.1; six saved windows reaggregate **312.21995813943926 h** with zero saved-scalar residual |
| Scientific/native source | 20 native/scientific/example/config/data files unchanged from RC v0.1; 23 exact analytical function bodies still hash-checked |
| AST portability | Structural hash no longer uses ast.dump; added regression verifies dump-format independence without removing exact-source identity checks |
| Privacy/dependencies | No personal absolute paths, unapproved contacts, credential markers, private logs or raw geographic/kernel payloads found by bounded static checks; approved publication contact intentionally retained |
| Attribution | Seven provider families reviewed; existing notices retained; only missing notice details added; no specific unresolved rendered-figure issue identified |
| Inventory | PUBLIC_FILE_SELECTION.csv gives source/destination/hash/purpose/status; MANIFEST.sha256 covers all staged files except itself; review ZIP is verified against staged member hashes |

## Practical limits

The public examples reproduce controlled algorithms and saved-event aggregation, **not the full agricultural scientific study**. Its raw geographic database, kernels, full states/access histories and complete analytical companion/test suite are excluded. Numerical verification does not establish physical payload/ADCS performance, a feasible observation schedule, usable imagery or guaranteed mission revisit.

Native Python 3.13 was not executed because its local interpreter was unavailable. Python 3.12 remains the tested contract. Fresh network pip installation and POSIX execution were not tested; the isolated Windows environment was seeded offline with the specified distributions and PYTHONPATH cleared. Standard publication software/fonts are external dependencies, not redistributed binaries. External scientific URLs were preserved and selected provider requirements checked; universal future web availability is not guaranteed.

The accepted source PDFs/TeX, frozen releases and RC v0.1 remain unchanged. Added credits and availability notes are publication-only changes. Full details are in [PDF_PUBLICATION_DIFF.md](PDF_PUBLICATION_DIFF.md), [CARTOGRAPHIC_ATTRIBUTION_AUDIT.md](CARTOGRAPHIC_ATTRIBUTION_AUDIT.md), [dependency/privacy audit](DEPENDENCY_AND_PRIVACY_AUDIT.md) and the study's [QA directory](studies/2A-orbital-analysis/qa).

No technical publication blocker remains within this subset's stated scope. **Manual author publication approval is still required before any GitHub action.**
