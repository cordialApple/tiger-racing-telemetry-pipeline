from profiling.models import DatasetProfile


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return lines


def _number(value) -> str:
    if value is None:
        return ""
    return f"{value:g}"


def report(profile: DatasetProfile) -> str:
    lines = [
        f"# Dataset profile: `{profile.root}`",
        "",
        f"- files: {profile.file_count} ({profile.unique_content_count} unique by content)",
        f"- schemas: {len(profile.schemas)}",
        f"- channels: {len(profile.channels)}",
        f"- rows: {sum(f.row_count for f in profile.files):,}",
        "",
        "## Schemas",
        "",
    ]
    for key, names in profile.schemas.items():
        members = [f.rel_path for f in profile.files if f.schema_id == key]
        lines += [f"### `{key}` ({len(names)} channels, {len(members)} files)", ""]
        lines += [f"- `{path}`" for path in members]
        lines.append("")

    if len(profile.schemas) > 1:
        lines += ["### Drift", ""]
        keys = list(profile.schemas)
        base = set(profile.schemas[keys[0]])
        for key in keys[1:]:
            other = set(profile.schemas[key])
            lines.append(f"- `{keys[0]}` only: {sorted(base - other) or 'none'}")
            lines.append(f"- `{key}` only: {sorted(other - base) or 'none'}")
        lines.append("")

    if profile.duplicate_groups:
        lines += ["## Duplicate content", ""]
        for group in profile.duplicate_groups:
            lines.append("- " + ", ".join(f"`{path}`" for path in group))
        lines.append("")

    if profile.unreadable:
        lines += ["## Unreadable", ""]
        lines += [f"- `{path}`: {reason}" for path, reason in profile.unreadable]
        lines.append("")

    dead = [c for c in profile.channels if c.is_constant]
    if dead:
        lines += [
            "## Constant channels",
            "",
            f"{len(dead)} of {len(profile.channels)} never change across the whole dataset.",
            "",
        ]
        lines += [f"- `{c.name}` = {_number(c.min)}" for c in dead]
        lines.append("")

    lines += ["## Files", ""]
    lines += _table(
        ["file", "platform", "session_id", "rows", "channels", "Hz", "uniform", "sha"],
        [
            [
                f"`{f.rel_path}`", f.platform, f"`{f.session_id}`", f"{f.row_count:,}",
                str(f.channel_count), str(f.sample_hz), "yes" if f.spacing_uniform else "NO",
                f"`{f.content_sha}`",
            ]
            for f in profile.files
        ],
    )
    lines += ["", "## Channels", ""]
    lines += _table(
        ["channel", "unit", "platforms", "n", "missing", "min", "max", "type", "constant"],
        [
            [
                f"`{c.name}`", c.unit or "", ", ".join(c.platforms), f"{c.n:,}",
                f"{c.n_missing:,}", _number(c.min), _number(c.max), c.inferred_type,
                "yes" if c.is_constant else "",
            ]
            for c in profile.channels
        ],
    )
    return "\n".join(lines) + "\n"


def draft_specs(profile: DatasetProfile, platform: str) -> str:
    channels = [c for c in profile.channels if platform in c.platforms]
    lines = [
        f"# Draft sensor specifications: {platform}",
        "",
        f"Generated from `{profile.root}`. Ranges are the observed extremes, not",
        "engineering limits: widen them by hand and fill in descriptions before",
        f"promoting this file to `sensorspecs-{platform}.md`.",
        "",
    ]
    lines += _table(
        ["sensor_name", "description", "data_type", "unit", "min_range", "max_range"],
        [
            [c.name, "", c.inferred_type, c.unit or "", _number(c.min), _number(c.max)]
            for c in channels
        ],
    )
    return "\n".join(lines) + "\n"
