from __future__ import annotations

import csv
import io

from pydantic import BaseModel


class FuelPrice(BaseModel):
    station_id: int
    fuel_description: str
    price: float
    is_self_service: bool
    reported_at: str


class FuelStation(BaseModel):
    station_id: int
    manager: str
    brand: str
    station_type: str
    name: str
    address: str
    municipality: str
    province: str
    latitude: float
    longitude: float


def _skip_metadata(content: str) -> str:
    """Strip the first 'Estrazione del ...' line that MIMIT prepends to every export."""
    lines = content.splitlines(keepends=True)
    if lines and lines[0].startswith("Estrazione"):
        return "".join(lines[1:])
    return content


def parse_prices(content: str) -> list[FuelPrice]:
    reader = csv.DictReader(io.StringIO(_skip_metadata(content)), delimiter="|")
    records = []
    for row in reader:
        records.append(FuelPrice(
            station_id=int(row["idImpianto"]),
            fuel_description=row["descCarburante"].strip(),
            price=float(row["prezzo"].replace(",", ".")),
            is_self_service=row["isSelf"].strip() == "1",
            reported_at=row["dtComu"].strip(),
        ))
    return records


def parse_stations(content: str) -> list[FuelStation]:
    reader = csv.DictReader(io.StringIO(_skip_metadata(content)), delimiter="|")
    records = []
    for row in reader:
        records.append(FuelStation(
            station_id=int(row["idImpianto"]),
            manager=row["Gestore"].strip(),
            brand=row["Bandiera"].strip(),
            station_type=row["Tipo Impianto"].strip(),
            name=row["Nome Impianto"].strip(),
            address=row["Indirizzo"].strip(),
            municipality=row["Comune"].strip(),
            province=row["Provincia"].strip(),
            latitude=float(row["Latitudine"].replace(",", ".")),
            longitude=float(row["Longitudine"].replace(",", ".")),
        ))
    return records
