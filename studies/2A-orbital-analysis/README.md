# Study 2A · Orbital Analysis

Study 2A assesses whether a single AtlasSAT spacecraft can meet the daylight revisit objective over agricultural targets in Chtouka-Massa, Morocco.

## Reference Configuration

| Element | Model input |
|---|---|
| Reference orbit | Approximately 550 km near-Sun-synchronous orbit at 97.5° inclination with a 10:30 target local mean time of descending node |
| Propagation | GMAT R2026a, 30 days, J2 gravity using Earth JGM2 degree 2 and order 0 |
| Payload concept | Five-band VNIR pushbroom imager |
| Optical geometry | Nominal 30 km nadir swath, 5–10 m target nadir ground sampling distance and 10 m provisional along-track ground sample |
| Pointing cases | Nadir reference and ideal independent ±10° and ±20° roll sensitivities |
| Target set | Provisional agricultural research mask within a seven-commune study boundary |

## Analysis Workflow

1. Propagate the [reference orbit in GMAT](simulation/GMAT/AtlasSAT_Nominal_30days_GUI.script) and export UTC EME2000 states in CCSDS OEM format.
2. Transform the exported states to the terrestrial ITRF93 frame in the [Python pipeline](src/atlas_analysis/pipeline.py).
3. Interpolate the terrestrial states and refine crossings of the pushbroom footprint boundaries. Classify daylight using the solar-centre elevation criterion at entry, midpoint and exit.
4. Compute area-weighted rolling coverage and complete no-access intervals from the end of one opportunity to the start of the next. Report record-edge censoring and targets with no access separately.
5. Compare selected orbital, optical and revisit calculations with [independent analytical checks](evidence/ANALYTICAL_COMPARISON.csv).

## Key Assumptions and Limitations

- The agricultural mask is provisional. Incomplete greenhouse source coverage affects the southern part of the study area.
- Terrestrial coordinates use Earth orientation data that include predictions.
- The roll sensitivities represent independent reachability at each target. The optical model uses a provisional ground sample. Optical IFOV and line acquisition rate are separate quantities.
- Payload performance, attitude determination and control, image quality and operational scheduling remain unvalidated.

See the [scientific limitations](evidence/SCIENTIFIC_LIMITATIONS.md) for the initial true-anomaly sensitivity at fixed osculating inputs, the treatment of censored intervals and the historical seven-day archive exception.

## Key Results

| Measure | Result |
|---|---|
| Daylight revisit requirement | ≤72 h |
| Maximum complete daylight no-access interval | **312.22 h** for the nominal 30 km swath and ideal ±20° roll |
| Worst-case sampled agricultural target | Sidi Bibi |
| Requirement verdict | **NOT MET** |

Even in the ideal ±20° case, the minimum area coverage across rolling 72 h daylight windows is 0%. The historical reference point is excluded from the agricultural gap calculation. The result concerns modelled daylight opportunity under the stated assumptions. An achievable imaging schedule requires separate operational validation. [Saved results](data/published_results.json) · [Result traceability](evidence/RESULT_TRACEABILITY.csv) · [Gap and censoring figure](figures/04_gap_evidence.png)

## Figures

| Chtouka-Massa study region | Near-Sun-synchronous reference orbit |
|---|---|
| <img src="figures/11_Technical_Atlas_Compact_RevD3_2.png" width="300" alt="Technical atlas showing the seven-commune study boundary and provisional agricultural mask"> | <img src="figures/10_Orbital_Globe_Compact_RevD3_4.png" width="400" alt="Orbital globe showing the reference trajectory and Chtouka location"> |

## Publications

| Document | Publication |
|---|---|
| 2A | [Orbital analysis summary](documents/AtlasSAT_2A_Orbital_Analysis_OnePager_RevD3_4_Editorial_Rev1.pdf) |
| 2A-1 | [Orbital verification, coverage and revisit](documents/AtlasSAT_2A-1_Orbital_Analysis_RevD3_5_Editorial_Rev1.pdf) |
| 2A-2 | [Analytical derivations and independent verification](documents/AtlasSAT_2A-2_Analytical_Derivations_v0.2.1_Editorial_Rev1.pdf) |

## Repository Contents

| Path | Contents |
|---|---|
| [`simulation/GMAT/`](simulation/GMAT/) | Native GMAT mission |
| [`src/`](src/) | OEM processing, access geometry, revisit metrics and analytical formulas |
| [`figures/`](figures/) | Regional maps, orbit illustrations and result plots |
| [`data/`](data/) and [`evidence/`](evidence/) | Public example inputs, saved results, comparison records and limitations |
| [`documents/`](documents/) | Publications and the evidence index |

## Reproducibility

The public examples exercise the geometry, analytical formulas and gap aggregation from six saved daylight windows. Reproducing the full agricultural coverage study requires the archived target geometries, kernels and reference products.

- [GMAT GUI mission and output setup](docs/GMAT_GUI.md)
- [Python examples and test commands](docs/REPRODUCING_PUBLIC_EXAMPLES.md)
- [Reproducibility scope](../../REPRODUCIBILITY_SCOPE.md)
- [Public evidence index](documents/PUBLIC_EVIDENCE_AVAILABILITY.md)

## Data and Figure Sources

Map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) (ODbL). Natural Earth context is public domain. © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium. [Figure source notices and crop-data credits](figures/README.md)

Relief produced using Copernicus WorldDEM-30 © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018, provided under COPERNICUS by the European Union and ESA; all rights reserved. The organisations in charge of the Copernicus programme by law or by delegation do not incur any liability for any use of the Copernicus WorldDEM-30.
