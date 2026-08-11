# Dataset profile: `data/raw/2026`

- files: 26 (21 unique by content)
- schemas: 2
- channels: 60
- rows: 15,165

## Schemas

### `61ca8aace672` (60 channels, 1 files)

- `Drive Day 7_18/2026-7-18   17.55.26.csv`

### `c04d20aa28c5` (54 channels, 25 files)

- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.25.44.csv`
- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.27.33.csv`
- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.28.16.csv`
- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.28.42.csv`
- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.29.23.csv`
- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.30.04.csv`
- `Drive Day 7_18/Emiliano Drive/2026-7-18   21.30.30.csv`
- `Drive Day 7_18/Ryan Drive/2026-7-18   21.50.44.csv`
- `Drive Day 7_18/Ryan Drive/2026-7-18   21.53.09.csv`
- `Drive Day 7_18/Ryan Drive/2026-7-18   21.56.34(Weird FlowRate).csv`
- `Drive Day 7_18/Ryan Drive/2026-7-18   21.59.22.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.02.21.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.06.15.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.08.05.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.10.00.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.14.12.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.48.37.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.50.06.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   18.10.04.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   18.17.38.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   20.02.21.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   20.06.15.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   20.08.05.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   20.10.00.csv`
- `Drive Day 7_18/Yianni Drive/2026-7-18   20.14.12 (Still Pump Run).csv`

### Drift

- `61ca8aace672` only: ['ACC Lat', 'ACC Long', 'ACC Vert', 'Pitch Rate', 'Roll Rate', 'Yaw Rate']
- `c04d20aa28c5` only: none

## Duplicate content

- `Drive Day 7_18/Tristan Drive/2026-7-18   20.02.21.csv`, `Drive Day 7_18/Yianni Drive/2026-7-18   20.02.21.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.06.15.csv`, `Drive Day 7_18/Yianni Drive/2026-7-18   20.06.15.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.08.05.csv`, `Drive Day 7_18/Yianni Drive/2026-7-18   20.08.05.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.10.00.csv`, `Drive Day 7_18/Yianni Drive/2026-7-18   20.10.00.csv`
- `Drive Day 7_18/Tristan Drive/2026-7-18   20.14.12.csv`, `Drive Day 7_18/Yianni Drive/2026-7-18   20.14.12 (Still Pump Run).csv`

## Constant channels

21 of 60 never change across the whole dataset.

- `ACC Lat` = 0
- `ACC Long` = 0
- `ACC Vert` = 0
- `ALARMS1` = 0
- `Actual_Brake` = 0
- `Actual_FOC_id` = 0
- `Actual_FOC_iq` = 0
- `CAN1 Load` = 0
- `CAN2 ERRORS` = 0
- `CRC_Checksum` = 0
- `CRC_Checksum_22` = 0
- `CellId` = 0
- `LV Low` = 0
- `MC Throttle` = 0
- `Pitch Rate` = 0
- `Relay_State` = 0
- `Roll Rate` = 0
- `Rolling_Counter` = 0
- `TSB Temp` = 0
- `WATER T ALM` = 0
- `Yaw Rate` = 0

## Files

