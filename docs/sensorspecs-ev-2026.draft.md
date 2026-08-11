# Draft sensor specifications: ev-2026

Generated from `C:/Users/randl/Documents/GitHub/tiger-racing-telemetry-pipeline/data/raw/2026`. Ranges are the observed extremes, not
engineering limits: widen them by hand and fill in descriptions before
promoting this file to `sensorspecs-ev-2026.md`.

| sensor_name | description | data_type | unit | min_range | max_range |
| --- | --- | --- | --- | --- | --- |
| AC Current |  | float |  | -38 | 380.2 |
| ACC Lat |  | integer | g | 0 | 0 |
| ACC Long |  | integer | g | 0 | 0 |
| ACC Vert |  | integer | g | 0 | 0 |
| ALARMS1 |  | integer | decimal | 0 | 0 |
| AN3 |  | float | V | 4.858 | 4.868 |
| AN6 |  | float | V | 0 | 0.015 |
| Actual_Brake |  | integer | % | 0 | 0 |
| Actual_FOC_id |  | integer |  | 0 | 0 |
| Actual_FOC_iq |  | integer |  | 0 | 0 |
| CAN1 ERRORS |  | integer | hex | 16 | 32 |
| CAN1 Load |  | integer | % | 0 | 0 |
| CAN2 ERRORS |  | integer | decimal | 0 | 0 |
| CRC_Checksum |  | integer |  | 0 | 0 |
| CRC_Checksum_22 |  | integer |  | 0 | 0 |
| Cell Low |  | integer |  | 0 | 20 |
| CellId |  | integer |  | 0 | 0 |
| DC Current |  | float | A | 0 | 129.5 |
| Drive Enable |  | boolean |  | 0 | 1 |
| Energized |  | boolean |  | 0 | 1 |
| Fault Code |  | integer |  | 0 | 4 |
| Flowrate |  | integer |  | 0 | 4132 |
| Int Temp |  | integer | °C | 34 | 41 |
| LV Low |  | integer |  | 0 | 0 |
| Logging |  | boolean |  | 0 | 1 |
| MC Duty Cycle |  | float | % | -33.8 | 95 |
| MC Temp |  | float | °C | 25 | 68.9 |
| MC Temp High |  | boolean |  | 0 | 1 |
| MC Throttle |  | integer | % | 0 | 0 |
| MC Volts |  | integer | V | 1 | 341 |
| Motor RPM |  | float | Rpm | -1014 | 3326 |
| Motor Temp |  | float | °C | 22.9 | 61.9 |
| Motor Temp High |  | boolean |  | 0 | 1 |
| Pack_CCL |  | integer |  | 0 | 13 |
| Pack_Current |  | float |  | -16.9 | 161.1 |
| Pack_DCL |  | integer |  | 0 | 190 |
| Pack_Open_Volta |  | float |  | 0 | 1 |
| Pack_SOC |  | integer |  | 0 | 41 |
| Pitch Rate |  | integer | deg/sec | 0 | 0 |
| RTD |  | boolean |  | 0 | 1 |
| RadIn_Temp |  | integer | °C | 32 | 61 |
| RadOut_Tem |  | integer | °C | 29 | 58 |
| Relay_State |  | integer |  | 0 | 0 |
| Roll Rate |  | integer | deg/sec | 0 | 0 |
| Rolling_Counter |  | integer |  | 0 | 0 |
| Stop Logging |  | boolean |  | 0 | 1 |
| TSB HighTemp |  | integer |  | 0 | 41 |
| TSB Temp |  | integer |  | 0 | 0 |
| Therm1_HighVal |  | integer | °C | 0 | 41 |
| Therm1_ID |  | integer |  | -851583 | 0 |
| Therm1_LowVal |  | integer | °C | 0 | 20 |
| Therm1_ModNum |  | integer |  | 0 | 8 |
| Therm1_Val |  | integer | °C | 0 | 41 |
| Therm2_HighVal |  | integer | °C | 0 | 41 |
| Therm2_LowVal |  | integer | °C | 0 | 39 |
| Therm2_Val |  | integer | °C | 0 | 41 |
| VBAT |  | float | V | 13.244 | 14.817 |
| WATER T ALM |  | integer |  | 0 | 0 |
| Yaw Rate |  | integer | deg/sec | 0 | 0 |
| uFLAGS1 |  | integer | decimal | 0 | 160 |
