# Draft sensor specifications: ice-2023

Generated from `C:/Users/randl/Documents/GitHub/tiger-racing-telemetry-pipeline/data/raw/2023`. Ranges are the observed extremes, not
engineering limits: widen them by hand and fill in descriptions before
promoting this file to `sensorspecs-ice-2023.md`.

| sensor_name | description | data_type | unit | min_range | max_range |
| --- | --- | --- | --- | --- | --- |
| Av3E9 7 |  | integer | # | 0 | 0 |
| ECU Acc Ped Pos |  | float | % | 1 | 100 |
| ECU AirTemp |  | float | C | 20.75 | 28.15 |
| ECU AuxRPMLimSw |  | integer | # | 0 | 0 |
| ECU BatteryLtSw |  | integer | # | 0 | 0 |
| ECU BatteryVolt |  | float | V | 5.9288 | 13.6944 |
| ECU BrakePedSw |  | integer | # | 0 | 0 |
| ECU CheckEngLtSw |  | integer | # | 0 | 0 |
| ECU ClutchSw |  | integer | # | 0 | 0 |
| ECU CoolantTemp |  | float | C | 59.9672 | 110.743 |
| ECU Cru Last T S |  | integer | km/h | 0 | 0 |
| ECU Crui Spd Err |  | integer | km/h | 0 | 0 |
| ECU Cruise Ctr S |  | integer | # | 0 | 0 |
| ECU Cruise Trg S |  | integer | km/h | 0 | 0 |
| ECU DecelCutActi |  | float | # | 0 | 1 |
| ECU EngLimitAct |  | float | # | 0 | 2 |
| ECU FlatShSw |  | integer | # | 0 | 0 |
| ECU FuelTrimLTB1 |  | integer | % | 0 | 0 |
| ECU FuelTrimLTB2 |  | integer | % | 0 | 0 |
| ECU FuelTrimSTB1 |  | integer | % | 0 | 0 |
| ECU FuelTrimSTB2 |  | integer | % | 0 | 0 |
| ECU Gear |  | integer | gear | 0 | 0 |
| ECU Gear 2 |  | integer | gear | 0 | 0 |
| ECU GearSwitch |  | integer | # | 0 | 0 |
| ECU GenOut1DT |  | integer | % | 0 | 0 |
| ECU GenericSen1 |  | float | # | 485.462 | 4972.69 |
| ECU GenericSen10 |  | integer | # | 0 | 0 |
| ECU GenericSen2 |  | float | # | 461.524 | 4972 |
| ECU GenericSen3 |  | integer | # | 0 | 0 |
| ECU GenericSen4 |  | integer | # | 0 | 0 |
| ECU GenericSen5 |  | integer | # | 0 | 0 |
| ECU GenericSen6 |  | integer | # | 0 | 0 |
| ECU GenericSen7 |  | integer | # | 0 | 0 |
| ECU GenericSen8 |  | integer | # | 0 | 0 |
| ECU GenericSen9 |  | integer | # | 0 | 0 |
| ECU IgnitionAng1 dup 1 |  | float | deg | 3.8275 | 41.9528 |
| ECU IgnitionAng1 dup 2 |  | float | deg | 3.8275 | 41.9528 |
| ECU IgnitionAng2 dup 1 |  | float | deg | 3.8275 | 41.9528 |
| ECU IgnitionAng2 dup 2 |  | float | deg | 3.8275 | 41.9528 |
| ECU Inj Pres D |  | float | bar | 2.001 | 2.7998 |
| ECU InjDT1 |  | float | % | 0 | 77.8449 |
| ECU InjDT2 |  | integer | % | 0 | 0 |
| ECU InjectionDT3 dup 1 |  | integer | % | 0 | 0 |
| ECU InjectionDT3 dup 2 |  | integer | % | 0 | 0 |
| ECU InjectionDT4 dup 1 |  | integer | % | 0 | 0 |
| ECU InjectionDT4 dup 2 |  | integer | % | 0 | 0 |
| ECU KnockLev1 |  | integer | # | 0 | 0 |
| ECU KnockLev2 |  | integer | # | 0 | 0 |
| ECU Lambda1 |  | float | lambda | 0.004 | 4.6327 |
| ECU Laun Ctr Sw |  | integer | # | 0 | 0 |
| ECU RPM |  | float | rpm | 0 | 14706.2 |
| ECU RaceTimer |  | integer | ms | 0 | 0 |
| ECU TPSAct |  | float | # | 0 | 1 |
| ECU TargLambda |  | float | # | 0.9 | 1 |
| ECU ThrottlePos |  | float | % | 1.0117 | 100 |
| ECU TorDrRPMEI |  | integer | deg | 0 | 0 |
| ECU TorDrRPMIC |  | integer | deg | 0 | 0 |
| ECU TorqCIgnCorr dup 1 |  | integer | deg | 0 | 0 |
| ECU TorqCIgnCorr dup 2 |  | integer | deg | 0 | 0 |
| ECU TorqDrvsRPME |  | integer | deg/s | 0 | 0 |
| ECU TorqDrvsRPMT |  | integer | deg/s | 0 | 0 |
| ECU TrigCount |  | float | # | 0 | 21 |
| ECU TrigSyncLev |  | float | # | 0 | 2 |
| ECU VehSpeed |  | integer | km/h | 0 | 0 |
| ECU WheelDiff |  | integer | km/h | 0 | 0 |
| ECU WheelSlip |  | integer | km/h | 0 | 0 |
| ECU WheelSpdFL |  | integer | km/h | 0 | 0 |
| ECU WheelSpdFR |  | integer | km/h | 0 | 0 |
| ECU WheelSpdRL |  | integer | km/h | 0 | 0 |
| ECU WheelSpdRR |  | integer | km/h | 0 | 0 |
| External Voltage |  | float | V | 8.1591 | 13.9594 |
| InlineAcc |  | float | g | -1.7413 | 1.5473 |
| LateralAcc |  | float | g | -1.8574 | 1.6123 |
| Logger Temperature |  | float | C | 32.9375 | 39.1875 |
| Oil Pressure |  | float | bar | 0.0037 | 6.2456 |
| Oil Temp |  | float | C | 47.0625 | 103.311 |
| PitchRate |  | float | deg/s | -18.8461 | 19.0094 |
| PreCalcGear |  | integer | # | 0 | 0 |
| Rear Brake |  | float | bar | -1.9659 | 72.9145 |
| RollRate |  | float | deg/s | -28.1016 | 21.2422 |
| VerticalAcc |  | float | g | -3.6055 | -2.3223 |
| YawRate |  | float | deg/s | -97.8375 | 93.0656 |
