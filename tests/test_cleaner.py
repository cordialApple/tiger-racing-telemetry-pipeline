import pytest

from parser.cleaner import split_unit, strip_leading_comma


def test_leading_comma_stripped():
    assert strip_leading_comma(',"35.1","10.8"') == '"35.1","10.8"'


def test_only_one_comma_removed():
    assert strip_leading_comma(',,"x"') == ',"x"'


def test_line_without_leading_comma_unchanged():
    assert strip_leading_comma('"35.1","10.8"') == '"35.1","10.8"'


def test_header_line_unchanged():
    header = '"Time","Logger Temperature","External Voltage"'
    assert strip_leading_comma(header) == header


@pytest.mark.parametrize(
    ("column", "expected"),
    [
        ("Motor RPM [Rpm]", ("Motor RPM", "Rpm")),
        ("MC Temp [°C]", ("MC Temp", "°C")),
        ("CAN2 ERRORS [decimal]", ("CAN2 ERRORS", "decimal")),
        ("Flowrate", ("Flowrate", None)),
        ("  Pack_SOC  ", ("Pack_SOC", None)),
        ("Weird []", ("Weird", None)),
        ("Therm1 [C] raw", ("Therm1 [C] raw", None)),
        ("A [b] [c]", ("A [b]", "c")),
    ],
)
def test_split_unit(column, expected):
    assert split_unit(column) == expected
