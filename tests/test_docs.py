import json
import re

import pytest

import config

PAGES_DIR = config.ROOT / "powerbi" / "tiger-telemetry.Report" / "definition" / "pages"
_IMAGE = re.compile(r"!\[[^\]]*\]\((?P<target>[^)\s]+)\)")


def markdown_files():
    return sorted(
        path
        for path in config.ROOT.rglob("*.md")
        if ".git" not in path.parts and "node_modules" not in path.parts
    )


def local_images():
    for path in markdown_files():
        for match in _IMAGE.finditer(path.read_text(encoding="utf-8")):
            target = match["target"]
            if not target.startswith(("http://", "https://")):
                yield path, target


def page_names() -> set[str]:
    return {
        json.loads(path.read_text(encoding="utf-8"))["displayName"]
        for path in PAGES_DIR.glob("*/page.json")
    }


def test_every_markdown_image_resolves_on_disk():
    missing = [
        f"{path.relative_to(config.ROOT).as_posix()} -> {target}"
        for path, target in local_images()
        if not (path.parent / target).is_file()
    ]
    assert not missing, f"broken image links: {missing}"


def test_readme_hero_image_exists():
    # the shields.io badge block is also markdown images, so the hero is the first local one
    root_readme = config.ROOT / "README.md"
    heroes = [target for path, target in local_images() if path == root_readme]
    assert heroes, "root README has no local hero image"
    assert (config.ROOT / heroes[0]).is_file()


@pytest.mark.parametrize(
    "slug",
    ["season-overview", "session-deep-dive", "engine-health", "findings",
     "ev-drive-day", "ev-thermal", "ev-findings"],
)
def test_screenshot_is_referenced_by_the_reports_readme(slug):
    text = (config.ROOT / "reports" / "README.md").read_text(encoding="utf-8")
    assert f"({slug}.png)" in text


def test_report_pages_cover_both_platforms():
    names = page_names()
    assert len(names) == 7
    assert len([n for n in names if n.startswith("EV ")]) == 3


def test_every_report_page_has_a_screenshot():
    slugs = {p.stem for p in (config.ROOT / "reports").glob("*.png")}
    expected = {name.lower().replace(" ", "-") for name in page_names()}
    assert expected <= slugs, f"pages without a screenshot: {sorted(expected - slugs)}"
