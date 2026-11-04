# Reproducibility scope

| Workflow | Public evidence and requirements |
|---|---|
| Controlled OEM and optical geometry | Python, NumPy and SciPy reproduce parser checks and short-window and illumination behaviour with synthetic inputs |
| Independent analytical formulas | Controlled closed-form comparisons exercise the included analytical subset |
| Single-target gap aggregation | Six saved daylight windows reproduce the complete gap arithmetic for one Sidi Bibi target |
| Aggregate agricultural results and figures | Saved numerical records and visualisations are available for inspection |
| Native GMAT propagation | The mission script is inspectable and runnable with external GMAT R2026a and its model data |
| Full OEM and agricultural coverage analysis | Requires the omitted target geometries, kernels and reference products |
| Publications | The three accepted PDFs and their public evidence links are supplied. A complete LaTeX build is outside the current distribution. |
| Complete analytical companion | Requires the internal reference inputs and companion workflow. The public formulas and tests cover a subset. |
| Physical and operational validation | Outside the available evidence |

The [public examples](studies/2A-orbital-analysis/docs/REPRODUCING_PUBLIC_EXAMPLES.md) run with the documented Python environment. The controlled OEM is labelled NOT_GMAT and is an artificial parser fixture. Its geometry and illumination vectors are synthetic. The saved-event calculation repeats the aggregation of one target's intervals. Independent event discovery and a search across the agricultural mask require the complete study inputs.

See [complete-study input requirements](studies/2A-orbital-analysis/docs/INTERNAL_REPRODUCTION_REQUIREMENTS.md) and the [public evidence index](studies/2A-orbital-analysis/documents/PUBLIC_EVIDENCE_AVAILABILITY.md).
