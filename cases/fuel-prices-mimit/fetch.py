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
    f"(educational; +github.com/cioffiAI/api-archaeology; contact={CONTACT_EMAIL})"
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
        writer = csv.DictWriter(f, fieldnames=list(FuelPrice.model_fields.keys()))
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
