#!/usr/bin/env python3
"""Package the public demo, scripts and presentation without local artifacts."""

from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = {ROOT / name for name in (
        'README.md', 'presentation.html', 'index.html',
        'presentation-data.json', 'presentation-notes.json', 'benchmark.sh', '.gitignore', '.nojekyll',
        'assets/linkedin-qr.svg', 'assets/repository-qr.svg')}
    ignored = {'.build', '.swiftpm', '__pycache__', '.DS_Store'}
    for folder in ('Baseline', 'Optimized', 'Typecheck'):
        files.update(p for p in (ROOT / folder).rglob('*')
                     if p.is_file() and not ignored.intersection(p.relative_to(ROOT).parts))
    files.update(p for p in (ROOT / 'scripts').iterdir()
                 if p.suffix in {'.py', '.sh'})
    destination = ROOT / 'nslondon-build-time-demo.zip'
    temporary = destination.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, Path('nslondon-build-time-demo') / path.relative_to(ROOT))
    with zipfile.ZipFile(temporary) as archive:
        if archive.testzip():
            raise RuntimeError('Archive verification failed')
        if archive.read('nslondon-build-time-demo/presentation.html') != (ROOT / 'presentation.html').read_bytes():
            raise RuntimeError('Archived slides do not match')
        permissions = archive.getinfo('nslondon-build-time-demo/benchmark.sh').external_attr >> 16
        if not permissions & 0o111:
            raise RuntimeError('benchmark.sh must remain executable')
    temporary.replace(destination)
    print(f'{destination.name}: {len(files)} files, {destination.stat().st_size / 1_000_000:.2f} MB')


if __name__ == '__main__':
    main()
