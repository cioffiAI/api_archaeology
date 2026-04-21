from __future__ import annotations

import csv
import json
import sys
from io import StringIO
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cases" / "weather-historical"))

from parse import (  # noqa: E402
    StationObs,
    _extract_var,
    _gauss_boaga_to_degrees,
    _is_instantaneous,
    _is_15min_aggregate,
    parse_ndjson,
    write_csv,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_HOURLY_ROW = {
    "version": "0.1",
    "network": "agrmet",
    "ident": None,
    "lon": 958959,
    "lat": 4504139,
    "date": "2024-01-01T00:00:00Z",
    "data": [
        {"timerange": [], "level": [], "vars": {"B01019": {"v": "S. Nicolo'"}}},
        {"timerange": [1, 0, 900], "level": [1, None, None, None], "vars": {"B13011": {"v": 0.0}}},
        {
            "timerange": [0, 0, 3600],
            "level": [103, 2000, None, None],
            "vars": {"B12101": {"v": 279.85}, "B13003": {"v": 97}},
        },
    ],
}

_QUARTER_ROW = {
    "version": "0.1",
    "network": "agrmet",
    "ident": None,
    "lon": 958959,
    "lat": 4504139,
    "date": "2024-01-01T00:15:00Z",
    "data": [
        {"timerange": [1, 0, 900], "level": [1, None, None, None], "vars": {"B13011": {"v": 0.5}}},
    ],
}

_NDJSON = "\n".join([json.dumps(_HOURLY_ROW), json.dumps(_QUARTER_ROW)])


# ---------------------------------------------------------------------------
# Unit tests — helpers
# ---------------------------------------------------------------------------


def test_gauss_boaga_lon():
    lon, _ = _gauss_boaga_to_degrees(958959, 4504139)
    assert lon == pytest.approx(9.58959, abs=1e-5)


def test_gauss_boaga_lat():
    _, lat = _gauss_boaga_to_degrees(958959, 4504139)
    assert lat == pytest.approx(45.04139, abs=1e-5)


def test_extract_var_present():
    block = {"vars": {"B12101": {"v": 279.85}}}
    assert _extract_var(block, "B12101") == pytest.approx(279.85)


def test_extract_var_missing_code():
    block = {"vars": {"B12101": {"v": 279.85}}}
    assert _extract_var(block, "B13003") is None


def test_extract_var_null_value():
    block = {"vars": {"B12101": {"v": None}}}
    assert _extract_var(block, "B12101") is None


def test_is_instantaneous_true():
    assert _is_instantaneous([0, 0, 3600]) is True


def test_is_instantaneous_false_for_aggregate():
    assert _is_instantaneous([1, 0, 900]) is False


def test_is_instantaneous_false_for_empty():
    assert _is_instantaneous([]) is False


def test_is_15min_aggregate_true():
    assert _is_15min_aggregate([1, 0, 900]) is True


def test_is_15min_aggregate_false_wrong_duration():
    assert _is_15min_aggregate([1, 0, 3600]) is False


def test_is_15min_aggregate_false_wrong_type():
    assert _is_15min_aggregate([0, 0, 900]) is False


# ---------------------------------------------------------------------------
# Integration tests — parse_ndjson
# ---------------------------------------------------------------------------


def test_parse_ndjson_count():
    records = parse_ndjson(_NDJSON)
    assert len(records) == 2


def test_parse_ndjson_station_name():
    r = parse_ndjson(_NDJSON)[0]
    assert r.station_name == "S. Nicolo'"


def test_parse_ndjson_network():
    r = parse_ndjson(_NDJSON)[0]
    assert r.network == "agrmet"


def test_parse_ndjson_coordinates():
    r = parse_ndjson(_NDJSON)[0]
    assert r.lon_deg == pytest.approx(9.58959, abs=1e-5)
    assert r.lat_deg == pytest.approx(45.04139, abs=1e-5)


def test_parse_ndjson_timestamp():
    r = parse_ndjson(_NDJSON)[0]
    assert r.timestamp_utc == "2024-01-01T00:00:00Z"


def test_parse_ndjson_temperature_from_instant_block():
    r = parse_ndjson(_NDJSON)[0]
    assert r.temperature_k == pytest.approx(279.85)


def test_parse_ndjson_humidity_from_instant_block():
    r = parse_ndjson(_NDJSON)[0]
    assert r.humidity_pct == pytest.approx(97.0)


def test_parse_ndjson_precipitation_from_aggregate_block():
    # B13011 lives in the [1,0,900] block — must be extracted even on hourly rows
    r = parse_ndjson(_NDJSON)[0]
    assert r.precipitation_mm == pytest.approx(0.0)


def test_parse_ndjson_precipitation_quarter_row():
    # Quarter-hour rows have no instant block but still carry precipitation
    r = parse_ndjson(_NDJSON)[1]
    assert r.precipitation_mm == pytest.approx(0.5)


def test_parse_ndjson_no_instant_block_gives_none_temp():
    r = parse_ndjson(_NDJSON)[1]
    assert r.temperature_k is None
    assert r.humidity_pct is None


def test_parse_ndjson_temperature_c_property():
    r = parse_ndjson(_NDJSON)[0]
    assert r.temperature_c == pytest.approx(279.85 - 273.15, abs=0.01)


def test_parse_ndjson_temperature_c_none_when_no_temp():
    r = parse_ndjson(_NDJSON)[1]
    assert r.temperature_c is None


def test_parse_ndjson_empty_content():
    assert parse_ndjson("") == []


def test_parse_ndjson_blank_lines_ignored():
    assert parse_ndjson("\n\n") == []


# ---------------------------------------------------------------------------
# write_csv
# ---------------------------------------------------------------------------


def test_write_csv_columns(tmp_path):
    records = parse_ndjson(_NDJSON)
    out = tmp_path / "out.csv"
    write_csv(records, out)
    with out.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert set(reader.fieldnames) == {
            "station_name", "network", "lon_deg", "lat_deg", "timestamp_utc",
            "temperature_k", "temperature_c", "humidity_pct", "precipitation_mm", "solar_rad_wm2",
        }


def test_write_csv_row_count(tmp_path):
    records = parse_ndjson(_NDJSON)
    out = tmp_path / "out.csv"
    write_csv(records, out)
    with out.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2


def test_write_csv_empty_does_not_create_file(tmp_path):
    out = tmp_path / "out.csv"
    write_csv([], out)
    assert not out.exists()
