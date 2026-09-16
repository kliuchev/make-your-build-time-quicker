#!/usr/bin/env python3
"""Attach the separately measured slide examples to the presentation data."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATHS = {
    'expression': Path('evidence/expression-probe/report.json'),
    'manifest': Path('evidence/manifest-probe/report.json'),
}


def number(value):
    return f'{value:.2f}'


def load_reports():
    missing = [str(path) for path in REPORT_PATHS.values() if not (ROOT / path).is_file()]
    if missing:
        raise FileNotFoundError(
            'Local measurement reports are missing: ' + ', '.join(missing) +
            '. Run ./benchmark.sh to generate fresh results. The shipped presentation.html works offline.')
    return tuple(json.loads((ROOT / REPORT_PATHS[name]).read_text())
                 for name in ('expression', 'manifest'))


def enrich(data):
    expression, manifest = load_reports()
    if not expression['outputs_equal']:
        raise RuntimeError('Expression outputs must match')
    before = expression['medians']['before_ms']
    after = expression['medians']['after_ms']
    compile_time = manifest['direct_compile']['median_seconds']
    execute_time = manifest['direct_evaluate']['median_seconds']
    dump_time = manifest['swiftpm_end_to_end']['median_seconds']
    sources = [p for p in (ROOT / 'Baseline').rglob('*.swift')
               if p.name != 'Package.swift' and not {'.build', '.swiftpm'}.intersection(p.parts)]
    source_lines = sum(len(p.read_text().splitlines()) for p in sources)
    data['workload'].update(sourceFiles=len(sources), sourceLines=source_lines,
                            sourceLinesExcludeManifests=True)
    data['expressionSources'] = expression['source_text']
    data['microbenchmarkReports'] = {
        'expression': 'evidence/expression-probe/report.json',
        'manifest': 'evidence/manifest-probe/report.json'}
    data['slideValues'].update({
        'expression.repeats': str(expression['repeats']), 'manifest.repeats': str(manifest['repeats']),
        'expression.before': number(before), 'expression.after': number(after),
        'manifest.compile': number(compile_time), 'manifest.dump': number(dump_time),
        'manifest.execute': number(execute_time), 'manifest.serial100': str(round(100 * compile_time)),
        'project.sourceLines': f'{source_lines:,}'})
    data['noteValues'].update({
        'expression.beforeMs': number(before), 'expression.afterMs': number(after),
        'manifest.compileSeconds': number(compile_time),
        'manifest.executeSeconds': number(execute_time),
        'manifest.dumpSeconds': number(dump_time),
        'manifest.serial100Seconds': str(round(100 * compile_time)),
        'project.sourceLines': f'{source_lines:,}'})
    data['experimentNotes']['expression'] = (
        f"Standalone example: {expression['repeats']} repetitions. "
        f"Type checking the whole value() function: {number(before)} → {number(after)} ms. "
        'The only change is a Double annotation on the local x. '
        'Identical Double bit patterns were verified. This is not total build time.')
    data['experimentNotes']['manifest'] = (
        f"Standalone minimal manifest: {manifest['repeats']} repetitions. "
        f"swift package dump-package: {number(dump_time)} s; "
        f"swiftc compile + link: {number(compile_time)} s; "
        f"JSON execution: {number(execute_time)} s. "
        'These are separate measurements; their medians do not necessarily add up. '
        'OS file cache and shipped SDK modules are retained.')
    return data


def report_markdown():
    expression, manifest = load_reports()
    lines = ['', '## Standalone expression example', '',
             'Type-checking time for the **whole function** measured with `-debug-time-function-bodies`, seven repetitions. The only source change is an explicit `: Double` on the local value. Result bit patterns are identical.', '',
             '| Variant | Median, ms | Range, ms |', '|---|---:|---:|']
    for variant, label in [('before', 'Without annotation'), ('after', 'With `: Double`')]:
        lo, hi = expression['ranges_ms'][variant]
        lines.append(f"| {label} | {number(expression['medians'][variant + '_ms'])} | {number(lo)}–{number(hi)} |")
    lines += ['', 'Complete examples: `Typecheck/ExpressionBefore.swift`, `Typecheck/ExpressionAfter.swift`. Commands and logs: `evidence/expression-probe/`. This is a standalone microbenchmark, not a percentage improvement for the whole app.', '',
              '## Minimal Package.swift', '',
              'A four-line manifest with no targets, products or dependencies. Seven repetitions with fresh private caches. The order of direct measurements and SwiftPM runs alternates.', '',
              '| Measurement | Median, s | Range, s |', '|---|---:|---:|']
    for key, label in [('swiftpm_end_to_end', '`swift package dump-package`, end to end'),
                       ('direct_compile', 'Direct swiftc: compile + link'),
                       ('direct_evaluate', 'Direct manifest execution → JSON')]:
        row = manifest[key]; lo, hi = row['range_seconds']
        lines.append(f"| {label} | {number(row['median_seconds'])} | {number(lo)}–{number(hi)} |")
    lines += ['', 'This **does not establish a fixed minimum compilation cost of 0.6 s per manifest**. Multiplying the duration of individual processes illustrates total work, but does not guarantee the wall time of one build: manifests can share caches and be processed in parallel. `dump-package` time also includes CLI startup. Commands and logs: `evidence/manifest-probe/`.', '']
    return '\n'.join(lines)
