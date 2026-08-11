import csv
import hashlib
import re
import statistics
from datetime import date, datetime, timedelta
from itertools import pairwise
from pathlib import Path
from zoneinfo import ZoneInfo

from parser.cleaner import split_unit
from parser.models import ParsedSession, SessionMeta

_TZ = ZoneInfo("America/Chicago")
_FILENAME = re.compile(
    r"^(?P<date>\d{4}-\d{1,2}-\d{1,2})\s+"
    r"(?P<time>\d{2}\.\d{2}\.\d{2})\s*"
    r"(?:\((?P<note>[^)]*)\))?$"
)
_DRIVER_SUFFIX = " Drive"
_CLOCK_FORMAT = "%H:%M:%S.%f"
_DATE_FORMAT = "%Y-%m-%d"


class CanLogParser:
    platform = "ev-2026"

    def sniff(self, head: str) -> bool:
        return head.startswith("Time,")

    def parse(self, path) -> ParsedSession:
        path = Path(path)
        raw = path.read_bytes()
        rows = list(csv.reader(raw.decode("utf-8").splitlines()))
        data = [row for row in rows[1:] if row and any(cell.strip() for cell in row)]
        if len(data) < 2:
            raise ValueError(f"{path.name} has fewer than two data rows")

        names, units = self._columns(rows[0][1:])
        started_on, note = self._filename_fields(path)
        stamps = self._timestamps([row[0] for row in data], started_on)

        return ParsedSession(
            session=self._build_session(path, stamps, note),
            units=units,
            readings=self._readings(data, names, stamps),
            packet_id=hashlib.sha256(raw).hexdigest(),
            row_count=len(data),
        )

    @staticmethod
    def _columns(columns: list[str]) -> tuple[list[str], dict[str, str | None]]:
        names, units = [], {}
        for column in columns:
            name, unit = split_unit(column)
            if name in units:
                raise ValueError(f"duplicate channel {name!r} after unit stripping")
            names.append(name)
            units[name] = unit
        return names, units

    @staticmethod
    def _filename_fields(path: Path) -> tuple[date, str | None]:
        match = _FILENAME.match(path.stem.strip())
        if match is None:
            raise ValueError(f"unrecognised filename {path.name!r}")
        started_on = datetime.strptime(match["date"], _DATE_FORMAT).date()
        return started_on, (match["note"] or "").strip() or None

    @staticmethod
    def _timestamps(cells: list[str], started_on: date) -> list[datetime]:
        stamps, day, previous = [], started_on, None
        for cell in cells:
            clock = datetime.strptime(cell, _CLOCK_FORMAT).time()
            # logger records clock time only, so a backwards step means the run crossed midnight
            if previous is not None and clock < previous:
                day += timedelta(days=1)
            stamps.append(datetime.combine(day, clock, tzinfo=_TZ))
            previous = clock
        return stamps

    def _build_session(self, path: Path, stamps: list[datetime], note: str | None) -> SessionMeta:
        driver, event = self._location(path)
        return SessionMeta(
            session_id=self._session_id(stamps[0], driver),
            source_file=path.name,
            vehicle=None,
            racer=driver,
            championship=None,
            session_name=None,
            comment=note,
            started_at=stamps[0],
            sample_rate_hz=self._sample_rate(stamps),
            duration_s=round((stamps[-1] - stamps[0]).total_seconds()),
            segment_times=None,
            platform=self.platform,
            event=event,
        )

    @staticmethod
    def _location(path: Path) -> tuple[str | None, str | None]:
        parent = path.parent.name
        if parent.endswith(_DRIVER_SUFFIX):
            return parent[: -len(_DRIVER_SUFFIX)], path.parent.parent.name or None
        return None, parent or None

    @staticmethod
    def _session_id(started_at: datetime, driver: str | None) -> str:
        stamp = started_at.strftime("%Y-%m-%d_%H%M%S")
        return f"{stamp}_{driver.lower()}" if driver else stamp

    @staticmethod
    def _sample_rate(stamps: list[datetime]) -> int:
        deltas = [(b - a).total_seconds() for a, b in pairwise(stamps)]
        return round(1 / statistics.median(deltas))

    @staticmethod
    def _readings(data, names, stamps) -> list[tuple[datetime, str, float]]:
        rows = []
        for ts, row in zip(stamps, data, strict=True):
            for name, value in zip(names, row[1:], strict=False):
                if value:
                    rows.append((ts, name, float(value)))
        return rows
