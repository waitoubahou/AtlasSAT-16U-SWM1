# Assumptions and mathematical limitations — Document 2A-2 v0.1

## Governing mission assumptions retained

- Canonical epoch: 2026-10-20 12:00 UTC. Initial EarthMeanOfDate/MODEq elements: SMA 6928.1363 km, eccentricity 0.001, inclination 97.5°, RAAN 6.463170753756°, AOP/TA 0°/0°.
- JGM2 gravity at degree/order 2/0, μ=398600.4415 km³/s², radius 6378.1363 km, normalized C20 converted to J2=0.001082626724392697. Drag, SRP, relativity, tides and third-body forces are absent from the retained model.
- PrinceDormand78, nominal 30 s maximum internal step and 1e−11 accuracy; refined 15 s / 1e−12; native OEM 30 s Lagrange-order-7 exports are distinct from internal reports.
- Earth-fixed optical geometry uses the frozen ITRF93 postprocessing with bias/state-rotation derivative. Earth orientation is predicted over the study; no EOP is updated.
- WGS84 smooth, zero-height targets, aE=6378.137 km, f=1/298.257223563. This geometric radius is 0.7 m different from the gravity reference radius intentionally.
- Nominal 30 km angular swath at 550 km, provisional 10 m along-track projected slit, ideal 0°/±10°/±20° independent-per-target roll. None is a qualified instrument/control capability.
- Geometric solar centre elevation ≥0°, with archived ≥10° sensitivity. No 20° or 30° Sun-elevation sensitivity is invented.
- Fixed provisional agricultural mask and exact saved target weights; no geometry or classification change. Missing greenhouse-source footprint, uncertain source vintages/local accuracy, and all original caveats remain.

## Independent work versus shared evidence

| Calculation | Independent component | Shared/conditional component |
|---|---|---|
| Initial Cartesian state | Explicit conic/rotation equations and IAU76 polynomial | Canonical element values and GMAT's documented MODEq Rdot≈0 convention |
| Two-body solution | Universal anomaly/Lagrange coefficients; controlled eccentric/circular examples | Archived initial state for the trajectory comparison |
| J2 force/rates | Potential differentiation and Hamiltonian averaging | Adopted JGM2 constants and approximate fixed symmetry pole |
| Native refinement | Independent parsing and vector norms | Two already generated GMAT ephemerides |
| RAAN fits | Independent element extraction and regression | Same GMAT state history |
| Energy-based average-SMA prediction | Independent first-order energy averaging and linearization | Fixed-pole approximation; not a full mean-element transformation |
| Mean-SMA timing diagnostic | New arithmetic in the first-order equation | Saved time-average osculating SMA is not independently derived canonical mean SMA |
| Recurrence scale | Algebra and units | Saved nodal period and finite-interval fitted node rate |
| Local access example | Eight-point polynomial, differentiated velocity, own bisection and ray quadratic | Saved terrestrial knots and original targets; two examples only |
| Approximate daylight | Separate NOAA series implementation | Same event times/coordinates; approximation is not a precision solar ephemeris |
| Exact/censored gaps | Independent interval merging and arithmetic | Every opportunity is read from the saved event set |
| Whole-ROI coverage | Different event-to-hourly-start union/difference-array algorithm | Original 14,494 target weights, saved event midpoints and daylight flags |

No production helper is imported and no GMAT executable is invoked. Independently implemented methods do not mean an independent human reviewer has accepted this new calculation book.

## Mathematical limitations register

