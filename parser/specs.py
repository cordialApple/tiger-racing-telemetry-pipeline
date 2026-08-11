import re
from pathlib import Path

import config
from parser.models import SensorSpec

_PLATFORM = re.compile(r"^sensorspecs-(?P<platform>.+)\.md$")


class SpecLoader:
    def __init__(self, paths=None):
        self.paths = self._resolve(paths)

    def load(self) -> list[SensorSpec]:
        specs = []
        for path in self.paths:
            platform = self._platform(path)
            for cells in self._table_rows(path):
                name, description, data_type, unit, min_range, max_range = cells[:6]
                specs.append(SensorSpec(
                    name=name,
                    description=description,
                    unit=unit or None,
                    data_type=data_type,
                    min_range=self._to_float(min_range),
                    max_range=self._to_float(max_range),
                    platform=platform,
                ))
        return specs

    @staticmethod
    def _platform(path: Path) -> str | None:
        match = _PLATFORM.match(path.name)
        return match["platform"] if match else None

    @staticmethod
    def _resolve(paths) -> list[Path]:
        if paths is None:
            return sorted(
                p for p in config.DOCS_DIR.glob("sensorspecs*.md")
                if not p.name.endswith(".draft.md")
            )
        if isinstance(paths, (str, Path)):
            return [Path(paths)]
        return [Path(p) for p in paths]

    def _table_rows(self, path: Path) -> list[list[str]]:
        rows = []
        header_seen = False
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not header_seen:
                header_seen = True
                continue
            if all(set(c) <= {"-", ":"} for c in cells):
                continue
            rows.append(cells)
        return rows

    @staticmethod
    def _to_float(cell: str) -> float | None:
        return float(cell) if cell else None
