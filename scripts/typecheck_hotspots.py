#!/usr/bin/env python3
"""Measure valid, slow Swift expressions and verify equivalent runtime results.

Only the selected value() body is timed, including all intermediate statements.
No solver thresholds or performance heuristics are changed.
"""

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

from expression_probe import ROOT, run, write_json


CASES = {
    "product": {
        "title": "Nine factors, with a floating-point literal last",
        "paths": ("Typecheck/ExpressionBefore.swift", "Typecheck/ExpressionAfter.swift"),
        "change": "Give the local value an explicit Double type.",
        "origin": "Scaled version of the repository's original expression example.",
        "main": 'precondition(value() == 383040.0)\nprint(value().bitPattern)\n',
    },
    "predicate": {
        "title": "Generic key path API with optional enum comparisons",
        "paths": ("Typecheck/Hotspots/PredicateBefore.swift", "Typecheck/Hotspots/PredicateAfter.swift"),
        "change": "Annotate the closure parameter as Model and its return type as Bool.",
        "origin": "Adapted from Swift's rdar180205468 regression test; matches() executes the predicate for verification.",
        "source_url": "https://github.com/swiftlang/swift/blob/d8754319df83d6e93189337b645180f73038cb97/validation-test/Sema/type_checker_perf/slow/rdar180205468.swift",
        "upstream_blob_sha": "6a1bf6b050c758ad67fcde14bbc18c17984ed327",
        "main": '''let statuses: [Status] = [.active, .paused]
let optionalStatuses: [Status?] = [.active, .paused, nil]
for primary in statuses {
    for secondary in optionalStatuses {
        for fallback in statuses {
            let model = Model(primary: primary, secondary: secondary, fallback: fallback)
            let expected = primary == .active && secondary == .active && fallback == .active
            precondition(value(model) == expected)
            print(value(model))
        }
    }
}
''',
    },
    "base64": {
        "title": "String concatenation inside an overloaded Foundation initializer",
        "paths": ("Typecheck/Hotspots/Base64Before.swift", "Typecheck/Hotspots/Base64After.swift"),
        "change": "Extract the concatenation into a String-typed local value.",
        "origin": "Adapted from the rdar180902902 scaling test, using actual Foundation.Data and a valid Hello payload.",
        "source_url": "https://github.com/swiftlang/swift/blob/0c3bc9f591610887cb8bcf16cc16ac40f9669fc4/validation-test/Sema/type_checker_perf/slow/rdar180902902.swift.gyb",
        "upstream_blob_sha": "ac8f8865aa65a95b93cbb312cffe5a7b0dcceea9",
        "main": '''import Foundation
precondition(value() == Data("Hello".utf8))
print(Array(value()!))
''',
    },
}


def version_tuple(value):
    numbers = tuple(int(x) for x in value.split("."))
    return numbers + (0,) * (3 - len(numbers))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--swift-version", choices=("5", "6"), default="6")
    parser.add_argument("--require-xcode", default="27.1")
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/typecheck-hotspots"))
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("repeats must be positive")
    xcode = subprocess.check_output(["xcodebuild", "-version"], text=True).strip()
    match = re.search(r"Xcode ([\d.]+)", xcode)
    if not match or version_tuple(match[1]) < version_tuple(args.require_xcode):
        parser.error("Requires Xcode " + args.require_xcode + " or newer; selected: " + xcode)
    compiler = subprocess.check_output(["xcrun", "--find", "swiftc"], text=True).strip()
    evidence = ROOT / args.output_dir
    evidence.mkdir(parents=True, exist_ok=True)
    batch = evidence / (time.strftime("%Y%m%d-%H%M%S") + "-" + str(os.getpid()))
    batch.mkdir()
    report = {
        "method": "whole-function-typechecking-v1", "date": time.strftime("%Y-%m-%d"),
        "xcode": xcode, "swift": subprocess.check_output([compiler, "--version"], text=True).strip(),
        "developer_dir": os.environ.get("DEVELOPER_DIR") or subprocess.check_output(["xcode-select", "-p"], text=True).strip(),
        "language_mode": args.swift_version, "machine": platform.platform(),
        "repeats": args.repeats, "cases": {},
        "notes": [
            "Milliseconds are for the complete value() function, including all statements after splitting.",
            "Each sample uses a fresh compiler process and private empty module cache; compilation caching is off.",
            "Variant order alternates. OS page caches and SDK prebuilts are retained.",
            "Wall time is recorded separately and includes compiler startup and imports.",
            "No altered solver limits, disabled heuristics, or deliberately invalid expressions.",
            "Timings vary with hardware and compiler revisions; future compilers may fix these cases.",
        ],
    }
    for name, case in CASES.items():
        directory = batch / name
        directory.mkdir()
        texts = {variant: (ROOT / path).read_text() for variant, path in zip(("before", "after"), case["paths"])}
        snapshots = {}
        for variant, source in texts.items():
            snapshots[variant] = directory / (variant + ".swift")
            snapshots[variant].write_text(source)
        samples = []
        for trial in range(1, args.repeats + 1):
            for variant in (("before", "after") if trial % 2 else ("after", "before")):
                sample_dir = directory / ("trial-{:02d}-{}".format(trial, variant))
                sample_dir.mkdir()
                command = [compiler, "-swift-version", args.swift_version, "-typecheck",
                           "-module-cache-path", str(sample_dir / "modules"),
                           "-Xfrontend", "-debug-time-function-bodies", str(snapshots[variant])]
                seconds, _, log = run(command, sample_dir / "typecheck")
                times = re.findall(r"(?m)^([\d.]+)ms\s[^\n]*global function[^\n]*\.value(?:\(|@)", log)
                if len(times) != 1:
                    raise RuntimeError("Expected exactly one value() body timing: " + log)
                sample = {"trial": trial, "variant": variant, "function_ms": float(times[0]),
                          "wall_seconds": seconds}
                samples.append(sample)
                print(name, trial, variant, sample["function_ms"], "ms", flush=True)
        outputs = {}
        for variant in ("before", "after"):
            runtime = directory / ("runtime-" + variant)
            runtime.mkdir()
            main_source = runtime / "main.swift"
            main_source.write_text(case["main"])
            executable = runtime / "verify"
            command = [compiler, "-swift-version", args.swift_version, "-module-cache-path", str(runtime / "modules"),
                       str(snapshots[variant]), str(main_source), "-o", str(executable)]
            run(command, runtime / "compile")
            _, stdout, _ = run([str(executable)], runtime / "execute")
            outputs[variant] = stdout.strip()
        if outputs["before"] != outputs["after"]:
            raise RuntimeError(name + ": runtime outputs differ")
        values = {variant: [x["function_ms"] for x in samples if x["variant"] == variant]
                  for variant in ("before", "after")}
        medians = {variant + "_ms": statistics.median(v) for variant, v in values.items()}
        report["cases"][name] = {
            **{key: value for key, value in case.items() if key != "main"},
            "source_text": texts, "source_sha256": {key: hashlib.sha256(value.encode()).hexdigest() for key, value in texts.items()},
            "samples": samples, "medians": medians,
            "ranges_ms": {key: [min(v), max(v)] for key, v in values.items()},
            "speedup": medians["before_ms"] / medians["after_ms"],
            "saved_ms": medians["before_ms"] - medians["after_ms"],
            "outputs_equal": True, "output": outputs["before"],
        }
        write_json(batch / "report.json", report)
    write_json(evidence / "report.json", report)
    print("Report:", evidence / "report.json")
    for name, case in report["cases"].items():
        print(name, case["medians"], "speedup", round(case["speedup"], 1))


if __name__ == "__main__":
    main()
