from datetime import date
from typing import Optional
from pydantic import BaseModel


class ArtistStats(BaseModel):
    artist: str
    count: int


class HourlyStats(BaseModel):
    hour: int
    count: int


class WeekdayStats(BaseModel):
    weekday: str
    count: int


class DailyStats(BaseModel):
    date: date
    count: int


class YearlyStats(BaseModel):
    year: int
    count: int


class StatsSummary(BaseModel):
    total_logs: int
    favorite_artist: Optional[str] = None
    average_rating: Optional[float] = None
