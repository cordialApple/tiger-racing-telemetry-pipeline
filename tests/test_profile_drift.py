import json

import pytest

import config
from main import drop_dirs
from profiling.profiler import Profiler

DROPS = drop_dirs()


def golden_path(drop):
    return config.PROFILES_DIR / f"{drop.name}.json"


@pytest.mark.parametrize("drop", DROPS, ids=[d.name for d in DROPS])
def test_profile_matches_golden(drop):
    golden = json.loads(golden_path(drop).read_text(encoding="utf-8"))
    assert Profiler().run(drop).to_dict() == golden


@pytest.mark.parametrize("drop", DROPS, ids=[d.name for d in DROPS])
def test_every_file_is_readable(drop):
    golden = json.loads(golden_path(drop).read_text(encoding="utf-8"))
    assert golden["unreadable"] == []
    assert golden["file_count"] == len(golden["files"])


def test_every_drop_has_a_committed_profile():
    assert [d.name for d in DROPS] == ["2023", "2026"]
    assert all(golden_path(drop).exists() for drop in DROPS)
