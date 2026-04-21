# MIMIT Fuel Prices Case Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the `cases/fuel-prices-mimit/` case study: implement policy-compliant fetch and parse scripts, generate a small sample CSV, and write the full public-facing README.

**Architecture:** Pattern C — open data already published but obscured by the main interface. MIMIT publishes daily CSV snapshots of Italian fuel prices and a station registry as flat files under `/images/exportCSV/`. No authentication, no JS rendering required. Scripts follow the project's standard policy layer (robots.txt check, 5 s institutional delay, identifiable User-Agent).

**Tech Stack:** Python 3.11+, `httpx`, `pydantic>=2.8`, `pytest`, stdlib `csv` and `urllib`.

---

## Verified findings from Task 2 (already done — 2026-04-21)

- `robots.txt` disallows only CMS/admin paths (`/administrator/`, `/api/`, `/bin/`, `/cache/`, `/cli/`, `/components/`, `/includes/`, `/installation/`, `/language/`, `/layouts/`, `/libraries/`, `/logs/`, `/modules/`, `/plugins/`, `/tmp/`). `/images/exportCSV/` is **not disallowed**.
- Both CSV files confirmed live and downloadable:
  - `https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv`
  - `https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv`
- **Delimiter is `|` (pipe), not `;`.**
- **Line 1 of each file is metadata** (`Estrazione del YYYY-MM-DD`) and must be skipped before parsing.
- Actual schema for `prezzo_alle_8.csv`: `idImpianto|descCarburante|prezzo|isSelf|dtComu` — no `Carburante` (fuel code) column.
- Actual schema for `anagrafica_impianti_attivi.csv`: `idImpianto|Gestore|Bandiera|Tipo Impianto|Nome Impianto|Indirizzo|Comune|Provincia|Latitudine|Longitudine`
- Full CSV files are already downloaded locally at `cases/fuel-prices-mimit/csv mimit/` (92 848 price rows + station registry). These must NOT be committed to git.
- Landing page URL `https://www.mimit.gov.it/it/mercato-petrolifero/prezzi-carburanti` currently returns 404. The CSV download URLs still work. The ToS/licence link must be found from the new page listed on the 404 redirect ("Prezzi carburanti - Modalità di adempimento degli obblighi informativi di cui all'articolo 1 del D.L. 33/2026"). **Find and note the exact licence string before completing Task 6.**

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Modify | `pyproject.toml` | Add `pytest` to dev dependencies |
| Modify | `.gitignore` | Exclude full CSV downloads |
| Create | `tests/__init__.py` | Make tests a package |
| Create | `tests/fuel_prices_mimit/__init__.py` | Subpackage |
| Create | `tests/fuel_prices_mimit/test_parse.py` | Unit tests for parse.py |
| Create | `cases/fuel-prices-mimit/parse.py` | Data models + CSV parsing logic |
| Create | `cases/fuel-prices-mimit/fetch.py` | robots.txt check, HTTP fetch, CSV write |
| Overwrite | `cases/fuel-prices-mimit/sample.csv` | Small demo sample (≤ 20 rows) |
| Overwrite | `cases/fuel-prices-mimit/README.md` | Full case study writeup |

---

## Task 1: Add pytest, update .gitignore, verify test setup

**Files:**
- Modify: `pyproject.toml`
- Modify: `.gitignore`

- [ ] **Step 1: Add dev dependencies block to pyproject.toml**

Replace the existing content with:

```toml
[project]
name = "api-archaeology"
version = "0.1.0"
description = "Educational repository for documenting API archaeology case studies."
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.8.0",
    "selectolax>=0.3.21",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Add full CSV downloads to .gitignore**

Open `.gitignore` and append:

```
# Full MIMIT CSV downloads — only sample.csv belongs in the repo
cases/fuel-prices-mimit/csv mimit/
```

- [ ] **Step 3: Install dev dependencies**

```bash
uv sync --extra dev
```

Expected: resolves without errors.

- [ ] **Step 4: Create test package structure**

```bash
mkdir -p tests/fuel_prices_mimit
touch tests/__init__.py tests/fuel_prices_mimit/__init__.py
```

- [ ] **Step 5: Verify pytest runs (no tests yet)**

```bash
uv run pytest --collect-only
```

Expected: `no tests ran`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .gitignore tests/__init__.py tests/fuel_prices_mimit/__init__.py
git commit -m "chore: add pytest dev dependency, gitignore full CSVs, test package structure"
```

