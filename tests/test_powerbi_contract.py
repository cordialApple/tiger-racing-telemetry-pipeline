import json
import re

import pytest

import config
from api.models import Channel, Reading, SensorStat, SessionCatalog

MODEL_DIR = config.ROOT / "powerbi" / "tiger-telemetry.SemanticModel" / "definition"
TABLES_DIR = MODEL_DIR / "tables"
PAGES_DIR = config.ROOT / "powerbi" / "tiger-telemetry.Report" / "definition" / "pages"
_GUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
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


def model_members() -> set[tuple[str, str]]:
    members = set()
    for path in TABLES_DIR.glob("*.tmdl"):
        table = path.stem
        text = path.read_text(encoding="utf-8")
        for name in re.findall(r"^\tmeasure '([^']+)'", text, re.MULTILINE):
            members.add((table, name))
        for name in re.findall(r"^\tmeasure ([A-Za-z_]\w*) =", text, re.MULTILINE):
            members.add((table, name))
        for name in re.findall(r"^\tcolumn '([^']+)'", text, re.MULTILINE):
            members.add((table, name))
        for name in re.findall(r"^\tcolumn ([A-Za-z_]\w*)", text, re.MULTILINE):
            members.add((table, name))
    return members


def visual_files():
    return sorted(PAGES_DIR.glob("*/visuals/*/visual.json"))


def field_references(node, found):
    if isinstance(node, dict):
        for kind in ("Measure", "Column"):
            body = node.get(kind)
            if isinstance(body, dict) and "Property" in body:
                entity = body.get("Expression", {}).get("SourceRef", {}).get("Entity")
                if entity:
                    found.add((entity, body["Property"]))
        for value in node.values():
            field_references(value, found)
    elif isinstance(node, list):
        for value in node:
            field_references(value, found)
    return found


def test_every_visual_reference_resolves_in_the_model():
    known = model_members()
    unresolved = {}
    for path in visual_files():
        page = path.parents[2].name
        refs = field_references(json.loads(path.read_text(encoding="utf-8")), set())
        missing = sorted(refs - known)
        if missing:
            unresolved.setdefault(page, []).extend(missing)
    assert not unresolved, f"visuals reference members the model does not define: {unresolved}"


def test_page_order_matches_the_pages_on_disk():
    order = json.loads((PAGES_DIR / "pages.json").read_text(encoding="utf-8"))["pageOrder"]
    on_disk = {p.parent.name for p in PAGES_DIR.glob("*/page.json")}
    assert set(order) == on_disk
    assert len(order) == len(set(order))


def test_lineage_tags_are_unique_guids():
    tags = []
    for path in TABLES_DIR.glob("*.tmdl"):
        tags += re.findall(r"lineageTag: (\S+)", path.read_text(encoding="utf-8"))
    assert [t for t in tags if not _GUID.match(t)] == []
    assert len(tags) == len(set(tags))


def test_visual_names_are_unique_across_the_report():
    names = [json.loads(p.read_text(encoding="utf-8"))["name"] for p in visual_files()]
    assert len(names) == len(set(names))


def test_session_sort_key_does_not_assume_numeric_ids():
    text = tmdl("Sessions")
    assert "VALUE(Sessions[session_id])" not in text
    assert "column session_no = INT(Sessions[started_at_local] * 86400)" in text


def test_session_labels_use_event_local_time():
    text = tmdl("Sessions")
    assert 'FORMAT(Sessions[started_at_local], "MMM d HH:mm")' in text
    assert "started_at_local" in SessionCatalog.model_fields


def test_ev_measures_are_platform_scoped():
    text = tmdl("Channels")
    for measure in ("EV Dead Channels", "EV Channel Rows", "EV Channel Count"):
        body = text.split(f"measure '{measure}'", 1)[1].split("displayFolder", 1)[0]
        assert 'Channels[platform] = "ev-2026"' in body, measure
