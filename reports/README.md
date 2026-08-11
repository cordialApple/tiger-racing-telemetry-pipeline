# Telemetry Reports

Rendered pages from the Power BI report built over this repo's REST API
(`api/`), plus the season analyses. The report source is committed as a PBIP
project in [`powerbi/`](../powerbi/README.md); these PNGs are the shareable
output, since refreshing the real thing needs a live API.

Seven pages, four for the 2023 combustion car and three for the 2026 EV.

## 2023, UTA Autocross, Oct 7

All 18 logged sessions come from a single evening, so "season" here means that
one event. The figures below are reproducible from the model's measures.

### Season Overview

![Season Overview](season-overview.png)

This is the shape of the evening: 18 sessions, 33.7 min of total logged time, a
15K max RPM, and 1.86 g peak lateral. The per-session bars show how uneven the
runs were. Eight are 10–26 s aborted starts and restarts (note the three inside
two minutes around 20:16), while only a handful are full runs. Channel health
sits flat at ~39% for every session (see Findings for why), and peak
lateral/braking G track together on the real runs, which is the balance you want.

### Engine Health

![Engine Health](engine-health.png)

The cards read the season-worst: 110.7 °C coolant, 103.3 °C oil, and 0.931
average lambda (slightly rich). Temperatures climb with run length, so the short
runs sit in the 70s–80s while the long runs push past 100 °C. The **Max RPM vs
Max Coolant Temp** scatter shows the hottest points belong to the sustained
high-RPM runs, not the brief ones. The "Min Oil Pressure" card reads 0.00 because
at least one logged second sits at zero; the per-session floors are on the
Findings page.

### Findings

![Findings](findings.png)

The four things worth acting on, plus a calibration tell.

1. **Oil starvation under cornering.** At 8,000+ RPM, oil pressure averages
   ~3 bar, but the 1-second minimums drop to **0.64–0.83 bar** per session
   (the "more grip, less oil" scatter), with **187 s** of sub-1.5-bar dips at
   8k+ across the season. In S7 those dips coincided with ~1.2 g lateral load,
   more than double the session average, which is the classic wet-sump
   pickup-uncovering signature. Sub-1-bar at 8k+ RPM risks the rod bearings.
   *Action:* sump baffling, pickup relocation, or an Accusump, plus a
   low-pressure alarm and a bearing inspection.
2. **Cooling runs out on long runs.** Only the 7.6-minute S18 got hot, but it
   hit **110.7 °C** with **112 s above 100 °C**, and the curve never plateaus
   ("coolant temp over run time"). A 22-minute endurance would overheat this
   package. *Action:* radiator capacity, or fan and shroud ducting.
3. **Half the channels are flat, including the valuable half.** The donut shows
   **50 of 82 channels (61%) carried no signal** all season: every wheel speed,
   vehicle speed, wheel slip, gear position, GPS (hence the "NO GPS" session
   names), fuel trims, and knock. No speed traces, lap times, or slip analysis
   are possible from 2023 data. *Action:* fix the wiring and logger config before
   the next event, the single biggest data-quality lever.
4. **Full throttle is barely used.** On real runs (60 s+ and 8k+ RPM), wide-open
   throttle is only **~2–7%** of samples against a 14,706 max RPM. *Action:* a
   gearing or driver-coaching conversation.

**Bonus, an accelerometer offset.** The friction circle plots per-session average
longitudinal vs lateral G, and the cluster sits at roughly **−0.15 g / −0.18 g**
instead of centered on zero, a small but consistent sensor mounting/zero offset
worth trimming. A true per-second friction cloud spanning the full ±1.8 g
envelope would need the raw reading rows rather than the session-average measures
used here, which is a good next refinement.

## 2026, drive day, Jul 18

21 unique sessions across four drivers (Emiliano 7, Tristan 7, Ryan 4, Yianni 2,
plus one unattributed shakedown), 19.8 min of logged time at 10 Hz. Five files
were the same run filed under two drivers; `ingestion_source` keeps both
attributions. Screenshots for the three EV pages are pending an export from
Power BI Desktop; the numbers below come from the same measures those pages use.

### EV Drive Day

The drive day was made of very short runs. The longest session is **229 s** and
the deepest state-of-charge drop in any session is **4%**, so nothing here is
endurance-representative yet. Motor speed peaks at **3,326 RPM**, DC current at
**129.5 A**, AC current at **380.2 A**, and duty cycle at **95%**, which is a
real load even in short bursts.

### EV Thermal

Nothing overheated, but nothing plateaued either. Motor peaks at **61.9 °C** and
the controller at **68.9 °C**, with **696 samples (~70 s)** of motor temperature
at or above 55 °C. The radiator is the number to watch: inlet reaches 61 °C
against a 58 °C outlet, so the best heat rejection observed all day is a
**delta of 8 °C**. On runs this short that is untested, not proven.

### EV Findings

1. **The controller reported a fault for a fifth of the drive day.** `Fault Code`
   is non-zero on **2,641 of 11,913 samples (22%)**, reaching code 4. That is the
   single loudest signal in the drop and it belongs in a controller log review
   before the next session. *Action:* decode the fault codes against the
   controller manual and correlate with the current and duty-cycle traces.
2. **The flowrate sensor spikes out of physical range.** 150 samples exceed the
   0 to 40 spec, peaking at **4,132**. The team already suspected it, one file is
   literally named `(Weird FlowRate)`. *Action:* the cooling-loop flow number is
   not trustworthy until this is wired or scaled correctly, which also blocks any
   real heat-rejection math.
3. **21 of 60 channels are flat at zero.** Brake pressure, MC throttle, relay
   state, TSB temp, and the LV-low alarm all carried no signal, and the whole IMU
   block (`ACC Lat/Long/Vert`, roll/pitch/yaw rate) exists in only **1 of 26
   files**, which is why the drop has two schemas. No G traces or driver dynamics
   are possible from most of this data. *Action:* same lever as 2023, fix the
   logger config before the next event.
4. **Regen is present but barely used.** Motor speed goes negative on only
   **256 samples (~26 s)**, floor **-1,014 RPM**. Whether that is strategy,
   tuning, or driver habit is worth a conversation.
5. **LV supply is healthy.** `VBAT` holds **13.24 to 14.82 V** all day and the
   `LV Low` alarm never fires, so the low-voltage side is not a suspect.

## Reproducing

The visuals are driven by measures in the model's `Engine`, `Driver`,
`Dynamics`, and the six `EV *` folders (`Oil Dip Seconds (8k RPM)`, `Min Oil P at 8k (bar)`,
`Coolant Temp (C)`, `WOT Time % (Real Runs)`, the signed-G pair, etc.). To
rebuild from scratch: bring up the API (`docker compose up -d` then `python
main.py all`), point Power BI's Web/JSON connector at `http://localhost:8000`,
and model the star schema described in the root
[README](../README.md#api-power-bi-connection).
