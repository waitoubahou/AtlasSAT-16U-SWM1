# Analytical cross-references — Document 2A-1 RevD3.5

All references below use the **actual compiled numbering of Document 2A-2 v0.2.1**, 49 pages, 27 October 2026. Its unchanged PDF, Markdown, complete 84-row CSV and selected records are bundled under analytical_companion. No scientific calculation was run for this integration.

The five subject references are A–E; G identifies the general citation and T the compact comparison. Main-report subsection 3.2 combines A/B in one concise note. All references are to a separate companion, not equation numbers of the main report.

## G — Companion identity and evidence boundaries

**Main report:** §1.3 / 6.4 / evidence E18 / technical reference 10. **2A-2:** Reader's guide; Mathematical limitations register.

**Tables:** 1 p. 3, 34 p. 45.

**CSV IDs:** Reader/limitations register; document metadata.

**Evidence boundary:** Independent implementation does not establish physical/operational validation; A/F/N/R are provenance codes.

## A — Initialization, Keplerian versus J2 nodal period

**Main report:** §3.2. **2A-2:** 1–3.

**Equations:** (2.6) p. 8, (3.14) p. 13.

**Tables:** 3 p. 6, 4 p. 9, 8 p. 15.

**CSV IDs:** C01, C02, C03, C04.

**Evidence boundary:** Different force/period definitions; their difference is not propagation error.

## B — J2 precession and near-SSO assumptions

**Main report:** §3.2 / 3.3 comparison table. **2A-2:** 3–4.

**Equations:** (3.11) p. 13, (3.12) p. 13, (3.13) p. 13, (3.14) p. 13.

**Tables:** 8 p. 15, 9 p. 15, 10 p. 18.

**CSV IDs:** C05, C06, C13, C14.

**Evidence boundary:** First-order mean-element theory and finite-interval osculating fits have different averaging/frame definitions.

## C — Discrete Sidi Bibi recurrence and residual

**Main report:** §9.2 / 3.3 comparison table. **2A-2:** 5, §5.1.

**Equations:** (5.7) p. 22, (5.8) p. 23, (5.9) p. 23, (5.10) p. 23, (5.11) p. 24, (5.12) p. 24.

**Tables:** 16 p. 24, 17 p. 24, 18 p. 25.

**CSV IDs:** D02, D03, D04, D05, D06, D08.

**Evidence boundary:** Saved mean nodal period and empirical occupancy condition timing; independent integer counts do not prove optical eligibility/completeness.

## D — Pushbroom, LOS, roll, illumination and local boundary checks

**Main report:** §6.4. **2A-2:** 6–8.

**Equations:** (6.1) p. 29, (6.2) p. 29, (6.3) p. 29, (7.3) p. 31, (7.4) p. 31, (7.5) p. 31, (7.6) p. 31, (7.7) p. 31, (7.8) p. 32, (7.9) p. 32, (7.10) p. 32, (8.1) p. 35, (8.2) p. 35, (8.3) p. 35, (8.4) p. 35, (8.5) p. 35.

**Tables:** 26 p. 32, 27 p. 33, 28 p. 36.

**CSV IDs:** E1_entry, E1_exit, E2_entry, E2_exit, E1_solar, E2_solar.

**Evidence boundary:** Two local worked window checks; approximate solar check is a gross sign/scale comparison. No independent whole-ROI event search.

## E — Gap arithmetic, censoring and weighted rolling coverage

**Main report:** §9.2 / 3.3 comparison table. **2A-2:** 9–10.

**Equations:** (9.1) p. 37, (9.5) p. 38, (9.6) p. 38, (10.2) p. 40, (10.3) p. 40.

**Tables:** 30 p. 38, 31 p. 41, 32 p. 41.

**CSV IDs:** G01, W_S30_R20_daylight_72.

**Evidence boundary:** Independent aggregation of saved events/weights, not discovery of every event, all-cell imagery or an executable schedule.

## T — Three selected summary comparisons

**Main report:** §3.3 comparison table. **2A-2:** 3, 5, 10; final comparison.

**Tables:** 8 p. 15, 18 p. 25, 32 p. 41, 33 p. 43.

**CSV IDs:** C05, D02, W_S30_R20_daylight_72.

**Evidence boundary:** Summary display is rounded; full saved values and residuals remain in the complete 84-row CSV.

## Source and unit checks

ANALYTICAL_INTEGRATION_TRACEABILITY.csv lists every newly displayed numerical value, exact saved value, source field/row, unit and scope. Percent conversion is display-only; no opportunity or geographic quantity is recomputed. Stored Model B residual is read directly, not newly inferred from rounded hours.

No difference requiring a change to the frozen baseline was found. The first-order/fitted and Keplerian/nodal definition differences are retained and explained.

analytical_companion/SOURCE_MANIFEST.json describes the complete original analytical release. This report bundle contains selected, byte-identical companion records; evidence/E18_analytical_source_manifest.json identifies this subset. Complete analytical-code reproduction uses the frozen 2A-2 release, not this authoring-only package.
