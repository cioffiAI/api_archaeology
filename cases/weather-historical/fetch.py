from __future__ import annotations

import os
import sys
import time
import urllib.parse
import urllib.robotparser
from pathlib import Path

import gzip

import httpx
from selectolax.parser import HTMLParser

from parse import parse_ndjson, write_csv

BASE_URL = "https://dati-simc.arpae.it/opendata/osservati/meteo/storico"
INDEX_URL = f"{BASE_URL}/"
INSTITUTIONAL_DELAY = 2.0
CONTACT_EMAIL = os.getenv("API_ARCHAEOLOGY_CONTACT_EMAIL", "set-contact-email@example.com")
USER_AGENT = (
    f"ApiArchaeology/1.0 "
    f"(educational; +github.com/cioffiAI/api-archaeology; contact={CONTACT_EMAIL})"
)
SAMPLE_MONTH = "2024-01"
SAMPLE_CSV = Path(__file__).parent / "sample.csv"
SAMPLE_RECORDS = 20


def _build_client() -> httpx.Client:
    return httpx.Client(
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
        timeout=60.0,
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
        print(f"Warning: could not fetch robots.txt ({exc}). Proceeding.")
        return
    if not parser.can_fetch("*", target_url):
        raise RuntimeError(f"robots.txt disallows {target_url} — aborting.")


def _parse_index(html: str) -> list[str]:
    """Estrai tutti i link .json.gz dalla pagina index."""
    parser = HTMLParser(html)
    links: list[str] = []
    for node in parser.css("a"):
        href = node.attributes.get("href", "")
        if href.endswith(".json.gz"):
            links.append(href)
    return links


def _fetch_gzip(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    decompressed = gzip.decompress(response.content)
    return decompressed.decode("utf-8", errors="replace")


def main() -> None:
    with _build_client() as client:
        print("Checking robots.txt ...")
        _check_robots(client, INDEX_URL)

        print(f"Fetching index from {INDEX_URL} ...")
        response = client.get(INDEX_URL)
        response.raise_for_status()

        links = _parse_index(response.text)
        print(f"Found {len(links)} .json.gz files.")

        target = f"{BASE_URL}/{SAMPLE_MONTH}.json.gz"
        print(f"Checking for sample month: {target} ...")

        if f"{SAMPLE_MONTH}.json.gz" not in [Path(l).name for l in links]:
            print(f"Error: {SAMPLE_MONTH}.json.gz not found in index.", file=sys.stderr)
            sys.exit(1)

        print(f"Waiting {INSTITUTIONAL_DELAY}s (institutional rate limit) ...")
        time.sleep(INSTITUTIONAL_DELAY)

        print(f"Downloading {target} ...")
        ndjson_content = _fetch_gzip(client, target)
        print(f"Downloaded {len(ndjson_content):,} chars.")

        records = parse_ndjson(ndjson_content)
        print(f"Parsed {len(records)} station-timestep records.")

        if records:
            sample = records[:SAMPLE_RECORDS]
            write_csv(sample, SAMPLE_CSV)
            print(f"Wrote {len(sample)} rows to {SAMPLE_CSV}.")


if __name__ == "__main__":
    main()