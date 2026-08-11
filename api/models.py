from datetime import datetime

from pydantic import BaseModel


class SessionCatalog(BaseModel):
    session_id: str
    source_file: str
    platform: str | None
    event: str | None
    vehicle: str | None
    racer: str | None
    championship: str | None
    session_name: str | None
    comment: str | None
    started_at: datetime
    duration_s: int | None
    sample_rate_hz: int
    reading_count: int | None
    loaded_at: datetime | None


class Channel(BaseModel):
    session_id: str
    sensor_name: str
    platform: str | None
    description: str | None
    unit: str | None
    data_type: str
    min_range: float | None
    max_range: float | None
    n: int
    avg_value: float | None
    min_value: float | None
    max_value: float | None
    has_signal: bool


class Reading(BaseModel):
    session_id: str
    sensor_name: str
    ts: datetime
    t_seconds: float
    value: float | None
    avg_value: float | None
    min_value: float | None
    max_value: float | None


class ReadingPage(BaseModel):
    session_id: str
    sensor: str | None
    downsample: str
    limit: int
    offset: int
    total: int
    count: int
    rows: list[Reading]


class SensorStat(BaseModel):
    session_id: str
    sensor_name: str
    n: int
    avg_value: float | None
    min_value: float | None
    max_value: float | None
