// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature23Domain",
    products: [.library(name: "Feature23Domain", targets: ["Feature23Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature23Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
