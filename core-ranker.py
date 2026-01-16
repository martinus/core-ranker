#!/usr/bin/env python3
import os
import glob

# --- 0BSD License ---
# Permission to use, copy, modify, and/or distribute this software for any 
# purpose with or without fee is hereby granted.

def get_cpu_info():
    data = {}
    rank_files = glob.glob("/sys/devices/system/cpu/cpu[0-9]*/acpi_cppc/highest_perf")
    
    # Fallback if CPPC is missing (e.g. some Intel/Legacy)
    if not rank_files:
        logical_count = os.cpu_count()
        rank_files = [f"/sys/devices/system/cpu/cpu{i}/topology/core_id" for i in range(logical_count)]

    for path in rank_files:
        cpu_id = int(path.split('/')[-3].replace('cpu', ''))
        
        # Determine Rank (Performance Ranking)
        try:
            with open(path, 'r') as f:
                rank = int(f.read().strip())
        except: rank = 100

        # Determine SMT Status
        is_smt = False
        sibling_file = f"/sys/devices/system/cpu/cpu{cpu_id}/topology/thread_siblings_list"
        if os.path.exists(sibling_file):
            with open(sibling_file, 'r') as f:
                siblings = sorted([int(x) for x in f.read().strip().replace('-',',').split(',')])
                if cpu_id != siblings[0]:
                    is_smt = True
        
        data[cpu_id] = {'rank': rank, 'is_smt': is_smt}
    return data

def main():
    info = get_cpu_info()
    
    # SCORING LOGIC:
    # We want: Physical P > Physical E > SMT P > SMT E
    # We create a sort key: (is_smt, -rank)
    # This puts all Physical cores (is_smt=0) before all SMT cores (is_smt=1)
    # Within those groups, it sorts by performance rank.
    sorted_cpus = sorted(info.items(), key=lambda x: (x[1]['is_smt'], -x[1]['rank']))

    print(f"{'CPU ID':<8} | {'Rank':<6} | {'Status':<10} | {'Type'}")
    print("-" * 48)

    max_r = max(v['rank'] for v in info.values())
    min_r = min(v['rank'] for v in info.values())
    mid = min_r + (max_r - min_r) / 2

    for cpu_id, meta in sorted_cpus:
        c_type = "Performance" if meta['rank'] > mid else "Efficiency"
        status = "SMT/Log" if meta['is_smt'] else "Physical"
        print(f"cpu{cpu_id:<5} | {meta['rank']:<6} | {status:<10} | {c_type}")

    print("\nSorted list for taskset:")
    print(",".join(str(x[0]) for x in sorted_cpus))

if __name__ == "__main__":
    main()