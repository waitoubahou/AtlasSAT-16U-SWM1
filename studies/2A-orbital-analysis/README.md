# Study 2A · Orbital analysis

Study 2A evaluates optical access and daylight revisit for the conceptual AtlasSAT-16U-SWM1 mission over agricultural targets in Chtouka-Massa. The study compares nadir access with ideal independent roll sensitivities and verifies selected numerical results against analytical models.

## Model and methods

| Element | Study configuration |
|---|---|
| Orbit | Approximately 550 km, 97.5° inclination and 10:30 target local mean descending-node time |
| Propagation | GMAT R2026a, nominal 30 days, Earth JGM2 degree 2/order 0 |
| Payload concept | Five-band VNIR pushbroom, nominal 30 km nadir swath, 5–10 m target nadir GSD |
| Optical geometry | Provisional 10 m along-track ground sample. Ground sampling distance, optical IFOV and line acquisition rate are distinct. |
| Pointing | Nadir reference and ideal independent ±10° and ±20° roll sensitivities |
| Targets | Provisional seven-commune boundary and agricultural research mask |

The [native GMAT mission](simulation/GMAT/AtlasSAT_Nominal_30days_GUI.script) exports UTC EME2000 ephemerides in CCSDS OEM format. The [Python pipeline](src/atlas_analysis/pipeline.py) reads an explicit OEM and transforms the states to ITRF93. The optical solver interpolates terrestrial states and refines crossings of the along-track and cross-track angular boundaries. For daylight, it applies the solar-centre elevation threshold to the minimum of the values at entry, midpoint and exit. Coverage is area-weighted over rolling windows. A complete no-access gap runs from the end of one opportunity to the start of the next. Record-edge censoring and targets with no access are reported separately.

## Findings and limits

**The ≤72-hour daylight revisit requirement is NOT MET.** For the nominal swath and ideal ±20° roll, the maximum complete daylight gap is **312.22 h** at a sampled agricultural target in Sidi Bibi. The historical reference point is outside this calculation. Minimum area coverage across rolling 72-hour daylight windows is **0%**. See the [saved aggregate results](data/published_results.json), [result traceability](evidence/RESULT_TRACEABILITY.csv) and [analytical comparisons](evidence/ANALYTICAL_COMPARISON.csv).

Numerical verification tests the stated models and implementations. Geometric reachability describes intersection with the modelled footprint. Daylight optical opportunity applies the solar elevation criterion. Physical and operational validation would require evidence of payload performance, image quality, attitude control and an achievable observation schedule.

The provisional agricultural mask, incomplete southern greenhouse source, predicted Earth orientation and ideal roll limit the interpretation. The TA=90° case varies initial true anomaly at fixed osculating inputs. See the [scientific limitations](evidence/SCIENTIFIC_LIMITATIONS.md) for phase interpretation, censoring and the historical seven-day archive exception.

## Publications and public reproduction

The [publication index](documents/ACCEPTED_DOCUMENTS.md) lists 2A RevD3.4, 2A-1 RevD3.5 and 2A-2 v0.2.1. The [evidence index](documents/PUBLIC_EVIDENCE_AVAILABILITY.md) identifies the public records and the internal references cited by the PDFs. [Figure notices](figures/README.md) document upstream geographic and imagery sources.

The [GMAT guide](docs/GMAT_GUI.md) describes the native scenario and output setup. The [Python examples and tests](docs/REPRODUCING_PUBLIC_EXAMPLES.md) cover controlled geometry, analytical formulas and the six-window saved gap calculation. Full ROI reproduction requires the datasets and reference products listed in [complete-study input requirements](docs/INTERNAL_REPRODUCTION_REQUIREMENTS.md).

See [project attribution](../../ATTRIBUTION.md) for engineering contributions and source credits.
