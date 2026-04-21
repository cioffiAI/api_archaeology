# Case Study: MIMIT Fuel Prices (API Archaeology)

## Overview
This case study demonstrates the "API Archaeology" pattern: extracting structured data that is publicly available but hidden or obscured from the main user interface. In this instance, the Ministry of Enterprises and Made in Italy (MIMIT) publishes daily fuel price datasets in CSV format via direct URLs, even though the primary website focuses on visual summaries.

## Data Source
- **Source**: Ministero delle Imprese e del Made in Italy (MIMIT)
- **Data Type**: Daily fuel prices and station registry.
- **Current URL**: [https://www.mimit.gov.it/it/prezzo-medio-carburanti](https://www.mimit.gov.it/it/prezzo-medio-carburanti)
- **Direct Data Endpoint**: `https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv`
- **License**: The data is available for free reuse under the **IODL 2.0 (Licenza Aperta dei Dati Pubblici)**.

## Technical Implementation

### Robots.txt Review
The crawler respects the `robots.txt` policy of `www.mimit.gov.it`. Before fetching, the implementation checks if the specific CSV path is allowed. Based on the current configuration, the access is permitted, but a professional `User-Agent` and a mandatory institutional delay (5.0s) are implemented to avoid overloading the government servers.

### CSV Schema & Parsing
The source CSV files use a non-standard format:
- **Delimiter**: Pipe (`|`)
- **Metadata**: The first line of the file contains metadata and must be skipped before parsing the headers.
- **Encoding**: Typically `utf-8` or `windows-1252`.

**Sample Schema (`prezzo_alle_8.csv`):**
| Field | Description |
| :--- | :--- |
| `idImpianto` | Unique identifier for the fuel station |
| `descCarburante` | Description of the fuel type |
| `prezzo` | Price per liter (comma as decimal separator) |
| `isSelf` | Indicates if the station is self-service |
| `dtComu` | Date of communication |

## Reproduction Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/antonio-cioffi/api-archaeology.git
   cd api-archaeology/cases/fuel-prices-mimit
   ```

2. **Install dependencies**:
   ```bash
   pip install httpx pydantic
   ```

3. **Run the fetcher**:
   ```bash
   python fetch.py
   ```
   This script will check `robots.txt`, download the latest prices CSV, and generate a `sample.csv` containing the first 20 records.

4. **Verify the data**:
   Check `sample.csv` to ensure the data was correctly parsed and the decimal separators were converted to dots.

## Key Findings
- **Pattern**: The data is hosted in a static directory (`/images/exportCSV/`), which is often overlooked by standard site navigation.
- **Reliability**: The endpoints are stable and provide the raw data required for historical analysis, bypassing the need for complex HTML scraping.
