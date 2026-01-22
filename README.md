# core-ranker

Prints information about the system & CPU core rankings.

- [core-ranker](#core-ranker)
  - [Example Outputs](#example-outputs)
    - [13th Gen Intel(R) Core(TM) i9-13950HX](#13th-gen-intelr-coretm-i9-13950hx)
    - [AMD EPYC 9354P 32-Core Processor](#amd-epyc-9354p-32-core-processor)
    - [AMD Ryzen 5 5500GT with Radeon Graphics](#amd-ryzen-5-5500gt-with-radeon-graphics)
    - [AMD Ryzen 9 7950X 16-Core Processor](#amd-ryzen-9-7950x-16-core-processor)
    - [AMD Ryzen AI 7 350 w/ Radeon 860M](#amd-ryzen-ai-7-350-w-radeon-860m)
    - [Raspberry Pi 4 Model B Rev 1.2](#raspberry-pi-4-model-b-rev-12)


## Example Outputs

### 13th Gen Intel(R) Core(TM) i9-13950HX
```
CPU Model: 13th Gen Intel(R) Core(TM) i9-13950HX
Governor:  powersave (performance, powersave)
Turbo:     Enabled
Driver:    intel_pstate
Kernel:    6.18.5-100.fc42.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Jan 11 18:16:46 UTC 2026

Rank | CPU IDs | MHz min | MHz max
----:|:--------|--------:|--------:
  70 |   8,  9 |     800 |    5500
  70 |  10, 11 |     800 |    5500
  68 |   0,  1 |     800 |    5300
  68 |   2,  3 |     800 |    5300
  68 |   4,  5 |     800 |    5300
  68 |   6,  7 |     800 |    5300
  68 |  12, 13 |     800 |    5300
  68 |  14, 15 |     800 |    5300
  40 |      16 |     800 |    4000
  40 |      17 |     800 |    4000
  40 |      18 |     800 |    4000
  40 |      19 |     800 |    4000
  40 |      20 |     800 |    4000
  40 |      21 |     800 |    4000
  40 |      22 |     800 |    4000
  40 |      23 |     800 |    4000
  40 |      24 |     800 |    4000
  40 |      25 |     800 |    4000
  40 |      26 |     800 |    4000
  40 |      27 |     800 |    4000
  40 |      28 |     800 |    4000
  40 |      29 |     800 |    4000
  40 |      30 |     800 |    4000
  40 |      31 |     800 |    4000
```

### AMD EPYC 9354P 32-Core Processor
```
CPU Model: AMD EPYC 9354P 32-Core Processor
Governor:  schedutil (conservative, ondemand, userspace, powersave, performance, schedutil)
Turbo:     Enabled
Driver:    acpi-cpufreq
Kernel:    6.18.5-100.fc42.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Jan 11 18:16:46 UTC 2026

Rank | CPU IDs | MHz min | MHz max
----:|:--------|--------:|--------:
 255 |   0, 32 |    1500 |    3800
 255 |   1, 33 |    1500 |    3800
 255 |   2, 34 |    1500 |    3800
 255 |   3, 35 |    1500 |    3800
 255 |   4, 36 |    1500 |    3800
 255 |   5, 37 |    1500 |    3800
 255 |   6, 38 |    1500 |    3800
 255 |   7, 39 |    1500 |    3800
 255 |   8, 40 |    1500 |    3800
 255 |   9, 41 |    1500 |    3800
 255 |  10, 42 |    1500 |    3800
 255 |  11, 43 |    1500 |    3800
 255 |  12, 44 |    1500 |    3800
 255 |  13, 45 |    1500 |    3800
 255 |  14, 46 |    1500 |    3800
 255 |  15, 47 |    1500 |    3800
 255 |  16, 48 |    1500 |    3800
 255 |  17, 49 |    1500 |    3800
 255 |  18, 50 |    1500 |    3800
 255 |  19, 51 |    1500 |    3800
 255 |  20, 52 |    1500 |    3800
 255 |  21, 53 |    1500 |    3800
 255 |  22, 54 |    1500 |    3800
 255 |  23, 55 |    1500 |    3800
 255 |  24, 56 |    1500 |    3800
 255 |  25, 57 |    1500 |    3800
 255 |  26, 58 |    1500 |    3800
 255 |  27, 59 |    1500 |    3800
 255 |  28, 60 |    1500 |    3800
 255 |  29, 61 |    1500 |    3800
 255 |  30, 62 |    1500 |    3800
 255 |  31, 63 |    1500 |    3800
```

### AMD Ryzen 5 5500GT with Radeon Graphics
```
CPU Model: AMD Ryzen 5 5500GT with Radeon Graphics
Governor:  powersave (performance, powersave)
Turbo:     Enabled
Driver:    amd-pstate-epp
Kernel:    6.18.5-200.fc43.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Jan 11 17:09:32 UTC 2026

Rank | CPU IDs | MHz min | MHz max
----:|:--------|--------:|--------:
 186 |   0,  6 |     402 |    4459
 186 |   2,  8 |     402 |    4459
 181 |   4, 10 |     402 |    4459
 176 |   5, 11 |     402 |    4459
 171 |   1,  7 |     402 |    4459
 166 |   3,  9 |     402 |    4459
```

### AMD Ryzen 9 7950X 16-Core Processor

```
CPU Model: AMD Ryzen 9 7950X 16-Core Processor
Governor:  powersave (performance, powersave)
Turbo:     Enabled
Driver:    amd-pstate-epp
Kernel:    6.18.5-200.fc43.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Jan 11 17:09:32 UTC 2026

Rank | CPU IDs | MHz min | MHz max
----:|:--------|--------:|--------:
 236 |   1, 17 |     425 |    5883
 236 |   5, 21 |     425 |    5883
 231 |   3, 19 |     425 |    5883
 226 |   7, 23 |     425 |    5883
 221 |   4, 20 |     425 |    5883
 216 |   0, 16 |     425 |    5883
 211 |   6, 22 |     425 |    5883
 206 |   2, 18 |     425 |    5883
 201 |  13, 29 |     425 |    5883
 196 |  15, 31 |     425 |    5883
 191 |   9, 25 |     425 |    5883
 186 |  11, 27 |     425 |    5883
 181 |  12, 28 |     425 |    5883
 176 |  10, 26 |     425 |    5883
 171 |  14, 30 |     425 |    5883
 166 |   8, 24 |     425 |    5883
```

### AMD Ryzen AI 7 350 w/ Radeon 860M
```
CPU Model: AMD Ryzen AI 7 350 w/ Radeon 860M
Governor:  powersave (performance, powersave)
Turbo:     Enabled
Driver:    amd-pstate-epp
Kernel:    6.18.5-200.fc43.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Jan 11 17:09:32 UTC 2026

Rank | CPU IDs | MHz min | MHz max
----:|:--------|--------:|--------:
 214 |   6, 14 |     623 |    5090
 208 |   4, 12 |     623 |    5090
 202 |   0,  8 |     623 |    5090
 196 |   2, 10 |     623 |    5090
 135 |   1,  9 |     623 |    3506
 135 |   3, 11 |     623 |    3506
 135 |   5, 13 |     623 |    3506
 129 |   7, 15 |     623 |    3350
```

### Raspberry Pi 4 Model B Rev 1.2
```
CPU Model: Raspberry Pi 4 Model B Rev 1.2
Governor:  ondemand (conservative, ondemand, userspace, powersave, performance, schedutil)
Turbo:     unknown
Driver:    cpufreq-dt
Kernel:    6.1.0-rpi8-rpi-v8 #1 SMP PREEMPT Debian 1:6.1.73-1+rpt1 (2024-01-25)

Rank | CPU IDs | MHz min | MHz max
----:|:--------|--------:|--------:
 100 |       0 |     600 |    1500
 100 |       1 |     600 |    1500
 100 |       2 |     600 |    1500
 100 |       3 |     600 |    1500
```