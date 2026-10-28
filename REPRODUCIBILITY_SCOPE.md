# Reproducibility scope

| Level | Included and runnable? | Claim |
|---|---|---|
| Controlled geometry/OEM demonstration | Yes, Python + NumPy/SciPy | Reproduce synthetic parser/short-window/day-night behaviour |
| Independent analytical formula checks | Yes | Reproduce controlled circular-solution checks with unchanged formula bodies |
| Saved single-target gap aggregation | Yes | Recover the gap from six included archived intervals; no independent event discovery |
| Display archived aggregate results/figures | Yes | Inspect saved facts; underlying ROI computation is not reproduced |
| Native GMAT model | Script inspectable; external GMAT required for a future run | No new propagation performed in this candidate preparation |
| Real OEM → transformed states → agricultural ROI coverage | No, essential geographic/kernel/reference data withheld | Full scientific reproduction is not claimed |
| Analytical publication | Yes, complete 49-page PDF/TeX | Read and rebuild the publication; this is not the full executable companion |
| Full analytical companion/original 45-test suite | No, complete private reference bundle excluded | Public formula subset is not the full companion |
| Mission physical/operational validation | No | No flight, payload/ADCS, scheduling or usable imagery validation |

Run [public examples](studies/2A-orbital-analysis/docs/REPRODUCING_PUBLIC_EXAMPLES.md) with the explicit virtual-environment commands. Public files alone plus documented external software suffice for the first three rows. The saved intervals are processed numerical evidence, not new GMAT ephemerides.

The negative ≤72-hour daylight verdict is an accepted archived result. A public reaggregation of one target's supplied windows is not a fresh search for the worst target across the agricultural mask.

The public controlled OEM is labelled NOT_GMAT and must never be used as an orbital baseline. Synthetic paths and solar vectors exist to test algorithms, not to portray actual AtlasSAT passes.

See [internal input requirements](studies/2A-orbital-analysis/docs/INTERNAL_REPRODUCTION_REQUIREMENTS.md) for what complete reproduction needs. There is no automatic private-data fallback, remote dataset fetch, GMAT execution or hidden result-cache reuse in the demonstrated public workflow.

Publication rebuilding is now independently supported; it does not reproduce the scientific data pipeline. All three publication derivatives are included.
