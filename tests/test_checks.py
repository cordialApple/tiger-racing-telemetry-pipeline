import pytest

from checks.base import CheckContext, all_checks, run_checks
from checks.integrity import (
    DuplicateContent,
    SchemaDrift,
    SessionIdCollision,
    UnreadableFile,
    UnregisteredChannel,
)
from checks.quality import (
    ConstantChannel,
    MissingSamples,
    NonUniformSampling,
    OutOfSpecRange,
)
from checks.render import report
from parser.models import SensorSpec
from profiling.models import ChannelProfile, DatasetProfile, FileProfile


def channel(name="Motor RPM", n=10, n_missing=0, low=0.0, high=100.0, constant=False):
    return ChannelProfile(
        name=name, unit=None, platforms=("ev-2026",), n=n, n_missing=n_missing,
        min=low, max=high, inferred_type="float", is_constant=constant,
    )


def file_profile(rel_path="a.csv", session_id="s1", sha="aaa", schema="sch", uniform=True):
    return FileProfile(
        rel_path=rel_path, platform="ev-2026", session_id=session_id, content_sha=sha,
        schema_id=schema, row_count=10, channel_count=1, first_ts="2026-07-18T20:00:00",
        last_ts="2026-07-18T20:00:01", sample_hz=10, spacing_uniform=uniform,
    )


def profile(files=(), channels=(), schemas=None, duplicates=(), unreadable=()):
    return DatasetProfile(
        root="data/raw/2026", file_count=len(files) + len(unreadable),
        unique_content_count=len(files), files=tuple(files), channels=tuple(channels),
        schemas=schemas or {"sch": ("Motor RPM",)},
        duplicate_groups=tuple(duplicates), unreadable=tuple(unreadable),
    )


def context(prof, specs=()):
    return CheckContext(profiles={"2026": prof}, specs=list(specs))


SPEC = SensorSpec("Motor RPM", "", None, "float", 0, 100)


def test_unreadable_file_flagged():
    ctx = context(profile(unreadable=[("broken.csv", "ValueError: nope")]))
    findings = UnreadableFile().run(ctx)
    assert [f.subject for f in findings] == ["broken.csv"]


def test_session_id_collision_needs_differing_content():
    same = [file_profile("a.csv", "s1", "aaa"), file_profile("b.csv", "s1", "aaa")]
    differ = [file_profile("a.csv", "s1", "aaa"), file_profile("b.csv", "s1", "bbb")]
    assert list(SessionIdCollision().run(context(profile(files=same)))) == []
    assert len(list(SessionIdCollision().run(context(profile(files=differ))))) == 1


def test_unregistered_channel_flagged_only_without_a_spec():
    ctx = context(profile(channels=[channel()]))
    assert len(list(UnregisteredChannel().run(ctx))) == 1
    assert list(UnregisteredChannel().run(context(profile(channels=[channel()]), [SPEC]))) == []


def test_duplicate_content_names_the_other_files():
    ctx = context(profile(duplicates=[("a.csv", "b.csv")]))
    finding = next(iter(DuplicateContent().run(ctx)))
    assert finding.subject == "a.csv"
    assert "b.csv" in finding.detail


def test_schema_drift_lists_the_absent_channels():
    schemas = {"wide": ("A", "B"), "narrow": ("A",)}
    findings = list(SchemaDrift().run(context(profile(schemas=schemas))))
    assert [f.subject for f in findings] == ["narrow"]
    assert "B" in findings[0].detail


def test_schema_drift_silent_on_a_single_schema():
    assert list(SchemaDrift().run(context(profile()))) == []


def test_non_uniform_sampling_flagged():
    ctx = context(profile(files=[file_profile(uniform=False)]))
    assert len(list(NonUniformSampling().run(ctx))) == 1


@pytest.mark.parametrize(
    ("low", "high", "expected"),
    [(0.0, 100.0, 0), (-1.0, 100.0, 1), (0.0, 4132.0, 1)],
)
def test_out_of_spec_range(low, high, expected):
    ctx = context(profile(channels=[channel(low=low, high=high)]), [SPEC])
    assert len(list(OutOfSpecRange().run(ctx))) == expected


def test_out_of_spec_range_skips_channels_without_a_range():
    open_spec = SensorSpec("Motor RPM", "", None, "float", None, None)
    ctx = context(profile(channels=[channel(low=-999.0, high=999.0)]), [open_spec])
    assert list(OutOfSpecRange().run(ctx)) == []


def test_missing_samples_reports_share():
    ctx = context(profile(channels=[channel(n=3, n_missing=1)]))
    assert "25.0%" in next(iter(MissingSamples().run(ctx))).detail


def test_constant_channel_flagged():
    ctx = context(profile(channels=[channel(low=5.0, high=5.0, constant=True)]))
    assert len(list(ConstantChannel().run(ctx))) == 1


def test_constant_channel_ignores_empty_channels():
    ctx = context(profile(channels=[channel(n=0, low=None, high=None, constant=True)]))
    assert list(ConstantChannel().run(ctx)) == []


def test_every_check_is_discovered():
    ids = {check.id for check in all_checks()}
    assert ids == {
        "integrity.duplicate_content",
        "integrity.schema_drift",
        "integrity.session_id_collision",
        "integrity.unreadable_file",
        "integrity.unregistered_channel",
        "quality.constant_channel",
        "quality.missing_samples",
        "quality.non_uniform_sampling",
        "quality.out_of_spec_range",
    }


def test_findings_sort_errors_first():
    ctx = context(
        profile(
            channels=[channel(low=5.0, high=5.0, constant=True)],
            duplicates=[("a.csv", "b.csv")],
        )
    )
    severities = [f.severity for f in run_checks(ctx)]
    assert severities == sorted(severities, key=["error", "warning", "info"].index)


def test_report_renders_each_severity_section():
    ctx = context(profile(channels=[channel(low=5.0, high=5.0, constant=True)]))
    text = report(run_checks(ctx))
    assert "## error" in text
    assert "## info" in text
    assert "`integrity.unregistered_channel`" in text
