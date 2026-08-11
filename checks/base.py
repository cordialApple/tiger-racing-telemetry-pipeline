import importlib
import pkgutil
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

SEVERITIES = ("error", "warning", "info")


@dataclass(frozen=True)
class Finding:
    check_id: str
    severity: str
    scope: str
    subject: str
    detail: str


@dataclass(frozen=True)
class CheckContext:
    profiles: dict
    specs: list


class Check(Protocol):
    id: str
    severity: str
    title: str

    def run(self, ctx: CheckContext) -> Iterable[Finding]: ...


def all_checks() -> list[Check]:
    import checks

    discovered = []
    for module in pkgutil.iter_modules(checks.__path__):
        if module.name in ("base", "render"):
            continue
        discovered += importlib.import_module(f"checks.{module.name}").CHECKS
    return sorted(discovered, key=lambda check: check.id)


def run_checks(ctx: CheckContext, selected=None) -> list[Finding]:
    findings = []
    for check in all_checks() if selected is None else selected:
        findings += list(check.run(ctx))
    return sorted(
        findings,
        key=lambda f: (SEVERITIES.index(f.severity), f.check_id, f.scope, f.subject),
    )
