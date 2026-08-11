import pytest

from profiling.profiler import Profiler, schema_id
from profiling.render import draft_specs, report

HEADER = "Time,Motor RPM [Rpm],MC Temp [°C],Drive Enable"
WIDE_HEADER = HEADER + ",Flowrate"


def write(root, rel, header, rows):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(f"{clock},{values}" for clock, values in rows)
    path.write_text(f"{header}\n{body}\n", encoding="utf-8")
    return path


def drop(tmp_path, name="2026-7-18   20.02.21.csv", header=HEADER, rows=None):
    rows = rows or [("20:02:21.025", "1000,45,1"), ("20:02:21.125", "1200,45,1")]
    write(tmp_path, f"Tristan Drive/{name}", header, rows)
    return tmp_path


def test_schema_id_is_order_sensitive():
    assert schema_id(["a", "b"]) == schema_id(["a", "b"])
    assert schema_id(["a", "b"]) != schema_id(["b", "a"])


def test_profiles_channels_and_units(tmp_path):
    result = Profiler().run(drop(tmp_path))
    by_name = {c.name: c for c in result.channels}
    assert by_name["MC Temp"].unit == "°C"
    assert by_name["Motor RPM"].min == 1000
    assert by_name["Motor RPM"].max == 1200
    assert by_name["MC Temp"].is_constant
    assert by_name["Drive Enable"].inferred_type == "integer"


def test_detects_schema_drift(tmp_path):
    drop(tmp_path)
    write(
        tmp_path,
        "Ryan Drive/2026-7-18   21.50.44.csv",
        WIDE_HEADER,
        [("21:50:44.025", "900,40,1,4"), ("21:50:44.125", "950,40,1,4")],
    )
    result = Profiler().run(tmp_path)
    assert len(result.schemas) == 2
    assert sorted(len(names) for names in result.schemas.values()) == [3, 4]


def test_detects_duplicate_content(tmp_path):
    drop(tmp_path)
    rows = [("20:02:21.025", "1000,45,1"), ("20:02:21.125", "1200,45,1")]
    write(tmp_path, "Yianni Drive/2026-7-18   20.02.21.csv", HEADER, rows)
    result = Profiler().run(tmp_path)
    assert result.file_count == 2
    assert result.unique_content_count == 1
    assert len(result.duplicate_groups) == 1


def test_captures_unreadable_files_without_failing(tmp_path):
    drop(tmp_path)
    write(tmp_path, "Ryan Drive/nonsense.csv", "a,b", [("1", "2")])
    result = Profiler().run(tmp_path)
    assert len(result.files) == 1
    assert len(result.unreadable) == 1
    assert "nonsense.csv" in result.unreadable[0][0]


def test_flags_non_uniform_spacing(tmp_path):
    drop(
        tmp_path,
        rows=[
            ("20:02:21.025", "1000,45,1"),
            ("20:02:21.125", "1100,45,1"),
            ("20:02:21.925", "1200,45,1"),
        ],
    )
    assert Profiler().run(tmp_path).files[0].spacing_uniform is False


def test_missing_values_counted(tmp_path):
    drop(tmp_path, rows=[("20:02:21.025", "1000,45,1"), ("20:02:21.125", ",45,1")])
    by_name = {c.name: c for c in Profiler().run(tmp_path).channels}
    assert by_name["Motor RPM"].n == 1
    assert by_name["Motor RPM"].n_missing == 1


def test_report_and_draft_specs_render(tmp_path):
    result = Profiler().run(drop(tmp_path))
    text = report(result)
    assert "## Channels" in text
    assert "MC Temp" in text
    specs = draft_specs(result, "ev-2026")
    assert specs.count("\n|") == len(result.channels) + 2


@pytest.mark.parametrize("platform", ["ev-2026", "nope"])
def test_draft_specs_filters_by_platform(tmp_path, platform):
    result = Profiler().run(drop(tmp_path))
    expected = len(result.channels) if platform == "ev-2026" else 0
    assert draft_specs(result, platform).count("\n|") == expected + 2
