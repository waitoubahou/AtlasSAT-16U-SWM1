# Dependency and privacy audit — Public RC v0.2

| Workflow | External software | Public input scope |
|---|---|---|
| Three examples and 39 tests | Python 3.12; NumPy 2.5.4; SciPy 1.18.1 | Included synthetic fixture or six saved daylight windows |
| Optional real-OEM source interface | Above plus SpiceyPy 8.3.0 and PyERFA 2.0.1.5 | Requires explicit real OEM, reviewed configuration, geographic inputs and kernels, not supplied |
| Native GUI mission | GMAT R2026a and its runtime/data | Inspectable script; no new execution in this revision |
| Three publications | Tectonic 0.17.0/default bundle v33, standard fonts | All paired TeX and active figures included; independent rebuild passed |
| Optional PDF QA | pypdf 6.10.0; Pillow 13.0.0 for previews | Included publication/figure PDFs |

Python commands explicitly select the intended virtual environment after the Python 3.12 bootstrap. Tests ran in an isolated 3.12 virtual environment, offline-seeded with NumPy/SciPy and their native libraries; PYTHONPATH was cleared. A fresh network pip install and POSIX execution are not claimed. The locally installed 3.13 launcher was inaccessible, so native 3.13 execution is not claimed. The AST check now uses a canonical structural representation independent of ast.dump formatting; the 23 exact function-source hashes are unchanged and still checked. No scientific calculation was changed to accommodate a test.

## Publication and privacy scope

- Author name and the professional email already in the publications are retained with explicit author approval. No extra contact directory is added.
- The three accepted documents are supplied as identified public-distribution derivatives. Every original glyph/position is preserved; only credits, evidence-availability notes, destinations and metadata change.
- Portable source identifiers replace machine-specific locations. Internal reviews, private logs, full geographic databases, raw kernels, compiler files and caches are excluded.
- Static checks inspect textual files, PDF text/metadata/actions, PNG metadata, Python syntax and active local links for personal absolute paths, unapproved contacts and obvious credential markers. This bounded inspection is not a general security certification.
- Generated real-analysis manifests can contain local runtime paths. Future run outputs remain ignored and require review before uploading.
- Runtime packages, fonts, GMAT and compilers are external dependencies; their binaries are not redistributed. The existing Copernicus DEM notice is included only as a third-party notice.

## Source integrity

The GMAT mission and canonical scientific/parser/access modules retain the RC v0.1 content. The prior documented source-directory fingerprint/import-path adaptations remain. The analytical subset retains 23 exact source-function bodies. Only test serialization and release/package documentation changed in RC v0.2. No GMAT run, ROI/access/revisit recomputation, GIS processing or private-data fallback occurred.

There is no new project licence or software grant. See [attribution audit](CARTOGRAPHIC_ATTRIBUTION_AUDIT.md), [publication differences](PDF_PUBLICATION_DIFF.md) and [reproduction scope](REPRODUCIBILITY_SCOPE.md).
