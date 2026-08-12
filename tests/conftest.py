import psycopg
import pytest

import config
from db.connection import Database, TimescaleConfig
from db.schema_manager import SchemaManager
from parser.aim_parser import AimParser

SESSION_1 = config.RAW_DIR / "2023" / "1.csv"
_DB_FIXTURES = {"database", "loaded_db"}


def pytest_collection_modifyitems(config, items):
    for item in items:
        if _DB_FIXTURES & set(item.fixturenames):
            item.add_marker(pytest.mark.db)


@pytest.fixture(scope="session")
def parsed():
    return AimParser().parse(SESSION_1)


def _ensure_test_database(cfg: TimescaleConfig):
    admin = TimescaleConfig(dbname="postgres", user=cfg.user, password=cfg.password,
                            host=cfg.host, port=cfg.port)
    with psycopg.connect(admin.dsn(), autocommit=True) as conn:
        exists = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (cfg.dbname,)
        ).fetchone()
        if not exists:
            conn.execute(f'CREATE DATABASE "{cfg.dbname}"')


@pytest.fixture(scope="session")
def database():
    cfg = TimescaleConfig(dbname=config.TEST_DB_NAME)
    try:
        _ensure_test_database(cfg)
        db = Database(cfg)
        with db.connection() as conn:
            available = conn.execute(
                "SELECT 1 FROM pg_available_extensions WHERE name = 'timescaledb'"
            ).fetchone()
    except Exception as e:
        pytest.skip(f"no database available: {e}")
    if available is None:
        pytest.skip("timescaledb extension not available")
    SchemaManager(db).apply()
    yield db
    db.close()
