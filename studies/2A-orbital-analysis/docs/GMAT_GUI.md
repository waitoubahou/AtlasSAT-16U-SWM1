# Native GMAT GUI-first model

The included script is the accepted portable nominal mission from Master Release v1.0. It is human-readable, with spacecraft, force model, propagator, report, OEM and visualisation resources. No Python is required to inspect it.

| GUI resource | Preserved configuration |
|---|---|
| AtlasSAT16U / Orbit | 20 October 2026 12:00:00 UTC; EarthMeanOfDate/MODEq; SMA 6928.1363 km, eccentricity 0.001, inclination 97.5°, RAAN 6.463170753756°, AOP/TA 0° |
| AtlasEarth / AtlasProp | Earth JGM2 degree 2/order 0; drag/SRP/tides/relativity/third bodies disabled; PrinceDormand78, 30 s initial/max step, 0.001 s minimum, requested accuracy 1e-11 |
| Mission sequence | Stop at 2592000 elapsed seconds |
| AtlasOEM | EarthMJ2000Eq/EME2000, UTC CCSDS OEM, km and km/s, 30 s output, Lagrange order 7 |
| AtlasStates | Native A1/elapsed and Cartesian diagnostic report; EarthFixed columns are not the Python ITRF93 transform |
| AtlasOrbit / AtlasGroundTrack | Orbital visualisations, not optical coverage maps |

**Before a future manual execution**, configure fresh output filenames from the repository root:

    & ./studies/2A-orbital-analysis/tools/Configure-GMAT.ps1 -RunName my_nominal_001

This setup writes only a new working script, changes two Filename properties and does not launch GMAT. The helper refuses an existing run directory. Open the printed script using GMAT R2026a File > Open. Inspect/change native resources intentionally, then press F5 only if you intend a new run. Repeating an existing GMAT output filename can overwrite that working run; use a new configured name.

The portable source's bare filenames must not be run blindly against an installation's default output directory. No script in this public tree names a historical/master destination.

This release preparation **did not launch or execute GMAT**. GUI execution/equivalence evidence belongs to the accepted internal master, not to a new public-candidate run. GMAT R2026a and its gravity/time/orientation resources are external software; binaries and kernels are not redistributed. Preserve and record installation/data versions for new work.

In the accepted environment, an installed plugin converted OrbitView to OpenFramesInterface. Its OEM writer needed closing/reopening after mission completion to finalize buffered output. The strict OEM reader checks complete duration/cadence/metadata before analysis.

Changing epoch, altitude, inclination or initial elements does not recalibrate LTDN automatically or preserve numerical equivalence. SMA is Earth-centred distance, not altitude. The initial-TA study is not a pure phase comparison at fixed mean orbit.
