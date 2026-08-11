import json
import statistics
from datetime import timedelta
from pathlib import Path

import pytest

import config
from parser.canlog_parser import CanLogParser

GOLDEN = json.loads(
    (Path(__file__).parent / "golden" / "canlog_20_02_21.json").read_text(encoding="utf-8")
)
DROP = config.RAW_DIR / "2026" / "Drive Day 7_18"
SESSION = DROP / "Tristan Drive" / "2026-7-18   20.02.21.csv"


@pytest.fixture(scope="module")
def parsed():
    return CanLogParser().parse(SESSION)


def test_session_matches_reference(parsed):
    s = parsed.session
    assert s.source_file == GOLDEN["source_file"]
    assert s.session_id == GOLDEN["session_id"]
    assert s.platform == GOLDEN["platform"]
    assert s.racer == GOLDEN["racer"]
    assert s.event == GOLDEN["event"]
    assert s.started_at.isoformat() == GOLDEN["started_at"]
    assert s.sample_rate_hz == GOLDEN["sample_rate_hz"]
    assert s.duration_s == GOLDEN["duration_s"]


def test_readings_match_reference(parsed):
    assert parsed.row_count == GOLDEN["row_count"]
    assert len(parsed.readings) == GOLDEN["reading_count"]
    assert len(parsed.units) == GOLDEN["sensor_count"]
    rpm = [v for _ts, name, v in parsed.readings if name == "Motor RPM"]
    assert len(rpm) == GOLDEN["rpm_n"]
    assert min(rpm) == GOLDEN["rpm_min"]
    assert max(rpm) == GOLDEN["rpm_max"]
    assert round(statistics.fmean(rpm), 2) == GOLDEN["rpm_avg"]


def test_units_split_from_column_names(parsed):
    assert "Time" not in parsed.units
    assert parsed.units["MC Temp"] == GOLDEN["unit_mc_temp"]
    assert parsed.units["Flowrate"] is GOLDEN["unit_flowrate"]
    assert all("[" not in name for name in parsed.units)


def test_timestamps_come_from_the_file_not_the_sample_rate(parsed):
    stamps = [ts for ts, name, _v in parsed.readings if name == "Motor RPM"]
    assert stamps[1] - stamps[0] == timedelta(milliseconds=GOLDEN["rpm_spacing_ms"])
    assert stamps[0].microsecond == 25000


def test_driver_and_event_come_from_the_folder_path(parsed):
    assert parsed.session.racer == "Tristan"
    assert parsed.session.event == "Drive Day 7_18"


def test_file_outside_a_driver_folder_has_no_racer():
    session = CanLogParser().parse(DROP / "2026-7-18   17.55.26.csv").session
    assert session.racer is None
    assert session.event == "Drive Day 7_18"
    assert session.session_id == "2026-07-18_175526"


def test_note_in_filename_becomes_the_comment():
    path = DROP / "Yianni Drive" / "2026-7-18   20.14.12 (Still Pump Run).csv"
    assert CanLogParser().parse(path).session.comment == "Still Pump Run"


def test_note_without_leading_space_still_parses():
    path = DROP / "Ryan Drive" / "2026-7-18   21.56.34(Weird FlowRate).csv"
    assert CanLogParser().parse(path).session.comment == "Weird FlowRate"


def test_unrecognised_filename_rejected(tmp_path):
    path = tmp_path / "no-timestamp-here.csv"
    path.write_text("Time,A\n00:00:00.000,1\n00:00:00.100,2\n")
    with pytest.raises(ValueError, match="unrecognised filename"):
        CanLogParser().parse(path)


def test_single_row_file_rejected(tmp_path):
    path = tmp_path / "2026-7-18   20.02.21.csv"
    path.write_text("Time,A\n20:02:21.025,1\n")
    with pytest.raises(ValueError, match="fewer than two data rows"):
        CanLogParser().parse(path)


def test_midnight_rollover_advances_the_date(tmp_path):
    path = tmp_path / "2026-7-18   23.59.59.csv"
    path.write_text("Time,A\n23:59:59.900,1\n00:00:00.000,2\n00:00:00.100,3\n")
    stamps = [ts for ts, _name, _v in CanLogParser().parse(path).readings]
    assert stamps[0].date().isoformat() == "2026-07-18"
    assert stamps[1].date().isoformat() == "2026-07-19"
    assert stamps[2].date().isoformat() == "2026-07-19"
