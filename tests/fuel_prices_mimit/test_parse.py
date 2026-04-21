from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cases" / "fuel-prices-mimit"))

from parse import FuelPrice, FuelStation, parse_prices, parse_stations  # noqa: E402


PRICES_CSV = textwrap.dedent("""\
    Estrazione del 2026-04-21
    idImpianto|descCarburante|prezzo|isSelf|dtComu
    12345|Benzina|2.139|0|21/04/2026 08:00:00
    12345|Gasolio|1.987|1|21/04/2026 08:00:00
    99999|Benzina|2.201|0|21/04/2026 08:00:00
""")

STATIONS_CSV = textwrap.dedent("""\
    Estrazione del 2026-04-21
    idImpianto|Gestore|Bandiera|Tipo Impianto|Nome Impianto|Indirizzo|Comune|Provincia|Latitudine|Longitudine
    12345|MARIO ROSSI SRL|IP|Stradale|STAZIONE IP|VIA ROMA 1|ROMA|RM|41.8902|12.4922
    99999|BIANCHI CARLO|Q8|Stradale|Q8 CENTRO|CORSO ITALIA 5|MILANO|MI|45.4654|9.1859
""")


def test_parse_prices_count():
    assert len(parse_prices(PRICES_CSV)) == 3


def test_parse_prices_fields():
    r = parse_prices(PRICES_CSV)[0]
    assert r.station_id == 12345
    assert r.fuel_description == "Benzina"
    assert r.price == pytest.approx(2.139)
    assert r.is_self_service is False
    assert r.reported_at == "21/04/2026 08:00:00"


def test_parse_prices_self_service_flag():
    assert parse_prices(PRICES_CSV)[1].is_self_service is True


def test_parse_prices_empty():
    csv = "Estrazione del 2026-04-21\nidImpianto|descCarburante|prezzo|isSelf|dtComu\n"
    assert parse_prices(csv) == []


def test_parse_stations_count():
    assert len(parse_stations(STATIONS_CSV)) == 2


def test_parse_stations_fields():
    s = parse_stations(STATIONS_CSV)[0]
    assert s.station_id == 12345
    assert s.brand == "IP"
    assert s.municipality == "ROMA"
    assert s.province == "RM"
    assert s.latitude == pytest.approx(41.8902)
    assert s.longitude == pytest.approx(12.4922)
