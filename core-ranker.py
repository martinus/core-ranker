#!/usr/bin/env python3
from dataclasses import dataclass
import os
from pathlib import Path
import re

# --- 0BSD License ---
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.

CPU_BASE = Path("/sys/devices/system/cpu")
POLICY_BASE = Path("/sys/devices/system/cpu/cpufreq/policy0")


@dataclass
class CpuInfo:
    model_name: str = "unknown"
    driver: str = "unknown"
    governor: str = "unknown"
    available_governors: tuple[str, ...] = ()
    boost: str = "unknown"


@dataclass
class CoreInfo:
    rank: int
    siblings: tuple[int, ...]
    min_MHz: int
    max_MHz: int


def read_str(path: Path) -> str | None:
    """Read a string from a sysfs file, returning None on failure."""
    try:
        return path.read_text()
    except OSError:
        return None


def read_int(path: Path) -> int | None:
    """Read an integer from a sysfs file, returning None on failure."""
    try:
        if (data := read_str(path)) is not None:
            return int(data.strip())
    except ValueError:
        pass

    return None


def get_cpu_info() -> CpuInfo:
    cpu_info = CpuInfo(model_name="unknown")

    # /proc/cpuinfo
    pattern = re.compile(r"([^:\t]*)\s*: (.*)")
    with open("/proc/cpuinfo") as f:
        for line in f:
            m = pattern.match(line)

            # reads until empty line (no match, then next processor follows)
            if m == None:
                break

            match (m.group(1)):
                case "model name":
                    cpu_info.model_name = m.group(2).strip()

    if (boost := read_int(POLICY_BASE / "boost")) is not None:
        cpu_info.boost = "Enabled" if boost == 1 else "Disabled"

    if (governor := read_str(POLICY_BASE / "scaling_governor")) is not None:
        cpu_info.governor = governor.strip()

    if (governor := read_str(POLICY_BASE / "scaling_available_governors")) is not None:
        cpu_info.available_governors = tuple([g.strip() for g in governor.split(" ")])

    if (driver := read_str(POLICY_BASE / "scaling_driver")) is not None:
        cpu_info.driver = driver.strip()
    return cpu_info


def get_core_cpus() -> list[CoreInfo]:
    """Creates a list of CoreInfo, where core_siblings is filled. rank is dummy value 0."""
    base_path = "/sys/devices/system/cpu/"
    unique_cores = set()
    cpu_dirs = [d for d in os.listdir(base_path) if re.match(r"cpu\d+", d)]

    for cpu_dir in cpu_dirs:
        path = os.path.join(base_path, cpu_dir, "topology/thread_siblings_list")
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read().strip()
                threads: list[int] = []
                for part in content.split(","):
                    if "-" in part:
                        start, end = map(int, part.split("-"))
                        threads.extend(range(start, end + 1))
                    else:
                        threads.append(int(part))
                unique_cores.add(tuple(sorted(threads)))
    ret: list[CoreInfo] = []
    for cpus in list(unique_cores):
        ret.append(CoreInfo(rank=0, siblings=cpus, min_MHz=0, max_MHz=0))
    return ret


def sort(cores: list[CoreInfo]) -> None:
    """Sorts highest rank first, then ordered by siblings in increasing order"""
    cores.sort(key=lambda core: (-core.rank, core.siblings))


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


def update_ranks(cores: list[CoreInfo]) -> None:
    for core in cores:
        cpu_path = CPU_BASE / f"cpu{core.siblings[0]}"
        core.rank = get_rank(cpu_path)


def update_frequencies(cores: list[CoreInfo]) -> None:
    for core in cores:
        cpu_path = CPU_BASE / f"cpu{core.siblings[0]}"
        if (freq := read_int(cpu_path / "cpufreq/cpuinfo_min_freq")) is not None:
            core.min_MHz = freq // 1000
        if (freq := read_int(cpu_path / "cpufreq/cpuinfo_max_freq")) is not None:
            core.max_MHz = freq // 1000


def cores_as_markdown(cores: list[CoreInfo]) -> str:
    out = str()
    out += "Rank | CPU IDs | MHz min | MHz max\n----:|:--------|--------:|--------:\n"
    for core in cores:
        siblings_str = ", ".join([f"{sibling:>2}" for sibling in core.siblings])
        out += (
            f"{core.rank:>4} |{siblings_str:>8} |{core.min_MHz:>8} |{core.max_MHz:>8}\n"
        )
    return out


def main() -> None:
    cpu_info: CpuInfo = get_cpu_info()
    print(f"{cpu_info.model_name}")
    print(f"Governor: {cpu_info.governor} ({", ".join(cpu_info.available_governors)})")
    print(f"Driver:   {cpu_info.driver}")
    print(f"Turbo:    {cpu_info.boost}")
    print()

    cores: list[CoreInfo] = get_core_cpus()
    update_ranks(cores)
    update_frequencies(cores)
    sort(cores)
    print(f"{cores_as_markdown(cores)}")


if __name__ == "__main__":
    main()
