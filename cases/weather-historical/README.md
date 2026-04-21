# Case Study: ARPAE Historical Weather (API Archaeology)

## Overview

This case study demonstrates the "API Archaeology" pattern applied to a **time-series archive** — structured data published as a directory of compressed NDJSON files, rather than a traditional API endpoint.

ARPAE Emilia-Romagna publishes 20 years of meteorological observations (2006–2026) as monthly `.json.gz` archives, each containing station observations at 15-minute granularity. The challenge is navigating the archive listing, downloading the right files, and parsing the complex nested structure.

## Data Source

- **Source**: ARPAE Emilia-Romagna — SIMC (Servizio Idrometeorologico Regionale)
- **Data Type**: Historical meteorological observations from regional monitoring network
- **Archive URL**: `https://dati-simc.arpae.it/opendata/osservati/meteo/storico/`
- **License**: IODL 2.0 (Open Data Italia)
- **Coverage**: 2006-01 → 2026-04 (244 monthly files, ~3.5 GB compressed)

## Technical Implementation

### Archive Structure

The archive listing page (`/storico/`) contains links to 244 `.json.gz` files named `YYYY-MM.json.gz`. Each file is **NDJSON** — one JSON object per line, each representing a single station at a single timestep.

### JSON Schema

Each NDJSON line is structured as:

```json
{
  "version": "0.1",
  "network": "agrmet",
  "ident": null,
  "lon": 958959,     // Gauss-Boaga east coordinate (cm)
  "lat": 4504139,    // Gauss-Boaga north coordinate (cm)
  "date": "2024-01-01T00:00:00Z",  // ISO 8601 UTC
  "data": [
    { "timerange": [], "level": [], "vars": { "B01019": {"v": "S. Nicolo'"}, ... }},
    { "timerange": [1, 0, 900], "level": [1, null, null, null], "vars": { "B13011": {"v": 0.0} }},
    { "timerange": [0, 0, 3600], "level": [103, 2000, null, null],
      "vars": { "B12101": {"v": 279.85}, "B13003": {"v": 97} }}
  ]
}
```

The `data` array contains multiple blocks for different aggregation levels:
- **timerange[0]** = 0: instant (hourly), **1**: mean, **2**: min, **3**: max, **254**: processed
- **timerange[2]** = aggregation duration in seconds (0, 900, 3600, 86400)
- **level[0]** = 103/2000: altitude above sea level in meters

### BUFR Variable Codes

| Code | Variable | Unit |
|------|----------|------|
| B01019 | Station name | string |
| B12101 | Temperature | K (Kelvin) |
| B13003 | Relative humidity | % |
| B13011 | Precipitation | mm |
| B07030 | Solar radiation | W/m² |

### Coordinate System

Coordinates are in **Gauss-Boaga Roma40** (cm). Convert to WGS84 decimal degrees:
- `lon_deg = lon_cm / 100000.0`
- `lat_deg = lat_cm / 100000.0`

## Reproduction Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cioffiAI/api-archaeology.git
   cd api-archaeology/cases/weather-historical
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the fetcher**:
   ```bash
   python fetch.py
   ```
   This script checks the archive index, downloads `2024-01.json.gz` as a sample, and generates `sample.csv` with 20 records.

4. **Verify the data**:
   Check `sample.csv` for station name, coordinates, temperature (K and °C), and humidity.

## Key Findings

- **Pattern**: Time-series archive — directory listing + compressed NDJSON files
- **Reliability**: Archive is stable; 244 monthly files spanning 20 years
- **Complexity**: JSON structure requires careful parsing — variable blocks with different timerange/aggregation types, station metadata embedded in each record
- **Data gaps**: Instant measurements (temperature, humidity) available only at `hh:00`; other variables (precipitation) only at aggregate levels

## Notes

- No `robots.txt` at `dati-simc.arpae.it` (returns 404) — access is permitted
- Institutional delay of 2.0s implemented between requests
- Full archive would require downloading all 244 files (~3.5 GB compressed)