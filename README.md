# Make your build time quicker

**NSLondon · Sviatoslav Kliuchev**  
Lead Software Engineer at JPMorgan Personal Investing · [LinkedIn](https://www.linkedin.com/in/sviatoslav-kliuchev-50034097/)

Faster builds mean shorter AI feedback loops, quicker CI feedback and less time watching a progress bar. This talk explores type checking, compilation caching, package structure and build tooling—with reproducible Swift examples.

**[View the slides](https://kliuchev.github.io/make-your-build-time-quicker/)** · **[Download the demo ZIP](https://github.com/kliuchev/make-your-build-time-quicker/archive/refs/heads/main.zip)**

## Try it

Clone the repository, or download and extract the ZIP:

```sh
git clone https://github.com/kliuchev/make-your-build-time-quicker.git
cd make-your-build-time-quicker
./benchmark.sh
```

**Requirements:** macOS, a full Xcode installation selected as the command line toolchain, Python 3.9+ and a few GB of free space for temporary builds. Verified with **Xcode 27 / Swift 6.4**. No third-party Python packages are needed.

The default is **3 repetitions and 8 parallel jobs**. Adjust these for your machine:

```sh
./benchmark.sh --jobs 4 --repeats 5
```

The script runs the controlled build comparisons, checks that program outputs match, and measures the small expression, manifest and worktree examples. It generates **`RESULTS.md`** with your timings and refreshes the local slides.

Reports, evidence and temporary builds are local outputs excluded from Git: `RESULTS.md`, `evidence/` and `.benchmark-runs/`.

## Recorded results

Full-build medians from three runs on **Mac17,9 · arm64 · 24 GB RAM**, using **Xcode 27.0 / Swift 6.4**, Swift Build, Debug without DWARF and 8 jobs. Recorded on September 16, 2026.

| Comparison | Before | After | What changes |
|---|---:|---:|---|
| Type checking only | 9.28 s | 6.44 s | Explicit intermediate types; cache off |
| Compile cache only | 9.28 s | 4.75 s | Reuse a populated CAS; identical sources |
| Packages only | 52.63 s | 23.01 s → 9.28 s | 101 → 35 → 1 manifest |
| Combined | 52.63 s | 6.44 s / 4.76 s | Types + packages, with empty / warm compiler cache |

The cache-only replay recorded **204 hits and 0 misses**. Exact values, ranges and measurement conditions are embedded in [presentation-data.json](presentation-data.json) and the slide notes.

**This is a synthetic workload.** It deliberately combines many small packages with 64 long formatting functions in one module. These figures demonstrate the mechanisms; your project’s gains depend on its bottlenecks. Individual percentage improvements cannot be added together.

## What is being compared?

- **Baseline:** 33 features × Domain, Data and Presentation, plus Shared. That is 100 local dependency packages and one root executable package.
- **Optimized:** one manifest, the same 100 library targets and Demo executable. Long expressions in Feature01Presentation are split into typed intermediate values.
- **Intermediate variants:** generated during the run to isolate package structure from source changes—one package per feature, then one manifest with the original sources.

Fewer manifests reduce the work needed to compile and run `Package.swift` files, load package descriptions and prepare the graph. **Targets remain separate modules.** The demo has no network dependencies.

### Fresh builds and the cache

Every measurement starts with fresh build/DerivedData directories, manifest caches, module caches and temporary directories. User DerivedData is not reused.

For cache replay, **only the previously populated CAS remains warm**. Filling it is measured separately. A replay is therefore a clean rebuild with a warm compilation cache, not a completely cold cache.

The macOS file cache is not purged, and prebuilt SDK modules remain part of the installed toolchain. The main metric is elapsed command time.

## Explore the repository

| Path | Contents |
|---|---|
| `Baseline/` | Many packages and long expressions |
| `Optimized/` | One manifest and explicit intermediate types |
| `Typecheck/` | Standalone type-checking examples |
| `scripts/` | Benchmark runner, probes, project generator and slide tools |
| `presentation.html` | Self-contained slides; works offline |
| `presentation-data.json` | Recorded measurements used by the slides |
| `assets/` | Presentation assets |

Open `presentation.html` in a browser. Use **← / →** or the buttons to navigate, **N** for notes and **F** for fullscreen. The deck uses Apple system fonts on macOS, with system fallbacks elsewhere.

For branch workflows, `scripts/worktree-slot.sh` maintains stable worktree paths. Cache reuse across different directories requires matching inputs and appropriate path normalization; it is not automatic.

<details>
<summary>Technical sources</summary>

- [Swift 6.4 type checker improvements](https://forums.swift.org/t/recent-improvements-to-the-type-checker/87048)
- [Apple: Xcode build settings](https://developer.apple.com/documentation/xcode/build-settings-reference)
- [SwiftPM: manifest loading](https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageLoading/ManifestLoader.swift)
- [SwiftPM: targets and modules](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html#target)
- [Tuist: Xcode cache and path mapping](https://tuist.dev/en/docs/guides/features/cache/xcode-cache)
- [Bazel: remote caching](https://bazel.build/remote/caching)

</details>
