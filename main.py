import argparse
from pathlib import Path

import uvicorn

import config
from db.connection import Database
from db.repository import ReadingRepository
from db.schema_manager import SchemaManager
from loader.pipeline import Pipeline
from parser.registry import default_registry
from parser.specs import SpecLoader
from parser.validator import SensorValidator
from profiling.profiler import Profiler
from profiling.render import draft_specs, report


def build_pipeline(db):
    specs = SpecLoader().load()
    return Pipeline(
        db, config.RAW_DIR, config.PROCESSED_DIR,
        default_registry(), SensorValidator(specs),
        ReadingRepository(), specs,
    )


def ingest(db):
    sm = SchemaManager(db)
    sm.apply()
    results = build_pipeline(db).run()
    if any(r.status == "loaded" for r in results):
        sm.refresh_views()
    for r in results:
        detail = r.error if r.status == "error" else f"{r.readings} readings, {r.out_of_range} out of range"
        print(f"{r.source_file}: {r.status} ({detail})")


def drop_dirs(path=None) -> list:
    if path:
        return [Path(path)]
    return sorted(d for d in config.RAW_DIR.iterdir() if d.is_dir())


def profile(path=None):
    config.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    for drop in drop_dirs(path):
        result = Profiler().run(drop)
        (config.PROFILES_DIR / f"{drop.name}.json").write_text(
            result.to_json(), encoding="utf-8"
        )
        (config.REPORTS_DIR / f"profile-{drop.name}.md").write_text(
            report(result), encoding="utf-8"
        )
        for platform in sorted({f.platform for f in result.files}):
            (config.DOCS_DIR / f"sensorspecs-{platform}.draft.md").write_text(
                draft_specs(result, platform), encoding="utf-8"
            )
        print(
            f"{drop.name}: {result.file_count} files, {len(result.schemas)} schemas, "
            f"{len(result.channels)} channels, {len(result.unreadable)} unreadable"
        )


def serve():
    uvicorn.run("api.app:app", host=config.API_HOST, port=config.API_PORT)


def main():
    parser = argparse.ArgumentParser(description="FSAE telemetry pipeline")
    parser.add_argument("command", nargs="?", default="all",
                        choices=["profile", "ingest", "serve", "all"])
    parser.add_argument("path", nargs="?", help="drop directory (default: every one under data/raw)")
    args = parser.parse_args()
    if args.command == "profile":
        profile(args.path)
        return
    if args.command in ("ingest", "all"):
        ingest(Database())
    if args.command in ("serve", "all"):
        serve()


if __name__ == "__main__":
    main()
