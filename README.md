# AtlasSAT-16U-SWM1

**Souss Water Management 1 — 16U Earth Observation Spacecraft**

**Project status:** Work in progress

AtlasSAT-16U-SWM1 is an independent spacecraft engineering project investigating a 16U Earth observation satellite for agricultural and water-resource monitoring in the Souss-Massa region of Morocco.

[Engineering portfolio](https://waitoubahou.github.io/projects/atlassat-16u/) · [Study 2A · Orbital Analysis](studies/2A-orbital-analysis/README.md)

## Mission

The mission concept uses visible and near-infrared imaging to support agricultural monitoring and water-resource assessment in the Chtouka-Massa plain. The reference payload is a five-band VNIR pushbroom imager. The project investigates how the observation requirements drive orbit selection, spacecraft configuration, subsystem packaging and analysis.

## Spacecraft Configuration

| Item | Reference configuration |
|---|---|
| Spacecraft class | 16U CubeSat |
| Mission | Agricultural and water-resource monitoring |
| Region of interest | Chtouka-Massa agricultural plain, Souss-Massa, Morocco |
| Reference orbit | Approximately 550 km near-Sun-synchronous orbit at 97.5° inclination |
| Payload concept | Five-band VNIR pushbroom imager with a nominal 30 km nadir swath |
| Mechanical architecture | Longitudinal rails, end plates, bulkheads and side panels with stacked subsystem volumes |
| Design environment | CAD assembly and finite-element analysis for mechanical studies, GMAT R2026a and Python for orbital analysis |
| Current maturity | Preliminary spacecraft configuration with the orbital analysis published |

## Engineering Programme

| Document | Study | Status |
|---|---|---|
| 1A | Mission Overview | Planned |
| 1B | Requirements | Planned |
| 2A | [Orbital Analysis](studies/2A-orbital-analysis/README.md) | Published |
| 3A | Structural Assembly & Drawings | Planned |
| 3B | Quasi-static Structural Analysis | Planned |
| 3C | Modal Analysis | Planned |
| 3D | Thermal Analysis | Planned |
| 4A | Preliminary System Model | Planned |

Publication status refers to controlled technical documents. Preliminary engineering work may exist before a document is released.

## Published Engineering Work

### Study 2A · Orbital Analysis

Study 2A combines GMAT R2026a propagation, Python analysis with NumPy and SciPy, and independent analytical checks. For the nominal 30 km swath and ideal ±20° roll case, the maximum complete daylight no-access interval is **312.22 h**. The **≤72 h daylight revisit requirement is NOT MET**. See the [Study 2A methods and results](studies/2A-orbital-analysis/README.md).

## Technical Documentation

| Document | Publication |
|---|---|
| 2A | [Orbital analysis summary](studies/2A-orbital-analysis/documents/AtlasSAT_2A_Orbital_Analysis_OnePager_RevD3_4_Editorial_Rev1.pdf) |
| 2A-1 | [Orbital verification, coverage and revisit](studies/2A-orbital-analysis/documents/AtlasSAT_2A-1_Orbital_Analysis_RevD3_5_Editorial_Rev1.pdf) |
| 2A-2 | [Analytical derivations and independent verification](studies/2A-orbital-analysis/documents/AtlasSAT_2A-2_Analytical_Derivations_v0.2.1_Editorial_Rev1.pdf) |

## Project Documentation

- [Contributions and attribution](ATTRIBUTION.md)
- [Publication history](PUBLICATION_HISTORY.md)
- [Figure and data source notices](studies/2A-orbital-analysis/figures/README.md)
