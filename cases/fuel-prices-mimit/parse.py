import csv
from typing import List
from pydantic import BaseModel, field_validator
from pathlib import Path

class FuelPrice(BaseModel):
    station_id: str
    fuel_description: str
    price: float
    is_self: str
    date: str

    @field_validator("price", mode="before")
    @classmethod
    def parse_price(cls, v):
        if isinstance(v, str):
            # Replace comma with dot for float conversion
            v = v.replace(",", ".")
        return float(v)

class FuelStation(BaseModel):
    station_id: str
    name: str
    address: str
    city: str
    province: str

def _skip_metadata(file_obj):
    """Skips the first line (metadata) of the file."""
    file_obj.readline()

def parse_prices(file_path: str) -> List[FuelPrice]:
    prices = []
    with open(file_path, "r", encoding="utf-8") as f:
        _skip_metadata(f)
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            prices.append(
                FuelPrice(
                    station_id=row["idImpianto"],
                    fuel_description=row["descCarburante"],
                    price=row["prezzo"],
                    is_self=row["isSelf"],
                    date=row["dtComu"],
                )
            )
    return prices

def parse_stations(file_path: str) -> List[FuelStation]:
    stations = []
    with open(file_path, "r", encoding="utf-8") as f:
        _skip_metadata(f)
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            stations.append(
                FuelStation(
                    station_id=row["idImpianto"],
                    name=row["descImpianto"],
                    address=row["indirizzo"],
                    city=row["comune"],
                    province=row["provincia"],
                )
            )
    return stations
