# Sensor specifications: ev-2026

Advisory operating ranges for the 60 CAN logger channels in
`data/raw/2026/`. These are engineering expectations for the 2026 electric
car, not observed extremes, and validation is advisory only. Empty range
cells denote counters, bitfields, checksums, and switch-like channels.

| sensor_name | description | data_type | unit | min_range | max_range |
| --- | --- | --- | --- | --- | --- |
| AC Current | Motor controller AC phase current | float |  | -400 | 400 |
| ACC Lat | Lateral acceleration | float | g | -3 | 3 |
| ACC Long | Longitudinal acceleration | float | g | -3 | 3 |
| ACC Vert | Vertical acceleration | float | g | -4 | 4 |
| ALARMS1 | Logger alarm bitfield | integer | decimal |  |  |
| AN3 | Logger analogue input 3 | float | V | 0 | 5 |
| AN6 | Logger analogue input 6 | float | V | 0 | 5 |
| Actual_Brake | Brake pedal position reported by the controller | float | % | 0 | 100 |
| Actual_FOC_id | Field-oriented control direct-axis current | float |  | -400 | 400 |
| Actual_FOC_iq | Field-oriented control quadrature-axis current | float |  | -400 | 400 |
| CAN1 ERRORS | CAN bus 1 error counter | integer | hex | 0 | 255 |
| CAN1 Load | CAN bus 1 utilisation | float | % | 0 | 100 |
| CAN2 ERRORS | CAN bus 2 error counter | integer | decimal | 0 | 255 |
| CRC_Checksum | Inverter frame checksum | integer |  |  |  |
| CRC_Checksum_22 | Secondary inverter frame checksum | integer |  |  |  |
| Cell Low | Lowest cell temperature reported by the BMS | integer |  | 0 | 60 |
| CellId | BMS cell index for the reported value | integer |  |  |  |
| DC Current | Tractive system DC bus current | float | A | -200 | 400 |
| Drive Enable | Inverter drive enable | boolean |  |  |  |
| Energized | Tractive system energised | boolean |  |  |  |
| Fault Code | Motor controller fault code | integer |  |  |  |
| Flowrate | Coolant flow rate | integer |  | 0 | 40 |
| Int Temp | Logger internal temperature | integer | °C | -10 | 85 |
| LV Low | Low-voltage battery warning | boolean |  |  |  |
| Logging | Logger actively recording | boolean |  |  |  |
| MC Duty Cycle | Motor controller PWM duty cycle | float | % | -100 | 100 |
| MC Temp | Motor controller heatsink temperature | float | °C | -10 | 90 |
| MC Temp High | Motor controller over-temperature warning | boolean |  |  |  |
| MC Throttle | Throttle demand seen by the motor controller | float | % | 0 | 100 |
| MC Volts | Motor controller DC bus voltage | float | V | 0 | 400 |
| Motor RPM | Motor rotational speed | float | Rpm | -6000 | 6000 |
| Motor Temp | Motor stator temperature | float | °C | -10 | 120 |
| Motor Temp High | Motor over-temperature warning | boolean |  |  |  |
| Pack_CCL | Pack charge current limit | integer |  | 0 | 200 |
| Pack_Current | Accumulator pack current | float |  | -200 | 400 |
| Pack_DCL | Pack discharge current limit | integer |  | 0 | 400 |
| Pack_Open_Volta | Pack open-circuit voltage (name truncated by the DBC export) | float |  | 0 | 400 |
| Pack_SOC | Pack state of charge | integer |  | 0 | 100 |
| Pitch Rate | Pitch rate | float | deg/sec | -300 | 300 |
| RTD | Ready-to-drive state | boolean |  |  |  |
| RadIn_Temp | Radiator inlet coolant temperature | integer | °C | -10 | 90 |
| RadOut_Tem | Radiator outlet coolant temperature (name truncated by the DBC export) | integer | °C | -10 | 90 |
| Relay_State | Accumulator relay state bitfield | integer |  |  |  |
| Roll Rate | Roll rate | float | deg/sec | -300 | 300 |
| Rolling_Counter | Inverter frame rolling counter | integer |  |  |  |
| Stop Logging | Logger stop request | boolean |  |  |  |
| TSB HighTemp | Highest tractive system battery temperature | integer |  | 0 | 60 |
| TSB Temp | Tractive system battery temperature warning | boolean |  |  |  |
| Therm1_HighVal | Thermistor bank 1 highest reading | integer | °C | 0 | 60 |
| Therm1_ID | Thermistor bank 1 sensor id | integer |  |  |  |
| Therm1_LowVal | Thermistor bank 1 lowest reading | integer | °C | 0 | 60 |
| Therm1_ModNum | Thermistor bank 1 module number | integer |  |  |  |
| Therm1_Val | Thermistor bank 1 current reading | integer | °C | 0 | 60 |
| Therm2_HighVal | Thermistor bank 2 highest reading | integer | °C | 0 | 60 |
| Therm2_LowVal | Thermistor bank 2 lowest reading | integer | °C | 0 | 60 |
| Therm2_Val | Thermistor bank 2 current reading | integer | °C | 0 | 60 |
| VBAT | Low-voltage battery voltage | float | V | 10 | 16 |
| WATER T ALM | Coolant temperature alarm | boolean |  |  |  |
| Yaw Rate | Yaw rate | float | deg/sec | -300 | 300 |
| uFLAGS1 | Logger user flag bitfield | integer | decimal |  |  |
