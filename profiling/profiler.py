import hashlib
from collections import defaultdict
from itertools import pairwise
from pathlib import Path

import config
from parser.registry import default_registry
from profiling.models import ChannelProfile, DatasetProfile, FileProfile

_DISTINCT_CAP = 3


class _Channel:
    def __init__(self, unit):
        self.unit = unit
        self.platforms = set()
        self.n = 0
        self.expected = 0
        self.min = None
        self.max = None
        self.fractional = 0
        self.distinct = set()

    def add(self, value):
        self.n += 1
        self.min = value if self.min is None else min(self.min, value)
        self.max = value if self.max is None else max(self.max, value)
        if value != int(value):
            self.fractional += 1
        if len(self.distinct) <= _DISTINCT_CAP:
            self.distinct.add(value)

    @property
    def inferred_type(self) -> str:
        if self.distinct <= {0.0, 1.0} and len(self.distinct) == 2:
            return "boolean"
        return "float" if self.fractional else "integer"

    def freeze(self, name) -> ChannelProfile:
        return ChannelProfile(
            name=name,
            unit=self.unit,
            platforms=tuple(sorted(self.platforms)),
            n=self.n,
            n_missing=self.expected - self.n,
            min=self.min,
            max=self.max,
            inferred_type=self.inferred_type,
            is_constant=self.min == self.max,
        )


def schema_id(names) -> str:
    joined = "\n".join(names).encode("utf-8")
    return hashlib.sha256(joined).hexdigest()[:12]


class Profiler:
    def __init__(self, registry=None):
        self._registry = registry or default_registry()

    def run(self, root) -> DatasetProfile:
        root = Path(root)
        files, unreadable = [], []
        channels: dict[str, _Channel] = {}
        schemas: dict[str, tuple[str, ...]] = {}
        by_content: dict[str, list[str]] = defaultdict(list)

        for path in sorted(root.rglob("*.csv")):
            rel = path.relative_to(root).as_posix()
            try:
                parsed = self._registry.parse(path)
            except Exception as error:
                unreadable.append((rel, f"{type(error).__name__}: {error}"))
                continue
            files.append(self._file_profile(rel, parsed, schemas))
            by_content[parsed.packet_id].append(rel)
            self._accumulate(parsed, channels)

        return DatasetProfile(
            root=self._label(root),
            file_count=len(files) + len(unreadable),
            unique_content_count=len(by_content),
            files=tuple(files),
            schemas=dict(sorted(schemas.items())),
            channels=tuple(
                channels[name].freeze(name) for name in sorted(channels)
            ),
            duplicate_groups=tuple(
                tuple(group) for group in by_content.values() if len(group) > 1
            ),
            unreadable=tuple(unreadable),
        )

    @staticmethod
    def _label(root: Path) -> str:
        # goldens are committed, so the recorded root must not carry a machine-specific prefix
        try:
            return root.resolve().relative_to(config.ROOT).as_posix()
        except ValueError:
            return root.name

    @staticmethod
    def _file_profile(rel, parsed, schemas) -> FileProfile:
        names = tuple(parsed.units)
        key = schema_id(names)
        schemas.setdefault(key, names)
        stamps = sorted({ts for ts, _name, _value in parsed.readings})
        deltas = {round((b - a).total_seconds(), 6) for a, b in pairwise(stamps)}
        return FileProfile(
            rel_path=rel,
            platform=parsed.session.platform,
            session_id=parsed.session.session_id,
            content_sha=parsed.packet_id[:12],
            schema_id=key,
            row_count=parsed.row_count,
            channel_count=len(names),
            first_ts=stamps[0].isoformat(),
            last_ts=stamps[-1].isoformat(),
            sample_hz=parsed.session.sample_rate_hz,
            spacing_uniform=len(deltas) == 1,
        )

    @staticmethod
    def _accumulate(parsed, channels):
        platform = parsed.session.platform
        for name, unit in parsed.units.items():
            channel = channels.setdefault(name, _Channel(unit))
            channel.platforms.add(platform)
            channel.expected += parsed.row_count
        for _ts, name, value in parsed.readings:
            channels[name].add(value)
