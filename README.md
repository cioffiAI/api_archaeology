# api-archaeology

Finding the APIs behind the websites that pretend they do not have one.

## The thesis
For many categories of data, the paid market exists largely because of information asymmetry. The public source already exists, for free, if you know where to look, and where to look is a skill that can be taught.

This repository documents a method for identifying undocumented HTTP endpoints behind data-heavy websites, with three case studies across unrelated domains:
- sports data
- historical weather
- fuel prices

The method is in `METHOD.md`. The ethical and operational constraints are in `ETHICS.md`.

## Why this matters
Most modern data-heavy websites are thin clients on top of their own backend APIs. The browser calls those APIs to render the UI. If the data is public and the site does not actively defend the endpoint, the interesting work is not HTML scraping. The interesting work is recognizing which backend calls matter, characterizing them correctly, and deciding when reuse is legitimate.

This repo is about that recognition step. It is not a scraping framework and it is not a bypass tool.

## Repository structure
- `METHOD.md`: domain-agnostic methodology in four phases
- `ETHICS.md`: scope, rate limiting, robots.txt, ToS and removal policy
- `cases/sports-aggregator/`: first case study scaffold
- `cases/weather-historical/`: second case study placeholder
- `cases/fuel-prices-mimit/`: third case study placeholder
- `paper/`: mini-paper output planned for Phase 3

## Case studies
### `cases/sports-aggregator/`
Pattern: semantically filtered tabular endpoints.

This is the entry-level case because it is the most common and most didactic pattern. In the public repo, the target is intentionally framed generically and does not expose the original site name or live endpoint details.

### `cases/weather-historical/`
Pattern: time-series endpoints behind a restrictive UI.

The likely target class is a regional environmental agency or comparable public-source portal.

### `cases/fuel-prices-mimit/`
Pattern: open data already published, but obscured by the main UI.

This case focuses on the Italian fuel price observatory data published under the MIMIT ecosystem.

## Quickstart
```bash
uv venv
uv sync
python cases/sports-aggregator/fetch.py
```

The current `fetch.py` is intentionally a scaffold. It enforces policy defaults and stops before targeting any real endpoint.

## Ethics and scope
This repository is educational. Scripts must use conservative rate limits, an identifying User-Agent, and no authentication bypass. Raw datasets are not redistributed here. Only small demonstration samples belong in the repo.

If you represent one of the documented targets and want a case study modified or removed, the policy in `ETHICS.md` applies.

## Current status
Phase 1 is in progress:
- repo scaffold created
- method and ethics documents created
- first case study scaffold created
- endpoint characterization still missing

The next real work is not more scaffolding. It is one complete case study with reproducible observations.
