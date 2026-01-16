#!/bin/bash
A=16
B=31
BENCH_DURATION=10s
SLEEP_DURATION=2
for i in $(seq 1 10);
do
    CPU=$A
    sleep $SLEEP_DURATION
    taskset -c $CPU stress-ng --matrix 1 --timeout $BENCH_DURATION --metrics-brief 2>&1 | awk -v CPU="$CPU" '/^[^:]*: metrc: .* matrix[[:space:]]/ {print $(NF-1) " " CPU; exit}'
    CPU=$B
    sleep $SLEEP_DURATION
    taskset -c $CPU stress-ng --matrix 1 --timeout $BENCH_DURATION --metrics-brief 2>&1 | awk -v CPU="$CPU" '/^[^:]*: metrc: .* matrix[[:space:]]/ {print $(NF-1) " " CPU; exit}'
done