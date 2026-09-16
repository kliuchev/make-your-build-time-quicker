#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export auditable measurements and update the offline talk."""
import argparse
import gzip
import json
from pathlib import Path
import shutil
import statistics

from benchmark_environment import environment_labels
from update_presentation import update
from presentation_microbenchmarks import enrich, report_markdown

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def number(value):
    return f'{value:.2f}'


def publish(report_path):
    report_path = Path(report_path).resolve()
    report = json.loads(report_path.read_text())
    if not report.get('outputs_equal'):
        raise RuntimeError('Only a completed, verified matrix can update the presentation')
    aggregates = {(row['id'], row['mode']): row for row in report['aggregates']}
    required = [(name, mode) for name in ('baseline','feature','single','optimized') for mode in (('cold_off','cache_fill','cache_hit') if name in ('single','optimized') else ('cold_off',))]
    if any(key not in aggregates or aggregates[key]['repeats'] != report['repeats'] for key in required):
        raise RuntimeError('The matrix is incomplete')
    def seconds(name, mode='cold_off'): return aggregates[(name,mode)]['median_seconds']
    def gain(before,after):
        delta=100*(1-after/before)
        return f'{abs(delta):.1f}% {"less" if delta >= 0 else "more"} time at the median'
    machine,toolchain=environment_labels(report['swift'],report['jobs'])
    backend=report.get('build_system','native')
    evidence=ROOT/'evidence/isolated'
    evidence.mkdir(parents=True,exist_ok=True)
    for sample in report['samples']:
        destination=evidence/f"trial-{sample['trial']:02d}"/sample['id']/sample['mode']
        destination.mkdir(parents=True,exist_ok=True)
        audit=sample['audit']
        for key,filename in [('command_path','command.json')]:
            shutil.copyfile(audit[key],destination/filename)
        with open(audit['log_path'],'rb') as source, gzip.open(destination/'build.log.gz','wb') as target:
            shutil.copyfileobj(source,target)
        for request in Path(audit['log_path']).parent.glob('build-request-*.json'):
            shutil.copyfile(request,destination/request.name)
        audit['evidence_command']=str((destination/'command.json').relative_to(ROOT))
        audit['evidence_log']=str((destination/'build.log.gz').relative_to(ROOT))
    source_audit=report_path.parent/'source-audit.json'
    if source_audit.exists():shutil.copyfile(source_audit,evidence/'source-audit.json')
    for probe in report.get('typecheck_probes',[]):
        for key in ('log_path','command_path'):
            source=Path(probe.get(key,probe.get('audit',{}).get(key,'')))
            if source.is_file():
                destination=evidence/'probes'/source.relative_to(report_path.parent/'probes')
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source,destination)
    for observation in report.get('worktree_probes',[]):
        log=Path(observation['log_path'])
        destination=evidence/'worktree-probes'/log.relative_to(report_path.parent/'worktree-probes')
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(log,destination)
        shutil.copyfile(log.with_suffix('.json'),destination.with_suffix('.json'))
    write_json(evidence/'report.json',report)
    before=seconds('baseline'); feature=seconds('feature'); single=seconds('single'); typed=seconds('optimized'); cached=seconds('single','cache_hit');combined=seconds('optimized','cache_hit')
    hits=statistics.median(aggregates[('single','cache_hit')]['cache_hits_each'])
    misses=statistics.median(aggregates[('single','cache_hit')]['cache_misses_each'])
    nums={'type.before':single,'type.after':typed,'cache.before':single,'cache.after':cached,'packages.baseline':before,'packages.feature':feature,'packages.single':single,'combined.before':before,'combined.cold':typed,'combined.after':combined}
    values={key:number(value)+( ' s' if key.startswith(('packages.','combined.')) else '') for key,value in nums.items()}
    values.update({'type.gain':gain(single,typed),'packages.gain':gain(before,single),'combined.gain':gain(before,combined),'cache.hits':f'{hits:g} cache hits','cache.misses':f'{misses:g} misses'})
    note_values={'typecheckOnly.beforeSeconds':number(single),'typecheckOnly.afterSeconds':number(typed),'cacheOnly.beforeSeconds':number(single),'cacheOnly.afterSeconds':number(cached),'cacheOnly.hits':f'{hits:g}','packagesOnly.baselineSeconds':number(before),'packagesOnly.featureSeconds':number(feature),'packagesOnly.singleSeconds':number(single),'combined.beforeSeconds':number(before),'combined.afterSeconds':number(combined)}
    def detail(name,mode='cold_off'):
        row=aggregates[(name,mode)];lo,hi=row['range_seconds']
        return f"{name}/{mode}: median {number(row['median_seconds'])} s, range {number(lo)}–{number(hi)} s."
    common=f"{machine}. {toolchain}. Backend: {backend}. Time from command launch to process exit. {report['configuration']}. All build artifacts and module caches are fresh. OS file cache was not purged."
    notes={'type':' '.join([detail('single'),detail('optimized'),common]),'cache':' '.join([detail('single'),detail('single','cache_fill'),detail('single','cache_hit'),common]),'packages':' '.join([detail('baseline'),detail('feature'),detail('single'),common]),'combined':' '.join([detail('baseline'),detail('optimized'),detail('optimized','cache_fill'),detail('optimized','cache_hit'),common])}
    data={'status':'measured','date':report['date'],'machine':machine,'toolchain':toolchain,'backend':backend,'repetitions':report['repeats'],'workload':{'libraryTargets':100,'executableTargets':1,'formatters':64,'termsPerFormatter':120},'slideValues':values,'slideNumbers':nums,'noteValues':note_values,'experimentNotes':notes,'reportPath':'evidence/isolated/report.json'}
    data['slideValues']['build.repeats'] = str(report['repeats'])
    data['noteValues']['build.repeats'] = str(report['repeats'])
    enrich(data)
    write_json(ROOT/'presentation-data.json',data)
    update()
    lines=['# Isolated measurements of each technique','',common,'','## What changes in each comparison','', '| Experiment | Before | After | What stays the same |','|---|---|---|---|','| Type checking | 64 long expressions | 64 functions with short typed parts | One manifest, 101 targets, cache OFF |','| Compilation cache | Cache OFF | Warm CAS ON | Sources, one manifest, flags other than cache settings and cache remarks, fresh build/module caches |','| Packages | 101 manifests | 35, then 1 | Bytes of every Swift source file, 101 targets, cache OFF |','| Combined | 101 manifests, long expressions, cache OFF | 1 manifest, short parts, warm CAS | Program output, 101 targets, toolchain and configuration |','','## Results','', '| Variant | Compiler cache state | Median, s | Range, s | Hits / misses |','|---|---|---:|---:|---:|']
    names={'baseline':'101 manifests, original expressions','feature':'35 manifests, original expressions','single':'1 manifest, original expressions','optimized':'1 manifest, typed parts'}
    modes={'cold_off':'OFF, all private caches empty','cache_fill':'ON, first CAS fill','cache_hit':'ON, only CAS warm'}
    for row in report['aggregates']:
        lines.append(f"| {names[row['id']]} | {modes[row['mode']]} | {number(row['median_seconds'])} | {number(row['range_seconds'][0])}–{number(row['range_seconds'][1])} | {row['cache_hits_each']} / {row['cache_misses_each']} |")
    lines+=['','## How the comparison is controlled','','- Each measurement starts with fresh scratch/build directories, SwiftPM manifest cache, compiler module cache and temporary directories. User DerivedData is not reused.','- Cache fill starts with an empty CAS. Before a cache hit run, all ordinary artifacts are removed while CAS is retained. Source and output paths remain the same for this pair.','- Every variant retains 100 library targets + Demo. Source hashes confirm identical sources in the package-only variants. The type-only difference is confined to Feature01Presentation.','- Demo output is identical across all builds. Commands, actual cache paths, compiler job counts and remarks are available in the JSON and full logs.','- OS file cache is not purged. Prebuilt SDK modules are part of the installed toolchain.','- Synthetic workload: one file with 64 functions, each containing 120 String terms. These results describe this graph; they do not predict a percentage improvement for every iOS app.','- The first cache fill is included in the report but excluded from replay time. A warm CAS is not a fully cold cache.','- Total command time includes process teardown. Hit count is not a wall-time saving; build phases in the raw report are diagnostic.','','## Summary', '',f"Type checking: {number(single)} → {number(typed)} s. {gain(single,typed)}.",f"Compilation cache: {number(single)} → {number(cached)} s. {gain(single,cached)}.",f"Packages: {number(before)} → {number(feature)} → {number(single)} s. {gain(before,single)}.",f"Combined: {number(before)} → {number(combined)} s with a warm CAS. {gain(before,combined)}.",'','Percentages from different techniques cannot be added: on a cache hit, the compiler does not repeat type checking for that job.','','Generated evidence: `evidence/isolated/report.json`, `source-audit.json`, commands and `build.log.gz` for every build. These local files are created by ./benchmark.sh and are not required to view the shipped offline presentation.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n'+report_markdown())
    return data


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('report');args=parser.parse_args();publish(args.report)
