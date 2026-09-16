// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature13Domain",
    products: [.library(name: "Feature13Domain", targets: ["Feature13Domain"])],
    dependencies: [.package(path: "../Shared")],
    targets: [.target(name: "Feature13Domain", dependencies: [.product(name: "Shared", package: "Shared")])]
)
