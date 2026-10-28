# Focused cartographic attribution audit — RC v0.2

Review date: 28 October 2026. Scope: the accepted static publication figures, not a new geographic dataset release. All approved image/vector/TikZ bytes are preserved. No raw OSM, DEM, Sentinel, WorldCover, WorldCereal or greenhouse database is redistributed.

## Existing credits and targeted additions

The accepted publications already identify OSM (ODbL), ESA/PCG (CC BY), Natural Earth (public domain), Copernicus DEM and modified Sentinel data. The passage figure already prints the modified Sentinel 2026 notice. Existing notices were kept. The public copies add only the missing printed OSM copyright URL, exact WorldCover acknowledgement, unambiguous dataset/CC BY credit links and the DEM liability sentence. These appear in the publication source notes and distribution notices; the approved figures themselves are unchanged.

| Source | Concrete basis / required credit | RC v0.2 decision |
|---|---|---|
| OpenStreetMap | [Copyright/ODbL](https://www.openstreetmap.org/copyright), [OSMF static attribution guidance](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines): contributor credit and visible copyright URL | Existing OSM/ODbL credit retained; full printed URL added to the one-pager/report map notices and README. Static rendered-work scope; no geometry/database release or new OSM edits |
| Copernicus Sentinel-2 | [Sentinel legal notice](https://cds.climate.copernicus.eu/licences/ec-sentinel): modified-data acknowledgement with year | Existing modified Sentinel 2026 credit in passage image retained; one-pager distribution credit added. October imagery is contextual, not event-time weather or AtlasSAT imagery |
| Copernicus DEM GLO-30 | Existing original licence, Article 6; [collection information](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM) | Existing full DLR 2010–2014 / Airbus 2014–2018 / EU/ESA credit retained. Liability sentence added. Original licence PDF supplied unchanged; no endorsement implied |
| ESA WorldCover 2021 v200 | [Data-access acknowledgement](https://esa-worldcover.org/en/data-access), [Zanaga et al. dataset](https://doi.org/10.5281/zenodo.7254221), CC BY 4.0 | Exact acknowledgement added; original ESA/CC BY source credit preserved; classification transformation documented |
| ESA WorldCereal 2021 v100 | [Product page](https://esa-worldcereal.org/en/products/global-maps), [Van Tricht et al. dataset](https://doi.org/10.5281/zenodo.7875105), CC BY 4.0 in saved primary metadata | Dataset DOI/author and CC BY credit added to notices; global temporary-crop product only, not unrelated contributor reference data |
| Global-PCG-10, Figshare v2 | Original Figshare record identifies CC BY 4.0; [Niu et al. dataset](https://doi.org/10.6084/m9.figshare.27731148.v2), [paper](https://doi.org/10.5194/essd-17-5065-2025) | Author/dataset/version/CC BY links retained in distribution notices and linked in publication credits. Southern missing-source coverage caveat unchanged |
| Natural Earth | [Provider public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/) | Existing Natural Earth public-domain credit retained; approved outline convention and locator unchanged |

These provider terms/primary records were checked, including the retained original DEM licence and saved dataset metadata. No project licence is introduced or changed. The audit identifies no specific unresolved redistribution issue for the **rendered figures and publications in this candidate**. It does not certify redistributability of the complete private combined geographic database or extend any provider endorsement.

## Per-asset decisions

| Public figure / asset | Upstream material / role | Status |
|---|---|---|
| 02_access_and_tracks.png | Saved geometry/ground tracks over provisional research geography; OSM, ESA/PCG classifications | Included unchanged with source notices; no raw target database |
| 03_rolling_coverage.png | Project-generated saved numerical chart | Included unchanged |
| 04_gap_evidence.png | Project-generated complete/censored gap chart | Included unchanged |
| 05_swath_sensitivity.png | Project-generated saved sensitivity chart | Included unchanged |
| 06_convergence_and_phase.png | Project-generated saved convergence/initial-TA chart | Included unchanged |
| 07_Technical_Atlas_main_600dpi.png | Corrected OSM coast, roads/rivers/communes, DEM relief, ESA/PCG mask | Included unchanged; printed provider notices in PDF and distribution |
| 07_Technical_Atlas_legend_600dpi.png | Project cartographic key | Included unchanged |
| 07_Technical_Atlas_locator_600dpi.png | Refined Natural Earth context / approved locator | Included unchanged; geographic convention preserved |
| 08_Technical_Orbital_Globe.pdf | Preserved GMAT-derived orbital display and Natural Earth context | Included unchanged; snapshot/predicted-EOP qualification retained |
| 09_Three_Orbital_Passages.png | Modified Sentinel mosaic, OSM/ESA/PCG context and saved ray-traced passages | Included unchanged; existing visible 2026 Sentinel/source notice retained |
| 10_Orbital_Globe_Compact_RevD3_4.pdf | Compact approved orbit/Natural Earth illustration | Included unchanged |
| 10_Orbital_Globe_Compact_RevD3_4.png | Existing approved PNG variant for root README | Included byte-identically from accepted RevD3.4; not newly rendered |
| 11_Technical_Atlas_Compact_RevD3_2.png | Approved compact map with OSM, DEM, ESA/PCG, Natural Earth | Included unchanged; README and one-pager carry full notices |
| 12_Figure4_Concept_RevD3_2.tikz | Editorial optical-geometry concept | Included unchanged; no new geometry or physical validation |
| 13_Daylight_Timeline.pdf | Project-generated saved access timeline | Included unchanged |
| 13_Daylight_Timeline_Compact.pdf | Compact project timeline | Included unchanged |

The primary mask and seven-commune boundary remain provisional; no official institutional agricultural perimeter or new field validation is claimed. The greenhouse omission and Earth-orientation limitations remain visible. Source notices are in [the figure directory](studies/2A-orbital-analysis/figures/README.md) and [the documents directory](studies/2A-orbital-analysis/documents/THIRD_PARTY_NOTICES.md). Original asset hashes are recorded in QA and the file-selection ledger.
