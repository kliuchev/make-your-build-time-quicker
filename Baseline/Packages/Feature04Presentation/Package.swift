// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature04Presentation",
    products: [.library(name: "Feature04Presentation", targets: ["Feature04Presentation"])],
    dependencies: [.package(path: "../Feature04Domain"),
        .package(path: "../Feature04Data")],
    targets: [.target(name: "Feature04Presentation", dependencies: [.product(name: "Feature04Domain", package: "Feature04Domain"), .product(name: "Feature04Data", package: "Feature04Data")])]
)
