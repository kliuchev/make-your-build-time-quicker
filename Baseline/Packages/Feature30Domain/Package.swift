// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature30Domain",
    products: [.library(name: "Feature30Domain", targets: ["Feature30Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature30Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
