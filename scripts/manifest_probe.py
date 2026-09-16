#!/usr/bin/env python3
"""Measure a minimal Swift manifest, separating compilation from evaluation."""

import argparse
import json
import os
from pathlib import Path
import platform
import re
import statistics
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = '// swift-tools-version: 6.0\nimport PackageDescription\n\nlet package = Package(name: "Minimal")\n'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(command, directory, environment, log):
    start = time.perf_counter()
    result = subprocess.run(command, cwd=directory, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    seconds = time.perf_counter() - start
    log.with_suffix(".stdout.log").write_text(result.stdout, encoding="utf-8")
    log.with_suffix(".stderr.log").write_text(result.stderr, encoding="utf-8")
    write_json(log.with_suffix(".command.json"), {"argv": command, "cwd": str(directory),
               "seconds": seconds, "returncode": result.returncode})
    if result.returncode:
        raise RuntimeError("Command failed: {}\n{}".format(log, result.stderr))
    return seconds, result.stdout, result.stderr


def prepare(directory):
    directory.mkdir(parents=True)
    project = directory / "project"
    project.mkdir()
    (project / "Package.swift").write_text(MANIFEST, encoding="utf-8")
    state = directory / "state"
    paths = {name: state / name for name in ("build", "package-cache", "modules", "config", "security", "tmp")}
    if any(path.exists() for path in paths.values()):
        raise RuntimeError("Fresh-cache precondition failed")
    env = os.environ.copy()
    overrides = {"SWIFTPM_MODULECACHE_OVERRIDE": str(paths["modules"]),
                 "CLANG_MODULE_CACHE_PATH": str(paths["modules"]), "TMPDIR": str(paths["tmp"]) + "/"}
    paths["tmp"].mkdir(parents=True)
    env.update(overrides)
    write_json(directory / "environment.json", {"overrides": overrides,
               "all_cache_paths_absent_before": True, "paths": {key: str(value) for key, value in paths.items()}})
    return project, paths, env


def swiftpm_probe(directory, swift):
    project, paths, env = prepare(directory)
    command = [swift, "package", "--package-path", str(project), "--scratch-path", str(paths["build"]),
               "--cache-path", str(paths["package-cache"]), "--manifest-cache", "local",
               "--config-path", str(paths["config"]), "--security-path", str(paths["security"]),
               "--verbose", "dump-package"]
    seconds, output, diagnostics = run(command, project, env, directory / "dump-package")
    if json.loads(output)["name"] != "Minimal":
        raise RuntimeError("Unexpected SwiftPM manifest output")
    target = re.search(r"(?:^|\s)-target\s+(\S+)", diagnostics)
    return {"seconds": seconds, "all_cache_paths_absent_before": True,
            "target": target.group(1) if target else None, "log_directory": str(directory)}


def direct_probe(directory, compiler, runtime, sdk, target):
    project, paths, env = prepare(directory)
    executable = directory / "manifest"
    command = [compiler, "-L", str(runtime), "-lPackageDescription", "-Xlinker", "-rpath", "-Xlinker", str(runtime),
               "-target", target, "-swift-version", "6", "-I", str(runtime), "-sdk", sdk,
               "-package-description-version", "6.0.0", "-module-cache-path", str(paths["modules"]),
               str(project / "Package.swift"), "-o", str(executable)]
    compile_seconds, _, _ = run(command, project, env, directory / "compile")
    run_seconds, output, _ = run([str(executable), "-fileno", "1"], project, env, directory / "evaluate")
    if json.loads(output)["package"]["name"] != "Minimal":
        raise RuntimeError("Unexpected direct manifest output")
    return {"compile_seconds": compile_seconds, "evaluate_seconds": run_seconds,
            "compile_plus_evaluate_seconds": compile_seconds + run_seconds,
            "all_cache_paths_absent_before": True, "log_directory": str(directory)}


def summary(values):
    return {"median_seconds": statistics.median(values), "range_seconds": [min(values), max(values)], "samples_seconds": values}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("repeats must be positive")
    evidence = ROOT / "evidence/manifest-probe"
    evidence.mkdir(parents=True, exist_ok=True)
    batch = evidence / (time.strftime("%Y%m%d-%H%M%S") + "-" + str(os.getpid()))
    batch.mkdir()
    swift = subprocess.check_output(["xcrun", "--find", "swift"], text=True).strip()
    compiler = subprocess.check_output(["xcrun", "--find", "swiftc"], text=True).strip()
    runtime = Path(compiler).parent.parent / "lib/swift/pm/ManifestAPI"
    sdk = subprocess.check_output(["xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True).strip()
    reference = swiftpm_probe(batch / "reference-command", swift)
    target = reference["target"]
    if not target:
        raise RuntimeError("Could not extract SwiftPM's manifest target triple")
    samples = []
    for trial in range(1, args.repeats + 1):
        sample = {"trial": trial}
        order = ("swiftpm", "direct") if trial % 2 else ("direct", "swiftpm")
        for method in order:
            directory = batch / ("trial-{:02d}".format(trial)) / method
            sample[method] = (swiftpm_probe(directory, swift) if method == "swiftpm"
                              else direct_probe(directory, compiler, runtime, sdk, target))
        samples.append(sample)
        print("Trial {}: dump-package {:.4f}s; compile {:.4f}s; JSON execution {:.4f}s".format(
              trial, sample["swiftpm"]["seconds"], sample["direct"]["compile_seconds"], sample["direct"]["evaluate_seconds"]), flush=True)
    version = subprocess.run([swift, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True).stdout.strip()
    report = {"method": "minimal-manifest-fresh-caches-v1", "date": time.strftime("%Y-%m-%d"),
              "python": platform.python_version(), "machine": platform.platform(), "swift": version,
              "manifest_source": MANIFEST, "swift_tools_version": "6.0", "runtime": str(runtime), "sdk": sdk,
              "target": target, "repeats": args.repeats, "samples": samples, "batch": str(batch),
              "swiftpm_end_to_end": summary([value["swiftpm"]["seconds"] for value in samples]),
              "direct_compile": summary([value["direct"]["compile_seconds"] for value in samples]),
              "direct_evaluate": summary([value["direct"]["evaluate_seconds"] for value in samples]),
              "direct_compile_plus_evaluate": summary([value["direct"]["compile_plus_evaluate_seconds"] for value in samples]),
              "notes": ["Each measurement uses fresh private manifest, build, package and compiler module cache paths.",
                        "The untimed reference run discovers SwiftPM's exact manifest deployment target; its logs are retained.",
                        "swift package dump-package includes CLI startup, manifest compilation/evaluation and package-model output.",
                        "Direct swiftc compilation includes compiling and linking the manifest executable. Direct JSON execution is a separate unsandboxed process; it is not the complete SwiftPM loader.",
                        "No package target sources are built. The manifest has only a package name, with no products, targets or dependencies.",
                        "OS page cache is not purged; SDK and toolchain prebuilts remain available.",
                        "Do not multiply an isolated per-process median by package count to claim a guaranteed total build wall time. Packages can share module caches and overlap work within one build."]}
    write_json(batch / "report.json", report)
    write_json(evidence / "report.json", report)
    print(json.dumps({key: report[key] for key in ("swiftpm_end_to_end", "direct_compile", "direct_evaluate")}, indent=2))
    print("Report: {}".format(evidence / "report.json"))
    return evidence / "report.json"


if __name__ == "__main__":
    main()
