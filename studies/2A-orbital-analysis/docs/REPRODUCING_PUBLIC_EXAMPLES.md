# Public examples — commands and limits

Use the repository root as the working directory. Python 3.12, NumPy 2.5.4 and SciPy 1.18.1 are the tested software contract. No kernels, raster/vector data, private paths or network service are read by the three public examples.

## Windows PowerShell

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r studies/2A-orbital-analysis/requirements-public.txt
    .\.venv\Scripts\python.exe -B studies/2A-orbital-analysis/examples/controlled_geometry.py
    .\.venv\Scripts\python.exe -B studies/2A-orbital-analysis/examples/analytical_checks.py
    .\.venv\Scripts\python.exe -B studies/2A-orbital-analysis/examples/replay_saved_gap.py
    .\.venv\Scripts\python.exe -B -m unittest discover -s studies/2A-orbital-analysis/tests -v
    .\.venv\Scripts\python.exe -B tools/verify_candidate.py

## POSIX equivalent

    python3.12 -m venv .venv
    .venv/bin/python -m pip install -r studies/2A-orbital-analysis/requirements-public.txt
    .venv/bin/python -B studies/2A-orbital-analysis/examples/controlled_geometry.py
    .venv/bin/python -B studies/2A-orbital-analysis/examples/analytical_checks.py
    .venv/bin/python -B studies/2A-orbital-analysis/examples/replay_saved_gap.py
    .venv/bin/python -B -m unittest discover -s studies/2A-orbital-analysis/tests -v
    .venv/bin/python -B tools/verify_candidate.py

The POSIX commands are documented equivalents, not a claim that a POSIX environment was executed during this review. Environment activation is optional; explicit interpreter paths prevent accidentally using a different Python.

## Expected behaviour

1. **controlled_geometry.py:** parse the clearly marked two-row artificial OEM fixture; construct a linear terrestrial test path; detect three roll-case windows with duration below 2 ms, although neither endpoint sample sees the narrow slit; distinguish synthetic day and night Sun vectors. This is a controlled geometry test, not a GMAT ground track or observed scene.
2. **analytical_checks.py:** compare the independent universal-anomaly formula with a controlled circular closed form. It uses toy inputs, does not read saved mission states and does not integrate a force model. Residual assertions are 1e-8 km position and 1e-10 km/s velocity.
3. **replay_saved_gap.py:** read six genuine saved point windows and recompute their complete exit-to-next-entry gap. Expected maximum: 312.21995813943926 h; residual against the included saved scalar: 0 h; the 72-hour failure flag is true. This is saved-event aggregation, not independent event detection or a full-ROI worst-case search.
4. **Tests:** 39 tests: 24 retained parser/geometry/metrics tests with import/config path changes, plus 15 public-scope/formula/example tests. The private 45-test analytical suite and full-ROI regression are not bundled or claimed.

Examples print JSON and do not overwrite included reference inputs. Runtime outputs, environments and caches are ignored by the proposed .gitignore. No disk result cache is used.

The public data file data/published_results.json and the included result figures are archived study summaries. Displaying or checking their saved numbers does not reproduce their underlying full-dataset calculations.

## Optional full OEM source interface

The full parser/frame/access modules are included for engineering inspection, separately from the reproducible examples. To inspect their CLI after installing optional dependencies:

    .\.venv\Scripts\python.exe -m pip install -r studies/2A-orbital-analysis/requirements-optional-oem.txt
    .\.venv\Scripts\python.exe -B studies/2A-orbital-analysis/src/analyze.py --help

A real execution requires an explicit OEM, geographic targets and a reviewed complete analysis configuration with kernel/geographic hash pins. None is silently substituted from the private workspace. config/optical_geometry.json is only a controlled-example configuration, not a complete OEM workflow configuration. See INTERNAL_REPRODUCTION_REQUIREMENTS.md.
