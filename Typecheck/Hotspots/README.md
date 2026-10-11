# Slow, valid type-checking examples

These examples target **hundreds or thousands of milliseconds saved per function**, rather than a large ratio on a tiny baseline. Both versions compile with the default solver limits and produce the same result. They were measured on **Xcode 27.1 beta, build 27A9269 / Apple Swift 6.4**, on Mac17,9 · arm64 · 24 GB RAM, on October 11, 2026.

The recorded medians, ranges, individual samples, compiler version and source hashes are in [measurements.json](measurements.json). The primary series uses **Swift 6 language mode**, seven repetitions. A second series in Swift 5 mode is included for comparison. These are **type-checking times for the complete `value()` function**, including all statements introduced by splitting; they are not runtime or full application build times.

| Example | Before, ms | After, ms | Saved, ms | Speedup |
|---|---:|---:|---:|---:|
| Nine factors + `: Double` | 1002.98 | 4.54 | 998.44 | 221× |
| Typed generic closure | 2096.05 | 1.53 | 2094.52 | 1370× |
| Typed Base64 string | 552.86 | 7.78 | 545.08 | 71× |

| Example | Before range, ms | After range, ms |
|---|---:|---:|
| Nine factors + `: Double` | 910.48–1216.15 | 4.21–5.60 |
| Typed generic closure | 1986.31–2162.45 | 1.43–3.14 |
| Typed Base64 string | 548.37–554.95 | 7.67–8.74 |

## Reproduce

```sh
python3 scripts/typecheck_hotspots.py --repeats 7
python3 scripts/refresh_microbenchmarks.py --expression-only --hotspots
```

The runner requires Xcode **27.1 or newer**, selected via `xcode-select` or `DEVELOPER_DIR`. It saves commands, source snapshots, stdout/stderr logs and fresh measurements under `evidence/typecheck-hotspots/`. It checks actual runtime output independently from timing. The second command updates only expression content in the slides; the existing full-build and manifest measurements retain their original dates and toolchains.

To compare Swift 5 language mode without overwriting the primary report:

```sh
python3 scripts/typecheck_hotspots.py --swift-version 5 --repeats 7 \
  --output-dir evidence/typecheck-hotspots-swift5
```

Each timed run starts a fresh compiler process and private empty module cache. Compilation caching is off; OS page caches and SDK prebuilts are retained. Before/after order alternates. No solver thresholds are raised and no performance heuristics are disabled. Future compilers may make these examples faster; rerun instead of assuming the recorded ratios still apply.

## 1. Nine factors: one type annotation

The complete code fits on the existing presentation slide:

```swift
func value() -> Double {
    let x = 1 * 2 * 3 * 4
        * 5 * 6 * 7 * 8 * 9.5
    return x
}
```

```swift
func value() -> Double {
    let x: Double = 1 * 2 * 3 * 4
        * 5 * 6 * 7 * 8 * 9.5
    return x
}
```

The integer literals and overloaded `*` operators precede the only floating-point literal. An explicit local type provides context for the whole expression. The return type alone does not provide that context to the preceding local initializer. This is a deliberately synthetic stress test, scaled from the repository's old seven-factor example. Runtime verification checks both `383040.0` and the exact Double bit pattern.

Complete sources: [before](../ExpressionBefore.swift), [after](../ExpressionAfter.swift).

## 2. Generic key path API and optional enum comparisons

The slow function:

```swift
func value(_ model: Model) -> Bool {
    matches(model, key: \.primary) {
        $0.primary == .active &&
        $0.secondary == .active &&
        $0.fallback == .active
    }
}
```

Give the closure explicit parameter and result types:

```swift
func value(_ model: Model) -> Bool {
    matches(model, key: \.primary) { (item: Model) -> Bool in
        item.primary == .active &&
        item.secondary == .active &&
        item.fallback == .active
    }
}
```

`Model` contains two nonoptional enum properties and one optional property. `matches<Field, Item>` accepts an item, `KeyPath<Item, Field>` and `(Item) -> Bool`, then evaluates the predicate. This small stand-in for a generic API exposes a remaining inference problem involving a key path, shorthand enum cases, optional promotion and chained comparisons. Every one of the 12 combinations of enum/optional values is checked against the expected Boolean result.

Adapted from the compiler's [rdar180205468 regression test](https://github.com/swiftlang/swift/blob/d8754319df83d6e93189337b645180f73038cb97/validation-test/Sema/type_checker_perf/slow/rdar180205468.swift). The original helper is empty; this version evaluates the predicate to make output equivalence testable. The complete setup is included in both [before](PredicateBefore.swift) and [after](PredicateAfter.swift), so no external dependency or hidden overload is required.

## 3. Foundation initializer overloads and string concatenation

The slow version uses the real `Foundation.Data`:

```swift
func value() -> Data? {
    return Data(base64Encoded:
        "S" + "G" + "V" + "s" + "b" + "G8=", options: [])
}
```

Extract an explicitly typed intermediate value:

```swift
func value() -> Data? {
    let encoded: String =
        "S" + "G" + "V" + "s" + "b" + "G8="
    return Data(base64Encoded: encoded, options: [])
}
```

This combines a concatenation with overloaded `Data(base64Encoded:options:)` initializers accepting `String` or `Data`. Giving the concatenation a `String` context reduces the inference work before resolving the initializer. Both variants decode the valid payload to the five bytes of `Hello`, checked with a precondition.

Adapted from the compiler's [rdar180902902 scaling test](https://github.com/swiftlang/swift/blob/0c3bc9f591610887cb8bcf16cc16ac40f9669fc4/validation-test/Sema/type_checker_perf/slow/rdar180902902.swift.gyb), which documents the interaction between initializer overloads and collection `+` overloads. This version uses Foundation, rather than a stub `Data` type. Sources: [before](Base64Before.swift), [after](Base64After.swift).

## Why these cases were selected

The repository's old slide example measured 22.52 → 4.09 ms. Extending it by only two factors moves it into the hundreds-of-milliseconds range on this toolchain. The other two cases cover generic closures and framework overloads rather than more arithmetic.

The upstream `slow` directory also contains deliberately invalid programs, tests that lower the solver's limit, and examples that Swift 6.4 has already made fast. Those are useful compiler tests, but they should not be presented as a successful build before/after comparison. These examples were independently compiled and executed with ordinary limits.

The measurement flag is described in the compiler's [performance guide](https://github.com/swiftlang/swift/blob/main/docs/CompilerPerformance.md). The relevant Swift 6.4 changes are described by the compiler team in [Recent improvements to the type checker](https://forums.swift.org/t/recent-improvements-to-the-type-checker/87048).
