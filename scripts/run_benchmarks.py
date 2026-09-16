#!/usr/bin/env python3
"""Run the complete comparison and refresh its report and slides."""
from cache_experiment import main as measure
from publish_results import publish
from worktree_probe import run as probe_paths
from pathlib import Path
import subprocess
import sys

if __name__ == '__main__':
    report = measure()
    probe_paths(report)
    for script in ('manifest_probe.py', 'expression_probe.py'):
        subprocess.run([sys.executable, str(Path(__file__).with_name(script))], check=True)
    publish(report)
    print('\nUpdated RESULTS.md, evidence/isolated/, and presentation.html')
