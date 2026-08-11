import re

import pytest

import config
from api.models import Channel, Reading, SensorStat, SessionCatalog

TABLES_DIR = (
    config.ROOT / "powerbi" / "tiger-telemetry.SemanticModel" / "definition" / "tables"
)
_FROM_RECORDS = re.compile(r"\{(?P<columns>[^{}]*)\},\s*MissingField\.UseNull")
_QUOTED = re.compile(r'"([^"]+)"')

CONTRACT = {
    "Sessions": SessionCatalog,
    "Channels": Channel,
    "Readings": Reading,
    "Stats": SensorStat,
}
DERIVED_IN_POWER_QUERY = {"channel_key"}
SERVER_ONLY = {"loaded_at"}


def tmdl(table: str) -> str:
    return (TABLES_DIR / f"{table}.tmdl").read_text(encoding="utf-8")


def requested_columns(table: str) -> set[str]:
    match = _FROM_RECORDS.search(tmdl(table))
    assert match, f"{table}.tmdl has no Table.FromRecords column list"
    return set(_QUOTED.findall(match["columns"]))


def partition_count(table: str) -> int:
    return len(re.findall(r"^\tpartition ", tmdl(table), re.MULTILINE))


@pytest.mark.parametrize("table", sorted(CONTRACT))
def test_power_query_requests_only_columns_the_api_serves(table):
    served = set(CONTRACT[table].model_fields)
    assert requested_columns(table) <= served


@pytest.mark.parametrize("table", sorted(CONTRACT))
def test_power_query_requests_every_column_the_api_serves(table):
    served = set(CONTRACT[table].model_fields) - SERVER_ONLY
    assert served <= requested_columns(table)


@pytest.mark.parametrize("table", sorted(CONTRACT))
def test_declared_columns_are_sourced_or_derived(table):
    sourced = set(re.findall(r"sourceColumn: (\S+)", tmdl(table)))
    assert sourced <= requested_columns(table) | DERIVED_IN_POWER_QUERY


@pytest.mark.parametrize("table", ["Channels", "Readings", "Stats"])
def test_no_session_ids_are_hardcoded(table):
    text = tmdl(table)
    assert 'session_id = "' not in text
    assert "sessions/1/sensors" not in text
    assert partition_count(table) == 1


def test_session_sort_key_does_not_assume_numeric_ids():
    text = tmdl("Sessions")
    assert "VALUE(Sessions[session_id])" not in text
    assert "column session_no = INT(Sessions[started_at] * 86400)" in text
