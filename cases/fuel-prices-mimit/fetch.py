import csv
import time
import urllib.robotparser
from pathlib import Path
from typing import List

import httpx
from cases.fuel_prices_mimit.parse import FuelPrice, parse_prices

# Configuration
PRICES_URL = "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv"
ROBOTS_URL = "https://www.mimit.gov.it/robots.txt"
INSTITUTIONAL_DELAY = 5.0
CONTACT_EMAIL = "p3zzotto1926@gmail.com"
REPO_URL = "https://github.com/antonio-cioffi/api-archaeology"
USER_AGENT = f"api-archaeology-crawler (contact: {CONTACT_EMAIL}, repo: {REPO_URL})"

def _build_client() -> httpx.Client:
    \"\"\"Returns an httpx Client with the configured User-Agent and timeout.\"\"\"
    return httpx.Client(
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
        timeout=30.0
    )

def _check_robots(client: httpx.Client):
    \"\"\"Checks robots.txt to see if downloading the prices CSV is allowed.\"\"\"
    rp = urllib.robotparser.RobotFileParser()
    try:
        response = client.get(ROBOTS_URL)
        rp.parse(response.text.splitlines())
    except Exception as e:
        # If robots.txt is missing or unreachable, we assume it's allowed or
        # handle it as a warning, but here we follow the spec to check it.
        print(f"Warning: Could not fetch robots.txt: {e}")
        return

    if not rp.can_fetch(USER_AGENT, PRICES_URL):
        raise RuntimeError(f"Access to {PRICES_URL} is forbidden by robots.txt")

def _fetch_csv(client: httpx.Client) -> str:
    \"\"\"Downloads the CSV and handles encoding."""\"\"\"
    response = client.get(PRICES_URL)
    response.raise_for_status()

    content = response.content
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("windows-1252")

def _write_sample(prices: List[FuelPrice], output_path: str = "sample.csv"):
    \"\"\"Writes the first 20 prices to a sample CSV file.\"\"\"
    sample = prices[:20]
    if not sample:
        print("No prices to write to sample.")
        return

    # Use Pydantic model fields as headers
    fieldnames = FuelPrice.__fields__.keys() if hasattr(FuelPrice, '__fields__') else FuelPrice.model_fields.keys()

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for price in sample:
            writer.writerow(price.dict() if hasattr(price, 'dict') else price.model_dump())

def main():
    with _build_client() as client:
        print("Checking robots.txt...")
        _check_robots(client)

        print(f"Respecting institutional delay: {INSTITUTIONAL_DELAY}s...")
        time.sleep(INSTITUTIONAL_DELAY)

        print("Fetching prices CSV...")
        csv_content = _fetch_csv(client)

        # Save to temporary file for the parser to read
        tmp_file = Path("temp_prices.csv")
        tmp_file.write_text(csv_content, encoding="utf-8")

        try:
            print("Parsing prices...")
            prices = parse_prices(str(tmp_file))

            print(f"Writing sample of {len(prices[:20])} records to sample.csv...")
            _write_sample(prices)
            print("Done.")
        finally:
            if tmp_file.exists():
                tmp_file.unlink()

if __name__ == "__main__":
    main()
