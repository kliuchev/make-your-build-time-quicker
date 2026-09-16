#!/usr/bin/env python3
"""Check compiler cache identity when an identical file changes its path."""
from pathlib import Path
import json
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def run(report_path):
    report_path=Path(report_path)
    report=json.loads(report_path.read_text())
    directory=report_path.parent/'worktree-probes'
    if directory.exists():
        raise RuntimeError('Worktree probe directory already exists')
    observations=[]
    for trial in range(1,4):
        state=directory/f'trial-{trial}'
        for name in ('slot-01','slot-02'):
            source=state/name/'Shared.swift';source.parent.mkdir(parents=True)
            shutil.copyfile(ROOT/'Optimized/Sources/Shared/Shared.swift',source)
        for mode,slot in [('fill','slot-01'),('same_path','slot-01'),('other_path','slot-02')]:
            command=['swiftc','-c','-module-name','PathProbe','-explicit-module-build',
                     '-module-cache-path',str(state/'modules'),'-cache-compile-job',
                     '-cas-path',str(state/'cas'),'-Rcache-compile-job',
                     str(state/slot/'Shared.swift'),'-o',str(state/'Shared.o')]
            completed=subprocess.run(command,capture_output=True,text=True,check=True)
            output=completed.stdout+completed.stderr
            (state/f'{mode}.log').write_text(output)
            hits=output.count('cache hit for input file');misses=output.count('cache miss for input file')
            expected=(1,0) if mode=='same_path' else (0,1)
            if (hits,misses)!=expected:
                raise RuntimeError(f'Unexpected path probe: {mode}, hits={hits}, misses={misses}')
            observation={'trial':trial,'mode':mode,'hits':hits,'misses':misses,'argv':command,'log_path':str(state/f'{mode}.log')}
            (state/f'{mode}.json').write_text(json.dumps(observation,indent=2)+'\n')
            observations.append(observation)
    report['worktree_probes']=observations
    report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return observations
