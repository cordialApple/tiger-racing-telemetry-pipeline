from datetime import UTC, datetime

from db.repository import ReadingRepository
from db.schema_manager import SchemaManager
from parser.models import SensorSpec, SessionMeta

SESSION_ID = "test_session_repo"
PACKET_ID = "test_packet_repo"
SOURCE_FILE = "test_repo_fixture.csv"
STARTED = datetime(2023, 6, 1, 12, 0, 0, tzinfo=UTC)


def _cleanup(conn):
    conn.execute("DELETE FROM sensor_readings WHERE session_id = %s", (SESSION_ID,))
    conn.execute("DELETE FROM ingestion_source WHERE packet_id = %s", (PACKET_ID,))
    conn.execute("DELETE FROM ingestion_log WHERE packet_id = %s", (PACKET_ID,))
    conn.execute("DELETE FROM sessions WHERE session_id = %s", (SESSION_ID,))


def test_full_ingestion_cycle(database):
    SchemaManager(database).apply()
    repo = ReadingRepository()

    sensors = [
        SensorSpec("rpm", "Engine RPM", "rpm", "float", 0, 15000, "ice-2023"),
        SensorSpec("speed", "Vehicle speed", "kph", "float", 0, 300, "ice-2023"),
    ]
    readings = [
        (STARTED, "rpm", 1000.0),
        (STARTED, "speed", 25.0),
        (STARTED.replace(second=1), "rpm", 2000.0),
        (STARTED.replace(second=1), "speed", 40.0),
    ]
    meta = SessionMeta(
        session_id=SESSION_ID, source_file=SOURCE_FILE, vehicle="TR23", racer="Driver",
        championship="FSAE", session_name="Test", comment=None, started_at=STARTED,
        sample_rate_hz=20, duration_s=2, segment_times=None,
        platform="ice-2023", event="Drive Day 7_18",
    )

    with database.connection() as conn:
        _cleanup(conn)
        repo.upsert_sensors(conn, sensors)
        repo.insert_session(conn, meta)
        assert repo.is_loaded(conn, PACKET_ID) is False

        written = repo.copy_readings(conn, SESSION_ID, readings)
        assert written == len(readings)

        repo.log_ingestion(conn, PACKET_ID, SESSION_ID, SOURCE_FILE, 2, written)
        assert repo.is_loaded(conn, PACKET_ID) is True

        n = conn.execute(
            "SELECT count(*) FROM sensor_readings WHERE session_id = %s", (SESSION_ID,)
        ).fetchone()[0]
        assert n == len(readings)

        assert conn.execute(
            "SELECT platform, event FROM sessions WHERE session_id = %s", (SESSION_ID,)
        ).fetchone() == ("ice-2023", "Drive Day 7_18")
        assert conn.execute(
            "SELECT platform FROM sensors WHERE sensor_name = 'rpm'"
        ).fetchone()[0] == "ice-2023"

        _cleanup(conn)


def test_duplicate_source_paths_are_all_recorded(database):
    SchemaManager(database).apply()
    repo = ReadingRepository()
    meta = SessionMeta(
        session_id=SESSION_ID, source_file=SOURCE_FILE, vehicle=None, racer="Tristan",
        championship=None, session_name=None, comment=None, started_at=STARTED,
        sample_rate_hz=10, duration_s=2, segment_times=None,
        platform="ev-2026", event="Drive Day 7_18",
    )

    with database.connection() as conn:
        _cleanup(conn)
        repo.insert_session(conn, meta)
        repo.log_ingestion(conn, PACKET_ID, SESSION_ID, "Tristan Drive/a.csv", 1, 0)
        repo.record_source(conn, PACKET_ID, "Tristan Drive/a.csv")
        repo.record_source(conn, PACKET_ID, "Yianni Drive/a.csv")
        repo.record_source(conn, PACKET_ID, "Yianni Drive/a.csv")

        paths = conn.execute(
            "SELECT source_path FROM ingestion_source WHERE packet_id = %s ORDER BY source_path",
            (PACKET_ID,),
        ).fetchall()
        assert [p[0] for p in paths] == ["Tristan Drive/a.csv", "Yianni Drive/a.csv"]

        _cleanup(conn)


def test_source_file_no_longer_unique(database):
    SchemaManager(database).apply()
    with database.connection() as conn:
        constraint = conn.execute(
            "SELECT 1 FROM pg_constraint WHERE conname = 'sessions_source_file_key'"
        ).fetchone()
        assert constraint is None
