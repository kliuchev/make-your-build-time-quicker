// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature09Presentation",
    products: [.library(name: "Feature09Presentation", targets: ["Feature09Presentation"])],
    dependencies: [.package(path: "../Feature09Domain"),
        .package(path: "../Feature09Data")],
    targets: [.target(name: "Feature09Presentation", dependencies: [.product(name: "Feature09Domain", package: "Feature09Domain"), .product(name: "Feature09Data", package: "Feature09Data")])]
)
