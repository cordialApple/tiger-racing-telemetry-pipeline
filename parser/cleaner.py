import re

_UNIT_SUFFIX = re.compile(r"^(?P<name>.+?)\s*\[(?P<unit>[^\]]*)\]$")


def strip_leading_comma(line: str) -> str:
    return line[1:] if line.startswith(",") else line


def split_unit(column: str) -> tuple[str, str | None]:
    match = _UNIT_SUFFIX.match(column.strip())
    if match is None:
        return column.strip(), None
    return match["name"], match["unit"].strip() or None
