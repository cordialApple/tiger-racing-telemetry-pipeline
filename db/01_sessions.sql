CREATE TABLE IF NOT EXISTS sessions (
    session_id     TEXT PRIMARY KEY,
    source_file    TEXT NOT NULL,
    platform       TEXT,
    event          TEXT,
    vehicle        TEXT,
    racer          TEXT,
    championship   TEXT,
    session_name   TEXT,
    comment        TEXT,
    started_at     TIMESTAMPTZ NOT NULL,
    sample_rate_hz INTEGER NOT NULL,
    duration_s     INTEGER,
    segment_times  TEXT,
    created_at     TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE sessions ADD COLUMN IF NOT EXISTS platform TEXT;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS event TEXT;

ALTER TABLE sessions DROP CONSTRAINT IF EXISTS sessions_source_file_key;

CREATE INDEX IF NOT EXISTS idx_sessions_platform ON sessions (platform, started_at);
