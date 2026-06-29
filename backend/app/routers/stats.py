from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.crud import stats as stats_crud
from backend.app.schemas.stats import (
    ArtistStats,
    HourlyStats,
    WeekdayStats,
    DailyStats,
    YearlyStats,
    StatsSummary,
)

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=StatsSummary)
def get_stats_summary(db: Session = Depends(get_db)):
    return stats_crud.stats_summary(db)


@router.get("/artist", response_model=list[ArtistStats])
def get_artist_stats(db: Session = Depends(get_db)):
    return stats_crud.stats_by_artist(db)


@router.get("/hourly", response_model=list[HourlyStats])
def get_hourly_stats(db: Session = Depends(get_db)):
    return stats_crud.stats_by_hourly(db)


@router.get("/weekday", response_model=list[WeekdayStats])
def get_weekday_stats(db: Session = Depends(get_db)):
    return stats_crud.stats_by_weekday(db)


@router.get("/daily", response_model=list[DailyStats])
def get_daily_stats(db: Session = Depends(get_db)):
    return stats_crud.stats_by_daily(db)


@router.get("/yearly", response_model=list[YearlyStats])
def get_yearly_stats(db: Session = Depends(get_db)):
    return stats_crud.stats_by_yearly(db)