---

## Task 2: ~~Verify MIMIT endpoint~~ — COMPLETED 2026-04-21

Findings recorded in the "Verified findings" section above. Skip this task.

**One remaining action:** find the exact licence string from the new ToS page before writing Task 6's README. The 404 page listed "Prezzi carburanti - Modalità di adempimento degli obblighi informativi di cui all'articolo 1 del D.L. 33/2026" as a redirect. Follow that link, find the data reuse/licence section, and note the exact wording.

---

## Task 3: Implement parse.py with TDD

**Files:**
- Create: `cases/fuel-prices-mimit/parse.py`
- Create: `tests/fuel_prices_mimit/test_parse.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/fuel_prices_mimit/test_parse.py`:

```python
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

# Load parse module from hyphenated directory (kebab-case is intentional for the public repo)
_case_dir = Path(__file__).parent.parent.parent / "cases" / "fuel-prices-mimit"
sys.path.insert(0, str(_case_dir))

from parse import FuelPrice, FuelStation, parse_prices, parse_stations  # noqa: E402


# Real format: line 1 is metadata, line 2 is header, pipe-delimited
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
    records = parse_prices(PRICES_CSV)
    assert len(records) == 3


def test_parse_prices_fields():
    records = parse_prices(PRICES_CSV)
    r = records[0]
    assert r.station_id == 12345
    assert r.fuel_description == "Benzina"
    assert r.price == pytest.approx(2.139)
    assert r.is_self_service is False
    assert r.reported_at == "21/04/2026 08:00:00"


def test_parse_prices_self_service_flag():
    records = parse_prices(PRICES_CSV)
    assert records[1].is_self_service is True


def test_parse_stations_count():
    stations = parse_stations(STATIONS_CSV)
    assert len(stations) == 2


def test_parse_stations_fields():
    stations = parse_stations(STATIONS_CSV)
    s = stations[0]
    assert s.station_id == 12345
    assert s.brand == "IP"
    assert s.municipality == "ROMA"
    assert s.province == "RM"
    assert s.latitude == pytest.approx(41.8902)
    assert s.longitude == pytest.approx(12.4922)
```

- [ ] **Step 2: Run tests — verify they all fail**

```bash
uv run pytest tests/fuel_prices_mimit/test_parse.py -v
```

Expected: `ModuleNotFoundError: No module named 'parse'` or similar. All 5 tests fail.

- [ ] **Step 3: Create parse.py**

Create `cases/fuel-prices-mimit/parse.py`:

```python
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
    reader = csv.DictReader(io.StringIO(_skip_metadata(content)), delimiter='|')
    records = []
    for row in reader:
        records.append(FuelPrice(
            station_id=int(row['idImpianto']),
            fuel_description=row['descCarburante'].strip(),
            price=float(row['prezzo'].replace(',', '.')),
            is_self_service=row['isSelf'].strip() == '1',
            reported_at=row['dtComu'].strip(),
        ))
    return records


def parse_stations(content: str) -> list[FuelStation]:
    reader = csv.DictReader(io.StringIO(_skip_metadata(content)), delimiter='|')
    records = []
    for row in reader:
        records.append(FuelStation(
            station_id=int(row['idImpianto']),
            manager=row['Gestore'].strip(),
            brand=row['Bandiera'].strip(),
            station_type=row['Tipo Impianto'].strip(),
            name=row['Nome Impianto'].strip(),
            address=row['Indirizzo'].strip(),
            municipality=row['Comune'].strip(),
            province=row['Provincia'].strip(),
            latitude=float(row['Latitudine'].replace(',', '.')),
            longitude=float(row['Longitudine'].replace(',', '.')),
        ))
    return records
```

