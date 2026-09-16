#!/usr/bin/env python3
"""Generate the two deterministic SwiftPM graphs used by the talk."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Baseline"
FAST = ROOT / "Optimized"
TYPECHECK_FUNCTIONS = 64


def label_body(optimized: bool, indent: str) -> str:
    if not optimized:
        lines = ['let label = ' + ' + '.join(['model.title'] * 120)]
    else:
        lines = [f'let chunk{n}: String = ' + ' + '.join(['model.title'] * 10) for n in range(1, 13)]
        lines.append('let label: String = ' + ' + '.join(f'chunk{n}' for n in range(1, 13)))
    lines.append('return "\\(label):\\(model.score)"')
    return ('\n' + indent).join(lines)


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def manifest(name: str, dependencies: list[tuple[str, str]], target_dependencies: list[str]) -> str:
    packages = ",\n        ".join(f'.package(path: "{path}")' for _, path in dependencies)
    target_deps = ", ".join(f'.product(name: "{item}", package: "{item}")' for item in target_dependencies)
    return f'''// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "{name}",
    products: [.library(name: "{name}", targets: ["{name}"])],
    dependencies: [{packages}],
    targets: [.target(name: "{name}", dependencies: [{target_deps}])]
)
'''


def source(name: str, layer: str, feature: int, optimized: bool) -> str:
    if layer == "Domain":
        return f'''import Shared

public struct {name}Model: Sendable {{
    public let id: Int
    public let title: String

    public init(id: Int, title: String) {{
        self.id = id
        self.title = title
    }}

    public var score: Int {{ SharedScore.value(id) + {feature} }}
}}
'''
    if layer == "Data":
        return f'''import {feature_name(feature, "Domain")}

public enum {name}Repository {{
    public static func load(_ id: Int) -> {feature_name(feature, "Domain")}Model {{
        {feature_name(feature, "Domain")}Model(id: id, title: "Feature {feature}")
    }}
}}
'''
    domain = feature_name(feature, "Domain")
    data = feature_name(feature, "Data")
    extra = ""
    body = 'return "\\(model.title):\\(model.score)"'
    if feature == 1:
        calls = ',\n            '.join(f'format{n:02d}(model)' for n in range(TYPECHECK_FUNCTIONS))
        body = f'let labels: [String] = [\n            {calls}\n        ]\n        return labels.joined(separator: "|")'
        extra = '\n    // Repeated formatting makes type-checking cost measurable.\n'
        for n in range(TYPECHECK_FUNCTIONS):
            extra += f'''    private static func format{n:02d}(_ model: {domain}Model) -> String {{
        {label_body(optimized, '        ')}
    }}

'''
    return f'''import {domain}
import {data}

public enum {name}Screen {{
    public static func render(_ id: Int) -> String {{
        let model: {domain}Model = {data}Repository.load(id)
        {body}
    }}
{extra}
}}
'''


def feature_name(number: int, layer: str) -> str:
    return f"Feature{number:02d}{layer}"


def generate() -> None:
    write(BASE / "Packages/Shared/Package.swift", manifest("Shared", [], []))
    shared = '''public enum SharedScore {
    public static func value(_ input: Int) -> Int { input * 3 + 7 }
}
'''
    write(BASE / "Packages/Shared/Sources/Shared/Shared.swift", shared)
    write(FAST / "Sources/Shared/Shared.swift", shared)

    targets = ['.target(name: "Shared")']
    for number in range(1, 34):
        domain = feature_name(number, "Domain")
        data = feature_name(number, "Data")
        presentation = feature_name(number, "Presentation")
        specs = [
            (domain, "Domain", [("Shared", "../Shared")], ["Shared"], ['"Shared"']),
            (data, "Data", [(domain, f"../{domain}")], [domain], [f'"{domain}"']),
            (presentation, "Presentation", [(domain, f"../{domain}"), (data, f"../{data}")], [domain, data], [f'"{domain}"', f'"{data}"']),
        ]
        for name, layer, deps, product_deps, target_deps in specs:
            package = BASE / "Packages" / name
            write(package / "Package.swift", manifest(name, deps, product_deps))
            write(package / "Sources" / name / f"{name}.swift", source(name, layer, number, False))
            write(FAST / "Sources" / name / f"{name}.swift", source(name, layer, number, True))
            targets.append(f'.target(name: "{name}", dependencies: [{", ".join(target_deps)}])')

    presentations = [feature_name(n, "Presentation") for n in range(1, 34)]
    calls = "\n".join(f'    print({name}Screen.render({n}))' for n, name in enumerate(presentations, 1))
    imports = "\n".join(f'import {name}' for name in presentations)
    app = f'{imports}\n\n@main struct Demo {{\n    static func main() {{\n{calls}\n    }}\n}}\n'
    write(BASE / "Sources/Demo/main.swift", app)
    write(FAST / "Sources/Demo/main.swift", app)
    baseline_deps = ",\n        ".join(f'.package(path: "Packages/{name}")' for name in presentations)
    baseline_products = ", ".join(f'.product(name: "{name}", package: "{name}")' for name in presentations)
    write(BASE / "Package.swift", f'''// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "BuildTimeBaseline",
    products: [.executable(name: "Demo", targets: ["Demo"])],
    dependencies: [{baseline_deps}],
    targets: [.executableTarget(name: "Demo", dependencies: [{baseline_products}])]
)
''')
    app_dependencies = ", ".join(f'"{name}"' for name in presentations)
    fast_targets = ",\n        ".join(targets + [f'.executableTarget(name: "Demo", dependencies: [{app_dependencies}])'])
    write(FAST / "Package.swift", f'''// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "BuildTimeOptimized",
    products: [.executable(name: "Demo", targets: ["Demo"])],
    targets: [
        {fast_targets}
    ]
)
''')
    for name, optimized in (("Baseline", False), ("Optimized", True)):
        value = 'struct Model { let title: String; let score: Int }\n\n'
        for n in range(TYPECHECK_FUNCTIONS):
            value += f'func format{n:02d}(_ model: Model) -> String {{\n    {label_body(optimized, "    ")}\n}}\n\n'
        calls = ', '.join(f'format{n:02d}(model)' for n in range(TYPECHECK_FUNCTIONS))
        value += f'func render(_ model: Model) -> String {{\n    let labels: [String] = [{calls}]\n    return labels.joined(separator: "|")\n}}\n'
        write(ROOT / "Typecheck" / f"{name}.swift", value)


if __name__ == "__main__":
    generate()
