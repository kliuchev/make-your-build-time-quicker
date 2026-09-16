#!/usr/bin/env python3
"""Refresh the small examples without running the full build matrix again."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from presentation_microbenchmarks import REPORT_PATHS, enrich, report_markdown

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    path = ROOT / 'presentation-data.json'
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
