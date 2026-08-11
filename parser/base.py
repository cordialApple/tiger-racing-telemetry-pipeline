from pathlib import Path
from typing import Protocol

from parser.models import ParsedSession

_HEAD_BYTES = 4096


class UnknownFormatError(Exception):
    pass


class TelemetryParser(Protocol):
    platform: str

    def sniff(self, head: str) -> bool: ...

    def parse(self, path: Path) -> ParsedSession: ...


def read_head(path: Path) -> str:
    return Path(path).read_bytes()[:_HEAD_BYTES].decode("utf-8", errors="replace")


class ParserRegistry:
    def __init__(self, parsers: list[TelemetryParser]):
        self._parsers = list(parsers)

    def for_path(self, path) -> TelemetryParser:
        path = Path(path)
        matches = [p for p in self._parsers if p.sniff(read_head(path))]
        if not matches:
            raise UnknownFormatError(f"no parser recognises {path.name}")
        if len(matches) > 1:
            raise UnknownFormatError(
                f"{path.name} matched {sorted(p.platform for p in matches)}"
            )
        return matches[0]

    def parse(self, path) -> ParsedSession:
        return self.for_path(path).parse(path)
