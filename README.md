# core-ranker

Runtime of two threads. Benchmark was done like so:

```sh
BENCH_DURATION=10 CPU=7,15 taskset -c $CPU stress-ng --matrix 2 --timeout $BENCH_DURATION --metrics-brief
```

AMD Ryzen 9 7950X 16-Core Processor
16 cores, no efficiency ones, each with Hyperthreadding

ops/sec  |    %   | what
--------:|-------:|:-----------------------
13598.43 | 100.0% | 2 fastest cores
13138.98 |  96.6% | 2 slowest cores
 8210.99 |  60.3% | fastest core, using Hyperthreadding
 8071.79 |  59.4% | slowest core, using Hyperthreadding
 6867.98 |  50.5% | fastest core, NOT using Hyperthreadding
 6867.37 |  50.5% | slowest core, NOT using Hyperthreadding


AMD Ryzen AI 7 350
4 performance cores,4 efficiency cores, each with Hyperthreadding

ops/sec  |    %   | what
--------:|-------:|:-----------------------
14197.41 | 100.0% | 2 fastest performance cores
14066.00 |  99.1% | 2 slowest performance cores
 9504.42 |  66.9% | 2 fastest efficiency cores
 9510.20 |  70.0% | 2 slowest efficiency cores
 7204.34 |  50.7% | fastest performance core, using Hyperthreadding
 7216.04 |  50.8% | slowest performance core, using Hyperthreadding
 4944.82 |  34.8% | fastest efficiency core, using Hyperthreadding
 4752.17 |  33.5% | slowest efficiency core, using Hyperthreadding
 7078.17 |  49.9% | fastest performance core, NOT using Hyperthreadding
 7057.21 |  49.7% | slowest performance core, NOT using Hyperthreadding
 4832.43 |  34.0% | fastest efficiency core, NOT using Hyperthreadding
 4654.00 |  32.8% | slowest efficiency core, NOT using Hyperthreadding


