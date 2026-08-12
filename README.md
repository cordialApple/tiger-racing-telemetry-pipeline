# Tiger Racing Telemetry Pipeline

> Offline pipeline that turns two seasons of Formula SAE logger exports, a 2023 AiM combustion car and a 2026 CAN electric car, into a queryable TimescaleDB and serves them to a Power BI performance dashboard.

[![tests](https://github.com/cordialApple/tiger-racing-telemetry-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/cordialApple/tiger-racing-telemetry-pipeline/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org)
[![TimescaleDB](https://img.shields.io/badge/TimescaleDB-PG16-fdb515.svg)](https://www.timescale.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-dashboard-f2c811.svg)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![EV Drive Day](reports/ev-drive-day.png)

## What it is

Telemetry from two Formula SAE cars, one directory per season under `data/raw/`:

- **2023**: combustion car, AiM logger, 18 sessions from one evening at UTA
  Autocross on Oct 7 2023.
- **2026**: electric car, CAN logger, 26 files from the Jul 18 drive day, nested
  by event and driver. Disjoint channel set from 2023; no channel names overlap.

The pipeline ingests the raw CSV exports, lands them in TimescaleDB, and serves
SQL views to Power BI. The dashboard above is the payoff.

## Highlights

- **Idempotent ingest.** Each file is keyed by content hash, so re-runs skip work already done.
- **TimescaleDB hypertable.** Long-format `(ts, session_id, sensor_name, value)` with a 1 Hz continuous aggregate.
- **Typed REST API.** FastAPI endpoints with fixed, Pydantic-validated column sets for Power BI.
- **Per-file error isolation.** One bad session fails alone; the rest of the batch loads.
- **Findings that matter.** 2023 surfaced oil starvation under cornering, cooling limits, dead channels, and low throttle usage. 2026 surfaced coolant flow at ~40% of the inverter minimum, peak temperature driven by heat soak rather than driving, inverter overcurrent trips, and a BMS channel labelled `Pack_SOC` that is really a pack temperature. See [`reports/`](reports/README.md).

## Architecture

```
data/raw/<season>/**/*.csv
    │
    ▼
profile → check                    profiling/  checks/
    │
    ▼
sniff → parse → validate           parser/
    │
    ▼
load → TimescaleDB hypertable      loader/  db/
    │
    ▼
SQL views → FastAPI REST API       db/views/  api/
    │
    ▼
Power BI dashboard                 powerbi/  reports/
```

## Quick Start

Prerequisites: Docker and Python 3.11+.

```
docker compose up -d              # TimescaleDB on localhost:5432 (waits for healthcheck)
pip install -r requirements.txt
python main.py all                # ingest every file in data/raw, then serve the API
```

The API comes up on `http://localhost:8000`, with live OpenAPI docs at
`http://localhost:8000/docs`.

Defaults live in `config.py` and are overridable via `PGHOST`, `PGPORT`,
`PGUSER`, `PGPASSWORD`, `PGDATABASE`, `API_HOST`, and `API_PORT`.

## Project Structure

```
config.py         centralized paths, API host/port, and DB connection defaults
profiling/        DB-free dataset profiler, markdown report, draft spec generator
checks/           discoverable data checks that regenerate reports/findings.*
profiles/         committed golden profiles, one per drop, diffed by CI
data/raw/2023/    AiM CSV exports from the 2023 combustion car (one file per session)
data/raw/2026/    CAN logger exports from the 2026 EV, nested <event>/<driver>/
data/processed/   files move here after a successful load, mirroring the raw layout
parser/           CSV cleaner, AiM parser, sensor spec loader, advisory validator
db/               psycopg connection, schema (.sql per table), repository, views/
loader/           ingestion pipeline (per-file error isolation)
api/              FastAPI REST API consumed by Power BI (serving layer over the views)
powerbi/          PBIP project (TMDL semantic model + PBIR report), the dashboard source
reports/          rendered Power BI dashboards (screenshots) and findings writeup
docs/             sensorspecs-<platform>.md (advisory sensor ranges, one per car)
tests/            pytest suite; db-marked tests skip without a reachable TimescaleDB
main.py           entrypoint (profile / check / ingest / serve / all)
```

## Usage

```
python main.py profile   # profile every drop under data/raw, refresh profiles/ and reports/
python main.py check     # run checks/, rewrite reports/findings.*, exit 1 on any error
python main.py ingest    # apply schema, then load every file in data/raw
python main.py serve     # start the REST API
python main.py all       # ingest then serve (default)
```

Both `profile` and `check` are database-free. Profile a new drop before ingesting
it: the profile records the channel set, sample spacing, duplicate groups, and
per-channel extremes, and CI fails when a fresh run stops matching the committed
copy in `profiles/`.

Loading is idempotent: each file is keyed by a content hash in `ingestion_log`,
so re-running skips files already loaded.

A file that fails to parse or load is reported and left in `data/raw` for retry,
and the rest of the batch continues.

`data/raw` is a committed corpus, so ingest leaves it alone; the content hash
already prevents double-loading. Set `ARCHIVE_PROCESSED=1` to restore the old
behaviour of moving loaded files into `data/processed/`.

## Data Model

- `sessions`: one row per logger file, carrying `platform` and `event`.
- `sensors`: registry seeded from every `docs/sensorspecs-<platform>.md`.
- `ingestion_source`: every path a given content hash was filed under, so a file
  copied into two drivers' folders keeps both attributions.
- `sensor_readings`: long-format hypertable `(ts, session_id, sensor_name, value)`.
  Timestamps are synthesized from the session start at the file's sample rate.
  There are no FK constraints, since the pipeline enforces integrity and this keeps COPY fast.
- `ingestion_log`: content-hash packet tracking for idempotency.

## Views

- `v_session_catalog`: session list with reading counts.
- `v_sensor_readings`: raw long-format readings with unit, elapsed seconds, and
  `value` mirrored as `avg_value`/`min_value`/`max_value` so the raw feed shares
  one column set with the 1 Hz feed.
- `v_session_sensor_stats`: per session/sensor count, avg, min, max.
- `v_sensor_1hz`: 1 Hz TimescaleDB continuous aggregate (`bucket`, `avg`/`min`/`max`).
- `v_sensor_1hz_enriched`: `v_sensor_1hz` joined to session and sensor metadata,
  exposing `ts`, `t_seconds`, `unit`, and the same `value`/`avg`/`min`/`max`
  columns as `v_sensor_readings`.
- `v_session_channels`: channel dimension per session, combining sensor spec
  metadata with `n`/`avg`/`min`/`max` from the stats view and a `has_signal` flag
  that is `false` when both min and max are 0.

## API (Power BI connection)

Point Power BI's Web/JSON connector at `http://localhost:8000`. Each endpoint
returns one fixed column set, validated by a Pydantic `response_model`.

- `GET /sessions`: Sessions dimension (from `v_session_catalog`), including
  `platform` (`ice-2023` / `ev-2026`), `event`, and the free-text `comment` the
  team wrote into the filename.
- `GET /sessions/{session_id}/sensors`: Channel dimension (from `v_session_channels`).
- `GET /readings?session_id=&sensor=&start=&end=&downsample=1hz|raw&limit=&offset=`:
  paginated envelope `{session_id, sensor, downsample, limit, offset, total,
  count, rows}`. Omit `sensor` for the full long-format fact feed, or supply it
  to drill into one channel. `raw` and `1hz` rows share the same eight columns,
  and `total` lets Power BI page deterministically.
- `GET /stats?session_id=&sensor=`: pre-aggregated fact (from `v_session_sensor_stats`).

The star-schema mapping in Power BI:

- `Sessions[session_id]` one-to-many `Readings[session_id]`
- `Channels[session_id, sensor_name]` one-to-many `Readings[sensor_name]`
- `Stats` relates by both keys as a parallel summary fact
- `Sessions[platform]` slices the whole model by car and season

`Channels`, `Readings`, and `Stats` each load through one Power Query partition
that fans out over whatever `GET /sessions` returns, so a new season needs no
model edit. `tests/test_powerbi_contract.py` asserts the requested column lists
still match the Pydantic response models.

## Testing & CI

```
pytest                  # everything
pytest -m "not db"      # parsers, profiler, checks, Power BI contract
pytest -m db            # repository, hypertable, continuous aggregate
ruff check .
```

Tests that need a database are marked `db` automatically: `conftest.py` tags any
test reaching for the `database` or `loaded_db` fixture, so the marker cannot
drift from reality. They skip when no TimescaleDB is reachable.

Those tests delete rows, so they run against their own database, `<PGDATABASE>_test`
(override with `PGDATABASE_TEST`), created on first use. Running `pytest` never
touches the database you ingest into.

CI (`.github/workflows/tests.yml`) runs three jobs:

- `lint`: `ruff check`.
- `fast`: no service container on Python 3.11 and 3.13, so the profiler and
  checks are proven database-free. Also runs `python main.py check`, which exits
  non-zero on any error-severity finding.
- `db`: full suite against a pinned `timescale/timescaledb:2.27.1-pg16` service
  container, with a pre-flight assert so the DB tests can never skip silently.

## License

Released under the [MIT License](LICENSE).