1. A first-order mean-element theory is not an exact equation for initial osculating elements. Its nodal-period mismatch is documented rather than tuned away.
2. Mean-anomaly/perigee rates at low eccentricity should be interpreted through a nonsingular combination; a precise physical apsidal-precession claim is not made.
3. Fitted EME2000 osculating RAAN slopes and mean-equator secular theory have different averaging/frame definitions; their residual is contextual, not an integrator-error estimate.
4. The saved initial LTDN residual is a numerical clock calculation under an approximate UTC/UT1 convention, not physical submicrosecond accuracy.
5. Earth orientation model-version differences are not truth-error bounds; future EOP is predicted.
6. The approximately 15-day comb is not an exact repeating-ground-track orbit. Its longitude displacement is not perpendicular swath spacing and does not include the entire discrete/daylight event geometry.
7. The legacy daily-comb displacement differs from the literal 15-orbit block remainder when the relative rotation rate differs from 360°/day. Both definitions are shown.
8. Adding flat swath half width to h tan(roll) is a further approximation to h tan(roll+half-FOV); neither scalar hand estimate reproduces exact ellipsoid access.
9. A root tolerance controls the selected interpolated equation, not physical position/orientation error; grazing roots may be ill-conditioned.
10. Two local event checks do not prove exhaustive global event discovery. Historical broader numerical checks are cited as R evidence, not rerun here.
11. Saved daylight flags use entry/midpoint/exit Sun sampling, not an exhaustive continuous-minimum proof. The worked examples are far from a terminator.
12. NOAA solar differences of tenths of a degree are expected for a gross approximation; this check verifies sign/scale only.
13. Endpoint subtraction verifies a duration, not absence of omitted intervening opportunities.
14. A fully censored 720 h span is not a complete recurrence and is not counted twice. Observed spans greater than 72 h establish finite-span failure; a finite sample cannot establish universal all-season compliance.
15. Hourly-start rolling coverage uses midpoint membership in closed windows. Interval-overlap coverage and continuous-start coverage are different estimators.
16. Exact agricultural area weights do not make representative points equivalent to full-cell image coverage. Fine-grid mean convergence does not certify every field edge or crop class.
17. The primary 396.47 km² research mask is not an official or locally validated current agricultural census. Greenhouse-source omission percentages do not estimate missing hectares.
18. Numerical state agreement, software-transfer tests and this independent calculation companion do not establish operational imaging feasibility, clouds, SNR/MTF, slew/settle, attitude accuracy, orbit determination accuracy or flight qualification.
19. The inherited v0.2 integrity discrepancy remains documented. Complete original ZIP members are copied only into the new verification package; no original is repaired.
20. Source-hosted full IERS/CCSDS PDFs were not fully retrievable through web research; no numerical conclusion relies on an unread PDF. Installed GMAT documentation, actual source outputs and directly consulted primary references provide the used evidence.

## Controlled outcome

The negative ≤72-hour daylight-revisit verdict is preserved. No mission configuration, constellation, drag model, observation schedule, ADCS or communications analysis is performed. Any later use of these derivations in 2A-1 requires separate engineering review and a new publication revision.


## Additional v0.2 boundaries

- Models A/B use the archived mean descending-node period. The three-and-three ±20° cluster occupancy is observed, not independently derived from rational arithmetic.
- 226/15 is a user-proposed near-return candidate checked retrospectively with actual node counts and a small-denominator rate calculation. Its longitude closure is nonzero; it is not an exact repeating orbit.
- The 196-period estimate is conditional on occupancy. The narrower ±10° envelope has two-and-one occupancy and a 226-cycle long gap.
- Newly counted nodes are independent arithmetic on frozen numerical states. ITRF93 and EME2000 equators differ; only integer associations coincide for the selected events. The 30/60-second interpolation test does not qualify the underlying orbit/orientation.
- The exact node-span/event-phase residual decomposition is a reconstruction using archived event times. It explains the discrepancy, not independent event discovery.
- The absolute-phase route receives no saved optical-event anchor, saved mean nodal period, fitted numerical RAAN rate or phase offset. It uses a previously derived first-order energy estimate, not a complete canonical osculating-to-mean transformation.
- UT1≈UTC and mean-sidereal/moving-equator geometry are analytical simplifications. Eccentric radial motion, nutation, polar motion and short-period corrections are omitted. Subsecond centre agreement can include cancellation.
- A 120/60-second candidate scan comparison checks the smooth approximate fan-zero model only. It does not replace the validated production solver or prove millisecond optical entry/exit or all-ROI completeness.
- Conditional saved-midpoint-plus-226T recurrence is level C. It must not be relabelled an independent absolute-phase prediction.
- No new state propagation, access history, physical instrument/ADCS qualification or observation schedule is produced. The frozen negative ≤72-hour daylight-revisit verdict remains.