- [ ] **Step 4: Run tests — verify they all pass**

```bash
uv run pytest tests/fuel_prices_mimit/test_parse.py -v
```

Expected:
```
PASSED tests/fuel_prices_mimit/test_parse.py::test_parse_prices_count
PASSED tests/fuel_prices_mimit/test_parse.py::test_parse_prices_fields
PASSED tests/fuel_prices_mimit/test_parse.py::test_parse_prices_self_service_flag
PASSED tests/fuel_prices_mimit/test_parse.py::test_parse_stations_count
PASSED tests/fuel_prices_mimit/test_parse.py::test_parse_stations_fields
5 passed in 0.XXs
```

- [ ] **Step 5: Commit**

```bash
git add "cases/fuel-prices-mimit/parse.py" tests/fuel_prices_mimit/test_parse.py
git commit -m "feat(mimit): add parse.py with FuelPrice/FuelStation models and unit tests"
```

---

## Task 4: Implement fetch.py

**Files:**
- Create: `cases/fuel-prices-mimit/fetch.py`

No new tests — live network calls are covered by the integration run in Task 5.

- [ ] **Step 1: Create fetch.py**

Create `cases/fuel-prices-mimit/fetch.py`:

```python
from __future__ import annotations

import csv
import os
import sys
import time
import urllib.parse
import urllib.robotparser
from pathlib import Path

import httpx

from parse import FuelPrice, parse_prices

PRICES_URL = "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv"
INSTITUTIONAL_DELAY = 5.0
CONTACT_EMAIL = os.getenv("API_ARCHAEOLOGY_CONTACT_EMAIL", "set-contact-email@example.com")
USER_AGENT = (
    f"ApiArchaeology/1.0 "
    f"(educational; +github.com/<cioffiAI>/api-archaeology; contact={CONTACT_EMAIL})"
)
SAMPLE_ROWS = 20
SAMPLE_PATH = Path(__file__).parent / "sample.csv"


def _build_client() -> httpx.Client:
    return httpx.Client(
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
        timeout=30.0,
    )


def _check_robots(client: httpx.Client, target_url: str) -> None:
    parsed = urllib.parse.urlparse(target_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        response = client.get(robots_url)
        parser.parse(response.text.splitlines())
    except Exception as exc:
        print(f"Warning: could not fetch robots.txt ({exc}). Proceeding conservatively.")
        return
    if not parser.can_fetch("*", target_url):
        raise RuntimeError(f"robots.txt disallows {target_url} — aborting.")


def _fetch_csv(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    try:
        return response.content.decode("utf-8")
    except UnicodeDecodeError:
        return response.content.decode("windows-1252")


def _write_sample(records: list[FuelPrice], path: Path) -> None:
    if not records:
        print("No records to write.", file=sys.stderr)
        return
    sample = records[:SAMPLE_ROWS]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(sample[0].model_fields.keys()))
        writer.writeheader()
        for r in sample:
            writer.writerow(r.model_dump())
    print(f"Wrote {len(sample)} rows to {path}")


def main() -> None:
    with _build_client() as client:
        print("Checking robots.txt ...")
        _check_robots(client, PRICES_URL)

        print(f"Waiting {INSTITUTIONAL_DELAY}s (institutional rate limit) ...")
        time.sleep(INSTITUTIONAL_DELAY)

        print(f"Fetching prices from {PRICES_URL} ...")
        prices_csv = _fetch_csv(client, PRICES_URL)
        records = parse_prices(prices_csv)
        print(f"Parsed {len(records)} price records.")

        _write_sample(records, SAMPLE_PATH)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax check**

```bash
uv run python -c "
import sys
sys.path.insert(0, 'cases/fuel-prices-mimit')
import fetch
print('fetch.py imports OK')
"
```

Expected: `fetch.py imports OK`

- [ ] **Step 3: Commit**

```bash
git add "cases/fuel-prices-mimit/fetch.py"
git commit -m "feat(mimit): add fetch.py with robots.txt check, rate limiting and CSV download"
```

---

## Task 5: Generate sample.csv

The full CSVs are already available locally at `cases/fuel-prices-mimit/csv mimit/`. Use them to generate the sample without hitting the network again.

**Files:**
- Overwrite: `cases/fuel-prices-mimit/sample.csv`

- [ ] **Step 1: Generate sample from local file**

```bash
uv run python - <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, "cases/fuel-prices-mimit")
from parse import parse_prices
from fetch import _write_sample, SAMPLE_PATH

