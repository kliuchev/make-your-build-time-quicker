// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature21Domain",
    products: [.library(name: "Feature21Domain", targets: ["Feature21Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature21Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
