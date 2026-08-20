# Data Licensing, Source Provenance & Offline Fallback Catalog

> **Document Status**: Active Register  
> **Target Platform**: Crime Nexus (CT-DFIR-01)  
> **Primary Objective**: Comprehensive Inventory of Data Sources, IP Licenses, & Offline Resilience Protocols  

---

## 1. Executive Summary

The **Crime Nexus (CT-DFIR-01)** platform integrates multiple spatial, legal, and safety data assets. To ensure strict legal compliance, intellectual property integrity, and reliable air-gapped operational readiness, this document establishes:

1. **Licensing Framework**: Legal terms governing each data source used across the platform.
2. **Provenance & Source Attribution**: Official origins and data providers.
3. **Offline Fallback Catalog**: Zero-dependency local storage assets and fallback strategies enabling 100% functionality without external internet access or API connectivity.

---

## 2. Spatial Data & GeoJSON Maps

### 🗺️ Boundary & Infrastructure Datasets
Spatial layers form the base map and administrative jurisdiction overlays for crime hotspot visualization.

| Dataset Asset | Source & Provider | License | Terms & Attribution |
| :--- | :--- | :--- | :--- |
| **Tamil Nadu District Boundaries** | Survey of India / ISRO Bhuvan Portal | Open Government Data (OGD) License India | Free for educational, research, and government use with attribution. |
| **Precinct Jurisdiction Maps** | State Police GIS Portal / Local Cartography | Internal Government Public Data / CC-BY 4.0 | Anonymized administrative boundaries without tactical security details. |
| **Road Network & Intersections** | OpenStreetMap (OSM) Contributors | Open Database License (ODbL 1.0) | Requires standard OpenStreetMap attribution (`© OpenStreetMap contributors`). |
| **Land Use & Landmark Layers** | ISRO Bhuvan / State Urban Development | OGD India / Creative Commons CC-BY 4.0 | Aggregated zoning data for contextual hotspot analysis. |

### 🔌 Offline Fallback Strategy for GeoJSON Maps
- **Bundled Storage Location**: Pre-packaged in `assets/geojson/` and `Component_datasets/spatial/` (e.g., `tamil_nadu_districts.geojson`, `chennai_precincts.geojson`).
- **Tile Rendering Fallback**: If external map tile servers (e.g., OpenStreetMap HTTP tiles) are unreachable:
  - System switches seamlessly to offline vector rendering via **PyDeck / Folium static offline GeoJSON layers**.
  - Local spatial point-in-polygon matching is executed using **Shapely** and **R-Tree spatial index** locally without calling external geocoding endpoints.

---

## 3. Crime Data & FIR Datasets

### 🚔 Incident Records & Legal Tagging
Crime datasets power hotspot density estimation, legal classification tagging (IPC, NDPS, Arms Act), and seasonal forecasting.

| Dataset Asset | Source & Provider | License | Terms & Attribution |
| :--- | :--- | :--- | :--- |
| **Synthetic FIR Dataset (PoC)** | Crime Nexus Synthetic Generator (`Component_datasets/`) | Creative Commons Zero (CC0 1.0 Universal - Public Domain) | Realistically structured synthetic data for safe research and demonstration. |
| **Aggregated Crime Statistics** | National Crime Records Bureau (NCRB) | OGD License India | Publicly published annual statistics; no PII or raw victim data used. |
| **IPC & Bare Acts Taxonomy** | Legislative Department, Ministry of Law & Justice | Public Domain (Government of India Works) | Official statutory law section classifications and legal penal codes. |

### 🔌 Offline Fallback Strategy for Crime Data
- **Bundled Storage Location**: Pre-populated SQLite local database at `data/crime_nexus.db` and static Parquet/CSV benchmark files under `Component_datasets/data/`.
- **Database Fallback Mechanism**:
  - In air-gapped deployments, all analytics queries route directly to the local SQLite database.
  - No remote cloud database connections or external API calls are required.
  - Spatial coordinates undergo local Gaussian jittering ($\pm 500\text{m}$) before local rendering.

---

## 4. iRAD (Integrated Road Accident Database) & Traffic Safety Data

### 🚗 Accident Hotspots & Blackspots
Accident data is overlaid with crime hotspots to optimize multi-agency emergency response and patrol routes.

| Dataset Asset | Source & Provider | License | Terms & Attribution |
| :--- | :--- | :--- | :--- |
| **iRAD Incident Summary** | Ministry of Road Transport and Highways (MoRTH) / NIC | MoRTH Open Data Initiative / iRAD Research License | Anonymized collision intensity, severity indices, and road safety markers. |
| **High-Risk Road Blackspots** | Tamil Nadu Road Safety Executive (TNRSC) | Government Open Access / OGD License India | Identifies top accident-prone road stretches and intersection nodes. |

### 🔌 Offline Fallback Strategy for iRAD Data
- **Bundled Storage Location**: Cached offline JSON and GeoJSON catalog at `Component_datasets/accident_data.json` and `assets/geojson/accident_blackspots.geojson`.
- **Analytical Fallback Mechanism**:
  - When live iRAD server API synchronization is unavailable, Crime Nexus loads the bundled local JSON cache.
  - Buffering and proximity joins between patrol routes and accident blackspots use local **Scikit-Learn KDTree** and **Geopandas** computational buffers.

---

## 5. Master Data Licensing & Fallback Matrix

| Data Domain | File / Bundle Path | License Type | Internet Needed? | Offline Fallback Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **District GeoJSON** | `assets/geojson/tamilnadu_districts.geojson` | OGD India | ❌ No | Static GeoJSON polygon loader |
| **Precinct GeoJSON** | `Component_datasets/spatial/precincts.geojson` | CC-BY 4.0 | ❌ No | Shapely local polygon indexing |
| **Road Network** | `assets/geojson/road_network.geojson` | ODbL 1.0 | ❌ No | NetworkX graph calculations |
| **Crime Database** | `data/crime_nexus.db` | CC0 1.0 (Synthetic) | ❌ No | SQLite local embedded engine |
| **Legal Acts Matrix** | `Component_datasets/legal_sections.json` | Public Domain | ❌ No | Memory-mapped JSON lookup table |
| **iRAD Blackspots** | `Component_datasets/accident_data.json` | MoRTH License | ❌ No | Local spatial KDTree distance buffer |

---

## 6. Verification & Compliance Guidelines

1. **Re-licensing Checks**: Any new spatial or traffic dataset ingested into Crime Nexus must be audited for non-commercial or restrictive clauses prior to inclusion in main builds.
2. **Third-Party Attribution**: All map views rendered in the UI display explicit copyright attribution footers for OpenStreetMap and Survey of India OGD data.
3. **Air-Gap Readiness Test**: Running `streamlit run app/app.py` in an environment with network interfaces disabled (`DISCONNECTED` network state) must achieve 100% feature coverage without thrown network timeouts.
