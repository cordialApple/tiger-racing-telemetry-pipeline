import pytest

import config
from db.connection import Database
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


@pytest.fixture(scope="session")
def database():
    db = Database()
    try:
        with db.connection() as conn:
            available = conn.execute(
                "SELECT 1 FROM pg_available_extensions WHERE name = 'timescaledb'"
            ).fetchone()
    except Exception as e:
        pytest.skip(f"no database available: {e}")
    if available is None:
        pytest.skip("timescaledb extension not available")
    yield db
    db.close()