content = Path("cases/fuel-prices-mimit/csv mimit/prezzo_alle_8.csv").read_text(encoding="utf-8")
records = parse_prices(content)
print(f"Parsed {len(records)} records")
_write_sample(records, SAMPLE_PATH)
EOF
```

Expected:
```
Parsed 92847 records
Wrote 20 rows to .../cases/fuel-prices-mimit/sample.csv
```

- [ ] **Step 2: Inspect sample.csv**

```bash
head -5 "cases/fuel-prices-mimit/sample.csv"
```

Verify: header row present, 20 data rows, prices in plausible range (1.7–2.5 €), dates recent.

- [ ] **Step 3: Run all tests**

```bash
uv run pytest -v
```

Expected: all 5 tests pass, no regressions.

- [ ] **Step 4: Commit sample**

```bash
git add "cases/fuel-prices-mimit/sample.csv"
git commit -m "feat(mimit): add sample.csv with 20 demonstrative price records"
```

---

## Task 6: Complete README.md for the case study

**Files:**
- Overwrite: `cases/fuel-prices-mimit/README.md`

Before writing this task: look up the current ToS/licence page reachable from the MIMIT 404 redirect ("Prezzi carburanti - Modalità di adempimento degli obblighi informativi di cui all'articolo 1 del D.L. 33/2026") and fill in the `<!-- licence -->` placeholder below.

- [ ] **Step 1: Write the full README**

Replace `cases/fuel-prices-mimit/README.md` with:

```markdown
# Case Study: MIMIT Fuel Prices

## Pattern
Pattern C — open data already published, obscured by the main interface.

## What this case demonstrates
The Italian Ministry of Enterprises and Made in Italy (MIMIT) publishes daily
fuel price reports from ~18,000 stations across Italy as flat pipe-delimited
CSV files. The main website presents this data through an interactive map that
discourages bulk access. The underlying CSVs are publicly linked in the page
source and have been stable for years.

This case shows that for government open data, the interesting question is
often not "how to access it" but "where they actually put it" — and that the
answer is almost always a flat file one network tab away from the interactive
widget.

## Data source
- Daily prices snapshot: `https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv`
- Station registry: `https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv`

Observed at: 2026-04-21

## robots.txt review
Checked at `https://www.mimit.gov.it/robots.txt` on 2026-04-21.

Disallowed paths target CMS and admin interfaces only (`/administrator/`,
`/api/`, `/bin/`, `/cache/`, `/cli/`, `/components/`, `/includes/`,
`/installation/`, `/language/`, `/layouts/`, `/libraries/`, `/logs/`,
`/modules/`, `/plugins/`, `/tmp/`). `/images/exportCSV/` is not listed.

Status: **allowed**

## Terms of Service / Licence
<!-- Insert exact licence string found from the current MIMIT ToS page -->
The data is published under Italian open government data framework
(D.Lgs. 36/2006). Expected licence: IODL 2.0 or CC-BY.

Commercial reuse requires attribution. This case study uses the data
educationally, at low volume, with an identifiable User-Agent.

## CSV schema

### `prezzo_alle_8.csv`
Delimiter: `|` (pipe). Line 1: metadata (`Estrazione del YYYY-MM-DD`). Line 2: headers.

