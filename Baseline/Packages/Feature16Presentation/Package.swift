// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature16Presentation",
    products: [.library(name: "Feature16Presentation", targets: ["Feature16Presentation"])],
    dependencies: [.package(path: "../Feature16Domain"),
        .package(path: "../Feature16Data")],
    targets: [.target(name: "Feature16Presentation", dependencies: [.product(name: "Feature16Domain", package: "Feature16Domain"), .product(name: "Feature16Data", package: "Feature16Data")])]
)
