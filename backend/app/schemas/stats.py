from datetime import date
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
