# Power BI Telemetry Report

Power BI project (`.pbip`, PBIR format) over the telemetry served by this repo's
REST API, covering both cars. Open `tiger-telemetry.pbip` in Power BI Desktop.

Seven pages: four for the 2023 combustion car (Season Overview, Session
Deep-Dive, Engine Health, Findings) and three for the 2026 electric car (EV Drive
Day, EV Thermal, EV Findings).

The 2026 pages carry no page-level filter, by design. 2026 channel names are
disjoint from 2023, so every sensor-scoped measure is already car-scoped and
Power BI drops the session categories that come back blank. The two measures that
are not sensor-scoped, `EV Sessions` and `EV Track Time (min)`, filter on
`Sessions[platform]` in DAX instead.

**The `.pbix` is a build output, not a source.** The `.pbip` plus the `.Report`
and `.SemanticModel` folders are the source of truth and the only part that
diffs. To produce a `.pbix`, open the `.pbip` in Power BI Desktop and use
File > Save As. `2023-Telemetry-Pipeline-V1.pbix` is an older binary kept for
reference.

Everything here is plain JSON/TMDL, so the report and semantic model diff like
code. The machine-local data cache (`.pbi/cache.abf`) is gitignored, so on first
open the visuals are empty until you refresh, and refresh needs the pipeline
running:

```
docker compose up -d        # TimescaleDB (volume keeps prior ingests)
python main.py all          # ingest data/raw, then serve the API on :8000
```

then **Refresh** in Power BI Desktop.

## Pages

| Page | What it shows |
|---|---|
| Season Overview | KPI cards (sessions, track time, max RPM, peak lateral G) and per-session bars for track time, channel health, RPM, and peak G |
| Session Deep-Dive | Session + sensor slicers driving a 1 Hz trace (avg with min/max envelope) and a channel summary table |
| Engine Health | Coolant/oil temps, oil pressure, lambda, and WOT cards; temps and oil pressure per session; RPM-vs-coolant scatter |
| Findings | The 2023 analysis distilled: oil-starvation evidence, coolant-vs-runtime curves, real-run WOT share, live-vs-flat channels, and a friction circle |

## 2023 findings (UTA Autocross, Oct 7)

All 18 logged sessions are from one evening. The numbers below come from the
model's measures and are reproducible from the Findings page.

1. **Oil starvation under cornering.** At 8,000+ RPM, oil pressure averages
   ~3 bar but the 1-second minimums dip to **0.64–0.69 bar** in every hard
   session (S7, S14, S18). In S7 there were 28 s of sub-1.5-bar dips at 8k+,
   during which the car averaged **1.24 g lateral / 1.07 g longitudinal** vs
   session averages of 0.53 / 0.50 — the classic wet-sump pickup-uncovering
   signature. Action: sump baffling / pickup / Accusump, a low-pressure alarm,
   and a bearing inspection.
2. **Cooling runs out on long runs.** Only the 7.6-minute S18 got hot, but it
   hit **110.7 °C coolant** (112 s ≥ 100°, 67 s ≥ 105°, 22 s ≥ 110°) with oil
   at 103 °C, and the temperature curve never plateaus. A 22-minute endurance
   would overheat this package. Action: radiator capacity / fan & shroud
   ducting.
3. **Half the channel list is flat — including the valuable half.** 50 of 82
   channels carried no signal all season: all four wheel speeds, vehicle
   speed, wheel slip, gear position, GPS (every session is literally named
   "NO GPS"), fuel trims, knock. No speed traces, lap times, or slip analysis
   are possible from 2023 data. Action: wiring/logger config before the next
   event — the single biggest data-quality lever.
4. **Full throttle is barely used.** On real runs (60 s+ duration and 8k+ max
   RPM — 7 of the 18 sessions qualify), wide-open throttle is only **2–7 %**
   of samples against a 14,706 max RPM. Gearing or driver-coaching
   conversation.
5. **Grip ceiling:** peak lateral 1.86 g (S7), peak braking 1.74 g (S6) — see
   the friction circle on the Findings page.

## Model notes

- Star schema per the API contract: `Sessions` and `Sensors` dimensions →
  `Channels` (per-session sensor health) → `Readings` (1 Hz long-format fact)
  and `Stats` (full-rate per-session/sensor summary). Composite channel keys
  are `session_id|sensor_name`.
- `Channels`, `Readings`, and `Stats` use **one M partition per session**
  (18 each), each a single static `Web.Contents` call against
  `http://localhost:8000`. Multi-request M in one query trips Power Query's
  privacy-level firewall on an unconfigured source; single-call partitions
  avoid that structurally and allow per-session refresh. The 2023 archive is
  frozen at 18 sessions; a new session means adding one partition per fact
  table.
- Measures live in display folders: Season, Health, Telemetry, Engine
  (incl. `Oil Dip Seconds (8k RPM)`, `Min Oil P at 8k (bar)`,
  `Coolant Temp (C)`), Driver (`WOT Time %`, `WOT Time % (Real Runs)`), and
  Dynamics (peak/signed G measures for the friction circle).
- Channel-pinned measures (e.g. `Coolant Temp (C)`) filter
  `Sensors[sensor_name]` internally so visuals need no slicer or filter pane
  entry; cross-channel measures align channels on `Readings[t_seconds]` via
  `TREATAS`.
