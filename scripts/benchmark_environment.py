#!/usr/bin/env python3
"""Describe the Mac and Swift toolchain used for a benchmark report."""

import platform
import re
import subprocess


def environment_labels(swift_version, jobs):
    model = subprocess.check_output(["sysctl", "-n", "hw.model"], text=True).strip()
    memory = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True)) / 1024 ** 3
    xcode = subprocess.check_output(["xcodebuild", "-version"], text=True).splitlines()[0]
    swift_match = re.search(r"Swift version ([\d.]+)", swift_version)
    swift = swift_match.group(1) if swift_match else swift_version.splitlines()[0]
    return (f"{model} · {platform.machine()} · {memory:g} GB RAM",
            f"{xcode} · Swift {swift} · Debug · {jobs} jobs")
