# Sports Aggregator Case Study

## Status
Scaffold only. Endpoint characterization has not been completed yet.

## Public framing
This case study is intentionally framed generically as a sports data aggregator. The public repo should not expose the original site name, full live URL or real endpoint details until the case is fully reviewed against the repo's ethics policy and publication framing.

## Pattern
Semantically filtered tabular endpoints.

Typical shape:
- table-like responses
- filters such as season, competition, round or date
- parameters that map closely to visible UI controls

## What still needs to be documented
1. Target summary
2. Discovery sequence with DevTools screenshots
3. Endpoint characterization
4. Rate limit observations
5. ToS review
6. Market context
7. Small sample dataset

## File roles
- `fetch.py`: policy-aware request scaffold
- `parse.py`: normalization scaffold
- `sample.csv`: demonstration sample only, not bulk data

## Publication note
Do not fill this file with invented endpoint details. Characterize the real target first, then document only what is defensible to publish.