| file | platform | session_id | rows | channels | Hz | uniform | sha |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Drive Day 7_18/2026-7-18   17.55.26.csv` | ev-2026 | `2026-07-18_175526` | 339 | 60 | 10 | yes | `c5c639ca1fa3` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.25.44.csv` | ev-2026 | `2026-07-18_212544_emiliano` | 579 | 54 | 10 | yes | `200a690cbeb5` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.27.33.csv` | ev-2026 | `2026-07-18_212733_emiliano` | 419 | 54 | 10 | yes | `5e9e04831922` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.28.16.csv` | ev-2026 | `2026-07-18_212816_emiliano` | 220 | 54 | 10 | yes | `07173121b153` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.28.42.csv` | ev-2026 | `2026-07-18_212842_emiliano` | 220 | 54 | 10 | yes | `f26c5b91a912` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.29.23.csv` | ev-2026 | `2026-07-18_212923_emiliano` | 380 | 54 | 10 | yes | `67460352e955` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.30.04.csv` | ev-2026 | `2026-07-18_213004_emiliano` | 220 | 54 | 10 | yes | `1a8433bf1168` |
| `Drive Day 7_18/Emiliano Drive/2026-7-18   21.30.30.csv` | ev-2026 | `2026-07-18_213030_emiliano` | 260 | 54 | 10 | yes | `2f775054c4e7` |
| `Drive Day 7_18/Ryan Drive/2026-7-18   21.50.44.csv` | ev-2026 | `2026-07-18_215044_ryan` | 658 | 54 | 10 | yes | `6939b3836a08` |
| `Drive Day 7_18/Ryan Drive/2026-7-18   21.53.09.csv` | ev-2026 | `2026-07-18_215309_ryan` | 380 | 54 | 10 | yes | `1cca7c275163` |
| `Drive Day 7_18/Ryan Drive/2026-7-18   21.56.34(Weird FlowRate).csv` | ev-2026 | `2026-07-18_215634_ryan` | 419 | 54 | 10 | yes | `f8a2dfe19bc5` |
| `Drive Day 7_18/Ryan Drive/2026-7-18   21.59.22.csv` | ev-2026 | `2026-07-18_215922_ryan` | 220 | 54 | 10 | yes | `4c8d0190b666` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.02.21.csv` | ev-2026 | `2026-07-18_200221_tristan` | 897 | 54 | 10 | yes | `6faa00635374` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.06.15.csv` | ev-2026 | `2026-07-18_200615_tristan` | 738 | 54 | 10 | yes | `25aa01e1dcba` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.08.05.csv` | ev-2026 | `2026-07-18_200805_tristan` | 180 | 54 | 10 | yes | `554af5ad576c` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.10.00.csv` | ev-2026 | `2026-07-18_201000_tristan` | 858 | 54 | 10 | yes | `629d7d57091b` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.14.12.csv` | ev-2026 | `2026-07-18_201412_tristan` | 579 | 54 | 10 | yes | `564a12f3d813` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.48.37.csv` | ev-2026 | `2026-07-18_204837_tristan` | 579 | 54 | 10 | yes | `e57d3de89d6f` |
| `Drive Day 7_18/Tristan Drive/2026-7-18   20.50.06.csv` | ev-2026 | `2026-07-18_205006_tristan` | 2,292 | 54 | 10 | yes | `667a6e15a439` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   18.10.04.csv` | ev-2026 | `2026-07-18_181004_yianni` | 897 | 54 | 10 | yes | `953f71ef131b` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   18.17.38.csv` | ev-2026 | `2026-07-18_181738_yianni` | 579 | 54 | 10 | yes | `382db1f8ede7` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   20.02.21.csv` | ev-2026 | `2026-07-18_200221_yianni` | 897 | 54 | 10 | yes | `6faa00635374` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   20.06.15.csv` | ev-2026 | `2026-07-18_200615_yianni` | 738 | 54 | 10 | yes | `25aa01e1dcba` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   20.08.05.csv` | ev-2026 | `2026-07-18_200805_yianni` | 180 | 54 | 10 | yes | `554af5ad576c` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   20.10.00.csv` | ev-2026 | `2026-07-18_201000_yianni` | 858 | 54 | 10 | yes | `629d7d57091b` |
| `Drive Day 7_18/Yianni Drive/2026-7-18   20.14.12 (Still Pump Run).csv` | ev-2026 | `2026-07-18_201412_yianni` | 579 | 54 | 10 | yes | `564a12f3d813` |

## Channels

| channel | unit | platforms | n | missing | min | max | type | constant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AC Current` |  | ev-2026 | 15,165 | 0 | -38 | 380.2 | float |  |
| `ACC Lat` | g | ev-2026 | 339 | 0 | 0 | 0 | integer | yes |
| `ACC Long` | g | ev-2026 | 339 | 0 | 0 | 0 | integer | yes |
| `ACC Vert` | g | ev-2026 | 339 | 0 | 0 | 0 | integer | yes |
| `ALARMS1` | decimal | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `AN3` | V | ev-2026 | 15,165 | 0 | 4.858 | 4.868 | float |  |
| `AN6` | V | ev-2026 | 15,165 | 0 | 0 | 0.015 | float |  |
| `Actual_Brake` | % | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Actual_FOC_id` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Actual_FOC_iq` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `CAN1 ERRORS` | hex | ev-2026 | 15,165 | 0 | 16 | 32 | integer |  |
| `CAN1 Load` | % | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `CAN2 ERRORS` | decimal | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `CRC_Checksum` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `CRC_Checksum_22` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Cell Low` |  | ev-2026 | 15,165 | 0 | 0 | 20 | integer |  |
| `CellId` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `DC Current` | A | ev-2026 | 15,165 | 0 | 0 | 129.5 | float |  |
| `Drive Enable` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `Energized` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `Fault Code` |  | ev-2026 | 15,165 | 0 | 0 | 4 | integer |  |
| `Flowrate` |  | ev-2026 | 15,165 | 0 | 0 | 4132 | integer |  |
| `Int Temp` | °C | ev-2026 | 15,165 | 0 | 34 | 41 | integer |  |
| `LV Low` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Logging` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `MC Duty Cycle` | % | ev-2026 | 15,165 | 0 | -33.8 | 95 | float |  |
| `MC Temp` | °C | ev-2026 | 15,165 | 0 | 25 | 68.9 | float |  |
| `MC Temp High` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `MC Throttle` | % | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `MC Volts` | V | ev-2026 | 15,165 | 0 | 1 | 341 | integer |  |
| `Motor RPM` | Rpm | ev-2026 | 15,165 | 0 | -1014 | 3326 | float |  |
| `Motor Temp` | °C | ev-2026 | 15,165 | 0 | 22.9 | 61.9 | float |  |
| `Motor Temp High` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `Pack_CCL` |  | ev-2026 | 15,165 | 0 | 0 | 13 | integer |  |
| `Pack_Current` |  | ev-2026 | 15,165 | 0 | -16.9 | 161.1 | float |  |
| `Pack_DCL` |  | ev-2026 | 15,165 | 0 | 0 | 190 | integer |  |
| `Pack_Open_Volta` |  | ev-2026 | 15,165 | 0 | 0 | 1 | float |  |
| `Pack_SOC` |  | ev-2026 | 15,165 | 0 | 0 | 41 | integer |  |
| `Pitch Rate` | deg/sec | ev-2026 | 339 | 0 | 0 | 0 | integer | yes |
| `RTD` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `RadIn_Temp` | °C | ev-2026 | 15,165 | 0 | 32 | 61 | integer |  |
| `RadOut_Tem` | °C | ev-2026 | 15,165 | 0 | 29 | 58 | integer |  |
| `Relay_State` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Roll Rate` | deg/sec | ev-2026 | 339 | 0 | 0 | 0 | integer | yes |
| `Rolling_Counter` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Stop Logging` |  | ev-2026 | 15,165 | 0 | 0 | 1 | boolean |  |
| `TSB HighTemp` |  | ev-2026 | 15,165 | 0 | 0 | 41 | integer |  |
| `TSB Temp` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Therm1_HighVal` | °C | ev-2026 | 15,165 | 0 | 0 | 41 | integer |  |
| `Therm1_ID` |  | ev-2026 | 15,165 | 0 | -851583 | 0 | integer |  |
| `Therm1_LowVal` | °C | ev-2026 | 15,165 | 0 | 0 | 20 | integer |  |
| `Therm1_ModNum` |  | ev-2026 | 15,165 | 0 | 0 | 8 | integer |  |
| `Therm1_Val` | °C | ev-2026 | 15,165 | 0 | 0 | 41 | integer |  |
| `Therm2_HighVal` | °C | ev-2026 | 15,165 | 0 | 0 | 41 | integer |  |
| `Therm2_LowVal` | °C | ev-2026 | 15,165 | 0 | 0 | 39 | integer |  |
| `Therm2_Val` | °C | ev-2026 | 15,165 | 0 | 0 | 41 | integer |  |
| `VBAT` | V | ev-2026 | 15,165 | 0 | 13.244 | 14.817 | float |  |
| `WATER T ALM` |  | ev-2026 | 15,165 | 0 | 0 | 0 | integer | yes |
| `Yaw Rate` | deg/sec | ev-2026 | 339 | 0 | 0 | 0 | integer | yes |
| `uFLAGS1` | decimal | ev-2026 | 15,165 | 0 | 0 | 160 | integer |  |
