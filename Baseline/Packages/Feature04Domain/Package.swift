// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature04Domain",
    products: [.library(name: "Feature04Domain", targets: ["Feature04Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature04Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
