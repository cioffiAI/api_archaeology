from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SportsRecord(BaseModel):
    competition: str = Field(default="")
    season: str = Field(default="")
    event_date: str = Field(default="")
    home_team: str = Field(default="")
    away_team: str = Field(default="")


def normalize_record(raw: dict[str, Any]) -> SportsRecord:
    return SportsRecord(
        competition=str(raw.get("competition", "")),
        season=str(raw.get("season", "")),
        event_date=str(raw.get("event_date", "")),
        home_team=str(raw.get("home_team", "")),
        away_team=str(raw.get("away_team", "")),
    )
