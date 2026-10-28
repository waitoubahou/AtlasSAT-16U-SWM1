# Scientific conclusions and evidence limits

The accepted single-satellite baseline **fails the ≤72-hour daylight revisit target**. The saved maximum complete gap for nominal 30 km swath and ideal ±20° roll is 312.21995813943926 h (reported 312.22 h) for an agricultural target in Sidi Bibi. The historical reference point is excluded from agricultural worst-case calculations.

This repository candidate preserves four distinct claims:

| Level | What it establishes |
|---|---|
| Numerical verification | Parser, equation, geometry and algorithm checks; archived internal regressions establish numerical consistency for their tested inputs. |
| Geometric reachability | A modelled target intersects the footprint under the stated ideal independent roll bound. |
| Daylight optical opportunity | Geometric reachability with geometric solar-centre elevation ≥0°; a saved ≥10° sensitivity is a separate threshold. |
| Physical/operational validation | Not established: no flight-qualified payload/ADCS, schedulability, acquired image quality or mission service guarantee. |

The seven-commune agricultural geometry is a provisional research mask, not an official institutional perimeter or locally validated classification. The southern greenhouse-source omission affects 22.04% of the outer study boundary and 6.861% of the primary mask. Source vintages and conservative screening can omit farms or misclassify current agricultural use.

The orbit is a preserved J2-only preliminary model. Predicted Earth orientation and frame assumptions limit geographical interpretation. The 10 m along-track sample is provisional, distinct from optical IFOV and line acquisition rate. Ideal ±10°/±20° roll represents independent per-target reachability, not unlimited slew, perfect pointing or a feasible observation schedule.

The TA=90° sensitivity is a change in initial true anomaly at fixed osculating inputs, not a pure phase shift of a fixed mean orbit. No new scenario is calculated here.

Complete no-access gaps use previous exit to next entry; left/right censored spans and no-access targets remain distinct. The public example contains only six saved point windows and does not reproduce the full mask, spatial convergence, orbital phase, EOP or swath studies.

The current historical v0.2 nominal outputs were already truncated; complete original-archive references separately support seven-day claims. That exception is distinct from an earlier OEM creation-header discrepancy. Neither is repaired here.
