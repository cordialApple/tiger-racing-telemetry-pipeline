import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileResult:
    source_file: str
    status: str
    readings: int = 0
    out_of_range: int = 0
    error: str | None = None


class Pipeline:
    def __init__(self, db, source_dir, processed_dir, parser, validator, repo, specs):
        self.db = db
        self.source_dir = Path(source_dir)
        self.processed_dir = Path(processed_dir)
        self.parser = parser
        self.validator = validator
        self.repo = repo
        self.specs = specs

    def run(self) -> list[FileResult]:
        with self.db.connection() as conn:
            self.repo.upsert_sensors(conn, self.specs)
        return [self.process(p) for p in sorted(self.source_dir.rglob("*.csv"))]

    def process(self, path: Path) -> FileResult:
        source_path = path.relative_to(self.source_dir).as_posix()
        try:
            return self._load(path, source_path)
        except Exception as e:
            return FileResult(source_path, "error", error=str(e))

    def _load(self, path: Path, source_path: str) -> FileResult:
        parsed = self.parser.parse(path)
        with self.db.connection() as conn:
            if self.repo.is_loaded(conn, parsed.packet_id):
                # same bytes filed under another path still deserve attribution
                self.repo.record_source(conn, parsed.packet_id, source_path)
                return FileResult(source_path, "skipped")
            report = self.validator.validate(parsed.readings)
            self.repo.insert_session(conn, parsed.session)
            written = self.repo.copy_readings(conn, parsed.session.session_id, parsed.readings)
            self.repo.log_ingestion(
                conn, parsed.packet_id, parsed.session.session_id,
                source_path, parsed.row_count, written,
            )
            self.repo.record_source(conn, parsed.packet_id, source_path)
        self._archive(path)
        return FileResult(source_path, "loaded", written, report.out_of_range)

    def _archive(self, path: Path):
        target = self.processed_dir / path.relative_to(self.source_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(target))
