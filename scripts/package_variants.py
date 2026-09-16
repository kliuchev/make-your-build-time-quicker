#!/usr/bin/env python3
"""Create the package-only comparison without changing target source bytes."""

from pathlib import Path
import shutil


def create_feature_merged(source: Path, destination: Path) -> None:
    (destination / "Packages").mkdir(parents=True)
    shutil.copytree(source / "Packages/Shared", destination / "Packages/Shared")
    shutil.copytree(source / "Sources/Demo", destination / "Sources/Demo")
    packages = []
    app_dependencies = []
    for number in range(1, 34):
        feature = f"Feature{number:02d}"
        domain, data, presentation = (f"{feature}{layer}" for layer in ("Domain", "Data", "Presentation"))
        package = destination / "Packages" / feature
        for target in (domain, data, presentation):
            target_source = source / "Packages" / target / "Sources" / target / f"{target}.swift"
            target_dest = package / "Sources" / target / f"{target}.swift"
            target_dest.parent.mkdir(parents=True)
            shutil.copyfile(target_source, target_dest)
        (package / "Package.swift").write_text(f'''// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "{feature}",
    products: [.library(name: "{presentation}", targets: ["{presentation}"])],
    dependencies: [.package(path: "../Shared")],
    targets: [
        .target(name: "{domain}", dependencies: [.product(name: "Shared", package: "Shared")]),
        .target(name: "{data}", dependencies: ["{domain}"]),
        .target(name: "{presentation}", dependencies: ["{domain}", "{data}"])
    ]
)
''', encoding="utf-8")
        packages.append(f'.package(path: "Packages/{feature}")')
        app_dependencies.append(f'.product(name: "{presentation}", package: "{feature}")')
    (destination / "Package.swift").write_text(f'''// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "BuildTimeFeatureMerged",
    products: [.executable(name: "Demo", targets: ["Demo"])],
    dependencies: [{", ".join(packages)}],
    targets: [.executableTarget(name: "Demo", dependencies: [{", ".join(app_dependencies)}])]
)
''', encoding="utf-8")
