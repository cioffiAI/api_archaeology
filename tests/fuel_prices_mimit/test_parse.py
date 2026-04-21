import sys
import os
from pathlib import Path

# Workaround to import from cases/fuel-prices-mimit (kebab-case)
sys.path.insert(0, os.path.abspath("cases/fuel-prices-mimit"))

import pytest
from parse import parse_prices, parse_stations, FuelPrice, FuelStation

def test_parse_prices():
    # Mock CSV content with metadata line and PIPE delimiter
    content = "Estrazione del 2024-01-01\nidImpianto|descCarburante|prezzo|isSelf|dtComu\n123|Benzina|1,850|S|2024-01-01\n456|Diesel|1,720|N|2024-01-01"

    with open("test_prices.csv", "w", encoding="utf-8") as f:
        f.write(content)

    prices = parse_prices("test_prices.csv")

    assert len(prices) == 2
    assert isinstance(prices[0], FuelPrice)
    assert prices[0].station_id == "123"
    assert prices[0].fuel_description == "Benzina"
    assert prices[0].price == 1.850
    assert prices[0].is_self == "S"
    assert prices[0].date == "2024-01-01"

    os.remove("test_prices.csv")

def test_parse_stations():
    content = "Estrazione del 2024-01-01\nidImpianto|descImpianto|indirizzo|comune|provincia\n123|Stazione A|Via Roma 1|Milano|MI\n456|Stazione B|Via Torino 2|Roma|RM"

    with open("test_stations.csv", "w", encoding="utf-8") as f:
        f.write(content)

    stations = parse_stations("test_stations.csv")

    assert len(stations) == 2
    assert isinstance(stations[0], FuelStation)
    assert stations[0].station_id == "123"
    assert stations[0].name == "Stazione A"
    assert stations[0].address == "Via Roma 1"
    assert stations[0].city == "Milano"
    assert stations[0].province == "MI"

    os.remove("test_stations.csv")

def test_parse_prices_empty():
    content = "Estrazione del 2024-01-01\nidImpianto|descCarburante|prezzo|isSelf|dtComu"
    with open("test_empty_prices.csv", "w", encoding="utf-8") as f:
        f.write(content)

    prices = parse_prices("test_empty_prices.csv")
    assert prices == []
    os.remove("test_empty_prices.csv")

def test_parse_stations_empty():
    content = "Estrazione del 2024-01-01\nidImpianto|descImpianto|indirizzo|comune|provincia"
    with open("test_empty_stations.csv", "w", encoding="utf-8") as f:
        f.write(content)

    stations = parse_stations("test_empty_stations.csv")
    assert stations == []
    os.remove("test_empty_stations.csv")

def test_parse_prices_malformed_price():
    content = "Estrazione del 2024-01-01\nidImpianto|descCarburante|prezzo|isSelf|dtComu\n123|Benzina|invalid|S|2024-01-01"
    with open("test_bad_price.csv", "w", encoding="utf-8") as f:
        f.write(content)

    with pytest.raises(ValueError):
        parse_prices("test_bad_price.csv")
    os.remove("test_bad_price.csv")
