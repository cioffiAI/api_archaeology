# API Archaeology: A Method

Most modern data-heavy websites are not monolithic HTML pages. They are frontends that render the UI by calling the site's own backend over HTTP and receiving structured data in return. That behavior is public by necessity: the frontend runs in the browser, so what it does is observable.

This document describes a systematic method for identifying those backend calls, characterizing them enough to be reused responsibly, and deciding when the effort is justified.

## Terminology
Two things are called "API" and the distinction matters:
- A documented API is a product. It has docs, a contract, API keys, stability promises and usually a paid plan.
- An undocumented internal API is the plumbing a public website uses to serve itself. Structurally it is still HTTP requests plus structured responses, but without a published contract or support.

This project is about the second category. It is not about bypassing authentication, defeating anti-bot systems, or accessing intentionally private data.

## The four phases
### Phase 1: Observation
Open the target site with DevTools on the Network tab and filter to `XHR` or `Fetch`. Interact with the UI normally: change dates, filters, pages or views. The goal is not immediate understanding. The goal is an inventory of requests that appear when the UI renders new data.

### Phase 2: Separation
Separate data-bearing requests from noise.

Data-bearing requests usually have:
- structured responses such as JSON or XML
- semantic parameters such as dates, IDs, ranges or names
- payloads that clearly match what the UI is showing

Ignore assets, analytics, fonts, tracking calls and similar noise.

### Phase 3: Characterization
For each candidate endpoint, answer a fixed set of questions:
- Does it require authentication?
- Can it be called from a fresh context and still return data?
- Which parameters are semantically necessary?
- Is pagination involved?
- What rate limit behavior is visible empirically?
- Does `robots.txt` or the site's ToS create an operational stop condition?

The output of this phase is a short written specification that another person can reproduce.

### Phase 4: Minimal reuse
Once the endpoint is characterized, the resulting script should be small and readable. It should perform the minimal HTTP calls, parse the structured payload, and persist the result in a portable format such as CSV, Parquet or SQLite.

If the script becomes complex before the endpoint is understood, the real problem is probably incomplete characterization.

## Three recurring patterns
### Pattern A: Semantically filtered tabular endpoints
Typical of sports aggregators and similar interfaces. The UI shows filterable tables and the backend exposes endpoints whose parameters map closely to visible controls.

### Pattern B: Time-series behind restrictive UI controls
Typical of historical weather portals. The frontend offers narrow date windows while the backend often accepts wider ranges than the UI suggests.

### Pattern C: Open data already published, but obscured by UI
Typical of government or regulated-industry datasets. The data is public already, but the site foregrounds a map or search UI rather than the flat feed.

## When the method does not apply
Stop when any of these is true:
- the data requires real authentication
- the site uses serious anti-bot protection
- the payload is intentionally obfuscated or signed
- the site's ToS clearly forbids automated access

In those cases the defensible path is to stop or use the official documented API if one exists.

## What the method is for
Appropriate uses:
- educational inspection of public data
- one-off research
- journalism on public datasets
- academic analysis on small scale
- personal projects that do not run as a service

Inappropriate uses:
- commercial services built on undocumented endpoints
- mass-download pipelines
- redistribution of raw data at scale
- anything that is hard to defend to the site operator in plain language

## A closing observation
The technical result matters, but the more interesting result is usually economic: a meaningful share of the data market is a market for easier access, not for intrinsically scarce data. The skill demonstrated here is recognizing when that gap is small.
