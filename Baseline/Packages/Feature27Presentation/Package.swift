// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature27Presentation",
    products: [.library(name: "Feature27Presentation", targets: ["Feature27Presentation"])],
    dependencies: [.package(path: "../Feature27Domain"),
        .package(path: "../Feature27Data")],
    targets: [.target(name: "Feature27Presentation", dependencies: [.product(name: "Feature27Domain", package: "Feature27Domain"), .product(name: "Feature27Data", package: "Feature27Data")])]
)
