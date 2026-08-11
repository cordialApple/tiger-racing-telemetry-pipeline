import pytest

import config
from parser.base import ParserRegistry, UnknownFormatError
from parser.registry import default_registry

AIM_SESSION = config.RAW_DIR / "2023" / "1.csv"
CANLOG_SESSION = (
    config.RAW_DIR / "2026" / "Drive Day 7_18" / "Tristan Drive" / "2026-7-18   20.02.21.csv"
)


class AlwaysMatches:
    platform = "always"

    def sniff(self, head):
        return True

    def parse(self, path):
        raise AssertionError("not reached")


@pytest.mark.parametrize(
    ("path", "platform"),
    [(AIM_SESSION, "ice-2023"), (CANLOG_SESSION, "ev-2026")],
)
def test_sniffs_the_right_parser(path, platform):
    assert default_registry().for_path(path).platform == platform


def test_parse_dispatches_by_format():
    assert default_registry().parse(CANLOG_SESSION).session.platform == "ev-2026"


def test_unrecognised_format_rejected(tmp_path):
    path = tmp_path / "mystery.csv"
    path.write_text("a,b,c\n1,2,3\n")
    with pytest.raises(UnknownFormatError, match="no parser recognises"):
        default_registry().for_path(path)


def test_ambiguous_format_rejected():
    registry = ParserRegistry([AlwaysMatches(), AlwaysMatches()])
    with pytest.raises(UnknownFormatError, match="matched"):
        registry.for_path(AIM_SESSION)


def test_head_read_is_bounded(tmp_path):
    path = tmp_path / "huge.csv"
    path.write_text("Time," + "x" * 100_000)
    assert default_registry().for_path(path).platform == "ev-2026"
