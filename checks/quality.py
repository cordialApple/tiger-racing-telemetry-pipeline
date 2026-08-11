from checks.base import Finding


class NonUniformSampling:
    id = "quality.non_uniform_sampling"
    severity = "warning"
    title = "File whose samples are not evenly spaced"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            for file in profile.files:
                if not file.spacing_uniform:
                    yield Finding(
                        self.id, self.severity, drop, file.rel_path,
                        f"declared {file.sample_hz} Hz but sample spacing varies",
                    )


class OutOfSpecRange:
    id = "quality.out_of_spec_range"
    severity = "warning"
    title = "Channel that leaves its advisory range"

    def run(self, ctx):
        specs = {spec.name: spec for spec in ctx.specs}
        for drop, profile in ctx.profiles.items():
            for channel in profile.channels:
                spec = specs.get(channel.name)
                if spec is None or spec.min_range is None or spec.max_range is None:
                    continue
                if channel.min is None or channel.max is None:
                    continue
                if channel.min >= spec.min_range and channel.max <= spec.max_range:
                    continue
                yield Finding(
                    self.id, self.severity, drop, channel.name,
                    f"observed {channel.min:g} to {channel.max:g}, "
                    f"spec is {spec.min_range:g} to {spec.max_range:g}",
                )


class MissingSamples:
    id = "quality.missing_samples"
    severity = "warning"
    title = "Channel with blank cells in the source files"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            for channel in profile.channels:
                if channel.n_missing:
                    total = channel.n + channel.n_missing
                    share = channel.n_missing / total
                    yield Finding(
                        self.id, self.severity, drop, channel.name,
                        f"{channel.n_missing:,} of {total:,} samples blank ({share:.1%})",
                    )


class ConstantChannel:
    id = "quality.constant_channel"
    severity = "info"
    title = "Channel that never changes"

    def run(self, ctx):
        for drop, profile in ctx.profiles.items():
            for channel in profile.channels:
                if channel.is_constant and channel.n:
                    yield Finding(
                        self.id, self.severity, drop, channel.name,
                        f"constant at {channel.min:g} across {channel.n:,} samples",
                    )


CHECKS = [NonUniformSampling(), OutOfSpecRange(), MissingSamples(), ConstantChannel()]
