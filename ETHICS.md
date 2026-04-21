# Ethics and Scope Policy

This repository documents a technique for accessing data through websites' own internal APIs. That technique is legitimate for a narrow set of uses and inappropriate for others. This document defines the boundary and the operational rules that apply to every case study in this repository.

## Intended use
This repository is educational. Appropriate uses include:
- personal research
- academic study
- journalism based on public data
- one-off analyses
- learning how modern web applications expose their data

Inappropriate uses include:
- building a commercial service on undocumented endpoints
- mass-downloading content for redistribution
- circumventing paid tiers that provide genuine value
- targeting sites that explicitly prohibit automated access

## Operational rules
Every script in this repository should enforce the following defaults:

### Rate limiting
- minimum delay of 2 seconds between requests to the same host
- default of 5 seconds for smaller or institutional hosts
- scripts must reject values below 1 second

### User-Agent
Requests must identify themselves honestly, with a format equivalent to:

`ApiArchaeology/1.0 (educational; +github.com/<user>/api-archaeology)`

A contact email should be configurable through environment variable.

### robots.txt
Scripts should read `robots.txt` before running and skip explicitly disallowed paths for general crawlers.

### Data handling
- no raw dataset redistribution in the repository
- only small demonstration samples belong in version control
- no authentication bypass

If a target later introduces authentication, the relevant case study should be updated and the code removed or clearly marked non-functional.

## Terms of service
Each case study should cite the site's ToS as observed at the time of the study and explain why the specific educational, rate-limited and non-redistributive use is or is not compatible.

Where the ToS is ambiguous, the ambiguity must be stated. Where it is clearly prohibitive, the case study should not be included.

## Removal requests
If a site operator asks for a case study to be modified or removed, the default response is compliance within one week. Technical argument is usually cheap; reputational cost is not.

## Liability
Users are responsible for ensuring that any real-world use complies with applicable law and with the terms of service of the target site. This repository does not endorse derivative uses that exceed the educational scope described here.

## One rule
If you would be uncomfortable explaining the exact workflow to the site operator, stop. The goal is a method that remains technically clear and ethically defensible.
