# Dataset profile: `C:/Users/randl/Documents/GitHub/tiger-racing-telemetry-pipeline/data/raw/2023`

- files: 18 (18 unique by content)
- schemas: 1
- channels: 82
- rows: 40,460

## Schemas

### `79be3c1abc9a` (82 channels, 18 files)

- `1.csv`
- `10.csv`
- `11.csv`
- `12.csv`
- `13.csv`
- `14.csv`
- `15.csv`
- `16.csv`
- `17.csv`
- `18.csv`
- `2.csv`
- `3.csv`
- `4.csv`
- `5.csv`
- `6.csv`
- `7.csv`
- `8.csv`
- `9.csv`

## Constant channels

50 of 82 never change across the whole dataset.

- `Av3E9 7` = 0
- `ECU AuxRPMLimSw` = 0
- `ECU BatteryLtSw` = 0
- `ECU BrakePedSw` = 0
- `ECU CheckEngLtSw` = 0
- `ECU ClutchSw` = 0
- `ECU Cru Last T S` = 0
- `ECU Crui Spd Err` = 0
- `ECU Cruise Ctr S` = 0
- `ECU Cruise Trg S` = 0
- `ECU FlatShSw` = 0
- `ECU FuelTrimLTB1` = 0
- `ECU FuelTrimLTB2` = 0
- `ECU FuelTrimSTB1` = 0
- `ECU FuelTrimSTB2` = 0
- `ECU Gear` = 0
- `ECU Gear 2` = 0
- `ECU GearSwitch` = 0
- `ECU GenOut1DT` = 0
- `ECU GenericSen10` = 0
- `ECU GenericSen3` = 0
- `ECU GenericSen4` = 0
- `ECU GenericSen5` = 0
- `ECU GenericSen6` = 0
- `ECU GenericSen7` = 0
- `ECU GenericSen8` = 0
- `ECU GenericSen9` = 0
- `ECU InjDT2` = 0
- `ECU InjectionDT3 dup 1` = 0
- `ECU InjectionDT3 dup 2` = 0
- `ECU InjectionDT4 dup 1` = 0
- `ECU InjectionDT4 dup 2` = 0
- `ECU KnockLev1` = 0
- `ECU KnockLev2` = 0
- `ECU Laun Ctr Sw` = 0
- `ECU RaceTimer` = 0
- `ECU TorDrRPMEI` = 0
- `ECU TorDrRPMIC` = 0
- `ECU TorqCIgnCorr dup 1` = 0
- `ECU TorqCIgnCorr dup 2` = 0
- `ECU TorqDrvsRPME` = 0
- `ECU TorqDrvsRPMT` = 0
- `ECU VehSpeed` = 0
- `ECU WheelDiff` = 0
- `ECU WheelSlip` = 0
- `ECU WheelSpdFL` = 0
- `ECU WheelSpdFR` = 0
- `ECU WheelSpdRL` = 0
- `ECU WheelSpdRR` = 0
- `PreCalcGear` = 0

## Files

