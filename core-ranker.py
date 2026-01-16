#!/usr/bin/env python3
from pathlib import Path

# --- 0BSD License ---
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.

CPU_BASE = Path("/sys/devices/system/cpu")


def read_int(path: Path) -> int | None:
    """Read an integer from a sysfs file, returning None on failure."""
    try:
        return int(path.read_text().strip())
    except (OSError, ValueError):
        return None


def get_rank(cpu_path: Path) -> int:
    """Determine CPU performance rank from various sysfs sources."""
    # Try AMD CPPC
    if (rank := read_int(cpu_path / "acpi_cppc/highest_perf")) is not None:
        return rank
    # Try Intel ITMT score
    if (rank := read_int(cpu_path / "topology/itmt_score")) is not None:
        return rank
    # Try Intel base frequency (convert kHz to MHz)
    if (freq := read_int(cpu_path / "cpufreq/base_frequency")) is not None:
        return freq // 1000
    # Fallback to core_id
    if (rank := read_int(cpu_path / "topology/core_id")) is not None:
        return rank
    return 100


def is_smt_thread(cpu_path: Path, cpu_id: int) -> bool:
    """Check if this CPU is an SMT/Hyperthread (not the first thread of its core)."""
    sibling_file = cpu_path / "topology/thread_siblings_list"
    if not sibling_file.exists():
        return False
    try:
        siblings = sorted(
            int(x) for x in sibling_file.read_text().strip().replace("-", ",").split(",")
        )
        return cpu_id != siblings[0]
    except (OSError, ValueError):
        return False


def get_cpu_info() -> dict[int, dict]:
    """Gather rank and SMT status for all CPUs."""
    import os
    data = {}
    for cpu_id in range(os.cpu_count() or 0):
        cpu_path = CPU_BASE / f"cpu{cpu_id}"
        data[cpu_id] = {
            "rank": get_rank(cpu_path),
            "is_smt": is_smt_thread(cpu_path, cpu_id),
        }
    return data


def main():
    info = get_cpu_info()

    # Physical cores first, then SMT/Hyperthreads; within groups, highest rank first
    sorted_cpus = sorted(info.items(), key=lambda x: (x[1]["is_smt"], -x[1]["rank"]))

    print(f"{'cpuid':<4} | {'Rank':<4} | {'Status'}")
    print("------+------+----------")
    
    for cpu_id, meta in sorted_cpus:
        status = "SMT/HT" if meta["is_smt"] else "Physical"
        print(f"{cpu_id:>5} | {meta['rank']:>4} | {status}")

    print("\nSorted list for taskset:")
    print(",".join(str(x[0]) for x in sorted_cpus))


if __name__ == "__main__":
    main()
