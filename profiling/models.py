import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ChannelProfile:
    name: str
    unit: str | None
    platforms: tuple[str, ...]
    n: int
    n_missing: int
    min: float | None
    max: float | None
    inferred_type: str
    is_constant: bool


@dataclass(frozen=True)
class FileProfile:
    rel_path: str
    platform: str
    session_id: str
    content_sha: str
    schema_id: str
    row_count: int
    channel_count: int
    first_ts: str
    last_ts: str
    sample_hz: int
    spacing_uniform: bool


@dataclass(frozen=True)
class DatasetProfile:
    root: str
    file_count: int
    unique_content_count: int
    files: tuple[FileProfile, ...]
    schemas: dict[str, tuple[str, ...]]
    channels: tuple[ChannelProfile, ...]
    duplicate_groups: tuple[tuple[str, ...], ...]
    unreadable: tuple[tuple[str, str], ...]

    def to_dict(self) -> dict:
        # round-trip through JSON so tuples become lists and goldens compare exactly
        return json.loads(json.dumps(asdict(self)))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n"