| file | platform | session_id | rows | channels | Hz | uniform | sha |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1.csv` | ice-2023 | `1` | 1,800 | 82 | 20 | yes | `e31fe09fca09` |
| `10.csv` | ice-2023 | `10` | 420 | 82 | 20 | yes | `2391ec60e4e5` |
| `11.csv` | ice-2023 | `11` | 400 | 82 | 20 | yes | `a36ac29dfdc8` |
| `12.csv` | ice-2023 | `12` | 4,840 | 82 | 20 | yes | `10fb1d7513de` |
| `13.csv` | ice-2023 | `13` | 4,580 | 82 | 20 | yes | `8f9f03e9b2a5` |
| `14.csv` | ice-2023 | `14` | 4,220 | 82 | 20 | yes | `a763214a2552` |
| `15.csv` | ice-2023 | `15` | 680 | 82 | 20 | yes | `b9b990dbdb56` |
| `16.csv` | ice-2023 | `16` | 440 | 82 | 20 | yes | `c08fe9842bdf` |
| `17.csv` | ice-2023 | `17` | 260 | 82 | 20 | yes | `e42285ae6d7c` |
| `18.csv` | ice-2023 | `18` | 9,140 | 82 | 20 | yes | `dc86f93aa60f` |
| `2.csv` | ice-2023 | `2` | 220 | 82 | 20 | yes | `06d515409148` |
| `3.csv` | ice-2023 | `3` | 520 | 82 | 20 | yes | `1405237fcbfd` |
| `4.csv` | ice-2023 | `4` | 2,480 | 82 | 20 | yes | `067653b14890` |
| `5.csv` | ice-2023 | `5` | 200 | 82 | 20 | yes | `0e017b9e1b47` |
| `6.csv` | ice-2023 | `6` | 2,160 | 82 | 20 | yes | `7c6efc554f20` |
| `7.csv` | ice-2023 | `7` | 4,360 | 82 | 20 | yes | `eb6353bdd3c4` |
| `8.csv` | ice-2023 | `8` | 3,520 | 82 | 20 | yes | `7461efab496c` |
| `9.csv` | ice-2023 | `9` | 220 | 82 | 20 | yes | `3765399bc6a1` |

## Channels

| channel | unit | platforms | n | missing | min | max | type | constant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Av3E9 7` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Acc Ped Pos` | % | ice-2023 | 40,460 | 0 | 1 | 100 | float |  |
| `ECU AirTemp` | C | ice-2023 | 40,460 | 0 | 20.75 | 28.15 | float |  |
| `ECU AuxRPMLimSw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU BatteryLtSw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU BatteryVolt` | V | ice-2023 | 40,460 | 0 | 5.9288 | 13.6944 | float |  |
| `ECU BrakePedSw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU CheckEngLtSw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU ClutchSw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU CoolantTemp` | C | ice-2023 | 40,460 | 0 | 59.9672 | 110.743 | float |  |
| `ECU Cru Last T S` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Crui Spd Err` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Cruise Ctr S` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Cruise Trg S` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU DecelCutActi` | # | ice-2023 | 40,460 | 0 | 0 | 1 | float |  |
| `ECU EngLimitAct` | # | ice-2023 | 40,460 | 0 | 0 | 2 | float |  |
| `ECU FlatShSw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU FuelTrimLTB1` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU FuelTrimLTB2` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU FuelTrimSTB1` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU FuelTrimSTB2` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Gear` | gear | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Gear 2` | gear | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GearSwitch` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenOut1DT` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen1` | # | ice-2023 | 40,460 | 0 | 485.462 | 4972.69 | float |  |
| `ECU GenericSen10` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen2` | # | ice-2023 | 40,460 | 0 | 461.524 | 4972 | float |  |
| `ECU GenericSen3` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen4` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen5` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen6` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen7` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen8` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU GenericSen9` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU IgnitionAng1 dup 1` | deg | ice-2023 | 40,460 | 0 | 3.8275 | 41.9528 | float |  |
| `ECU IgnitionAng1 dup 2` | deg | ice-2023 | 40,460 | 0 | 3.8275 | 41.9528 | float |  |
| `ECU IgnitionAng2 dup 1` | deg | ice-2023 | 40,460 | 0 | 3.8275 | 41.9528 | float |  |
| `ECU IgnitionAng2 dup 2` | deg | ice-2023 | 40,460 | 0 | 3.8275 | 41.9528 | float |  |
| `ECU Inj Pres D` | bar | ice-2023 | 40,460 | 0 | 2.001 | 2.7998 | float |  |
| `ECU InjDT1` | % | ice-2023 | 40,460 | 0 | 0 | 77.8449 | float |  |
| `ECU InjDT2` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU InjectionDT3 dup 1` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU InjectionDT3 dup 2` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU InjectionDT4 dup 1` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU InjectionDT4 dup 2` | % | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU KnockLev1` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU KnockLev2` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU Lambda1` | lambda | ice-2023 | 40,460 | 0 | 0.004 | 4.6327 | float |  |
| `ECU Laun Ctr Sw` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU RPM` | rpm | ice-2023 | 40,460 | 0 | 0 | 14706.2 | float |  |
| `ECU RaceTimer` | ms | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TPSAct` | # | ice-2023 | 40,460 | 0 | 0 | 1 | float |  |
| `ECU TargLambda` | # | ice-2023 | 40,460 | 0 | 0.9 | 1 | float |  |
| `ECU ThrottlePos` | % | ice-2023 | 40,460 | 0 | 1.0117 | 100 | float |  |
| `ECU TorDrRPMEI` | deg | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TorDrRPMIC` | deg | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TorqCIgnCorr dup 1` | deg | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TorqCIgnCorr dup 2` | deg | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TorqDrvsRPME` | deg/s | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TorqDrvsRPMT` | deg/s | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU TrigCount` | # | ice-2023 | 40,460 | 0 | 0 | 21 | float |  |
| `ECU TrigSyncLev` | # | ice-2023 | 40,460 | 0 | 0 | 2 | float |  |
| `ECU VehSpeed` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU WheelDiff` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU WheelSlip` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU WheelSpdFL` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU WheelSpdFR` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU WheelSpdRL` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `ECU WheelSpdRR` | km/h | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `External Voltage` | V | ice-2023 | 40,460 | 0 | 8.1591 | 13.9594 | float |  |
| `InlineAcc` | g | ice-2023 | 40,460 | 0 | -1.7413 | 1.5473 | float |  |
| `LateralAcc` | g | ice-2023 | 40,460 | 0 | -1.8574 | 1.6123 | float |  |
| `Logger Temperature` | C | ice-2023 | 40,460 | 0 | 32.9375 | 39.1875 | float |  |
| `Oil Pressure` | bar | ice-2023 | 40,460 | 0 | 0.0037 | 6.2456 | float |  |
| `Oil Temp` | C | ice-2023 | 40,460 | 0 | 47.0625 | 103.311 | float |  |
| `PitchRate` | deg/s | ice-2023 | 40,460 | 0 | -18.8461 | 19.0094 | float |  |
| `PreCalcGear` | # | ice-2023 | 40,460 | 0 | 0 | 0 | integer | yes |
| `Rear Brake` | bar | ice-2023 | 40,460 | 0 | -1.9659 | 72.9145 | float |  |
| `RollRate` | deg/s | ice-2023 | 40,460 | 0 | -28.1016 | 21.2422 | float |  |
| `VerticalAcc` | g | ice-2023 | 40,460 | 0 | -3.6055 | -2.3223 | float |  |
| `YawRate` | deg/s | ice-2023 | 40,460 | 0 | -97.8375 | 93.0656 | float |  |
