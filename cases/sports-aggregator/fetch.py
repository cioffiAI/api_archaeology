from __future__ import annotations

import os
import sys
import time
import urllib.parse
import urllib.robotparser

import httpx


MIN_DELAY_SECONDS = 2.0
INSTITUTIONAL_DELAY_SECONDS = 5.0
DEFAULT_DELAY_SECONDS = MIN_DELAY_SECONDS
CONTACT_EMAIL = os.getenv("API_ARCHAEOLOGY_CONTACT_EMAIL", "set-contact-email@example.com")
USER_AGENT = (
    "ApiArchaeology/1.0 "
    "(educational; +github.com/<cioffiAI>/api-archaeology; "
    f"contact={'cioffi.antonio2004@gmail.com'})"
)


def build_client() -> httpx.Client:
    return httpx.Client(
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
        timeout=30.0,
    )


def ensure_allowed_by_robots(target_url: str, user_agent: str) -> None:
    parsed = urllib.parse.urlparse(target_url)
    robots_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    parser.read()
    if not parser.can_fetch(user_agent, target_url):
        raise RuntimeError(f"robots.txt disallows access to {target_url}")


def enforce_delay(delay_seconds: float = DEFAULT_DELAY_SECONDS) -> None:
    if delay_seconds < 1.0:
        raise ValueError("Delay below 1 second is not allowed by project policy.")
    time.sleep(delay_seconds)


def fail_closed() -> None:
    raise RuntimeError(
        "Sports case study scaffold: no live endpoint is configured in this "
        "repository. Public materials stay generic and omit target-specific "
        "request details. Any future implementation must also stay outside "
        "robots.txt-disallowed paths."
    )


def main() -> None:
    print("Sports aggregator case study is currently a scaffold.")
    print("No live target is configured in this repository.")
    print(f"Default User-Agent: {USER_AGENT}")
    print(f"Default delay: {DEFAULT_DELAY_SECONDS} seconds")
    try:
        fail_closed()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
