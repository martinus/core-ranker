#!/bin/bash
taskset -c 1 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "A " $(NF-1); exit}'
taskset -c 8 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "B " $(NF-1); exit}'
taskset -c 1 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "A " $(NF-1); exit}'
taskset -c 8 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "B " $(NF-1); exit}'
taskset -c 1 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "A " $(NF-1); exit}'
taskset -c 8 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "B " $(NF-1); exit}'
taskset -c 1 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "A " $(NF-1); exit}'
taskset -c 8 stress-ng --cpu 1 --cpu-method fft --timeout 10s --metrics-brief 2>&1 | awk '/^[^:]*: metrc: .* cpu[[:space:]]/ {print "B " $(NF-1); exit}'
