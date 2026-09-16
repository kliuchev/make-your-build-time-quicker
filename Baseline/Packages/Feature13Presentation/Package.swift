// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature13Presentation",
    products: [.library(name: "Feature13Presentation", targets: ["Feature13Presentation"])],
    dependencies: [.package(path: "../Feature13Domain"),
        .package(path: "../Feature13Data")],
    targets: [.target(name: "Feature13Presentation", dependencies: [.product(name: "Feature13Domain", package: "Feature13Domain"), .product(name: "Feature13Data", package: "Feature13Data")])]
)
