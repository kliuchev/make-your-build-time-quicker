#!/usr/bin/env python3
"""Refresh the small examples without running the full build matrix again."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from presentation_microbenchmarks import REPORT_PATHS, enrich, enrich_expression, report_markdown

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expression-only', action='store_true',
                        help='Refresh the expression slide without requiring full-build or manifest reports')
    parser.add_argument('--hotspots', action='store_true',
                        help='Use the product case from the latest hotspot suite (with --expression-only)')
    args = parser.parse_args()
    if args.hotspots and not args.expression_only:
        parser.error('--hotspots requires --expression-only')
    path = ROOT / 'presentation-data.json'
    if args.expression_only:
        hotspots = ROOT / 'evidence/typecheck-hotspots/report.json'
        if args.hotspots:
            suite = json.loads(hotspots.read_text())
            expression = {**suite['cases']['product'], **{key: suite[key] for key in (
                'date', 'xcode', 'swift', 'language_mode', 'machine', 'repeats')}}
        else:
            expression = json.loads((ROOT / REPORT_PATHS['expression']).read_text())
        data = enrich_expression(json.loads(path.read_text()), expression)
        if hotspots.is_file():
            suite = json.loads(hotspots.read_text())
            data['typecheckHotspots'] = {
                **{key: suite[key] for key in ('date', 'xcode', 'language_mode', 'repeats')},
                'reportPath': 'Typecheck/Hotspots/measurements.json',
                'cases': {name: {key: case[key] for key in (
                    'title', 'paths', 'medians', 'ranges_ms', 'speedup', 'saved_ms', 'outputs_equal')}
                    for name, case in suite['cases'].items()}}
        if args.hotspots:
            data['microbenchmarkReports']['expression'] = 'evidence/typecheck-hotspots/report.json (product case)'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_presentation.py')], check=True)
        return
    results = ROOT / 'RESULTS.md'
    required = [path, results] + [ROOT / report for report in REPORT_PATHS.values()]
    missing = [str(item.relative_to(ROOT)) for item in required if not item.is_file()]
    if missing:
        raise SystemExit(
            'Cannot refresh: local result files are missing: ' + ', '.join(missing) +
            '.\nRun ./benchmark.sh to generate fresh measurements and RESULTS.md. '
            'The shipped presentation.html works offline.')
    data = enrich(json.loads(path.read_text()))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    prefix = results.read_text().split('\n## Standalone expression example', 1)[0]
    results.write_text(prefix.rstrip() + '\n' + report_markdown())
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_presentation.py')], check=True)


if __name__ == '__main__':
    main()
