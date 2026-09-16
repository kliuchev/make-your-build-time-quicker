// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature14Domain",
    products: [.library(name: "Feature14Domain", targets: ["Feature14Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature14Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
