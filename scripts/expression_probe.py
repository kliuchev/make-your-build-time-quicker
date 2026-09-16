#!/usr/bin/env python3
"""Measure the compiler's type-checking time for the complete example function."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import statistics
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {"before": ROOT / "Typecheck/ExpressionBefore.swift", "after": ROOT / "Typecheck/ExpressionAfter.swift"}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(command, log):
    start = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    seconds = time.perf_counter() - start
    log.with_suffix(".stdout.log").write_text(result.stdout, encoding="utf-8")
    log.with_suffix(".stderr.log").write_text(result.stderr, encoding="utf-8")
    write_json(log.with_suffix(".command.json"), {"argv": command, "cwd": str(ROOT),
               "wall_seconds": seconds, "returncode": result.returncode})
    if result.returncode:
        raise RuntimeError("Command failed: {}\n{}".format(log, result.stderr))
    return seconds, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("repeats must be positive")
    evidence = ROOT / "evidence/expression-probe"
    evidence.mkdir(parents=True, exist_ok=True)
    batch = evidence / (time.strftime("%Y%m%d-%H%M%S") + "-" + str(os.getpid()))
    batch.mkdir()
    compiler = subprocess.check_output(["xcrun", "--find", "swiftc"], text=True).strip()
    source_text = {key: path.read_text() for key, path in SOURCES.items()}
    snapshots = {}
    for variant, text in source_text.items():
        snapshot = batch / (variant + ".swift")
        snapshot.write_text(text)
        snapshots[variant] = snapshot
        if len(text.splitlines()) > 12 or max(map(len, text.splitlines())) > 48:
            raise RuntimeError("Example exceeds the slide's code size limit")
    samples = []
    for trial in range(1, args.repeats + 1):
        order = ("before", "after") if trial % 2 else ("after", "before")
        for variant in order:
            directory = batch / ("trial-{:02d}-{}".format(trial, variant))
            directory.mkdir()
            modules = directory / "modules"
            if modules.exists():
                raise RuntimeError("Expected a fresh module cache")
            command = [compiler, "-typecheck", "-module-cache-path", str(modules),
                       "-Xfrontend", "-debug-time-function-bodies", str(snapshots[variant])]
            seconds, _, output = run(command, directory / "typecheck")
            values = re.findall(r"(?m)^([\d.]+)ms\s[^\n]*global function[^\n]*\.value\(", output)
            if len(values) != 1:
                raise RuntimeError("Expected one timing for the complete value() body: " + output)
            sample = {"trial": trial, "variant": variant, "function_ms": float(values[0]),
                      "wall_seconds": seconds, "module_cache_empty_before": True,
                      "compiler_cache_enabled": False, "log_directory": str(directory)}
            samples.append(sample)
            print("Trial {} {}: whole value() body {} ms".format(trial, variant, sample["function_ms"]), flush=True)
    outputs = {}
    for variant in ("before", "after"):
        directory = batch / ("runtime-" + variant)
        directory.mkdir()
        main_source = directory / "main.swift"
        main_source.write_text('print(value().bitPattern)\n', encoding="utf-8")
        executable = directory / "verify"
        command = [compiler, "-module-cache-path", str(directory / "modules"), str(snapshots[variant]),
                   str(main_source), "-o", str(executable)]
        run(command, directory / "compile")
        _, stdout, _ = run([str(executable)], directory / "execute")
        outputs[variant] = stdout.strip()
    if outputs["before"] != outputs["after"]:
        raise RuntimeError("Runtime Double bit patterns differ")
    values = {variant: [sample["function_ms"] for sample in samples if sample["variant"] == variant]
              for variant in ("before", "after")}
    report = {"method": "whole-function-typechecking-v1", "date": time.strftime("%Y-%m-%d"),
              "python": platform.python_version(), "machine": platform.platform(),
              "swift": subprocess.run([compiler, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True).stdout.strip(),
              "repeats": args.repeats, "samples": samples,
              "medians": {variant + "_ms": statistics.median(value) for variant, value in values.items()},
              "ranges_ms": {variant: [min(value), max(value)] for variant, value in values.items()},
              "source_paths": {key: str(value) for key, value in SOURCES.items()},
              "source_snapshots": {key: str(value) for key, value in snapshots.items()},
              "source_text": source_text,
              "source_sha256": {key: hashlib.sha256(value.encode()).hexdigest() for key, value in source_text.items()},
              "outputs_equal": True, "double_bit_patterns": outputs, "batch": str(batch),
              "notes": ["The reported milliseconds come from -debug-time-function-bodies for the complete value() body, not the slowest subexpression.",
                        "The only source change is the explicit Double annotation on the local x variable.",
                        "Both functions are independently compiled and executed; their Double bit patterns match.",
                        "Each timing sample starts a fresh swiftc process with a new private module cache. Compiler caching is disabled.",
                        "Order alternates across trials. SDK/toolchain prebuilts and OS page cache remain available.",
                        "These are small-function type-checking timings, not complete application build speedups."]}
    write_json(batch / "report.json", report)
    write_json(evidence / "report.json", report)
    print(json.dumps({"medians": report["medians"], "ranges_ms": report["ranges_ms"], "outputs_equal": True}, indent=2))
    print("Report: {}".format(evidence / "report.json"))
    return evidence / "report.json"


if __name__ == "__main__":
    main()