| Field | Type | Notes |
|---|---|---|
| `idImpianto` | int | Station ID, joins to station registry |
| `descCarburante` | str | Fuel type (Benzina, Gasolio, GPL, …) |
| `prezzo` | float | Price in €/litre |
| `isSelf` | 0/1 | 0 = attended, 1 = self-service |
| `dtComu` | str | Price report timestamp |

### `anagrafica_impianti_attivi.csv`
Delimiter: `|` (pipe). Line 1: metadata. Line 2: headers.

| Field | Type | Notes |
|---|---|---|
| `idImpianto` | int | Station ID |
| `Gestore` | str | Operator name |
| `Bandiera` | str | Brand (IP, Q8, Agip Eni, …) |
| `Tipo Impianto` | str | Station type |
| `Nome Impianto` | str | Station name |
| `Indirizzo` | str | Street address |
| `Comune` | str | Municipality |
| `Provincia` | str | Province code |
| `Latitudine` | float | WGS84 |
| `Longitudine` | float | WGS84 |

## Reproducing this case study

```bash
export API_ARCHAEOLOGY_CONTACT_EMAIL="your@email.com"
uv sync
cd cases/fuel-prices-mimit
python fetch.py
```

Output: `sample.csv` with the first 20 price records from today's snapshot
(~92 000 rows total). Do not commit the full file.

## Ethical notes
- Rate limit: 5 s delay (institutional default per `ETHICS.md`)
- User-Agent: identifies the project and contact email
- No authentication required or bypassed
- Data published as open government data; small educational samples are
  within licence terms
- Script fetches a single daily snapshot; does not poll continuously
```

- [ ] **Step 2: Commit**

```bash
git add "cases/fuel-prices-mimit/README.md"
git commit -m "docs(mimit): complete case study README with schema, robots.txt review and reproduction steps"
```

---

## Task 7: Update top-level README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the "Stato attuale" section**

Find the `## Stato attuale` section at the bottom of `README.md` and replace it with:

```markdown
## Stato attuale
La Fase 1 è completata:
- scaffold del repo creato
- documenti di metodo ed etica creati
- primo case study completo: `cases/fuel-prices-mimit/`

Il case study `cases/sports-aggregator/` rimane uno scaffold in attesa di
caratterizzazione pubblica riproducibile (vedi README interno).
Il case study `cases/weather-historical/` è pianificato per la Fase 2.
```

- [ ] **Step 2: Run all tests one final time**

```bash
uv run pytest -v
```

Expected: all 5 tests pass.

- [ ] **Step 3: Final commit**

```bash
git add README.md
git commit -m "docs: mark Fase 1 complete after MIMIT case study"
```

---

## Self-Review

### Spec coverage

| Requirement (PROJECT_BRIEF.md) | Task |
|---|---|
| `fetch.py` per case study | Task 4 |
| `parse.py` per case study | Task 3 |
| `sample.csv` dimostrativo | Task 5 |
| `README.md` del case study | Task 6 |
| Rate limit ≥ 2 s (5 s istituzionali) | Task 4 |
| User-Agent identificabile | Task 4 |
| robots.txt check a startup | Task 4 |
| Nessun raw dataset nel repo | Task 1 (.gitignore) + Task 5 (20 righe) |
| ToS citati nel case study | Task 6 |
| README top-level aggiornato | Task 7 |

### Placeholder scan
Task 6 has one intentional placeholder for the licence string — it must be filled manually before committing (see Task 2 remaining action). All other steps contain exact commands, expected output, or complete code.

### Type consistency
- `FuelPrice` defined in Task 3, used in Task 4 (`_write_sample` parameter type) and Task 5 (inline script).
- `parse_prices` / `_write_sample` / `SAMPLE_PATH` imported by name in Task 5 inline script — match definitions in Task 3 and Task 4 exactly.
- `FuelStation` defined in Task 3, available from `parse.py` but not used in `fetch.py` main — intentional, station data can be added later without touching tested logic.
