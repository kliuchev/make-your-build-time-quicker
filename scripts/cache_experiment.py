#!/usr/bin/env python3
"""Compare full SwiftPM builds while reusing only the compiler CAS."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import statistics
import subprocess
import time

from package_variants import create_feature_merged


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = (
    ("baseline", "Baseline", 101),
    ("feature", "FeatureMerged", 35),
    ("single", "Consolidated", 1),
    ("optimized", "Optimized", 1),
)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest_sources(project):
    values = {}
    for source in sorted(project.rglob("*.swift")):
        if source.name != "Package.swift":
            values[source.stem] = hashlib.sha256(source.read_bytes()).hexdigest()
    return values


def prepare_templates(batch):
    templates = batch / "templates"
    for name in ("Baseline", "Optimized"):
        shutil.copytree(ROOT / name, templates / name,
                        ignore=shutil.ignore_patterns(".build", ".swiftpm", ".DS_Store"))
    create_feature_merged(templates / "Baseline", templates / "FeatureMerged")
    shutil.copytree(templates / "Optimized", templates / "Consolidated")
    shutil.copyfile(
        templates / "Baseline/Packages/Feature01Presentation/Sources/Feature01Presentation/Feature01Presentation.swift",
        templates / "Consolidated/Sources/Feature01Presentation/Feature01Presentation.swift",
    )
    sources = {name: digest_sources(templates / name) for _, name, _ in VARIANTS}
    if not sources["Baseline"] == sources["FeatureMerged"] == sources["Consolidated"]:
        raise RuntimeError("Package variants must contain identical Swift target sources")
    differences = [key for key in sources["Consolidated"]
                   if sources["Consolidated"][key] != sources["Optimized"].get(key)]
    if differences != ["Feature01Presentation"]:
        raise RuntimeError(f"Unexpected optimized source differences: {differences}")
    if any(len(value) != 101 for value in sources.values()):
        raise RuntimeError("Expected 101 Swift target source files")
    write_json(batch / "source-audit.json", sources)
    return templates


def capture(command, project, environment, log):
    start = time.perf_counter()
    first_build_message = None
    build_complete_message = None
    with log.open("w", encoding="utf-8") as stream:
        process = subprocess.Popen(command, cwd=project, env=environment, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in process.stdout:
            stream.write(line)
            if first_build_message is None and "Building for debugging" in line:
                first_build_message = time.perf_counter() - start
            if "Build complete!" in line:
                build_complete_message = time.perf_counter() - start
        code = process.wait()
    seconds = time.perf_counter() - start
    output = log.read_text(encoding="utf-8")
    if code:
        raise RuntimeError(f"Build failed ({code}); see {log}\n{output[-3500:]}")
    return seconds, first_build_message, build_complete_message, output


def run_sample(directory, project, trial, identifier, manifests, mode, jobs, backend="swiftbuild"):
    state = directory / "state"
    cas = directory / "cas"
    evidence = directory / mode
    evidence.mkdir(exist_ok=True)
    recover = (evidence / "timing.json").exists() and (evidence / "build.log").exists() and state.exists()
    recorded = json.loads((evidence / "command.json").read_text()) if recover else None
    if state.exists() and not recover:
        # Only this experiment's generated state is removed; source and CAS stay put.
        if state.parent != directory or not directory.is_relative_to(ROOT / ".benchmark-runs"):
            raise RuntimeError("Refusing to remove an unexpected state directory")
        shutil.rmtree(state)
    if mode == "cache_fill" and cas.exists() and not recover:
        # Swift Build may initialize CAS metadata even when compilation caching is off.
        if cas.parent != directory or not directory.is_relative_to(ROOT / ".benchmark-runs"):
            raise RuntimeError("Refusing to remove an unexpected CAS directory")
        shutil.rmtree(cas)
    paths = {key: state / value for key, value in {
        "scratch": "build", "package_cache": "package-cache", "config": "config",
        "security": "security", "manifest_modules": "manifest-modules",
        "target_modules": "target-modules", "temporary": "tmp",
    }.items()}
    before = recorded["before"] if recover else {key: {"path": str(path), "existed": path.exists()} for key, path in paths.items()}
    if any(value["existed"] for value in before.values()):
        raise RuntimeError("Expected empty artifact, manifest, and module cache paths")
    cas_files_before = recorded["cas_files_before"] if recover else (sum(1 for path in cas.rglob("*") if path.is_file()) if cas.exists() else 0)
    if mode == "cache_fill" and cas_files_before:
        raise RuntimeError("Cache fill must start with an empty CAS")
    if mode == "cache_hit" and not cas_files_before:
        raise RuntimeError("Cache replay requires a populated CAS")
    paths["temporary"].mkdir(parents=True, exist_ok=True)
    overrides = {
        "SWIFTPM_MODULECACHE_OVERRIDE": str(paths["manifest_modules"]),
        "CLANG_MODULE_CACHE_PATH": str(paths["manifest_modules"]),
        "TMPDIR": str(paths["temporary"]) + "/",
    }
    if backend == "swiftbuild":
        overrides.update({
            "EnableSwiftCachingByDefault": "YES" if mode != "cold_off" else "NO",
            "EnableClangCachingByDefault": "YES" if mode != "cold_off" else "NO",
            "CompilationCachingCASPath": str(cas),
        })
    environment = os.environ.copy()
    environment.update(overrides)
    command = [
        "swift", "build", "--build-system", backend, "--configuration", "debug",
        "-debug-info-format", "none", "--package-path", str(project),
        "--scratch-path", str(paths["scratch"]), "--cache-path", str(paths["package_cache"]),
        "--manifest-cache", "local", "--config-path", str(paths["config"]),
        "--security-path", str(paths["security"]), "--jobs", str(jobs), "--verbose",
    ]
    flags = ["-module-cache-path", str(paths["target_modules"])]
    if backend == "native":
        flags += ["-explicit-module-build"]
    if mode in ("cache_fill", "cache_hit"):
        if backend == "native":
            flags += ["-cache-compile-job", "-cas-path", str(cas)]
        flags += ["-Rcache-compile-job"]
    for flag in flags:
        command += ["-Xswiftc", flag]
    command_record = {"argv": command, "cwd": str(project), "env_overrides": overrides,
                      "before": before, "cas_files_before": cas_files_before}
    if recover and command_record != recorded:
        raise RuntimeError("Saved successful command differs; refusing to reuse its timing")
    write_json(evidence / "command.json", command_record)
    print(f"Trial {trial}: {identifier} / {mode}; fresh build, manifest and module caches", flush=True)
    if recover:
        timing = json.loads((evidence / "timing.json").read_text())
        seconds, marker, complete_marker = (timing[key] for key in
                                           ("seconds", "first_build_message_seconds", "build_complete_message_seconds"))
        output = (evidence / "build.log").read_text()
        print("  Revalidating the saved completed build; keeping its measured wall time", flush=True)
    else:
        seconds, marker, complete_marker, output = capture(command, project, environment, evidence / "build.log")
    write_json(evidence / "timing.json", {"seconds": seconds, "first_build_message_seconds": marker,
               "build_complete_message_seconds": complete_marker})
    # Concurrent cache remarks can split verbose commands and progress labels.
    command_output = re.sub(r"Cache (?:hit|miss)\r?\n", "", output)
    command_output = re.sub(r"<unknown>:0: (?:remark|warning|note):[^\n]*\n", "", command_output)
    cache_hits = output.count("cache hit for input file")
    cache_misses = output.count("cache miss for input file")
    cacheable_tasks = 202 if mode != "cold_off" else 0
    cache_summaries = re.findall(r"info: (\d+) hits / (\d+) cacheable tasks", output)
    if backend == "swiftbuild":
        compile_jobs = len(set(re.findall(r"\bCompile (\w+) \([^)]+\)", command_output)))
        emit_module_jobs = len(set(re.findall(r"\bEmitting module for (\w+)", command_output)))
        if mode != "cold_off":
            if len(cache_summaries) != 1:
                raise RuntimeError(f"Expected one Swift Build cache summary, got {cache_summaries}")
            cache_hits, cacheable_tasks = map(int, cache_summaries[0])
            cache_misses = cacheable_tasks - cache_hits
    else:
        compile_jobs = len(re.findall(r"(?m)^.*swift-frontend -frontend -c ", output))
        emit_module_jobs = len(re.findall(r"(?m)^.*swift-frontend -frontend -emit-module ", output))
    if (compile_jobs, emit_module_jobs) != (101, 101):
        raise RuntimeError(f"Expected 101 compile and 101 emit-module jobs, got {compile_jobs}, {emit_module_jobs}")
    if mode == "cold_off" and (cache_hits or cache_misses or "-cache-compile-job" in output):
        raise RuntimeError("Compiler cache unexpectedly active in cache-disabled build")
    if mode == "cache_fill" and (cache_hits != 0 or cache_misses < 202):
        raise RuntimeError(f"Cache fill expected misses for every target job; got {cache_hits} / {cache_misses}")
    if mode == "cache_hit" and (cache_hits < 202 or cache_misses != 0):
        raise RuntimeError(f"Cache replay expected hits for every target job; got {cache_hits} / {cache_misses}")
    actual_module_paths = sorted(set(re.findall(
        r"-(?:module-cache-path|sdk-module-cache-path|clang-scanner-module-cache-path)\s+(\S+)", command_output)))
    valid_module_paths = [path for path in actual_module_paths if Path(path.strip("'\"")).is_relative_to(state)]
    truncated_module_tokens = [path for path in actual_module_paths if path not in valid_module_paths
                               and any(valid.startswith(path) for valid in valid_module_paths)]
    if not valid_module_paths or any(path not in valid_module_paths + truncated_module_tokens for path in actual_module_paths):
        raise RuntimeError(f"Module caches escaped private state: {actual_module_paths}")
    actual_module_paths = valid_module_paths
    actual_cas_paths = sorted(set(re.findall(r"-cas-path\s+(\S+)", command_output)))
    if mode != "cold_off" and any(not Path(path.strip("'\"")).is_relative_to(cas) for path in actual_cas_paths):
        raise RuntimeError(f"Unexpected CAS path: {actual_cas_paths}")
    replay_paths = re.findall(r"replay output file '([^']+)'", output)
    replay_objects = sorted(set(path for path in replay_paths if path.endswith(".o")))
    replay_modules = sorted(set(path for path in replay_paths if path.endswith(".swiftmodule")))
    arenas = []
    if backend == "swiftbuild":
        object_outputs = list((paths["scratch"] / "out/Intermediates.noindex").glob("**/Objects-normal/*/*.o"))
        module_outputs = list((paths["scratch"] / "out/Intermediates.noindex").glob("**/Objects-normal/*/*.swiftmodule"))
        if (len(object_outputs), len(module_outputs)) != (101, 101):
            raise RuntimeError("Fresh build must produce all 101 object files and 101 Swift modules")
        requests = list(paths["scratch"].rglob("build-request.json"))
        if not requests:
            raise RuntimeError("Missing Swift Build arena evidence")
        for number, request_path in enumerate(requests):
            request = json.loads(request_path.read_text())
            arena = request["parameters"]["arenaInfo"]
            settings = request["parameters"]["overrides"]["synthesized"]["table"]
            module_setting = settings.get("MODULE_CACHE_DIR")
            module_flag = f"-module-cache-path {paths['target_modules']}"
            if module_setting != str(paths["target_modules"]) and module_flag not in settings.get("OTHER_SWIFT_FLAGS", ""):
                raise RuntimeError("Serialized module cache build setting differs from private path")
            if any(not Path(arena[key]).is_relative_to(paths["scratch"])
                   for key in ("derivedDataPath", "buildIntermediatesPath", "buildProductsPath")):
                raise RuntimeError("DerivedData arena escaped fresh private scratch")
            arenas.append(arena)
            shutil.copyfile(request_path, evidence / f"build-request-{number}.json")
        if mode == "cache_hit" and (len(replay_objects), len(replay_modules)) != (101, 101):
            raise RuntimeError("CAS replay must restore all 101 object and 101 module outputs")
        binaries = list((paths["scratch"] / "out/Products/Debug").glob("Demo"))
    else:
        binaries = list(paths["scratch"].glob("*/debug/Demo"))
    if len(binaries) != 1:
        raise RuntimeError(f"Expected one Demo executable, got {binaries}")
    program_output = subprocess.check_output([str(binaries[0])])
    (evidence / "stdout.txt").write_bytes(program_output)
    engine = re.search(r"Build complete! \(([\d.]+)(?: secs|s)\)", output)
    engine_seconds = float(engine.group(1)) if engine else None
    result = {
        "trial": trial, "id": identifier, "mode": mode, "manifests": manifests,
        "library_targets": 100, "total_targets": 101, "seconds": seconds,
        "first_build_message_seconds": marker, "engine_reported_seconds": engine_seconds,
        "build_complete_message_seconds": complete_marker,
        "post_complete_seconds": seconds - complete_marker if complete_marker is not None else None,
        "outside_engine_estimate_seconds": seconds - engine_seconds if engine_seconds is not None else None,
        "cache_hits": cache_hits, "cache_misses": cache_misses,
        "cacheable_tasks": cacheable_tasks,
        "compile_jobs": compile_jobs, "emit_module_jobs": emit_module_jobs,
        "output_sha256": hashlib.sha256(program_output).hexdigest(),
        "audit": {"all_artifact_roots_absent_before": True, "roots_before": before,
                  "only_reused_cache": "compiler CAS" if mode == "cache_hit" else None,
                  "cas_files_before": cas_files_before, "module_cache_paths": actual_module_paths,
                  "truncated_verbose_module_path_tokens": truncated_module_tokens,
                  "cas_paths": actual_cas_paths, "build_system": backend,
                  "derived_data_used": backend == "swiftbuild", "derived_data_arenas": arenas,
                  "replayed_object_outputs": replay_objects, "replayed_module_outputs": replay_modules,
                  "scratch_path": str(paths["scratch"]),
                  "source_path": str(project), "log_path": str(evidence / "build.log"),
                  "command_path": str(evidence / "command.json")},
    }
    write_json(evidence / "result.json", result)
    print(f"  {seconds:.2f} s; {compile_jobs} compile + {emit_module_jobs} module jobs; "
          f"{cache_hits} hits / {cache_misses} misses", flush=True)
    return result


def aggregate(samples):
    results = []
    for identifier, _, _ in VARIANTS:
        for mode in ("cold_off", "cache_fill", "cache_hit"):
            group = [sample for sample in samples if sample["id"] == identifier and sample["mode"] == mode]
            if not group:
                continue
            seconds = [sample["seconds"] for sample in group]
            results.append({"id": identifier, "mode": mode, "repeats": len(group),
                            "median_seconds": statistics.median(seconds),
                            "range_seconds": [min(seconds), max(seconds)],
                            "engine_median_seconds": statistics.median(sample["engine_reported_seconds"] for sample in group),
                            "outside_engine_median_seconds": statistics.median(sample["outside_engine_estimate_seconds"] for sample in group),
                            "first_build_message_median_seconds": statistics.median(sample["first_build_message_seconds"] for sample in group),
                            "cache_hits_each": [sample["cache_hits"] for sample in group],
                            "cache_misses_each": [sample["cache_misses"] for sample in group]})
    return results


def typecheck_probes(batch):
    results = []
    directory = batch / "probes"
    directory.mkdir()
    for trial in range(1, 4):
        for name in ("Baseline", "Optimized"):
            modules = directory / f"modules-{name}-{trial}"
            command = ["swiftc", "-typecheck", "-module-cache-path", str(modules),
                       "-Xfrontend", "-debug-time-expression-type-checking",
                       str(ROOT / "Typecheck" / f"{name}.swift")]
            log = directory / f"typecheck-{name.lower()}-{trial}.log"
            seconds, _, _, output = capture(command, ROOT, os.environ.copy(), log)
            times = [float(value) for value in re.findall(r"(?m)^([\d.]+)ms\s", output)]
            value = {"trial": trial, "variant": name.lower(), "seconds": seconds,
                     "slowest_expression_ms": max(times), "module_cache_empty_before": True,
                     "argv": command, "log_path": str(log)}
            write_json(log.with_suffix(".json"), value)
            results.append(value)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--build-system", choices=["swiftbuild", "native"], default="swiftbuild")
    parser.add_argument("--variants", nargs="+", choices=[value[0] for value in VARIANTS])
    parser.add_argument("--workload", choices=["current"], default="current")
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    if args.repeats < 1 or args.jobs < 1:
        parser.error("repeats and jobs must be positive")
    batch = args.resume.resolve() if args.resume else ROOT / ".benchmark-runs" / f"cache-research-matrix-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    if not batch.is_relative_to(ROOT / ".benchmark-runs") or not batch.name.startswith("cache-research-"):
        parser.error("Result directory must be a private cache-research directory")
    if not args.resume:
        batch.mkdir(parents=True)
    print(f"Report directory: {batch}", flush=True)
    templates = batch / "templates" if args.resume else prepare_templates(batch)
    swift = subprocess.run(["swift", "--version"], capture_output=True, text=True, check=True).stdout.strip()
    report = {"method": f"full-graph-{args.build_system}-cas-v2", "date": time.strftime("%Y-%m-%d"),
              "machine": platform.platform(), "swift": swift, "jobs": args.jobs, "repeats": args.repeats,
              "build_system": args.build_system, "configuration": "Debug (-Onone), no DWARF",
              "explicit_modules": True, "os_page_cache_purged": False,
              "notes": ["All samples rebuild from empty scratch, package manifest and compiler module cache paths.",
                        "Cache hit samples preserve only CAS; source and output paths remain identical to their cache fill.",
                        "Cache-off and cache-on use identical target graphs, sources, optimization and debug settings.",
                        "Cache-enabled builds also pass -Rcache-compile-job to record cache diagnostics; that instrumentation is included in wall time.",
                        "The project has 101 object compilations and 101 Swift module emissions; SDK jobs may also be cacheable.",
                        "Manifest evaluation, dependency scanning and linking still run during CAS replay.",
                        "Total process wall time is the primary comparison, including work after the Build complete message.",
                        "The Build complete timer and first output marker have backend-specific scopes; neither is pure compiler time."],
              "samples": [], "aggregates": []}
    if args.build_system == "native":
        report["notes"].append("Native backend is deprecated in the tested Swift 6.4 toolchain.")
    else:
        report["notes"].append("Source-backed Swift Build environment switches activate SWIFT_ENABLE_COMPILE_CACHE and CLANG_ENABLE_COMPILE_CACHE; CAS has an explicit private path.")
    if args.resume:
        saved = json.loads((batch / "report.json").read_text())
        for key in ("swift", "jobs", "repeats", "build_system"):
            if saved[key] != report[key]:
                parser.error(f"Resume configuration differs: {key}")
        report = saved
    selected = [value for value in VARIANTS if not args.variants or value[0] in args.variants]
    for trial in range(1, args.repeats + 1):
        order = selected if trial % 2 else list(reversed(selected))
        for identifier, name, manifests in order:
            directory = batch / f"trial-{trial:02d}" / identifier
            project = directory / "project"
            if not project.exists():
                shutil.copytree(templates / name, project)
            modes = ("cold_off", "cache_fill", "cache_hit") if identifier in ("single", "optimized") else ("cold_off",)
            for mode in modes:
                if any(value["trial"] == trial and value["id"] == identifier and value["mode"] == mode
                       for value in report["samples"]):
                    continue
                report["samples"].append(run_sample(directory, project, trial, identifier, manifests, mode, args.jobs, args.build_system))
                report["aggregates"] = aggregate(report["samples"])
                write_json(batch / "report.json", report)
    hashes = {sample["output_sha256"] for sample in report["samples"]}
    if len(hashes) != 1:
        raise RuntimeError("Demo output differs between samples")
    report["outputs_equal"] = True
    if "typecheck_probes" not in report:
        report["typecheck_probes"] = typecheck_probes(batch)
    write_json(batch / "report.json", report)
    lines = ["# Full project compiler cache experiment", "", f"{swift}; {report['configuration']}; {args.jobs} jobs.",
             "", "| Variant | Mode | Median seconds | Range | Hits / misses per build |",
             "|---|---|---:|---:|---|" ]
    for value in report["aggregates"]:
        lines.append(f"| {value['id']} | {value['mode']} | {value['median_seconds']:.2f} | "
                     f"{value['range_seconds'][0]:.2f}–{value['range_seconds'][1]:.2f} | "
                     f"{value['cache_hits_each']} / {value['cache_misses_each']} |")
    lines += ["", *[f"- {note}" for note in report["notes"]], "", "All executable outputs are identical."]
    (batch / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    print(f"Report: {batch / 'report.json'}", flush=True)
    return batch / "report.json"


if __name__ == "__main__":
    main()
