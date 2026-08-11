from collections import defaultdict

from checks.base import Finding


class UnreadableFile:
    id = "integrity.unreadable_file"
    severity = "error"
    title = "File the parser registry cannot read"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            for rel_path, reason in profile.unreadable:
                yield Finding(self.id, self.severity, drop, rel_path, reason)


class SessionIdCollision:
    id = "integrity.session_id_collision"
    severity = "error"
    title = "Distinct files that resolve to the same session_id"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            by_id = defaultdict(set)
            for file in profile.files:
                by_id[file.session_id].add(file.content_sha)
            for session_id, shas in sorted(by_id.items()):
                if len(shas) > 1:
                    yield Finding(
                        self.id, self.severity, drop, session_id,
                        f"{len(shas)} files with different content share this session_id",
                    )


class UnregisteredChannel:
    id = "integrity.unregistered_channel"
    severity = "error"
    title = "Channel with no sensor spec"

    def run(self, ctx):
        known = {spec.name for spec in ctx.specs}
        for drop, profile in ctx.profiles.items():
            for channel in profile.channels:
                if channel.name not in known:
                    yield Finding(
                        self.id, self.severity, drop, channel.name,
                        "no row in docs/sensorspecs*.md, so it drops out of v_session_channels",
                    )


class DuplicateContent:
    id = "integrity.duplicate_content"
    severity = "warning"
    title = "Byte-identical files filed in more than one place"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            for group in profile.duplicate_groups:
                others = ", ".join(group[1:])
                yield Finding(
                    self.id, self.severity, drop, group[0],
                    f"identical content also filed as {others}",
                )


class SchemaDrift:
    id = "integrity.schema_drift"
    severity = "info"
    title = "Channel set that varies within one drop"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            if len(profile.schemas) < 2:
                continue
            union = set().union(*(set(names) for names in profile.schemas.values()))
            for key, names in profile.schemas.items():
                absent = sorted(union - set(names))
                if absent:
                    yield Finding(
                        self.id, self.severity, drop, key,
                        f"missing {len(absent)} channels present elsewhere in the drop: "
                        f"{', '.join(absent)}",
                    )


CHECKS = [
    UnreadableFile(),
    SessionIdCollision(),
    UnregisteredChannel(),
    DuplicateContent(),
    SchemaDrift(),
]
