from __future__ import annotations

import csv
import json
from pathlib import Path

from pydantic import BaseModel


# Codici BUFR principali (archivio ARPAE Emilia-Romagna)
BUFR_TEMP = "B12101"    # Temperatura (K)
BUFR_HUMIDITY = "B13003"  # Umidità relativa (%)
BUFR_PRECIP = "B13011"   # Precipitazione (mm)
BUFR_SOLAR = "B07030"    # Radiazione solare (W/m²)


def _gauss_boaga_to_degrees(lon_cm: int, lat_cm: int) -> tuple[float, float]:
    """Converti coordinate Gauss-Boaga (cm) a gradi decimali WGS84."""
    lon_deg = lon_cm / 100000.0
    lat_deg = lat_cm / 100000.0
    return round(lon_deg, 6), round(lat_deg, 6)


def _extract_var(data_block: dict, bufr_code: str) -> float | None:
    """Estrai valore di una variabile BUFR da un blocco data."""
    vars_dict = data_block.get("vars", {})
    entry = vars_dict.get(bufr_code)
    if entry and isinstance(entry, dict) and "v" in entry:
        val = entry["v"]
        if val is not None:
            return float(val)
    return None


def _is_instantaneous(timerange: list) -> bool:
    """Timerange[0] == 0 significa lettura istantanea (oraria)."""
    return bool(timerange) and timerange[0] == 0


def _is_15min_aggregate(timerange: list) -> bool:
    """Timerange[0] == 1 e durata == 900s: accumulato 15 min, contiene B13011 (precipitazione)."""
    return bool(timerange and timerange[0] == 1 and len(timerange) >= 3 and timerange[2] == 900)


class StationObs(BaseModel):
    station_name: str
    network: str
    lon_deg: float
    lat_deg: float
    timestamp_utc: str
    temperature_k: float | None
    humidity_pct: float | None
    precipitation_mm: float | None
    solar_rad_wm2: float | None

    @property
    def temperature_c(self) -> float | None:
        if self.temperature_k is not None:
            return round(self.temperature_k - 273.15, 2)
        return None


def parse_ndjson(content: str) -> list[StationObs]:
    """
    Parse NDJSON (una riga JSON per stazione-timestep).
    Per ogni riga:
    - Cerca in TUTTI i blocchi data per B01019 (nome stazione)
    - Il blocco con timerange=[1,0,900] contiene metadata stazione (rete)
    - Il blocco con timerange[0]=0 (istantaneo) contiene variabili meteo
    """
    records: list[StationObs] = []
    for raw_line in content.splitlines():
        if not raw_line.strip():
            continue
        obj = json.loads(raw_line)

        data_blocks = obj.get("data", [])
        precip_block = None
        instant_blocks: list[dict] = []
        station_name = ""

        for block in data_blocks:
            tr = block.get("timerange", [])
            vars_block = block.get("vars", {})

            # B01019 contiene il nome della stazione
            if "B01019" in vars_block:
                station_name = vars_block["B01019"].get("v", "")

            if _is_15min_aggregate(tr):
                precip_block = block
            elif _is_instantaneous(tr):
                instant_blocks.append(block)

        network = obj.get("network", "")
        lon_cm = obj.get("lon", 0)
        lat_cm = obj.get("lat", 0)
        lon_deg, lat_deg = _gauss_boaga_to_degrees(lon_cm, lat_cm)

        timestamp_utc = obj.get("date", "")

        temp_k = None
        humidity = None
        precip = None
        solar = None

        for ib in instant_blocks:
            if temp_k is None:
                temp_k = _extract_var(ib, BUFR_TEMP)
            if humidity is None:
                humidity = _extract_var(ib, BUFR_HUMIDITY)
            if solar is None:
                solar = _extract_var(ib, BUFR_SOLAR)

        # B13011 (precipitazione) è nel blocco accumulato 15 min, non in quello istantaneo
        if precip_block is not None:
            precip = _extract_var(precip_block, BUFR_PRECIP)

        records.append(StationObs(
            station_name=str(station_name),
            network=str(network),
            lon_deg=lon_deg,
            lat_deg=lat_deg,
            timestamp_utc=timestamp_utc,
            temperature_k=temp_k,
            humidity_pct=humidity,
            precipitation_mm=precip,
            solar_rad_wm2=solar,
        ))

    return records


def write_csv(records: list[StationObs], path: Path) -> None:
    if not records:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "station_name", "network", "lon_deg", "lat_deg", "timestamp_utc",
            "temperature_k", "temperature_c", "humidity_pct", "precipitation_mm", "solar_rad_wm2"
        ])
        writer.writeheader()
        for r in records:
            row = r.model_dump()
            row["temperature_c"] = r.temperature_c
            writer.writerow(row)