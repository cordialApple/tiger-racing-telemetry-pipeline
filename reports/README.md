# Telemetry Reports

Rendered pages from the Power BI report built over this repo's REST API
(`api/`), plus the 2023 season analysis. All 18 logged sessions come from a
single evening — **UTA Autocross, Oct 7 2023** — so "season" here means that
one event. Figures below are reproducible from the model's measures.

The Power BI project itself isn't committed (it's a local artifact that needs a
live API to refresh); these PNGs are the shareable output.

## Season Overview

![Season Overview](season-overview.png)

The shape of the evening: **18 sessions, 33.7 min** of total logged time, a
**15K** max RPM, and **1.86 g** peak lateral. The per-session bars expose how
uneven the runs were — eight are 10–26 s aborted starts/restarts (note the
three inside two minutes around 20:16), while only a handful are full runs.
Channel health sits flat at ~39% for every session (see Findings for why), and
peak lateral/braking G track together on the real runs, which is the balance you
want.

## Engine Health

![Engine Health](engine-health.png)

Cards read the season-worst: **110.7 °C** coolant, **103.3 °C** oil, **0.931**
average lambda (slightly rich). Temperatures climb with run length — the short
runs sit in the 70s–80s, the long runs push past 100 °C. The **Max RPM vs Max
Coolant Temp** scatter shows the hottest points belong to the sustained
high-RPM runs, not the brief ones. (The "Min Oil Pressure" card reads 0.00
because at least one logged second sits at zero; the per-session floors are on
the Findings page.)

## Findings

![Findings](findings.png)

The four things worth acting on, plus a calibration tell.

1. **Oil starvation under cornering.** At 8,000+ RPM, oil pressure averages
   ~3 bar but the 1-second minimums drop to **0.64–0.83 bar** per session
   (the "more grip, less oil" scatter), with **187 s** of sub-1.5-bar dips at
   8k+ across the season. In S7 those dips coincided with ~1.2 g lateral load —
   more than double the session average — the classic wet-sump pickup-uncovering
   signature. Sub-1-bar at 8k+ RPM risks the rod bearings. *Action:* sump
   baffling / pickup relocation / Accusump, a low-pressure alarm, and a bearing
   inspection.
2. **Cooling runs out on long runs.** Only the 7.6-minute S18 got hot, but it
   hit **110.7 °C** with **112 s above 100 °C** and the curve never plateaus
   ("coolant temp over run time"). A 22-minute endurance would overheat this
   package. *Action:* radiator capacity / fan & shroud ducting.
3. **Half the channels are flat — including the valuable half.** The donut shows
   **50 of 82 channels (61%) carried no signal** all season: every wheel speed,
   vehicle speed, wheel slip, gear position, GPS (hence "NO GPS" session names),
   fuel trims, and knock. No speed traces, lap times, or slip analysis are
   possible from 2023 data. *Action:* wiring/logger config before the next
   event — the single biggest data-quality lever.
4. **Full throttle is barely used.** On real runs (60 s+ and 8k+ RPM), wide-open
   throttle is only **~2–7%** of samples against a 14,706 max RPM. *Action:*
   gearing or driver-coaching conversation.

**Bonus — accelerometer offset.** The friction circle plots per-session average
longitudinal vs lateral G, and the cluster sits at roughly **−0.15 g / −0.18 g**
instead of centered on zero — a small but consistent sensor mounting/zero
offset worth trimming. (A true per-second friction cloud spanning the full
±1.8 g envelope would need the raw reading rows rather than the session-average
measures used here — a good next refinement.)

## Reproducing

The visuals are driven by measures in the model's `Engine`, `Driver`, and
`Dynamics` folders (`Oil Dip Seconds (8k RPM)`, `Min Oil P at 8k (bar)`,
`Coolant Temp (C)`, `WOT Time % (Real Runs)`, the signed-G pair, …). To rebuild
from scratch: bring up the API (`docker compose up -d` then `python main.py
all`), point Power BI's Web/JSON connector at `http://localhost:8000`, and model
the star schema described in the root [README](../README.md#powerbi-connection).
