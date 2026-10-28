# Rebuild the public PDFs — no scientific execution

Run from the repository root. The paired public TeX sources, all 15 accepted active figure assets, selected evidence sidecars and existing third-party notices are supplied. No private master, raw GIS, SPICE kernel, GMAT execution, QGIS processing or scientific calculation is needed.

Tested compiler: Tectonic 0.17.0, XeTeX/default bundle v33. Standard TeX packages and fonts are external software; a fresh installation may need network access to obtain them. No fonts or compiler binaries are redistributed.

    .\.venv\Scripts\python.exe -B tools/build_publications.py --tectonic tectonic --destination working/publications_001

If an incomplete offline bundle is missing standard AMS Type 1 fonts, use the optional --font-directory argument pointing to an existing standard AMSFonts directory. The tested environment used that fallback, without font substitution. The script refuses an existing destination, writes only into the new build folder and does not replace repository PDFs.

The output directory contains documents/, figures/, evidence/ and third_party/ for compilation, plus BUILD_RESULTS.json and compiler logs. It is a publication build workspace, not a separate copy of the entire scientific repository.

The expected outputs are 1, 21 and 49 pages. The public derivatives are not byte-identical to the accepted PDFs because notices/relative links and PDF metadata differ. Scientific body/figure/layout equivalence and exact exceptions are recorded in the root PDF_PUBLICATION_DIFF.md and qa records.

For optional PDF-link verification after installing pypdf:

    .\.venv\Scripts\python.exe -m pip install -r studies/2A-orbital-analysis/requirements-publication-qa.txt
    .\.venv\Scripts\python.exe -B tools/verify_candidate.py --pdf-links

The ordinary public numerical examples continue to require only NumPy/SciPy.
