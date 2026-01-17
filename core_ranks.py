#!/usr/bin/env python3

"""
A utility to print CPU topology and performance ranking information.

This script parses Linux sysfs and /proc/cpuinfo to display:
- CPU model, governor, and turbo status.
- Core rankings (performance order used by the scheduler).
- Sibling cores (SMT/Hyper-Threading pairs).
- Min and max frequencies per core group.

--- 0BSD License ---
Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.
"""

from dataclasses import dataclass
from pathlib import Path
import re


CPU_BASE = Path("/sys/devices/system/cpu")
POLICY_BASE = Path("/sys/devices/system/cpu/cpufreq/policy0")


@dataclass
class CpuInfo:
    """Generic CPU information"""

    model_name: str = "unknown"
    driver: str = "unknown"
    governor: str = "unknown"
    available_governors: tuple[str, ...] = ()
    boost: str = "unknown"

    def __str__(self) -> str:
        out = str()
        out += f"{self.model_name}"
        out += f"\nGovernor: {self.governor} ({', '.join(self.available_governors)})"
        out += f"\nDriver:   {self.driver}"
        out += f"\nTurbo:    {self.boost}"
        return out


@dataclass
class CoreInfo:
    """Information per CPU core"""

    rank: int = 0
    siblings: tuple[int, ...] = ()
    min_mhz: int = 0
    max_mhz: int = 0


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
    """Fetch CPU info data"""
    cpu_info = CpuInfo(model_name="unknown")

    # /proc/cpuinfo
    pattern = re.compile(r"([^:\t]*)\s*: (.*)")
    with Path("/proc/cpuinfo").open(encoding="utf8") as f:
        for line in f:
            m: re.Match[str] | None = pattern.match(line)

            # reads until empty line (no match, then next processor follows)
            if m is None:
                break

            match m.group(1):
                case "model name":
                    cpu_info.model_name = m.group(2).strip()

    if (boost := read_int(POLICY_BASE / "boost")) is not None:
        cpu_info.boost = "Enabled" if boost == 1 else "Disabled"
    elif (no_turbo := read_int(CPU_BASE / "intel_pstate/no_turbo")) is not None:
        cpu_info.boost = "Enabled" if no_turbo == 0 else "Disabled"

    if (governor := read_str(POLICY_BASE / "scaling_governor")) is not None:
        cpu_info.governor = governor.strip()

    if (governor := read_str(POLICY_BASE / "scaling_available_governors")) is not None:
        cpu_info.available_governors = tuple(
            [g.strip() for g in governor.strip().split(" ")]
        )

    if (driver := read_str(POLICY_BASE / "scaling_driver")) is not None:
        cpu_info.driver = driver.strip()
    return cpu_info


def get_core_cpus() -> list[CoreInfo]:
    """Creates a list of CoreInfo, where core_siblings is filled. rank is dummy value 0."""
    unique_cores = set()

    for cpu_dir in CPU_BASE.iterdir():
        if (
            threads_str := read_str(cpu_dir / "topology/thread_siblings_list")
        ) is not None:
            threads: list[int] = []
            for part in threads_str.strip().split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    threads.extend(range(start, end + 1))
                else:
                    threads.append(int(part))
            unique_cores.add(tuple(sorted(threads)))

    cores = [CoreInfo(siblings=cpus) for cpus in unique_cores]
    # sorts highest rank first, then ordered by siblings in increasing order"
    cores.sort(key=lambda core: (-core.rank, core.siblings))
    return cores


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


def get_min_max_frequencies(cpu_path: Path) -> tuple[int, ...]:
    """updates min and max frequency of each core"""
    min_mhz = 0
    max_mhz = 0
    if (freq := read_int(cpu_path / "cpufreq/cpuinfo_min_freq")) is not None:
        min_mhz = freq // 1000
    if (freq := read_int(cpu_path / "cpufreq/cpuinfo_max_freq")) is not None:
        max_mhz = freq // 1000

    return (min_mhz, max_mhz)


def update_cores(cores):
    """Updates per-core information, reading only the first sibling's information"""
    for core in cores:
        cpu_path = CPU_BASE / f"cpu{core.siblings[0]}"
        core.rank = get_rank(cpu_path)
        core.min_mhz, core.max_mhz = get_min_max_frequencies(cpu_path)


def cores_as_markdown(cores: list[CoreInfo]) -> str:
    """Prints a nice markdown table for the information of all cores"""
    out = str()
    out += "Rank | CPU IDs | MHz min | MHz max\n----:|:--------|--------:|--------:\n"
    for core in cores:
        siblings_str = ", ".join([f"{sibling:>2}" for sibling in core.siblings])
        out += (
            f"{core.rank:>4} |{siblings_str:>8} |{core.min_mhz:>8} |{core.max_mhz:>8}\n"
        )
    return out


def main() -> None:
    """Prints the full CPU information"""
    cpu_info: CpuInfo = get_cpu_info()

    cores: list[CoreInfo] = get_core_cpus()
    update_cores(cores)
    print(cpu_info)
    print()
    print(cores_as_markdown(cores))


if __name__ == "__main__":
    main()
