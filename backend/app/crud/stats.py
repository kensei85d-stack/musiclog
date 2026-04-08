from collections import Counter
from datetime import date
from sqlalchemy.orm import Session, joinedload

from backend.app.models.Play_history import PlayHistory
from backend.app.models.track import Track


def _load_play_histories(db: Session):
    return db.query(PlayHistory).options(
        joinedload(PlayHistory.track).joinedload(Track.artist)
    ).all()


def stats_by_artist(db: Session):
    histories = _load_play_histories(db)
    counts = Counter(
        history.track.artist.name
        for history in histories
        if history.track is not None and history.track.artist is not None
    )
    return [
        {"artist": name, "count": count}
        for name, count in counts.most_common()
    ]


def stats_by_hourly(db: Session):
    histories = _load_play_histories(db)
    counts = Counter(history.played_at.hour for history in histories if history.played_at is not None)
    return [
        {"hour": hour, "count": count}
        for hour, count in sorted(counts.items())
    ]


def stats_by_weekday(db: Session):
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    histories = _load_play_histories(db)
    counts = Counter(
        weekday_names[history.played_at.weekday()]
        for history in histories
        if history.played_at is not None
    )
    return [
        {"weekday": weekday, "count": count}
        for weekday, count in counts.items()
    ]


def stats_by_daily(db: Session):
    histories = _load_play_histories(db)
    counts = Counter(
        history.played_at.date()
        for history in histories
        if history.played_at is not None
    )
    return [
        {"date": played_date, "count": count}
        for played_date, count in sorted(counts.items())
    ]


def stats_by_yearly(db: Session):
    histories = _load_play_histories(db)
    counts = Counter(
        history.played_at.year
        for history in histories
        if history.played_at is not None
    )
    return [
        {"year": year, "count": count}
        for year, count in sorted(counts.items())
    ]
